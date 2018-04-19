import os
import re
import os.path
import time


def GetFileList(dir, fileList):
    new_dir = dir
    if os.path.isfile(dir):
        fileList.append(dir.encode('utf-8').decode('utf-8'))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            #如果需要忽略某些文件夹，使用以下代码
            #if s == "xxx":
                #continue
            new_dir = os.path.join(dir,s)
            GetFileList(new_dir, fileList)
    return fileList

rq = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
today_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
dir = os.getcwd()
# dir = 'D:\\daily'
daily_path = dir + '\\' + today_time + '\\'
config_path = dir + '\\config.ini'
w_path = dir + '\\' + rq + '.log'

w = open(w_path, 'w', encoding='UTF-8')
f = open(config_path, 'r', encoding='utf_8_sig')

namelist = []
w.write(u'完整的名单：'),
for list_namelist in f:
    list_namelist = list_namelist.strip()
    list_namelist = re.sub(" ", "", list_namelist)
    if list_namelist == '':
        pass
    else:
        w.write(list_namelist),
        w.write(' '),
        namelist.append(list_namelist)
w.write('[%d]' % len(namelist))
f.close()

file_list = dir + '\\' + today_time + '\\'
filelist = GetFileList(file_list, [])
last = []
for e in filelist:
    e = os.path.basename(e)
    # 新的匹配
    e = re.sub(" ", "", e)
    # e = re.sub("(?isu)^\S*技术部", "", e)
    # e = re.sub("(?isu)^\S*产品部", "", e)
    # e = re.sub("(?isu)^\S*运营部", "", e)
    # e = re.sub("(?isu)日报\S*$", "", e)
    e = re.sub("[A-Za-z0-9\!\%\[\]\,\。\.\-\(\)]", "", e)
    # 新的匹配
    last.append(e)

uncommitted = []
committed = []
while len(namelist) > 0:
    m = namelist.pop()
    un = 'False'
    for n in last:
        if m in n:
            committed.append(m)
            un = 'True'
    if un == 'False':
        uncommitted.append(m)

w.write('\n\n提交的名单：'),
for list_committed in committed:
    w.write(list_committed),
    w.write(' '),
w.write('[%d]' % len(committed))

w.write('\n\n未提交名单：'),
for list_uncommitted in uncommitted:
    w.write(list_uncommitted),
    w.write(' '),
w.write('[%d]' % len(uncommitted))

w.close()