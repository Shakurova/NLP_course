# -*- coding: utf-8 -*-
import csv


gr1 = ['cолнечный', 'лунный', 'бледный', 'ослепительный', 'красный', 'зеленый', 'желтый','фонарь', 'свеча', 'яркий',
		'электрический', 'луна', 'солнце']
gr2 = ['Чуть', 'ни', 'дневной', 'забрезжить']
gr3 = ['гореть', 'включать', 'включить', 'погаснуть', 'гаснуть', 'гасить', 'тушить', 'верхний', 'погасить', u'зажечь',
		'зажечься', 'зажигаться']
gr4 = ['на']
gr5 = []
gr6 = ['внутренний', 'исходить']
gr7 = ['истина', 'любовь', 'проливать', 'пролить', 'знание']
gr8 = ['мой']
gr9 = ['на', 'новый', 'старый', 'увидеть', 'появляться', 'божий']
gr10 = ['белый', 'в']
gr11 = ['высший']



all_gr = [gr1, gr2, gr3, gr4, gr5, gr6, gr7, gr8, gr9, gr10, gr11]
rows = []

with open('svet_notext.csv', 'r', encoding='utf-8') as i:

	for line in i:
		# print(line.split(';'))
		print([one.replace('\n', '') for one in line.split(';')])
		arr = [one.replace('\n', '') for one in line.split(';')]
		_arr = []
		for gr in all_gr:
			for word in arr[:2]:
				if word in gr:
					print('да')
					print(all_gr.index(gr)+1)
					_arr.append('1')
					break
				else:
					_arr.append('0')
					break
		print(arr+_arr)
		print('='*10)

		rows.append(arr+_arr)

with open('svet_keywords.csv', 'w', encoding='utf-8') as w:
	out = csv.writer(w, delimiter=',')
	out.writerows(rows)

