# -*- conding: utf-8 -*-

import os
import requests
from bs4 import BeautifulSoup
import re
import selenium as se
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


LIST_EXCLUDE = ['isName', 'mode', 'cols', 'typeins', 'fn', 'url', 'thumb', 'yellowBox', 'clickId', 'mobileMode',
				'svg', 'statHeaders', 'answerColIdx', 'isTablet', 'recommendedTypeins', 'moderate', 'whatkind',
				'private', 'preview', 'ext', 'customType', 'rating', 'searchlevel', 'triggers', 'nominations',
				'subscribeScreen', 'dotX', 'dotY', 'path', 'svgHeight', 'svgWidth', 'svgHiddenPaths', 
				'missingDotsTextShow', 'missingDotsTextHide', 'hint', 'image', 'display', 'answerOrder',
				'numRandom', 'sortOrder', 'tableOrder', 'x'] #we don't want this stuff in our answers

dic_languages = {'fr':{'link':'fr/', 'login':'Connexion'}, 
			'en':{'link':'', 'login':'Login'}, 
			'it':{'link':'it/', 'login':'Login'}, 
			'es':{'link':'es/', 'login':'Conéctate'}, 
			'de':{'link':'de/', 'login':'Anmelden'}, 
			'nl':{'link':'nl/', 'login':'Log in'}, 
			'pl':{'link':'pl/', 'login':'Zaloguj'}, 
			'pt':{'link':'pt/', 'login':'Logar'}, 
			'fi':{'link':'fi/', 'login':'Kirjaudu sisään'}}


def shit_to_list(browser, my_list):
	'''Transforms a list with a lot of useless things into a more readable list'''

	new_list = []
	n = len(my_list)
	i = 0

	while i<n-1: 

		elem = my_list[i].replace(',',"").replace("\"",'') #Replacing ugly characters by nothing
		elem.replace('\\\\u00e9', 'é') #Pretty sure this part is useless
		elem.replace('\\\\u00e0', 'à')


		if elem in LIST_EXCLUDE: #excluding some stuff we don't want 
			i+=1
			continue

		new_list.append(elem)

		i+=1


	return new_list

def get_answers(browser, quizz_link):


	r = requests.get(quizz_link) 
	page_content = r.content

	soup = BeautifulSoup(page_content, 'html.parser')
	soup.script.encode("utf-8")


	scripts = soup.find_all('script', type='text/javascript') #Answers are un a script tag 
	var_reponses = scripts[0]

	script_text = str(list(var_reponses)[0]).replace('var _page = ', '') 
	index_reponses = script_text.find('answers')
	string_reponses = script_text[index_reponses-1:].replace('<br \/>', '')#getting rid of strings and characters we don't want
	s = string_reponses.encode(encoding='UTF-8',errors='strict') #pretty sure this part is useless too

	pattern = ',"[-A-Za-z0-9\s \\\ \{\}]+"|\{[-A-Za-z0-9\s \\\]+\}'#using regular expressions to find the answers
																	

	raw_answers = re.findall(pattern, string_reponses) #finding answers


	answers = shit_to_list(browser, raw_answers)#creating the list of answers

	return answers

def get_links(browser):
	#all_quizzs = browser.find_element_by_xpath('//*[@id="inner-page"]/div[3]/div/div[1]/div/div[3]/div[1]/div[4]') #use this to find untaken quizzes
	all_quizzs = browser.find_element_by_xpath('/html/body/div/div/div[2]/div[3]/div/div[1]/div/div[3]/div[1]/div[2]') #use this to find all quizzes

	all_quizzs.click()

	quizzs_table = browser.find_element_by_tag_name('tbody') 
	quizz_link_elements = quizzs_table.find_elements_by_tag_name('a') #getting links' <a> 
	quizz_links = []

	for link in quizz_link_elements :
		l = link.get_property("href") #getting links
		quizz_links.append(l)

	return quizz_links

def complete_quizz(browser,link):

	browser.get(link)

	start_button = browser.find_element_by_id('start-button') #finding the start button
	start_button.click()

	answers = get_answers(browser, link) #getting the answers

	input_box = browser.find_element_by_id('txt-answer-box')

	for answer in answers:
		answer.replace('\\\\', '\\').replace('\\u00e9', 'é')
		answer.replace('\\\\', '\\').replace('\\u00e0', 'à')
		answer.replace('\\\\', '\\').replace('\\u00e8', 'è').replace('}','')
		answer.replace('\\\\', '\\').replace('\\u00ea', 'è').replace('{','') #once again, not sure this is usefull
		input_box.send_keys(answer)
		input_box.clear()

	abandon_button = browser.find_element_by_xpath('/html/body/div/div/div[2]/div[3]/div/div[1]/div/div[2]/div[5]/div/div[1]/div[1]/div[2]')
	abandon_button.click() #abandoning when all the answers were submitted

def complete_all(browser, links):

	
	size = len(links)

	for link in links: #going through all the links to solve the quizzes
		try : 
			complete_quizz(browser, link)
		except : 
			pass

	return failed_quizzs

def solve_for_language(browser):

	links = get_links(browser)

	complete_all(browser, links) #solving all the quizzes for all the languages


# -------- Errors --------------------------------

class LanguageError(Exception):


    def __init__(self, language, message=" is not valid"):
        self.salary = salary
        self.message = str(language)+message
        super().__init__(self.message)


# ------------------------------------------------


class BotPunk:

	def __init__(self, username, password, PATH=''):

		self.PATH = PATH #The path to your chrome driver

		self.browser = None

		self.username = username
		self.password = password
		


	def connexion(self, lg_depart):

		self.browser = webdriver.Chrome(self.PATH)
		self.browser.maximize_window() #For maximizing window
		self.browser.implicitly_wait(1) #gives an implicit wait for 1 seconds


		user_home_page = 'https://www.jetpunk.com/'+dic_languages[lg_depart]['link']+'user-stats'#user's home page where we'll get get the 
																					 		#links to all the quizzes
		self.browser.get(user_home_page)

		connexion = self.browser.find_element_by_link_text(dic_languages[lg_depart]['login']) 
		connexion.click()

		inputs_div = self.browser.find_elements_by_class_name('row') #finding rows that contain the login inputs

		username_input = None
		password_input = None

		list_inputs = []

		for elem in inputs_div :
				input = elem.find_elements_by_tag_name('input') 
				if input == [] :
					pass
				else :
					list_inputs.append(input) #finds the input fields where the username and the password need to be put

		username_input = list_inputs[0][0]
		password_input = list_inputs[1][0]

		username_input.send_keys(self.username)
		password_input.send_keys(self.password)

		div_login_button = self.browser.find_element_by_xpath('//*[@id="login-modal"]/div/div[2]/div[3]')
		login_button = div_login_button.find_element_by_tag_name('button')
		login_button.click()


	def run(self, languages='all'):
		'''
			runs the bot
			languages= 'all' => quizzes will be resolved for all the languages
					 = 'en-fr-fi' => quizzes will be solved only for those languaes
		'''
		self.connexion('en')

		if languages=='all':

			for key in dic_languages:

				self.browser.get('https://www.jetpunk.com/'+dic_languages[key]['link']+'user-stats')
				solve_for_language(self.browser)

		else :

			list_lang = languages.split('-')

			for lang in list_lang : 
				if lang not in dic_languages.keys() : 
					raise Exception


			for lang in list_lang:

				self.browser.get('https://www.jetpunk.com/'+dic_languages[key]['link']+'user-stats')
				solve_for_language(self.browser, key)


#j = BotPunk('your-username', 'your-password', 'the-path-to-your-chrome-driver')
#j.run()
