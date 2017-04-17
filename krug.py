#!/usr/bin/python
#coding: utf8

import sys
from datetime import datetime  
from datetime import timedelta 
import base

Dni = [u'Пн', u'Вт', u'Cр', u'Чт', u'Пт', u'Сб', u'Вс']
data_format = '%d.%m.%Y'
date = datetime.strptime('24.12.2017', data_format)
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

god = date.year
god1 = god
if (date - Paskha(god1)).days < 0 :	god1 -= 1
PS1 = Paskha(god1)
PS2 = Paskha(god1 + 1)
MrFr = PS2 - timedelta(weeks = 10)
Troica = PS1 + timedelta(weeks = 7)
Vozdv = datetime(god1, 9, 27)
#Kresch = datetime(god1, 1, 19)
Luka = Vozdv
while True :
	Luka += timedelta(days = 1)      #"понедельник, следующий за этой Неделей, и есть искомый понедельник – начало Лукиных седмиц"
	if (Luka.weekday() == 6) : break #Вс 
Luka += timedelta(days = 1) #Пн
Sdvig_Luka = 18 - (Luka - Troica).days / 7 - 1
Matf = Luka - timedelta(days = 3)
if Vozdv.weekday() == 4 : #Пт
	Matf -= timedelta(days = 1)		#"пяток по Воздвижении Креста указан здесь в качестве крайнего срока"
Mf_Ots = Troica + timedelta(weeks = 17, days = 1) #Пн  
Lk_Ots = Luka + timedelta(weeks = 16) #Пн
Lk_Ots_sdvig = (MrFr - Lk_Ots + timedelta(days = 1)).days / 7
print u"Предыдущая Пасха: " + SD(PS1)
print u"Троица: " + SD(Troica)
print u"Следующая Пасха: " + SD(PS2)
print u"Неделя о мытаре и фарисее: " + SD(MrFr)
print u"Конец Матфеева ряда: " + SD(Matf)
if Mf_Ots < Matf :
	print u"Начало Воздвиженской отступки: " + SD(Mf_Ots)	
print u"Начало Лукина ряда: " + SD(Luka) #в Пн после Недели по Воздвижении #Лк: 35 из 30-й 29.01.2016
print u"Сдвиг седмиц Лукина ряда: " + str(Sdvig_Luka) #в Пн после Недели по Воздвижении
print u"Начало Богоявленской отступки: " + SD(Lk_Ots)	
#print Lk_Ots_sdvig  

Sedm_Troici = (date - Troica).days / 7 + 1
Sedm_Paskhe = (date - PS1).days / 7 + 1
Sedm_do_Paskhi = (PS2 - date).days / 7
glas = (Sedm_Paskhe - 1) % 8
if glas == 0 : glas = 8

print u"Седмиц по Пасхе: " + str(Sedm_Paskhe)
print u"Седмиц до Пасхи: " + str(Sedm_do_Paskhi)
print u"Седмиц по Пятидесятнице: " + str(Sedm_Troici)
print u"Глас седмицы: " + str(glas)

def In(sedm_Ps, den_sedm) :
	return base.Raspisanie_Triodi(1, sedm_Ps, den_sedm, 0)

def Mf(sedm_Tr, den_sedm) :
	sedm = sedm_Tr
	if sedm > 17 :
		sedm = 10 + sedm - 17  #30.09.2015 - зачала Мф взяты из 11-й седмицы

	return base.Raspisanie_Triodi(2, sedm, den_sedm, sedm_Tr)

def Lk(sedm_Tr, den_sedm) :
	sedm = sedm_Tr + Sdvig_Luka
	if date >= Lk_Ots :
		sedm -= Lk_Ots_sdvig
		if Lk_Ots_sdvig == 5 :    #[30, 31, 17, 32, 33]
			if sedm == 29 or sedm == 30 : sedm += 1
			elif sedm == 31 : sedm = 17 

	return base.Raspisanie_Triodi(3, sedm, den_sedm, sedm_Tr)

def Tr(sedm_Tr, den_sedm) :
	sedm = (date - MrFr).days / 7 + 1
	return base.Raspisanie_Triodi(4, sedm, den_sedm, sedm_Tr)

def Get_TM(dt) :
	den_sedm = dt.weekday()
	sedm_Tr = (dt - Troica).days / 7 + 1
	sedm_Ps = (dt - PS1).days / 7 + 1
	glas = (sedm_Ps - 1) % 8
	if glas == 0 : glas = 8

	tr = None
	mn = None
	if date < Troica : 		#До Пятидесятницы
		tr = In(sedm_Ps, den_sedm)
	elif date < Luka : 		#до Лукина ряда
		tr = Mf(sedm_Tr, den_sedm)
	elif date < MrFr : 		#до Недели о мытаре и фарисее
		tr = Lk(sedm_Tr, den_sedm)
	else :			   		#10-ть седмиц до Пасхи
		tr = Tr(sedm_Tr, den_sedm)		
	mn = base.Raspisanie_Minei(dt)
	return (tr, mn)

base.Init(god1, PS1)
dt = PS1
Krug = {}

while dt < PS2 :	

#	print SD(date) 
#	print "\ttriod:" + str(tr)
#	print "\tminea:" + str(mn)
	(tr, mn) = Get_TM(dt)
	Krug[SD(dt)] = {}
	Krug[SD(dt)]['Tr'] = tr
	Krug[SD(dt)]['Mn'] = mn	
	dt += timedelta(days = 1)

print Krug[SD(date)]

ned_28_Tr = Troica + timedelta(weeks = 28)
ned_29_Tr = Troica + timedelta(weeks = 29)
ned_praotec = datetime(god1 + 1, 1, 7)
while True :
	ned_praotec -= timedelta(days = 1)      
	if (ned_praotec.weekday() == 6) : break #первое Вс до Рождества 
while True :
	ned_praotec -= timedelta(days = 1)      
	if (ned_praotec.weekday() == 6) : break #второе Вс до Рождества

print SD(ned_28_Tr)
print SD(ned_29_Tr)
print SD(ned_praotec)
#print Get_TM(date)


def Process(dst, src, mask, replace) :
	for k in src.keys() :
		if type(src[k]) is list :
			flag = 0
			if mask :
				if k in mask :	
					flag = 1
			else :
				flag = 1

			if flag :
				if type(dst.get(k)) is not list :
					dst[k] = []
				if replace :	
					dst[k] = src[k]
				else :
					dst[k] += src[k]

		if type(src[k]) is dict :
			if type(dst.get(k)) is not dict :				
				dst[k] = {}
			Process(dst[k], src[k], mask, replace)




src = Krug[SD(date)]['Tr']
dst = Krug[SD(date)]['Mn']
print src
print dst
mask = []
Process(dst, src, mask, 0)
print src
print dst
