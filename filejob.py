import datetime
import ParseTable
from datetime import date


def open_table(group, url):
    if datetime.datetime.today().weekday() == 6:
        d1 = date(2020, 1, 4)
        d2 = date.today()
        result = (d2 - d1).days // 7
        ParseTable.ParseWebTables(group, f"{url}&wk={result+1}")
    else:
        ParseTable.ParseWebTables(group, f"{url}")
    f = open(f'table/{group}.txt', encoding='utf-8')
    file_content = f.read()
    symbol_delete = ['[', ']', '\'', '\\t', '\\r', '\\n', 'None', ',']
    for x in symbol_delete:
        file_content = file_content.replace(x, '')
    f.close()
    return file_content


weekday = ['Понедельник', 'Вторник', "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]


def get_week_day(now_date):
    return weekday[now_date]


def edit_table_all(group, url_group):
    all_text = open_table(group, url_group)
    for day in weekday:
        if all_text.find(day) != -1:
            index = all_text.find(day)
            all_text = all_text[:index] + '\n' + all_text[index:]
    return all_text


def get_table(group, url_group):
    now_day = datetime.datetime.today().weekday()
    table = open_table(group, url_group)
    if table.find(get_week_day(now_day)) == -1:
        return "сегодня отдыхаете молодые"
    first_symbol = table.find(get_week_day(now_day))
    try:
        next_day = now_day + 1
        last_symbol = table.find(get_week_day(next_day))
        return table[first_symbol:last_symbol]
    except:
        try:
            return table[first_symbol:]
        except:
            return table[:]


def get_table_next_day(group , url_group):
    now_day = datetime.datetime.today().weekday() + 1
    table = open_table(group, url_group)
    if now_day == 7:
        now_day = 0
    if table.find(get_week_day(now_day)) == -1:
        return "завтра отдыхаете молодые"
    first_symbol = table.find(get_week_day(now_day))
    try:
        next_day = now_day + 1
        last_symbol = table.find(get_week_day(next_day))
        return table[first_symbol:last_symbol]
    except:
        try:
            return table[first_symbol:]
        except:
            return edit_table_all(group, url_group)[:]


def get_table_all(group, url_group):
    return edit_table_all(group, url_group)[:]