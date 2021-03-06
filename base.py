#!/usr/bin/python
#coding: utf8
import re
import sys
import copy
from datetime import datetime  
from datetime import timedelta 

Dni = ['PN', 'VT', 'SR', 'CT', 'PT', 'SB', 'ND']
Minea = {}
Triod = {}


def Parse_M(text, god1, PS1) :
	mes = 0
	den = None
	slujba = None
	dt = None
	ng = datetime(god1, 1, 1)
	dD = (god1 - god1 % 100)/100 - (god1 - god1 % 400)/400 - 2
	res = iter(re.findall(r'[A-Z\-+][A-Z0-9]+|"[^"\n]+"', text))
	for t in res :   #new match
		t = t.encode('utf-8')
		if dt == datetime(2016, 1, 2) : print t
		t2 = t[0:2]
		if t2 == 'DN' :
			dt = datetime(day = int(t[2:]), month = mes, year = god1) + timedelta(days=dD)		
			if dt < PS1 :
				dt = datetime(day = int(t[2:]), month = mes, year = god1 + 1) + timedelta(days=dD)						
			den = Minea.setdefault("%i.%i" % (dt.day, dt.month), {})
			slujba = den.setdefault('LT', {})

		elif t2 == 'MS' :
			mes = int(t[2:])
		elif t2 in ['LT', 'VR', 'UT', 'ML', 'CH'] :					
			den = Minea.setdefault("%i.%i" % (dt.day, dt.month), {})
			slujba = den.setdefault(t, {})
		elif t2 in ['MF','MK','LK','IN'] :
			slujba.setdefault('EV', []).append(t)
		elif t2 == 'ZA' :						
			slujba.setdefault('AP', []).append(t)
		if t[0] == '-' or t[0] == '+' :
			if t[1:] in Dni :
				while Dni[dt.weekday()] != t[1:] :
					if t[0] == '-' :
						dt -= timedelta(days = 1)
					else :
						dt += timedelta(days = 1)				

			den = Minea.setdefault("%i.%i" % (dt.day, dt.month), {})
			slujba = den.setdefault('LT', {})			
		elif t2 == 'IZ' or t2 == 'ZS':
			den.setdefault('ADD', []).append(t)			
		else :
			pass


def Parse_T(text) :
	sedmica = None
	den = None
	slujba = None
	res = re.findall(r'[A-Z][A-Z0-9]+|"[^"]+"', text) 
	for t in res :   #new match
		t = t.encode('utf-8')

		t2 = t[0:2]
		if t2 == 'SD' :		
			sedmica = Triod.setdefault(t, {})
			den = None
			slujba = None
		elif t2 in Dni :
			den = sedmica.setdefault(t, {})
			slujba = None
		elif t2 in ['LT', 'VR', 'UT', 'ML', 'CH'] :
			slujba = den.setdefault(t, {})
		elif t2 == 'ZA' :
			if slujba == None : slujba = den.setdefault('LT', {})
			slujba.setdefault('AP', []).append(t)
		elif t2 in ['MF','MK','LK','IN', 'VE'] :
			if slujba == None : slujba = den.setdefault('LT', {})
			slujba.setdefault('EV', []).append(t)
		elif t2 == 'IZ' or t2 == 'ZS':
			den.setdefault('ADD', []).append(t)			
		else :
			pass
	#		print t.decode('utf-8')

def Perestanovka(src, dst, mask, replace) :

	if type(src) is not dict : return
	if type(dst) is not dict : 
		dst = {} 

	for k in src.keys() :
		if type(src[k]) is list :
			flag = 0
			if mask :
				if k in mask :	
					flag = 1
			else :
				flag = 1

			if flag :
				if replace :	
					dst[k] = src[k]
				else :
					if type(dst.get(k)) is not list :
						dst[k] = src[k]
					else :
						dst[k] += src[k]

		if type(src[k]) is dict :
			if type(dst.get(k)) is not dict :				
				dst[k] = {}
			Perestanovka(src[k], dst[k], mask, replace)

def Load_M(fname, god1, PS1) :
	f = open(fname)	
	m = Parse_M(f.read().decode('utf8'), god1, PS1)
	f.close()
	return m

def Load_T(fname) :
	f = open(fname)	
	m = Parse_T(f.read().decode('utf8'))
	f.close()
	return m

def Init(god1, PS1) :
	Load_M('ev_minea', god1, PS1)
	Load_M('ap_minea', god1, PS1)
	Load_T('ev_triod')
	Load_T('ap_triod')

def Raspisanie_Minei(date) :
	return Minea.get("%i.%i" % (date.day, date.month))

def Raspisanie_Triodi(per, sdm, den, sedm_po_Troici) :
	VEV = ['MF116', 'MK70', 'MK71', 'LK112', 'LK113', 'LK114', 'IN63', 'IN64', 'IN65', 'IN66', 'IN67']
	res = None
	sedm = None
	if per == 1 :
		sedm = Triod.get('SDP' + str(sdm))
	elif per == 2 or per == 3 :
		sedm = Triod.get('SDT' + str(sdm))
	elif per == 4 :		
		sedm = Triod.get('SDV' + str(sdm))

	if sedm :
		dn = sedm.get(Dni[den])

		if dn :
			res = copy.deepcopy(dn)
	
			if per == 2 or per == 3 :
				if sdm != sedm_po_Troici :
#					print '>>>', sedm_po_Troici
					sdm_ap = Triod.get('SDT' + str(sedm_po_Troici))
					if sdm_ap :
						dn_ap = sdm_ap.get(Dni[den])
						Perestanovka(dn_ap, res, ['AP'], 1)


			if per > 1 and Dni[den] == 'ND' :
				ut = res.get('UT')		
				if ut :
					ev = ut.get('EV')			
					if ev :
						if 'VEV' in ev :
							i = ev.index('VEV')
							ev.pop(i)
							evn = (sedm_po_Troici - 2) % 11
							ev.insert(i, VEV[evn])

	return res

def GetFilesByMask(root, mask) :
    res = []
    tree = os.walk(root) 
    for path, dirs, files in tree :
       for fname in files :
           if fnmatch.fnmatch(fname, mask) :
               res.append(os.path.join(path, fname))
    return res 

#Load('ap_ot_paskhi.ld')
#Load('ev_triod')
#Load('ap_minea.ld')
#Load('ev_minea')

#print Minea
if __name__ == "__main__" :         
#	Minea = Load_M('ev_minea', 2016)
#	print Minea
		
	Load_T('ev_triod')
	print Triod
	
#	print Raspisanie_Minei(d)
#	print Raspisanie_Paskhalii(4, 2, 2)