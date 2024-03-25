from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from trial.models import Workout, Exercises, ExSets
from trial.forms import SessionForm, UpdateExercisesFormset, ExerciseForm, SetFormset


@login_required
def view_all_sessions(request):
    sessions_data = Workout.objects.filter(member=request.user)
    # sessions_data = Workout.objects.all().order_by('id')
    return render(request, 'all_sessions.html', {'sessions_data': sessions_data})


def log_session(request):
    new_session = Workout.objects.create(member=request.user)
    return HttpResponseRedirect(f'/update-session/{new_session.id}')


def update_session(request, session_id):
    session = Workout.objects.get(id=session_id)
    if request.method == 'POST':
        session_form = SessionForm(request.POST, instance=session)
        formset = UpdateExercisesFormset(request.POST, instance=session)
        if formset.is_valid() and session_form.is_valid():
            session_form.save()
            formset.save()
            return redirect('view_session', session_id=session_id)
    else:
        formset = UpdateExercisesFormset(instance=session)
        session_form = SessionForm(instance=session)
    return render(request, 'log_session.html', {
        'formset': formset,
        'session_id': session.id,
        'session_form': session_form
    })


def add_exercise(request, session_id):
    new_exercise = Exercises.objects.create(workout_id=session_id)
    return HttpResponseRedirect(f'/add-sets/{new_exercise.id}')


def add_sets(request, exercise_id):
    new_exercise = Exercises.objects.get(id=exercise_id)
    template = 'add_sets.html'
    if request.method == 'POST':
        exercise = ExerciseForm(request.POST)
        formset = SetFormset(request.POST)
        if formset.is_valid() and exercise.is_valid():
            ex_name = exercise.cleaned_data['ex_name']
            Exercises.objects.filter(id=exercise_id).update(ex_name=ex_name)
            for form in formset:
                ex_weight = form.cleaned_data.get('ex_weight')
                ex_reps = form.cleaned_data.get('ex_reps')
                if ex_weight and ex_reps:
                    ExSets.objects.create(exercise=new_exercise, ex_weight=ex_weight, ex_reps=ex_reps)
                if ex_weight and not ex_reps:
                    ExSets.objects.create(exercise=new_exercise, ex_weight=ex_weight, ex_reps=0)
                if ex_reps and not ex_weight:
                    ExSets.objects.create(exercise=new_exercise, ex_weight=0, ex_reps=ex_reps)
                else:
                    ExSets.objects.create(exercise=new_exercise, ex_weight=0, ex_reps=0)
            return redirect(f'/update-session/{new_exercise.workout_id}')
    elif request.method == 'GET':
        formset = SetFormset()
        exercise = ExerciseForm(request.GET)
    return render(request, template, {
        'exercise': exercise,
        'formset': formset,
    })


def view_session(request, session_id):
    session_data = Workout.objects.get(id=session_id)
    exercise_data = Exercises.objects.filter(workout=session_data)
    dict = {}
    for ex in exercise_data:
        sets = ExSets.objects.filter(exercise=ex)
        for rep in sets:
            if ex.ex_name not in dict:
                dict[ex.ex_name] = [[[rep.ex_weight], [rep.ex_reps], [rep.exercise_id]]]
            else:
                dict[ex.ex_name].append([[rep.ex_weight], [rep.ex_reps], [rep.exercise_id]])
    template = 'view_session.html' if exercise_data else 'empty_view.html'
    return render(request, template, {
        'session_data': session_data,
        'exercise_data': exercise_data,
        'session_id': session_id,
        'dict': dict
    })

def exercise_del(request, exercise_id):
    exercise = Exercises.objects.get(id=exercise_id)
    if request.method == 'POST':
        exercise.delete()
        return redirect('view_session', session_id=exercise.workout_id)
    return render(request, 'delete_ex.html', {'exercise': exercise})


def session_del(request, session_id):
    session = Workout.objects.get(id=session_id)
    if request.method == 'POST':
        session.delete()
        return redirect('/')
    return render(request, 'delete_session.html', {'session': session})
