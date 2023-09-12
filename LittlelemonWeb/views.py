from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.views import APIView
#GENERIC VIEW
from rest_framework import generics
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer
#Week 2 Lesson 2 Serializer
from django.shortcuts import get_object_or_404
		#WEEK 3 LESSON 1 PAGINATION
from django.core.paginator import Paginator, EmptyPage
# Week 3 Lesson 2 Video 1
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

# Week 3 Lesson 2 Video 2
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import UserRateThrottle
# throttles.py
from .throttles import TenCallsPerMinute

#Week 3 Lesson 2 Video 6
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User, Group

# Create your views here.


#WEEK 2 VIDEO 2
#API End Point
#WRITE ['POST'] TO allow post request too not only get.
#@api_view(['POST','GET'])
#def books(request):
#	return Response('List of the books',
#		 	status=status.HTTP_200_OK)


class BookList(APIView):
	#def get(self, request):
	#	return Response({"message":"list of the books"}, status.HTTP_200_OK)
	def get(self, request):
		author = request.GET.get('author')
		if(author):
			return Response({"message":"list of the books by" + author}, status.HTTP_200_OK)

		return Response({"message":"list of the books"}, status.HTTP_200_OK)

	#def post(self, request):
	#	return Response({"message":"new of the books"}, status.HTTP_201_CREATED)

	def post(self, request):
		return Response({"title":request.data.get('title')}, status.HTTP_201_CREATED)

	#How to accept the primary key and methods of the class based views
class Book(APIView):
	def get(self, request, pk):
		return Response({"message":"single book with id " + str(pk)}, status.HTTP_200_OK)

	def put(self, request, pk):
		return Response({"title":request.data.get('title')}, status.HTTP_200_OK)


#GENERIC VIEW CLASSE WEEK 2 LESSON 1 RESTAURANT MEUN API

# create a view class

class MenuItemsView(generics.ListCreateAPIView):
	queryset = MenuItem.objects.all() #fetch
	serializer_class = MenuItemSerializer #display and store records properly
	ordering_fields = ['price', 'inventory'] # WEEK 3 LAB
	filterset_fields = ['price', 'inventory']
	search_fields = ['title']

class CategoryView(generics.ListCreateAPIView):
	queryset = Category.objects.all() #fetch
	serializer_class = CategorySerializer #display and store records properly
	




#For Delete and Update
class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
	queryset = MenuItem.objects.all()
	serializer_class = MenuItemSerializer


#WEEK 2 LESSON 2 SERIALIZERS (Convert multiple or single data base record to json data and save alot of time by not doing anything manually)
#@api_view()
#def menu_items(request):
#	items = MenuItem.objects.all()
#	return Response(items.values())


# when you hide the database field use this function
#@api_view()
#def menu_items(request):
	##items = MenuItem.objects.all()
	## when you are converting a connected model to string you must also change your view files to load the related model in a single SQL code
	#items = MenuItem.objects.select_related('category').all()
	#serialized_item = MenuItemSerializer(items, many=True)#many = True is necessary when you convert list into json data
	#return Response(serialized_item.data)#convert list to json data

#now use the serializer for the single record
#for this add a new function
#@api_view()
#def single_item(request, id):
	##item = MenuItem.objects.get(pk=id)
	##for more friendly error use this code instead of above one
	#item = get_object_or_404(MenuItem,pk=id)
	#serialized_item = MenuItemSerializer(item) #many=True is not written because it's not required to convert the single object
	#return Response(serialized_item.data)


#@api_view()
#def category_items(request):
	#items = Category.objects.all()
	#serialized_item = CategorySerializer(items, many=True)#many = True is necessary when you convert list into json data
	#return Response(serialized_item.data)#convert list to json data


# DESEARIALIZATION WEEK 2 LESSON 2
@api_view(['GET','POST'])
def menu_items(request):
	if (request.method == 'GET'):
		items = MenuItem.objects.select_related('category').all()
		#WEEK 3 LESSON 1 FILTERING AND SEARCHING
		category_name = request.query_params.get('category')
		to_price = request.query_params.get('to_price')
		search = request.query_params.get('search')
		#WEEK 3 LESSON 1 ORDERING
		ordering = request.query_params.get('ordering')
		#WEEK 3 LESSON 1 PAGINATION
		perpage = request.query_params.get('perpage',default=2)
		page = request.query_params.get('page', default=1)
		if category_name:
			items = items.filter(category__title=category_name)# __ is used because the title field is belong to the category model is linked to the menu item model
		if to_price:
			items = items.filter(price__lte=to_price)# lte is a conditional operator or fields lookup and the price__lte means price is less than or equals to a value.
			# to filter for an exact price, you can use price=to_price
		if search:
			items = items.filter(title__startswith=search) # if anywhere in the title use title__contains
			# if you want to filter case insensative use istartswith or icontains
		if ordering:
			items = items.order_by(ordering)
		# if you want to filter both price and invetory(items)
		if ordering:
			ordering_fields = ordering.split(",")
			items = items.order_by(*ordering_fields)
		
		paginator = Paginator(items,per_page=perpage)
		try:
			items = paginator.page(number=page)
		except EmptyPage:
			items = []
		serialized_item = MenuItemSerializer(items, many=True)#many = True is necessary when you convert list into json data
		return Response(serialized_item.data)#convert list to json data
	if request.method == 'POST':
		serialized_item = MenuItemSerializer(data=request.data)
		serialized_item.is_valid(raise_exception=True)
		#serialized_item.validated_data #to validate the data
		serialized_item.save()
		#you can access the record after saving it
		# you can not access this data attribute until the save method is called.
		#if you need to access the data before calling the save method you can use the validated data attribute.
		return Response(serialized_item.data, status.HTTP_201_CREATED)

@api_view()
def single_item(request, id):
	##item = MenuItem.objects.get(pk=id)
	##for more friendly error use this code instead of above one
	item = get_object_or_404(MenuItem,pk=id)
	serialized_item = MenuItemSerializer(item) #many=True is not written because it's not required to convert the single object
	return Response(serialized_item.data)


# Week 3 Lesson 2 Video 1 (TOKEN BASED AUTH)

@api_view()
@permission_classes([IsAuthenticated]) # will return a secret message for the authenticated user
def secret(request):
	return Response({"message":"Some secret message"})

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
	if request.user.groups.filter(name='Manager').exists():
		return Response({"message": "Only Manager Should See This"})
	else:
		return Response({"message":"You are not authorized"}, 403)
	

#Week 3 Lesson 2 Video 2

@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
	return Response({"message":"successful"})

@api_view()
@permission_classes([IsAuthenticated])
#@throttle_classes([UserRateThrottle])
# throttles.py
@throttle_classes([TenCallsPerMinute])
def throttle_check_auth(request):
	return Response({"message":"message for the logged in users only"})


# Week 3 Lesson 2 Video 6
@api_view(['POST'])
@permission_classes([IsAdminUser])
def managers(request):
	#if the username is present
	username = request.data['username']
	#find it 
	if username:
		user = get_object_or_404(User, username=username)
		managers = Group.objects.get(name="Manager")
		#if you need to delete the function modify this
		#managers.user_set.add(user)
		if request.method == 'POST':
			managers.user_set.add(user)
		elif request.method == 'DELETE':
			managers.user_set.remove(user)
		return Response({"message":"ok"})
	return Response({"message": "error"}, status.HTTP_400_BAD_REQUEST)