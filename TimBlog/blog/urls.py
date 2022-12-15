from django.urls import path
from . import views
from .feeds import LatestPostFeeds

app_name = 'blog'  # defines the application name. Allows you to organize URLs by app name

urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    # path('', views.PostListView.as_view(), name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('feed/', LatestPostFeeds(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
]  # the <> captures the value specified and returns it as a string


