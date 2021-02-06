from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
# 继承并扩民系统默认User类
class User(AbstractUser):
    phone = models.CharField(max_length=11, unique=True, blank=False)
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)
    profile = models.CharField(max_length=500, blank=True)

    class Meta:
        db_table = 'tb_users'  # 修改表名
        verbose_name = '用户管理'  # admin 后台展示
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.phone

# settings
