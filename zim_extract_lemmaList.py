# -*- coding: utf-8 -*-
import codecs
import re
import pandas as pd
from collections import Counter
# import cPickle

from zim1 import ZimFile


#regular expressions
lempat = r'<h1.*?>(.*?)</h1>'
locpat1 = r'</h2>.*?</h2>'
locpat2 = r'</h2>.*?</body>'
pospat = r'>(.*?)</h3>'

language = u'English' #CHANGE
ln = language


fout = codecs.open('English_lemma_list.txt','wb','utf-8') #CHANGE

article_tuples = ZimFile(open('wiktionary_en_all_nopic_2016-12.zim','rb')).article_tuples()

#count is actually a unique idx for every table, could get large but who cares
count = 0 
for at in article_tuples:
	body = at[2].decode('utf-8')
	if language + u'</h2>' in body:
		print(body)
		break;
		#this is probably a Spanish lemma
		match = re.search(lempat,body,flags=re.U|re.DOTALL)
		if match:
			lemma = match.group(1)
			#try to find the language block
			match = re.search(ln+locpat1,body,flags=re.U|re.DOTALL)
			if not match:
				match = re.search(ln+locpat2,body,flags=re.U|re.DOTALL)
			if match:
				text = match.group()
				matches = re.findall(pospat,text)
				for x in matches:
					fout.write(lemma + '\t' + x + '\n')
				if lemma == "Amur":
					html = codecs.open("Amur.html", 'wb', 'utf-8')
					html.write(body)
					html.close()
					break;

#clean up
fout.close()


