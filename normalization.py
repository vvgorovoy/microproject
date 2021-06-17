# -*- coding: utf-8 -*-

import json

#dir_path = '/home/student/rawData/'
dir_path = 'C:/Users/vova-/Desktop/ВУЗ/ПРОЕКТНЫЙ СЕМИНАР/Микропроект/data/'
jitsiclasses_path = dir_path + 'JitsiClasses.json'
jitsisession_path = dir_path + 'JitsiSession.json'
gitstats_path = dir_path + 'GitStats.json'
zulipstats_path = dir_path + 'ZulipStats.json'

pathes = [jitsiclasses_path, jitsisession_path, gitstats_path, zulipstats_path]

new_jitsiclasses_path = dir_path + 'new_JitsiClasses.json'
new_jitsisession_path = dir_path + 'new_JitsiSession.json'
new_gitstats_path = dir_path + 'new_GitStats.json'
new_zulipstats_path = dir_path + 'new_ZulipStats.json'

new_pathes = [new_jitsiclasses_path, new_jitsisession_path, new_gitstats_path, new_zulipstats_path]

def normalization(path, new_path):
    with open(path, 'r', encoding = 'utf-8') as f:
        full_text = json.load(f)         
    with open(new_path, 'w', encoding='utf-8') as nf:
        json.dump(full_text, nf, indent=2, ensure_ascii=False)

for path, new_path in zip(pathes, new_pathes):    
    normalization(path, new_path)