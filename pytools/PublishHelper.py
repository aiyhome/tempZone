#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
# layaair2-cmd是layaair 2.0的命令行工具，依赖于node.js环境，
# 1.安装node.js环境
# 2.安装全局gulp,命令行cmd输入：npm install gulp -g (layaair2-cmd依赖于gulp)
# 3.安装全局layaair2-cmd,命令行cmd输入：npm install layaair2-cmd -g
 
使用例子：
PublishHelper.py --indir D:/H5DZGame/trunk --outdir D:/www
PublishHelper.py --i D:/H5DZGame/trunk --o D:/www
'''

import os
import sys
import time
import argparse
import shutil

VERSION = '0.0.1'
NPM_CLI_BIN = 'C:/Users/Dzg_gz/AppData/Roaming/npm'
LAYAIR_CLI_VERSION = '1.0'


def log(msg):
    local_time = time.localtime(time.time())
    time_stamp = time.strftime('[%Y-%m-%d %H:%M:%S]', local_time)
    print(time_stamp + ' ' + msg)


def get_current_file_dir():
    return os.path.dirname(__file__)


def copy_proj(srcdir, dstdir):
    cpy_items = ['.laya', 'bin', 'laya', 'libs', 'src',
                 'DZGame.laya', 'module.def', 'tsconfig.json']
    if not os.path.exists(dstdir):
        os.mkdir(dstdir)
    for i in range(1, len(cpy_items)):
        srcpath = os.path.join(srcdir, cpy_items[i])
        topath = os.path.join(dstdir, cpy_items[i])
        if os.path.isfile(srcpath):
            shutil.copyfile(srcpath, topath)
        else:
            shutil.copytree(srcpath, topath)


def publish(opts):
    ver_code = int(time.time())
    ver_name = time.strftime('%Y%m%d%H%M', time.localtime())
    publish_mode = opts.mode
    project_dir = opts.indir
    publish_out_dir = os.path.join(opts.outdir, 'h5/'+publish_mode)
    if publish_mode == 'debug':
        project_dir = publish_out_dir+'_src'
        if os.path.exists(project_dir):
            shutil.rmtree(project_dir)
        copy_proj(opts.indir, project_dir)
    os.chdir(project_dir)
    retval = os.getcwd()
    log('change workplace to dir:'+retval)

    if LAYAIR_CLI_VERSION == '1.0':
        cmd = '%s/layaair-cmd publish -n %s' % (NPM_CLI_BIN, ver_name)
        os.system(cmd)
    generate_out_dir = os.path.join(project_dir, 'release/layaweb/' + ver_name)
    if os.path.exists(publish_out_dir):
        shutil.rmtree(publish_out_dir)
    log('copy %s to %s' % (generate_out_dir, publish_out_dir))
    shutil.copytree(generate_out_dir, publish_out_dir)
    shutil.rmtree(generate_out_dir)

    os.chdir(publish_out_dir)
    retval = os.getcwd()
    log('change workplace to dir:'+retval)
    os.system('%s/layadcc .' % NPM_CLI_BIN)
    # alone
    os.system('%s/layadcc %s -cache -url http://stand.alone.version/index.html' %
              (NPM_CLI_BIN, publish_out_dir))
# layanative2 refreshres [-p all|ios|android_eclipse|android_studio|wkwebview] [--path path] [-u url]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version',
                        help='tool version info', default=None)
    parser.add_argument(
        '-i', '--indir', help='project start directory path', required=True, default=None)
    parser.add_argument(
        '-o', '--outdir', help='project publish out directory path', required=True, default=None)
    parser.add_argument(
        '-m', '--mode', help='project publish mode', type=str, default='debug')
    args = parser.parse_args()
    print(args)
    publish(args)


if __name__ == '__main__':
    main()
