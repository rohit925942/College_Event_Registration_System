from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Event(models.Model):
    event_name = models.CharField(max_length=100)
    event_date = models.DateField()
    venue = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.event_name
    
class Registration(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (
            'student',
            'event'
        )