#! /usr/bin/py

import sleep
import datetime

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

def crawl_loop():
    global got_list
    got_list={}

    while true:
        got_list=merge_got_list(salt.countloop(get_list, rounds, limit, threads), got_list)
        get_list=gen_get_list(got_list)

