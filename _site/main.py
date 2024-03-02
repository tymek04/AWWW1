import requests
import re
from bs4 import BeautifulSoup
from googlesearch import search


def get_languages():
    result = requests.get('https://www.tiobe.com/tiobe-index/')
    soup = BeautifulSoup(result.text, 'html.parser')
    elements = soup.select('#top20 > tbody > tr > td')
    rows = []
    for i in range(len(elements)):
        if i % 7 == 4:
            rows.append([])
        if i % 7 >= 4:
            rows[len(rows)-1].append(elements[i].text)
    return rows

def get_more_info(language):
    urls = search(language+' programming language wikipedia', lang='en', num_results=30)
    wikipedia = ""
    for x in urls:
        if 'wikipedia' in x and 'simple.wikipedia' not in x and 'en' in x:
            if language != 'C#' or 'C_Sharp' in x:
                wikipedia = x
                break
    result = requests.get(wikipedia)
    soup = BeautifulSoup(result.text, 'html.parser')
    info = soup.select('#mw-content-text > div.mw-content-ltr')[0].contents
    info = list(filter(lambda x: x.name in ['p', 'h2', 'ol', 'ul'], info))
    ind = 0
    for x in info:
        if x.name == 'p' and ('class' not in x.attrs.keys() or x['class'] != ['mw-empty-elt']):
            break
        ind += 1
    basic_info = ""
    while ind < len(info) and info[ind].name != 'h2':
        if info[ind].name == 'p':
            basic_info += info[ind].text+'\n'
        elif info[ind].name == 'ul':
            for li in info[ind].children:
                if li.name == 'li':
                    basic_info += '- '+li.text+'\n'
        elif info[ind].name == 'ol':
            cur = 0
            for i in range(len(info[ind].contents)):
                if info[ind].contents[i].name == 'li':
                    basic_info += str(cur+1)+'. '+info[ind].contents[i].text+'\n'
                    cur += 1

        ind += 1
    basic_info = re.sub('\[[0-9]\]', '', basic_info)
    basic_info = re.sub('\[[0-9][0-9]\]', '', basic_info)
    basic_info = re.sub('\[update\]', '', basic_info)
    basic_info = re.sub('\[[a-z]\]', '', basic_info)
    return (wikipedia, basic_info[:-1])

def create_markdown(position, language):
    markdown_text = '# '+language+'\n'+'## Basic info\n'
    info = get_more_info(language)
    markdown_text += info[1]
    markdown_text += '\n## More info\n'
    markdown_text += '[Link to the wikipedia page]('+info[0]+')'
    with open('./language'+str(position)+'.md', 'w') as f:
        f.write(markdown_text)

def create_markdowns(languages):
    for i in range(20):
        create_markdown(i+1, languages[i][0])

def create_list_page(languages):
    markdown_text = '# Top 20 programming languages\n'
    for i in range(20):
        markdown_text += '## '+str(i+1)+'. '+languages[i][0]+'\n'
        markdown_text += '- Popularity: '+languages[i][1]+'\n'
        markdown_text += '- Popuarity change in last month: '+languages[i][2]+'\n'
        markdown_text += '- [More information](./language'+str(i+1)+'.md)\n'
    with open('./ranking''.md', 'w') as f:
        f.write(markdown_text)

def create_main_page():
    markdown_text = '# Programming languages\n'
    markdown_text += 'A programming language is a system of notation for writingcomputer programs.\n\n'
    markdown_text += 'A programming language is described by its syntax (form) and semantics (meaning). '
    markdown_text += 'It gets its basis from formal languages.\n\n'
    markdown_text += 'A language usually has at least one implementation in the form of a compiler '
    markdown_text += 'or interpreter, allowing programs written in the language to be executed.\n\n'
    markdown_text += 'Programming language theory is the subfield of computer science that studies '
    markdown_text += 'the design, implementation, analysis, chracterization, and classification '
    markdown_text += 'of programming languages.\n\n'
    markdown_text += '[Here You can find the ranking of top 20 programming languages](./ranking.md)'
    with open('./main_page''.md', 'w') as f:
        f.write(markdown_text)

if __name__ == '__main__':
    create_main_page()
