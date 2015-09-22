#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Clicktionary - A CLI wiktionary client. """

from __future__ import division, print_function
from argparse import ArgumentParser
from requests import get
from bs4 import BeautifulSoup
from bs4 import NavigableString
from bs4 import Comment


DESC = 'Clicktionary - A (buggy) CLI wiktionary client.'
DICT_HELP = ('the language of the dictionary, as the two letter language code'
             ' (example: en)')
LANG_HELP = 'the language of the word to lookup, written out (example: German)'
WORD_HELP = 'the word to look up in the dictionary (example: Kater)'


def main():

    parser = ArgumentParser(description=DESC, )
    parser.add_argument('dict', help=DICT_HELP, )
    parser.add_argument('lang', help=LANG_HELP)
    parser.add_argument('word', help=WORD_HELP)

    args = parser.parse_args()

    data = get('http://' + args.dict + '.wiktionary.org/wiki/' + args.word)
    soup = BeautifulSoup(data.content, 'html.parser')
    content = ''

    target = soup.find(id=args.lang)

    current = target.parent.next_sibling
    counter = 1
    while (current.name != 'h2'):
        if isinstance(current, Comment):
            break
        if current.name == 'ol':
            counter = 1
        if isinstance(current, NavigableString):
            content += current
        else:
            for tag in current:
                if tag.name == 'li':
                    if tag.parent.name == 'ol':
                        content += str(counter) + '. '
                        counter += 1
                    else:
                        content += '* '
                if isinstance(tag, NavigableString):
                    content += tag
                else:
                    for string in tag.strings:
                        content += string

        current = current.next_sibling

    # cleanup
    content = content.replace('\n\n\n\n', '\n')
    content = content.replace('\n\n\n', '\n')
    content = content.replace('[edit]', ' ' + '-' * 50)

    print(content)

    return 0

if __name__ == '__main__':
    main()
