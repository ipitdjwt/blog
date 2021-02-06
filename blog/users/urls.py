# 子应用users的视图路由
from django.urls import path
from users.views import RegisterView

urlpatterns = [
    # path参数一： 路由
    # path参数二： 视图函数名
    path('register/', RegisterView.as_view(), name='register'),
]
