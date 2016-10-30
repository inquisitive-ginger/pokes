from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Count

from .forms import RegisterForm, LoginForm
from .models import User, Poke

def index(request):
    if 'user_id' not in request.session:
        return redirect('/login')

    current_user = User.objects.get(id=request.session['user_id'])
    other_users_qs = User.objects.exclude(id=current_user.id)
    poked_by_count = Poke.objects.filter(pokee=current_user).values('poker').distinct().count()
    total_pokes_received = 0

    other_users = []
    for pokee in other_users_qs:
        other_users.append({
            'user': pokee,
            'pokes_inflicted': Poke.objects.filter(poker=current_user, pokee=pokee).count()
        })

    try:
        pokes_received_qs = Poke.objects.filter(pokee=current_user).values('poker').annotate(poke_count=Count('poker')).order_by('-poke_count')
        pokes_received = []
        for poke_group in pokes_received_qs:
            total_pokes_received += poke_group['poke_count']
            pokes_received.append({
                'user': User.objects.get(id=poke_group['poker']),
                'pokes_received': poke_group['poke_count']
            })
    except Poke.DoesNotExist:
        pokes_received = []

    context = {
        'user': current_user,
        'others': other_users,
        'poked_by_count': poked_by_count,
        'received_poke_count': total_pokes_received,
        'pokes_received': pokes_received
    }

    return render(request, "zpokes/index.html", context)

def register(request):
    if 'user_id' in request.session:
        return redirect('/')

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            return redirect('/login')
    else:
        register_form = RegisterForm()

    return render(request, 'zpokes/register.html', {'form': register_form})

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = User.objects.get(email=request.POST['email'])
            request.session['user_id'] = user.id
            return redirect('/')
    else:
        login_form = LoginForm()

    return render(request, 'zpokes/login.html', {'form': login_form})

def logout(request):
    if 'user_id' in request.session:
        request.session.pop('user_id')

    return redirect('/login')

def poke_user(request, id):
    print "wtf"
    if request.method == 'POST':
        poker = User.objects.get(id=request.session['user_id'])
        pokee = User.objects.get(id=id)
        new_poke = Poke(poker=poker, pokee=pokee)
        new_poke.save()

    return redirect('/')
