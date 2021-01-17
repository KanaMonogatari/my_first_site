from django.shortcuts import HttpResponseRedirect


def redirect(request):
    return HttpResponseRedirect('feed/')