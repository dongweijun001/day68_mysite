from django import forms
from captcha.fields import CaptchaField, CaptchaTextInput

class UserForm(forms.Form):
    username=forms.CharField(label='用户', max_length=128, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'username','autofocus':''}))
    password=forms.CharField(label='密码', max_length=256,widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'password'}))
    # captcha=CaptchaField(label='验证码', widget=CaptchaField(attrs={'class':'form-control', 'placeholder':'username','autofocus':''}))
    captcha=CaptchaField(label='验证码', widget=CaptchaTextInput(attrs={'class':'form-control', 'placeholder':'验证码','autofocus':''}))

class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'新用户名','autofocus':''}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'密码'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'确认密码'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    captcha = CaptchaField(label='验证码', widget=CaptchaTextInput(attrs={'class':'form-control', 'placeholder':'验证码','autofocus':''}))