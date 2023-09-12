from django.db import models

# Create your models here.

#WEEK 2 LESSON 2 RELATIONSHIP SERIALIZER
#Create category model and connected to the menu item model.

class Category(models.Model):
	slug = models.SlugField()
	title = models.CharField(max_length=255)

	def __str__(self)-> str:
		return self.title
	
 	

# WEEK 2 LESSON 1 Restaurant Menu API Project with DRF

#you need a database model first

class MenuItem(models.Model):
	title = models.CharField(max_length=225)
	price = models.DecimalField(max_digits=6, decimal_places=2)
	inventory = models.SmallIntegerField()
	category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)

	def __str__(self)-> str:
		return self.title


	#Now serealized the object 
	#serealized help to conver model instances into python datatypes but can be display as 
	#json or xml, It's also helps to converts the http request body into python datatypes and map into a model instance.

