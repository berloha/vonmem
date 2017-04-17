#!/usr/bin/python
#coding: utf8

import sys
from datetime import datetime  
from datetime import timedelta 
import base

Dni = [u'Пн', u'Вт', u'Cр', u'Чт', u'Пт', u'Сб', u'Вс']
data_format = '%d.%m.%Y'
date = datetime.strptime('27.06.1915', data_format)
if len(sys.argv) > 1 : date = datetime.strptime(sys.argv[1], data_format)

def SD(d) :
	return d.strftime('%d.%m.%Y')

def Paskha(y) :
	a = y % 19
	b = y % 4
	c = y % 7
	d = (19 * a + 15) % 30 
	d += (2 * b + 4 * c + 6 * d + 6) % 7
	if d < 9 :
		return datetime(y, 3, 22 + d) + timedelta(days=13)
	else :
		return datetime(y, 4, d - 9) + timedelta(days=13)

den_mes = date.day
mes = date.month
den_sedm = date.weekday()
print u"Дата: " + SD(date) + ", " + Dni[den_sedm]

god1 = date.year
if (date - Paskha(god1)).days < 0 :	god1 -= 1

PS1 = Paskha(god1)
PS2 = Paskha(god1 + 1)
Sedm_po_Paskhe = (date - PS1).days / 7 + 1
Sedm_do_Paskhi = (PS2 - date).days / 7

Troica = PS1 + timedelta(weeks = 7)
Vozdv = datetime(god1, 9, 27)
Kresch = datetime(god1, 1, 19)
Sedm_po_Troici = (date - Troica).days / 7 + 1

glas = (Sedm_po_Paskhe - 1) % 8
if glas == 0 : glas = 8


MrFr = PS2 - timedelta(weeks = 10)

print u"Предыдущая Пасха: " + SD(PS1)
print u"Троица: " + SD(Troica)
print u"Следующая Пасха: " + SD(PS2)
print u"Неделя о мытаре и фарисее: " + SD(MrFr)
print u"Седмиц по Пасхе: " + str(Sedm_po_Paskhe)
print u"Седмиц до Пасхи: " + str(Sedm_do_Paskhi)
print u"Седмиц по Пятидесятнице: " + str(Sedm_po_Troici)
print u"Глас седмицы: " + str(glas)

#print Troica
#print u"Период: " + str(Period)

Luka = Vozdv
while True :
	Luka += timedelta(days = 1)      #"понедельник, следующий за этой Неделей, и есть искомый понедельник – начало Лукиных седмиц"
	if (Luka.weekday() == 6) : break #Вс 
Luka += timedelta(days = 1) #Пн
sdvig_Luka = 18 - (Luka - Troica).days / 7 - 1
Matf = Luka - timedelta(days = 3)
if Vozdv.weekday() == 4 : #Пт
	Matf -= timedelta(days = 1)		#"пяток по Воздвижении Креста указан здесь в качестве крайнего срока"
Mf_Ots = Troica + timedelta(weeks = 17, days = 1) #Пн  
Lk_Ots = Luka + timedelta(weeks = 16) #Пн
Lk_Ots_sdvig = (MrFr - Lk_Ots + timedelta(days = 1)).days / 7

#Лк: 35 из 30-й 29.01.2016

print u"Конец Матфеева ряда: " + SD(Matf)
#if Mf_Ots > 0 :
#	print u"Начало Воздвиженской отступки: " + SD(Matf - timedelta(days = Mf_Ots))	
if Mf_Ots < Matf :
	print u"Начало Воздвиженской отступки: " + SD(Mf_Ots)	

print u"Начало Лукина ряда: " + SD(Luka) #в Пн после Недели по Воздвижении
print u"Сдвиг седмиц Лукина ряда: " + str(sdvig_Luka) #в Пн после Недели по Воздвижении
print u"Начало Богоявленской отступки: " + SD(Lk_Ots)	

print Lk_Ots_sdvig  

def In() :
	print "SDP" + str(Sedm_po_Paskhe) + " " + Dni[den_sedm]
	print base.Raspisanie_Triodi(1, Sedm_po_Paskhe, den_sedm, Sedm_po_Troici)


def Mf() :
	sedm = Sedm_po_Troici
	if sedm > 17 :
		sedm = 10 + sedm - 17  #30.09.2015 - зачала Мф взяты из 11-й седмицы

	print "SDT" + str(sedm) + " " + Dni[den_sedm]
	print base.Raspisanie_Triodi(2, sedm, den_sedm, Sedm_po_Troici)


def Lk() :
	sedm = Sedm_po_Troici + sdvig_Luka
	if date >= Lk_Ots :
		sedm -= Lk_Ots_sdvig
		if Lk_Ots_sdvig == 5 :    #[30, 31, 17, 32, 33]
			if sedm == 29 or sedm == 30 : sedm += 1
			elif sedm == 31 : sedm = 17 

	print "SDT" + str(sedm) + " " + Dni[den_sedm]
	print base.Raspisanie_Triodi(3, sedm, den_sedm, Sedm_po_Troici)

def Tr() :
	sedm = (date - MrFr).days / 7 + 1
	print "SDV" + str(sedm) + " " + Dni[den_sedm]
	print base.Raspisanie_Triodi(4, sedm, den_sedm, Sedm_po_Troici)


if date < Troica : 		#До Пятидесятницы
	In()
elif date < Luka : 		#до Лукина ряда
	Mf()
elif date < MrFr : 		#до Недели о мытаре и фарисее
	Lk()
else :			   		#10-ть седмиц до Пасхи
	Tr()

print base.Raspisanie_Minei(date)