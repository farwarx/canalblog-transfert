import os
from cx_Freeze import setup, Executable
import sys

# Need to adapt you PATH
username = "JohnSmith"
PYTHON_INSTALL_DIR  = "C:/Users/" + username + "/AppData/Local/Programs/Python/Python39"

os.environ['TCL_LIBRARY'] = PYTHON_INSTALL_DIR + '/tcl/tcl8.6'
os.environ['TK_LIBRARY'] = PYTHON_INSTALL_DIR + '/tcl/tk8.6'

ico = "ico/icone_v1.ico"
company_name = 'Farwarx'
product_name = 'Canalblog-transferts'
target_name = "Canablog-transferts"

build_exe_options = {
    #packages : ["os","requests","urllib","urllib3","bs4","yaml","importlib","pathlib","time","mimetypes","urllib.parse"],
    'packages' : [],
    'excludes' : [],
    'include_files' : [PYTHON_INSTALL_DIR + "/DLLs/tcl86t.dll", PYTHON_INSTALL_DIR + "/DLLs/tk86t.dll"]
}


bdist_msi_options = {
       'upgrade_code' : '{ef26d731-1f31-4f31-b231-a81502b88d31}',
       'add_to_path': True,
       'initial_target_dir': r'[ProgramFilesFolder]\%s\%s' % (company_name, product_name),
       'install_icon' : ico,
       'target_name' : target_name
}

base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('main.py',
               targetName=target_name,
               base=base,
               shortcutName="Canablog-transferts",
               shortcutDir="DesktopFolder",
               icon=ico)
]

setup(name='Canablog down/up load picture',
      version = '1.0',
      description = 'Download and upload picture on Canalblog plateform',
      author="farwarx",
      options = {
          "build_exe" : build_exe_options,
          "bdist_msi" : bdist_msi_options
      },
      executables = executables)