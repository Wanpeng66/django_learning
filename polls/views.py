from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse
from django.template import loader

from .models import Question


def index(request):
    question_list = get_list_or_404(Question)
    content = {
        "question_list": question_list
    }
    return render(request=request, template_name="polls/index.html", context=content)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {
        "question": question
    }
    return render(request, "polls/detail.html", context)


def results(request, question_id):
    resp = " you're looking at the result of question %s "
    return HttpResponse(resp % question_id)


def votes(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choice = question.choice_set.get(pk=request.POST.get("choice"))
    choice.votes += 1
    choice.save()
    return HttpResponse(" you're voting for choice %s " % request.POST.get("choice"))
