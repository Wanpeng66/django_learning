from django.db import models
from django.utils import timezone
import datetime


class Question(models.Model):
    question_content = models.CharField(max_length=255)
    publish_time = models.DateTimeField("data published")

    def __str__(self):
        return "{'question_content': " + self.question_content + ", 'publish_time': " + str(self.publish_time) + " }"

    def was_publish_recently(self):
        return self.publish_time >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_content = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return "{ 'Question': " + self.question.__str__() + ", 'choice_content': " + self.choice_content + \
               ", 'votes': " + str(self.votes) + " }"


class Person(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
