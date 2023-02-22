from django.db import models
from django.utils.translation import gettext_lazy as _


BOOLEAN_CHOICES = ((True, "Yes"), (False, "No"))


class BloodGroup(models.TextChoices):
    Apos = 'A +ve', _('A +ve')
    Aneg = 'A -ve', _('A -ve')
    Bpos = 'B +ve', _('B +ve')
    Bneg = 'B -ve', _('B -ve')
    Opos = 'O +ve', _('O +ve')
    Oneg = 'O -ve', _('O -ve')
    ABpos = 'AB +ve', _('AB +ve')
    ABneg = 'AB -ve', _('AB -ve')
    __empty__ = _('---')


class Gender(models.TextChoices):
    MALE = "M", _("Male")
    FEMALE = "F", _("Female")
    OTHERS = "O", _("Others")

    __empty__ = _("---")
