#!/usr/bin/python
# -*- coding: utf-8 -*-
import django
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User, Group
from django.template.context import Context, RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, \
    logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
#from events.models import Event
from users.models import UserProfile, College
from django.utils.translation import ugettext as _
from users.forms import *
from django.contrib.sessions.models import Session
#from django.core.mail import EmailMessage, EmailMultiAlternatives
#from django.core.mail import send_mail as mailsender
#from recaptcha.client import captcha
import sha
import random
import datetime


def method_splitter(request, *args, **kwargs):
    get_view = kwargs.pop('GET', None)
    post_view = kwargs.pop('POST', None)
    if request.method == 'GET' and get_view is not None:
        return get_view(request, *args, **kwargs)
    elif request.method == 'POST' and post_view is not None:
        return post_view(request, *args, **kwargs)
    raise Http404

def login_get(request):
    if request.user.is_authenticated():
        currentuser = request.user
        if request.user.is_superuser:
            return HttpResponseRedirect(settings.BASE_URL + 'admin/')
        else:
            return HttpResponseRedirect(settings.BASE_URL)
    form = LoginForm()
    try:
        msg=request.session['msg']
        del request.session['msg']
    except:
        pass
    return render_to_response('users/login.html', locals(),
                              context_instance=RequestContext(request))


def login_post(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth_login(request, user)
	return HttpResponse('You have successfully logged in');
        '''
	try:
            nextURL = request.GET['next']
        except:
            nextURL = ''
        if nextURL != '':
            nextURL = nextURL[1:]  # For removing the leading slash from in front of the next parameter
            redirectURL = settings.BASE_URL + nextURL
            return HttpResponseRedirect(redirectURL)
        if user.is_superuser:
            return HttpResponseRedirect(settings.BASE_URL + 'admin/')
        elif user.get_profile().is_core:
            return HttpResponseRedirect(settings.BASE_URL + 'core/')
        elif user.get_profile().is_coord_of:
            return HttpResponseRedirect(settings.BASE_URL + 'coord/')
        elif user.get_profile().is_hospi:
            return HttpResponseRedirect(settings.BASE_URL + 'controlroom/home/')
        else:
            return HttpResponseRedirect(settings.BASE_URL)
	'''
    
    msg = 'Username and Password does not match!!!'  
    form = LoginForm()
    return render_to_response('users/login.html', locals(),
                              context_instance=RequestContext(request))

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(settings.BASE_URL)

def register_get(request):
    form = AddUserForm()
    #post_url = settings.BASE_URL + 'user/register/'
    #captcha_response = ''  # Added so that nothing gets displayed in the template if this variable is not set
    return render_to_response('users/register.html', locals(),
                              context_instance=RequestContext(request))


def register_post(request):
    """
        This is the user registration view
    """

    form = AddUserForm(request.POST)
    #@captcha_response = ''  # Added so that nothing gets displayed in the template if this variable is not set
    
    # talk to the reCAPTCHA service
    '''response = captcha.submit(  
        request.POST.get('recaptcha_challenge_field'),  
        request.POST.get('recaptcha_response_field'),  
        settings.RECAPTCHA_PRIVATE_KEY,  
        request.META['REMOTE_ADDR'],)  
          
    # see if the user correctly entered CAPTCHA information  
    # and handle it accordingly.  
    if response.is_valid:
	'''  
    if form.is_valid():
            data = form.cleaned_data
            new_user = User(first_name=data['first_name'],
                            last_name=data['last_name'],
                            username=data['username'], email=data['email'])
            new_user.set_password(data['password'])
            new_user.is_active = False
            new_user.save()
            x = 1300000 + new_user.id 
            salt = sha.new(str(random.random())).hexdigest()[:5]
            activation_key = sha.new(salt + new_user.username).hexdigest()
            #key_expires = datetime.datetime.today() + datetime.timedelta(2)
            userprofile = UserProfile(
                user=new_user,
                activation_key=activation_key,
                #key_expires=key_expires,
                gender=data['gender'],
                age=data['age'],
                branch=data['branch'],
                mobile_number=data['mobile_number'],
                college=data['college'],
                college_roll=data['college_roll'],
                shaastra_id= ("SHA" + str(x)),
                #want_accomodation = data['want_accomodation'],
                )
            userprofile.save()
            #mail_template = get_template('email/activate.html')
            '''body = \
                mail_template.render(Context({'username': new_user.username,
                                     'BASE_URL': settings.BASE_URL,
                                     'activationkey': userprofile.activation_key}))
            mailsender('Your new Shaastra2013 account confirmation', body,
                       'noreply@shaastra.org', [new_user.email],
                       fail_silently=False)
            request.session['registered_user'] = True
            request.session['msg']="A mail has been sent to the mail id you provided. Please activate your account within 48 hours. Check your spam folder if you do not receive the mail in your inbox."'''
            request.session['registered_user'] = True
            request.session['msg']="You have registered successfully"
            return HttpResponseRedirect(settings.BASE_URL+'user/login')
    #else:
    #    captcha_response = response.error_code
    return render_to_response('users/register.html', locals(),
                              context_instance=RequestContext(request))

