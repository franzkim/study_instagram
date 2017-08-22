from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput,
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
    )

    # clean <fieldname> 메서드를 사용해서
    # username 필드에 대한 유효성 검증을 실행
    def clean_username(self):
        username = self.cleaned_data['username']
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'Username already exist'
            )
        return username

    def clean_password2(self):
        # password1과 password2를 비교하여 같은지 검증
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                'Password mismatch'
            )
        return password2

    def create_user(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        return User.objects.create_user(
            username=username,
            password=password
        )
