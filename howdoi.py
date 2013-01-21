#!/usr/bin/env python

##################################################
#
# howdoi - a code search tool.
# written by Benjamin Gleitzman (gleitz@mit.edu)
# inspired by Rich Jones (rich@anomos.info)
#
##################################################

import argparse
import re
import requests
import urllib
import stackexchange
site = stackexchange.Site(stackexchange.StackOverflow)
site.be_inclusive()
import json

from pyquery import PyQuery as pq

S_KEY = 'PYAS3ZkXgxblnJFaB1BAmA(('
GOOGLE_SEARCH_URL = "https://www.google.com/search?q=site:stackoverflow.com%20{0}"
DUCK_SEARCH_URL = "http://duckduckgo.com/html?q=site%3Astackoverflow.com%20{0}"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17"

site = stackexchange.Site(stackexchange.StackOverflow)
site.be_inclusive()
# so = stackexchange.Site(stackexchange.StackOverflow, S_KEY)
# so.impose_throttling = True
# so.throttle_stop = False


def get_result(url):
    print "URL :: " + url
    return requests.get(url, headers={'User-Agent': USER_AGENT}).text

def get_stack_result(q_id):
    print str(q_id)
    question = site.question(q_id) 
    answers = question.answers[0].body
    if len(answers) < 1:
        return ''
    return answers[0].body



def is_question(link):
    return re.search('questions/\d+/', link)


def get_google_links(query):
    url = GOOGLE_SEARCH_URL.format(urllib.quote(query))
    result = get_result(url)
    html = pq(result)
    return [a.attrib['href'] for a in html('.l')]


def get_duck_links(query):
    url = DUCK_SEARCH_URL.format(urllib.quote(query))
    result = get_result(url)
    html = pq(result)
    links = [l.find('a').attrib['href'] for l in html('.links_main')]


def get_link_at_pos(links, pos):
    pos = int(pos) - 1
    for link in links:
        if is_question(link):
            if pos == 0:
                break
            else:
                pos = pos - 1
                continue
    return link


def get_instructions(args):
    links = get_google_links(args['query'])
    
    if not links:
        return None
    
    text = None
    
    for link in links:
        #link = get_link_at_pos(links, args['pos'])
        if args.get('link'):
            return link
        print link
        if "stackoverflow.com" in link:
            arr = link.split('/')
            first_answer = pq(get_stack_result(int(arr[4])))
        else:
            link = link + '?answertab=votes'
            page = get_result(link)
            html = pq(page)
            first_answer = html('.answer').eq(0)
        
        instructions = first_answer.find('pre') or first_answer.find('code')
        print instructions
        if args['all'] or not instructions:
            text = first_answer.find('.post-text').eq(0).text()
        else:
            text = instructions.eq(0).text()
        
        if text:
            break

    return text


def howdoi(args):
    args['query'] = ' '.join(args['query']).replace('?', '')
    instructions = get_instructions(args) or 'Sorry, couldn\'t find any help with that topic'
    print instructions
    return instructions


def command_line_runner():
    parser = argparse.ArgumentParser(description='code search tool')
    parser.add_argument('query', metavar='QUERY', type=str, nargs=argparse.REMAINDER,
                        help='the question to answer')
    parser.add_argument('-p','--pos', help='select answer in specified position (default: 1)', default=1)
    parser.add_argument('-a','--all', help='display the full text of the answer',
                        action='store_true')
    parser.add_argument('-l','--link', help='display only the answer link',
                        action='store_true')
    args = vars(parser.parse_args())
    howdoi(args)

if __name__ == '__main__':
    command_line_runner()
    