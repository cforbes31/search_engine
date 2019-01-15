from pprint import pprint
import requests
from string import punctuation

def get_page(url):
    page = requests.get(url).text
    return page

# content = requests.get("https://udacity.github.io/cs101x/index.html").text
# print(content)

def scrap_links(content):
    linklist = []
    endquote = 0
    while content.find('href=',endquote+1) != -1:
        startlink = content.find('href=', endquote+1)
        startquote = content.find('"',startlink)
        endquote = content.find('"',startquote+1)
        url = content[startquote+1:endquote]
        if url not in linklist and (url[:8] == 'https://' or url[:7] == 'http://'):
            linklist.append(url)
    return linklist

# pprint(scrap_links(get_page("https://udacity.github.io/cs101x/index.html")))

def add_to_index(index, keyword, url):
    if index.get(keyword) == None:
        index[keyword] = [url]
    else:
        if url not in index[keyword]:
            index[keyword] = index[keyword].append(url)

def add_page_to_index(index, url, content):
    # words = content.split()
    # for word in words:
    #     if "<" not in word and ">" not in word and "{" not in word and "}" not in word and "." not in word and ";" not in word and ":" not in word and "!" not in word and '"' not in word and "#" not in word and "$" not in word and "%" not in word and "(" not in word and ")" not in word and "&" not in word and "'" not in word and "|" not in word and "," not in word and "[" not in word and "]" not in word and "-" not in word and "^" not in word and "_" not in word and "/" not in word:
    #         add_to_index(index, word, url)
    words = content.split()
    state = True
    for word in words:
        for char in punctuation:
            if char in word:
                state = False
                break
            state = True
        if state == True:
            add_to_index(index, word, url)
        # if "<" not in word and ">" not in word and "{" not in word and "}" not in word and "." not in word and ";" not in word and ":" not in word and "!" not in word and '"' not in word and "#" not in word and "$" not in word and "%" not in word and "(" not in word and ")" not in word and "&" not in word and "'" not in word and "|" not in word and "," not in word and "[" not in word and "]" not in word and "-" not in word and "^" not in word and "_" not in word and "/" not in word:
            # add_to_index(index, word, url)

def combine(a,b):
    c = a[:]
    for item in b:
        if item not in a:
            c.append(item)
    return c

print(combine([1,2,3],[4,5,6]))

def build_index(seed):
    crawled = []
    tocrawl = [seed]
    index = {}
    while tocrawl and len(crawled) < 20:
        # scrap_links(get_page(seed))
        url = tocrawl.pop()
        # print(url)
        if url not in crawled:
            content = get_page(url)
            # print(content)
            add_page_to_index(index, url, content)
            tocrawl = combine(tocrawl, scrap_links(content))
            # print(tocrawl)
            print(scrap_links(content))
            crawled.append(url)
    # print(len(crawled))
    # print(len(tocrawl))
    return index

def lookup(keyword,index):
    return index.get(keyword)

## testcases

# testIndex = build_index("https://udacity.github.io/cs101x/index.html")
testIndex2 = build_index("https://en.wikipedia.org/wiki/Main_Page")

# pprint(testIndex)
pprint(testIndex2)



print(lookup("Google",testIndex2))
