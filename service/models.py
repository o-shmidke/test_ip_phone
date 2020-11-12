from django.db import models


class Permission(models.Model):
    perm = models.BooleanField(verbose_name='Доступ к управлению сервисом', default=False)

    def __str__(self):
        return self.perm
