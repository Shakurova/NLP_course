# -*- coding: utf-8 -*-

from nltk.wsd import lesk
import codecs
from nltk.corpus import wordnet


if __name__ == '__main__':

	# 1 Все значения (синсеты) для лексемы plant
	print u'Все значения (синсеты) для лексемы plant:'
	for ss in wordnet.synsets('plant'):
		print(ss, ss.definition())

	print '=' * 30

	# 2 Определения для лексемы plant в значении (а) "завод" и в значении (b) "растение"
	set1 = wordnet.synset('plant.n.01')  # завод
	set2 = wordnet.synset('plant.n.02')  # растение
	print u'Plant в значении "завод":', set1.definition()
	print u'Plant в значении "растение":', set2.definition()

	print '=' * 30

	# 3 Два произвольных контекста для слова plant в значениях (a) "завод" и (b) "растение"
	sent1 = "Workers at the plant noticed a discrepancy in the amount of material being reprocessed that enters pipes that lead to a set of centrifuges and the amount of material actually arriving at the centrifuges"
	sent2 = "Found nearly 30 miles east of San Francisco Park aged 35 identified the small pink flowering plant said to resemble baby's breath during a routine visit to the mountain"
	sent1_splited = sent1.split()
	sent2_splited = sent2.split()
	print u'Значение в первом предложении:', lesk(sent1_splited, 'plant').definition()
	print u'Значение в первом предложении:', lesk(sent2_splited, 'plant').definition()

	print '=' * 30

	# 4 Гиперонимы для значения (a) и гиперонимы для значения (b)
	print u'Гипероним для plant(завод):', set1.hypernyms()
	print u'Гипероним для plant(растение):', set2.hypernyms()

	print '=' * 30

	# 5.1 Min расстояние между значением plant(завод) и значениями лексемы industry

	# завод
	industry_arr = []
	print u'Все значения (синсеты) для лексемы industry:'
	for ss in wordnet.synsets('industry'):
		print(ss, ss.definition())
		industry_arr.append(ss)   # все синсеты industry

	arr_industry = [set1.path_similarity(_s) for _s in industry_arr]
	print arr_industry  	# расстояние между plant(завод) и значениями industry
	print u'Min расстояние между plant(завод) и значениями industry:', min(arr_industry)

	arr_industry2 = [set2.path_similarity(_s) for _s in industry_arr]
	print arr_industry2		# расстояние между plant(растение) и значениями industry

	print '=' * 30

	# 5.2 Min расстояние между значением plant(растение) и значениями лексемы leaf

	# растение
	leaf_arr = []
	print u'Все значения (синсеты) для лексемы leaf:'
	for ss in wordnet.synsets('leaf'):
		print(ss, ss.definition())
		leaf_arr.append(ss)    # все синсеты leaf

	arr_leaf = [set2.path_similarity(_s) for _s in leaf_arr]
	print arr_leaf			 # расстояние между plant(растение) и значениями leaf
	print u'Min расстояние между plant(растение) и значениями leaf:', min(arr_leaf)

	arr_leaf1 = [set1.path_similarity(_s) for _s in leaf_arr]
	print arr_leaf1			# расстояние между plant(завод) и значениями leaf

	print min(min(arr_industry), min(arr_leaf1))
	print min(min(arr_industry2), min(arr_leaf))

	# d(plant: "растение", rattlesnake's master) и d(organism, whole)
	whole = wordnet.synsets('whole', 'n')[0]
	organism = wordnet.synsets('organism', 'n')[0]
	print wordnet.path_similarity(whole, organism)
