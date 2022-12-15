from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    changefreq = 'weekly'  # indicates how often posts are changed
    priority = 0.9  # prioritizes relevance. Max value is 1

    def items(self):  # Returns the queryset of objects to include in sitemap
        return Post.published.all()

    def lastmod(self, obj):  # Returns ladt time object was modified
        return obj.updated
