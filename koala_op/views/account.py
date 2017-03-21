# coding=utf-8
from datetime import datetime, timedelta
import json
import urllib
import urllib2

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

from koala_op.logic import account_controller as AC

rc = AC.RegionController()


@ensure_csrf_cookie
def index(request):
    global rc
    try:
        print request.session['file_path']
    except Exception as e:
        pass
    provinces = rc.get_top_region()
    cities = rc.get_sub_region(provinces[0]['id'])
    districts = rc.get_sub_region(cities[0]['id'])
    schools = rc.get_school(districts[0]['regionCode'])
    context = {
        'provinces': provinces,
        'cities': cities,
        'districts': districts,
        'schools': schools
    }
    return render(request, 'koala_op/account/account.html', context=context)


def upload(request):
    f = request.FILES['file']
    if 'csv' in f.name:
        data = []
        for i in f:
            line = i.strip('\r').split(',')
            print line[5] == '男'
            data.append(line)
        file_path = 'static/file/tmp_file/{}'.format(f.name)
        with open(file_path, 'w+') as f_out:
            for chunks in f.chunks():
                f_out.write(chunks)
        request.session['file_path'] = file_path
        return render(request, 'koala_op/account/student_table.html', {'data': data})
    else:
        return HttpResponse(status=400, content='file type error')


def get_sub_area(request):
    global rc
    if request.GET.get('province_id'):
        p_id = request.GET.get('province_id')
        res = rc.get_sub_region(p_id)
        return HttpResponse(json.dumps(res))
    elif request.GET.get('city_id'):
        c_id = request.GET.get('city_id')
        res = rc.get_sub_region(c_id)
        return HttpResponse(json.dumps(res))
    elif request.GET.get('district_id'):
        code = request.GET.get('district_id')
        res = rc.get_school(code)
        return HttpResponse(json.dumps(res))
    else:
        return HttpResponse(status=400, content='parameter not valid')


def create_school_master(request):
    """
    创建校长
    :param request:
    :return:
    """
    ac = AC.AccountController()
    school_id = request.POST.get('school_id')
    if school_id:
        account, psd = ac.create_school_master(school_id)
        return HttpResponse(json.dumps(dict(account=account, psd=psd)))


def create_class(request):
    ac = AC.AccountController()
    school_id = request.POST.get('school_id')
    grade = request.POST.get('grade')
    name = request.POST.get('name')
    if school_id:
        res = ac.create_class(school_id, dict(grade=grade, full_name=name))
        return HttpResponse(json.dumps(res))


def create_students(request):
    ac = AC.AccountController()
    school_id = request.POST.get('school_id')
    join_code = request.POST.get('join_code')
    file_path = request.session['file_path']
    print school_id, join_code, file_path
    if school_id:
        res = ac.create_student_from_file(school_id, join_code, file_path)
        return HttpResponse(json.dumps(res))

