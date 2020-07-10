import time
import random
import requests
import numpy as np

API_ENDPOINT = "http://192.168.0.132"
X = 16
Y = 115

frame_buffer = np.empty((X, Y), dtype=bool)

def set_diff(enable=True):
	val = bytes("0")
	if enable:
		val = bytes("1")
	fluepdot_api("/rendering/mode", val)

def render_buffer():
	str = ""
	for line in frame_buffer:
		for val in line:
			if val:
				str += "X"
			else:
				str += " "
		str += "\n"
	data = bytes(str, "utf-8")
	render(data)

def render(data):
	fluepdot_api("/framebuffer", data=data)

def fluepdot_api(path, data):
	requests.post(API_ENDPOINT + path, data=data)

def random_jumps():
	for x in np.nditer(frame_buffer, flags=['external_loop'],  op_flags=["readwrite"], order="F"):
		vals = [True]
		vals.extend([False] * 5)
		if random.choice(vals):
			x[...] = True
		else:
			x[...] = False
		
if __name__ == "__main__":
	while True:
		random_jumps()
		render_buffer()
		time.sleep(0.3)
		continue
		render_buffer()
		frame_buffer.fill(False)
		time.sleep(17)
