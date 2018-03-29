import os
import sys
import subprocess


hashes = []
md5 = ''


def main():
    mounter()
    get_MD5()
    unmount()
    printer()


def mounter():
    for file in range(1, len(sys.argv)):
        cur_dir = os.getcwd()
        cur_dir += '/'+str(sys.argv[file])
        a = subprocess.call(['hdiutil',  'attach', cur_dir])


def get_MD5():
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
    for i in range(0,len(hashes),2):
        md5_path = '/' + hashes[i].split('/')[1] + '/' + hashes[i].split('/')[2] + '/'
        subprocess.call(['hdiutil', 'detach', md5_path])


def printer():
    print ('path:' + '\t\t\t\t\t\t\t\t' + 'MD5:')
    for i in range(0,len(hashes),2):
        print (hashes[i] + '\t' + hashes[i+1])


if __name__ == '__main__':
    main()