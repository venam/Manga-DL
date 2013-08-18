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
import completer,park,reader,readline,sys,os

__version__    = "0.3"
__author__     = "venam"
__maintainer__ = "venam"
__email__      = "patrick at unixhub.net"
__status__     = "working but needs updates"

class main(object):
	def __init__(self):
		self.conf = {
		"manga_location":"",
		"manga_name":"",
		"start_chapter":"",
		"end_chapter":""
		}
		self.comp = completer.Completer()
		readline.set_completer_delims(' \t\n;')
		readline.parse_and_bind("tab:complete")
		readline.set_completer(self.comp.complete)

	def take_conf(self):
		self.conf['manga_location'] = raw_input("Enter the mangas location     -> ")
		self.conf['manga_name']	    = raw_input("Enter the manga name          -> ")
		self.conf['start_chapter']  = raw_input("Enter the manga start chapter -> ")
		self.conf['end_chapter']    = raw_input("Enter the manga end chapter   -> ")

	def start(self,which,take_conf):
		if which == "park":
			print "[+] You have chosen mangapark instead of mangareader (default)"
		if take_conf:
			self.take_conf()
		if which == "park":
			downloader = park.mangapark_downloader(
				self.conf['manga_name'],
				self.conf['start_chapter'],
				self.conf['end_chapter'],
				self.conf['manga_location'],
				"default")

		else:
			downloader = reader.mangareader_downloader(
				self.conf['manga_name'],
				self.conf['start_chapter'],
				self.conf['end_chapter'],
				self.conf['manga_location'],
				"aria2c --max-tries=0 --max-file-not-found=20 --lowest-speed-limit=0 --allow-overwrite --connect-timeout=60 -q ")
		downloader.run()

	def fill_in(self,which):
		self.conf['manga_location'] = sys.argv[0]
		self.conf['manga_name']     = sys.argv[1]
		self.conf['start_chapter']  = sys.argv[2]
		self.conf['end_chapter']    = sys.argv[3]
		self.start(which,False)

	def procedure(self):
		if len(sys.argv) > 1:
			sys.argv.remove(sys.argv[0])
			if "-park" == sys.argv[0]:
				if len(sys.argv) == 1:
					self.start("park",True)
				elif len(sys.argv) == 5:
					sys.argv.remove(sys.argv[0])
					self.fill_in("park")
			elif len(sys.argv) == 4:
				self.fill_in("")
			else:
				print "\nUsage: \nstart the script with 4 args: location manga_name start end\nor if you want to use mangapark add the '-park' before the location\nOr directly call the script without args\n"
		else:
			self.start("",True)

if __name__ == "__main__":
	main().procedure()
