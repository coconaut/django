from django.shortcuts import render
from django import forms
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from mysite.functions import apologize, is_logged
from profiles.models import Profile
from families.models import Posts,Thread
from django.db.models import F #for faster updating and avoiding race condition



class PostForm(ModelForm):
    text = forms.CharField(label='Post something.', help_text='1000 chars max', widget=forms.Textarea)
    pic = forms.ImageField(label='Share a picture.', required=False, widget=forms.FileInput(attrs={'id': 'choose_pic'}))
    class Meta:
        model = Posts
        fields = ['pic', 'text']


class ThreadForm(ModelForm):
    subject = forms.CharField(label='Subject of thread.', help_text='100 chars max')
    class Meta:
        model = Thread
        fields = ['subject']


def fam_reroute(request):
    try:
        fam = request.session['fam']
        return HttpResponseRedirect("/family/%s/" % fam)
    #if not logged in, redirect to login page
    except KeyError:
        return HttpResponseRedirect("/login")


def family(request, familyname):
    try:
        if is_logged(request):
            if request.session['fam'].lower() == familyname.lower():
                needs = {'title': familyname, 'family': familyname, 'user_name': request.session['username']}
                return render(request, 'family/family_home.html', needs)
            else:
                return apologize(request, "You do not have permission to view this family page.")
    except KeyError:
        return HttpResponseRedirect('/login')


def getPost(request, at_target, set_type):
    post_object = PostForm(request.POST, request.FILES)
    refresher = str(request.build_absolute_uri())
    if post_object.is_valid():
        prof = Profile.objects.get(id=request.session['id'])
        thumby = prof.profile_pic
        new_post = Posts(text=post_object.cleaned_data['text'], pic=post_object.cleaned_data['pic'],
                         user_id=request.session['id'], username=request.session['username'],
                         fam_num=request.session['num'], fam_name=request.session['fam'],
                         type=set_type, at=at_target, thumbnail=thumby)
        new_post.save()
        return HttpResponseRedirect('%s' % refresher)
    else:
        return apologize(request, "The post didn't work...Make sure to enter some text!")


def getThread(request, at_target, set_type):
    thread_object = ThreadForm(request.POST)
    refresher = str(request.build_absolute_uri())
    if thread_object.is_valid():
        new_thread = Thread(subject=thread_object.cleaned_data['subject'],
                         author=request.session['username'],
                         fam_name=request.session['fam'],
                         type=set_type)
        new_thread.save()
        id = new_thread.id
        url = refresher + str(id)
        return HttpResponseRedirect('%s' % url)
    else:
        return apologize(request, "The thread didn't work...")



def fam_board(request, familyname, page, id):
    try:
        if is_logged(request):
            if request.session['fam'].lower() == familyname.lower():
                try:
                    thread = Thread.objects.get(id=id, type=page)
                    if request.method=="POST":
                        thread.post_count = F('post_count') + 1
                        thread.save(update_fields=['post_count'])
                        return getPost(request, id, page)

                    try:
                        board = Posts.objects.order_by('timestamp').filter(fam_name=familyname, at=id, \
                        type=page).values()
                    except Posts.DoesNotExist:
                        board = {}
                    #create post_form no matter what
                    post_form = PostForm()
                    title = str(familyname) + ' | ' + str(page) + ' | thread: ' + str(id)
                    needs = {'title': title, 'board': board, 'post_form': post_form,
                             'user_name': request.session['username'], 'subject': thread.subject, 'page': page,
                             'family': familyname}
                    return render(request, 'family/family_board.html', needs)
                except Thread.DoesNotExist:
                    return apologize(request, "invalid thread!")
            else:
                return apologize(request, "You do not have permission to view this family page.")
    except KeyError:
        return HttpResponseRedirect('/login')


def thread_page(request, familyname, page):

    if page not in ('discussion', 'social', 'support', 'collaborate', 'requests'):
        return apologize(request, "Not a valid page.")
    else:
        try:
            if is_logged(request):
                if request.session['fam'].lower() == familyname.lower():
                    if request.method == "POST":
                        return getThread(request, familyname, page)

                    try:

                        threads = Thread.objects.order_by('-timestamp').filter(fam_name=familyname, type=page).values()
                    except Thread.DoesNotExist:
                        threads = {}

                    thread_form = ThreadForm()
                    title = str(familyname) + ' | ' + str(page)
                    needs = {'title': title, 'threads': threads, 'thread_form': thread_form,
                             'user_name': request.session['username'], 'family': familyname}
                    return render(request, 'family/thread_page.html', needs)
                else:
                    return apologize(request, "You do not have permission to view this family page.")
        except KeyError:
            return HttpResponseRedirect('/login')





