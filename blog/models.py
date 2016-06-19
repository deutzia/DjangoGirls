from django.db import models
from django.utils import timezone

class Post(models.Model):
	author = models.ForeignKey('auth.User')
	title = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)
	edited_date = models.DateTimeField(blank=True, null=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.title

class Comment(models.Model):
	author = models.CharField(max_length=50)
	email = models.CharField(max_length=100)
	text = models.TextField()
	date = models.DateTimeField(default=timezone.now)
	commented_post = models.ForeignKey(Post, null=True)
	published = models.BooleanField(default=False)

	def publish(self):
		self.date = timezone.now()
		self.save()

	def __str__(self):
		return self.text
