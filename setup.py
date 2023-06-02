import cx_Freeze
import os


os.environ["TCL_LIBRARY"] = r"C:\Users\Hosein\AppData\Local\Programs\Python\Python38\tcl\tcl8.6"
os.environ["TK_LIBRARY"] = r"C:\Users\Hosein\AppData\Local\Programs\Python\Python38\tcl\tk8.6"

cx_Freeze.setup(name="Project1",
                options={
                    "build_exe":{
                        "packages":["project1_console_app"
                                    ,"re"
                                    ,"requests"
                                    ,"tkinter"
                                    ]
                                }
                        },
                description="Test deployment for easy access.",
                executables=[cx_Freeze.Executable("project1_gui_app.py" ,base="Win32GUI")]
                )
