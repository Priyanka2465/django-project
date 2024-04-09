from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    usertype=models.CharField(max_length=20,default="user")
    email=models.EmailField()
    firstname=models.CharField(max_length=20)
    lastname=models.CharField(max_length=20)
    mobile=models.PositiveBigIntegerField()
    password=models.CharField(max_length=20)
    profile=models.ImageField(default="",upload_to="picture/")


    def __str__(self):
        return self.firstname
    
class Event(models.Model):
    manager=models.ForeignKey(User,on_delete=models.CASCADE)
    event_name=models.CharField(max_length=100)
    event_date=models.CharField(max_length=100)
    event_venue=models.CharField(max_length=100)
    event_time=models.CharField(max_length=100)
    event_price=models.PositiveIntegerField()
    event_desc=models.TextField()
    event_image=models.ImageField(upload_to="event_images")

    def __str__(self):
        return self.manager.firstname + "-" + self.event_name
    
class BookEvent(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    booking_date=models.DateTimeField(default=timezone.now)
    payment_status=models.BooleanField(default=False)

    def __str__(self):
        return self.user.firstname + "-" + self.event.event_name