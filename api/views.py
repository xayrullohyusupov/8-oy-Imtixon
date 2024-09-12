from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from staff.models import Position, Staff, Shift, StaffShift, StaffAttendance
from .serializers import PositionSerializer, StaffSerializer, ShiftSerializer, StaffShiftSerializer, StaffAttendanceSerializer

class IsStaffPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsAuthenticatedPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
class IsStaffOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user

class PositionList(APIView):
    permission_classes = [IsStaffPermission]

    def get(self, request):
        positions = Position.objects.all()
        serializer = PositionSerializer(positions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PositionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PositionDetail(APIView):
    permission_classes = [IsStaffPermission]

    def get(self, request, pk):
        position = Position.objects.get(pk=pk)
        serializer = PositionSerializer(position)
        return Response(serializer.data)

    def put(self, request, pk):
        position = Position.objects.get(pk=pk)
        serializer = PositionSerializer(position, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        position = Position.objects.get(pk=pk)
        position.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StaffList(APIView):
    permission_classes = [IsAuthenticatedPermission]

    def get(self, request):
        staff = Staff.objects.all()
        serializer = StaffSerializer(staff, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_staff:
            serializer = StaffSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)

class StaffDetail(APIView):
    permission_classes = [IsAuthenticatedPermission]

    def get(self, request, pk):
        staff = Staff.objects.get(pk=pk)
        serializer = StaffSerializer(staff)
        return Response(serializer.data)

    def put(self, request, pk):
        if request.user.is_staff:
            staff = Staff.objects.get(pk=pk)
            serializer = StaffSerializer(staff, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        if request.user.is_staff:
            staff = Staff.objects.get(pk=pk)
            staff.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

class ShiftList(APIView):
    permission_classes = [IsStaffPermission]

    def get(self, request):
        shifts = Shift.objects.all()
        serializer = ShiftSerializer(shifts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ShiftSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShiftDetail(APIView):
    permission_classes = [IsStaffPermission]

    def get(self, request, pk):
        shift = Shift.objects.get(pk=pk)
        serializer = ShiftSerializer(shift)
        return Response(serializer.data)

    def put(self, request, pk):
        shift = Shift.objects.get(pk=pk)
        serializer = ShiftSerializer(shift, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        shift = Shift.objects.get(pk=pk)
        shift.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StaffShiftList(APIView):
    permission_classes = [IsStaffPermission]

    def get(self, request):
        staff_shifts = StaffShift.objects.all()
        serializer = StaffShiftSerializer(staff_shifts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StaffShiftSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StaffShiftDetail(APIView):
    permission_classes = [IsStaffPermission]

    def get(self, request, pk):
        staff_shift = StaffShift.objects.get(pk=pk)
        serializer = StaffShiftSerializer(staff_shift)
        return Response(serializer.data)

    def put(self, request, pk):
        staff_shift = StaffShift.objects.get(pk=pk)
        serializer = StaffShiftSerializer(staff_shift, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        staff_shift = StaffShift.objects.get(pk=pk)
        staff_shift.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StaffAttendanceList(APIView):
    permission_classes = [IsAuthenticatedPermission]

    def get(self, request):
        staff_attendance = StaffAttendance.objects.all()
        serializer = StaffAttendanceSerializer(staff_attendance, many=True)
        return Response(serializer.data)

class StaffAttendanceDetail(APIView):
    permission_classes = [IsStaffOrOwner]

    def get(self, request, pk):
        staff_attendance = StaffAttendance.objects.get(pk=pk)
        serializer = StaffAttendanceSerializer(staff_attendance)
        return Response(serializer.data)
