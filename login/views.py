from django.shortcuts import render
from django.shortcuts import HttpResponse
from login import models


# user_list = []


def index(request):
    # return HttpResponse("hello world...")
    # return render(request, "index.html")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        # current_user = {"username": username, "password": password}
        # user_list.append(current_user)

        models.UserInfo.objects.create(username=username, password=password)
    user_list = models.UserInfo.objects.all()
    return render(request, "index.html", {"data": user_list})
