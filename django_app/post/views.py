from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse

from .models import Post

User = get_user_model()


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'post/post_list.html', context)


def post_detail(request, post_pk):
    try:
        post = Post.objects.get(pk=post_pk)
    except Post.DoesNotExist as e:
        # 1. 404 Notfound를 띄워준다.
        # return HttpResponseNotFound('Post not found, detail {}'.format(e))

        # 2. post_list view로 돌아간다.

        # 2-1. redirect를 사용
        # return redirect('post:post_list')
        # 2-2. HttpResponseRedirect
        url = reverse('post:post_list')
        return HttpResponseRedirect(url)

    template = loader.get_template('post/post_detail.html')
    context = {
        'post': post,
    }
    rendered_string = template.render(context=context, request=request)
    return HttpResponse(rendered_string)


def post_create(request):
    if request.method == 'POST':
        # get_user_model을 이용해서 얻은 User클래스(Django에서 인증에 사용하는 유저모델)에서 임의의 유저 한명을 가져온다.
        user = User.objects.first()
        # 새 Post 객체를 생성하고 DB에 저
        post = Post.objects.create(
            author=user,
            # request.FILES에서 파일 가져오기
            # 가져온 파일을 ImageField에 넣도록 설정
            # 'file'은 POST요청시 input[type="file"]이 가진 name속성
            photo=request.FILES['file'],
        )

        comment_string = request.POST.get('comment', '')
        if comment_string:
            # 댓글로 사용할 문자열이 전달된 경우 위에서 생성한 post객체에 연결되는 Comment를 생성해준다.
            post.comment_set.create(
                # 임의의 User를 사용 하므로 나중에 실제로 로그인된 사용자로 바꾸어주어야 한다.
                author=user,
                content=comment_string,
            )
        return redirect('post:post_detail', post_pk=post.pk)

    else:
        return render(request, 'post/post_create.html')


def post_modify(request):
    pass


def post_delete(request):
    pass


def comment_create(request):
    pass


def comment_modify(request):
    pass


def comment_delete(request):
    pass


def post_anyway(request):
    return redirect('post:post_list')
