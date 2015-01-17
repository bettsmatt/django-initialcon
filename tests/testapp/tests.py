from django.test import TestCase
from django.core.urlresolvers import reverse


class ExampleTest(TestCase):

    def test_name_with_single_space_does_not_error(self):
        self.client.get(reverse('initialcon:generate', kwargs={'name': ' '}))
