from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import make_aware
from datetime import datetime
from .models import Recipe, Category


class RecipeViewsTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Салати")

        created_2023 = make_aware(datetime(2023, 5, 10, 12, 0))
        created_2022 = make_aware(datetime(2022, 6, 5, 12, 0))

        self.recipe_2023 = Recipe.objects.create(
            title="Test Recipe 2023",
            description="Тестовий опис",
            instructions="Інструкції",
            ingredients="Інгредієнти",
            created_at=created_2023,
            updated_at=created_2023,
            category=self.category,
        )
        self.recipe_2022 = Recipe.objects.create(
            title="Test Recipe 2022",
            description="Опис 2022",
            instructions="Інструкції 2022",
            ingredients="Інгредієнти 2022",
            created_at=created_2022,
            updated_at=created_2022,
            category=self.category,
        )

    def test_main_view_shows_only_2023_recipes(self):
        response = self.client.get(reverse("main"))
        content = response.content.decode()
        print("MAIN HTML:\n", content)
        self.assertIn("Test Recipe 2023", content)
        self.assertNotIn("Test Recipe 2022", content)

    def test_recipe_detail_view(self):
        response = self.client.get(reverse("recipe_detail", args=[self.recipe_2023.id]))
        content = response.content.decode()
        print("DETAIL HTML:\n", content)
        self.assertIn("Test Recipe 2023", content)
        self.assertIn("Тестовий опис", content)
