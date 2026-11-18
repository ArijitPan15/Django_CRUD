from django.test import TestCase
from django.urls import reverse

from .models import Stream


class StreamViewTests(TestCase):
    def setUp(self):
        self.stream = Stream.objects.create(name="Science", description="Initial")

    def test_add_stream_rejects_blank_name(self):
        response = self.client.post(
            reverse("_add"), {"stream_name": "  ", "stream_description": "Test"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Stream.objects.count(), 1)

    def test_edit_stream_updates_data(self):
        response = self.client.post(
            reverse("_edit", args=[self.stream.pk]),
            {"stream_name": "Arts", "stream_description": "Updated"},
        )
        self.assertEqual(response.status_code, 200)
        self.stream.refresh_from_db()
        self.assertEqual(self.stream.name, "Arts")
        self.assertEqual(self.stream.description, "Updated")

    def test_edit_stream_rejects_duplicate_name(self):
        Stream.objects.create(name="Commerce", description="Other")
        response = self.client.post(
            reverse("_edit", args=[self.stream.pk]),
            {"stream_name": "Commerce", "stream_description": "Updated"},
        )
        self.assertEqual(response.status_code, 400)
        self.stream.refresh_from_db()
        self.assertEqual(self.stream.name, "Science")

    def test_delete_stream_requires_post(self):
        url = reverse("delete_stream", args=[self.stream.pk])
        self.assertEqual(self.client.get(url).status_code, 405)
        self.assertTrue(Stream.objects.filter(pk=self.stream.pk).exists())

        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Stream.objects.filter(pk=self.stream.pk).exists())

    def test_edit_stream_returns_not_found_for_missing_record(self):
        response = self.client.post(
            reverse("_edit", args=[99999]),
            {"stream_name": "Arts", "stream_description": "Updated"},
        )
        self.assertEqual(response.status_code, 404)
