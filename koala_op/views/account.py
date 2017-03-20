# coding=utf-8

from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from datetime import datetime, timedelta

from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect


def index(request):
    time = datetime.now()
    return render(request, 'koala_op/account.html')


def handle_file_upload(f):
    pass


def upload(request):
    f = request.FILES['file']
    # for i in f:
    #     print i.strip('\r').split(',')
    with open('static/file/tmp_file/{}'.format(f.name), 'w+') as f_out:
        for chunks in f.chunks():
            f_out.write(chunks)
    return HttpResponse('hello')
