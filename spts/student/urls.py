from django.urls import path
from .views import TeacherRegisterView,StudentRegisterView,ClassListView,TeacherLoginView,ClassRegisterView,StudentInfoView,MarksView,SubjectWiseMarksView
from .views import StudentDashBoardView,StudentLoginView,StudentProfileInfoView,StudentListView
urlpatterns=[
    path('teacher/register/', TeacherRegisterView.as_view()),
    path('student/register/',StudentRegisterView.as_view()),
    path('class/register/',ClassRegisterView.as_view()),
    path('teacher/login/',TeacherLoginView.as_view()),
    path('teacher/classes',ClassListView.as_view()),
    path('marks/',MarksView.as_view()),#add marks
    path('marks/<int:mark_id>/',MarksView.as_view()),
    path('student/login/',StudentLoginView.as_view()),
    path('student/<int:student_id>/',StudentInfoView.as_view()),
    path('student/<int:student_id>/dasboard/',StudentDashBoardView.as_view()),
    path('student/<int:student_id>/marks/<str:subject>/',SubjectWiseMarksView.as_view()),
    path('students/info/', StudentProfileInfoView.as_view()),
    path('class/<int:student_class>/students/',StudentListView.as_view()),
]
