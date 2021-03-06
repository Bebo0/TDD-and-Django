from django.db import models
from django.core.urlresolvers import reverse

from django.conf import settings
# Create your models here.

# inherits from models.Model
# Classes that inherit from models.Model map to tables in the database
# They generate an "id" attribute, which will be a primary key column in the database
# Whenever something is added in this file, have to run python manage.py makemigrations
# To create a real database, need to run python manage.py migrate.
# To clean DB, run rm db.sqlite3 then python manage.py migrate --noinput

class List(models.Model):
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True) # optional
	# Model objects are often associated with a particular URL. get_absolute_url
	# says what page displays the item.
	def get_absolute_url(self):
		return reverse('view_list', args=[self.id])

	@property
	def name(self):
		return self.item_set.first().text


class Item(models.Model):
	text = models.TextField(default='') # Django has other field types like IntegerField, CharField, DateField and so on. 
	#https://docs.djangoproject.com/en/1.11/ref/models/fields/
	list = models.ForeignKey(List, default=None)

	class Meta:
		ordering = ('id', )
		unique_together = ('list', 'text')


	def __str__(self):
		return self.text




