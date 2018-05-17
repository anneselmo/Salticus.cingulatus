#! /usr/bin/py

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
            if got_list[key][0] is not ngot_list[key][0]:
                got_list[key][0] = ngot_list[key][0]
                got_list[key][1].append(ngot_list[key][1][0])
        else:
             got_list[key]=ngot_list[key]
    return(got_list)

def guess_times(llist):
    glist={} 
    for item in llist:
        dif=0
        while i > len(item[1]):
            if i is not 0:
                last=item[1][i]
                dif=dif+(last - item[1][i-1])
        avg=dif/(i+1)
        glist[item]=int(last+avg)
    return(glist)

def gen_get_list(llist, time):
    get_list=[]
    ctime=int(datetime.datetime.now().timestamp())
    glist=guess_times(llist)
    for item in glist:
        if ctime+time > glist[item]:
            get_list.append(item)
    return(get_list)
                
def crawl_loop():
    global got_list
    try:
        got_list=cdb2dict(cpath+"/updates.dict.cdb")
        get_list=gen_get_list(got_list, 86400)
    except:
        got_list={}
    rounds=1
    limit=320
    threads=3
    got_list=merge_got_list(salt.countloop(, rounds, limit, threads), got_list)
    while True:
        got_list=merge_got_list(salt.countloop(get_list, rounds, limit, threads), got_list)
        get_list=gen_get_list(got_list)
        utils.dict2cdb(got_list, path+"/updates.dict.cdb") 
