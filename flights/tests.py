from django.test import TestCase
from rest_framework.test import APITestCase,APIRequestFactory,force_authenticate
from .views import FlightView
from django.contrib.auth.models import AnonymousUser,User
from rest_framework.authtoken.models import Token
from .models import Flight
# Create your tests here.
# class isminin sonu "TestCase" olmalı
class FlightTestCase(APITestCase):
    def setUp(self):
        
        self.factory=APIRequestFactory()

        self.user=User.objects.create_user(
            username='fatih',
            email='f@gmail.com',
            password='*secret11',
        )
        self.token=Token.objects.get(user=self.user)
        self.flight=Flight.objects.create(
            id=1,
            flight_number= "TK100", 
            operation_airlines= "THY", 
            departure_city= "Antalya", 
            arrival_city= "Amsterdam", 
            date_departure= "2022-12-03", 
            estimated_time= "15:27:22" 
        )
                    


    # fonksiyon yazarken "test" ile başlamalı

    def test_flight_list_as_guest(self):
        request=self.factory.get('/flights')
        response=FlightView.as_view({'get': 'list'})(request)
        # request.user=AnonymousUser
        self.assertEqual(response.status_code,200)   

    def test_flight_create_as_guest(self):
        request=self.factory.post('/flights')
        response=FlightView.as_view({'post': 'create'})(request)
        request.user=AnonymousUser()
        self.assertEqual(response.status_code,401)   

    def test_flight_create_as_login(self):
        request = self.factory.post('/flights', HTTP_AUTHORIZATION='Token ' + self.token.key)
        response=FlightView.as_view({'post': 'create'})(request)
        # request.user=AnonymousUser
        self.assertEqual(response.status_code,403)
    
    def test_flight_create_as_admin(self):
     
        data = {             
            "flight_number": "TK100", 
            "operation_airlines": "THY", 
            "departure_city": "Antalya", 
            "arrival_city": "Amsterdam", 
            "date_departure": "2022-12-03", 
            "estimated_time": "15:27:22" 
        }
       
        request = self.factory.post('/flights',data, HTTP_AUTHORIZATION='Token {}'.format(self.token))
        self.user.is_staff=True
        self.user.save()
        force_authenticate(request, user=self.user)
        response=FlightView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code,201)

    
    def test_flight_update_as_admin(self):
     
        data = {             
            "flight_number": "TK100", 
            "operation_airlines": "Lufthansa", 
            "departure_city": "berlin", 
            "arrival_city": "Amsterdam", 
            "date_departure": "2022-12-03", 
            "estimated_time": "15:27:22" 
        }
        request = self.factory.put('/flights/1',data, HTTP_AUTHORIZATION='Token {}'.format(self.token))
        self.user.is_staff=True
        self.user.save()
        force_authenticate(request, user=self.user)
        response=FlightView.as_view({'put': 'update'})(request,pk='1')
        self.assertEqual(response.status_code,200)

    def test_flight_str(self):
        self.assertEqual(str(self.flight),f"{self.flight.flight_number} - {self.flight.departure_city}- {self.flight.arrival_city}")
