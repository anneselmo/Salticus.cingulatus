#! /usr/bin/py

import os
import datetime

from time import sleep

import utils
import salt

def wait_until(utime):
    while datetime.datetime.now().timestamp() < utime:
        sleep(10)
    return(0)

def merge_got_list(ngot_list, got_list):
    for key in ngot_list:
        if key in got_list:
            if got_list[key][0][-1:] is not ngot_list[key][0]:
                got_list[key][0].append(ngot_list[key][0])
                got_list[key][1].append(ngot_list[key][1])
        else:
            got_list[key]=([ngot_list[key][0]], [ngot_list[key][1]])
    return(got_list)

def guess_times(llist):
    glist={}
    for item in llist:
        i=0
        value=0
        for time in llist[item][1]:
            if i is not 0:
                value=value+(time-llist[item][1][i-1])
            i=i+1
        glist[item]=int(value/i)
    return(glist)

def gen_get_list(llist, time):
    get_list=[]
    ctime=int(datetime.datetime.now().timestamp())
    glist=guess_times(llist)
    for item in glist:
        if ctime+time > glist[item]:
            get_list.append(item)
    return(get_list)
                
def crawl_loop(get_list):
    rounds=2
    limit=320
    threads=5
    wtime=86400
    root=os.path.abspath(".")
    place=root+"/qqqa/"
    global got_list
    try:
        got_list=cdb2dict(cpath+"/updates.dict.cdb")
        get_list=gen_get_list(got_list, 86400)
    except:
        got_list={}
    got_list=merge_got_list(salt.countloop(get_list, rounds, limit, threads, 0), got_list)
    get_list=gen_get_list(got_list, wtime)
    wait_until(int(datetime.datetime.now().timestamp())+wtime)
    while True:
        try:
            os.chdir(place)
        except:
            os.makedirs(place)
            os.chdir(place)
        got_list=merge_got_list(salt.countloop(get_list, rounds, limit, threads, 0), got_list)
        get_list=gen_get_list(got_list)
        print(get_list)
        utils.dict2cdb(got_list, path+"/updates.dict.cdb")
        utils.dict2cdb(got_list, path+datetime.datetime.now().strftime("%F.%S")+"/updates.dict.cdb")
        wait_until(int(datetime.datetime.now().timestamp())+wtime)
    return(got_list)
