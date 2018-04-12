from django.shortcuts import render,redirect
from social_django.models import UserSocialAuth
import requests

def index(request):
    return render(request, 'gitshow/index.html')

def profile(request):
    user = UserSocialAuth.objects.filter(user=request.user)
    extra=user.values('extra_data')[0]['extra_data']['access_token']
    print(extra)
    r = requests.get('https://api.github.com/user',auth=(request.user, extra))
    repos = []
    if r.status_code == 200:
        name = r.json()['name']
        ava = r.json()['avatar_url']
        rr = requests.get(r.json()['repos_url'], auth=(request.user, extra))
        for i in range(int(r.json()['public_repos'])):
            repos.append(rr.json()[i]['name'])
        return render(request, 'gitshow/profile.html', {'name': name, 'ava': ava, 'repos': repos})

    return redirect('index')
