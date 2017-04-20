from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'accounts'

urlpatterns = [
    # EMPLOYEE
    # accounts/employee/register/
    url(r'^employee/register/$', views.registerEmployee, name='employee-add'),
    url(r'^employee/login/$', views.loginEmployee, name='employee-login'),
    url(r'^employee/logout/$', views.logoutEmployee, name='employee-logout'),
    url(r'^employee/skillmatch/$', views.matchSkill, name='employee-match'),
    url(r'^employee/index/$', login_required(views.indexEmployee.as_view()), name='employee-index'),
    # CLIENT
    url(r'^client/register/$', views.registerClient, name='client-add'),
    url(r'^client/login/$', views.loginClient, name='client-login'),
    url(r'^client/logout/$', views.logoutClient, name='client-logout'),
    url(r'^client/job/$', login_required(views.jobopportunity.as_view()), name='client-job'),
    url(r'^client/index/$', login_required(views.indexClient.as_view()), name='client-index'),
    # APPLICANT
    url(r'^applicant/register/$', views.registerApplicant, name='applicant-add'),
    url(r'^applicant/login/$', views.loginApplicant, name='applicant-login'),
    url(r'^applicant/logout/$', views.logoutApplicant, name='applicant-logout'),
    url(r'^applicant/index/$', login_required(views.indexApplicant.as_view()), name='applicant-index'),
    url(r'^applicant/requirement/$', login_required(views.requirementsApplicant.as_view()),
        name='applicant-requirement'),
    url(r'^applicant/education/$', login_required(views.educationApplicant.as_view()),
        name='applicant-education'),
    url(r'^applicant/skills/$', login_required(views.skillApplicant.as_view()), name='applicant-skill'),
]
