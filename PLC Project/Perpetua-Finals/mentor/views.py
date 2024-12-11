import csv
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from login.models import Department, Admin, Class, Mentee, Mentor, Calender, Course, Attendance, Timetable, Teache
from django.contrib import messages

# Create your views here.
fac = ""
dep = ""
cla = ""
cou = ""


def initial(fact, dept):
    global fac, dep
    fac = fact
    dep = dept
    return


def tial(clat, cout):
    global cla, cou
    cla = clat
    cou = cout
    return


def faclogin(request):
    if request.method == "POST":
        u, p = request.POST.get('email'), request.POST.get('password')
        faco = Mentor.objects.filter(mentor_id=u)
        if faco.exists():
            if faco.get().f_password == p:
                d = faco.get().dept_id.dept_id
                initial(u, d)
                return updatedindex(request)
            else:
                messages.error(request, 'Invalid Credentials')
                return redirect('index')
        else:
            messages.error(request, 'No such User exists')
            return redirect('index')
    else:
        messages.error(request, 'Enter Credentials')
        return redirect('index')


def updatedprofile(request):
    if request.method == "POST":
        try:
            fact = Mentor.objects.filter(mentor_id=fac)
            fn = request.POST.get('fn')
            ln = request.POST.get('ln')
            pa = request.POST.get('pass')
            if fn != "":
                Mentor.objects.filter(mentor_id=fac).update(f_name=fn)
            if ln != "":
                Mentor.objects.filter(mentor_id=fac).update(l_name=ln)
            if pa != "":
                Mentor.objects.filter(mentor_id=fac).update(f_password=pa)
            di = fact.get().dept_id.dept_id
        except:
            messages.error(request, 'Oops something went wrong!')
            return redirect('updatedadd')
    faco = Mentor.objects.filter(mentor_id=fac)
    dept = Department.objects.filter(dept_id=dep)
    teach = Teache.objects.filter(mentor_id=fac)
    clas = []
    for i in teach:
        clas.append([i.class_id.class_id, i.course_id.course_id])
    return render(request, 'updatedprofile.html', {'clas': clas, 'fac': faco.get(), 'dept': dept.get()})


def editatt(request):
    dept = Department.objects.filter(dept_id=dep)
    faco = Mentor.objects.filter(mentor_id=fac)
    teach = Teache.objects.filter(mentor_id=fac)
    clao = Class.objects.filter(class_id=cla)
    couo = Course.objects.filter(course_id=cou)
    stud = Mentee.objects.all().filter(class_id=cla)
    atte = Attendance.objects.all().filter(course_id=cou, mentor_id=fac).order_by('-date')
    if request.method == "POST":
        dict = request.POST
        for stud1 in stud:
            if stud1.mentee_id in dict.keys():
                if dict.get('bate'):
                    try:
                        a = Attendance.objects.filter(mentee_id=stud1, mentor_id=faco.get(), course_id=couo.get(),
                                                      date=dict.get('bate')).get()
                        if a.presence:
                            p = 0
                        else:
                            p = 1
                        Attendance.objects.filter(mentee_id=stud1, mentor_id=faco.get(), course_id=couo.get(),
                                                  date=dict.get('bate')).update(presence=p)
                        messages.success(request, 'Attendance Edited.')
                    except:
                        print(dict.get('bate').exists())
                        messages.error(request, 'Value does not Exist')
                        return redirect('updatedadd')
    return redirect('updatedadd')


def updatedindex(request):
    dept = Department.objects.filter(dept_id=dep)
    faco = Mentor.objects.filter(mentor_id=fac)
    teach = Teache.objects.filter(mentor_id=fac)
    clas = []
    for i in teach:
        clas.append([i.class_id.class_id, i.course_id.course_id])
    return render(request, 'updatedindex.html', {'clas': clas, 'teach': teach})


def updatedadd(request):
    dept = Department.objects.filter(dept_id=dep)
    faco = Mentor.objects.filter(mentor_id=fac)
    teach = Teache.objects.filter(mentor_id=fac)
    clas = []
    for i in teach:
        clas.append([i.class_id.class_id, i.course_id.course_id])
    clao = Class.objects.filter(class_id=cla)
    couo = Course.objects.filter(course_id=cou)
    stud = Mentee.objects.all().filter(class_id=cla)
    atte = Attendance.objects.all().filter(course_id=cou, mentor_id=fac).order_by('-date')
    if request.method == "POST":
        n = request.POST.get('classg')
        if n is not None:
            n, p = n[:n.find('$')], n[n.find('$') + 1:]
            tial(n, p)
        dict = request.POST
        for stud1 in stud:
            if stud1.mentee_id in dict.keys():
                p = 0
            else:
                p = 1
            if dict.get('bate'):
                try:
                    a = Attendance(mentee_id=stud1, mentor_id=faco.get(), course_id=couo.get(), date=dict.get('bate'),
                                   presence=p)
                    a.save()
                    messages.success(request, 'Attendance Added.')
                except Exception as e:
                    messages.error(request, f'Value already Exists {e}')
                    return redirect('updatedadd')
    clao = Class.objects.filter(class_id=cla)
    couo = Course.objects.filter(course_id=cou)
    stud = Mentee.objects.all().filter(class_id=cla)
    dept = Department.objects.filter(dept_id=dep)
    faco = Mentor.objects.filter(mentor_id=fac)
    teach = Teache.objects.filter(mentor_id=fac)
    if stud.exists():
        dept = stud.first().dept_id
    else:
        dept = dept.get()
    atte = Attendance.objects.all().filter(course_id=cou, mentor_id=fac).order_by('-date')
    join_requests = ClassJoinRequest.objects.all().filter(teache_id__class_id=cla, teache_id__course_id=cou, status=ClassJoinRequest.Status.PENDING)
    return render(request, 'updatedadd.html',
                  {'stud': stud, 'fac': faco.get(), 'clat': clao.get(), 'cout': couo.get(), 'dept': dept, 'atte': atte,
                   'clas': clas, 'join_requests': join_requests})


def fac_report(request):
    if request.method == "POST":
        dict = request.POST
        for i in dict.keys():
            if i != 'csrfmiddlewaretoken':
                j = i
                break
        n, p = j[:j.find('$')], j[j.find('$') + 1:]
        tial(n, p)
    a = [1]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="AttendanceReport.csv"'
    stud = Mentee.objects.all().filter(class_id=cla)
    atte = Attendance.objects.all().filter(course_id=cou, mentor_id=fac).order_by('mentee_id', 'date')
    writer = csv.writer(response)

    writer.writerow(['Stud-Id', 'Class-Id', 'Dept', 'Course-Id', 'Date', 'Status'])
    for i in atte:
        if i.mentee_id in stud:
            if i.presence:
                writer.writerow([i.mentee_id.mentee_id, cla, dep, cou, i.date, 'Present'])
            else:
                writer.writerow([i.mentee_id.mentee_id, cla, dep, cou, i.date, 'Absent'])
    return response


from django.utils import timezone
from django.views import View
from django.shortcuts import get_object_or_404
from login.models import ClassJoinRequest, Attendance


class UpdateJoinStatusView(View):
    def post(self, request):
        join_request_id = request.POST.get('join_request_id')
        new_status = request.POST.get('status')
        print(join_request_id, new_status)
        join_request = get_object_or_404(ClassJoinRequest, id=join_request_id)

        join_request.status = new_status
        join_request.save()

        if new_status == ClassJoinRequest.Status.ACCEPTED:
            mentee = join_request.mentee_id
            teache = join_request.teache_id
            course = teache.course_id
            Attendance.objects.create(
                mentee_id=mentee,
                mentor_id=teache.mentor_id,
                course_id=course,
                date=timezone.now().date(),
                presence=1,
                periods=1
            )
            messages.success(request, 'Join request accepted')
        elif new_status == ClassJoinRequest.Status.REJECTED:
            messages.info(request, 'Join request rejected.')

        return redirect('updatedadd')
