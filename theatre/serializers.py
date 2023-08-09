from rest_framework import serializers

from theatre.models import (
    Genre,
    Actor,
    Play,
    TheatreHall,
    Performance,
    Reservation,
    Ticket
)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = "__all__"


class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = "__all__"


class PlaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Play
        fields = "__all__"


class PlayListSerializer(PlaySerializer):
    genres = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    actors = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )


class TheatreHallSerializer(serializers.ModelSerializer):

    class Meta:
        model = TheatreHall
        fields = "__all__"


class PerformanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Performance
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = "__all__"
