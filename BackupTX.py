import os
import shutil

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
            shutil.rmtree(path)
            return
        except:
            pass
        try:
            os.remove('BACKUP.zip')
            return
        except:
            pass

dirr = {}
dir_path = os.path.dirname(__file__)
backup_path = os.path.join(dir_path, 'backup') # Create backup folder dir variable
menu = 1
opt = 0

while menu != 0:
    os.system('cls')
    opt = int(input('1. Backup\n2. Restore\n3. Exit\n\nSelect option: '))
    os.system('cls')

    if opt == 1: # Backup
        RemoveDir('BACKUP.zip')
        RemoveDir('backup')

        for path in os.listdir(dir_path): # Get all files dir from dir.txt and save in dirr dict
            if path == 'dir.txt':
                with open(path) as f:
                    for line in f:
                        dirr[GetLastDir(FixDir(line))] = {
                            'name': GetLastDir(FixDir(line)),
                            'path': FixDir(line)
                        }

        for i in dirr: # This loop create all backups from dir.txt
            backdir = ''
            backdir = os.path.join(backup_path, dirr[i].get('name'))
            shutil.copytree(dirr[i].get('path'), backdir)
            print(f'Backup {dirr[i].get("name")} created')

        with open(FixDir(backup_path) + 'locations.txt', "w") as f: # Write all backups in locations.txt
            for i in dirr:
                f.write(f'{dirr[i].get("name")};{dirr[i].get("path")}\n')

        shutil.make_archive('BACKUP', 'zip', backup_path) # Create backup zip file

        RemoveDir('backup') # Remove backup folder
        input('\nPress any key to continue...')
    if opt == 2: # Restore
        dirr = {}

        if os.path.exists('BACKUP.zip'): # check if backup.zip exists
            shutil.unpack_archive('BACKUP.zip', 'backup') # unpacking backup.zip
            with open(FixDir(backup_path) + 'locations.txt', "r") as f: # Read locations.txt
                for line in f:
                    y, k = FixDir(line).split(';')
                    dirr[y] = {
                        'name': y,
                        'path': k
                    }
            for i in dirr: # Restore all backups
                shutil.copytree(FixDir(backup_path) + dirr[i].get('name'), dirr[i].get('path'))
                print(f'{dirr[i].get("name")} Restored')
            RemoveDir('backup') # Remove backup folder
            input('\nPress any key to continue...')
        else:
            print('BACKUP.zip not found!')
            input('\n\nPress any key to continue...')

    if opt == 3: # Exit
        menu = 0