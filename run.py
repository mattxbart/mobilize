import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString, Tag
from jinja2 import Template
import re
import os

base_dir = '/home/mbartolome/mobiletest/mobilize'

template = Template(open(os.path.join(base_dir, 'bootstrap.html')).read())
scrape = [
    ('http://www.sdcwa.org/find-your-water-district', 'find-your-water-district'),
    ('http://www.sdcwa.org/protecting-regional-water-supply-reliability','protecting-regional-water-supply-reliability'),
    ('http://www.sdcwa.org/conservation-programs-rebates','conservation-programs-rebates'),
    ('http://www.sdcwa.org/drought-resources','drought-resources'),
    ('http://www.sdcwa.org/drought-contact','drought-contact'),
    ('http://www.sdcwa.org/drought-freebies','drought-freebies'),
    ('http://www.sdcwa.org/water-saving-superstars-partners','water-saving-superstars-partners'),
    ('http://www.sdcwa.org/drought-state-restrictions','drought-state-restrictions'),
    ('http://www.sdcwa.org/drought-campaign-ads-messages','drought-campaign-ads-messages'),
    ('http://www.sdcwa.org/drought-information','drought-information'),
    ('http://www.sdcwa.org/drought-10-watersmart-tips','drought-10-watersmart-tips'),
    ('http://www.sdcwa.org/drought-conditions', 'drought-conditions'),
    ('http://www.sdcwa.org/drought-faq', 'drought-faq'),
    ('http://www.sdcwa.org/water-use', 'water-use'),
      ]
links = []

img_re = re.compile(r"image-")

i = 1
for link,slug in scrape:
    print link
    r = requests.get(link)
    t = r.text
    soup = BeautifulSoup(t, 'html.parser')
    soup.prettify(formatter='html')
    title = soup.h1.contents[0]

    stuff = soup.body.findAll('div', {"class": "node odd full-node node-type-page"})
    if not stuff:
        stuff = soup.body.findAll('div', {"class": "content-group row nested grid12-9"})

    body_content = ''
    for thing in stuff:

        for style in thing.findAll('style'):
            style.replace_with('')

        for content in thing.findAll('div'):

            if content.h1:
                content.h1.replace_with('')
                
            for div in content.findAll('div', {"class": "breadcrumb"}):
                div.replace_with("")

            for div in content.findAll('div', {"id": "faq-expand-all"}):
                div.replace_with("")

            for div in content.findAll('div', {"class": "share-wrapper"}):
                div.replace_with("")

            for img in content.findAll('img'):
                del img['style']
                img['class'] = 'img-responsive'
            for div in content.findAll('div', {"class": "links"}):
                div.replace_with("")

            for div in content.findAll('div', {"class": "dashed-line"}):
                div.replace_with("")

            for div in content.findAll('div'):
                pass

            for span in content.findAll('span', {"class": "photo-title"}):
                span['class'] = 'caption'

            for div in content.findAll('div', {"class": img_re}):
                for c in div.find_all('span', {"class": "photo-caption"}):
                    caption = "".join(c.find_all(text=True))
                img = div.img
                del img['style']
                img['class'] = 'img-responsive'
                new_caption = soup.new_tag("div")
                new_caption['class'] = 'caption'

                text = soup.new_tag("h4")
                text.append(caption)
                new_caption.append(text)
                img.append(new_caption)
                div.replace_with(img)
            body_content+=str(content)
            break
    content = template.render(title=title, body=body_content.decode('utf-8', 'ignore'))

    link = '{0}.html'.format(slug)
    links.append({"href":link, "title": title})
    f = open(os.path.join(base_dir, 'pages/{0}'.format(link)), 'w')
    f.write(content.encode('utf-8'))
    i += 1


index_template = Template(open(os.path.join(base_dir, 'index.html')).read())
c = index_template.render(links=links)
f = open(os.path.join(base_dir, 'pages/index.html'), 'w')
f.write(c)

