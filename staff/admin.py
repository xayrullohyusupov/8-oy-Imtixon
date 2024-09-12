from django.contrib import admin
from .models import Position, Staff, Shift, StaffShift, StaffAttendance

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title']

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name']
    list_display = ['first_name', 'last_name', 'position']
    list_filter = ['position']

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ['start_time', 'end_time']

@admin.register(StaffShift)
class StaffShiftAdmin(admin.ModelAdmin):
    list_display = ['staff', 'shift', 'date']
    list_filter = ['shift', 'date']

@admin.register(StaffAttendance)
class StaffAttendanceAdmin(admin.ModelAdmin):
    list_display = ['staff', 'date', 'is_present']
    list_filter = ['date', 'is_present']
    search_fields = ['staff__first_name', 'staff__last_name']
