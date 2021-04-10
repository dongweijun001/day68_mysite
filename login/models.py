from django.db import models

# Create your models here.

class User(models.Model):
    gender_choice=(
        ('male','男'),
        ('female','女')
    )
    name=models.CharField(max_length=32,verbose_name='姓名', unique=True)
    password=models.CharField(max_length=256,verbose_name='密码')
    email=models.EmailField(verbose_name='邮箱',unique=True)
    sex=models.CharField(max_length=32,choices=gender_choice, verbose_name='性别',default='男')
    c_time=models.DateTimeField(auto_now_add=True)
    has_confirmed=models.BooleanField(default=False)

    def __str__(self):
        return self.name
    class Meta:
        ordering=['-c_time']
        verbose_name='用户'
        verbose_name_plural='用户'

class ConfirmString(models.Model):
    code=models.CharField(max_length=256)
    user=models.OneToOneField('User', on_delete=models.CASCADE)
    c_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + ": "+ self.code

    class Meta:
        ordering=['-c_time']
        verbose_name='激活码'
        verbose_name_plural='激活码'


