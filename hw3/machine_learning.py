# -*- coding: utf-8 -*-

import codecs
import csv
import numpy
import numpy as np
from nltk.tokenize import TreebankWordTokenizer
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(color_codes=True)

tokenizer = TreebankWordTokenizer()
vowels = [u'а', u'о', u'э', u'и', u'у', u'ы', u'е', u'ё', u'ю', u'я']


def text_cleaner(text_text):
	""" Нормализация текста, преобразование текста твита в склеенные пробелом леммы.
	На вход предложение, на выход список слов """

	RUS_LETTERS = u'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
	ALL_LETTERS_SET = set(list(RUS_LETTERS))  # Может удалять английские символы? #

	# 1. Все буквы в нижний регистр
	text_text = text_text.lower()

	# 2. Удаление всех небукв
	letters_only = ''
	for _c in text_text:
		if _c in ALL_LETTERS_SET:
			letters_only += _c
		else:
			letters_only += ' '

	# 3. Заменяем множественные пробелы
	while '  ' in letters_only:
		letters_only = letters_only.replace('  ', ' ')

	# 4. Токенизация
	word_list = tokenizer.tokenize(letters_only)

	return word_list


def cleaner(text_text):
	""" Нормализация текста, преобразование текста твита в склеенные пробелом леммы.
	На вход предложение, на выход строка """

	RUS_LETTERS = u'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
	ALL_LETTERS_SET = set(list(RUS_LETTERS))  # Может удалять английские символы? #

	# 1. Все буквы в нижний регистр
	text_text = text_text.lower()

	# 2. Удаление всех небукв
	letters_only = ''
	for _c in text_text:
		if _c in ALL_LETTERS_SET:
			letters_only += _c
		else:
			letters_only += ' '

	# 3. Заменяем множественные пробелы
	while '  ' in letters_only:
		letters_only = letters_only.replace('  ', ' ')

	return letters_only


def median(l):
	""" Вычисление медианы """
	half = len(l) // 2
	l.sort()
	if not len(l) % 2:
		return (l[half - 1] + l[half]) / 2.0
	return l[half]


def open_file(file):
	""" Сплитизация """

	sentances = []

	with codecs.open(file, 'r', encoding='utf8') as f:
		a = f.read()
		for _s in a.split('.'):
			sentances.append(_s)		# все предложения
	return sentances


def vectoriser(_s):
	""" Функция делает из предложения вектор из 5 признаков. """
	vector = []
	# print(_s)

	# 1. Длина предложения в буквах
	letters = []
	for l in list(cleaner(_s)):
		if l != ' ':
			letters.append(l)
	# print u'Длина предложения в буквах:',  len(letters)
	vector.append(len(letters))

	# 2. Число различных букв
	letters = set()
	for l in list(cleaner(_s)):
		letters.add(l)
	# print u'Число различных букв в предложении:',  len(letters)
	vector.append(len(letters))

	# 3. Число гласных в предложении
	v = 0  					# сколько глаcных в предложении
	for l in list(cleaner(_s)):
		if l in vowels:
			v += 1
	# print u'Число гласных в предложении:',  v
	vector.append(v)

	# 4. Медиана числа букв в слове
	word_letters_arr = []  	# массив числа букв в слове
	for _w in text_cleaner(_s):
		word_letters_arr.append(len(_w))
	try:
		# print u'Медиана числа букв в слове:',  median(word_letters_arr)
		vector.append(median(word_letters_arr))
	except:
		pass

	# 5. Медиана гласных в слове
	word_letters_arr = []  # массив числа гласных в слове
	for _w in text_cleaner(_s):
		v = 0
		for _l in list(_w):
			if _l in vowels:
				v += 1
		word_letters_arr.append(v)
	try:
		# print u'Медиана гласных в слове:',  median(word_letters_arr)
		vector.append(median(word_letters_arr))
	except:
		pass

	return vector


def unison_shuffled_copies(a, b):
	assert len(a) == len(b)
	p = numpy.random.permutation(len(a))
	return a[p], b[p]


if __name__ == '__main__':

	s1 = u'Но - женщина - в ответ на обожанье Она лукавит, гордости полна, И отвечает страсти, столь открытой, Упрямыми ударами копыта.'
	s2 = u'Он не таит ни скуки, ни вражды.'
	a1 = u'Успехи ее в свете были больше, чем обеих ее старших сестер, и больше, чем даже ожидала княгиня.'
	a2 = u'Облонский уже не раз испытывал это случающееся после обеда крайнее раздвоение вместо сближения и знал, что надо делать в этих случаях.'

	# Создание обучающей выборки
	X_train = []
	Y_train = []

	# print u'Анна Каренина Толстого:'
	sentances_a_train = open_file('anna_train.txt')
	for _s in sentances_a_train:
		vector = vectoriser(_s)
		# print(vector)
		if len(vector) == 5:
			X_train.append(vector)
			Y_train.append('a')

	# print('='*60)

	# print u'Сонеты Шекспира:'
	sentances_s_train = open_file('sonets_train.txt')
	for _s in sentances_s_train:
		vector = vectoriser(_s)
		# print(vector)
		if len(vector) == 5:
			X_train.append(vector)
			Y_train.append('s')

	X_train = np.array(X_train)
	Y_train = np.array(Y_train)

	# Синхронная рандомизация обучающих массивов
	X_train_2, Y_train_2 = unison_shuffled_copies(X_train, Y_train)

	# Создание тестовой выборки

	X_test = []
	Y_test = []
	all_sentances = []

	sentances_a_test = open_file('anna_test.txt')
	for _s in sentances_a_test:
		vector = vectoriser(_s)
		# print(vector)
		if len(vector) == 5:
			X_test.append(vector)
			Y_test.append('a')
			_s = _s.replace('\r\n', ' ')
			_s = _s.replace('\n', ' ')
			_s = _s.replace('\t', ' ')
			all_sentances.append(_s.encode('utf-8'))

	sentances_s_test = open_file('sonets_test.txt')
	for _s in sentances_s_test:
		vector = vectoriser(_s)
		# print(vector)
		if len(vector) == 5:
			X_test.append(vector)
			Y_test.append('s')
			_s = _s.replace('\r\n', ' ')
			_s = _s.replace('\n', ' ')
			_s = _s.replace('\t', ' ')
			all_sentances.append(_s.encode('utf-8'))

	X_test = np.array(X_test)
	Y_test = np.array(Y_test)
	all_sentances = np.array(all_sentances)

	# Обучение и тестирование модели GaussianNB
	# GaussianNB
	clf = GaussianNB()
	clf.fit(X_train_2, Y_train_2)
	Y_predicted = clf.predict(X_test)
	print classification_report(Y_test, Y_predicted)
	print u'The accuracy score is {:.2%}'.format(accuracy_score(Y_test, Y_predicted))

	# Запись результов в файл
	output = pd.DataFrame(data={'Class': Y_predicted, 'Real': Y_test,
								'Text': all_sentances})
	output.to_csv('result.csv', index=False, sep='\t', quoting=csv.QUOTE_MINIMAL)

	# Вывод ошибочных примеров
	print u'Примеры, где классификатор ошибается: '
	print u'Текст "', s1, u'" относится к классу', clf.predict(vectoriser(s1)), u', правильный класс  ["s"]'
	print u'Текст "', s2, u'" относится к классу', clf.predict(vectoriser(s2)), u', правильный класс  ["s"]'
	print u'Текст "', a1, u'" относится к классу', clf.predict(vectoriser(a1)), u', правильный класс  ["a"]'
	print u'Текст "', a2, u'" относится к классу', clf.predict(vectoriser(a2)), u', правильный класс  ["a"]'
