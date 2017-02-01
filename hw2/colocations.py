# -*- coding: utf-8 -*-

import nltk
from nltk.collocations import *
from nltk.metrics.spearman import *

my_top_words = ['суд удовлетворить иск', 'суд принять решение', 'суд отклонить иск', 'cуд огласить приговор',
                'суд возобновить слушание', 'суд наложить арест', 'суд вынести приговор', 'суд выслушать приговор',
                'суд исполнить решение', 'суд обжаловать приговор', 'суд отложить слушание', 'суд отменить решение']


def parse_file(file='court-V-N.csv'):
    documents = []
    with open(file) as collocations:
        for line in collocations:
            line_splited = line.split()
            line = ' '.join(line_splited)
            line = line.lower().replace(',', '').replace('\n', '').replace('  ', ' ')
            line_arr = line.split()
            documents.append(line_arr)     # массив массивов на вход в nltk

    return documents


def method1():
    """ Этот метод выводит 12 топ-триграмм с их частотностями в убывающем подярке """
    print('Первый метод выводит 12 топ-триграмм с их частотностями в убывающем подярке')
    arr = []
    finder = TrigramCollocationFinder.from_documents(documents)
    print('Совпавшие триграммы: ')
    for _i in sorted(finder.ngram_fd.items(), key=lambda t: (-t[1], t[0]))[:12]:
        result = str(_i[0][0]) + ' ' + str(_i[0][1]) + ' ' + str(_i[0][2])
        arr.append(result)
        check(result)
    spearman(arr)


def method2():
    """ Этот метод берет 12 самых частотных триграмм """
    print('Второй метод берет 12 самых частотных триграмм.')
    trigram_measures = nltk.collocations.TrigramAssocMeasures()
    arr = []
    finder = TrigramCollocationFinder.from_documents(documents)
    print('Совпавшие триграммы: ')
    for _i in sorted(finder.nbest(trigram_measures.raw_freq, 12)):
        result = str(_i[0]) + ' ' + str(_i[1]) + ' ' + str(_i[2])
        arr.append(result)
        check(result)
    spearman(arr[::-1])


# def other_methods():
#     bigram_measures = nltk.collocations.BigramAssocMeasures()
#     trigram_measures = nltk.collocations.TrigramAssocMeasures()
#
#     # топ-10 биграм
#     finder = BigramCollocationFinder.from_documents(documents)
#     for _i in finder.nbest(bigram_measures.pmi, 10):
#         print(str(_i[0]) + ' ' + str(_i[1]))
#
#     print('=' * 10)
#
#     # топ-5 биграм
#     for _i in finder.nbest(bigram_measures.pmi, 5):
#         print(str(_i[0]) + ' ' + str(_i[1]))
#
#     print('=' * 10)
#
#     # фильтр: игнорировать биграммы, которые встретились реже трех раз
#     finder.apply_freq_filter(3)
#     for _i in finder.nbest(bigram_measures.pmi, 10):
#         print(str(_i[0]) + ' ' + str(_i[1]))
#
#     print('=' * 10)
#
#     ignored_words = nltk.corpus.stopwords.words('russian')
#     finder = BigramCollocationFinder.from_documents(documents)
#     finder.apply_word_filter(lambda w: len(w) < 3 or w.lower() in ignored_words)
#     for _i in finder.nbest(bigram_measures.likelihood_ratio, 10):
#         print(str(_i[0]) + ' ' + str(_i[1]))
#
#
#     print('=' * 10)
#     arr = []
#     ignored_words = nltk.corpus.stopwords.words('russian')
#     finder = TrigramCollocationFinder.from_documents(documents)
#     finder.apply_word_filter(lambda w: len(w) < 3 or w.lower() in ignored_words)
#     finder.apply_freq_filter(10)
#     for _i in finder.nbest(trigram_measures.likelihood_ratio, 10):
#         result = str(_i[0]) + ' ' + str(_i[1]) + ' ' + str(_i[2])
#         arr.append(result)
#         check(result)
#     spearman(arr)
#
#     print('=' * 10)
#     arr = []
#     finder = TrigramCollocationFinder.from_documents(documents)
#     print(len(finder.score_ngrams(trigram_measures.raw_freq)))
#     for _i in sorted(finder.above_score(trigram_measures.raw_freq, 1.0 / len(tuple(nltk.trigrams(documents)))))[:12]:
#         result = str(_i[0]) + ' ' + str(_i[1]) + ' ' + str(_i[2])
#         arr.append(result)
#         check(arr)
#     spearman(arr)
#
#     print('=' * 10)
#     arr = []
#     k = []
#     finder = TrigramCollocationFinder.from_documents(documents)
#     finder.apply_freq_filter(10)
#     arr = []
#     for _i in finder.score_ngrams(trigram_measures.raw_freq):
#         k.append((str(_i[0][0]) + ' ' + str(_i[0][1]) + ' ' + str(_i[0][2]), int(_i[1])))
#         result = str(_i[0][0]) + ' ' + str(_i[0][1]) + ' ' + str(_i[0][2])
#         arr.append(result)
#         check(result)
#     spearman2(k)

def check(result):
    """ Совпавшие """
    if result in my_top_words:
        print('- ' + result)


def spearman(result):
    """ Мера качества – ранговый коэффициент корреляции Спирмена между золотым стандартом и
    моим автоматически сгенерируемым списком """
    print('Золотой стандарт:', list(ranks_from_sequence(my_top_words)))
    print('Полученный список:', list(ranks_from_sequence(result)))
    print('Коэффициент корреляции Спирмана равен %0.1f' % spearman_correlation(list(ranks_from_sequence(my_top_words)),
                                                                               list(ranks_from_sequence(result))))

# def spearman2(result):
#     """ Мера качества – ранговый коэффициент корреляции Спирмена между золотым стандартом и
#     моим автоматически сгенерируемым списком """
#     print('Золотой стандарт:', list(ranks_from_sequence(my_top_words)))
#     print('Полученный список:', result)
#     # print('%0.1f' % spearman_correlation(ranks_from_sequence(my_top_words), ranks_from_sequence(result)))
#     print('Коэффициент корреляции Спирмана равен %0.1f' % spearman_correlation(list(ranks_from_sequence(my_top_words)),
#                                                                                result))

if __name__ == '__main__':
    documents = parse_file()
    method1()
    print('=' * 30)
    method2()
    print('=' * 30)
    print('Метод 2 работает лучше  ')

