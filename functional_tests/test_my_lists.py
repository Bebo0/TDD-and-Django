from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionalTest
User = get_user_model()

""" Each client (IP) is given a unique session ID which is stored in a cookie and submitted with ever request.
The server will store this ID somewhere (typically in the database) and then it
can recognize each request that comes in as being from a particular client.
The server can mark a client's session as being an authenticated (logged in) session
and associate it with a user ID in its database. 

A session is a dictionary-like data structure, and the user ID is stored under the key 
given by django.contrib.auth.SESSION_KEY.
"""

class MyListsTest(FunctionalTest):

	def create_pre_authenticated_session(self, email):

		user = User.objects.create(email=email)
		session = SessionStore()
		session[SESSION_KEY] = user.pk # we create a session object in the db
		# the session key is the primary key of the user object which is actually the user's email address
		session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
		session.save()
		## to set a cookie we need to first visit the domain.
		## 404 pages load the quickest!
		self.browser.get(self.live_server_url + "/404_no_such_url/")
		self.browser.add_cookie(dict(
			name=settings.SESSION_COOKIE_NAME,
			value=session.session_key, # we then add a cookie to the browser that matches the session on the server.
			# on our next visit to the site, the server should recognize us as a logged-in user.
			path='/',
		))

	def test_logged_in_users_lists_are_saved_as_my_lists(self):
		email = 'edith@example.com'
		self.browser.get(self.live_server_url)
		self.wait_to_be_logged_out(email)

		# Edith is a logged-in user
		self.create_pre_authenticated_session(email)
		self.browser.get(self.live_server_url)
		self.wait_to_be_logged_in(email)