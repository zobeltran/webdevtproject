from django.contrib import admin
from .models import CustomUser, Employee, Client, Requirement
from .models import Education, SkillMatching, Applicant
from .models import Specialized, JobOpportunity

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Employee)
admin.site.register(Client)
admin.site.register(Applicant)
admin.site.register(Specialized)
admin.site.register(JobOpportunity)
admin.site.register(Requirement)
admin.site.register(Education)
admin.site.register(SkillMatching)
