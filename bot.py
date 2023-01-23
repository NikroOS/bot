# -*- coding: utf-8 -*-

## Подключаем библеотеки и импортируем из них функции
from vkbottle.bot import Bot, Message # Бибилеотека vkbottle
from vkbottle import Keyboard, Text, KeyboardButtonColor # Бибилеотека vkbottle
from config import token # Файл конфигурации config.py
from loguru import logger # Библеотка логов loguru (позволяет отключить дебагер стр:)
import sqlite3 # Библеотека работы с бд SQlite3
import ParseTable # Импорт скрипта с парсинга
from filejob import get_table, get_table_next_day, get_table_all # Импорт скрипта вывода расписания с парсинга
from idsgroups import id_group #Импорт ловаря групп и их id в расписании
import datetime

bot = Bot(token=token) ## Присваиваем наш токен из config.py

CHOUSEKYRS = (
		Keyboard(one_time=False, inline=True)
		.add(Text("1 курс", {"cmd": "1kyrs"}), color=KeyboardButtonColor.SECONDARY)
		.add(Text("2 курс", {"cmd": "2kyrs"}), color=KeyboardButtonColor.SECONDARY)
		.row()
		.add(Text("3 курс", {"cmd": "3kyrs"}), color=KeyboardButtonColor.SECONDARY)
		.add(Text("4 курс", {"cmd": "4kyrs"}), color=KeyboardButtonColor.SECONDARY)
		.get_json()
	)

	## Выбор групп 1 курса
CHOOSEGROUP1k = (
		Keyboard(one_time=True, inline=False)
		.add(Text("1ИБ-3", {"cmd": "1IB-3"}), color=KeyboardButtonColor.SECONDARY)
		.add(Text("1ИБ-4к", {"cmd": "1IB-4k"}), color=KeyboardButtonColor.SECONDARY)
		.add(Text("1ИКС-4", {"cmd": "1IKS-4"}), color=KeyboardButtonColor.SECONDARY)
		.row()
		.add(Text("1ИКС-5к", {"cmd": "1IKS-5k"}), color=KeyboardButtonColor.SECONDARY)
		.add(Text("1ИСПВ-4", {"cmd": "1ISPV-4"}), color=KeyboardButtonColor.SECONDARY)
		.add(Text("1ИСПВ-5к", {"cmd": "1ISPV-5k"}), color=KeyboardButtonColor.SECONDARY)
		.row()
		.add(Text("1ИСПИ-3", {"cmd": "1ISPI-3"}), color=KeyboardButtonColor.SECONDARY)
		.add(Text("1ИСПИ-4к", {"cmd": "1ISPI-4k"}), color=KeyboardButtonColor.SECONDARY)
		.add(Text("1ИСПП-16", {"cmd": "1ISPP-16"}), color=KeyboardButtonColor.SECONDARY)
		.row()
		.add(Text("1ИСПП-17", {"cmd": "1ISPP-17"}), color=KeyboardButtonColor.SECONDARY)
		.add(Text("1ИСПП-18к", {"cmd": "1ISPP-18k"}), color=KeyboardButtonColor.SECONDARY)
		.add(Text("1ИСПП-19к", {"cmd": "1ISPP-19k"}), color=KeyboardButtonColor.SECONDARY)
		.row()
		.add(Text("1ИСПП-20к", {"cmd": "1ISPP-20k"}), color=KeyboardButtonColor.SECONDARY)
		.add(Text("1ИСПП-21к", {"cmd": "1ISPP-21k"}), color=KeyboardButtonColor.SECONDARY)
		.add(Text("1ПС-6", {"cmd": "1PS-6"}), color=KeyboardButtonColor.SECONDARY)
		.row()
		.add(Text("1ССА-7", {"cmd": "1CCA-7"}), color=KeyboardButtonColor.SECONDARY)
		.add(Text("1ССА-8к", {"cmd": "1CCA-8k"}), color=KeyboardButtonColor.SECONDARY)
		.get_json()
	)

	## Выбор групп 2 курса
CHOOSEGROUP2k = (
			Keyboard(one_time=True, inline=False)
			.add(Text("2ИБ-1к", {"cmd": "2IB-1к"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("2ИБ-2к", {"cmd": "2IB-2k"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("2ИКС-2", {"cmd": "2IKS-2"}), color=KeyboardButtonColor.SECONDARY)
			.row()
			.add(Text("2ИКС-3к", {"cmd": "2IKS-3k"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("2ИСПВ-1", {"cmd": "2ISPV-1"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("2ИСПВ-2к", {"cmd": "2ISPV-2k"}), color=KeyboardButtonColor.SECONDARY)
			.row()
			.add(Text("2ИСПВ-3к", {"cmd": "2ISPV-3k"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("2ИСПИ-1", {"cmd": "2ISPI-1"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("2ИСПИ-2к", {"cmd": "2ISPI-2k"}), color=KeyboardButtonColor.SECONDARY)
			.row()
			.add(Text("2ИСПП-11", {"cmd": "2ISPP-11"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("2ИСПП-12", {"cmd": "2ISPP-12"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("2ИСПП-13к", {"cmd": "2ISPP-13k"}), color=KeyboardButtonColor.SECONDARY)
			.row()
			.add(Text("2ИСПП-14к", {"cmd": "2ISPP-14k"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("2ИСПП-15к", {"cmd": "2ISPP-15k"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("2ПС-5", {"cmd": "2PS-5"}), color=KeyboardButtonColor.SECONDARY)
			.row()
			.add(Text("2ССА-4", {"cmd": "2CCA-4"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("2ССА-5", {"cmd": "2CCA-5"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("2ССА-6к", {"cmd": "2CCA-6k"}), color=KeyboardButtonColor.SECONDARY)
			.get_json()
	)

	## Выбор групп 3 курса
CHOOSEGROUP3k = (
			Keyboard(one_time=True, inline=False)
			.add(Text("3ИКС-1", {"cmd": "3IKS-1"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("3ИС-21", {"cmd": "3IS-21"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("3ИС-22", {"cmd": "3IS-22"}), color=KeyboardButtonColor.SECONDARY)
			.row()
			.add(Text("3ИСПП-10к", {"cmd": "3ISPP-10k"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("3ИСПП-5", {"cmd": "3ISPP-5"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("3ИСПП-6", {"cmd": "3ISPP-6"}), color=KeyboardButtonColor.SECONDARY)
			.row()
			.add(Text("3ИСПП-7к", {"cmd": "3ISPP-7k"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("3ИСПП-8к", {"cmd": "3ISPP-8k"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("3ИСПП-9к", {"cmd": "3ISPP-9k"}), color=KeyboardButtonColor.SECONDARY)
			.row()
			.add(Text("3МТС-78", {"cmd": "3MTC-78"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("3ПКС-33", {"cmd": "3PKS-33"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("3ПКС-34", {"cmd": "3PKS-34"}), color=KeyboardButtonColor.SECONDARY)
			.row()
			.add(Text("3ПКС-35к", {"cmd": "3PKS-35k"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("3ПС-4", {"cmd": "3PS-4"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("3СК-69", {"cmd": "3CK-69"}), color=KeyboardButtonColor.SECONDARY)
			.row()
			.add(Text("3ССА-1к", {"cmd": "3CCA-1k"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("3ССА-2к", {"cmd": "3CCA-2k"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("3ССА-3к", {"cmd": "3CCA-3k"}), color=KeyboardButtonColor.SECONDARY)
			.get_json()
	)

	## Выбор групп 4 курса
CHOOSEGROUP4k = (
			Keyboard(one_time=True, inline=False)
			.add(Text("4ИС-18", {"cmd": "4IS-18"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("4ИС-19к", {"cmd": "4IS-19k"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("4ИС-20", {"cmd": "4IS-20"}), color=KeyboardButtonColor.SECONDARY)
			.row()
			.add(Text("4ИСПП-1к", {"cmd": "4ISPP-1k"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("4ИСПП-2к", {"cmd": "4ISPP-2k"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("4ИСПП-3к", {"cmd": "4ISPP-3k"}), color=KeyboardButtonColor.SECONDARY)
			.row()
			.add(Text("4МТС-77", {"cmd": "4MTC-77"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("4ПКС-29", {"cmd": "4PKS-29"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("4ПКС-30", {"cmd": "4PKS-30"}), color=KeyboardButtonColor.SECONDARY)
			.row()
			.add(Text("4ПКС-32к", {"cmd": "4PKS-32k"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("4СК-67/68", {"cmd": "4CK-67/68"}), color=KeyboardButtonColor.SECONDARY)
			.get_json()
	)

HELPN = (
			Keyboard(one_time=False, inline=True)
			.add(Text("!начать", {"cmd": "rasp"}), color=KeyboardButtonColor.PRIMARY)
			.get_json()
	)

HELPY = (
			Keyboard(one_time=False, inline=True)
			.add(Text("!р", {"cmd": "rasp"}), color=KeyboardButtonColor.SECONDARY)
			.add(Text("!кнопка", {"cmd": "rasp"}), color=KeyboardButtonColor.SECONDARY)
			.row()
			.add(Text("!убрать_кнопку", {"cmd": "rasp"}), color=KeyboardButtonColor.SECONDARY)
			.get_json()
	)

	## Вызвать клавиатуру с главными кнопками
MAINBUTTONS = (
			Keyboard(one_time=False, inline=False)
			.add(Text("📜 сегодня 📜", {"cmd": "rasp"}))
			.add(Text("📜 завтра 📜", {"cmd": "rasp"}), color=KeyboardButtonColor.SECONDARY)
			.row()
			.add(Text("📜 неделя 📜", {"cmd": "rasp"}), color=KeyboardButtonColor.SECONDARY)
			.get_json()
	)

	## отозвать любую клавиатуру
DISMAINBUTTONS = (
			Keyboard(one_time=True, inline=False)
			.get_json()
	)

attachment = 'video248532640_456240472'
uff = 'video179965919_456239756'

@bot.on.chat_message()
async def start_handler(message: Message):
	## Проверяем есть ли беседа в бд
	try:
		conn = sqlite3.connect('kspsutischedule.db')
		cur = conn.cursor()
		cur.execute(f"SELECT peerid FROM peers WHERE peerid = {message.peer_id}").fetchone()[0]
		have_id_in_database = '+'
		conn.commit()
		conn.close()
	except:
		have_id_in_database = '-'

## Обрезаем мусор с сообщение юзера
	message.text = message.text.replace('[club218353637|@kspsutischedule] ', '')

## Процесс регистрации
	if message.text.lower() == '!начать' and have_id_in_database == '-':
		await message.answer('Выберите курс', keyboard = CHOUSEKYRS)
	elif message.text.lower() == '1 курс' and have_id_in_database == '-':
		await message.answer('Выберите группу', keyboard = CHOOSEGROUP1k)
	elif message.text.lower() == '2 курс' and have_id_in_database == '-':
		await message.answer('Выберите группу', keyboard = CHOOSEGROUP2k)
	elif message.text.lower() == '3 курс' and have_id_in_database == '-':
		await message.answer('Выберите группу', keyboard = CHOOSEGROUP3k)
	elif message.text.lower() == '4 курс' and have_id_in_database == '-':
		await message.answer('Выберите группу', keyboard = CHOOSEGROUP4k)
	elif message.text in id_group and have_id_in_database == '-':
		conn = sqlite3.connect('kspsutischedule.db')
		cur = conn.cursor()
		sql = f"INSERT INTO peers(peerid, groups, raspid) VALUES (?, ?, ?)"
		data = (message.peer_id, message.text, id_group[message.text])
		cur.execute(sql, data)
		conn.commit()
		conn.close()
		await message.answer('╔ Успешная регистрация!\n║\n╠[👍]\n║\n╚ Все команды: !помощь', keyboard=MAINBUTTONS)
		await message.answer("Спасибо что попробовали нашего бота!", attachment=attachment)
## Процесс помощи не зарегистрированным
	elif message.text.lower() == '!помощь' and have_id_in_database == '-':
		await message.answer('╔ Вы не выбрали группу!\n║\n╠[⚠]\n║\n╚ Выбрать группу', keyboard=HELPN)

## Процесс помощи зарегистрированным
	elif message.text.lower() == '!помощь' and have_id_in_database == '+':
		await message.answer('╔ !р - получить расписание\n║\n╠[📜] !кнопка - вызвать кнопку\n║\n╚ !убрать_кнопку - отключить кнопку', keyboard=HELPY)


## Если нет в бд и просит расписание по команде:
	elif message.text == '!р' and have_id_in_database == '-':
		await message.answer('╔ Вы не выбрали группу!\n║\n╠[⚠]\n║\n╚ Выбрать группу', keyboard=HELPN)

## Если есть в бд и просит расписание по команде:
	elif message.text.lower() == '!р' and have_id_in_database == '+':
		conn = sqlite3.connect('kspsutischedule.db')
		cur = conn.cursor()
		name_group = cur.execute(f"SELECT groups FROM peers WHERE peerid = {message.peer_id}").fetchone()[0]
		url_group1 = cur.execute(f"SELECT raspid FROM peers WHERE peerid = {message.peer_id}").fetchone()[0]
		url_group = f'https://lk.ks.psuti.ru/?mn=2&obj={url_group1}'
		conn.commit()
		conn.close()
		await message.answer(get_table(name_group, url_group))

	elif message.text.lower() == '📜 неделя 📜' and have_id_in_database == '+':
		conn = sqlite3.connect('kspsutischedule.db')
		cur = conn.cursor()
		name_group = cur.execute(f"SELECT groups FROM peers WHERE peerid = {message.peer_id}").fetchone()[0]
		url_group1 = cur.execute(f"SELECT raspid FROM peers WHERE peerid = {message.peer_id}").fetchone()[0]
		url_group = f'https://lk.ks.psuti.ru/?mn=2&obj={url_group1}'
		conn.commit()
		conn.close()
		await message.answer(get_table_all(name_group, url_group))

	elif message.text.lower() == '📜 завтра 📜' and have_id_in_database == '+':
		conn = sqlite3.connect('kspsutischedule.db')
		cur = conn.cursor()
		name_group = cur.execute(f"SELECT groups FROM peers WHERE peerid = {message.peer_id}").fetchone()[0]
		url_group1 = cur.execute(f"SELECT raspid FROM peers WHERE peerid = {message.peer_id}").fetchone()[0]
		url_group = f'https://lk.ks.psuti.ru/?mn=2&obj={url_group1}'
		conn.commit()
		conn.close()
		await message.answer(get_table_next_day(name_group, url_group))

## Если есть в бд и просит расписание по кнопке:
	elif message.text.lower() == '📜 сегодня 📜' and have_id_in_database == '+':
		conn = sqlite3.connect('kspsutischedule.db')
		cur = conn.cursor()
		name_group = cur.execute(f"SELECT groups FROM peers WHERE peerid = {message.peer_id}").fetchone()[0]
		url_group1 = cur.execute(f"SELECT raspid FROM peers WHERE peerid = {message.peer_id}").fetchone()[0]
		url_group = f'https://lk.ks.psuti.ru/?mn=2&obj={url_group1}'
		conn.commit()
		conn.close()
		await message.answer(get_table(name_group, url_group))
 
## Показать главные кнопки
	elif message.text.lower() == '!клава' and have_id_in_database == '+':
		await message.answer('Клавиатура активирована', keyboard=MAINBUTTONS)
	
## Убрать все кнопки
	elif message.text.lower() == '!убрать клаву':
		await message.answer('Клавиатура деактивирована', keyboard=DISMAINBUTTONS)
	## Баг-репорт
	elif message.text.lower() == '!бот ахуеный': 
		await message.answer('нет, ты ахуенный', attachment=uff)

		## -------------------------------------------------------------- БОТ В ЛС -------------------------------------------------------------- ##

LSCHOOSE = (
    Keyboard(one_time=False, inline=False)
    .add(Text("Преподаватель", {"cmd": "rasp"}), color=KeyboardButtonColor.SECONDARY)
		.add(Text("Студент", {"cmd": "rasp"}), color=KeyboardButtonColor.SECONDARY)
    .get_json()
)

@bot.on.private_message()
async def start_handler(message: Message):
	## Проверяем есть ли беседа в бд
	try:
		conn = sqlite3.connect('kspsutischedule_user.db')
		cur = conn.cursor()
		cur.execute(f"SELECT peerid FROM peers WHERE peerid = {message.peer_id}").fetchone()[0]
		user_id_in_database = '+'
		conn.commit()
		conn.close()
	except:
		user_id_in_database = '-'
	if message.text == 'Начать' and user_id_in_database == '-':
		await message.answer(f'Здравствуйте!\n\nВы Преподаватель или Cтудент?', keyboard=LSCHOOSE)
	elif message.text.lower() == 'Преподаватель' and user_id_in_database == '-':
		await message.answer('Ваше ФИО?')
	elif message.text.lower() == 'Преподаватель' and user_id_in_database == '-':
		await message.answer('Запомнил!\nЗдесь вы можете:\n\nУзнать своё расписание\n\nНаписать в беседу студентов определённой группы')
	


## Бот будет работать вечно
bot.run_forever()