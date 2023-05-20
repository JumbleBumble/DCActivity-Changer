import time
import customtkinter as ctk
import threading
import os


#Root Setup
root = ctk.CTk()
root.geometry("300x200")
root.title("DC Activity")
root.attributes("-topmost", False)

#//ANCHOR COLORS ---------------------------------------
TopBarFGColor = '#7289da'      
BackFGColor = '#8f72da'        
ButtonFGColor = '#6ebad9'      
ButtonBCColor = '#72a2da'       
ButtonTextColor = 'white'    
ButtonBW = 2


#Configuring Root
root.configure(fg_color=BackFGColor)
root.columnconfigure(0,weight=1)
root.columnconfigure(1,weight=1)
root.rowconfigure(0,weight=1)
root.rowconfigure(1,weight=1)
root.rowconfigure(2,weight=1)
root.rowconfigure(3,weight=1)


#//ANCHOR UTILITY WINDOWS ----------------------------------------
def CloseWindow(self):
    self.withdraw()

class NotificationWindow(ctk.CTkToplevel):
    def __init__(self,text,nclass, *args, **kwargs):
        super().__init__(*args, **kwargs)
        global Scriptentry
        self.anchor = ctk.SE
        if nclass == 'Warning':
            self.title('Warning')
            self.label = ctk.CTkLabel(self,text_color='red', text=text)
        else:
            self.title('Success')
            self.label = ctk.CTkLabel(self,text_color='green', text=text)
        self.label.pack()
        self.okbutton = ctk.CTkButton(self,text='Ok',fg_color="black",hover_color='grey',command = lambda: CloseWindow(self))
        self.okbutton.pack()
        NewLen = len(text) * 5
        NewWidth=100 + NewLen
        self.geometry(f"{NewWidth}x50")
        self.attributes("-topmost", True)
        self.focus_force()
        self.lift()




#//ANCHOR LIB CHECK ----------------------------------------
current_directory = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(current_directory, "lib")
if os.path.isdir(lib_path):
    SDKPath = os.path.join(lib_path, "discord_game_sdk.dll")
    if os.path.exists(SDKPath):
         import discordsdk as dsdk
    else:
        NotificationWindow(text=f'MISSING discord_game_sdk.dll ERROR',nclass='Warning')
else:
    NotificationWindow(text=f'MISSING LIB FOLDER ERROR',nclass='Warning')




#//ANCHOR ICON CHECK ----------------------------------------
icon_path = os.path.join(current_directory, "discordico.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)




#//ANCHOR ActivitySet ----------------------------------------
KillThread = False
def ActivitySet():
    global dsdk
    global KillThread

    try:
        if dsdk:
            dsdkcheck = True
    except Exception as e:
        NotificationWindow(text=f'IMPORT ERROR: {e} (Make sure you have the lib folder with the discordSDK in same directory)',nclass='Warning')

    if 'dsdkcheck' in locals():
        ActiveState = Activityentry.get()
        ActiveID = IDentry.get()
        try:
            app = dsdk.Discord(int(ActiveID), dsdk.CreateFlags.default)
            activity_manager = app.get_activity_manager()
            activity = dsdk.Activity()
            activity.state = ActiveState
        except Exception as e:
            NotificationWindow(text=f'ACTIVITY ERROR: {e} (Make sure your using a valid application ID)',nclass='Warning')

        def callback(result):
            if result == dsdk.Result.ok:
                NotificationWindow(text=f'Successfully set the activity!',nclass='W')
            else:
                NotificationWindow(text=f'ERROR: {result} (Make sure your using a valid application ID)',nclass='Warning')
                raise Exception(result)

        activity_manager.update_activity(activity, callback)
        KillThread = True

        try:
            while 1:
                time.sleep(1/10)
                app.run_callbacks()
                if not KillThread:
                    return
        except Exception as e:
            NotificationWindow(text=f'CALLBACK ERROR: {e} (Make sure your using a valid application ID)',nclass='Warning')
    else:
        NotificationWindow(text=f'ERROR: DISCORDSDK NOT IMPORTED! (Make sure you have the lib folder with the discordSDK in same directory)',nclass='Warning')



def ActivityThread():
    global KillThread
    if KillThread:
        KillThread = False
    ActiveThread = threading.Thread(target=ActivitySet)
    ActiveThread.start()




#//ANCHOR INTERFACE ----------------------------------------

#Is basically the topbar color of the GUI that holds some stuff
MainFrame = ctk.CTkFrame(root,height=50,width=300,fg_color=TopBarFGColor,bg_color=TopBarFGColor,border_color='#72a2da',border_width=2)
root.configure(border_color='#72a2da')
root.configure(border_width=12)
MainFrame.grid(column = 0, row = 0,columnspan=2,sticky="nsew")
MainFrame.columnconfigure(0,weight=1)
MainFrame.rowconfigure(0,weight=1)
MainFrame.rowconfigure(1,weight=1)

#Top Title
LuawlLabelStyle = ('Trebuchet MS',17)
Luawllabel = ctk.CTkLabel(MainFrame,font=LuawlLabelStyle, text="Discord Activity Changer", fg_color="transparent")
Luawllabel.grid(column = 0, row = 0,pady=3)

#Entry box for Application ID
IDentry = ctk.CTkEntry(root,width=310, placeholder_text="Application ID")
IDentry.grid(column = 0, row = 1,columnspan=2,pady=5,sticky="nsew")

#Entry box for Activity Description
Activityentry = ctk.CTkEntry(root,width=310, placeholder_text="Activity Description")
Activityentry.grid(column = 0, row = 2,columnspan=2,pady=5,sticky="nsew")

#Set Activity button
Activitybutton = ctk.CTkButton(root,height=70, text="Set Activity",text_color=ButtonTextColor,fg_color=ButtonFGColor,border_color=ButtonBCColor,border_width=ButtonBW,hover_color='#5b70be', command = ActivityThread)
Activitybutton.grid(column = 0, row = 3,columnspan = 2,pady=15,padx=15,sticky="nsew")


ctk.set_appearance_mode("dark")
root.mainloop()

#Makes sure to kill the thread if the mainloop is broken (Basically cleanup for when they exit the app)
KillThread = False