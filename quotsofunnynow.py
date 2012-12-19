#!/usr/bin/env python

import urllib2
import time

def get_random_page(url='http://uncyclopedia.wikia.com/wiki/Special:Random/'):
    return urllib2.urlopen(url).readlines()

def add_title(line, title):
    if ' on ' not in line:
        return line.strip() + ' on ' + title

def clean_author(line, title):
    if '<' not in line and '>' not in line:
        return add_title(line, title)
    if not line:
        return add_title('~ Unknown', title)
    return add_title('~ '+line.rsplit('title="')[1].rsplit('"')[0], title)

def get_quote(line, title=''):
    spans = line.rsplit('<span')
    quote = ''
    author = ''

    for span in spans:
        if 'quoteline' in span:
            quote = span.rsplit('>')[1].rsplit('</span')[0]
        elif 'quoteauthor' in span:
            author = span.rsplit('>')[1].rsplit('</span')[0]

    if '<' in quote or '>' in quote:
        return None, None

    try:
        return quote, clean_author(author,title)
    except Exception as ex:
        return None, None

def get_quotes(lines=[]):
    quotes = []
    title=''

    for line in lines:
        if '<title>' in line:
            title = get_title(line)
        if 'quoteline' in line:
            q, a = get_quote(line, title)
            if not q or not a:
                continue
            quotes.append((q,a))

    return quotes

def get_title(line):
    if '<title>' not in line:
        return ''
    return line.rsplit('<title>')[1].rsplit(' -')[0]

def get_me_all_quotes(filename='quotes.txt'):
    import os

    lines = []

    if not os.path.exists(filename):
        try:
            f = open(filename, 'w')
        except IOError as ex:
            print 'Error:' + str(ex)
            return
    else:
        try:
            f = open(filename, 'r')
            lines = f.readlines()
            f.close()
            f = open(filename, 'a')
        except IOError as ex:
            print 'Error: '+str(ex)
            return

    while True:
        time.sleep(2)
        qs = get_quotes(get_random_page())

        if not qs:
            continue

        string = ''

        for q, a in qs:
            if q + '\t' + a + "\n" in lines:
                continue
            print q + '\t' + a + "\n"
            f.write(q + '\t' + a + "\n")
            f.flush()

    f.close()

def get_me_a_quote():
    while(True):
        qs = get_quotes(get_random_page())

        if not qs:
            continue

        string = ''

        string += qs[0][0] + "\n"
        string += '\t\t\t\t' +  qs[0][1]

        return string
        break

def enter_the_flying_man(quote):
    flying_man = r'''
                              """
                              i i'
                              \~;\
                               \; \
                                \ ;\    ====
                                 \ ;\  ==== \
                            __,--';;;\-' (  0
                      __,--';;; ;;; ;;\      >
               __,--'\\ ;;; ;;; ;;; ;;;\--__<
        _ _,--' __,--'\\  ;;; __,~~' \ ;\
       (_)|_,--' __,--'\\;,~~'        \ ;\
       |(_)|_,--'       ~~             \; \
       || |                             \ ;\
        |_/                              !~!,
                                     .---"""---.
                                     |         |
                                     | P E O S |
                                     |         |
                                     `---------'

    '''

    print flying_man + quote


def load_random_quote(filename='quotes.txt'):
    try:
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()
    except IOError as ex:
        print 'Error: Could not open file '+filename+'. Reason: '+str(ex)
        return

    import random
    random.seed(random.random())
    line = lines[random.randint(0, len(lines)-1)].rsplit('\t')
    quote = line[0]
    author = line[1]
    enter_the_flying_man(quote + '\n\t\t\t' + author)


if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Random quotes from uncyclopedia.')
    parser.add_argument('-u', '--update', metavar='FILENAME', help='update quotes and use FILENAME.')
    parser.add_argument('-r', '--realtime', action='store_true', default=False, help='print a quote directly from uncyclopedia.')

    args = parser.parse_args()

    if args.realtime:
        enter_the_flying_man(get_me_a_quote())
    elif args.update:
        get_me_all_quotes(args.update)
    else:
        load_random_quote()
