from rest_framework import serializers
from .models import *

class FlightSerializer(serializers.ModelSerializer):   
    class Meta:
        model=Flight
        fields="__all__"

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Passenger
        fields="__all__"


class ReservationSerializer(serializers.ModelSerializer):
    flight=serializers.StringRelatedField()
    flight_id=serializers.IntegerField()

    user=serializers.StringRelatedField()
    user_id=serializers.IntegerField()
    # passenger=serializers.StringRelatedField()
    # passenger=serializers.IntegerField()
    passenger= PassengerSerializer(many=True)
    class Meta:
        model=Reservation
        fields=(
            "id",
            "flight", 
            "flight_id", 
            "user",  
            "user_id",
            "passenger"
            )
