from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTests(TestCase):
    # Test the publicly available ingredient API

    def setUp(self):
        self.client = APIClient()
    
    '''def test_login_required(self):
        # Test that login is required to access the endpoint
        res = self.client.get(INGREDIENTS_URL)

        self.assetEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)'''


class PrivateIngredientsApiTests(TestCase):
    # Test the private ingredient API

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@appdev.com',
            'testpassword'
        )
        self.client.force_authenticate(self.user)
    
    def test_retrieve_ingredient_list(self):
        # Test retrieving a list of ingredients
        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Salt')

        res = self.client.get(INGREDIENTS_URL)

        ingredient = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredient, many=True)
        self.assetEqual(res.status_code, status.HTTP_200_OK)
        self.assetEqual(res.data, serializer.data)
    
    def test_ingredient_limited_to_user(self):
        # Test the ingredients for the authenticated user are returned
        user2 = get_user_model().objects.create_user(
            'test@appdev.com',
            'testpassword'
        )
        Ingredient.objects.create(user=user2, name='Vinegar')
        ingredient  = Ingredient.objects.create(user=self.user, name='Tumeric')

        res = self.client.get(INGREDIENTS_URL)

        self.assetEqual(res.status_code, status.HTTP_200_OK)
        self.assetEqual(len(res.data), 1)
        self.assetEqual(res.data[0]['name'], ingredient.name)