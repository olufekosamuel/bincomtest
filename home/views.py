
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
    result = []
    mike = []
    
    if request.method == "POST":
        local = request.POST['lgaselected']
        if local:
            """
            res = AnnouncedLgaResults.objects.filter(lga_name=local)
            for r in res:
                print(r.party_abbreviation+" "+str(r.party_score))
            
            """
            polls = PollingUnit.objects.filter(lga_id=local)
            for poll in polls:
                #print(poll.lga_id)
                result.append(AnnouncedPuResults.objects.filter(polling_unit_uniqueid=poll.polling_unit_id))
                """
                print(result)
                for res in result:
                    print(res.party_abbreviation+":"+str(res.party_score))
                    mydb.extend(list([res.party_abbreviation,res.party_score ]))
                """
           
            for i in range(len(result)):
                for j in range(len(result[i])):
                    #print(result[i][j])
                    mike.append(result[i][j])
            return render(request, 'lga.html', {'locals':lga})
    return render(request, 'lga.html', {'locals':lga,'party':party})

def lgaresult(request):
    pass
