from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating an ew user with a email is successful"""
        email = "test#test@gmail.com"
        password = 'TestGmail'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the emil for new user is normalized"""
        email = 'test@GMAIL.COM'
        user = get_user_model().objects.create_user(email, '12334121Test')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test232323')

    def test_create_new_superuser(self):
        """Test creating an new superuser"""
        email = "superuser@gmail.com"
        password = 'TestGmail'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
