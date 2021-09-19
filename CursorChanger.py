import win32api
import time
import win32gui
import win32con
import ctypes

OCR_APPSTARTING = 32650     #Standard arrow and small hourglass
OCR_NORMAL = 32512          #Standard arrow
OCR_CROSS = 32515   		#Crosshair
OCR_HAND = 32649   			#Hand
OCR_HELP = 32651   			#Arrow and question mark
OCR_IBEAM = 32513   		#I-beam
OCR_NO = 32648   			#Slashed circle
OCR_SIZEALL = 32646   		#Four-pointed arrow pointing north, south, east, and west
OCR_SIZENESW = 32643		 #Double-pointed arrow pointing northeast and southwest
OCR_SIZENS = 32645 			#Double-pointed arrow pointing north and south
OCR_SIZENWSE = 32642		 #Double-pointed arrow pointing northwest and southeast
OCR_SIZEWE = 32644 			#Double-pointed arrow pointing west and east
OCR_UP = 32516 				#Vertical arrow
OCR_WAIT = 32514			 #Hourglass






class _CursorChanger(object):
	"""docstring for CursorChanger"""
	CURSOR_IDS = [OCR_APPSTARTING, OCR_NORMAL,OCR_CROSS,OCR_HAND, OCR_HELP, OCR_IBEAM, OCR_NO, OCR_SIZEALL, OCR_SIZENESW, OCR_SIZENS,OCR_SIZENWSE,OCR_SIZEWE,OCR_UP ,OCR_WAIT]
	CURSOR_BACKUPS = {} 


	def __init__(self):
		self.backup_all()
	
	def __del__(self):
		self.restore_all()

	def get_current(self,cursor_id):
		hold = win32gui.LoadImage(0, cursor_id, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_SHARED )
		hsave = ctypes.windll.user32.CopyImage(hold, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_COPYFROMRESOURCE)
		return hsave

	def backup(self,cursor_id):
		hsave = self.get_current(cursor_id)
		self.CURSOR_BACKUPS[cursor_id] = hsave
		return hsave

	def backup_all(self,):
		for cursor_id in self.CURSOR_IDS:
			self.backup(cursor_id)
		#print('Default Cursors Backed Up')
	def restore(self,cursor_id):
		ctypes.windll.user32.SetSystemCursor(self.CURSOR_BACKUPS[cursor_id], cursor_id)

	def restore_all(self):
	
		for cursor_id in self.CURSOR_BACKUPS:
			self.restore(cursor_id)
		#print('Default Cursors Restored')

	@staticmethod		
	def open_cursor_image(filename):
		hcursor = win32gui.LoadImage(0, filename, 
	                             win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE);
		return hcursor

	
	def change(self,cursor_image,cursor_id):
		self.backup(cursor_id)
		ctypes.windll.user32.SetSystemCursor(cursor_image, cursor_id)


CursorChanger = _CursorChanger()

if __name__ == '__main__':
	

	
	cross1 = CursorChanger.get_current(OCR_CROSS)
	cross2 = CursorChanger.get_current(OCR_CROSS)
	CursorChanger.change(cross1,OCR_NORMAL)
	CursorChanger.change(cross2,OCR_IBEAM)
	time.sleep(5)

	
	

