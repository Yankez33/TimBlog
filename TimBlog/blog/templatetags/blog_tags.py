from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


@register.simple_tag  # Will return number of posts published in the blog...in the sidebar
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')  # Will show the latest posts in the sidebar... up to 5
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag  # Will show the posts with the most comments...up to 5
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))  # DJG102: Using safe strings bypasses the Django XSS protection.
    # Found in 'mark_safe(markdown.markdown(text))'.
