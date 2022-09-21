import datetime
from django.core.exceptions import ValidationError

from django.db import models
from django.core.validators import MinValueValidator


class Student(models.Model):

    name = models.CharField(max_length=255, verbose_name="Student Name")
    dob = models.DateField(verbose_name="Date of Birth")
    no_of_degree = models.IntegerField(
        verbose_name="How many Degree you have?",
        validators=[MinValueValidator(0, message="You can't provide negative value.")],
    )

    created_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.dob > datetime.date.today():
            raise ValidationError("Your DOB can't be in future")
        super(Student, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
