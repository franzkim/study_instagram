from django.contrib.auth import login as django_login, logout as django_logout, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import LoginForm

User = get_user_model()


def login(request):
    if request.method == 'POST':

        ### Form클래스 미사용시

        # username = request.POST['username']
        # password = request.POST['password']
        # user = authenticate(
        #     request,
        #     username=username,
        #     password=password,
        # )
        # if user is not None:
        #     django_login(request, user)
        #     return redirect('post:post_list')
        # else:
        #     return HttpResponse('Login credentials invalid')

        ### Form클래스 사용시

        # Bound Form 생성
        form = LoginForm(data=request.POST)
        # Bound Form의 유효성 검증
        if form.is_valid():
            user = form.cleaned_data['user']
            django_login(request, user)
            return redirect('post:post_list')
    else:
        if request.user.is_authenticated:
            return redirect('post:post_list')
        # LoginForm인스턴스를 생성해서 context에 넘김
        form = LoginForm()
        context = {
            'form': form,
        }
        # render시 context에는 LoginForm클래스형 form객체가 포함됨
        return render(request, 'member/login.html', context)


def logout(request):
    django_logout(request)
    return redirect('post:post_list')


def signup(request):
    if request.method == 'POST':
        # username, password1, password2에 POST로 전달받은 데이터를 할당
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        # username에 해당하는 User가 있는지 검사
        if User.objects.filter(username=username).exists():
            # 이미 존재하는 username일 경우
            return HttpResponse('Username is already exist')
        # password1과 password2가 같은지 검사
        elif password1 != password2:
            # 다를 경우
            return HttpResponse('Password and Password Check are not equal')

        # 위의 두 경우가 아닌 경우 유저를 생성
        user = User.objects.create_user(
            username=username,
            password=password1,
        )
        # 생성한 유저를 로그인 시킴
        django_login(request, user)
        # 이후 post_list 뷰로 이동
        return redirect('post:post_list')
    else:
        return render(request, 'member/signup.html')
