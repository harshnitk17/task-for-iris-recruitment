from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render,redirect
from .forms import UserForm,ProfileForm,ImageForm,query
from .models import Profile,item
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def myprofile(request):
    if request.user.is_authenticated:
        username=request.user.username
        date_c=request.user.date_joined
        return render(request, 'myprofile.html', {'username':username,'date_c':date_c,})
    else:
        error="not signed in"
        return render(request, 'myprofile.html', {'error':error,})

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('market:myprofile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'updateprofile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def add(request):
    form= ImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        q=item.objects.last()
        add_id=q.id
        q.user_id=request.user.id
        q.save()
        return HttpResponseRedirect(reverse('market:show_add', args=(add_id,)))


    context= {'form': form,}


    return render(request, 'add.html', context)

def show_add(request,add_id):
    q=get_object_or_404(item, id=add_id)
    imagefile= q.imagefile
    description=q.description
    title=q.title
    price=q.price
    type=q.type
    date=q.date
    user_id=q.user_id
    status=0
    if q.status=="sold":
        status=1
    w=get_object_or_404(User,id=user_id)
    username=w.username
    address=w.profile.address
    mobile=w.profile.mobile
    email=w.email
    context={'imagefile':imagefile,'description':description,'title':title,'type':type,'price':price,'time':date,'user_id':user_id,'username':username,'email':email,'address':address,'add_id':add_id,'status':status,'mobile':mobile,}
    return render(request, 'show_add.html', context)

def market(request):
    form=query()
    if request.POST:
        form=query(request.POST)
        if form.is_valid():
            w=form.cleaned_data['keyword']
            return HttpResponseRedirect(reverse('market:search', args=(w,)))

    titles=item.objects.filter(type="Sell",status="notsold").exclude(user_id=request.user.id).values_list('title',flat=True).order_by('-date')[0:4]
    prices=item.objects.filter(type="Sell",status="notsold").exclude(user_id=request.user.id).values_list('price',flat=True).order_by('-date')[0:4]
    ids=item.objects.filter(type="Sell",status="notsold").exclude(user_id=request.user.id).values_list('id',flat=True).order_by('-date')[0:4]
    imagefile=item.objects.filter(type="Sell",status="notsold").exclude(user_id=request.user.id).values_list('imagefile',flat=True).order_by('-date')[0:4]
    s_id=[]
    usernames=[]
    for i in range(len(ids)):
        q=get_object_or_404(item, id=ids[i])
        s_id.append(q.user_id)
    for i in range(len(ids)):
        q=get_object_or_404(User, id=s_id[i])
        usernames.append(q.username)

    titlesr=item.objects.filter(type="Rent",status="notsold").exclude(user_id=request.user.id).values_list('title',flat=True).order_by('-date')[0:4]
    pricesr=item.objects.filter(type="Rent",status="notsold").exclude(user_id=request.user.id).values_list('price',flat=True).order_by('-date')[0:4]
    idsr=item.objects.filter(type="Rent",status="notsold").exclude(user_id=request.user.id).values_list('id',flat=True).order_by('-date')[0:4]
    imagefiler=item.objects.filter(type="Rent",status="notsold").exclude(user_id=request.user.id).values_list('imagefile',flat=True).order_by('-date')[0:4]
    s_idr=[]
    usernamesr=[]
    for i in range(len(idsr)):
        q=get_object_or_404(item, id=idsr[i])
        s_idr.append(q.user_id)
    for i in range(len(idsr)):
        q=get_object_or_404(User, id=s_idr[i])
        usernamesr.append(q.username)
    context={'latest_s':titles,'list1':usernames,'list2':prices,'id':ids,'imagefile':imagefile,'latest_r':titlesr,'list1r':usernamesr,'list2r':pricesr,'idr':idsr,'imagefiler':imagefiler ,'form':form,}
    return render(request, 'market.html', context)

def sell(request):
    objects=item.objects.filter(type="Sell",status="notsold").exclude(user_id=request.user.id).order_by('-date')

    context={'objects':objects,}
    return render(request,'sell.html',context)

def rent(request):
    objects=item.objects.filter(type="Rent",status="notsold").exclude(user_id=request.user.id).order_by('-date')
    context={'objects':objects,}
    return render(request,'rent.html',context)
def search(request,keyword):
    objects=item.objects.filter(tag__icontains=keyword,status="notsold").exclude(user_id=request.user.id).order_by('-date')
    context={'objects':objects,'keyword':keyword,}
    return render(request,'search.html',context)
def myadds(request):
    if request.user.is_authenticated:
        username_id=request.user.id
        objects=item.objects.filter(user_id=username_id).order_by('-date')
        return render(request, 'myadds.html', {'objects':objects,})
    else:
        error="not signed in"
        return render(request, 'myadds.html', {'error':error,})
def edit_add(request,add_id):
    q=get_object_or_404(item,id=add_id)
    q.status="sold"
    q.save()
    return HttpResponseRedirect(reverse('market:show_add', args=(add_id,)))
