from django.shortcuts import render
from .models import *
from .serializers import FlightSerializer,ReservationSerializer,PassengerSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from .permissions import IsAdminOrReadOnly
from datetime import datetime,date

# Create your views here.
class FlightView(viewsets.ModelViewSet):
    queryset=Flight.objects.all()
    serializer_class=FlightSerializer
    # permission_classes= [IsAdminUser]  
    permission_classes= [IsAdminOrReadOnly]  

    # şu andan onceki uçuşları getirme
    def get_queryset(self):
        queryset = super().get_queryset()

        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')
        today = date.today()
        
        if self.request.user.is_staff: 
            return queryset
        else:
            # print(now) 
            # now o anki tarih ve zamanı alıyor
            # "2023-08-07 13:42:46.564569"
            #__gt great then
           #__gte great then or equal
           #__lt less then 
           #__lte less then or equal
            queryset = Flight.objects.filter(date_departure__gt=now)

            # if Flight.objects.filter(date_departure=today):
            #     today_qs = Flight.objects.filter(date_departure=today).filter(estimated_time__gt=current_time)
            #     queryset = queryset.union(today_qs)
                
            return queryset

class ReservationView(viewsets.ModelViewSet):

    queryset=Reservation.objects.all()
    serializer_class=ReservationSerializer
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)

class PassengerView(viewsets.ModelViewSet):
    queryset=Passenger.objects.all()
    serializer_class=PassengerSerializer