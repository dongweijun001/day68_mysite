import os
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE']='day68_mysite.settings'

# ff52a8ac67b63471
if __name__ == '__main__':
    # send_mail(
    #     '来自董卫军的测试邮件',
    #     '欢迎访问董卫军的新网站，分享各自的观点和经验',
    #     'zilyzdwj@sina.com',
    #     ['zilyzdwj@126.com'],
    # )

    subject, from_email, to = '来自董卫军的测试邮件', 'zilyzdwj@sina.com', 'zilyzdwj@126.com'
    text_content = '欢迎访问www.sina.com，这里是董卫军的博客和教程站点，专注于Python和Django技术的分享！'
    html_content = '<p>欢迎访问<a href="http://www.liujiangblog.com" target=blank>www.liujiangblog.com</a>，这里是刘江的博客和教程站点，本站专注于Python、Django和机器学习技术的分享！</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()