from django import forms
from .models import Staff, StaffShift, StaffAttendance

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'position']

class StaffShiftForm(forms.ModelForm):
    class Meta:
        model = StaffShift
        fields = ['shift', 'date']

class StaffAttendanceForm(forms.ModelForm):
    class Meta:
        model = StaffAttendance
        fields = ['date', 'is_present']
