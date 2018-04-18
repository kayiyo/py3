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

rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
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
for line in f:
    line = line.strip()
    line = re.sub(" ", "", line)
    if line == '':
        pass
    else:
        w.write(line),
        w.write(' '),
        namelist.append(line)
    # print(line)
len_namelist = len(namelist)
# if len_namelist < 0:
#     len_namelist = 0
w.write('[%d]' % len_namelist)
f.close()

file_list = dir + '\\' + today_time + '\\'
list = GetFileList(file_list, [])
last = []
for e in list:
    e = os.path.basename(e)
    # 新的匹配
    e = re.sub(" ", "", e)
    e = re.sub(u"(?isu)\S*技术部", "", e)
    e = re.sub(u"(?isu)\S*产品部", "", e)
    e = re.sub(u"(?isu)\S*运营部", "", e)
    e = re.sub(u"(?isu)日报\S*", "", e)
    e = re.sub("[A-Za-z0-9\!\%\[\]\,\。\.\-\(\)]", "", e)
    # 新的匹配
    last.append(e)
w.write('\n\n提交的名单：'),
for last_name in last:
    w.write(last_name),
    w.write(' '),
w.write('[%d]' % len(last))

w.write('\n\n未提交名单：'),
uncommitted = []
for m in namelist:
    if m in last:
        pass
    else:
        uncommitted.append(m)
        w.write(m),
        w.write(' '),
len_uncommitted = len(uncommitted)
# if len_uncommitted < 0:
#     len_uncommitted = 1
w.write('[%d]' % len_uncommitted)

w.close()
