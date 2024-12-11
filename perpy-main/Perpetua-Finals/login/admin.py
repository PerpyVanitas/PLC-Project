import csv

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.db import models
from django.http import HttpResponse
from django.urls import path

from .models import Department, Class, Mentee, Mentor, Calender, Course, Attendance, Timetable, Teache, ClassJoinRequest

admin.site.site_header = 'ADMIN ACCOUNT'
admin.site.site_title = 'Smart Attendance Manager |'
admin.site.index_title = ""


class AttendanceD(models.Model):
    class Meta:
        verbose_name_plural = 'Attendance Report'
        app_label = 'login'


def my_custom_view(request):
    a = [1]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="AttendanceReport.csv"'
    atte = Attendance.objects.all().order_by('mentee_id', 'course_id', 'date')
    writer = csv.writer(response)
    writer.writerow(['Stud-Id', 'Faculty-Id', 'Dept', 'Course-Id', 'Date(dd-mm-yyyy)', 'Status'])
    for i in atte:
        if i.presence:
            writer.writerow(
                [i.mentee_id.mentee_id, i.mentor_id.mentor_id, i.mentee_id.dept_id.dept_id, i.course_id.course_id,
                 i.date,
                 'Present'])
        else:
            writer.writerow(
                [i.mentee_id.mentee_id, i.mentor_id.mentor_id, i.mentee_id.dept_id.dept_id, i.course_id.course_id,
                 i.date,
                 'Absent'])
    return response


class DummyModelAdmin(admin.ModelAdmin):
    model = AttendanceD

    def get_urls(self):
        view_name = '{}_{}_changelist'.format(
            self.model._meta.app_label, self.model._meta.model_name)
        return [
            path('my_admin_path/', my_custom_view, name=view_name),
        ]


class StudAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj:
            fields.remove('s_password')
        return fields


class FacAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj:
            fields.remove('f_password')
        return fields


admin.site.register(Mentee, StudAdmin)
admin.site.register(AttendanceD, DummyModelAdmin)
admin.site.register(Department)
admin.site.register(Class)
admin.site.register(Mentor, FacAdmin)
admin.site.register(Calender)
admin.site.register(Course)
admin.site.register(Attendance)
admin.site.register(Timetable)
admin.site.register(Teache)
admin.site.register(ClassJoinRequest)
admin.site.unregister(User)
admin.site.unregister(Group)
