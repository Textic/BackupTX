import os
import shutil
import msvcrt

def GetLastDir(path):
    LastDir = os.path.basename(os.path.normpath(path))
    return LastDir

def FixDir(path): # Fix dir format
    if path.endswith('\n'):
        path = path[:-1]
    if path[-1:] != '\\':
        path = path + '\\'
    return path

def RemoveDir(path): # Remove backup dir
    if os.path.exists(path):
        try:
            shutil.rmtree(path) # Remove dir
            return
        except:
            pass
        try:
            os.remove(path) # Remove file
            return
        except:
            pass

def ShowList(dirr): # Show list of backup files
    l = 1
    for i in dirr:
        print(f'{l}. Status: {dirr[i].get("status")}\n   Name: {dirr[i].get("name")}\n   Dir: {dirr[i].get("path")}\n')
        l += 1

def GetRestoreList(opt): # Get list of backup files
    if opt == 1:
        if os.path.exists('BACKUP.zip'): # check if backup.zip exists
            shutil.unpack_archive('BACKUP.zip', 'backup') # unpacking backup.zip
            with open(FixDir(backup_path) + 'locations.txt', "r") as f: # Read locations.txt
                for line in f:
                    y, k = FixDir(line).split(';')
                    dirr[y] = {
                        'name': y,
                        'path': k,
                        'status': True
                    }
            return dirr
        else:
            return False
    elif opt == 2:
        if os.path.exists('dir.txt'): # check if dir.txt exists
            for path in os.listdir(dir_path): # Get all files dir from dir.txt and save in dirr dict
                if path == 'dir.txt':
                    with open(path) as f:
                        for line in f:
                            if not line[:2].lower() in AllDiskLetters:
                                continue
                            dirr[GetLastDir(FixDir(line))] = {
                                'name': GetLastDir(FixDir(line)),
                                'path': FixDir(line),
                                'status': True
                            }
            return dirr
        else:
            return False

def Press():
    print('\nPress any key to continue...')
    msvcrt.getch()

AllDiskLetters = ["a:", "b:", "c:", "d:", "e:", "f:", "g:", "h:", "i:", "j:", "k:", "l:", "m:", "n:", "o:", "p:", "q:", "r:", "s:", "t:", "u:", "v:", "w:", "x:", "y:", "z:"]
dirr = {}
dir_path = os.path.dirname(__file__)
backup_path = os.path.join(dir_path, 'backup') # Create backup folder dir variable
menu = 1
opt = 0
dirr = GetRestoreList(2)

while menu != 0:
    os.system('cls')
    opt = int(input('1. Backup\n2. Restore\n3. Show\Edit List\n4. Refresh List\n5. Exit\n\nSelect option: '))
    os.system('cls')
    if opt == 1: # Backup
        RemoveDir('BACKUP.zip')
        RemoveDir('backup')
        for i in dirr: # This loop create all backups from dir.txt
            if dirr[i]['status'] == True:
                backdir = ''
                backdir = os.path.join(backup_path, dirr[i].get('name'))
                shutil.copytree(dirr[i].get('path'), backdir)
                print(f'Backup {dirr[i].get("name")} created')
        if dirr[i]['status'] == True:
            with open(FixDir(backup_path) + 'locations.txt', "w") as f: # Write all backups in locations.txt
                for i in dirr:
                    f.write(f'{dirr[i].get("name")};{dirr[i].get("path")}\n')
        shutil.make_archive('BACKUP', 'zip', backup_path) # Create backup zip file
        RemoveDir('backup') # Remove backup folder
        Press()
    if opt == 2: # Restore
        if GetRestoreList(1) != False:
            for i in dirr: # Restore all backups
                if dirr[i]['status'] == True:
                    shutil.copytree(FixDir(backup_path) + dirr[i].get('name'), dirr[i].get('path'))
                    print(f'{dirr[i].get("name")} Restored')
            RemoveDir('backup') # Remove backup folder
            Press()
        else:
            print('BACKUP.zip not found!')
            Press()
    if opt == 3: # Show\Edit list
        if GetRestoreList(1) != False:
            ShowList(dirr)
            Press()
        else:
            print('BACKUP.zip not found!')
            Press()
    if opt == 4: # Refresh list
        dirr = GetRestoreList(2)
    if opt == 5: # Exit
        break
