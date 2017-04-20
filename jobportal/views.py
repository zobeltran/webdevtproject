from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import CreateView
from .forms import EmployeeRegistration, ClientRegistration, ApplicantRegistration
from .forms import ApplicantLogin, EmployeeMatchSkill, EmployeeLogin, ClientLogin
from .models import Employee, Client, Applicant, Requirement, Education, JobOpportunity, Specialized, SkillMatching
from django.contrib.auth import authenticate, login as auth_login, logout
from django.core.urlresolvers import reverse_lazy

# Create your views here.


def index(request):
    return render(request, 'index.html')


def register(request):
    return render(request, 'register.html')


def login(request):
    return render(request, 'login.html')


def registerEmployee(request):
    if request.method == 'POST':
        employee_form = EmployeeRegistration(request.POST)
        if employee_form.is_valid():
            employee_form.save()
            return redirect('/accounts/employee/login')
        else:
            return render(request, 'employee/register.html', {'form': employee_form})

    else:
        employee_form = EmployeeRegistration()

        args = {'form': employee_form}
        return render(request, 'employee/register.html', args)


def registerClient(request):
    if request.method == 'POST':
        client_form = ClientRegistration(request.POST, request.FILES)
        if client_form.is_valid():
            client_form.save()
            return redirect('/accounts/client/login')
        else:
            return render(request, 'client/register.html', {'form': client_form})

    else:
        client_form = ClientRegistration()

        args = {'form': client_form}
        return render(request, 'client/register.html', args)


def registerApplicant(request):
    if request.method == 'POST':
        applicant_form = ApplicantRegistration(request.POST, request.FILES)
        if applicant_form.is_valid():
            applicant_form.save()
            return redirect('/accounts/applicant/login')
        else:
            return render(request, 'applicant/register.html', {'form': applicant_form})
    else:
        applicant_form = ApplicantRegistration()
        args = {'form': applicant_form}
        return render(request, 'applicant/register.html', args)


def loginApplicant(request):
    # print(request.user.is_authenticated())
    title = "Login"
    template_name = 'applicant/login.html'
    form = ApplicantLogin(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(username=email, password=password)
        auth_login(request, user)
        # print(request.user.is_authenticated())
        return redirect('/accounts/applicant/index')
    return render(request, template_name, {'form': form, 'title': title})


def loginEmployee(request):
    title = "Login"
    template_name = 'employee/login.html'
    form = EmployeeLogin(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(username=email, password=password)
        auth_login(request, user)
        # print(request.user.is_authenticated())
        return redirect('/accounts/employee/index')
    return render(request, template_name, {'form': form, 'title': title})


def loginClient(request):
    title = "Login"
    template_name = 'client/login.html'
    form = ClientLogin(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(username=email, password=password)
        auth_login(request, user)
        # print(request.user.is_authenticated())
        return redirect('/accounts/client/index')
    return render(request, template_name, {'form': form, 'title': title})


def logoutApplicant(request):
    logout(request)
    template_name = 'applicant/logout.html'
    return render(request, template_name)


def logoutEmployee(request):
    logout(request)
    template_name = 'employee/logout.html'
    return render(request, template_name)


def logoutClient(request):
    logout(request)
    template_name = 'client/logout.html'
    return render(request, template_name)


class indexApplicant(generic.TemplateView):
    template_name = 'applicant/index.html'
    model = Applicant
    context_object_name = 'applicant'

    def get_queryset(self):
        applicant = Applicant.objects.filter(user=self.request.user)
        return applicant


class indexClient(generic.TemplateView):
    template_name = 'client/index.html'
    model = Client
    context_object_name = 'client'

    def get_queryset(self):
        client = Client.objects.filter(user=self.request.user)
        return client


class indexEmployee(generic.TemplateView):
    template_name = 'employee/index.html'
    model = Employee
    context_object_name = 'employee'

    def get_queryset(self):
        employee = Employee.objects.filter(user=self.request.user)
        return employee


class requirementsApplicant(generic.CreateView):
    model = Requirement
    template_name = 'applicant/requirements.html'
    fields = ['SSS', 'Phil_Health', 'TIN', 'NBI_Clearance', 'Marriage_Contract', 'TOR',
              'Picture', 'Employee_Certificate', 'Clearance_To_Transfer', 'Clearance_From_SSS']

    success_url = reverse_lazy('accounts:applicant-index')

    def form_valid(self, form):
        form.instance.User = self.request.user.applicant
        return super(requirementsApplicant, self).form_valid(form)


class educationApplicant(generic.CreateView):
    model = Education
    template_name = 'applicant/educationform.html'
    fields = ['School_Name', 'Education_Attained']
    success_url = reverse_lazy('accounts:applicant-index')

    def form_valid(self, form):
        form.instance.User = self.request.user.applicant
        return super(educationApplicant, self).form_valid(form)


class jobopportunity(generic.CreateView):
    model = JobOpportunity
    template_name = 'client/job.html'
    fields = ['Job_Post', 'Required_Applicants']

    success_url = reverse_lazy('accounts:client-job')

    def form_valid(self, form):
        form.instance.User = self.request.user.client
        return super(jobopportunity, self).form_valid(form)


class skillApplicant(generic.CreateView):
    model = Specialized
    template_name = 'applicant/skills.html'
    fields = ['Specialization', 'SubSkill']

    success_url = reverse_lazy('accounts:applicant-skill')

    def form_valid(self, form):
        form.instance.User = self.request.user.applicant
        return super(skillApplicant, self).form_valid(form)


def matchSkill(request):
    if request.method == "POST":
        form = EmployeeMatchSkill(request.POST)
        if form.is_valid():
            match = form.save(commit=False)
            match.save()
            return redirect('accounts:employee-index')
    else:
        form = EmployeeMatchSkill()
    return render(request, 'employee/skillmatch.html', {'form': form})
