import time
import random
import re
import requests
import numpy as np
from fonts.font_rendering import Font, Bitmap

CORONA_TABLE_ENDPOINT = 'https://pavelmayer.de/covid/risks/_dash-layout'
API_ENDPOINT = 'http://192.168.0.132'
X = 115
Y = 16

frame_buffer = Bitmap(X, Y)

def reset_buffer():
    for i in range(len(frame_buffer.pixels)):
        frame_buffer.pixels[i] = 0

def set_diff(enable=True):
	val = bytes('0', 'utf-8')
	if enable:
		val = bytes('1', 'utf-8')
	fluepdot_api('/rendering/mode', val)

def render_buffer():
    raw_render_buffer()
    time.sleep(0.3)

def raw_render_buffer():
    text_render = str(frame_buffer)
    data = bytes(text_render, 'utf-8')
    render(data)

def render(data):
	fluepdot_api('/framebuffer', data=data)

def fluepdot_api(path, data):
	requests.post(API_ENDPOINT + path, data=data)

def random_jumps():
	for x in np.nditer(frame_buffer.pixels, flags=['external_loop'],  op_flags=['readwrite'], order='F'):
		vals = [True]
		vals.extend([False] * 5)
		if random.choice(vals):
			x[...] = True
		else:
			x[...] = False

def display_text(text):
    font = Font('fonts/RobotoCondensed-Medium.ttf', 16)
    text_buffer = font.render_text(text)
    #if not text_buffer.height == 16:
    #    raise Exception('Font height must be 16, current height is {}'.format(text_buffer.height))
    frame_buffer.bitblt(text_buffer, 0, 0)
    render_buffer()
    reset_buffer()

def berlin_corona_table():
    res = requests.get(CORONA_TABLE_ENDPOINT)
    data_table = res.json()['props']['children'][2]['props']['data']
    berlin_data = [x for x in data_table if x['Bundesland'] == 'Berlin']
    berlin_data.sort(key=lambda x: int(x['Rang']))
    return berlin_data

def corona_status():
    berlin_data = berlin_corona_table()
    display_text('Corona Status')
    for entry in berlin_data:
        hyphen_regex = re.compile('-\w*')
        district = entry['Landkreis'].replace('SK Berlin', '')
        district = hyphen_regex.sub('', district)
        district = district.strip()
        rank = entry['Rang']
        risk = entry['Kontaktrisiko']
        risk = str(int(risk))
        display_text(district)
        display_text('Rsk: 1/{} #{}'.format(risk, rank)) 

if __name__ == '__main__':
    set_diff()
    while True:
        corona_status()
        time.sleep(5)
        random_jumps()
        render_buffer()
        time.sleep(2)
        continue
        render_buffer()
        frame_buffer.fill(False)
        time.sleep(17)
