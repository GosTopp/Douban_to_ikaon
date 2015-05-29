# -*- coding: utf-8 -*-
import json
import urllib

def get_books(user_name, start=0, count=100, status='', info=[]):
    '''
    Fetch and parse the user_name's collection of books on douban.
    The maximum count douban allows is 100.
    status can be 'read', 'reading', 'wish' and ''. With '', all books are fetched.
    A list of dicts is returned.
    '''
    book_url = "https://api.douban.com//v2/book/user/{0}/collections?start={1}&status={2}&count={3}"
    url = book_url.format(user_name, start, status, count)
    response = urllib.urlopen(url);
    data = json.loads(response.read())
    collection = data['collections']
    if collection:
        for book in collection:
            tmp = {}
            tmp['status'] = book['status']
            tmp['title'] = book['book'].get('title', '')
            try:
                tmp['rating'] = book['rating'].get('value', '')
            except KeyError:
                tmp['rating'] = ''
            tmp['author_list'] = book['book'].get('author', []) # A list, still in Unicode.
            tmp['pubdate'] = book['book'].get('pubdate', '')
            tmp['comment'] = book.get('comment','')
            info.append(tmp)
        start = start + count
        info = get_books(user_name, start, count, status, info)
    else:
        return info
    return info

def ikaon_print(book_info):
    '''
    Print book_info in ikaon.
    book_info is a dict in the list returned by get_books().
    '''
    title = book_info['title'].encode("utf-8")
    author_list = []
    for author in book_info['author_list']:
        author_list.append(author.encode("utf-8"))
    author = ', '.join(author_list)
    pubdate = book_info['pubdate'].encode("utf-8")
    rating = book_info['rating'].encode("utf-8")
    comment = book_info['comment'].encode("utf-8")
    status = book_info['status'].encode("utf-8")
    statuses = {'read': '读过', 'reading': '在读', 'wish': '想读'}
    ikaon_book = '*{status}#《{title}》'
    if author and pubdate:
        ikaon_book += '({author}，{pubdate}）'
    elif author:
        ikaon_book += '({author}）'
    elif pubdate:
        ikaon_book += '({pubdate}）'

    if rating or comment:
        ikaon_book += '/'
    if rating:
        ikaon_book += '/+{rating}'
    if comment:
        ikaon_book += '/({comment})'
    return ikaon_book.format(status=statuses[status], title=title, author=author, pubdate=pubdate, rating=rating, comment=comment)

user_name = 'tcya'
info = get_books(user_name)
for book in info:
    print ikaon_print(book)

