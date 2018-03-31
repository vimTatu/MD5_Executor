import os
import sys
import subprocess


hashes = []
md5 = ''


def main():
    for name in sys.argv[1:]:
        mount(name)
        hashes.append(name)
        get_md5()
        unmount()
    printer()


def mount(dmg_name):
    cur_dir = os.getcwd()
    cur_dir += '/'+str(dmg_name)
    subprocess.call(['hdiutil',  'attach', cur_dir])


def get_md5():
    for dirs in os.walk('/Volumes/'):
        for directory in dirs:
            if directory != [] and 'VMware Shared Folder' and 'Macintosh HD' and str(directory).__contains__('Contents/MacOS'):
                for file in os.walk(str(directory)):
                    md5_path = ''
                    for parts in file:
                        if parts != [] and not parts.__contains__('Contents/MacOS'):
                            if str(parts.__contains__('[\'')):
                                temp = str(parts)
                                temp = temp.replace('\'', '').replace('[', '').replace(']', '')
                                md5_path = md5_path + '/' + temp 
                        elif parts != []: 
                            md5_path = str(parts)
                    md5 = subprocess.check_output(['md5', md5_path])
                    md5 = md5.split('= ')
                    hashes.append(md5_path)
                    hashes.append(md5[1].replace('\n', ''))


def unmount():
    for dirs in os.walk('/Volumes/'):
        for directory in dirs:
            if directory != [] and 'VMware Shared Folder' and 'Macintosh HD':
                subprocess.call(['hdiutil', 'detach', str(directory)])


def printer():
    with open ('report.txt', 'a') as file:
        print ('DMG Name | \t \t path | \t \t \t MD5 |')
        file.write('DMG Name | \t \t path | \t \t \t MD5 | \n ')
        for i in range(0, len(hashes), 3):
            print hashes[i] + '\t\t' + hashes[i+1] + ' \t\t\t' + hashes[i+2]
            file.write(hashes[i] + '\t\t' + hashes[i+1] + ' \t\t\t' + hashes[i+2] + '\n')

if __name__ == '__main__':
    main()
