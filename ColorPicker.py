import tkinter   as tk

import mss

from PIL import Image

import time

from CursorChanger import *

from pynput.mouse import Listener


greeen_screen_color = '#867e36'
sct = mss.mss()
#print(sct.monitors)
def get_screenshot():
	monitor_1 = sct.monitors[0]
	screenshot = sct.grab(monitor_1)
	img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
	#img.show()
	return img

class App(object):
	pos = None
	listener = None
	pix = None
	value_type = 'rgb'
	def __init__(self,root):
		self.root = root
		self.root.title("Color Picker")
		self.build()
	def bring2front(self):
		self.root.attributes("-topmost", True)
		self.root.attributes("-topmost", False)
		
	def test(self):
		self.value_type = 'hex' if self.value_type == 'rgb' else 'rgb'
		self.rgb_hex_button.configure(text = self.value_type.upper())
		
		if self.pix:
			self.update_value()
			
	def build(self):
		root = self.root
		
		l = tk.LabelFrame(root, text="RGB Color Picker", padx=0, pady=0)
		l.pack(fill = 'x')

		value = tk.StringVar()
		value.set("None") 
		
		button=  tk.Button(l, text="Pick Color", command=self.get_RGB_button_callback)
		button.pack(pady=10,side = 'left' )

		rgb_hex_button=  tk.Button(l, text="RGB", command=self.test)
		rgb_hex_button.pack(pady=10,side = 'left' )
		#--------------------------------#
		width = 200
		l2 = tk.LabelFrame(root, text="",width = width,height =25,padx=0, pady=0)
		l2.pack()


		entree = tk.Entry(l2, textvariable=value,width=10)
		#entree.pack(side = 'left')
		entree.place(relheight=0.9, relwidth=1-25/width) #relheight, relwidth 
		
		color_box = tk.Canvas(l2, bg="white",highlightthickness=1, highlightbackground="black")
		#color_box.pack(side = 'right' )
		color_box.place( relx=1,relheight=1,relwidth=25/width,anchor = 'ne')
		### --------- instance attributes ----------###
		self.value = value
		self.button = button
		self.color_box = color_box
		self.rgb_hex_button = rgb_hex_button
		root.update()

		root.minsize(root.winfo_width(), root.winfo_height())
				
	def get_RGB_button_callback(self):
		if not self.button["state"] == 'disabled':
			self.button["state"] ="disabled"
			self.make_cross()
			self.root.after(200,self._waiting_for_press)
		
	def _waiting_for_press(self):
		
		pos = self.get_mouse_click()
		#img = get_screenshot()
		#print(pos)

		#pix = img.getpixel(pos)
		#self.value.set('RGB = '+str(pix)) 
		#print(pix)
		
	def update_value(self):
		
		hexx_value = '#%02x%02x%02x' % self.pix 
		rgb_value = str(self.pix)

		self.value.set(hexx_value if self.value_type == 'hex' else rgb_value) 
		self.color_box.configure(bg=hexx_value)
	@staticmethod
	def make_cross():
		cross1 = CursorChanger.get_current(OCR_CROSS)
		cross2 = CursorChanger.get_current(OCR_CROSS)
		cross3 = CursorChanger.get_current(OCR_CROSS)
		CursorChanger.change(cross1,OCR_NORMAL)
		CursorChanger.change(cross2,OCR_IBEAM)
		CursorChanger.change(cross3,OCR_HAND)
	def get_pix(self,img,pos):
		x,y = pos
		monitor = sct.monitors[0]
		x = x - monitor['left']
		return x,y

	def on_click(self,x,y,button,b):
		self.pos = (x,y)
		img = get_screenshot()
		self.pix = img.getpixel(self.get_pix(img,self.pos))
		self.listener.stop()
		self.root.after(10,self.bring2front)
		self.root.after(100,CursorChanger.restore_all)
		self.root.after(0,self.update_value)
		self.root.after(75, lambda :self.button.configure(state = "normal")) 
		
		#print((x,y))

	def get_mouse_click(self):
		self.listener = Listener(on_click = self.on_click)
		self.listener.start()
		#self.listener.join()
		return self.pos
	

	
import tempfile 
import base64
import os
from my_icon import icon_base64 as icon
icondata= base64.b64decode(icon)
tempFile = 'icon.ico'

tempDir = tempfile.TemporaryDirectory()

tempFile = tempDir.name + '\\'+tempFile



iconfile= open(tempFile,"wb")
iconfile.write(icondata)
iconfile.close()
root = tk.Tk()
#icon_path = 'icon.ico'


root.wm_iconbitmap(tempFile)
#os.remove(tempFile)

app = App(root)
app.tempDir = tempDir
#img = Image.open('icon.png')


root.mainloop() 

