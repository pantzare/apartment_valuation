from django.shortcuts import render
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
import pandas as pd
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)

		if form.is_valid():
		    post = form.save(commit=False)
		    post.author = request.user
		    post.published_date = timezone.now()
		    post.save()
		    return redirect('valuation')
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})

def valuation(request):
	url='https://www.hemnet.se/salda/bostader?location_ids%5B%5D=473499&item_types%5B%5D=bostadsratt&rooms_max=1&sold_age=3m'
	#url = 'https://www.hemnet.se/salda/bostader?location_ids%5B%5D=473498&item_types%5B%5D=bostadsratt&rooms_min=2&rooms_max=2&sold_age=3m'
	#imports data from 1 bedroom apartments in Råsunda sold in the last 3 months
	response = requests.get(url)

	soup = BeautifulSoup(response.text, 'html.parser')
	apartments_price=soup.findAll("span", {"class": "sold-property-listing__subheading sold-property-listing--left"})
	#prints every price item in the HTML

	price_list=[]

	for i in apartments_price:
		price_list.append(i.string.split()[1]+i.string.split()[2]+i.string.split()[3])
		#splitting the strings and puts the numbers back together, makes a list of them

	df=pd.DataFrame(data=price_list, columns=['Price'])
	#makes DF of list

	apartments_size=soup.findAll("div", {"class": "sold-property-listing__subheading sold-property-listing--left"})
	#repeating for apartment size

	size_list=[]

	for i in apartments_size:
		size_list.append(i.string.split()[0].replace(",","."))
		#replaces comma with point to enable conversion to float

	df['Size']=size_list

	df["Price"] = pd.to_numeric(df["Price"], downcast="float")
	df["Size"] = pd.to_numeric(df["Size"], downcast="float")
	#Converting from string to float

	df["price/m2"]=df["Price"]/df["Size"]

	X = np.array(df["Size"]).reshape(-1,1)
	y = np.array(df["price/m2"])
	reg = LinearRegression(fit_intercept=True).fit(X, y)

	my_apartment_size=float(Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[0].size)
	my_apartment=reg.predict([[my_apartment_size]])*my_apartment_size
	my_apartment_value=round(my_apartment[0],0)

	return render(request, 'blog/valuation.html', {'my_apartment_value': my_apartment_value})

def valuation2(request):
	value=float(Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[0].size)*68000
	return render(request, 'blog/valuation.html', {'my_apartment_value': value})