import mechanize, re, sys, os, time

class mangapark_downloader(object):
    def __init__(self,manga_name,chapter,end_chapter,manga_location):
        self.manga_location = manga_location
        self.manga_name     = manga_name
        self.chapter        = chapter
        self.end_chapter    = end_chapter
        self.current_image  = "000"
        self.img            = ""
        self.imgs           = []
        self.chapters       = []
        self.br             = mechanize.Browser()

    def increase_current(self):
        self.current_image = str(int(self.current_image)+1)
        if len(self.current_image) == 1:
            self.current_image = "00"+self.current_image
        elif len(self.current_image) == 2:
            self.current_image = "0"+self.current_image

    def increase_chapter(self):
        self.chapter = str(int(self.chapter)+1)

    def scrap_page(self):
        for a in self.br.links():
            if a.text=='All':
                tmp = a.url.split(self.manga_name)
                if not "-" in tmp[1] and "+" not in tmp[1]:
                    self.chapters.append("http://www.mangapark.com"+a.url)
        self.chapters.reverse()
        if len(self.chapters)==0:
            print "No manga"
            sys.exit(1)

    def scrap_images(self):
        images = re.findall("<em><a target=\"_blank\" (.*)</a></em>",self.br.response().read())
        for img in images:
            img = re.findall("href=\"(.*)\" title",img)
            self.imgs.append(img[0])

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

    def  download_each_imgs(self):
        self.manage_chapters()
        for an_img in self.imgs:
            self.img = str(an_img)
            not_saved_yet = True
            while not_saved_yet:
                try:
                    self.download_image()
                    not_saved_yet = False
                except Exception,e:
                    time.sleep(2)
                    print e
            self.increase_current()


    def download_image(self):
        image_response = self.br.open_novisit(self.img)
        image = image_response.read()
        self.manage_chapters()
        writing = open(self.current_image+'.jpg', 'wb')
        writing.write(image)
        writing.close()
        print "[*] Image saved to "+ os.getcwd() + "/"+self.current_image+".jpg"

    def open_new_chapter(self,chapt):
        try:
            self.br.open(str(self.chapters[chapt]))
        except Exception,e:
            print e
            time.sleep(2)
            self.open_new_chapter(chapt)

    def start_downloading(self):
        if int(self.end_chapter) > len(self.chapters):
            self.end_chapter = str(len(self.chapters)-1)
        for chapt in xrange(int(self.chapter)-1,int(self.end_chapter)+1):
            self.open_new_chapter(chapt)
            self.scrap_images()
            self.download_each_imgs()

            self.current_image = "000"
            self.imgs           = []
            self.increase_chapter()

    def open_first_page(self):
        try:
            self.br.open("http://www.mangapark.com/manga/"+self.manga_name+"/")
        except:
            time.sleep(2)
            self.open_first_page()

    def run(self):
        self.open_first_page()
        self.scrap_page()
        self.start_downloading()
        print "[*] Finished all the downloads\nEnjoy You Reading!"
