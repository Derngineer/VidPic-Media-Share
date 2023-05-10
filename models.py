from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.






class Profile(models.Model):

	user = models.OneToOneField(User, on_delete = models.CASCADE)
	avatar = models.ImageField(default = "default.jpg", upload_to = "profile_images")
	bio = models.TextField()

	def __str__(self):
		return self.user.username



class Video(models.Model):
	MEDIA_TYPE = 'video'
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	title = models.CharField(max_length = 200, default = 'nonsense')
	description = models.CharField(max_length = 300, null = True, default ="some string")
	vid = models.FileField(null = True, blank = True,upload_to = "videos")
	upload_date = models.DateTimeField(default = timezone.now)
	like_count = models.IntegerField(default = 0)


	def __str__(self):
		return self.title

	



class Picture(models.Model):
	MEDIA_TYPE = 'picture'
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	title = models.CharField(max_length = 200, default = 'nonsense')
	description = models.CharField(max_length = 300,null = True)
	img = models.ImageField(upload_to ="pictures", blank = True)
	upload_date = models.DateTimeField(default = timezone.now)



	def __str__(self):
		return self.title

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='video_likes')
    # picture = models.ForeignKey(Picture, on_delete=models.CASCADE, related_name='picture_likes')

    class Meta:
        unique_together = ('user', 'video')


    def __str__(self):
    	return f'{self.user} like {self.video}'






