# -*- coding: utf-8 -*-

import json
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from airium import Airium

#dir_path = '/home/student/rawData/'
dir_path = 'C:/Users/vova-/Desktop/ВУЗ/ПРОЕКТНЫЙ СЕМИНАР/Микропроект/data/'

username = 'vvgorovoy@miem.hse.ru'
login = username[:username.find('@')]

#output_path = f'/home/student/student_stats/{login}/'
output_path = dir_path

jitsisession_path = dir_path + 'JitsiSession.json'
gitstats_path = dir_path + 'GitStats.json'
zulipstats_path = dir_path + 'ZulipStats.json'

def get_dict(path):
    """Открытие json-файла и перевод данных в словарь питона"""
    with open(path, 'r', encoding = 'utf-8') as file:
        text = json.load(file)
    return text

def get_jitsi_stats(path, nick):
    """
    Получение кол-ва посещенных проектных семинаров и списка дат их проведения
    и получение кол-ва посещенных проектов на постерной сессии со списком дат
    посещения
    """
    info = get_dict(path)
    sem = 0
    proj = 0
    dates_sem = []
    dates_pr = []
    for item in info:
        if item['username'] == nick:
            if item['room'] == '312':
                sem += 1
                if sem > 1:
                    if datetime.strptime(item['date'], '%Y-%m-%d') != dates_sem[sem-2]:
                        dates_sem.append(datetime.strptime(item['date'], '%Y-%m-%d'))
                    else:
                        sem -= 1
                else:
                    dates_sem.append(datetime.strptime(item['date'], '%Y-%m-%d'))
            if item['room'][:7] == 'project':
                proj += 1
                dates_pr.append(datetime.strptime(item['date'], '%Y-%m-%d'))
    return sem, proj, dates_sem, dates_pr

def get_zulip_stats(path, nick):
    """Получение кол-ва сообщений в Zulip и списка дат их отправления"""
    info = get_dict(path)
    dates_mes = []
    for item in info:
        if item['email'] == nick:
            mes = len(item['messages'])
            for message in item['messages']:
                dates_mes.append(datetime.strptime(message['timestamp'][:10], '%Y-%m-%d'))
    return mes, dates_mes

def get_git_stats(path, nick):
    """Получение числа коммитов и списка дат совершения этих коммитов"""
    coms = 0
    dates_com = []
    git_acc = False
    for item in get_dict(path):
        if item['email'] == nick:
            git_acc = True
            projects = item['projects']
            coms += projects[0]['commitCount']
            if coms > 0:
                for commit in projects[0]['commits']:
                    dates_com.append(datetime.strptime(commit['committed_date'][:10], '%Y-%m-%d'))
    return coms, dates_com, git_acc


def get_dots(dates, xdates):
    """Получение координат всех точек"""
    dots = {
        'x': [0],
        'y': [0]
        }
    num = 0
    numx = 0
    for i in np.arange(len(xdates)):
        numx += 1
        dots['x'].append(numx)
        dots['y'].append(num)
        if xdates[i] in dates:
            num += dates.count(xdates[i])
            dots['y'].append(num)

        else:
            dots['y'].append(num)
        dots['x'].append(numx)
    return dots

def visualize(sem_dates, project_dates, mes_dates, com_dates):
    """Визуализация данных"""
    all_dates = sem_dates + project_dates + mes_dates + com_dates + [datetime.now()]
    all_dates = list(set(all_dates))
    all_dates.sort()
    xlabels = ['01.01.2021']
    for date in all_dates:
        xlabels.append(datetime.strftime(date, "%d.%m.%Y"))
    yticks = np.arange(max(len(sem_dates), len(project_dates), len(mes_dates), len(com_dates))+1)

    sem_dots = get_dots(sem_dates, all_dates)
    pr_dots = get_dots(project_dates, all_dates)
    zulip_dots = get_dots(mes_dates, all_dates)
    git_dots = get_dots(com_dates, all_dates)

    fig, ax = plt.subplots()

    ax.plot(sem_dots['x'], sem_dots['y'], color = 'b', label = 'Посещенные семинары')
    ax.plot(pr_dots['x'], pr_dots['y'], color = 'r', label = 'Посещенные проекты')
    ax.plot(zulip_dots['x'], zulip_dots['y'], color = 'g', label = 'Сообщения в Zulip')
    ax.plot(git_dots['x'], git_dots['y'], color = 'orange', label = 'Коммиты в GitLab')

    ax.legend(bbox_to_anchor=(0, .99, 1, 0), ncol = 2)

    ax.set_xticks(np.arange(len(xlabels)))
    ax.set_xticklabels(xlabels, rotation = 35)
    ax.set_yticks(yticks)

    ax.grid()
    plt.show()
    fig.subplots_adjust(top=0.85, bottom=0.2)
    fig.savefig(f'{output_path}graph.jpg')

def get_mark(ns, npr, nm, nc, tf_git_acc):
    """Получение итоговой оценки"""
    tf_zulip = nm>0
    tf_git = nc>0
    mark = round(0.5*ns + 0.5*npr + 2*tf_zulip + tf_git + tf_git_acc)
    if mark>10:
        mark = 10
    return mark

a = Airium()

def generate_html(mark):
    """Генерация html-страницы"""
    a('<!DOCTYPE html>')
    with a.html(lang='en'):
        with a.head():
            a.meta(charset='UTF-8')
            a.title(_t = 'Динамика цифрового следа')
        with a.body():
            with a.div():
                a.img(src='graph.jpg')
            a.h3(_t = f'Пользователь: {username}')
            a.h2(_t = f'Итоговая оценка: {mark}')
            a.h4(_t=f'Даннные актуальны на {datetime.strftime(datetime.now(),"%d.%m.%Y %H:%M:%S")}')
    with open(f'{output_path}{login}.html', 'w', encoding="utf-8") as file:
        file.write(str(a))


num_sems, num_projects, sem_dates, project_dates = get_jitsi_stats(jitsisession_path, username)

num_messages, mes_dates = get_zulip_stats(zulipstats_path, username)

num_commits, com_dates, has_git_acc = get_git_stats(gitstats_path, username)

visualize(sem_dates, project_dates, mes_dates, com_dates)

grade = get_mark(num_sems, num_projects, num_messages, num_commits, has_git_acc)

generate_html(grade)
