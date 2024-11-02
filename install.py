import os
import os.path
import platform
import shutil
import enum
import json
import subprocess

pt = platform.platform()

LINUX = "Linux"
WINDOWS = "Windows"
LOCAL_CONFIG_FOLDER = "dotfiles"

class Action(enum.Enum):
    Overwrite = 1
    Append = 2
    Skip = 3
    BASHRC = 4


current_platform = WINDOWS if pt.startswith(WINDOWS) else LINUX

class Config:
    def __init__(self, name, local_path, remote_path, f_type, action) -> None:
        self.name = name
        self.local_path = os.path.join(LOCAL_CONFIG_FOLDER, local_path)
        self.remote_path = remote_path
        self.f_type = f_type
        self.action = Action[action]

    def handle_file(self):
        # implement skipping
        file_path = os.path.expanduser(os.path.expandvars(self.remote_path))
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        if self.action == Action.Overwrite:
            shutil.copyfile(self.local_path, file_path)
        elif self.action == Action.Append:
            with open(self.local_path, "r") as handler:
                data = handler.read()
            
            with open(file_path, "a") as handler:
                handler.write(f"\n\n{data}")
        elif self.action == Action.BASHRC:
            shutil.copyfile(self.local_path, file_path)
            str = "[ -f $HOME/.custom-bashrc ] && . $HOME/.custom-bashrc"
            bash_rc_path = os.path.expanduser("~/.bashrc")
            with open(bash_rc_path, "r") as file:
                data = file.read().split("\n")
            if not any([x.strip() == str for x in data]):
                with open(file_path, "a") as handler:
                    handler.write(f"\n\n{str}")

    def handle_folder(self):
        folder_path = os.path.expanduser(os.path.expandvars(self.remote_path))
        lp = self.local_path

        # implement skipping
        os.makedirs(folder_path, exist_ok=True)
        
        if self.action == Action.Overwrite:
            for file in os.listdir(lp):
                shutil.copyfile(os.path.join(lp, file), os.path.join(folder_path, file))

        elif self.action == Action.Append:
            for file in os.listdir(lp):
                with open(os.path.join(lp, file), "r") as handler:
                    data = handler.read()
                
                with open(os.path.join(folder_path, file), "a") as handler:
                    handler.write(f"\n\n{data}")
    
    def run(self):
        if self.f_type == "directory":
            self.handle_folder()
        else:
            self.handle_file()
            
        print(f"Finished writing {self.name}")

if __name__ == "__main__":
    print("Detecting operating System")
    print(current_platform)
    print()

    file = current_platform.lower() + "_loc.json"
    with open(file, "r") as handler:
        json_data = json.load(handler)
    configs = [Config(**cfg) for cfg in json_data]
    
    [cfg.run() for cfg in configs]

    # for dt in locations[current_platform]:
    #     print(f"Trying to write {dt['name']}")
    #     if dt["type"] == "file":
    #         handle_file(dt)
    #     elif dt["type"] == "directory":
    #         handle_folder(dt)
    #     print(f"{dt['name']} written")
    #     print()

    print("Finished successful")
    