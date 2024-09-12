from django.shortcuts import render,redirect,get_object_or_404
from .models import Position, Staff, Shift, StaffShift, StaffAttendance
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import HttpResponse
from faker import Faker
from .forms import StaffForm,StaffShiftForm,StaffAttendanceForm


def index(request):
    search_query = request.GET.get('search', '')
    
    staff_list = Staff.objects.all()
    shift_list = Shift.objects.all()
    staff_shift_list = StaffShift.objects.all()
    attendance_list = StaffAttendance.objects.all()

    if search_query:
        staff_list = staff_list.filter(
            first_name__icontains=search_query
        ) | staff_list.filter(
            last_name__icontains=search_query
        )

    staff_data = []
    for staff in staff_list:
        staff_shifts = staff_shift_list.filter(staff=staff)
        for staff_shift in staff_shifts:
            shift = shift_list.filter(id=staff_shift.shift.id).first()
            attendance = attendance_list.filter(staff=staff, date=staff_shift.date).first()
            staff_data.append({
                'staff': staff,
                'shift': shift,
                'staff_shift': staff_shift,
                'attendance': attendance
            })

    context = {
        'search_query': search_query,
        'staff_data': staff_data,
    }
    return render(request, 'index.html', context)
def register_user(request):
    """
    Foydalanuvchini ro'yxatdan o'tkazish
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Bu foydalanuvchi nomi allaqachon mavjud. Iltimos, boshqa nom tanlang.")
        else:
            user = User.objects.create_user(username=username)
            user.set_password(password)
            user.save()
            messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz! Iltimos, tizimga kiring.")
            return redirect('login_user')
    
    return render(request, 'register.html')

def login_user(request):
    """
    Ro'yxatdan o'tgan foydalanuvchini kirish
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Tizimga muvaffaqiyatli kirdingiz!")
            return redirect('index')  # 'index' sahifasiga yo'naltirish
        else:
            messages.error(request, "Login yoki parol xato. Iltimos, qaytadan urinib ko'ring.")
    
    return render(request, 'login.html')

def logout_user(request):
    """
    Foydalanuvchini tizimdan chiqarish
    """
    logout(request)
    messages.success(request, "Tizimdan muvaffaqiyatli chiqdingiz!")
    return redirect('login_user')




fake = Faker()

def populate_db(request):
    positions = ['Manager', 'Waiter', 'Chef', 'Bartender']
    for title in positions:
        Position.objects.get_or_create(title=title)

    for _ in range(10):
        Staff.objects.get_or_create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            position=Position.objects.order_by('?').first()
        )

    for _ in range(5):
        Shift.objects.get_or_create(
            start_time=fake.date_time_this_year(before_now=True, after_now=False),
            end_time=fake.date_time_this_year(before_now=False, after_now=True)
        )

   
    staff_list = Staff.objects.all()
    shift_list = Shift.objects.all()
    for _ in range(10):
        StaffShift.objects.get_or_create(
            staff=staff_list.order_by('?').first(),
            shift=shift_list.order_by('?').first(),
            date=fake.date_this_year()
        )

    for staff in staff_list:
        for _ in range(3):
            StaffAttendance.objects.get_or_create(
                staff=staff,
                date=fake.date_this_year(),
                is_present=fake.boolean()
            )

    return HttpResponse("Database populated with fake data!")


def add_staff(request):
    if request.method == 'POST':
        staff_form = StaffForm(request.POST)
        shift_form = StaffShiftForm(request.POST)
        attendance_form = StaffAttendanceForm(request.POST)
        if staff_form.is_valid() and shift_form.is_valid() and attendance_form.is_valid():
            staff = staff_form.save()
            shift = shift_form.save(commit=False)
            shift.staff = staff
            shift.save()
            attendance = attendance_form.save(commit=False)
            attendance.staff = staff
            attendance.save()
            return redirect('index') 
    else:
        staff_form = StaffForm()
        shift_form = StaffShiftForm()
        attendance_form = StaffAttendanceForm()
    return render(request, 'staff_add.html', {
        'staff_form': staff_form,
        'shift_form': shift_form,
        'attendance_form': attendance_form,
    })

def update_staff_attendance(request, pk):
    staff_attendance = get_object_or_404(StaffAttendance, pk=pk)
    if request.method == 'POST':
        form = StaffAttendanceForm(request.POST, instance=staff_attendance)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = StaffAttendanceForm(instance=staff_attendance)
    return render(request, 'update_staff_attendance.html', {'form': form})

def delete_staff_attendance(request, pk):
    staff_attendance = get_object_or_404(StaffAttendance, pk=pk)
    if request.method == 'POST':
        staff_attendance.delete()
        return redirect('index')
    return render(request, 'confirm_delete.html', {'object': staff_attendance})