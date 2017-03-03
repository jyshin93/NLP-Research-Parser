from collections import defaultdict

from bs4 import Tag, BeautifulSoup
from parser.general import GeneralParser
from parser.helper import get_html_tree_from_url
import re
import csv

class EnParser(GeneralParser):
    tested_url = [
        "https://en.wiktionary.org/wiki/canto",
    ]

    def __init__(self):
        super(EnParser, self).__init__()
        self.edition = 'en'
        self.page_state = []

    # override the parent class method

    def parse_page(self, soup):
        """ Yield for each language section
        """
        # try:
        #     page_heading = soup.find('div', class_='mw-body-content').previous_sibling.text
        # except AttributeError as e:
        #     print(soup)
        page_content = soup.find('div', id='mw-content-text')
        page_heading = None
        element = soup.find('div', class_='mw-body-content') or page_content
        while not page_heading:
            if element is None:
                return None
            element = element.previous_sibling
            if isinstance(element, Tag):
                page_heading = element.text
        speech_list = ['Noun', 'Pronoun', 'Verb', 'Adjective', 'Adverb', 'Conjunction', 'Proper noun']
        head = ''
        headword_lang = ''
        pos = ''
        additional_pos = ''
        count = 0
        # if page_heading.startswith('A'):
        for element in page_content.children:
            if isinstance(element, Tag):
                if count == 100:
                    break;
                #only words that are starting with 'A'
                if re.match("^[A]",head):
                    count += 1
                    level = self.get_heading_level(element.name)
                    if level == 2:
                        headword_lang = self.get_heading_text(element)
                        head = page_heading
                        additional_pos = ''
                    elif level == 3:
                        pos = self.get_heading_text(element)
                        additional_pos = ''
                    elif level == 4:
                        pos = self.get_heading_text(element)                
                        additional_pos = ''

                    if level == 5:
                        additional_pos = ''
                        pos = self.get_heading_text(element)

                    if element.name == 'p':
                        if pos == 'Pronunciation':
                            self.page_state.append((headword_lang, pos, additional_pos, head, element))
                        elif 'Etymology' in pos:
                            self.page_state.append((headword_lang, pos, additional_pos, head, element))
                        else:
                            if pos in speech_list:
                                string = self.remove_tag(element)
                                additional_pos = string[len(head):]

                    if element.name == 'ol':
                        if head:
                            if pos:
                                self.parse_ol(headword_lang, pos, additional_pos, head, element)
                    if element.name == 'ul':
                        if head:
                            if pos:
                                self.parse_ul(headword_lang, pos, additional_pos, head, element)
                                  
        # parsing without parenthesis
        self.csv_writer()



    def csv_writer(self):
        with open('wiktionary_en_parse.csv', 'w') as csvfile:
            fieldnames = ['headword_lang', 'head', 'pos', 'additional_pos', 'trans(no paren)', 'trans(with paren)', 'original_html']
            writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
            writer.writeheader()
            for content in self.page_state:
                s = str(content[4])
                translation = self.remove_tag(s)
                output = self.remove_parenthesis(translation)
                #eliminate long explanation (but not final yet, still has some bugs)
                # if '.' in output:
                #     output = output[0 : output.index('.')]
                # else:
                #     output = output
                if len(output) > 0:
                    if output[0] == ' ':
                        output = output[1:]
                if content[1] == 'Noun' or content[1] == 'Verb' or content[1] == 'Proper Noun':
                    if output[:2] == 'a ':
                        output = output[2:]
                    elif output[:3] == 'an ':
                        output = output[3:]
                    elif output[:3] == 'to ':
                        output = output[3:]
                if content[1] != 'See also':
                    writer.writerow({'headword_lang' : content[0], 'head' : content[3], 'pos' : content[1], 'additional_pos' : content[2],
                      'trans(no paren)' : output, 'trans(with paren)' : translation, 'original_html' : s})

    def parse_ol(self, headword_lang, pos, additional_pos, head, element):
        for li in element:
            if li != "\n":
                # li_soup = BeautifulSoup(str(li), 'html.parser')
                # all_soup = li_soup.find_all('a')
                # trans = ''
                # if len(all_soup) > 0:
                #     trans = all_soup
                self.page_state.append((headword_lang, pos, additional_pos, head, li))

    def parse_ul(self, headword_lang, pos, additional_pos, head, element):
        if pos != 'Anagrams' and pos != 'Descendants':
            tag_list = []
            for li in element:
                if li != '\n':
                    tag_list.append(li)
            tag = ', '.join(str(x) for x in tag_list)
            self.page_state.append((headword_lang, pos, additional_pos, head, tag))

    def remove_tag(self, string):
        return re.sub('<[^>]+>', '', str(string))

    def remove_parenthesis(self, string):
        return re.sub(r'\([^)]*\)', '', string)
