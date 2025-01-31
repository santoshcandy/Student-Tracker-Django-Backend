from django.db import models

# Create your models here.
 
from django.contrib.auth.hashers import make_password

# class Teacher(models.Model):
#     name = models.CharField(max_length=100)
#     phone_number = models.CharField(max_length=15, unique=True)
#     subject = models.CharField(max_length=30)
#     password = models.CharField(max_length=255)  # Increase length for the hashed password

#     def save(self, *args, **kwargs):
#         # Hash the password before saving
#         if self.password:
#             self.password = make_password(self.password)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    subject = models.CharField(max_length=30)
    password = models.CharField(max_length=255)  # Increase length for the hashed password

    def save(self, *args, **kwargs):
        # Hash the password before saving if it exists
        if self.password and not self.password.startswith('$'):  # Ensure password isn't already hashed
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Class(models.Model):
    name= models.CharField(max_length=20,unique=True)
#    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,related_name="classes")

    def __str__(self):
        return self.name

class Student(models.Model):
    name=models.CharField(max_length=100)
    reg_number = models.CharField(max_length=20,unique=True)
    dob=models.DateField()
    sex=models.CharField(max_length=10, choices=(("Male","male"),("Female","female")))
    overall_score=models.FloatField(default=0)
    Student_class=models.ForeignKey(Class,on_delete=models.CASCADE,related_name="student")

    def __str__(self):
        return f"{self.name}-{self.reg_number}"
    

class Mark(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name="marks")
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE,related_name="marks")
    subject=models.CharField(max_length=100)
    assessment_marks=models.FloatField(default=0)
    seminar_marks=models.FloatField(default=0)
    assigment_marks=models.FloatField(default=0)
    behaviour_marks=models.FloatField(default=0)


    class Meta:
        unique_together=("student","subject")
    
    def total_score(self):
        return self.assessment_marks+self.seminar_marks+self.behaviour_marks

    def __str__(self):
        return f"{self.student.name}-{self.subject}"







    