import platform
import os
import shutil
import enum
import subprocess

pt = platform.platform()

linux = "Linux"
windows = "Windows"

class Action(enum.Enum):
    Overwrite = 1
    Append = 2
    Skip = 3


current_platform = windows if pt.startswith(windows) else linux

locations = {
    windows: [
        {
            "name": "powershell profile",
            "local_path": "ps_profile",
            "remote_path": r"%USERPROFILE%\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1",
            "type": "file",
            "action": Action.Overwrite 
        },
        {
            "name": "vs code",
            "local_path": "code",
            "remote_path": r"%APPDATA%\Code\User",
            "type": "directory",
            "action": Action.Overwrite 
        },
        {
            "name": "vim",
            "local_path": "vimrc",
            "remote_path": r"%USERPROFILE%\.vimrc",
            "type": "file",
            "action": Action.Overwrite
        }
    ],
    linux: [
        {
            "name": "bashrc",
            "local_path": "bashrc",
            "remote_path": "$HOME/.bashrc",
            "type": "file",
            "action": Action.Append
        },
        {
            "name": "vs code",
            "local_path": "code",
            "remote_path": r"$HOME/.config/Code/User",
            "type": "directory",
            "action": Action.Overwrite
        },
        {
            "name": "vim",
            "local_path": "vimrc",
            "remote_path": "$HOME/.vimrc",
            "type": "file",
            "action": Action.Overwrite
        }
    ]
}

def _replace_home(str: str):
    home = os.path.expanduser("~")
    local_appdata = os.getenv('LOCALAPPDATA')
    if current_platform == linux:
        return str.replace("$HOME", home)
    else:
        return  str.replace("%USERPROFILE%", home).replace("%APPDATA%", local_appdata)

def handle_file(file_obj):
    rp = _replace_home(file_obj["remote_path"])
    # implement skipping
    os.makedirs(os.path.dirname(rp), exist_ok=True)
    
    if file_obj["action"] == Action.Overwrite:
        shutil.copyfile(file_obj["local_path"], rp)
    elif file_obj["action"] == Action.Append:
        with open(file_obj["local_path"], "r") as handler:
            data = handler.read()
        
        with open(rp, "a") as handler:
            handler.write(f"\n\n{data}")
    
def handle_folder(folder_obj):
    rp = _replace_home(folder_obj["remote_path"])
    lp = folder_obj["local_path"]
    # implement skipping
    os.makedirs(rp, exist_ok=True)
    
    if folder_obj["action"] == Action.Overwrite:
        for file in os.listdir(lp):
            shutil.copyfile(os.path.join(lp, file), os.path.join(rp, file))

    elif folder_obj["action"] == Action.Append:
        for file in os.listdir(lp):
            with open(os.path.join(lp, file), "r") as handler:
                data = handler.read()
            
            with open(os.path.join(rp, file), "a") as handler:
                handler.write(f"\n\n{data}")
        

if __name__ == "__main__":
    print("Detecting operating System")
    print(current_platform)
    print()

    for dt in locations[current_platform]:
        print(f"Trying to write {dt['name']}")
        if dt["type"] == "file":
            handle_file(dt)
        elif dt["type"] == "directory":
            handle_folder(dt)
        print(f"{dt['name']} written")
        print()

    print("Finished successful")
    
    if current_platform == linux:
        subprocess.Popen(["source", "~/.bashrc"])