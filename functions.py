import os
from bs4 import BeautifulSoup
import re
import mimetypes
import yaml
from urllib.parse import urlparse, parse_qs
from os.path import splitext, basename, isfile
from pathlib import Path

class Canalblog:
    def __init__(self):
        self.data = []

    def create_arbo(dir):
        try:
            os.mkdir(dir)
            return True
        except FileExistsError:
            #print("Dir :", dir, "already exist")
            return True
        except:
            return False

    def gen_conf_file(login,passwd,blog):
        try:
            config = {'cca':{'login':login, 'pass':passwd,'blog':blog}}
            Canalblog.write_conf_file(config)
            return True
        except:
            return False

    def write_conf_file(conf):
        try:
            with open(config_file, 'w') as yaml_file:
                yaml.dump(conf, yaml_file, default_flow_style=False)
            return True
        except:
            return False

    def conf_file():
        dir = str(Path.home()) + "/.cca"
        #print(dir)
        Canalblog.create_arbo(dir)
        file = "config.yaml"
        global config_file
        config_file = dir + "/" + file
        if not os.path.isfile(config_file):
            login = ""
            passwd = ""
            blog = ""
            Canalblog.gen_conf_file(login,passwd,blog)
        try:
            with open(config_file, 'r') as conf_file:
                return yaml.load(conf_file, Loader=yaml.FullLoader)
        except:
            return False

    def dl_album_list(input):
        llist = []
        bs = BeautifulSoup(input, 'html.parser')
        albumlist = bs.find("ul", {'class':'albumlist'})
        bs2 = BeautifulSoup(str(albumlist), "html.parser")
        for s in bs2.find_all("a", href=True):
            if s.has_attr('title'):
                llist.append({'href':s['href'], 'title':s['title']})
        return llist

    def blog_list(url_source, input):
        blist = []
        bs = BeautifulSoup(input, 'html.parser')
        for div in bs.find_all('div', {'class':'wbloginfohead'}):
            url2 = div.find('a', {'class': 'wsettingsbut'})['href']
            url = url_source + "/" + url2
            bid = parse_qs(urlparse(url).query)["bid"][0]
            btitle = div.find('div', {'class': 'wblogtitle'}).string
            bsubdomain_url = div.find('a', {'title': btitle})['href']
            bsubdomain = urlparse(bsubdomain_url).netloc.split(".")[0]
            blist.append({'title':btitle, 'id':bid, 'subdomain':bsubdomain})
        return blist

    def up_album_list(input):
        flist = []
        bs = BeautifulSoup(input, 'html.parser')
        for div in bs.find_all('div', {'class':'box'}):
            album_create = Canalblog.export_create(div.find_all("i"))
            album_create = str(album_create)
            album_id = Canalblog.export_id(div.find_all)
            album_id = str(album_id).replace("[","").replace("]","").replace("'","")
            album_name = Canalblog.export_name(div.get_text)
            album_name = str(album_name).replace("\xa0","")
            if album_create != 'None':        
                flist.append({'date':album_create, 'aid':album_id, 'name':album_name[:-1]})
        return flist

    def dl_picture_list(page):
        llist = []
        bs = BeautifulSoup(page, "html.parser")
        for s in bs.find("div", {'id':'album-content'}).find_all('img'):
            if s.has_attr('alt'):
                src = s['src'].replace('_q.','_o.')
                ext = splitext(basename(urlparse(s['src']).path))[1]
                filename = s['alt'].replace(' ','-') + ext
                llist.append({'src':src, 'filename':filename})
        return llist

    def export_create(text):
        for date in text:
            return date.text

    def export_id(text):
        elist = []
        for link in text('a', href=True):
            href = link['href']
            if "aid=" in href:
                args = dict(x.split('=') for x in href.split('&'))
                elist.append(str(args['aid']))
        return sorted(set(elist))

    def export_name(text):
        for line in str(text).splitlines():
            if "<strong>Nom de l'album" in line:
                sub1 = re.sub("^.*</strong> ", "", line)
                return re.sub("<i>.*$", "", sub1)

    def up_picture_list(path):
        llist = []
        for img in os.listdir(path):
            if img.lower().endswith(".jpg"):
                llist.append(img)
            if img.lower().endswith(".png"):
                llist.append(img)
            if img.lower().endswith(".gif"):
                llist.append(img)
        return llist

    def upload_gen_post(file_name,album_id):
        return {'albumDestId':album_id,
            'pane':1,
            'mediaAlbumPos':0,
            'dialogueType':2,
            'filename':file_name,
            'sendFile':'true',
            'close':'true'}

    def upload_gen_file(file_path,file_name):
        file_mime = mimetypes.guess_type(file_path + "/" + file_name)[0]
        file_content = open(file_path + "/" + file_name, "rb")
        return {'file': (file_name, file_content, file_mime)}
