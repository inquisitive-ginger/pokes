from django import forms
from .models import User
from datetime import datetime

# list of last 125 years for D.O.B. select
BIRTH_YEAR_CHOICES = range(datetime.today().year, datetime.today().year - 125, -1)

class RegisterForm(forms.ModelForm):
    password_confirmation = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('name', 'alias', 'email', 'date_of_birth', 'password', 'password_confirmation')
        widgets = {
            'password': forms.PasswordInput,
            'date_of_birth': forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES, attrs={"class": "input"})
        }

    # add password confirmation and age valdiation
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = self.cleaned_data['password']
        confirm = self.cleaned_data['password_confirmation']
        date_of_birth = self.cleaned_data['date_of_birth']

        if password != confirm:
            raise forms.ValidationError("Passwords do not match.")

    # call set_password on user which uses bcrypt to hash the raw password
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ( 'email', 'password')
        widgets = { 'password': forms.PasswordInput }

    # don't care about unique email on login, just registration
    def validate_unique(self):
        pass

    # verify user credentials against db
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError('Email/Password combo is incorrect.')

        user = User.objects.get(email=email)
        if not user.check_password(password):
            raise forms.ValidationError('Email/Password combo is incorrect.')
