import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path
from functions import Canalblog
import requests
import time

class Main(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(Login)
        #self.switch_frame(Download)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class Login(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master.title("Canalblog Custom App - " + __class__.__name__ + " - by Farwarx")
        global s
        s = requests.Session()
        #self.master.geometry("320x240")

        self.login_frame = tk.Frame(self, width=400, height=500, bg="red")
        self.login_frame.pack(side="top", expand=True)
        self.login_title = tk.Label(self.login_frame, text="Canalblog Custom App")
        self.login_title.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        self.login_label = tk.Label(self.login_frame, text="Login")
        self.login_label.grid(row=1, column=0, padx=10, pady=10)
        self.login_entry = tk.Entry(self.login_frame, width=15)
        self.login_entry.grid(row=1, column=1, padx=10, pady=10)

        self.pass_label = tk.Label(self.login_frame, text="Password")
        self.pass_label.grid(row=2, column=0, padx=10, pady=10)    
        self.pass_entry = tk.Entry(self.login_frame, width=15, show="*")
        self.pass_entry.grid(row=2, column=1, padx=10, pady=10)
  
        self.blog_label = tk.Label(self.login_frame, text="Blogname")
        self.blog_label.grid(row=3, column=0, padx=10, pady=10)    
        self.blog_entry = tk.Entry(self.login_frame, width=15)
        self.blog_entry.grid(row=3, column=1, padx=10, pady=10)

        self.remember = tk.BooleanVar()
        self.remember.set(False)
        self.login_remember_button = tk.Checkbutton(self.login_frame, text="Remember me", variable=self.remember)
        self.login_remember_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        self.login_connexion_button = tk.Button(self.login_frame, text="Connexion", command=lambda: self.login_blog(master))
        self.login_connexion_button.grid(row=5, column=0, columnspan=3, padx=10, pady=10)
        
        self.quit_button = tk.Button(self.login_frame, text="Quit", command=self.quit)
        self.quit_button.grid(row=5, column=3, padx=10, pady=10)

        self.conf = Canalblog.conf_file()
        if type(self.conf) is dict:
            self.login_entry.insert(0, self.conf["cca"]["login"])
            self.pass_entry.insert(0, self.conf["cca"]["pass"])
            self.blog_entry.insert(0, self.conf["cca"]["blog"])

    def login_blog(self, master):
        global shared_url_dl, shared_url_source, shared_blog_name
        login = self.login_entry.get()
        passwd = self.pass_entry.get()
        blog = self.blog_entry.get()
        if self.remember.get():
            Canalblog.gen_conf_file(login,passwd,blog)
        shared_blog_name = blog
        url_blog = "http://" + blog + ".canalblog.com"
        shared_url_dl = url_blog
        url_source = "https://www.canalblog.com"
        url_login = url_source + "/cf/security/SessionController.cfc?method=login"
        shared_url_source = url_source
        if not login or not passwd or not blog:
            tk.messagebox.showerror ("Connexion - login, password or blog missing", "Login or password or blog missing")
        elif login and passwd and blog:
            payload = {'memberid':login,'password':passwd,'rememberme':1,'returnTo':url_blog,'erroron':'blogprotected','errorReturnTo':'/cf/login.cfm'}
            s_login = s.post(url_login, data=payload)
            if s_login.text.find('login.cfm') == -1:
                tk.messagebox.showinfo("Connexion - Successful", "Connexion successful!")
                master.switch_frame(Choice)
            else:
                tk.messagebox.showerror("Connexion - Failed", "Connexion failed! login or password incorrect")
        else:
            tk.messagebox.showerror("Connexion - Failed", "???????")

class Choice(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master.title("Canalblog Custom App - " + __class__.__name__ + " - by Farwarx")
        #self.master.geometry("320x240")

        self.choice_frame = tk.Frame(self, width=400, height=500, bg="yellow")
        self.choice_frame.pack(side="top", expand=True)
        self.choice_label = tk.Label(self.choice_frame, text="Download or Upload picture")
        self.choice_label.grid(row=0, columnspan=2, padx=10, pady=10)
        self.download_button = tk.Button(self.choice_frame, text="Download", command=lambda: master.switch_frame(Download))
        self.download_button.grid(row=1, column=0, padx=10, pady=10)
        self.upload_button = tk.Button(self.choice_frame, text="Upload", command=lambda: master.switch_frame(Upload))
        self.upload_button.grid(row=1, column=1, padx=10, pady=10)
        self.quit_button = tk.Button(self.choice_frame, text="Quit", command=self.quit)
        self.quit_button.grid(row=2, column=2, padx=10, pady=10)

class Download(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master.title("Canalblog Custom App - " + __class__.__name__ + " - by Farwarx")

        self.pc_dir = str(Path.home())
        #self.master.geometry("320x240")

        self.main_frame = tk.Frame(self, width=400, height=500, bg="green")
        self.main_frame.pack(side="top", expand=True)
        self.main_label = tk.Label(self.main_frame, text="Download")
        self.main_label.grid(row=0, columnspan=4, padx=10, pady=10)


        self.album_label = tk.Label(self.main_frame, text="Choose one album")
        self.album_label.grid(row=1, column=0, padx=10, pady=10)
        
        self.album_listing()
        self.album_combo = ttk.Combobox(self.main_frame, values=self.album_list, state='readonly', width=self.album_list_width)
        self.album_combo.current(0)
        self.album_combo.grid(row=1, column=1, columnspan=3, padx=10, pady=10)

        self.dldir_label = tk.Label(self.main_frame, text="Choose dir to download picture")
        self.dldir_label.grid(row=2, column=0, padx=10, pady=10)
        self.dldir_button = tk.Button(self.main_frame, text="Browse dir", command=self.browse_button)
        self.dldir_button.grid(row=2, column=1, padx=10, pady=10)
        self.dldir_label2 = tk.Label(self.main_frame, text=self.pc_dir)
        self.dldir_label2.grid(row=2, column=2, columnspan=2, padx=10, pady=10)

        self.dl_button = tk.Button(self.main_frame, text="Download", command=lambda : self.launch())
        self.dl_button.grid(row=4, column=0, padx=10, pady=10)

        self.return_button = tk.Button(self.main_frame, text="Return", command=lambda : master.switch_frame(Choice))
        self.return_button.grid(row=4, column=1, padx=10, pady=10)
        self.quit_button = tk.Button(self.main_frame, text="Quit", command=self.quit)
        self.quit_button.grid(row=4, column=4, padx=10, pady=10)

    def launch(self):
        self.album = self.album_combo.get()
        try:
            self.album # TODO - test non fonctionnel
            self.pc_dir
        except:
            print("TOTO: except")
        else:
            #print("Download: " + self.album + " to: " + self.pc_dir)
            if tk.messagebox.askyesno("Download...", "Download album \"" + self.album + "\" in dir \"" + self.pc_dir + "\""):
                #tk.messagebox.showinfo("Download in progress", "In progress...")
                self.dl_popup = tk.Toplevel()
                self.dl_label = tk.Label(self.dl_popup, text="Files being downloaded")
                self.progress=0
                self.progress_var = tk.DoubleVar()
                self.dl_progress = ttk.Progressbar(self.dl_popup, variable=self.progress_var, maximum=100)
                self.dl_label.grid(row=0,column=0)
                self.dl_progress.grid(row=1, column=0, padx=10, pady=10)
                self.dl_popup.pack_slaves()
                self.dl_picture()
                self.dl_popup.destroy()
                tk.messagebox.showinfo("Download successful", "Download successful")
                self.dl_button['text'] = "Downloaded"
            else:
                tk.messagebox.showinfo("Download aborted", "Download aborted")

    def browse_button(self):
        self.pc_dir = tk.filedialog.askdirectory()
        self.dldir_label2['text'] = self.pc_dir

    def album_listing(self):
        album_list = []
        album_page = s.get(shared_url_dl)
        self.album_list_full = Canalblog.dl_album_list(album_page.text)
        #print(self.album_list_full)
        for album in self.album_list_full:
             album_list.append(album["title"])
        self.album_list = album_list
        try:
            self.album_list_width = max(len(s) for s in self.album_list)
        except:
            self.album_list_width = 20

    def dl_picture(self):
        #print("dl_picture function")
        try:
            pic_numb1 = self.album.split(":")[1].replace(" photos","").replace(" ","")
            pic_numb = range(int(pic_numb1))
        
            url_blog = next(filter(lambda blog: blog['title'] == self.album, self.album_list_full))['href']
            self.album_dir = url_blog.split("/")[4]
            print("url_blog: " + url_blog + " ; album_dir: " + self.album_dir)
            if Canalblog.create_arbo(self.pc_dir + "/" + self.album_dir) == True:
                r2 = s.get(url_blog)
                pic_list = Canalblog.dl_picture_list(r2.text)
                self.progress_step = float(100.0/len(pic_numb))
                for element in pic_list:
                    self.dl_popup.update()
                    pic = s.get(element["src"])
                    pic_file = self.pc_dir + "/" + self.album_dir + "/" + element['filename']
                    print(element["src"] + " ; " + pic_file)
                    open(pic_file, 'wb').write(pic.content)
                    self.progress += self.progress_step
                    self.progress_var.set(self.progress)
        except:
            tk.messagebox.showerror("Fatal error", "Fatal error - Download/dl_picture")

class Upload(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master.title("Canalblog Custom App - " + __class__.__name__ + " - by Farwarx")

        self.pc_dir = str(Path.home())
        #self.master.geometry("320x240")

        self.main_frame = tk.Frame(self, width=400, height=500, bg="green")
        self.main_frame.pack(side="top", expand=True)
        self.main_label = tk.Label(self.main_frame, text="Upload")
        self.main_label.grid(row=0, columnspan=4, padx=10, pady=10)


        self.album_label = tk.Label(self.main_frame, text="Choose one album")
        self.album_label.grid(row=1, column=0, padx=10, pady=10)
        
        self.album_listing()
        self.album_combo = ttk.Combobox(self.main_frame, values=self.album_list, state='readonly', width=self.album_list_width)
        self.album_combo.current(0)
        self.album_combo.grid(row=1, column=1, columnspan=3, padx=10, pady=10)

        self.updir_label = tk.Label(self.main_frame, text="Choose dir containing picture to upload")
        self.updir_label.grid(row=2, column=0, padx=10, pady=10)
        self.updir_button = tk.Button(self.main_frame, text="Browse dir", command=self.browse_button)
        self.updir_button.grid(row=2, column=1, padx=10, pady=10)
        self.updir_label2 = tk.Label(self.main_frame, text=self.pc_dir)
        self.updir_label2.grid(row=2, column=2, columnspan=2, padx=10, pady=10)

        self.up_button = tk.Button(self.main_frame, text="Upload", command=lambda : self.launch())
        self.up_button.grid(row=4, column=0, padx=10, pady=10)
        self.return_button = tk.Button(self.main_frame, text="Return", command=lambda : master.switch_frame(Choice))
        self.return_button.grid(row=4, column=1, padx=10, pady=10)
        self.quit_button = tk.Button(self.main_frame, text="Quit", command=self.quit)
        self.quit_button.grid(row=4, column=4, padx=10, pady=10)

    def launch(self):
        self.album = self.album_combo.get()
        try:
            self.album # TODO - test non fonctionnel
            self.pc_dir
        except:
            print("TOTO: except")
        else:
            print("Upload: " + self.pc_dir + "to: " + self.album)
            if tk.messagebox.askyesno("Upload...", "Upload picture from \"" + self.pc_dir + "\" to album \""):
                self.up_popup = tk.Toplevel()
                self.up_label = tk.Label(self.up_popup, text="Files being uploaded")
                self.progress=0
                self.progress_var = tk.DoubleVar()
                self.up_progress = ttk.Progressbar(self.up_popup, variable=self.progress_var, maximum=100)
                self.up_label.grid(row=0,column=0)
                self.up_progress.grid(row=1, column=0, padx=10, pady=10)
                self.up_popup.pack_slaves()
                self.up_picture()
                self.up_popup.destroy()
                tk.messagebox.showinfo("Upload successful", "Upload successful")
                self.up_button['text'] = "Uploaded"
            else:
                tk.messagebox.showinfo("Uploaded aborted", "Uploaded aborted")

    def browse_button(self):
        self.pc_dir = tk.filedialog.askdirectory()
        self.updir_label2['text'] = self.pc_dir

    def album_listing(self):
        # search blog id
        url_blog_list = shared_url_source + "/cf/my/"
        blog_page = s.get(url_blog_list)
        blist = Canalblog.blog_list(shared_url_source, blog_page.text)
        self.bid = next(filter(lambda x: x['subdomain'] == shared_blog_name, blist))['id']
        # search album from the selected blog
        url_up = url_blog_list + "/?nav=blog.medialib&bid=" + self.bid
        album_list = []
        album_page = s.get(url_up)
        self.album_list_full = Canalblog.up_album_list(album_page.text)
        print(self.album_list_full)
        for album in self.album_list_full:
             album_list.append(album["name"] + " " + album["date"])
        self.album_list = album_list
        try:
            self.album_list_width = max(len(s) for s in self.album_list)
        except:
            self.album_list_width = 20

    def up_picture(self):
        try:
            self.album = self.album.split(" (")[0]
            up_list = Canalblog.up_picture_list(self.pc_dir)
            #print(up_list)
            pic_numb1 = len(up_list)
            pic_numb = range(int(pic_numb1))
            #print(pic_numb1)
            url_up_final = shared_url_source + "/cf/my/?nav=blog.upload.picture&bid=" + self.bid + "&pane=1&uploaderver=0"
            album_id = next(filter(lambda x: x['name'] == self.album, self.album_list_full))['aid']

            self.progress_step = float(100.0/len(pic_numb))
            for filename in up_list:
                self.up_popup.update()
                #print(filename)
                upload_post = Canalblog.upload_gen_post(filename, album_id)
                upload_file = Canalblog.upload_gen_file(self.pc_dir,filename)
                s.post(url_up_final, data=upload_post, files=upload_file)
                time.sleep(1)
                self.progress += self.progress_step
                self.progress_var.set(self.progress)
        except:
            tk.messagebox.showerror("Fatal error", "Fatal error - Upload/up_picture")


if __name__ == "__main__":
    app = Main()
    app.mainloop()