from rest_framework import serializers
from .models import Teacher,Class,Student,Mark

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model=Teacher
        fields=['id','name','phone_number','subject','password']
        extra_kwargs={'password':{'write_only':True}}

# class ClassSerializer(serializers.ModelSerializer):
#     teacher_name =serializers.CharField(source='teacher.name',read_only=True)
#     class Meta:
#         model=Class
#         fields=['id','name','teacher','teacher_name']
class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model=Class
        fields=['id','name']   
class StudentSerializer(serializers.ModelSerializer):
    student_class_name =serializers.CharField(source='Student_class.name',read_only=True)
    class Meta:
        model=Student
        fields=['id','name','reg_number','dob','sex','overall_score','Student_class','student_class_name']

class MarkSerializer(serializers.ModelSerializer):
    teacher_name =serializers.CharField(source='teacher.name',read_only=True)
    student_name =serializers.CharField(source='student.name',read_only=True)

    class Meta:
        model=Mark
        fields=['id','student','teacher','subject','assigment_marks','seminar_marks',  'assessment_marks',  'behaviour_marks','student_name',"teacher_name"]
    
       
       