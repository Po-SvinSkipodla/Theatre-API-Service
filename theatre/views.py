from django.shortcuts import render
from rest_framework import viewsets

from theatre.models import (
    Genre,
    Actor,
    Ticket,
    Reservation,
    Performance,
    TheatreHall,
    Play,
)
from theatre.serializers import (
    GenreSerializer,
    ActorSerializer,
    TicketSerializer,
    ReservationSerializer,
    PerformanceSerializer,
    TheatreHallSerializer,
    PlaySerializer, PlayListSerializer,
)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.prefetch_related("genres", "actors")
    serializer_class = PlaySerializer

    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer

        return PlaySerializer


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
