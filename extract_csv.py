import os
import sys
import csv

class National_Parse():
	def __init__(self, path_text):
		self.csvPath = path_text
		self.national_list = ['Spanish', 'German', 'French', 'Italian', 'Portuguese']
		self.national_lang = {}
		self.fieldnames = ['headword_lang', 'head', 'pos', 'additional_pos', 'trans(no paren)', 'trans(with paren)', 'original_html']
		for nation in self.national_list:
			self.national_lang[nation] = []
		self.parse()		

	#parsing main 5 head words into dictionary
	def parse(self):
		with open(self.csvPath, 'r') as r:
			for csv_file in r:
				csv_file = csv_file.split('\n')[0]
				with open(csv_file, 'r') as f:
					#import DictReader for csv
					reader = csv.DictReader(f)
					for row in reader:
						headword = row['headword_lang']
						if headword in self.national_list:
							self.national_lang[headword].append(row)
		self.extract_csv()

	#making into csv file
	def extract_csv(self):
		#for each headerwords
		for headword, national_lang in self.national_lang.items():
			#write header
			write_file = open("All_" + headword + '.csv', 'w+b')
			writer = csv.DictWriter(write_file, fieldnames=self.fieldnames)
			writer.writeheader()
			#write elements
			for element in national_lang:
				writer.writerow(element)

def main():
	csv_parser = National_Parse('path_text.txt')

if __name__ == '__main__':
	main()