import csv

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

from login.models import Department, Mentee, Attendance, Teache

# Create your views here.
stu = ""
dep = ""
cla = ""
cou = ""


def initial(stut, dept):
    global stu, dep
    stu = stut
    dep = dept
    return


def tial(clat, cout):
    global cla, cou
    cla = clat
    cou = cout
    print(clat)
    print(cout)
    return


def studlogin(request):
    if request.method == "POST":
        u, p = request.POST.get('email'), request.POST.get('password')
        stud = Mentee.objects.filter(mentee_id=u)
        if stud.exists():
            if stud.get().s_password == p:
                d = stud.get().dept_id.dept_id
                initial(u, d)
                return studindex(request)
            else:
                messages.error(request, 'Invalid Credentials')
                return redirect('index')
        else:
            messages.error(request, 'No such User exists')
            return redirect('index')
    else:
        messages.error(request, 'Enter Credentials')
        return redirect('index')


def studprofile(request):
    if request.method == "POST":
        try:
            stud = Mentee.objects.filter(mentee_id=stu)
            fn = request.POST.get('fn')
            ln = request.POST.get('ln')
            pa = request.POST.get('pass')
            if fn != "":
                Mentee.objects.filter(mentee_id=stu).update(f_name=fn)
            if ln != "":
                Mentee.objects.filter(mentee_id=stu).update(l_name=ln)
            if pa != "":
                Mentee.objects.filter(mentee_id=stu).update(f_password=pa)
        except:
            messages.error(request, 'Oops something went wrong!')
            return redirect('studprofile')
    stud = Mentee.objects.filter(mentee_id=stu)
    print(stud)
    return render(request, 'studprofile.html', {'stu': stud.get()})


def studindex(request):
    dept = Department.objects.filter(dept_id=dep)
    stud = Mentee.objects.filter(mentee_id=stu)
    atte = Attendance.objects.all().filter(mentee_id=stu).order_by('-date')
    cour, cou = [], []
    for i in atte:
        if i.course_id not in cour:
            cour.append(i.course_id)
    for i in cour:
        cou.append([i.course_id, 0, Attendance.objects.all().filter(mentee_id=stu, course_id=i.course_id).count(), 0,
                    i.course_name])
    for i in atte:
        for j in range(len(cou)):
            if i.course_id.course_id == cou[j][0]:
                if i.presence:
                    cou[j][1] += 1
    for i in cou:
        i[3] = int(i[1] / i[2] * 100)
    coud = []
    for i in cou:
        if i[3] <= 75:
            coud.append(i)

    teach_list = Teache.objects.select_related('mentor_id', 'course_id', 'class_id')

    return render(request, 'studindex.html', {'stud': stud, 'cou': coud, 'teach_list':teach_list})


def studadd(request):
    dept = Department.objects.filter(dept_id=dep)
    stud = Mentee.objects.filter(mentee_id=stu)
    atte = Attendance.objects.all().filter(mentee_id=stu).order_by('-date')
    cour, cou = [], []
    for i in atte:
        if i.course_id not in cour:
            cour.append(i.course_id)
    for i in cour:
        cou.append([i.course_id, 0, Attendance.objects.all().filter(mentee_id=stu, course_id=i.course_id).count(), 0,
                    i.course_name])
    for i in atte:
        for j in range(len(cou)):
            if i.course_id.course_id == cou[j][0]:
                if i.presence:
                    cou[j][1] += 1
    for i in cou:
        i[3] = int(i[1] / i[2] * 100)
    print(cou)
    return render(request, 'studadd.html', {'stud': stud, 'cou': cou})


def stud_report(request):
    if request.method == "POST":
        dict = request.POST
        for i in dict.keys():
            if i != 'csrfmiddlewaretoken':
                j = i
                break
        p = j
        tial(cla, p)
    a = [1]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="AttendanceReport.csv"'
    stud = Mentee.objects.all().filter(mentee_id=stu)
    atte = Attendance.objects.all().filter(course_id=cou, mentee_id=stu).order_by('mentor_id', 'date')
    writer = csv.writer(response)

    writer.writerow(['Mentor-Id', 'Class-Id', 'Dept', 'Course-Id', 'Date', 'Status'])
    for i in atte:
        if i.presence:
            writer.writerow(
                [i.mentor_id.mentor_id, stud.get().class_id.class_id, stud.get().dept_id.dept_id, cou, i.date,
                 'Present'])
        else:
            writer.writerow(
                [i.mentor_id.mentor_id, stud.get().class_id.class_id, stud.get().dept_id.dept_id, cou, i.date,
                 'Absent'])
    return response


from django.views import View
from django.shortcuts import get_object_or_404
from login.models import ClassJoinRequest


class JoinClassView(View):
    def post(self, request):
        class_id = request.POST.get('class_id')
        print(class_id)
        mentee = get_object_or_404(Mentee, mentee_id=stu)
        teache = get_object_or_404(Teache, class_id=class_id)

        # Check if the mentee is already an attendant in the specific class
        is_attendant = Attendance.objects.filter(mentee_id=mentee, course_id=teache.course_id).exists()

        if is_attendant:
            messages.info(request, 'You are already an attendant in this class.')
        else:
            # Check for the latest request
            latest_request = ClassJoinRequest.objects.filter(mentee_id=mentee, teache_id=teache).order_by(
                '-created_at').first()

            if latest_request and latest_request.status == 'pending':
                messages.info(request, 'You have already requested to join this class.')
            else:
                join_request = ClassJoinRequest.objects.create(mentee_id=mentee, teache_id=teache)
                messages.success(request, 'Join request created successfully.')

        return redirect('studindex')



