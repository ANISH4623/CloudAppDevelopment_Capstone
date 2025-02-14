from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from djangoapp.restapis import get_dealer_reviews_from_cf, get_dealers_from_cf,get_dealer_by_id
# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context= {}
    if request.method == "GET":
        return render(request,'djangoapp/about.html',context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request,'djangoapp/contact.html',context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp/index.html')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
        # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context= {}
    if request.method == "GET":
        url = "http://127.0.0.1:3000/dealerships/get"
        dealer_names = []
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        for dealer in dealerships:
            dealer_names.append(dealer.short_name)
        # Concat all dealer's short name
        context["dealers"] = dealer_names
        
        # Return a list of dealer short name
        return render(request,'djangoapp/index.html',context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url_ds = "http://127.0.0.1:3000/dealerships/get?id={}".format(dealer_id)
        url_r = "http://127.0.0.1:5000/api/get_reviews?id={}".format(dealer_id)
        # Get dealers from the URL
        context = {
            "dealer": get_dealers_from_cf(url_ds)[0],
            "reviews": get_dealer_reviews_from_cf(url_r, dealer_id),
        }
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    if request.method == "GET":
        url = "http://127.0.0.1:3000/dealerships/get?id={}".format(dealer_id)
        # Get dealers from the URL
        context = {
            "cars": CarModel.objects.all(),
            "dealer": get_dealers_from_cf(url)[0],
        }
        print(context)
        return render(request, 'djangoapp/add_review.html', context)
    if request.method == "POST":
        form = request.POST
        review = {
            "name": f"{request.user.first_name} {request.user.last_name}",
            "dealership": dealer_id,
            "review": form["content"],
            "purchase": form.get("purchasecheck"),
            }
        if form.get("purchasecheck"):
            review["purchasedate"] = datetime.strptime(form.get("purchasedate"), "%m/%d/%Y").isoformat()
            car = CarModel.objects.get(pk=form["car"])
            review["car_make"] = car.car_make.name
            review["car_model"] = car.name
            review["car_year"]= car.year.strftime("%Y")
        json_payload = {"review": review}
        URL ='http://127.0.0.1:5000/api/post_reviews'
        post_request(URL, json_payload, dealerId=dealer_id)
    return redirect("djangoapp:dealer_details", dealer_id=dealer_id)

