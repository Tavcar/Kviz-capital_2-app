#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import jinja2
import webapp2
from random import randint
import random

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class Country(object):
    def __init__(self, name, capital, image):
        self.name = name
        self.capital = capital
        self.image = image

"""def main():
    drzave_file = open("drzave.txt", "w")

    drzave_list = []

    for item in drzave_file:
        name, capital, image = item.split(";")

        country = Country(name=name, capital=capital, image=image)
        drzave_list.append(country)
"""

def RandomCountry(drzave_list):
    a = random.choice(drzave_list)
    return a

drzave = [Country("Slovenija", "Ljubljana",
                  "http://www.hotelcubo.com/wp-content/uploads/2014/09/Ljubljana_Jeseni%C4%8Dnik.jpg"),
          Country("Hrvaska", "Zagreb",
                  "http://www.travelandleisure.com/sites/default/files/styles/tnl_redesign_article_landing_page/public/1448052729/zagreb-croatia-WTG0116.jpg?itok=IIpWCtBo"),
          Country("Avstrija", "Dunaj",
                  "http://www.austria.info/media/17083/thumbnails/stadtansicht-wien--oesterreich-werbung-julius-silver--d.jpg.3146497.jpg")]

b = RandomCountry(drzave)
a = b

class MainHandler(BaseHandler):
    def get(self):

        params = {"picture": b.image, "country": b.name}
        return self.render_template("kviz.html", params=params)

    def post(self):
        ugibanje = self.request.get("vnos")

        if ugibanje.lower() == a.capital.lower():
            a = RandomCountry(drzave)
            global a
            sporocilo = {"sporocilo": "Pravilen!", "picture": a.image, "country": a.name}
            return self.render_template("kviz.html",params=sporocilo)
        else:
            a = RandomCountry(drzave)
            global a
            sporocilo = {"sporocilo": "Napacen", "picture": a.image, "country": a.name}
            return self.render_template("kviz.html",params=sporocilo)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
