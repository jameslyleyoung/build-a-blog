import webapp2
import os
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Post(db.Model):
    title = db.StringProperty(required = True)
    post = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class Index(Handler):
    def get(self):
        self.render("base.html")

    def post(self):
        title = self.request.get("title")
        post = self.request.get("post")

        if title and post:
            a = Post(title=title, post=post)
            a.put()

            self.redirect('/')
        else:
            error = "we need both a title and some text for a post!"
            self.render_blog(title, art, error)

class NewPost(Handler):
    def get(self):
        self.render("newpost.html")

    def post(self):
        title = self.request.get("title")
        post = self.request.get("post")

        if title and post:
            a = Post(title=title, post=post)
            a.put()

            self.redirect('/')
        else:
            error = "we need both a title and some text for a post!"
            self.render("newpost.html", title=title, post=post, error=error)

class Blog(Handler):
    def render_blog(self, title="", posts="", error=""):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 5")

        self.render("blog.html", title=title, error=error, posts=posts)

    def get(self):
        self.render_blog()

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/newpost', NewPost),
    ('/blog', Blog)
], debug=True)
