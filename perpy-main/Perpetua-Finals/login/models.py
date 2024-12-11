from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

DAYS_CHOICE = [('mon', 'Monday'), ('tue', 'Tuesday'), ('wed', 'Wednesday'), ('thu', 'Thursday'), ('fri', 'Friday'),
               ('sat', 'Saturday'), ]
LEAVE_CHOICE = [('ml', 'Medical Leave'), ('od', 'On Duty')]


class Department(models.Model):
    dept_id = models.CharField(max_length=20, primary_key=True)
    dept_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.dept_name} ({self.dept_id})"


class Admin(models.Model):
    admin_id = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=30)

    def __str__(self):
        return f"Admin: {self.admin_id}"


class Class(models.Model):
    class_id = models.CharField(max_length=20, primary_key=True)
    total_students = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])

    def __str__(self):
        return f"Class {self.class_id} - {self.total_students} students"


class Mentee(models.Model):
    mentee_id = models.CharField(max_length=20, primary_key=True)
    s_password = models.CharField(max_length=30)
    in_out = models.CharField(max_length=5)
    f_name = models.CharField(max_length=20)
    l_name = models.CharField(max_length=20)
    dept_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return f"Student: {self.f_name} {self.l_name} ({self.mentee_id}) - {self.dept_id} - {self.class_id}"


class Mentor(models.Model):
    mentor_id = models.CharField(max_length=20, primary_key=True)
    f_password = models.CharField(max_length=30)
    f_name = models.CharField(max_length=20)
    l_name = models.CharField(max_length=20)
    dept_id = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"Faculty: {self.f_name} {self.l_name} ({self.mentor_id}) - {self.dept_id}"


class Calender(models.Model):
    i = models.AutoField(primary_key=True)
    dates = models.DateField()
    day = models.CharField(max_length=9, choices=DAYS_CHOICE, default=None, blank=False)

    def __str__(self):
        return f"Calendar: {self.dates} - {self.day}"


class Course(models.Model):
    course_id = models.CharField(max_length=20, primary_key=True)
    course_name = models.CharField(max_length=50)
    credits = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"Course: {self.course_name} ({self.course_id}) - {self.credits} credits"


class Attendance(models.Model):
    mentee_id = models.ForeignKey(Mentee, on_delete=models.CASCADE)
    mentor_id = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    presence = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    periods = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)], default=1)

    class Meta:
        unique_together = (("mentee_id", "course_id", "date"),)

    def __str__(self):
        return f"Attendance: {self.mentee_id} - {self.course_id} on {self.date} - Presence: {self.presence} - Periods: {self.periods}"


class Slot(models.Model):
    period_id = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)], primary_key=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"Slot: Period {self.period_id} - {self.start_time} to {self.end_time}"


class Holiday(models.Model):
    date = models.DateField(primary_key=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"Holiday: {self.date} - {self.description}"


class Advisor(models.Model):
    mentor_id = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return f"Advisor: {self.mentor_id} - Class: {self.class_id}"


class Leave(models.Model):
    mentee_id = models.ForeignKey(Mentee, on_delete=models.CASCADE)
    reason = models.CharField(max_length=100)
    leave_type = models.CharField(max_length=9, choices=LEAVE_CHOICE, default=None, blank=False)
    approved = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1)])

    def __str__(self):
        approval_status = "Approved" if self.approved == 1 else "Not Approved"
        return f"Leave: {self.mentee_id} - {self.leave_type} - {self.reason} ({approval_status})"


class Timetable(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    day = models.CharField(max_length=9, choices=DAYS_CHOICE, default=None, blank=False)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    periods_id = models.ForeignKey(Slot, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("class_id", "course_id", "day", "periods_id"),)

    def __str__(self):
        return f"Timetable: {self.class_id} - {self.course_id} on {self.day} - Period {self.periods_id.period_id}"


class Teache(models.Model):
    mentor_id = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("course_id", "class_id"),)

    def __str__(self):
        return f"Teache: {self.mentor_id} teaching {self.course_id} for {self.class_id}"


class ClassJoinRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACCEPTED = 'accepted', 'Accepted'
        REJECTED = 'rejected', 'Rejected'

    teache_id = models.ForeignKey(Teache, on_delete=models.CASCADE)
    mentee_id = models.ForeignKey(Mentee, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Join Request: {self.mentee_id} - {self.teache_id} - {self.status}"

