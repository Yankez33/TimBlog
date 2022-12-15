from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):  # adds status field to model for draft / published
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)  # creates title for blog post
    slug = models.SlugField(max_length=250, unique_for_date='publish')  # creates URLs for blog post. unique_for_date
    # prevents storing of duplicated posts by defining slugs to be unique for publication date
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')  # defines user of the post
    # and CASCADE ensures when a user is deleted, all related posts are deleted from the database
    body = models.TextField()  # creates the body of the blog post
    publish = models.DateTimeField(default=timezone.now)  # stores the date / time the post was published
    created = models.DateTimeField(auto_now_add=True)  # stores the date / time the post was created
    updated = models.DateTimeField(auto_now=True)  # stores the date / time post was last updated
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)  # see class Status
    objects = models.Manager()  # The default manager
    published = PublishedManager()  # Our custom manager
    tags = TaggableManager()  # allows for tags within posts

    class Meta:
        ordering = ['-publish']  # sets the default ordering for the model
        indexes = [models.Index(fields=['-publish'])]  # improves queries performance.  The - before publish defines
        # descending order

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # A Conical URL. It allows you to specify the URL for the master copy of a page
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'




