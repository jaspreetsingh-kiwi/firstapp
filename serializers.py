# import serializer from rest_framework
from rest_framework import serializers
  
# import model from models.py
from .models import Booking
from .models import Passenger

# Create a model serializer 


class PassengerSerializer(serializers.ModelSerializer):
    """
    It will automatically generate a set of fields for Passenger Model.
    It will automatically generate validators for the Passenger serializer.
    """
    aadhar=serializers.CharField(min_length=12,max_length=12)
    passport=serializers.CharField(min_length=9,max_length=9)
    
    # specify model and fields
    class Meta:
        model = Passenger
        fields = ('pass_Name', 'ptype', 'email', 'phone', 'dob', 'age', 'passport' , 'aadhar')

    #validate aadhar is in digit or else show invalid aadhar number 
    def validate_aadhar(self,value):
        if value.isdigit():
             return value
        else:
             raise serializers.ValidationError('invalid aadhar number')

    #validate passport is in aplhanumeric or else show invalid passport number 
    def validate_passport(self,value):
        if value.isalnum() and not value.isalpha() and not value.isdigit():
             return value
        else:
             raise serializers.ValidationError('invalid passport number')

    

# Create a model serializer 

class BookingSerializer(serializers.ModelSerializer):
    """
    It will automatically generate a set of fields for Booking Model.
    It will automatically generate validators for the Booking serializer.
    """
    passenger = PassengerSerializer(many=True)
    pan = serializers.CharField(min_length=10,max_length=10)
    # specify model and fields
    class Meta:
        model = Booking
        fields = ('user','email', 'phone', 'pan','passenger')


    def create(self, validated_data):
        email =  validated_data.pop('email')
        phone =  validated_data.pop('phone')
        pan =  validated_data.pop('pan')
        passengers =  validated_data.pop('passenger')
        user =  validated_data.pop('user')

        booking = Booking.objects.create(user=user, email=email , phone=phone, pan=pan)
        for passenger in passengers:
            Passenger.objects.create(booking=booking, **passenger)

        return booking

    #validate pan  is in alphanumeric or not else show invalid pan number 
    def validate_pan(self,value):
        if value.isalnum() and not value.isalpha()  and not value.isdigit():
             return value
        else:
             raise serializers.ValidationError('invalid pan number')


