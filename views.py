from django.shortcuts import render,redirect,get_object_or_404
from . models import Profile, Picture,Video,Like
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .forms import VideoForm, PictureForm
import random
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout


# from .models import Video, Picture, Like

# Create your views here.


from django.shortcuts import get_object_or_404, redirect, reverse


def logout_view(request):
	logout(request)
	return redirect(reverse('signin'))


def like_video(request, video_id):
	
	video = get_object_or_404(Video, id= video_id)
	Like.objects.get_or_create(user=request.user, video=video)
	# return redirect('index')
	return HttpResponseRedirect(reverse('video_detail', kwargs ={'video_id': video.id}))


# def like_video(request, video_id):
#     video = get_object_or_404(Video, pk=video_id)
#     user = request.user
#     like, created = Like.objects.get_or_create(user=user, video=video)

#     if not created:
#         like.delete()
#         return JsonResponse({'liked': False, 'count': video.like_set.count()})

#     return JsonResponse({'liked': True, 'count': video.like_set.count()})


  



def signup(request):
	form = UserCreationForm()
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = auth.authenticate(username = username, password = raw_password)
			login(request, user)
			messages.success(request, "You have successfully signed up")
			return redirect('home')
		else:
			messages.success(request, "form incorrect")


	return render(request,"vidpic/signup.html",{"form": form})


def login(request):
	if request.method == 'POST':
		form = AuthenticationForm(request, data = request.POST)
		if form.is_valid():
			username = request.POST['username']
			password= request.POST['password']
			user = auth.authenticate(username = username , password = password)
			if user is not None:
				auth.login(request,user)
				return redirect('index')

			else:
				messages.info(request, "Invalid Username or Password")
				return redirect('login')

		else:
			messages.error(request, "Invalid username or password.")

	form =AuthenticationForm()
	return render(request,"vidpic/login.html",{'form': form})



def video_details(request, video_id):
	video = Video.objects.get(id= video_id)
	context = {
	"video":video
	}
	return render(request, "vidpic/video_details.html", context)











def index(request):








	videos = list(Video.objects.all())
	pictures = list(Picture.objects.all())

	for video in videos:
		video.like_count = video.video_likes.count()
		video.save()
	
	random.shuffle(videos)
	random.shuffle(pictures)

	mixed_media = videos + pictures
	random.shuffle(mixed_media)
	
	return render(request, "vidpic/index.html", { "videos": videos, "pictures": pictures, "mixed_media": mixed_media})



def profile(request, pk):
	user = request.user
	profiles = get_object_or_404(Profile, user_id=pk)
	pictures =Picture.objects.filter(user_id = pk)
	videos = Video.objects.filter(user_id = pk)
	picture_form = PictureForm()
	video_form = VideoForm()
	if request.method == 'POST' and 'picture_submit' in request.POST:
		picture_form = PictureForm(request.POST, request.FILES)
		if picture_form.is_valid():
			picture = picture_form.save(commit=False)
			picture.user = request.user
			picture.save()
			return redirect('account', pk=pk)
	elif request.method == 'POST' and 'video_submit' in request.POST:
		video_form = VideoForm(request.POST, request.FILES)
		if video_form.is_valid():
			video = video_form.save(commit=False)
			video.user = request.user
			video.save()
			return redirect('account', pk=pk)
	return render(request, 'vidpic/profile.html', {'profiles': profiles, 'picture_form': picture_form, 'video_form': video_form, 'pictures':pictures,'videos':videos})

def profile_list(request):
	profile_list = Profile.objects.all()



	return render(request,"vidpic/profilelist.html",{"profile_list":profile_list})

def aboutus(request):
	return render(request,"vidpic/aboutus.html",{})