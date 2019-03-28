import xml.etree.cElementTree as ET
from datetime import datetime

from django.http import HttpResponse

from .models import MyProductModel


def generate_sitemap(request):

    _url = "https://www.your-website.com/"  # <-- Your website domain.
    dt = datetime.now().strftime("%Y-%m-%d")  # <-- Get current date and time.

    schema_loc = ("http://www.sitemaps.org/schemas/sitemap/0.9 "
                  "http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd")

    # check if the x-appengine-cron header exists
    if request.META.get('HTTP_X_APPENGINE_CRON'):
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
        # <-- Return "Not Allowed" for everybody else.
        return HttpResponse(status="403")
