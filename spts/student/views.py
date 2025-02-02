from django.shortcuts import render

# Create your views here.
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework import status
from .models import Teacher,Mark,Student,Class,Subject
from .serializers import StudentSerializer,MarkSerializer,ClassSerializer,TeacherSerializer,SubjectSerializer
from rest_framework.response import Response
from datetime import timezone
# class TeacherRegisterView(APIView):
#     def post(self,request):
#         serializer=TeacherSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message':"Teacher registered succesfully"},status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class TeacherRegisterView(APIView):
    def post(self, request):
        # Extract data from the request
        name = request.data.get('name')
        phone_number = request.data.get('phone_number')
        subject = request.data.get('subject')
        password = request.data.get('password')

        # Check if all required fields are provided
        if not name or not phone_number or not subject or not password:
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the teacher object and save to the database
        try:
            teacher = Teacher(
                name=name,
                phone_number=phone_number,
                subject=subject,
                password=password  # No need to hash here, as it's done in the model's save method
            )
            teacher.save()  # This will hash the password automatically through the model's save method
            return Response(
                {'message': 'Teacher registered successfully', 'teacher_id': teacher.id},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class StudentRegisterView(APIView):
    def post(self,request):
        serializer=StudentSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response({'message':"student registered succesfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




class ClassRegisterView(APIView):
    def post(self,request):
        serializer=ClassSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response({'message':"class registered succesfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class SubjectRegister(APIView):
    def post(self,request):
        serializer=SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':"class registered succesfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class TeacherLoginView(APIView):
    def post(self, request):
        phone = request.data.get('phone_number')
        password = request.data.get("password")
        
         
        if not phone or not password:
            return Response({'error': 'Phone number and password are required'}, status=status.HTTP_400_BAD_REQUEST)

         
        teacher = Teacher.objects.filter(phone_number=phone).first()
        
        if teacher and check_password(password, teacher.password):
            print({'teacher_id': teacher.id,"subject":teacher.subject})
            return Response({"message": "Login successful", 'teacher_id': teacher.id,"subject":teacher.subject})
        
      
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
class ClassListView(APIView):
    def get(self, request):
        classes=Class.objects.all()
        serializer=ClassSerializer(classes,many=True)
        return Response(serializer.data)
    


class SubjectListView(APIView):
    def get(self, request):
        subject=Subject.objects.all()
        serializer=SubjectSerializer(subject,many=True)
        return Response(serializer.data)
    
# class StudentListView(APIView):
#     def get(self,request,student_class):
#         students=Student.objects.filter(student_class_id=student_class)
#         serializer=StudentSerializer(students,many=True)
#         return Response(serializer.data)
class StudentListView(APIView):
    def get(self, request, student_class):
         
        students = Student.objects.filter(Student_class_id=student_class)
        
       
        serializer = StudentSerializer(students, many=True)
        
        return Response(serializer.data)


class StudentInfoView(APIView):
    def get(self,request,student_id):
        student=Student.objects.get(id=student_id)
        serializer=StudentSerializer(student)
        return Response(serializer.data)
   
class MarksViewe(APIView):
    def post(self,request):
        serializer=MarkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':"Marks added successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,mark_id):
        try:
             mark = Mark.objects.get(id=mark_id)
        except Mark.DoesNotExist:
            return Response({'error': 'Mark not found'}, status=status.HTTP_404_NOT_FOUND)

        mark=Mark.objects.get(id=mark_id)
        teacher_id=request.data.get("teacher_id")

        if mark.teacher.id != teacher_id:
            return Response({'error':'Permission denied'},status=status.HTTP_403_FORBIDDEN)
        
        serializer = MarkSerializer(mark, data=request.data , partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Marks updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MarksView(APIView):
    def post(self, request):
        # Creating a Mark serializer with the incoming data
        serializer = MarkSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'message': "Marks added successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, mark_id):
        try:
            # Fetch the Mark object
            mark = Mark.objects.get(id=mark_id)
        except Mark.DoesNotExist:
            # Return an error if the mark is not found
            return Response({'error': 'Mark not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the current teacher matches the teacher in the request
        teacher_id = request.data.get("teacher_id")
        
        # If the teacher does not match the one assigned to the mark, deny access
        if mark.teacher.id != teacher_id:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        # Partially update the mark (only the fields passed in the request)
        serializer = MarkSerializer(mark, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Marks updated successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class StudentLoginView(APIView):
#     def post(self, request):
#         reg_number=request.data.get("reg_number")
#         student=Student.objects.filter(reg_number=reg_number)
#         if student:
#             return Response({'message':'login succesfully' ,"student_id":student.id})
#         return Response({"erroe":'invalid ceridential'},status=status.HTTP_401_UNAUTHORIZED)
    
class StudentLoginView(APIView):
    def post(self, request):
        reg_number = request.data.get("reg_number")
        student = Student.objects.filter(reg_number=reg_number).first()  # .first() to get the first match or None

        if student:
            return Response({'message': 'login successfully', 'student_id': student.id})
        
        return Response({"error": 'invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# class StudentDashBoardView(APIView):
#     def get(self, request , student_id):
#         student = Student.objects.get(id=student_id)
#         marks = Mark.objects.filter(student=student)
#         serializer =MarkSerializer(marks, many=True)
#         total_marks=sum(marks.assessment_marks + marks.assiginment_marks +marks.seminar_marks + marks.behaviour_marks)
#         total_sub=marks.count()
#         data= {
#             'student_info':StudentSerializer(student).data,
#             'marks':marks,
#             'total_marks':total_marks,
#             'total_subject':total_sub,
#         }
#         return Response(data)
    

class StudentDashBoardView(APIView):
    def get(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        
        marks = Mark.objects.filter(student=student)
        
        # Calculate total_marks by iterating over the marks QuerySet
        total_mark = 0
        for mark in marks:
            total_mark += (mark.assessment_marks + mark.assigment_marks + mark.seminar_marks + mark.behaviour_marks)//4
        
        total_sub = marks.count()  # Count the number of subjects
        total_marks = total_mark//total_sub

        data = {
            'student_info': StudentSerializer(student).data,
            'marks': MarkSerializer(marks, many=True).data,  # Serialize marks for the response
            'total_marks': total_marks,
            'total_subject': total_sub,
        }
        
        return Response(data)


class SubjectWiseMarksView(APIView):
    def get(self,request,student_id , subject):
        marks = Mark.objects.filter(student_id=student_id,subject=subject)
        if marks:
            serializer=MarkSerializer(marks)
            return Response(serializer.data) 
        return Response({'error':'No marks found for given subject'}, status=status.HTTP_404_NOT_FOUND)
    

class StudentProfileInfoView(APIView):
    def get(self, request):
        students=Student.objects.all().order_by('-overall_score')
        data=[]
        for student in students:
            student_info={
                'name':student.name,
                'age':(timezone.now().year-student.dob.year),
                'class':student.Student_class.name,
                'reg_number':student.reg_number,
                'sex':student.sex,
                'overall_score':student.overall_score
            }
            data.append(student_info)
        return Response(data)