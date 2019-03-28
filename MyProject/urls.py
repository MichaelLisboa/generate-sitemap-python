from django.conf.urls import url
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^sitemap\.xml$',
        TemplateView.as_view(
            template_name='sitemap.xml',
            content_type='text/xml'
            )
        )
]
