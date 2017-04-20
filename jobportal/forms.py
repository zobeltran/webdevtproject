from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Employee, Client, Applicant, SkillMatching, JobOpportunity, Specialized
from django.contrib.auth import authenticate, login, logout

# Custom Input


class DateInput(forms.DateInput):
    input_type = 'date'


class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "My Object #%i" % obj.id

# Main Forms
# Registration


class EmployeeRegistration(UserCreationForm):
    civil_status_choices = (
        ('Single', 'Single'),
        ('Marrier', 'Married'),
    )
    email = forms.EmailField(required=True)
    Employee_No = forms.RegexField(required=True, regex=r'^([0-9\s]*)$',
                                   widget=forms.TextInput(),
                                   min_length=8, max_length=8,
                                   label="Employee No",
                                   error_messages={'invalid': "Employee number must only contain numbers"})
    Bldg_No = forms.RegexField(required=True,
                               regex=r'^([a-zA-Z0-9_ \s\-]*)$',
                               max_length=35, widget=forms.TextInput(),
                               label="Bldg No",
                               error_messages={'invalid': "This value may contain only letters, numbers and - characters."})
    Phone = forms.RegexField(required=True,
                             regex=r'^([0-9_\s\-]*)$',
                             widget=forms.TextInput(),
                             min_length=9, max_length=16,
                             label="Phone",
                             error_messages={'invalid': "This value may contain only numbers and - characters."})
    Mobile = forms.RegexField(required=True,
                              regex=r'^([0-9_\s\-]*)$',
                              widget=forms.TextInput(),
                              min_length=9, max_length=16,
                              label="Mobile",
                              error_messages={'invalid': "This value may contain only numbers and - characters."})
    Civil_Status = forms.ChoiceField(widget=forms.Select, choices=civil_status_choices)

    class Meta:
        model = Employee
        fields = (
            'email',
            'password1',
            'password2',
            'Employee_No',
            'First_Name',
            'Last_Name',
            'Bldg_No',
            'Street',
            'Municipality',
            'City',
            'Country',
            'Civil_Status',
            'Phone',
            'Mobile',
        )

        def save(self, commit=True):
            user = super(EmployeeRegistration, self).save(commit=False)
            user.Employee_No = self.cleaned_data['Employee_No']
            user.First_Name = self.cleaned_data['First_Name']
            user.Last_Name = self.cleaned_data['Last_Name']
            user.email = self.cleaned_data['email']
            user.Civil_Status = self.cleaned_data['Civil_Status']
            user.Phone = self.cleaned_data['Phone']
            user.Mobile = self.cleaned_data['Mobile']
            user.Bldg = self.cleaned_data['Bldg']
            user.Street = self.cleaned_data['Street']
            user.Municipality = self.cleaned_data['Municipality']
            user.City = self.cleaned_data['City']
            user.Country = self.cleaned_data['Country']

            if commit:
                user.save()
            return user


class ClientRegistration(UserCreationForm):
    Company_Name = forms.CharField(required=True, max_length=50)
    email = forms.EmailField(required=True, label="Representative's Email")
    First_Name = forms.CharField(label="Representative's First Name")
    Last_Name = forms.CharField(label="Representative's Last Name")
    Bldg_No = forms.RegexField(required=True,
                               regex=r'^([a-zA-Z0-9_ \s\-]*)$',
                               max_length=35, widget=forms.TextInput(),
                               label="Bldg No",
                               error_messages={'invalid': "This value may contain only letters, numbers and - characters."})
    Phone = forms.RegexField(required=True,
                             regex=r'^([0-9_\s\-]*)$',
                             widget=forms.TextInput(),
                             min_length=9, max_length=16,
                             label="Phone",
                             error_messages={'invalid': "This value may contain only numbers and - characters."})
    Mobile = forms.RegexField(required=True,
                              regex=r'^([0-9_\s\-]*)$',
                              widget=forms.TextInput(),
                              min_length=9, max_length=16,
                              label="Mobile",
                              error_messages={'invalid': "This value may contain only numbers and - characters."})

    class Meta:
        model = Client
        fields = (
            'email',
            'password1',
            'password2',
            'First_Name',
            'Last_Name',
            'Company_Name',
            'Logo',
            'Bldg_No',
            'Street',
            'Municipality',
            'City',
            'Country',
            'Phone',
            'Mobile',
            'Website',
        )

        def save(self, commit=True):
            user = super(ClientRegistration, self).save(commit=False)
            user.Company_Name = self.cleaned_data['Company_Name']
            user.Bldg_No = self.cleaned_data['Bldg_No']
            user.Street = self.cleaned_data['Street']
            user.Municipality = self.cleaned_data['Municipality']
            user.City = self.cleaned_data['City']
            user.Country = self.cleaned_data['Country']
            user.First_Name = self.cleaned_data['First_Name']
            user.Last_Name = self.cleaned_data['Last_Name']
            user.email = self.cleaned_data['email']
            user.Phone = self.cleaned_data['Phone']
            user.Mobile = self.cleaned_data['Mobile']
            user.Website = self.cleaned_data['Website']

            if commit:
                user.save()
            return user


class ApplicantRegistration(UserCreationForm):
    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    civil_status_choices = (
        ('Single', 'Single'),
        ('Marrier', 'Married'),
    )
    email = forms.EmailField(required=True)
    Bldg_No = forms.RegexField(required=True,
                               regex=r'^([a-zA-Z0-9_ \s\-]*)$',
                               max_length=35, widget=forms.TextInput(),
                               label="Bldg No",
                               error_messages={'invalid': "This value may contain only letters, numbers and - characters."})
    Phone = forms.RegexField(required=True,
                             regex=r'^([0-9_\s\-]*)$',
                             widget=forms.TextInput(),
                             min_length=9, max_length=16,
                             label="Phone",
                             error_messages={'invalid': "This value may contain only numbers and - characters."})
    Mobile = forms.RegexField(required=True,
                              regex=r'^([0-9_\s\-]*)$',
                              widget=forms.TextInput(),
                              min_length=9, max_length=16,
                              label="Mobile",
                              error_messages={'invalid': "This value may contain only numbers and - characters."})
    Gender = forms.ChoiceField(widget=forms.Select, choices=gender_choices)
    Civil_Status = forms.ChoiceField(widget=forms.Select, choices=civil_status_choices)

    class Meta:
        model = Applicant
        fields = (
            'email',
            'password1',
            'password2',
            'First_Name',
            'Last_Name',
            'NickName',
            'Birth_Date',
            'Birth_Place',
            'Gender',
            'Picture',
            'Civil_Status',
            'Bldg_No',
            'Street',
            'Municipality',
            'City',
            'Country',
        )
        widgets = {
            'Birth_Date': DateInput(),
        }
        help_texts = {
            'Birth_Date': 'Follow the format of Day/Month/Year. Example: 26/01/1996',
        }

        def save(self, commit=True):
            user = super(ApplicantRegistration, self), save(commit=False)
            user.First_Name = self.cleaned_data['First_Name']
            user.Last_Name = self.cleaned_data['Last_Name']
            user.NickName = self.cleaned_data['NickName']
            user.Birth_Date = self.cleaned_data['Birth_Date']
            user.Birth_Place = self.cleaned_data['Birth_Place']
            user.Civil_Status = self.cleaned_data['Civil_Status']
            user.Bldg_No = self.cleaned_data['Bldg_No']
            user.Street = self.cleaned_data['Street']
            user.Municipality = self.cleaned_data['Municipality']
            user.City = self.cleaned_data['City']
            user.Country = self.cleaned_data['Country']

            if commit:
                user.save()
            return user

# Log In


class ApplicantLogin(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = authenticate(username=email, password=password)
        if not user:
            raise forms.ValidationError("This user does not exist")
        if not user.check_password(password):
            raise forms.ValidationError("Incorrect password")
        if not user.is_active:
            raise forms.ValidationError("This user is no longer active.")
        return super(ApplicantLogin, self).clean(*args, **kwargs)


class EmployeeLogin(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = authenticate(username=email, password=password)
        if not user:
            raise forms.ValidationError("This user does not exist")
        if not user.check_password(password):
            raise forms.ValidationError("Incorrect password")
        if not user.is_active:
            raise forms.ValidationError("This user is no longer active.")
        return super(EmployeeLogin, self).clean(*args, **kwargs)


class ClientLogin(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = authenticate(username=email, password=password)
        if not user:
            raise forms.ValidationError("This user does not exist")
        if not user.check_password(password):
            raise forms.ValidationError("Incorrect password")
        if not user.is_active:
            raise forms.ValidationError("This user is no longer active.")
        return super(ClientLogin, self).clean(*args, **kwargs)


class EmployeeMatchSkill(forms.Form):
    Job = forms.ModelChoiceField(
        queryset=JobOpportunity.objects.all(), to_field_name="Job_Post")
    SpecSkill = forms.ModelMultipleChoiceField(
        queryset=Specialized.objects.all(), to_field_name="Specialization")

    class meta:
        model = SkillMatching
        fields = ['Job', 'SpecSkill']
