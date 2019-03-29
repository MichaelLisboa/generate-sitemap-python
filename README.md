#generate-sitemap-python

Sitemaps are useful for increasing the effectiveness of your SEO. If you head over to [Google's Search Console](https://search.google.com/search-console/about "Google Search Console") you'll find a section to upload a file called `sitemap.xml`.

There are many ways to create this file, from writing it manually (tedious) to having one of many sites out there index your site and generate the file for you. Either of those options are fine for smaller, static websites, but what if you have a large, high traffic, data driven site with constant updates? Well, then you run into problems :-(

But the solution is very easy.

#### This example is done in Python, but the idea is the same for any language.

First, this is what `sitemap.xml` looks like.

```
<?xml version='1.0' encoding='utf-8'?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
	<url>
		<loc>https://www.yoursite.com/</loc>
		<lastmod>2019-03-29</lastmod>
		<changefreq>weekly</changefreq>
		<priority>1.0</priority>
	</url>
	<url>
		<loc>https://www.yoursite.com/product/1/</loc>
		<lastmod>2019-03-29</lastmod>
		<changefreq>weekly</changefreq>
		<priority>0.8</priority>
	</url>
	<url>
		<loc>https://www.yoursite.com/product/2/</loc>
		<lastmod>2019-03-29</lastmod>
		<changefreq>weekly</changefreq>
		<priority>0.8</priority>
	</url>

  ...and so on ...
</urlset>
```

The first part is the XML declaration, which points to the schema on www.sitemaps.org. Following that are the nodes that point to pages on your website. As you can imagine, for large data driven websites with thousands of generated pages, maintaining this file can be really difficult.

##### Let's start coding.

Start by opening a new file in your text editor and add this block of code to generate the XML declaration and root `<url>` node:

```
import xml.etree.cElementTree as ET
from datetime import datetime

def generate_sitemap():

    schema_loc = ("http://www.sitemaps.org/schemas/sitemap/0.9 "
                  "http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd")

    root = ET.Element("urlset")
    root.attrib['xmlns:xsi'] = 'http://www.w3.org/2001/XMLSchema-instance'
    root.attrib['xsi:schemaLocation'] = schema_loc
    root.attrib['xmlns'] = "http://www.sitemaps.org/schemas/sitemap/0.9"

    tree = ET.ElementTree(root)
        tree.write("sitemap.xml",
                   encoding='utf-8', xml_declaration=True)
```
We've started by importing `xml.etree.cElementTree`, a built-in python package for parsing XML. Then we created a function called `generate_sitemap()`, in which we define XML schema info and the `<urlset>` node.

At this point, if you were to run this block of code in your Python Console, it would generate a sitemap.xml file in the current directory that looks sort of like this:

```
<?xml version='1.0' encoding='utf-8'?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
```

So we're off to a good start! Now under that, we're going to write code to generate our static pages like home page, login, registration, etc.

```
_url = "https://www.your-website.com/"  # <-- Your website domain.
dt = datetime.now().strftime("%Y-%m-%d")  # <-- Get current date and time.

doc = ET.SubElement(root, "url")
ET.SubElement(doc, "loc").text = _url
ET.SubElement(doc, "lastmod").text = dt
ET.SubElement(doc, "changefreq").text = 'weekly'
ET.SubElement(doc, "priority").text = "1.0"

doc = ET.SubElement(root, "url")
ET.SubElement(doc, "loc").text = (f"{_url}login/")
ET.SubElement(doc, "lastmod").text = dt
ET.SubElement(doc, "changefreq").text = 'weekly'
ET.SubElement(doc, "priority").text = "0.6"

doc = ET.SubElement(root, "url")
ET.SubElement(doc, "loc").text = f"{_url}register/"
ET.SubElement(doc, "lastmod").text = dt
ET.SubElement(doc, "changefreq").text = 'weekly'
ET.SubElement(doc, "priority").text = "0.6"
```

Just a lot of copy/paste going on. Let's break down what's happening here. We've set two variables:
- `_url` is your website root url.
- `dt` is the current date/time formatted as YYYY-MM-DD

Next we create the `<url>` node as a sub element to the document like this: `doc = ET.SubElement(root, "url")`. Then we create the `<loc>`, `<lastmod>`, `<changefreq>`, and `<priority>` nodes, which are child nodes of the `<url>` node.

Just for the sake of clarity, `f"{_url}login/"` is using string interpolation formatting to create your page URL. In this case, Python will render the string as `https://www.your-website.com/login`. This save us from having to write out your website URL over and over again.

If we were to run this code now, it will generate a file that looks like this:

```
<?xml version='1.0' encoding='utf-8'?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
	<url>
		<loc>https://www.your-website.com/</loc>
		<lastmod>2019-03-29</lastmod>
		<changefreq>weekly</changefreq>
		<priority>1.0</priority>
	</url>
	<url>
		<loc>https://www.your-website.com/login/</loc>
		<lastmod>2019-03-29</lastmod>
		<changefreq>weekly</changefreq>
		<priority>0.8</priority>
	</url>
	<url>
		<loc>https://www.your-website.com/register/</loc>
		<lastmod>2019-03-29</lastmod>
		<changefreq>weekly</changefreq>
		<priority>0.8</priority>
	</url>
</urlset>
```
Pretty cool, right? But what about all those web pages that are generated by your CMS or database? I mean, we can't possibly copy/paste that much stuff.

##### Querying your database

For this part I'm using Django as my frontend to Python. Again, you can use whatever framework or language you want, the idea is still the same. Open your Django app and copy/paste your code into views.py, updating it with the code below.

```
import xml.etree.cElementTree as ET
from datetime import datetime

from django.http import HttpResponse # <-- We need this to return a response
from .models import MyProductModel  # <-- Import my model


def generate_sitemap(request):

    _url = "https://www.your-website.com/"  # <-- Your website domain.
    dt = datetime.now().strftime("%Y-%m-%d")  # <-- Get current date and time.

    doc = ET.SubElement(root, "url")
    ET.SubElement(doc, "loc").text = _url
    ET.SubElement(doc, "lastmod").text = dt
    ET.SubElement(doc, "changefreq").text = 'weekly'
    ET.SubElement(doc, "priority").text = "1.0"

    doc = ET.SubElement(root, "url")
    ET.SubElement(doc, "loc").text = (f"{_url}login/")
    ET.SubElement(doc, "lastmod").text = dt
    ET.SubElement(doc, "changefreq").text = 'weekly'
    ET.SubElement(doc, "priority").text = "0.6"

    doc = ET.SubElement(root, "url")
    ET.SubElement(doc, "loc").text = f"{_url}register/"
    ET.SubElement(doc, "lastmod").text = dt
    ET.SubElement(doc, "changefreq").text = 'weekly'
    ET.SubElement(doc, "priority").text = "0.6"

    return HttpResponse(status="200")
```

We've imported our database model `MyProductModel`, and since we're using Django, we updated our `generate_sitemap` function with the `request` argument and we added an HTTP response.

In short, we've made our sitemap.xml generator into a web page. I'll explain why further down. But first, let's write the code to generate all of our product pages in the CMS.
```
products = MyProductModel.objects.all()

for product in products:  # <-- Loop through product queryset
  doc = ET.SubElement(root, "url")
        ET.SubElement(doc, "loc").text = f"{_url}{product.slug}/"
        ET.SubElement(doc, "lastmod").text = dt
        ET.SubElement(doc, "changefreq").text = 'weekly'
        ET.SubElement(doc, "priority").text = "0.8"
```
What we've done here is query our database for all "product" pages with `MyProductModel.objects.all()`, then loop through the queryset to generate `<url>` nodes for every page. This could be 10 products or 1000 or even more.

Let's look at our `<loc>` node. We were smart from the beginning when we added products to our system because we added slug fields. So instead of a URL like `your-website.com/1028346?sku=28473849/` our product page urls are pretty like `your-website.com/good-life-product/`.

Anyway, the final code looks like this:
```
import xml.etree.cElementTree as ET
from datetime import datetime

from django.http import HttpResponse
from .models import MyProductModel


def generate_sitemap(request):

    _url = "https://www.your-website.com/"  # <-- Your website domain.
    dt = datetime.now().strftime("%Y-%m-%d")  # <-- Get current date and time.

    schema_loc = ("http://www.sitemaps.org/schemas/sitemap/0.9 "
                  "http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd")

    root = ET.Element("urlset")
    root.attrib['xmlns:xsi'] = 'http://www.w3.org/2001/XMLSchema-instance'
    root.attrib['xsi:schemaLocation'] = schema_loc
    root.attrib['xmlns'] = "http://www.sitemaps.org/schemas/sitemap/0.9"

    doc = ET.SubElement(root, "url")
    ET.SubElement(doc, "loc").text = _url
    ET.SubElement(doc, "lastmod").text = dt
    ET.SubElement(doc, "changefreq").text = 'weekly'
    ET.SubElement(doc, "priority").text = "1.0"

    doc = ET.SubElement(root, "url")
    ET.SubElement(doc, "loc").text = (f"{_url}login/")
    ET.SubElement(doc, "lastmod").text = dt
    ET.SubElement(doc, "changefreq").text = 'weekly'
    ET.SubElement(doc, "priority").text = "0.6"

    doc = ET.SubElement(root, "url")
    ET.SubElement(doc, "loc").text = f"{_url}register/"
    ET.SubElement(doc, "lastmod").text = dt
    ET.SubElement(doc, "changefreq").text = 'weekly'
    ET.SubElement(doc, "priority").text = "0.6"

    products = MyProductModel.objects.all()

    for product in products:
      doc = ET.SubElement(root, "url")
            ET.SubElement(doc, "loc").text = f"{_url}{product.slug}/"
            ET.SubElement(doc, "lastmod").text = dt
            ET.SubElement(doc, "changefreq").text = 'weekly'
            ET.SubElement(doc, "priority").text = "0.8"

    tree = ET.ElementTree(root)
        tree.write("sitemap.xml",
                   encoding='utf-8', xml_declaration=True)

    return HttpResponse(status="200")
```

##### Adding the page to your urls.py

For Google to read your sitemap it needs to be rendered as a static XML file and available in your root as `your-website.com/sitemap.xml`. This means we need to add it to our URL patterns as a `TemplateView` in our urls.py.

```
# project/urls.py

from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^sitemap\.xml$',
        TemplateView.as_view(
            template_name='sitemap.xml',
            content_type='text/xml'
            )
        ),
]
```
`TemplateView` will load sitemap.xml, as a static file, from the root of your templates directory. Remember you need to set the content_type to `text/xml` if you want the file to render correctly.

<div class="uk-child-width-2-3@s uk-margin-large-top uk-margin-medium-bottom" uk-grid>
  <div>
    <div class="uk-panel uk-background-primary uk-light uk-padding-small uk-border-rounded">
      On a side note, you can load other static files using `TemplateView`. Here's an example of a boilerplate I use to serve robots.txt, ServiceWorker.js, and manifest.json.
    </div>
  </div>
</div>

```
from django.conf.urls import url
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^manifest\.json$',
        TemplateView.as_view(
            template_name='manifest.json',
            content_type='application/manifest+json'
            )
        ),
    url(r'^ServiceWorker\.js$',
        TemplateView.as_view(
            template_name='ServiceWorker.js',
            content_type='application/javascript'
            )
        ),
    url(r'^robots\.txt$',
        TemplateView.as_view(
            template_name='robots.txt',
            content_type='text/plain'
            )
        ),
    url(r'^sitemap\.xml$',
        TemplateView.as_view(
            template_name='sitemap.xml',
            content_type='text/xml'
            )
        ),
    url(r'^offline\.html$',
        TemplateView.as_view(
            template_name='offline.html',
            content_type='text/html'
            )
        ),
]
```

##### Google Cloud App Engine &amp; Cron jobs
Okay, so we have a url pattern set up to serve our sitemap.xml for search spiders, but how do we generate the file?

We're going to create a Cron job that automatically runs every couple of weeks, to generate our sitemap.xml, and save it to our templates directory.

<div class="uk-child-width-2-3@s uk-margin-large-top uk-margin-medium-bottom" uk-grid>
  <div>
    <div class="uk-panel uk-background-primary uk-light uk-padding-small uk-border-rounded">
      I'm not going to go into detail about setting up your project on Google Cloud, that's a whole other story. And again, you could be using another platform like AWS or even hosting yourself, it doesn't matter.
    </div>
  </div>
</div>

Let's create a url pattern for our `generate_sitemap` view and add it to the app urls.py:

```
# app/urls.py

from django.conf.urls import url

from . import views

urlpatterns = [

    ... other url patterns ...

    url(
        r'^generate-sitemap/$',
        views.generate_sitemap
    ),
]
```
Now you should be able to visit http://localhost:8000/generate-sitemap/ and your sitemap function will create the sitemap.xml file in your templates directory.

Excellent.

Next, in your project root directory, create a file called `cron.yaml` then add this:

```
# root/cron.yaml

cron:
- description: "Generate MySitemap CRON"
  url: /generate-sitemap/
  schedule: every 14 days
  retry_parameters:
    min_backoff_seconds: 120
    max_doublings: 5
```
This creates a Cron job for App Engine that will visit your generate_sitemap function at `www.your-website/generate-sitemap/` every 14 days to generate an updated sitemap.xml file and save it to your templates directory so that it's accessible by Google and other search engines.

Push the Cron job to App Engine with this terminal command:

`gcloud app deploy cron.yaml`

Then visit your Google Console, under App Engine, you'll see a link for Cron jobs, where you'll find your new "Generate MySitemap CRON" job listed.

<img src="https://raw.githubusercontent.com/MichaelLisboa/generate-sitemap-python/master/static/images/cron.png" />

Okay, you now have a Cron job set up to visit your sitemap generator every 14 days. But, there's a problem...

##### Security?

We don't want just anybody to have access, we only want our Cron job to access the function. But then, we can't give the Cron job admin access either.

So, we're going to use headers to exclude any connections not from our Cron job. This is safe because the `x-appengine-cron` header is only passed within Google's network, meaning it's unlikely to be spoofed.

We need to update our view to block everybody except our Cron job.

```
import xml.etree.cElementTree as ET
from datetime import datetime

from django.http import HttpResponse
from .models import MyProductModel


def generate_sitemap(request):

    _url = "https://www.your-website.com/"  # <-- Your website domain.
    dt = datetime.now().strftime("%Y-%m-%d")  # <-- Get current date and time.

    schema_loc = ("http://www.sitemaps.org/schemas/sitemap/0.9 "
                  "http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd")

    if request.META.get('HTTP_X_APPENGINE_CRON'):  #  <-- check if the x-appengine-cron header exists
      root = ET.Element("urlset")
      root.attrib['xmlns:xsi'] = 'http://www.w3.org/2001/XMLSchema-instance'
      root.attrib['xsi:schemaLocation'] = schema_loc
      root.attrib['xmlns'] = "http://www.sitemaps.org/schemas/sitemap/0.9"

      doc = ET.SubElement(root, "url")
      ET.SubElement(doc, "loc").text = _url
      ET.SubElement(doc, "lastmod").text = dt
      ET.SubElement(doc, "changefreq").text = 'weekly'
      ET.SubElement(doc, "priority").text = "1.0"

      doc = ET.SubElement(root, "url")
      ET.SubElement(doc, "loc").text = (f"{_url}login/")
      ET.SubElement(doc, "lastmod").text = dt
      ET.SubElement(doc, "changefreq").text = 'weekly'
      ET.SubElement(doc, "priority").text = "0.6"

      doc = ET.SubElement(root, "url")
      ET.SubElement(doc, "loc").text = f"{_url}register/"
      ET.SubElement(doc, "lastmod").text = dt
      ET.SubElement(doc, "changefreq").text = 'weekly'
      ET.SubElement(doc, "priority").text = "0.6"

      products = MyProductModel.objects.all()

      for product in products:
        doc = ET.SubElement(root, "url")
              ET.SubElement(doc, "loc").text = f"{_url}{product.slug}/"
              ET.SubElement(doc, "lastmod").text = dt
              ET.SubElement(doc, "changefreq").text = 'weekly'
              ET.SubElement(doc, "priority").text = "0.8"

      tree = ET.ElementTree(root)
          tree.write("sitemap.xml",
                     encoding='utf-8', xml_declaration=True)

      return HttpResponse(status="200")
    else:
      return HttpResponse(status="403")  # <-- Return "Not Allowed" for everybody else.
```

Now you can deploy your project `gcloud app deploy` and test your Cron job by clicking the "Run now" button on your Cron page on Google Console.

And that's it!
