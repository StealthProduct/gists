from django.db import models
from yourbaseclass import TimeStampMixin, ImageWithAlt
from yourconstantclass import BOOLEAN_CHOICES, Gender, BloodGroup
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class UserType(models.IntegerChoices):
    ADMIN = 100, _("Admin")
    TEACHER = 200, _("Teacher")

    NONE = -1, _("None")

    __empty__ = _("---")


class PersonalDetails(TimeStampMixin):
    mother_name = models.CharField(max_length=128)
    father_name = models.CharField(max_length=128)
    blood_group = models.CharField(
        max_length=6, choices=BloodGroup.choices, default=BloodGroup.__empty__)
    vehicle_number = models.CharField(max_length=15, null=True, blank=True)
    home_address = models.CharField(max_length=128)
    date_of_birth = models.DateField(default=None, blank=True, null=True)
    date_of_joining = models.DateField(default=None, blank=True, null=True)

    class Meta:
        verbose_name = 'Personal Detail'
        verbose_name_plural = 'Personal Details'


class MyUser(AbstractUser, TimeStampMixin):
    full_name = models.CharField(
        max_length=300,
        help_text="Full name"
    )
    phone_number = models.CharField(
        validators=[
            RegexValidator(
                regex=r"^[4-9]\d{9}$", message="Please enter a valid phone number."
            )
        ],
        max_length=10,
        null=True,
        blank=True,
        unique=True,
        help_text="Valid phone number"
    )
    parent = models.ForeignKey(
        "self", on_delete=models.PROTECT, null=True, blank=True)
    gender = models.CharField(
        max_length=1, choices=Gender.choices, default=Gender.OTHERS)
    type = models.IntegerField(choices=UserType.choices, default=UserType.NONE)
    is_onboarded = models.BooleanField(choices=BOOLEAN_CHOICES, default=False)
    is_activated = models.BooleanField(choices=BOOLEAN_CHOICES, default=True)
    is_new_user_password = models.BooleanField(default=False)
    is_password_changed = models.BooleanField(default=False)
    image = models.ForeignKey(
        ImageWithAlt,
        null=True,
        blank=True,
        related_name="user_image",
        on_delete=models.PROTECT,
        help_text="Display Picture of the user"
    )
    personal_info = models.OneToOneField(
        PersonalDetails,
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )

    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.full_name:
                self.full_name = self.first_name + " " + self.last_name
                self.full_name = self.full_name.strip()
        super(MyUser, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ('-is_active', '-created_at',)

    @property
    def is_admin(self):
        return self.type == UserType.ADMIN or self.is_superuser
