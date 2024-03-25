from .models import News
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class EditorRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_editor = True
        if commit:
            user.save()
        return user


class ViewerRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_viewer = True
        if commit:
            user.save()
        return user


# forms.py


class EditorLoginForm(AuthenticationForm):
    # Add any additional fields or customization for editor login form
    pass


class ViewerLoginForm(AuthenticationForm):
    # Add any additional fields or customization for viewer login form
    pass


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['category', 'Headline', 'image', 'Body']
