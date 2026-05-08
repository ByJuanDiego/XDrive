from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from upload.models import MasterFile


class UploadApiValidationTests(TestCase):
    """Additional unit tests for XDrive upload API edge cases."""

    def setUp(self):
        self.client = APIClient()
        self.last_chunk_url = reverse('chunkedfile-last-chunk')
        self.download_url = reverse('chunkedfile-download')
        self.merge_chunks_url = reverse('chunkedfile-merge-chunks')
        self.master_file = MasterFile.objects.create(
            file_name='empty.txt',
            md5_checksum='d41d8cd98f00b204e9800998ecf8427e',
            number_of_chunks=1,
        )

    def test_last_chunk_requires_master_file_id(self):
        response = self.client.get(self.last_chunk_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['error'],
            'master_file_id parameter is required',
        )

    def test_last_chunk_returns_not_found_when_master_file_has_no_chunks(self):
        response = self.client.get(
            self.last_chunk_url,
            {'master_file_id': self.master_file.id},
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data['message'],
            'No chunks found for this master file',
        )

    def test_download_requires_master_file_id(self):
        response = self.client.get(self.download_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['error'],
            'master_file_id parameter is required',
        )

    def test_download_returns_not_found_before_file_is_merged(self):
        response = self.client.get(
            self.download_url,
            {'master_file_id': self.master_file.id},
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data['error'],
            'File not found for this master_file',
        )

    def test_merge_chunks_requires_master_file_id(self):
        response = self.client.get(self.merge_chunks_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['error'],
            'master_file_id parameter is required',
        )
