from django import forms
from django.forms import TextInput, modelformset_factory, inlineformset_factory, NumberInput, BaseInlineFormSet, \
    IntegerField, ModelForm
from trial.models import Workout, Exercises, ExSets
from django.forms.formsets import formset_factory

...


class SessionForm(forms.ModelForm):
    duration_choices = (
        ("1", "<.5>"),
        ("2", ".5"),
        ("3", "1"),
        ("4", "2"),
        ("5", "3"),
        ("6", "4"),
        ("7", "5"),
        ("8", "6"),
        ("9", "7"),
        ("10", "8"),
        ("11", "9"),
        ("12", "10"),
    )

    class Meta:
        model = Workout
        exclude = 'id', 'member',
        widgets = {
            'name': TextInput(attrs={
                'placeholder': 'name your session'
            }),
        }

    duration = forms.ChoiceField(choices=duration_choices)
    date = forms.DateField(
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"]
    )


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercises
        exclude = 'id', 'workout',
        widgets = {
            'ex_name': TextInput(attrs={
                'placeholder': 'exercise'
            })
        }


class SetForm(ModelForm):
    class Meta:
        model = ExSets
        fields = '__all__'
        widgets = {
            'ex_weight': TextInput(attrs={
                'placeholder': 'weight'
            }),
            'ex_reps': TextInput(attrs={
                'placeholder': 'reps'
            })
        }


SetFormset = inlineformset_factory(Exercises, ExSets, form=SetForm, extra=1)

UpdateSetsFormset = inlineformset_factory(Exercises, ExSets, form=SetForm, extra=0)


class BaseExerciseFormset(BaseInlineFormSet):
    def add_fields(self, form, index):
        super(BaseExerciseFormset, self).add_fields(form, index)

        # save the formset in the 'nested' property
        form.nested = UpdateSetsFormset(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix='set-%s-%s' % (
                form.prefix,
                UpdateSetsFormset.get_default_prefix()),
        )

    def is_valid(self):
        result = super(BaseExerciseFormset, self).is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()

        return result

    def save(self, commit=True):

        result = super(BaseExerciseFormset, self).save(commit=commit)

        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result


UpdateExercisesFormset = inlineformset_factory(Workout, Exercises, formset=BaseExerciseFormset, form=ExerciseForm,
                                               extra=0)
