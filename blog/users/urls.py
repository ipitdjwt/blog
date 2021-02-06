# 子应用users的视图路由
from django.urls import path
from users.views import RegisterView, ImageCodeView, SmsView

urlpatterns = [
    # path参数一： 路由
    # path参数二： 视图函数名

    # 注册用户页
    path('register/', RegisterView.as_view(), name='register'),
    # 图片验证码
    path('imagecode/', ImageCodeView.as_view(), name='imagecode'),
    # sms
    path('smscode/', SmsView.as_view(), name='smscode'),
]
