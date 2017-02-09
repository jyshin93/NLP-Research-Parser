from collections import defaultdict

from bs4 import Tag
from parser.general import GeneralParser
from parser.helper import get_html_tree_from_url
import re

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
        speech_list = ['Noun', 'Pronoun', 'Verb', 'Adjective', 'Adverb', 'Conjunction']
        head = ''
        headword_lang = ''
        pos = ''
        for element in page_content.children:
            if isinstance(element, Tag):
                level = self.get_heading_level(element.name)
                if level == 2:
                    headword_lang = self.get_heading_text(element)
                    head = page_heading
                elif level == 3:
                    pos = self.get_heading_text(element)
                    if pos in speech_list:
                        pos = pos
                    else:
                        pos = ''
                elif level == 4:
                    pos = self.get_heading_text(element)
                    if pos in speech_list:
                        pos = pos
                    else:
                        pos = ''
                if element.name == 'ol':
                    for li in element:
                        if li != "\n":
                            if head:
                                if pos:
                                    self.page_state.append((headword_lang, pos, head, li))
        # printing with parse <a> or <li> tags but still parenthesis is there
        for content in self.page_state:
            s = str(content[3])
            translation = re.sub('<[^>]+>', '', s)
            print (content[0], ', ', content[1], ', ', content[2], ', ', translation)
