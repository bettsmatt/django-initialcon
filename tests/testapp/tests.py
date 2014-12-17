from django.test import TestCase, Client
from django.core.urlresolvers import reverse

class ExampleTest(TestCase):

    def test_fails(self):
        client = Client()
        response = client.get(reverse('initialcon:generate', kwargs={'name': 'matt'}))
        self.fail()
