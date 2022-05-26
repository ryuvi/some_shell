#!/usr/bin/env python3

from sys import stdout
from os import getcwd, system, listdir, chdir, remove, path
from colorama import Fore
from time import sleep
from shutil import copy, move

system('clear')
current_path = ''


def history(last_command):
    with open('my_shell.history', 'a') as f:
        f.write(last_command)


def set_path():
    global current_path
    current_path = getcwd()


def write_to_file(string, filename):
    with open(filename, 'a') as f:
        f.write(f'{string}\n')


def output(string):
    index = 5
    while index < len(string):
        if string[index] == '>':
            break
        stdout.write(string[index])
        stdout.flush()
        index += 1

    if '>' in string:
        index = 5
        text = ''
        while string[index] != '>':
            text += string[index]
            index += 1

        filename = ''
        index += 2
        while index < len(string):
            filename += string[index]
            index += 1

        write_to_file(text, filename)


    print('\n')


def list_dir(string):
    cm = string.split(' ')
    cm.pop(0)

    if cm in ([], None):
        cm.append('.')

    if cm[0] == '-la' and len(cm) == 1:
        cm.append('.')

    if cm[0] == '>':
        cm[0] = '.'

    if cm[0] == '-la' and len(cm) != 1 and cm[1] == '>':
        cm[1] = '.'

    dir_list = listdir(cm[0]) if '-la' not in cm else listdir(cm[1])
    other_list = []

    if '-la' not in cm:
        for i in dir_list:
            if i[0] != '.':
                other_list.append(i)

    if '-la' in cm:
        other_list = dir_list

    for i,f in enumerate(other_list):
        if (i % 4) == 0 and i != 0:
            stdout.write('\n')

        else:
            stdout.write(f'{f}  ')

    if '>' in string:
        index = 0
        while string[index] != '>':
            index += 1

        filename = ''
        index += 2
        while index < len(string):
            filename += string[index]
            index += 1

        for idx, fln in enumerate(other_list):
            write_to_file(fln, filename)

    print('\n')


def go_dir(string):
    cm = string.split(' ')
    cm.pop(0)

    chdir(cm[0])
    set_path()
    print('')


def show_path(string):
    if '>' in string:
        index = 0
        while string[index] != '>':
            index += 1

        fln = ''
        index += 2
        while index < len(string):
            fln += string[index]
            index += 1

        write_to_file(getcwd(), fln)

    print(f'{getcwd()}\n')


def delete_file(string):
    cm = string.split(' ')
    cm.pop(0)

    for filename in cm:
        remove(filename)

    print('\n')


def copy_file(string):
    cm = string.split(' ')
    cm.pop(0)

    copy(path.abspath(cm[0]), path.abspath(cm[1]))

    print('\n')


def output_file(cm, arg: None, filename):
    with open(filename, 'r') as f:
        print(f.read())

    #print('\n')


def move_file(string):
    cm = string.split(' ')
    cm.pop(0)

    move(path.abspath(cm[0]), path.abspath(cm[1]))
    print('')


def search_file(cm, search_dir, arg, name):
    dirlist = listdir(search_dir)


    while name not in dirlist:
        for d in dirlist:
            if path.isdir(d):
                df = path.join(path.abspath(d), d)
                dirlist = listdir(d)

    for n in dirlist:
        if name == n:
            print(path.join(path.abspath(df), n))

    print('')


set_path()

while True:
    if '/home/ryuvi' in current_path:
        current_path = current_path.replace('/home/ryuvi', '~')
    print(f"{Fore.MAGENTA}{current_path}{Fore.RESET}")
    command = input('▶ ')

    splitted_command = command.split(' ')
    cm = splitted_command[0]

    if cm == 'echo':
        output(command)

    elif cm == 'ls':
        list_dir(command)

    elif cm == 'cd':
        go_dir(command)

    elif cm == 'pwd':
        show_path(command)

    elif cm == 'del':
        delete_file(command)

    elif cm == 'cp':
        copy_file(command)

    elif cm == 'cat':
        output_file(cm, None, splitted_command[1])

    elif cm == 'clear':
        system('clear')

    elif cm == 'vim':
        if len(cm) == 1:
            system('nvim')
        else:
            system(f'nvim {splitted_command[1]}')

        print('')

    elif cm == 'exit':
        break

    elif cm == 'mv':
        move_file(command)

    elif cm == 'find':
        search_file(cm, splitted_command[1], splitted_command[2], splitted_command[3])

    else:
        print('Command not found on system!\n')
