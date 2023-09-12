from rest_framework import serializers
from .models import MenuItem, Category
from decimal import Decimal

#class MenuItemSerializer(serializers.ModelSerializer):
#	class Meta:
#		model = MenuItem
#		fields = ['id','title','price','inventory']


# Week 2 Lesson 2 Serializer HOW TO USE MODEL SERIALIZER IN THE DJANGO REST FRAMEWORK TO CONVERT MODEL INSTANCES QUICKLY AND EASILY TO JSON.
# when you hide the database field use this class
#class MenuItemSerializer(serializers.Serializer):
#	id = serializers.IntegerField()
#	title = serializers.CharField(max_length=255)
#	price = serializers.DecimalField(max_digits=6, decimal_places=2)
#	inventory = serializers.IntegerField()


class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ['id','slug','title']
#now use the serializer for the single record


#CHANGE THE INPUT FIELD BY USING SERIALIZATION
class MenuItemSerializer(serializers.ModelSerializer):
	stock = serializers.IntegerField(source='inventory')#linked and existing field with thesource arguments
	price_after_tax = serializers.SerializerMethodField(method_name = 'calculate_tax')
	#category = serializers.StringRelatedField() # to display category name
	#IF CATEGORY SERIALIZER IS CREATED THEN SKIP THE OBOVE STEP AND WRITE THIS, IT WILL SHOW ALL FIELDS
	category = CategorySerializer(read_only=True)# this category field shoudl be read only because it is only needed to display the category details in the get call.
	category_id = serializers.IntegerField(write_only=True)# to hide from the get request but show in post request
	class Meta:
		model = MenuItem
		fields = ['id','title','price','stock','price_after_tax', 'category', 'category_id']

#prive after tax
	def calculate_tax(self, product:MenuItem):
		return product.price * Decimal(1.1)


class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ['id','slug','title']