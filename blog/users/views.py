from django.shortcuts import render
from django.views import View
from django.http.response import HttpResponseBadRequest
from django.http.response import HttpResponse
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from django.http.response import JsonResponse
from utils.response_code import RETCODE
import logging
logger = logging.getLogger('django')
from random import randint
import re


# Create your views here. 注册视图

# 注册页
class RegisterView(View):
    # 注册页面渲染
    def get(self, request):
        return render(request, 'register.html')

    # 注册功能实现（短信验证码111111）
    def post(self, request):
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        confirm_password = request.POST.get('password2')
        sms = request.POST.get('sms_code')

        # 参数是否齐全
        if not all([mobile, password, confirm_password, sms]):  # 缺失必要信息
            return HttpResponseBadRequest('缺少必要信息')

        # 手机格式验证
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseBadRequest('手机号不符合规则')

        # 密码格式验证 8-20位 两密码是否一致
        if not re.match(r'^[0-9a-zA-Z]{8, 20}$', password):
            return HttpResponseBadRequest('请输入8-20位密码')

        if password != confirm_password:
            return HttpResponseBadRequest('两次输入密码不一致')


        # 验证码验证：
        # connection = get_redis_connection('default')
        # key = 'img:%s' % uuid
        # value = connection.get(key)
        #
        # # 如果无此KEY代表已过有效时间 60秒
        # if value is None:
        #     return JsonResponse({'code': RETCODE.IMAGECODEERR, 'ERRMSG': '验证码过期'})
        #
        # # 拿到VALUE后删除KEY
        # try:
        #     connection.delete(key)
        # except Exception as e:
        #     logger = logging.getLogger('django')
        #     logger.error(e)
        #
        # # 比对 忽略大小写，value为bytes类型
        # if value.decode().lower() != image_code.lower():
        #     return JsonResponse({'code': RETCODE.IMAGECODEERR, 'ERRMSG': '验证码输入错误！'})
        #
        # # 一切正常后
        # return JsonResponse({'code': RETCODE.IMAGECODEERR, 'ERRMSG': '验证码输入错误！'})


# 验证码
class ImageCodeView(View):
    def get(self, request):
        # 1 get uuid
        uuid = request.GET.get('uuid')
        if uuid is None:
            return HttpResponseBadRequest('no uuid check code')
        # 2 生成验证码 return 验证码文本 图片二进制流
        text, image_stream = captcha.generate_captcha()
        # 3 保存验证码内容到REDIS key = img:uuid value = text 过期时间60秒
        key = 'img:%s' % uuid
        connection = get_redis_connection('default')
        connection.setex(key, 60, text)
        # 4 返回图片给前端
        return HttpResponse(image_stream, content_type='image/jpeg')


# 短信
class SmsView(View):
    """
    短信验证码方案： 容联云 https://yuntongxun.com/  DOCUMENT: http://doc.yuntongxun.com/space/5a5098313b8496dd00dcdd7f
    注册登陆 >> 管制控制台 ACCOUNT SID, AUTH_TOKEN, APP_ID
    免费开发测试使用的模板ID为1，具体内容：【云通讯】您的验证码是{1}，请于{2}分钟内正确输入。其中{1}和{2}为短信模板参数。
    """
    def get(self, request):
        mobile = request.GET.get('mobile')
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('uuid')

        # 验证参数齐全
        if not all([mobile, image_code, uuid]):
            return JsonResponse({'code': RETCODE.NECESSARYPARAMERR, 'ERRMSG': '缺少必要信息'})

        # 验证码验证：
        connection = get_redis_connection('default')
        key = 'img:%s' % uuid
        value = connection.get(key)

        # 如果无此KEY代表已过有效时间 60秒
        if value is None:
            return JsonResponse({'code': RETCODE.IMAGECODEERR, 'ERRMSG': '验证码过期'})

        # 拿到VALUE后删除KEY
        try:
            connection.delete(key)
        except Exception as e:
            logger.error(e)

        # 比对 忽略大小写，redis取出的value为bytes类型 b'ABCD'
        if value.decode().lower() != image_code.lower():
            return JsonResponse({'code': RETCODE.IMAGECODEERR, 'ERRMSG': '验证码输入错误！'})

        # 一切正常后,生成6位数字sms,插入日志和REDIS
        # sms = '%06d' % randint(0, 999999)
        sms = '111111'  # 写死验证码 接入短信API后改掉
        logger.info(sms)
        connection.setex('sms:%s' % mobile, 180, sms)

        # 调用SMS接口发送生成的SMS到手机
        # CCP().send_template_sms(mobile, [sms, 5], 1)

        # 一切完成，返回响应
        return JsonResponse({'code': RETCODE.OK, 'ERRMSG': '短信已发送至手机！'})
