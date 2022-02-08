import os
import shutil

def GetLastDir(path):
    LastDir = os.path.basename(os.path.normpath(path))
    return LastDir

def FixDir(path): # Fix dir format
    if path.endswith('\n'):
        path = path[:-1]
    if path[-2:] != '\\':
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
dirlist = []
dir_path = os.path.dirname(__file__)

RemoveDir('BACKUP.zip')
RemoveDir('backup')

backup_path = os.path.join(dir_path, 'backup') # Create backup folder dir variable

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

# for path in os.listdir(dir_path): # Get all files dir from dir.txt and save in dirr dict
#     if path == 'dir.txt':
#         with open(path) as f:
#             for line in f:
#                 dirr[k] = line
#                 k += 1

# for i in range(len(dirr)): # This loop create all backups from dir.txt
#     backdir = ''
#     backdir = os.path.join(backup_path, GetLastDir(FixDir(dirr[i])))
#     shutil.copytree(FixDir(dirr[i]), backdir)

shutil.make_archive('BACKUP', 'zip', backup_path) # Create backup zip file

RemoveDir('backup')