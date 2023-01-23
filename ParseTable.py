from lxml import etree
import urllib.request


def indices(lst, element):
    result = []
    offset = -1
    while True:
        try:
            offset = lst.index(element, offset + 1)
        except ValueError:
            return result
        result.append(offset)


def ParseWebTables(name_group, url):
    site = url

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}


    request = urllib.request.Request(site, headers=hdr)
    web = urllib.request.urlopen(request)
    s = web.read()
    html = etree.HTML(s)

    ## Get all 'tr'
    tr_nodes = html.xpath('//table/tr')

    ## Get text from rest all 'tr'
    td_content = [[td.text for td in tr.xpath('td')] for tr in tr_nodes[1:]]

    WeekDayInWeb = html.xpath('//td[@bgcolor="3481A6"]')

    weekDayArrayInWeb = [[td.text for td in tr.xpath('h3')] for tr in WeekDayInWeb[1:]]

    weekDayAll = ['Понедельник', 'Вторник', "Среда", "Четверг", "Пятница", "Суббота"]

    cabinet = html.xpath('//*/text()')
    cabinet_array = []
    for content in cabinet:
        if content == '\n' :
                continue
        if content[:7] == 'Кабинет':
            cabinet_array.append(content)

    hueta = []
    #
    for day in weekDayArrayInWeb:
        if day == []:
            continue
        temp = str(*day)
        for x in weekDayAll:
            if temp.find(x) != -1:
                hueta.append('[' + temp + ']')

    new_hueta = []

    for content in td_content:
        if len(content) == 7:
            for x in content:
                if content.count(x) > 1 :
                    content.remove(x)
            new_hueta.append(content)
    new_hueta.pop(0)

    count = indices(new_hueta, [None,None,None])
    for x in range(len(indices(new_hueta, [None,None,None]))):
        position = count[x]
        new_hueta[position] = hueta[x]

    with open(f"table/{name_group}.txt", "w", encoding="utf-8") as file:
        step = 0
        for x in new_hueta:
            if x in hueta:
                print(x, sep='\n', file=file)
            else:
                print(f"{x}\n{cabinet_array[step]}", sep="\n", file=file)
                step += 1
