from django.shortcuts import render, redirect
from . import models
from . import forms
import hashlib

import datetime
from django.conf import settings
# Create your views here.


def hash_code(s, salt='mysite'):# 创建哈希密码
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def make_confirm_string(user):  # 创建激活码对象的方法
    # now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S' )
    now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S' )
    code=hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user,)
    return code


def send_mail(email, code): # 发注册邮件确认
    from django.core.mail import EmailMultiAlternatives
    subject="来自我的网站的注册激活码验证邮件"
    text_content="感谢您参与我的网站的激活码验证，这是董卫军的初创网站，欢迎提出宝贵意见，谢谢！"
    html_content=f'''
                    <p>感谢注册<a href="http://{'127.0.0.1:8000'}/confirm/?code={code}" target=blank>www.baidu.com</a>，\
                    这里是董卫军的博客和教程站点，专注于Python、Django和机器学习技术的分享！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{settings.CONFIRM_DAYS}天！</p>
                    '''
    msg_1=EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER,[email])
    msg_1.attach_alternative(html_content, 'text/html')
    msg_1.send()


def user_confirm(request): # 处理邮件激活码
    '''通过request.GET.get('code', None)从请求的url地址中获取确认码;'''
    code= request.GET.get('code', None)
    msg=''
    try:
        '''先去数据库内查询是否有对应的确认码'''
        confirm=models.ConfirmString.objects.get(code=code)
    except:
        '''如果没有，返回confirm.html页面，并提示'''
        msg='无效的请求或者确认'
        return render(request, 'login/confirm.html', locals())
    '''
    如果有，获取注册的时间c_time，加上设置的过期天数，这里是7天，然后与现在时间点进行对比
    如果时间已经超期，删除注册的用户，同时注册码也会一并删除，然后返回confirm.html页面，并提示
    '''
    c_time=confirm.c_time       # 含有时区信息
    now = datetime.datetime.now()   # 不含有时区信息
    if now > (c_time+datetime.timedelta(settings.CONFIRM_DAYS)).replace(tzinfo=None): # replace(tzinfo=None)将时区信息去除
        confirm.user.delete()
        msg='您的邮件已经过期，请重新注册'
        return render(request,'login/confirm.html', locals())

    else:
        '''
            如果未超期，修改用户的has_confirmed字段为True，并保存，表示通过确认了。然后删除注册码，但不删除用户本身。最后返回confirm.html页面，并提示。
        '''
        confirm.user.has_confirmed=True
        confirm.user.save()
        confirm.delete()
        msg="感谢确认，请使用账户登录！"
        return render(request,'login/confirm.html', locals())


def index(request):
    if not request.session.get('is_login',None):    # 判断是否登录
        return redirect('/login/')

    return render(request, 'login/index.html')


def register(request):
    if request.session.get('is_login', None): # 判断是否登录，如登录则不能注册
        return redirect('/login/')

    if request.method=='POST':
        register_form=forms.RegisterForm(request.POST)
        msg='请检查填写的内容'
        if register_form.is_valid():
            username=register_form.cleaned_data.get('username')
            password1=register_form.cleaned_data.get('password1')
            password2=register_form.cleaned_data.get('password2')
            email=register_form.cleaned_data.get('email')
            sex=register_form.cleaned_data.get('sex')

            if password1!=password2:    # 两次密码不一致
                msg='两次密码不一致！'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user=models.User.objects.filter(name=username)
                if same_name_user:   # 如果存在同类用户名
                    msg='用户名已经存在'
                    return render(request, 'login/register.html', locals())
                same_email_user=models.User.objects.filter(email=email)
                if same_email_user:
                    msg='该邮箱已经被注册了！'
                    return render(request, 'login/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                code=make_confirm_string(new_user)
                send_mail(email, code)

                msg='请前往邮箱确认'
                # return redirect('/login/')
                return render(request,'login/confirm.html', locals())
        else:
            return render(request, 'login/register.html', locals())

    # if request.session.get_expire_at_browser_close():
    #     request.session.flush()

    register_form=forms.RegisterForm()
    return render(request, 'login/register.html', locals())


# def login(request):
#     if request.method=='POST':
#         username=request.POST.get('username')
#         password=request.POST.get('password')
#
#         if username.strip() and password:
#             try:
#                 user=models.User.objects.get(name=username)
#             except:
#                 msg='用户不存在！'
#                 return render(request, 'login/login.html', {'message': msg})
#             if user.password==password:
#                 print(username, password)
#                 return redirect('/index/')
#             else:
#                 msg = '密码不正确！'
#                 return render(request, 'login/login.html', {'message': msg})
#     ...
#     return render(request, 'login/login.html')

def login(request):     # 利用forms组件
    if request.session.get('is_login',None):    # 不允许重复登录
        return redirect('/index/')

    # if request.session.get_expire_at_browser_close():   # 浏览器关闭，所有的session清空
    #     print(request.session.get_expire_at_browser_close())
    #     request.session.flush()

    if request.method=='POST':
        login_form=forms.UserForm(request.POST)
        msg='请检查填写的内容'
        if login_form.is_valid():
            # print(login_form.is_valid())
            username=login_form.cleaned_data.get('username')
            password=login_form.cleaned_data.get('password')
            # print(username, password)
            try:
                user=models.User.objects.get(name=username)
                # print(user)
            except:
                msg='用户不存在'
                return render(request, 'login/login.html', locals())

            if not user.has_confirmed:
                msg = '该用户还未经过邮件确认！'
                return render(request, 'login/confirm.html', locals())

            if user.password==hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                msg='密码不正确'
                return render(request,'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())

    login_form=forms.UserForm()
    return render(request, 'login/login.html', locals())


def logout(request):
    if not request.session.get('is_login', None): # 判断是否没有登录
        return redirect('/login/')
    request.session.flush() # 清空session里所有的内容
    """或者清理一部分内容"""
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']

    return redirect('/login/')