
from datetime import datetime
import datetime

from smtplib import SMTPException
from urllib.parse import urlparse
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render,redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.template.response import TemplateResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
#from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.authtoken.models import Token
from datetime import timedelta
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse

from .models import *


def index(request):
    pol = PollingUnit.objects.get(uniqueid=8)
    return render(request,'index.html')

def polling(request):
    pol = PollingUnit.objects.all()
    return render(request, 'poll.html', {'poll':pol})

def result(request, id):
    try:
        res = AnnouncedPuResults.objects.filter(polling_unit_uniqueid=id)
        print(res)
    except AnnouncedPuResults.DoesNotExist:
        pass
    return render(request, 'result.html', {'result':res})

def lgalist(request):
    lga = Lga.objects.all()
    party = Party.objects.all()
    return render(request, 'lga.html', {'locals':lga,'party':party})

def lgaresult(request, id, party):
    result = []
    total = 0
    polls = PollingUnit.objects.filter(lga_id=id)
    if party== "LABOUR":
        party="LABO"
    for poll in polls:
        results = AnnouncedPuResults.objects.filter(polling_unit_uniqueid=poll.polling_unit_id,party_abbreviation=party)
        for result in results:
            total += result.party_score    
    return JsonResponse({'totstat': total})

def storeresult(request):
    party = Party.objects.all()
    users = Agentname.objects.all()
    wards = Ward.objects.all()
    Laga = Lga.objects.all()
    if request.method == "POST":
        name = request.POST['pollname']
        no = request.POST['pollno']
        desc = request.POST['description']
        ward = request.POST['ward']
        lga = request.POST['lga']
        user = request.POST['user']

        polls = PollingUnit.objects.all().reverse()[0]
        try:
            PollingUnit.objects.get(polling_unit_number=no)
            error= "Polling Unit Already Exist"
            return render(request, 'storeresult.html', {'party':party,'users':users,'wards':wards,'lga':lga,'error':error})
        except PollingUnit.DoesNotExist:
            poll = PollingUnit.objects.create(polling_unit_number=no,polling_unit_name=name,polling_unit_description=desc,lat=0,long=0,entered_by_user=user,user_ip_address=0,lga_id=lga,ward_id=ward,polling_unit_id=polls.polling_unit_id+1,)
            poll.save()

        for part in party:
            if part.partyname== "LABOUR":
                res = AnnouncedPuResults.objects.create(party_abbreviation="LABO",party_score=request.POST[part.partyname],entered_by_user=user,user_ip_address=0,polling_unit_uniqueid=poll.polling_unit_id,date_entered=datetime.datetime.now())   
            else:
                res = AnnouncedPuResults.objects.create(party_abbreviation=part.partyname,party_score=request.POST[part.partyname],entered_by_user=user,user_ip_address=0,polling_unit_uniqueid=poll.polling_unit_id,date_entered=datetime.datetime.now())
            res.save()
        return render(request, 'storeresult.html', {'party':party,'users':users,'wards':wards,'lga':Laga})

    return render(request, 'storeresult.html', {'party':party,'users':users,'wards':wards,'lga':Laga})
