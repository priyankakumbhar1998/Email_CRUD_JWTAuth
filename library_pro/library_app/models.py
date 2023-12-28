from django.db import models

class Library(models.Model):
    book_name = models.CharField(max_length=40)
    book_no = models.IntegerField()
    book_author = models.CharField(max_length=40)
    book_price = models.IntegerField()

