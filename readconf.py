import configparser
import os
def get_conf_value(sections):
    conf = configparser.ConfigParser()
    conf.read("user.conf")
    kv = conf.items(sections)
    user = []
    for i in kv:
        user.append(i[1])
    return user

