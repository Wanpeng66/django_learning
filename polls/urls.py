from django.urls import path
from . import views


app_name = "polls"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:question_id>/", views.detail, name="question_detail"),
    path("<int:question_id>/result/", views.results, name="question_results"),
    path("<int:question_id>/vote/", views.votes, name="choice_vote")
]
