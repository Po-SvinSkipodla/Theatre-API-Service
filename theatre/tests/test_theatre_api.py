from django.test import TestCase
from user.models import User
from rest_framework.test import APIClient
from rest_framework import status
from theatre.models import Genre, Actor, Play, TheatreHall, Performance, Reservation, Ticket
from theatre.serializers import GenreSerializer, ActorSerializer, PlayListSerializer, TheatreHallSerializer, \
    PerformanceSerializer, ReservationSerializer, TicketSerializer


class GenreViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="testuser@test.com",
            password="testpassword"
        )
        self.genre_data = {
            "name": "Drama"
        }
        self.genre = Genre.objects.create(name="Comedy")

    def test_create_genre(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post("/genres/", self.genre_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        genre = Genre.objects.get(name="Drama")
        self.assertEqual(genre.name, "Drama")

    def test_list_genres(self):
        response = self.client.get("/genres/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn(GenreSerializer(self.genre).data, response.data)

    def test_retrieve_genre(self):
        response = self.client.get(f"/genres/{self.genre.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["name"], self.genre.name)

    def test_update_genre(self):
        self.client.force_authenticate(user=self.user)

        updated_data = {"name": "Romance"}
        response = self.client.put(f"/genres/{self.genre.id}/", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_genre = Genre.objects.get(id=self.genre.id)
        self.assertEqual(updated_genre.name, "Romance")

    def test_delete_genre(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(f"/genres/{self.genre.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Genre.DoesNotExist):
            Genre.objects.get(id=self.genre.id)


class ActorViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="testuser@test.com",
            password="testpassword"
        )
        self.actor = Actor.objects.create(first_name="John", last_name="Doe")

    def test_list_actors(self):
        response = self.client.get("/actors/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = ActorSerializer(self.actor).data
        self.assertIn(serializer_data, response.data)

    def test_retrieve_actor(self):
        response = self.client.get(f"/actors/{self.actor.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = ActorSerializer(self.actor).data
        self.assertEqual(response.data, serializer_data)

    def test_update_actor(self):
        self.client.force_login(user=self.user)

        updated_data = {
            "first_name": "John",
            "last_name": "Smith"
        }
        response = self.client.put(f"/actors/{self.actor.id}/", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_actor = Actor.objects.get(id=self.actor.id)
        self.assertEqual(updated_actor.full_name, "John Smith")

    def test_delete_actor(self):
        self.client.force_login(user=self.user)

        response = self.client.delete(f"/actors/{self.actor.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Actor.DoesNotExist):
            Actor.objects.get(id=self.actor.id)


class PlayViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="testuser@test.com",
            password="testpassword"
        )
        self.genre = Genre.objects.create(name="Drama")
        self.actor = Actor.objects.create(name="Jane Smith", bio="An award-winning actress.")
        self.play_data = {
            "title": "Romeo and Juliet",
            "description": "A tragic love story",
            "genres": [self.genre.id],
            "actors": [self.actor.id],
        }
        self.play = Play.objects.create(
            title="Hamlet",
            description="A classic Shakespearean play",
        )
        self.play.genres.add(self.genre)
        self.play.actors.add(self.actor)

    def test_list_plays(self):
        response = self.client.get("/plays/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn(self.play.title, [play["title"] for play in response.data])

    def test_retrieve_play(self):
        response = self.client.get(f"/plays/{self.play.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["title"], self.play.title)

    def test_update_play(self):
        self.client.force_authenticate(user=self.user)

        updated_data = {
            "title": "Macbeth",
            "description": "A tragedy by William Shakespeare",
            "genres": [self.genre.id],
            "actors": [self.actor.id],
        }
        response = self.client.put(f"/plays/{self.play.id}/", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_play = Play.objects.get(id=self.play.id)
        self.assertEqual(updated_play.title, "Macbeth")

    def test_delete_play(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(f"/plays/{self.play.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Play.DoesNotExist):
            Play.objects.get(id=self.play.id)


class TheatreHallViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="testuser@test.com",
            password="testpassword"
        )
        self.theatre_hall_data = {
            "name": "Main Hall",
            "capacity": 500,
        }
        self.theatre_hall = TheatreHall.objects.create(
            name="Small Hall",
            rows=10,
            seats_in_row=20,
        )

    def test_list_theatre_halls(self):
        response = self.client.get("/theatrehalls/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn(self.theatre_hall.name, [hall["name"] for hall in response.data])

    def test_create_theatre_hall(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post("/theatrehalls/", self.theatre_hall_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_theatre_hall = TheatreHall.objects.get(name="Main Hall")
        self.assertEqual(new_theatre_hall.capacity, 500)

    def test_update_theatre_hall(self):
        self.client.force_authenticate(user=self.user)

        updated_data = {
            "name": "Updated Hall",
            "rows": 5,
            "seats_in_row": 10,
        }
        response = self.client.put(f"/theatrehalls/{self.theatre_hall.id}/", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_theatre_hall = TheatreHall.objects.get(id=self.theatre_hall.id)
        self.assertEqual(updated_theatre_hall.name, "Updated Hall")

    def test_delete_theatre_hall(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(f"/theatrehalls/{self.theatre_hall.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(TheatreHall.DoesNotExist):
            TheatreHall.objects.get(id=self.theatre_hall.id)


class PerformanceViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="testuser@test.com",
            password="testpassword"
        )
        self.theatre_hall = TheatreHall.objects.create(
            name="Main Hall",
            rows=10,
            seats_in_row=20,
        )
        self.play = Play.objects.create(
            title="Hamlet",
            description="A classic Shakespearean play",
        )
        self.performance_data = {
            "play": self.play.id,
            "show_time": "2023-09-15T19:00:00Z",
            "theatre_hall": self.theatre_hall.id,
        }
        self.performance = Performance.objects.create(
            play=self.play,
            show_time="2023-09-20T15:00:00Z",
            theatre_hall=self.theatre_hall,
        )

    def test_list_performances(self):
        response = self.client.get("/performances/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.play.title, [performance["play"]["title"] for performance in response.data])

    def test_create_performance(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post("/performances/", self.performance_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_performance = Performance.objects.get(play=self.play)
        self.assertEqual(new_performance.show_time.strftime("%Y-%m-%dT%H:%M:%SZ"), "2023-09-15T19:00:00Z")

    def test_update_performance(self):
        self.client.force_authenticate(user=self.user)

        updated_data = {
            "play": self.play.id,
            "show_time": "2023-09-25T20:00:00Z",
            "theatre_hall": self.theatre_hall.id,
        }
        response = self.client.put(f"/performances/{self.performance.id}/", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_performance = Performance.objects.get(id=self.performance.id)
        self.assertEqual(updated_performance.play.title, "Hamlet")

    def test_delete_performance(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(f"/performances/{self.performance.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Performance.DoesNotExist):
            Performance.objects.get(id=self.performance.id)


class ReservationViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="testuser@test.com",
            password="testpassword"
        )
        self.reservation_data = {
            "created_at": "2023-09-10T12:00:00Z",
            "user": self.user.id,
        }
        self.reservation = Reservation.objects.create(
            created_at="2023-09-11T12:00:00Z",
            user=self.user,
        )

    def test_list_reservations(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/reservations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn(self.user.email, [reservation["user"] for reservation in response.data])

    def test_create_reservation(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post("/reservations/", self.reservation_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_reservation = Reservation.objects.get(id=response.data["id"])
        self.assertEqual(new_reservation.user.email, self.user.email)

    def test_update_reservation(self):
        self.client.force_authenticate(user=self.user)

        updated_data = {
            "created_at": "2023-09-12T12:00:00Z",
            "user": self.user.id,
        }
        response = self.client.put(f"/reservations/{self.reservation.id}/", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_reservation = Reservation.objects.get(id=self.reservation.id)
        self.assertEqual(updated_reservation.created_at, "2023-09-12T12:00:00Z")

    def test_delete_reservation(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(f"/reservations/{self.reservation.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Reservation.DoesNotExist):
            Reservation.objects.get(id=self.reservation.id)


class TicketViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="testuser@test.com",
            password="testpassword"
        )
        self.theatre_hall = TheatreHall.objects.create(
            name="Main Hall",
            capacity=500,
        )
        self.play = Play.objects.create(
            title="Sample Play",
            description="A sample play",
        )
        self.performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.theatre_hall,
            show_time="2023-09-20T14:00:00Z",
        )
        self.reservation = Reservation.objects.create(
            created_at="2023-09-10T10:00:00Z",
            user=self.user,
        )
        self.ticket_data = {
            "performance": self.performance.id,
            "reservation": self.reservation.id,
            "row": 1,
            "seat": 101,
        }
        self.ticket = Ticket.objects.create(
            performance=self.performance,
            reservation=self.reservation,
            row=2,
            seat=202,
        )

    def test_list_tickets(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/tickets/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn((self.ticket.row, self.ticket.seat), [(ticket["row"], ticket["seat"]) for ticket in response.data])

    def test_create_ticket(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post("/tickets/", self.ticket_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_ticket = Ticket.objects.get(id=response.data["id"])
        self.assertEqual(new_ticket.row, 1)
        self.assertEqual(new_ticket.seat, 101)
        self.assertEqual(new_ticket.performance, self.performance)
        self.assertEqual(new_ticket.reservation, self.reservation)

    def test_update_ticket(self):
        self.client.force_authenticate(user=self.user)

        updated_data = {
            "row": 3,
            "seat": 303,
        }
        response = self.client.put(f"/tickets/{self.ticket.id}/", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_ticket = Ticket.objects.get(id=self.ticket.id)
        self.assertEqual(updated_ticket.row, 3)
        self.assertEqual(updated_ticket.seat, 303)

    def test_delete_ticket(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(f"/tickets/{self.ticket.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Ticket.DoesNotExist):
            Ticket.objects.get(id=self.ticket.id)
