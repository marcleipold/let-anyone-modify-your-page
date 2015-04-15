import os

import jinja2
import webapp2
import cgi

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

def escape_html(s):
    return cgi.escape(s, quote = True)


months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

month_abbvs = dict((m[:3].lower(), m) for m in months)

def valid_month(month):
    if month:
        short_month = month[:3].lower()
        return month_abbvs.get(short_month)

def valid_day(day):
    if day and day.isdigit():
        day = int(day)
        if day > 0 and day <=31:
            return day

def valid_year(year):
    if year and year.isdigit():
        year = int(year)
        if year > 1900 and year <=2020:
            return year

form = """
<form method="post">
What is your Birthday?
<br>
<br>

<label> 
    Month
    <input type="text" name="month" value="%(month)s">
</label>

<label> 
    Day
    <input type="text" name="day" value="%(day)s">
</label>

<label> 
    Year
    <input type="text" name="year" value="%(year)s">
</label>
<div style="color: red">%(error)s</div>
<br>
<br>
<input type="submit">
</form>
"""






class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
    	t = jinja_env.get_template(template)
    	return t.render(params)

    def render(self, template, **kw):
    	self.write(self.render_str(template, **kw)) 

class MainPage(webapp2.RequestHandler):
    def write_form(self, error="", month="", day="", year=""):
        self.response.out.write(form % {"error": error,
                                        "month": escape_html(month),
                                        "day": escape_html(day),
                                        "year": escape_html(year)})

    def get(self):
        self.write_form()

    def post(self):
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')

        month = valid_month(user_month)
        day = valid_day(user_day)
        year = valid_year(user_year)

        if not (month and day and year):
            self.write_form("That doesn't look valid to me!!",
                            user_month, user_day, user_year)
        else:
            self.redirect("/shoppinglist")

class ShoppingList(Handler):
    def get(self):
        self.render('shoppinglist.html')

        # output = form_html
        # output_hidden = ""

        # items = self.request.get_all("food")
        # if items:
        #     output_items = ""
        #     for item in items:
        #         output_hidden += hidden_html % item
        #         output_items += item_html % item

        #     output_shopping = shopping_list_html % output_items
        #     output += output_shopping

        # output = output % output_hidden


app = webapp2.WSGIApplication([('/', MainPage), ('/shoppinglist', ShoppingList)],debug=True)
    						   