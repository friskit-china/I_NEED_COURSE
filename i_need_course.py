# -*- coding:utf-8
import urllib2
import sys
import re
import json
import time

entry_uri = 'http://grdms.bit.edu.cn/yjs/dwr/call/plaincall/YYPYCommonDWRController.pyJxjhSelectCourse.dwr'
cookie_filename = 'cookies.txt'
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: python i_need_course.py timeout(sec) <configure>'
        exit()
    timeout = int(sys.argv[1])
    configure_filename = sys.argv[2]
    configure_content = open(configure_filename, 'rb').read()
    cookie_content = open(cookie_filename, 'rb').read()

    try_count = 0
    while True:
        try_count += 1
        json_obj = None
        try:
            print "尝试第%d次抢课中....."%try_count
            request = urllib2.Request(url = entry_uri, data = configure_content)
            request.add_header('Accept', '*/*')
            request.add_header('Content-Type', 'text/plain')
            request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)')
            request.add_header('Host', 'grdms.bit.edu.cn')
            request.add_header('Cookie', cookie_content)
            response = urllib2.urlopen(request)
            response_text = response.read()
            json_content = re.findall(r'\[.*\]', response_text)
            json_obj = json.loads(json_content[0])
            #print json_obj # for debug
            status, msg_unicode = json_obj
            tmp = json.loads('{"i":"%s"}'%msg_unicode)
            msg = tmp['i'].encode('utf-8')
        except:
            status = "___timeout"

        if json_obj is not None and json_obj[0] == "success":
            print "抢课成功，程序结束"
            exit()
        if status == "___timeout":
            print "连接超时，即将重试"
        elif status == "failure":
            if msg == "选课时发生错误，超过限选人数。":
                print "尚未有人退课，抢课失败，一秒后重试...."
            elif msg == "选课时发生错误，该课程和学生已选课程存在时间冲突。":
                print u"该课程与学生已选课程存在时间冲突，程序结束"
                exit()
        else:
            print "未知状态，程序结束"
            exit()
        time.sleep(timeout)

