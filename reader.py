# -*- coding: UTF-8 -*-
'''
Copyright (c) 2013, Patrick Louis <patrick at unixhub.net>

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

	1.  The author is informed of the use of his/her code. The author does not have to consent to the use; however he/she must be informed.
	2.  If the author wishes to know when his/her code is being used, it the duty of the author to provide a current email address at the top of his/her code, above or included in the copyright statement.
	3.  The author can opt out of being contacted, by not providing a form of contact in the copyright statement.
	4.  If any portion of the author's code is used, credit must be given.
			a. For example, if the author's code is being modified and/or redistributed in the form of a closed-source binary program, then the end user must still be made somehow aware that the author's work has contributed to that program.
			b. If the code is being modified and/or redistributed in the form of code to be compiled, then the author's name in the copyright statement is sufficient.
	5.  The following copyright statement must be included at the beginning of the code, regardless of binary form or source code form.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
import re, os,time
from urllib import urlretrieve
from urllib import URLopener


class mangareader_downloader(object):
	def __init__(self,manga_name,chapter,end_chapter,manga_location,dl_manager):
		self.manga_location = manga_location
		self.manga_name	    = manga_name
		self.chapter		= chapter
		self.end_chapter	= end_chapter
		self.flag		    = False
		self.current_image  = "000"
		self.img			= ""
		self.next_link	    = ""
		self.current_page   = "http://www.mangareader.net/"+self.manga_name+"/"+self.chapter+"/"
		self.next_regex	    = "<span class=\"next\"><a href=\"([^\"]*)\">Next</a></span>"
		self.br             = URLopener()
		self.response       = ""
		self.response_lines = ""
		self.dl_manager	    = dl_manager
		self.resolved       = {
			'http://i0':'188.132.173.122',
			'http://i1':'188.132.173.3',
			'http://i2':'188.132.173.6',
			'http://i3':'188.132.173.9',
			'http://i4':'188.132.173.12',
			'http://i5':'188.132.173.15',
			'http://i6':'188.132.173.18',
			'http://i7':'188.132.173.21',
			'http://i8':'188.132.173.24',
			'http://i9':'188.132.173.27',
			'http://i10':'188.132.173.30',
			'http://i11':'188.132.173.33',
			'http://i12':'188.132.173.36',
			'http://i13':'188.132.173.39',
			'http://i14':'188.132.173.42',
			'http://i15':'188.132.173.45',
			'http://i16':'188.132.173.48',
			'http://i17':'188.132.173.51',
			'http://i18':'188.132.173.54',
			'http://i19':'188.132.173.57',
			'http://i20':'188.132.173.60',
			'http://i21':'188.132.173.63',
			'http://i22':'188.132.173.66',
			'http://i23':'188.132.173.69',
			'http://i24':'188.132.173.72',
			'http://i25':'188.132.173.75',
			'http://i26':'188.132.173.78',
			'http://i27':'188.132.173.81',
			'http://i28':'188.132.173.84',
			'http://i29':'188.132.173.87',
			'http://i30':'188.132.173.90',
			'http://i31':'188.132.173.93',
			'http://i32':'188.132.173.96',
			'http://i33':'188.132.173.99',
			'http://i34':'188.132.173.126',
			'http://i35':'188.132.173.129',
			'http://i36':'188.132.173.132',
			'http://i37':'188.132.173.135',
			'http://i38':'188.132.173.138',
			'http://i39':'188.132.173.141',
			'http://i40':'188.132.173.144',
			'http://i41':'188.132.173.200'
		}

	def increase_current(self):
		self.current_image = str(int(self.current_image)+1)
		if len(self.current_image) == 1:
			self.current_image = "00"+self.current_image
		elif len(self.current_image) == 2:
			self.current_image = "0"+self.current_image

	def increase_chapter(self):
		self.chapter = str(int(self.chapter)+1)

	def check_chapter_end(self):
		if self.next_link.split(self.manga_name)[1].split('/')[1] == self.current_page.split(self.manga_name)[1].split('/')[1]:
			return False
		elif "chapter-"+self.current_page.split(self.manga_name)[1].split('/')[1]+".html" == self.next_link.split(self.manga_name)[1].split('/')[1]:
			return False
		return True

	def not_published(self):
		if "is not published yet. Once" in self.response or self.chapter == str(int(self.end_chapter)+1):
			return True
		return False

	def go_to_next_page(self):
		if not self.check_chapter_end():
			self.increase_current()
		else:
			self.increase_chapter()
			self.current_image = "000"
		self.current_page = self.next_link

	def scrap_page(self):
		self.next_link = re.findall(self.next_regex ,self.response )[0]
		for a in self.response_lines:
			if '"><img id=\"img\"' in a:
				self.img	   = re.findall("src=\"([^\"]*)\" alt",a)[0]
				break
		self.next_link = "http://www.mangareader.net"+self.next_link

	def manage_chapters(self):
		if not os.path.exists(self.manga_location):
			os.mkdir(self.manga_location)
		os.chdir(self.manga_location)
		if not os.path.exists(self.manga_name):
			os.mkdir(self.manga_name)
		os.chdir(self.manga_name)
		if not os.path.exists(self.manga_name+"-"+self.chapter):
			os.mkdir(self.manga_name+"-"+self.chapter)
		os.chdir(self.manga_name+"-"+self.chapter)

	def download_image(self):
		self.manage_chapters()
		caching = self.img.split('.')[0]
		if caching in self.resolved:
			self.img = self.img.replace(
				caching+".mangareader.net",
				"http://"+self.resolved[caching])
		if self.dl_manager == 'default':
			urlretrieve(self.img, self.current_image+'.jpg' )
		else:
			status = 1
			while int(status) != 0:
				status = os.system(self.dl_manager +" "+self.img+ " -o "+self.current_image+".jpg")
		print "[*] Image saved to "+ os.getcwd() + "/"+self.current_image+".jpg"

	def start_downloading(self):
		try:
			self.response       = self.br.open(self.current_page).read()
			self.response_lines = self.response.split("\n")
			if not self.not_published():
				self.scrap_page()
				self.manage_chapters()
				self.download_image()
				self.go_to_next_page()
			else :
				self.flag = True
		except Exception,e:
			print e
			time.sleep(2)
			self.start_downloading()

	def run(self):
		while self.flag == False:
			self.start_downloading()
		print "[*] Finished all the downloads\nEnjoy Your Reading!"
