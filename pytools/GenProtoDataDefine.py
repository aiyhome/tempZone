#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import re
import time
import sys


def log(msg):
    local_time = time.localtime(time.time())
    time_stamp = time.strftime('[%Y-%m-%d %H:%M:%S]', local_time)
    print(time_stamp + ' ' + msg)


def getTsType(s_type, is_array):
    ts_type = ''
    if s_type in 'cbBhHiIlLfd':
        ts_type = 'number'
    elif s_type in 'sS':
        ts_type = 'string'
    elif len(s_type) > 1:
        ts_type = s_type
    else:
        ts_type = 'any'

    if is_array:
        ts_type = ts_type + '[]'
    return ts_type


def isUpperLetters(str_):
    ret = True
    wordlist = [chr(i) for i in range(97, 23)]
    for i in range(len(str_)):
        c = str_[i]
        if c in wordlist:
            if not c.isupper():
                ret = False
                break
    return ret


def upperFirstLetter(str_):
    return str_[0].upper()+str_[1:]


def parseSubProtoData(itstr):
    regex = re.compile(r'[/]\*\*\s*\@\s*(.*?)\s*\*[/]', re.S)
    ret = re.search(regex, itstr)
    cls_name = None
    if ret:
        w_str = ret.group(0)
        cls_name = ret.group(1)
    else:
        regex = re.compile(r'\[(.*?)\]', re.S)
        ret = re.search(regex, itstr)
        if ret:
            key = ret.group(1)
            if "'" in key or '"' in key:
                cls_name = key.replace('"', '').replace("'", '')
            elif '.' in key:
                arr = key.split('.')
                cls_name = arr[len(arr)-1]
                if isUpperLetters(cls_name):
                    cls_name += '_DATA'
                else:
                    cls_name += 'Data'
                upperFirstLetter(cls_name)
            else:
                cls_name = key
                if isUpperLetters(cls_name):
                    cls_name += '_DATA'
                else:
                    cls_name += 'Data'
                upperFirstLetter(cls_name)
    if cls_name:
        regex = re.compile(r'\[[\w.\'\"]+\]\s*\:\s*\[(.*)\]', re.S)
        ret = re.search(regex, itstr)
        propertys = None
        if ret:
            line_arr = ret.group(1).split('\n')
            propertys = {}
            for line in line_arr:
                if not line.isspace() and len(line) > 0:
                    # print(line)
                    regex = re.compile(r'\[(.*?)\]\,*\s*([//].*)*', re.S)
                    ret = re.search(regex, line)
                    if ret:
                        # print(ret.group(1),ret.group(2))
                        tmp_str = ret.group(1)
                        arr = tmp_str.split(',')
                        p_name = arr[0].strip().replace(
                            '"', '').replace("'", '')
                        p_type = arr[1].strip().replace(
                            '"', '').replace("'", '')
                        p_array = None
                        if len(arr) > 2:
                            p_array = arr[1]
                        p_note = ret.group(2)
                        propertys[p_name] = {
                            'name': p_name,
                            'type': p_type,
                            'array': p_array,
                            'note': p_note,
                            'ts_type': getTsType(p_type, p_array)
                        }
        return {'cls_name': cls_name, 'propertys': propertys}
    return None


def parseProtoSchemaData(content):
    regex = re.compile(r'export.*=\s*[{](.*)[}]', re.S)
    main_trunks = re.findall(regex, content)

    obj_datas = []
    regex = re.compile(
        r'([/**\s*@\w+\s**/]*\[[\w.\'\"]+\]\:\s*\[.*?\n\s*\]\s*)\,*', re.S)
    for obj_str in main_trunks:
        items = re.findall(regex, obj_str)
        if items:
            for i_str in items:
                data = parseSubProtoData(i_str)
                if data:
                    obj_datas.append(data)
    return obj_datas


def openFile(filepath, mode, encoding):
    if sys.version_info.major == 3:
        return open(filepath, mode, encoding=encoding)
    else:
        import codecs
        return codecs.open(filepath, mode, encoding)


def writeDataDefTs(objs, outflie, infile_basename):
    fp = openFile(outflie, 'a+', 'utf-8')
    fp.seek(0)
    fp.truncate()
    fp.write(u'/** 以下内容是根据%s由脚本GenProtoDataDefine.py生成导出 */\n\n' %
             infile_basename)
    for obj in objs:
        # print(obj)
        cls_name = obj['cls_name']
        fp.write('declare interface %s {\n' % cls_name)
        propertys = obj['propertys']
        if propertys:
            for k in propertys.keys():
                line = '    %s: %s;' % (k, propertys[k]['ts_type'])
                line = line.ljust(60)
                if 'note' in propertys[k] and propertys[k]['note']:
                    line = line + propertys[k]['note']
                fp.write(line + '\n')
        fp.write('}\n\n')
    fp.close()


def genDataDefTs(args):
    if not os.path.exists(args.infile):
        log('%s not exists' % args.infile)
        return
    infile = args.infile
    print(infile)
    fp = openFile(infile, 'r', 'utf-8')
    content = fp.read()
    fp.close()
    objs = parseProtoSchemaData(content)
    # print(alls)
    # print(objs)

    outflie = args.outfile
    if outflie == None:
        outflie = os.path.basename(infile).replace('Schema', 'DataDef')
        fname, fext = os.path.splitext(outflie)
        outflie = os.path.join(os.path.dirname(infile), fname+'.ts')
    outdir = os.path.dirname(outflie)
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    writeDataDefTs(objs, outflie, os.path.basename(infile))
    print(outflie)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', help='input path',
                        required=True, default=None)
    parser.add_argument('-o', '--outfile', help='out path',
                        required=False, default=None)
    args = parser.parse_args()
    print(args)
    genDataDefTs(args)


if __name__ == '__main__':
    main()
