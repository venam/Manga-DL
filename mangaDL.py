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
import re, mechanize, os, readline,time

#---complete the path---#
class Completer(object):
    def _listdir(self, root):
        res = []
        for name in os.listdir(root):
            path = os.path.join(root, name)
            if os.path.isdir(path):
                name += os.sep
            res.append(name)
        return res
    def _complete_path(self, path=None):
        if not path:
            return self._listdir('.')
        dirname, rest = os.path.split(path)
        tmp = dirname if dirname else '.'
        res = [os.path.join(dirname, p)
                for p in self._listdir(tmp) if p.startswith(rest)]
        if len(res) > 1 or not os.path.exists(path):
            return res
        if os.path.isdir(path):
            return [os.path.join(path, p) for p in self._listdir(path)]
        return [path + '']
    def complete_extra(self, args):
        return self._complete_path(args[-1])
    def complete(self, text, state):
        buffer = readline.get_line_buffer()
        line = readline.get_line_buffer().split()
        cmd = line[0].strip()
        impl = getattr(self, 'complete_%s' % "extra")
        args = line[0:]
        if args:
            return (impl(args) + [None])[state]
        return [cmd + ''][state]
        return results[state]


class mangareader_downloader(object):
    def __init__(self,manga_name,chapter,end_chapter,manga_location):
        self.manga_location = manga_location
        self.manga_name     = manga_name
        self.chapter        = chapter
        self.end_chapter    = end_chapter
        self.flag           = False
        self.current_image  = "000"
        self.img            = ""
        self.next_link      = ""
        self.current_page   = "http://www.mangareader.net/"+self.manga_name+"/"+self.chapter+"/"
        self.next_regex     = "<span class=\"next\"><a href=\"(.*)\">Next</a></span>"
        self.br             = mechanize.Browser()

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
        if "is not published yet. Once" in self.br.response().read() or self.chapter == str(int(self.end_chapter)+1):
            return True
        return False

    def go_to_next_page(self):
        if not self.check_chapter_end():
            self.increase_current()
        else:
            self.increase_chapter()
            self.current_image = "00"
        self.current_page = self.next_link

    def scrap_page(self):
        self.next_link = re.findall(self.next_regex ,self.br.response().read())[0]
        self.img       = re.findall("<a href=\""+self.next_link+"\"><img id=\"img\" (.*)\" name=\"img\" />",self.br.response().read())[0]
        self.img       = re.findall("src=\"(.*)\" alt",self.img)[0]
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
        image_response = self.br.open_novisit(self.img)
        image = image_response.read()
        self.manage_chapters()
        writing = open(self.current_image+'.jpg', 'wb')
        writing.write(image)
        writing.close()
        print "[*] Image saved to "+ os.getcwd() + "/"+self.current_image+".jpg"

    def start_downloading(self):
        try:
            self.br.open(self.current_page)
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
        print "[*] Finished all the downloads\nEnjoy You Reading!"

#---start completion---#
comp = Completer()
readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab:complete")
readline.set_completer(comp.complete)
manga_location = raw_input("Enter the mangas location -> ")
manga_name     = raw_input("Enter the manga name -> ")
start_chapter  = raw_input("Enter the manga start chapter -> ")
end_chapter    = raw_input("Enter the manga end chapter -> ")
downloader = mangareader_downloader(manga_name,start_chapter,end_chapter,manga_location)
downloader.run()
