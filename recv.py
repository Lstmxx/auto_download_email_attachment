# -*- coding: UTF-8 -*-
import poplib
import keyboard
import re
import email
from email.parser import Parser
from email.header import decode_header, Header
from email.utils import parseaddr
import time
import readconf
import os
import datetime
import Myemail

def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def get_charest(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

def save_file(path, Subject, filename, data, way='wb'):
    fpath = path+"\\"+Subject+"\\"
    if os.path.exists(fpath) == False:
        os.makedirs(fpath)
    if way == 'w':
        with open(fpath+filename, way, encoding="utf-8") as f:
            f.write(data)
    elif way == 'wb':
        with open(fpath+filename, way) as f:
            f.write(data)
    return fpath+filename

def get_email_value(msg, path, Subject):
    attachment_files = []
    html_path = ''
    txt_path = ''
    for part in msg.walk():
        file_name = part.get_filename()
        t = part.get_content_type()
        if t == "text/html" or t == "text/plain":
            content = part.get_payload(decode=True)
            charset = get_charest(part)
            if charset:
                content = content.decode(charset)
            if t == "text/html":
                html_path = save_file(path, Subject, Subject+'.html', content, way='w')
            elif t == "text/plain":
                txt_path = save_file(path, Subject, Subject+'.txt', content, way='w')
        if file_name:
            h = Header(file_name)  # 转换成Header类
            dh = decode_header(h)  # 转换成list类，格式为[(文件名，编码名)]
            filename, charset = dh[0]
            if charset:
                filename = decode_str(str(filename, charset))
            data = part.get_payload(decode=True)
            fp = save_file(path, Subject, filename, data)
            attachment_files.append(fp)
    return attachment_files,html_path,txt_path

def init_server(user):
    server = poplib.POP3(user[2])
    server.user(user[0])
    server.pass_(user[1])
    return server

def toMessage(lines):
    msg_context = b'\r\n'.join(lines).decode('utf-8')
    msg = Parser().parsestr(msg_context)
    return msg

def analysis_email(lines):
    e = Myemail.MyEmail()
    msg = toMessage(lines)
    date = time.strptime(msg.get("Date")[0:24], '%a, %d %b %Y %H:%M:%S')
    date = time.strftime("%Y%m%d", date)
    p = readconf.get_conf_value("save_path")
    if p[0] == '\\save':
        path = os.path.abspath(os.path.join(
            os.path.dirname("__filename__"))) + p[0] + "\\"+date
    else:
        path = p[0]+"\\"+date

    Subject = msg.get("Subject", '')
    Subject = decode_str(Subject)
    e.Subject = Subject

    sender = msg.get("From", '')
    hdr, addr = parseaddr(sender)
    name = decode_str(hdr)
    e.Sender = [name,addr]

    value = msg.get("To", '')
    value = value.replace('\r', "").replace('\n', "").replace('\t', "")
    list_to = value.split(",")
    dict_to = {}
    if len(list_to) > 1:
        for i in list_to:
            i = i.lstrip()
            d = i.split(' ')
            dict_to[d[0]] = d[1].replace('<', '').replace('>', '')
    else:
        hdr, addr = parseaddr(value)
        name = decode_str(hdr)
        dict_to[name] = addr
    e.Recipient = dict_to
    e.file,e.html,e.context=get_email_value(msg, path, Subject)
    return e

def main():
    user = readconf.get_conf_value("user")
    server = init_server(user)
    message_num, size = server.stat()
    print("start catch")
    num = 0
    size = 0
    em = Myemail.MyEmail()
    while True:
        server = init_server(user)
        try:
            if keyboard.is_pressed('q'):
                print('you quit')
                break
        except:
            break
        num,size = server.stat()
        if num > message_num:
            dist = num - message_num
            print("you have %s new emails" % dist)
            print("you have %s emails now" % num)
            print("save file now")
            s = datetime.datetime.now()
            for i in range(1,dist+1):
                _, lines, _ = server.retr(message_num+i)
                em = analysis_email(lines)
                em.showInfo(i)
                em.clear()
            e = datetime.datetime.now()
            message_num = num
            print("save_compile")
            print("use time:%s s" % (e-s))
        elif num < message_num:
            message_num = num

if __name__ == "__main__":
    main()
