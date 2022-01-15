from django.test import TestCase
from django.urls import resolve, reverse

from budget.forms import ExpenseForm
from budget.models import Category, Project
from budget.views import ProjectCreateView, ProjectListView, project_detail


class ProjectListViewTest(TestCase):
    def setUp(self):
        url = reverse("list")
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolves_correct_view(self):
        view = resolve("/")
        self.assertEquals(view.func.view_class, ProjectListView)


class ProjectCreateViewTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="Test Project", slug="test-project", budget="5000", days="21"
        )
        # test foreign key
        self.categories = Category.objects.create(
            name="Test Category", project=self.project
        )
        url = reverse("add")
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolves_correct_view(self):
        view = resolve("/add")
        self.assertEquals(view.func.view_class, ProjectCreateView)

    def test_csrf(self):
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_form_inputs(self):
        # view must contain six inputs: csrf, name, budget, days, categories = 2
        self.assertContains(self.response, "<input", 6)
        self.assertContains(self.response, 'type="text"', 2)
        self.assertContains(self.response, 'type="number"', 2)
        self.assertContains(self.response, 'type="hidden"', 2)


class ProjectDetailViewTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="Test Project", slug="test-project", budget="5000", days="21"
        )
        # test foreign key
        self.categories = Category.objects.create(
            name="Test Category", project=self.project
        )
        url = reverse("detail", kwargs={"project_slug": self.project.slug})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolves_correct_view(self):
        view = resolve("/test-project")
        self.assertEquals(view.func, project_detail)

    def test_csrf(self):
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_form_inputs(self):
        # view must contain three inputs: csrf, name, amount, and one select: category
        self.assertContains(self.response, "<input", 3)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="number"', 1)
        self.assertContains(self.response, 'type="hidden"', 1)
        self.assertContains(self.response, "<select", 1)


class ExpenseFormTest(TestCase):
    def test_form_has_fields(self):
        form = ExpenseForm()
        expected = [
            "title",
            "amount",
            "category",
        ]
        actual = list(form.fields)
        self.assertEqual(expected, actual)
