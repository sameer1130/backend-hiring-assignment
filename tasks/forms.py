from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Project, Task

User = get_user_model()  # Ensure we use the custom user model

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User  # Ensure we use Client (AUTH_USER_MODEL)
        fields = ["username", "email", "name", "password1", "password2"]

    def clean_password2(self):
        """Ensure both passwords match"""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", 'client']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "project", "status"]
