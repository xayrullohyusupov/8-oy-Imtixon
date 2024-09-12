from django.urls import path
from .views import PositionList, PositionDetail, StaffList, StaffDetail, ShiftList, ShiftDetail, StaffShiftList, StaffShiftDetail, StaffAttendanceList, StaffAttendanceDetail

urlpatterns = [
    path('positions/', PositionList.as_view(), name='position-list'),
    path('positions/<int:pk>/', PositionDetail.as_view(), name='position-detail'),
    
    path('staff/', StaffList.as_view(), name='staff-list'),
    path('staff/<int:pk>/', StaffDetail.as_view(), name='staff-detail'),
    
    path('shifts/', ShiftList.as_view(), name='shift-list'),
    path('shifts/<int:pk>/', ShiftDetail.as_view(), name='shift-detail'),
    
    path('staff-shifts/', StaffShiftList.as_view(), name='staff-shift-list'),
    path('staff-shifts/<int:pk>/', StaffShiftDetail.as_view(), name='staff-shift-detail'),
    
    path('staff-attendance/', StaffAttendanceList.as_view(), name='staff-attendance-list'),
    path('staff-attendance/<int:pk>/', StaffAttendanceDetail.as_view(), name='staff-attendance-detail'),
]
