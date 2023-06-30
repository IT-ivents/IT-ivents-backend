from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator
# from events.models import Event


class User(AbstractUser):
    """Кастомная модель пользователя"""

    ADMIN = "admin"
    USER = "user"
    MANAGER = "manager"
    role_choices = (
        (ADMIN, ADMIN),
        (USER, USER),
        (MANAGER, MANAGER)
    )
    email = models.EmailField("email address", unique=True)
    role = models.CharField(
        max_length=settings.USER_ROLE_NAME_LENGTH,
        choices=role_choices, default=USER
    )
    profile_photo = models.ImageField("Аватар", upload_to="users/avatars/",
                                      help_text="Аватар пользователя",
                                      blank=True)
    organization = models.CharField(
        "Организация",
        validators=[MinLengthValidator(2)],
        max_length=100,
        help_text="Название организации"
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_manager(self):
        return self.role == self.MANAGER

    class Meta:
        ordering = ["-id"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Organisation(models.Model):
    manager = models.OneToOneField(User,
                                   on_delete=models.CASCADE,
                                   verbose_name="Менеджер организации")
    name = models.CharField(max_length=200, db_index=True)

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"


# class OwnerEvents(models.Model):
#     author = models.ForeignKey(User,
#                                on_delete=models.CASCADE,
#                                verbose_name="Организатор")
#     event = models.ForeignKey(Event,
#                               on_delete=models.CASCADE)
#
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['owner', 'event'],
#                                     name='unique_owner_event')
#         ]
#
#     def __str__(self):
#         return f'{self.owner} создал событие {self.event}'
