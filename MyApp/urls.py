from django.conf.urls import url

from . import views

urlpatterns = [

    # ... other url patterns ...

    url(
        r'^generate-sitemap/$',
        views.generate_sitemap
    ),
]
