from django.db import models

from user.models import User


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)


class Play(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    actors = models.ManyToManyField(to=Actor, related_name="plays")
    genres = models.ManyToManyField(to=Genre, related_name="plays")


class TheatreHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.PositiveIntegerField()
    seat_in_row = models.PositiveIntegerField()


class Performance(models.Model):
    play = models.ForeignKey(to=Play, related_name="performances", on_delete=models.CASCADE)
    theatre_hall = models.ForeignKey(to=TheatreHall, related_name="performances", on_delete=models.CASCADE)
    show_time = models.DateTimeField()


class Reservation(models.Model):
    created_at = models.DateTimeField()
    user = models.ForeignKey(to=User, related_name="reservations", on_delete=models.CASCADE)


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    performance = models.ForeignKey(to=Performance, related_name="tickets", on_delete=models.CASCADE)
    reservation = models.ForeignKey(to=Reservation, related_name="tickets", on_delete=models.CASCADE)
