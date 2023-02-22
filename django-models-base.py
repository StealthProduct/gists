from django.db import models
from django.core.exceptions import ValidationError


BOOLEAN_CHOICES = ((True, "Yes"), (False, "No"))


def validate_file_size(value):
    filesize = value.size

    if filesize > (10 * 1024 * 1024):
        raise ValidationError(
            "You cannot upload file more than 10Mb. It will impact loading the website.")
    else:
        return value


class SingletonBaseModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class TimeStampMixin(models.Model):
    """TimeStampMixin acts as parent class to model for adding creation and update time fields

    Attributes
    ----------
    created_at : models.DateTimeField
        Auto adds the now value of datetime, and is not affected by further updates
    updated_at : models.DateTimeField
        Auto adds the now value of datetime, and is updated to new value when further updates happen
    """

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Created date & time")
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Last Updated date & time")
    is_active = models.BooleanField(
        default=True, choices=BOOLEAN_CHOICES, help_text="Whether the object is active",
        db_index=True
    )

    class Meta:
        abstract = True
        ordering = ('-created_at', )

    def update_object(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.save()


class FileWithAlt(TimeStampMixin):
    file = models.FileField(help_text="File field",
                            validators=[validate_file_size])
    alt = models.TextField(help_text="Alternate description of file")

    class Meta:
        verbose_name = "File"
        verbose_name_plural = "Files"
        ordering = ('-created_at', )

    def __str__(self):
        return str(self.file)
