from django.db import models

class Posts(models.Model):

    timestamp = models.DateTimeField(auto_now_add=True, unique=False)
    user_id = models.PositiveSmallIntegerField(unique=False)
    file = models.FileField(upload_to='posted_files/', null=True) #see forms/views for profile pic when setting up!
    pic = models.ImageField(upload_to='posted_pics/', null=True)
    text = models.CharField(max_length=1000)
    username = models.CharField(unique=False, max_length=15)
    type = models.CharField(unique=False, max_length=25)
    fam_num = models.PositiveSmallIntegerField(unique=False)
    fam_name = models.CharField(max_length=15)
    at = models.CharField(unique=False, max_length=15, null=True, blank=True)
    thread_id = models.PositiveSmallIntegerField(unique=False, null=True)
    thumbnail = models.ImageField(upload_to='user_pics', null=True)


class Thread(models.Model):

    author = models.CharField(max_length=15)
    subject = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now=True, unique=False)
    fam_name = models.CharField(unique=False, max_length=25)
    post_count = models.PositiveSmallIntegerField(unique=False, default=0)
    type = models.CharField(unique=False, max_length=25)




