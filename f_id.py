# coding:utf-8
import sys
import sqlite3
import os


class Info:
    tp = dict()
    tp["ffd8ffe000104a464946"] = "jpg"     # JPEG [jpg)
    tp["89504e470d0a1a0a0000"] = "png"     # PNG [png)
    tp["47494638396126026f01"] = "gif"     # GIF [gif)
    tp["49492a00227105008037"] = "tif"     # TIFF [tif)
    tp["424d228c010000000000"] = "bmp"     # 16色位图[bmp)
    tp["424d8240090000000000"] = "bmp"     # 24位位图[bmp)
    tp["424d8e1b030000000000"] = "bmp"     # 256色位图[bmp)
    tp["41433130313500000000"] = "dwg"     # CAD [dwg)
    tp["7b5c727466315c616e73"] = "rtf"     # Rich Text Format [rtf)
    tp["38425053000100000000"] = "psd"     # Photoshop [psd)
    tp["46726f6d3a203d3f6762"] = "eml"     # Email [Outlook Express 6] [eml)
    tp["d0cf11e0a1b11ae10000"] = "doc"     # MS Excel 注意：word、msi 和 excel的文件头一样
    tp["d0cf11e0a1b11ae10000"] = "vsd"     # Visio 绘图
    tp["5374616E64617264204A"] = "mdb"     # MS Access [mdb)
    tp["252150532D41646F6265"] = "ps"      #
    tp["255044462d312e350d0a"] = "pdf"     # Adobe Acrobat [pdf)
    tp["2e524d46000000120001"] = "rmvb"    # rmvb/rm相同
    tp["464c5601050000000900"] = "flv"     # flv与f4v相同
    tp["00000020667479706d70"] = "mp4"
    tp["49443303000000002176"] = "mp3"
    tp["000001ba210001000180"] = "mpg"
    tp["3026b2758e66cf11a6d9"] = "wmv"     # wmv与asf相同
    tp["52494646e27807005741"] = "wav"     # Wave [wav)
    tp["52494646d07d60074156"] = "avi"
    tp["4d546864000000060001"] = "mid"     # MIDI [mid)
    tp["504b0304140000000800"] = "zip"
    tp["526172211a0700cf9073"] = "rar"
    tp["504b03040a0000000000"] = "jar"
    tp["4d5a9000030000000400"] = "exe"    # 可执行文件
    tp["4d616e69666573742d56"] = "mf"    # MF文件
    tp["494e5345525420494e54"] = "sql"    # xml文件
    tp["1f8b0800000000000000"] = "gz"    # gz文件
    tp["6c6f67346a2e726f6f74"] = "properties"    # bat文件
    tp["cafebabe0000002e0041"] = "class"    # bat文件
    tp["49545346030000006000"] = "chm"    # bat文件
    tp["04000000010000001300"] = "mxp"    # bat文件
    tp["504b0304140006000800"] = "docx"    # docx文件
    tp["d0cf11e0a1b11ae10000"] = "wps"    # WPS文字wps、表格et、演示dps都是一样的
    tp["6431303a637265617465"] = "torrent"

def genFile(dir):
    for i in os.listdir(dir):
        p = os.path.join(dir, i)
        if os.path.isfile(p):
            yield p
        elif os.path.isdir(p):
            print('--------------')
            genFile(p)
        else:
            continue




def getFileData(fn):
    r = str()
    ext = getExtName(fn)
    with open(fn, 'rb') as f:
        t10 = f.read(10)
        for i in range(10):
            if 9 >= t10[i] >= 0:
                r += '0'+ hex(t10[i])[2:4]
            else:
                r += hex(t10[i])[2:4]
    ext =getExtName(fn)
    return r,ext


def getExtName(fn):
    import os
    if os.path.exists(fn) and os.path.isfile(fn):
        (filepath, tempfilename) = os.path.split(fn)
        (shotname, extension) = os.path.splitext(tempfilename)
        return extension
    else:
        return None




def buildDB(listdata=list()):
    conn = sqlite3.connect("fileinfo.db")
    s=conn.execute("""select count(*) from sqlite_master where type='table' and name='filevector'""")
    if s.fetchone()[0] ==0:
        conn.execute('''CREATE TABLE filevector
               (vec varchar(20) PRIMARY KEY  NOT NULL,
                extname   varchar(10)    NOT NULL,
                desc      varchar(50));''')

    sql = 'insert into vecinfo (vec,extname,des) values(?,?,?)'
    try:
        conn.executemany(sql,listdata)
        conn.commit()
    except Exception as e:
        raise Exception("更新数据库出错")



def handler(fn):
    r = str()
    with open(fn, 'rb') as f:
        t10 = f.read(10)
        for i in range(10):
            if 9 >= t10[i] >= 0:
                r += '0'+ hex(t10[i])[2:4]
            else:
                r += hex(t10[i])[2:4]
    print('-' * 40)
    if r in Info.tp.keys():
        print('-'*40)
        print("{0}的文件类型是:{1}".format(fn, Info.tp[r]))
        print('-'*40)



def main(argv):
   for i in genFile("d:\\tool"):
       print(i)

if __name__ == '__main__':
    main(sys.argv)
