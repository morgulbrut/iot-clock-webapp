__author__ = 't800'

import webapp2
import jinja2
import os
import json

from google.appengine.api import urlfetch
from google.appengine.api import urlfetch_errors


with open('config.json') as data_file:
    data = json.load(data_file)
    particle_id = data["Particle_ID"]
    access_token = data["Access_Token"]



clock_modes = ['Normal', 'Rainbow Secs', 'Random Secs', 'Rainbow and Random Secs', 'Trails', 'Rainbow Secs and Trails',
               'Random Secs and Trails', 'Rainbow, Random Secs and Trails', 'Reversed Normal', 'Reversed Rainbow Secs',
               'Reversed Rainbow and Random Secs', 'Reversed Random Secs', 'Reversed Trails',
               'Reversed Rainbow Secs and Trails', 'Reversed Random Secs and Trails',
               'Reversed Rainbow, Random Secs and Trails', 'Binary']

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        try:
            config = json.loads(urlfetch.fetch(
                'https://api.particle.io/v1/devices/' + particle_id + '/getConfig?access_token=' + access_token,
                method=urlfetch.GET).content)['result']
            params = eval(config)

            mode = params['mode']
            hour_hue = params['hourHue']
            minute_hue = params['minuteHue']
            second_hue = params['secondHue']
            brightness = params['brightness']
            wifi = params['wifi']

            self.build_form(mode, hour_hue, minute_hue, second_hue, brightness, wifi, False)


        except urlfetch_errors.DeadlineExceededError:
            template = JINJA_ENVIRONMENT.get_template('templates/offline.html')
            self.response.write(template.render())

        except:
            raise

    def post(self):

        mode = self.request.get('mode')
        hour_hue = self.request.get('hour_hue')
        minute_hue = self.request.get('minute_hue')
        second_hue = self.request.get('second_hue')
        brightness = self.request.get('brightness')

        urlfetch.fetch(
            'https://api.particle.io/v1/devices/' + particle_id + '/setHaMode?access_token=' + access_token,
            payload='params=' + str(mode), method=urlfetch.POST)
        urlfetch.fetch(
            'https://api.particle.io/v1/devices/' + particle_id + '/setHHue?access_token=' + access_token,
            payload='params=' + str(hour_hue), method=urlfetch.POST)
        urlfetch.fetch(
            'https://api.particle.io/v1/devices/' + particle_id + '/setMHue?access_token=' + access_token,
            payload='params=' + str(minute_hue), method=urlfetch.POST)
        urlfetch.fetch(
            'https://api.particle.io/v1/devices/' + particle_id + '/setSHue?access_token=' + access_token,
            payload='params=' + str(second_hue), method=urlfetch.POST)
        urlfetch.fetch(
            'https://api.particle.io/v1/devices/' + particle_id + '/setBright?access_token=' + access_token,
            payload='params=' + str(brightness), method=urlfetch.POST)

        wifi = json.loads(urlfetch.fetch(
            'https://api.particle.io/v1/devices/' + particle_id + '/getWifi?access_token=' + access_token,
            method=urlfetch.GET).content)['result']

        self.build_form(mode, hour_hue, minute_hue, second_hue, brightness, wifi, True)

        # self.response.write(self.request)

    def build_form(self, mode, hour_hue, minute_hue, second_hue, brightness, wifi, done):
        template_values = {'clock_modes': clock_modes, 'mode': mode, 'hour_hue': hour_hue, 'minute_hue': minute_hue,
                           'second_hue': second_hue, 'brightness': brightness, 'wifi': wifi, 'done': done}
        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
