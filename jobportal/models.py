from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.conf import settings
from django.core.urlresolvers import reverse

# Base User Manager for Custom User.


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        # Creates and Saves a User with the given email and password

        now = timezone.now()

        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_superuser,
                          last_login=now,
                          date_joined=now,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)

# Base Custom User


class CustomUser(AbstractBaseUser, PermissionsMixin):
    UserID = models.AutoField(primary_key=True)
    email = models.EmailField(blank=True, unique=True)
    First_Name = models.CharField(max_length=20)
    Last_Name = models.CharField(max_length=20)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['First_Name', 'Last_Name']

    objects = CustomUserManager()

    class Meta:  # Meta Data: Anything that isn't a field
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        full_info = "%s %s - %s" % (self.First_Name, self.Last_Name, self.email)
        return full_info.strip()

    def get_absolute_url(self):
        return "users/%s/" % urlquote(self.email)

    def get_full_name(self):
        # Returns the first_name with the last_name
        full_name = "%s %s" % (self.First_Name, self.Last_Name)
        return self.full_name.strip()

    def get_short_name(self):
        # Returns the short name for the user
        return self.First_Name

    def email_user(self, subject, message, from_email=None):
        # sends an email to this user
        send_mail(subject, message, from_email, [self.email])


# Classes with ForeignKey
class Applicant(CustomUser):
    ApplicantID = models.AutoField(primary_key=True)
    NickName = models.CharField(max_length=50)
    Birth_Date = models.DateField()
    Birth_Place = models.CharField(max_length=100)
    Gender = models.CharField(max_length=10)
    Civil_Status = models.CharField(max_length=20)
    Picture = models.FileField()
    Status = models.CharField(max_length=50, default="Applying")
    Bldg_No = models.CharField(max_length=50)
    Street = models.CharField(max_length=50)
    Municipality = models.CharField(max_length=50)
    City = models.CharField(max_length=50)
    Country = models.CharField(max_length=50)
    Phone = models.CharField(max_length=15)
    Mobile = models.CharField(max_length=11)

    def __str__(self):
        applicant = "%s - %s" % (self.NickName, self.Status)
        return applicant.strip()


class Employee(CustomUser):
    EmployeeID = models.AutoField(primary_key=True)
    # User = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Employee_No = models.CharField(max_length=15)
    Civil_Status = models.CharField(max_length=20)
    Phone = models.CharField(max_length=15)
    Mobile = models.CharField(max_length=11)
    Bldg_No = models.CharField(max_length=50)
    Street = models.CharField(max_length=50)
    Municipality = models.CharField(max_length=50)
    City = models.CharField(max_length=50)
    Country = models.CharField(max_length=50)

    def __str__(self):
        data = "%s - %s %s" % (self.Employee_No, self.First_Name, self.Last_Name)
        return self.data.strip()


class Client(CustomUser):
    ClientID = models.AutoField(primary_key=True)
    # User = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Company_Name = models.CharField(max_length=20)
    Logo = models.FileField()
    Bldg_No = models.CharField(max_length=50)
    Street = models.CharField(max_length=50)
    Municipality = models.CharField(max_length=50)
    City = models.CharField(max_length=50)
    Country = models.CharField(max_length=50)
    Phone = models.CharField(max_length=15)
    Mobile = models.CharField(max_length=11)
    Website = models.URLField()

    def __str__(self):
        return self.Company_Name


class Requirement(models.Model):
    RequirementID = models.AutoField(primary_key=True)
    User = models.OneToOneField(Applicant, on_delete=models.CASCADE)
    SSS = models.FileField()
    Phil_Health = models.FileField()
    TIN = models.FileField()
    NBI_Clearance = models.FileField()
    Marriage_Contract = models.FileField()
    TOR = models.FileField()
    Picture = models.FileField()
    Employee_Certificate = models.FileField()
    Clearance_To_Transfer = models.FileField()
    Clearance_From_SSS = models.FileField()

    def __str__(self):
        requirements = "%s's Requirements" % (self.User.NickName)
        return self.requirements


class Education(models.Model):
    EducationID = models.AutoField(primary_key=True)
    User = models.OneToOneField(Applicant, on_delete=models.CASCADE)
    School_Name = models.CharField(max_length=70)
    Education_Attained = models.CharField(max_length=100)

    def __str__(self):
        educational = "%s %s's Educational Background" % (self.User.First_Name, self.User.Last_Name)
        return educational


class JobOpportunity(models.Model):
    JobID = models.AutoField(primary_key=True)
    Client_Name = models.ForeignKey(Client, on_delete=models.CASCADE)
    Job_Post = models.CharField(max_length=50)
    Required_Applicants = models.PositiveIntegerField()

    def __str__(self):
        job = "%s - Applicant required: %s" % (self.Job_Post, self.Required_Applicants)
        return job.strip()

    class Meta:
        verbose_name = _('Job Opportunity')
        verbose_name_plural = _('Job Opportunities')


class Specialized(models.Model):
    SpecSkillsID = models.AutoField(primary_key=True)
    User = models.OneToOneField(Applicant, on_delete=models.CASCADE)
    Specialization = models.CharField(max_length=50)
    SubSkill = models.CharField(max_length=50)

    def __str__(self):
        skill = "%s - %s" % (self.Specialization, self.SubSkill)
        return skill.strip()

    class Meta:
        verbose_name = _('Specialization')
        verbose_name_plural = _('Specializations')


class SkillMatching(models.Model):
    SMID = models.AutoField(primary_key=True)
    Job = models.ForeignKey(JobOpportunity, on_delete=models.CASCADE)
    SpecSkill = models.ManyToManyField(Specialized)

    def __str__(self):
        sm = "%s - %s" % (self.Job.Job_Post, "Skill Matched")
        return sm
