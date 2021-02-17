from django import forms
from django.forms.models import ModelForm
from directory.models import *
from django.forms.widgets import CheckboxSelectMultiple

class AddTeacherForm(ModelForm):

    class Meta:
        model = Teacher
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AddTeacherForm, self).__init__(*args, **kwargs)
        self.fields["subjects"].widget = CheckboxSelectMultiple()
        self.fields["subjects"].queryset = Subjects.objects.all()


    def clean(self):
        super(AddTeacherForm, self).clean()
        subjects = self.cleaned_data.get('subjects')
        email = self.cleaned_data.get('email')
        phone_number = self.cleaned_data.get('phone_number')

        if Teacher.objects.filter(email=email).exists():
            self._errors['email'] = self.error_class([
                'Email Already Exists'])
        if Teacher.objects.filter(phone_number=phone_number).exists():
            self._errors['phone_number'] = self.error_class([
                'Phone Number Already Exists'])
        

        if len(subjects) > 5:
            self._errors['subjects'] = self.error_class([
                'Maximum 5 Subjects allowed'])


        return self.cleaned_data
