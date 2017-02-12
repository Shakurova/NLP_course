# -*- coding: utf-8 -*-

import codecs


def open_file(file):
	""" Сплитизация """
	sentances = []

	with codecs.open(file, 'r', encoding='utf8') as f:
		a = f.read()
		for _s in a.split('.'):
			sentances.append(_s)		# все предложения
	return sentances


def split_sentances(file, sentances):
	""" Сплитизация """

	with codecs.open(file[:-4] + '_test.txt', 'w', encoding='utf8') as w_test:
		with codecs.open(file[:-4] + '_train.txt', 'w', encoding='utf8') as w_train:
			length = len(sentances)
			print(length)
			print int(length/6)
			print length - int(length/6)

			# for line in sentances[int(length/6):]:
			for line in sentances[:984]:
				w_train.write(line + '.\n')
			# for line in sentances[:-(length - int(length/6))]:
			for line in sentances[984:1180]:
				w_test.write(line + '.\n')

if __name__ == '__main__':
	sentances = open_file('anna.txt')
	split_sentances('anna.txt', sentances)
	sentances = open_file('sonets.txt')
	split_sentances('sonets.txt', sentances)

