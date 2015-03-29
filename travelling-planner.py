#!/usr/local/bin/python
#-*- coding: utf-8 -*-

import sys
import os
import webapp2
import cgi
import re
import jinja2
import json

from tsp import solve_tsp

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

#####################

class L1H1_MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write("Hello, Udacity!")

#####################

class L2_MainPage(webapp2.RequestHandler):

    def write_form(self, error=""):
        form = """
        <form method="post" action="/l2/testform">
            <input type="password" name="q">
            <input type="submit">
        </form>
        <br>
        %(error)s
        """
        self.response.write(form % {"error": error})

    def get(self):
        self.write_form()


class L2_TestHandler(webapp2.RequestHandler):
    
    def post(self):
        q = self.request.get("q")
        self.response.write(q)
        # self.response.headers['Content-Type'] = 'text/plain'
        # self.response.write(self.request)

######################

class L2H1_MainPage(webapp2.RequestHandler):

    def write_form(self, text=""):
        form = """
        <p>Enter some text to ROT13:</p>
        <form method="post">
            <textarea name="text" rows="10" cols="50">%s</textarea>
            <br>
            <input type="submit">
        </form>
        """
        self.response.write(form % text)

    def get(self):
        self.write_form()

    def post(self):
        text = self.request.get("text")
        new_text = ''.join(map(self.rot13, text))
        print "----------"
        print text
        print new_text
        print cgi.escape(new_text)
        self.write_form(cgi.escape(new_text))

    def rot13(self, c):
        alpha_table = "abcdefghijklmnopqrstuvwxyz"
        if c.isalpha():
            new_idx = (alpha_table.index(c.lower()) + 13) % len(alpha_table)
            new_c = alpha_table[new_idx]
            if c.isupper():
                new_c = new_c.upper()
            return new_c
        else:
            return c

######################

class L2H2_MainPage(webapp2.RequestHandler):

    def write_signup_form(self, username="", email="",
        error_username="", error_password="", error_verify="", error_email=""):
        form = """
        <h1>Signup</h1>
        <form method="post">
            <label>Username
                <input name="username" type="text" value=%(username)s>
                <span style="color:red">%(error_username)s</span>
            </label>
            <br>
            <label>Password
                <input name="password" type="password" value="">
                <span style="color:red">%(error_password)s</span>
            </label>
            <br>
            <label>Verify Password
                <input name="verify" type="password" value="">
                <span style="color:red">%(error_verify)s</span>
            </label>
            <br>
            <label>Email (optional)
                <input name="email" type="text" value=%(email)s>
                <span style="color:red">%(error_email)s</span>
            </label>
            <br>
            <input type="submit">
        </form>
        """
        self.response.write(form % {"username": username, "email": email,
                "error_username": error_username, "error_password": error_password,
                "error_verify": error_verify, "error_email": error_email})

    def get(self):
        self.write_signup_form()

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        error_username = error_password = error_verify = error_email = ""
        success = True

        if not self.valid_username(username):
            error_username = "Invalid username."
            success = False

        elif not self.valid_password(password):
            error_password = "Invalid password."
            success = False

        elif not self.valid_verify(password, verify):
            error_verify = "Two passwords are not same."
            success = False

        elif not self.valid_email(email):
            error_email = "Invalid email."
            success = False

        if success:
            self.redirect("/l2h2/welcome?user=%s" % username)
        else:
            self.write_signup_form(username=username, email=email,
                error_username=error_username, error_password=error_password,
                error_verify=error_verify, error_email=error_email)


    def valid_username(self, username):
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        return username and USER_RE.match(username)

    def valid_password(self, password):
        PASSWORD_RE = re.compile(r"^.{3,20}$")
        return password and PASSWORD_RE.match(password)

    def valid_verify(self, password, verify):
        if password and (password == verify):
            return password
        else:
            return None

    def valid_email(self, email):
        EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
        return not email or EMAIL_RE.match(email)


class L2H2_Welcome(webapp2.RequestHandler):

    def get(self):
        username = self.request.get("user")
        self.response.write("Welcome, %s!" % username)

######################

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_data(self, data):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(data))

######################

class L3_MainPage(Handler):

    def render_front(self, title="", art="", error=""):
        self.render("base.html", title=title, art=art, error=error)

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")

        if title and art:
            self.write("Thanks!")
        else:
            self.render_front(title=title, art=art, error="Invalid input.")


##########################


class MainPage(Handler):

    def render_front(self):
        self.render("main.html")

    def get(self):
        print "get get request"
        self.render_front()

    def post(self):
        points = self.request.get("points")
        # points format (string): "(lat_1, lng_1)-(lat_2, lng_2)-...(lat_n, lng_n)"
        points = [tuple(map(float, p.lstrip('(').rstrip(')').split(','))) for p in points.split('-')]
        # print points
        route = solve_tsp(points, point_type='latlng', dist_type='Euclidean')
        # print route
        self.render_data(route)

############################

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/l3', L3_MainPage),
    ('/l1h1', L1H1_MainPage),
    ('/l2', L2_MainPage),
    ('/l2/testform', L2_TestHandler),
    ('/l2h1', L2H1_MainPage),
    ('/l2h2', L2H2_MainPage),
    ('/l2h2/welcome', L2H2_Welcome)
], debug=True)
        




