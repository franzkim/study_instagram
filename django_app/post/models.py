from django.conf import settings
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    photo = models.ImageField(upload_to='post', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='like_users',
        through='PostLike',
    )
    tags = models.ManyToManyField('Tag', blank=True)

    def add_comment(self, user, content):
        return self.comment_set.create(author=user, content=content)

    def add_tag(self, tag_name):
        tag, tag_created = Tag.objects.get_or_create(name=tag_name)
        if not self.tags.filter(id=tag.id).exists():
            self.tags.add(tag)

    @property
    def like_count(self):
        return self.like_users.count()


class PostLike(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='like_comments',
        through='CommentLike'
    )


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return 'Tag({})'.format(self.name)