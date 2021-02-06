"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
#  1. 导入系统的logging
import logging


# #  2. 创建（获取）日志器  setting中的loggers > django
# logger = logging.getLogger(name='django')
#
#
# def log(request):
#     #  3. 使用日志器记录信息
#     logger.info('this is an info')
#     return HttpResponse('fuckyou')

app_name = 'users'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('users.urls', 'users'), namespace='users')),

    # include参数为元组(urlconf_module, app_name) =
    # urlconf_module: 子应用的路由 users.urls
    # app_name： 子应用名字 users
    # namespace： 防止不同子应用间的路由命名冲突
    # path('', include(('users.urls', 'users'), namespace='users')),


    # 日志测试代码 注册路由
    # path('', log),
]
