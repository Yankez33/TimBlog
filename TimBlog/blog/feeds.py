import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post


class LatestPostFeeds(Feed):  # Defining the feed
    title = 'My Blog'
    link = reverse_lazy('blog:post_list')  # Generates the URL for the link. Reverse builds URLs by their name and passes
    #  optional parameters
    description = "New posts of my blog"

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):  # Will receive each item and return the title
        return item.title

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)  # Will convert markdown to HTML

    def item_pubdate(self, item):
        return item.publish
