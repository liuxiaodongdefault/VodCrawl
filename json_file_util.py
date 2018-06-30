# -*- coding: utf-8 -*-
import json



def write(json_name, data):
    with open(json_name + '.json', 'w') as json_file:
        json_file.write(json.dumps(data,ensure_ascii=False))

def load(json_name):
    with open(json_name + '.json') as json_file:
        data = json.load(json_file)
        return data