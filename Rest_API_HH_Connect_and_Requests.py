import re
import json
import pickle
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

class VacancyAnalyzer:

	url = 'https://api.hh.ru/vacancies'

	def __init__(self, search_criteria, search_field='name'):
    
        self.vacancies = []
        self.clusters = None
        self.skills = None
        self.skills_full = None
        self.keywords = None
        self.keywords_full = None
        self.extract = None
        self.areas = None
        self.dates = None
        self.experience = None
        self.unique = None
		
		self.search_criteria = search_criteria

        self.search_parameters ={
                                'text': search_criteria,
                                'per_page': 100,
                                'page': 0,
                                'clusters': 'true',
                                'describe_arguments': 'true',
                                }
        if search_field: self.search_parameters['search_field'] = search_field
        #if search_area: self.search_parameters['area'] = search_area

        self.__initial = True


	def full_vacancies_collector(self):

			brief_vacancies = []
			current_page = 0
			pages_count = current_page + 1

			while current_page < pages_count:
				self.search_parameters['page'] = current_page
				raw_response = requests.get(VacancyAnalyzer.url, params = self.search_parameters)
				response = raw_response.json()
				brief_vacancies += response.get('items')
				pages_count = response.get('pages')
				current_page += 1

			self.clusters = response.get('clusters')

			#collecting urls which link to full vacancy descriptions
			urls = [vacancy.get('url') for vacancy in brief_vacancies]

			#form a list of full vacancies
			self.vacancies = [requests.get(url).json() for url in tqdm(urls)]
			
			
			
	def select_info_prof(self):
		cities=['Махачкала','Якутск','Владикавказ','Нальчик','Черкеск','Ставрополь','Краснодар','Ростов на дону','Элиста','Астрахань','Майкоп','Волгоград','Воронеж','Белгород','Курск','Орел','Липецк','Тула','Брянск','Калуга','Смоленск','Москва','Рязань','Тамбов','Калининград','Псков','Великий Новгород','Тверь','Владимир','Пенза','Саратов','Саранск','Чебоксары','Ульяновск','Самара','Оренбург','Нижний Новгород','Йошкар-Ола','Казань','Иваново','Ярославль','Кострома','Санкт-Петербург','Киров','Уфа','Челябинск','Ижевск','Пермь','Екатеринбург','Курган','Сыктывкар','Мурманск','Петрозаводск','Вологда','Архангельск','Тюмень','Нарьян-Мар','Омск','Ханты-Мансийск','Салехард','Красноярск','Томск','Новосибирск','Барнаул','Кемерово','Горно-Алтайск','Кызыл','Абакан','Иркутск','Улан-Удэ','Чита','Благовещенск','Анадырь','Хабаровск','Биробиджан','Владивосток','Магадан','Южно-Сахалинск','Петропавловск-Камчатский','Магас','Грозный','Симферополь']
		data_info={}
		data_info[self.search_criteria]={}
		for city in cities: 				
			data_info[self.search_criteria][city]={}			
			
			quan_vac=len([vacancy
				for vacancy in self.vacancies
					if vacancy.get('area').get('name') == city])
			
			data_info[self.search_criteria][city]["Количество вакансий"]=quan_vac
			salaries = [vacancy.get('salary')
				for vacancy in self.vacancies
					if vacancy.get('salary') and vacancy.get('area').get('name') == city]
					
			salaries_rur = [salary 
                for salary in salaries 
                    if salary.get('currency') == 'RUR']
                
			salaries_rur_from_gross = [salary.get('from')*0.87 
                for salary in salaries_rur
                    if salary.get('from') and salary.get('gross')]
                    
			salaries_rur_from = [salary.get('from')
                for salary in salaries_rur
                    if salary.get('from') and not salary.get('gross')]
                    
			salaries_rur_from_all = salaries_rur_from + salaries_rur_from_gross            
			
			salaries_rur_from_sum = round( sum(salaries_rur_from_all) / len(salaries_rur_from_all)) if salaries_rur_from_all else "нет данных"                
			
			data_info[self.search_criteria][city]["Средняя заработная плата для начинающего специалиста"]=salaries_rur_from_sum

			raw_key_skills = [vacancy.get('key_skills') 
                for vacancy in self.vacancies 
                    if len(vacancy.get('key_skills')) != 0 and vacancy.get('area').get('name') == city]
                    
			key_skills = [key_skill['name'] for item in raw_key_skills for key_skill in item]
                        
			ks_entries_count_by_number = {key_skills.count(skill) : skill for skill in key_skills}
            
			keys_sort=sorted(ks_entries_count_by_number.items(), key=lambda x: x[0], reverse=True)
            
			top5_ks=keys_sort[:5]            
			top_ = [ks[1] for ks in top5_ks] if len(ks_entries_count_by_number) >2 else "нет данных" 
                
			data_info[self.search_criteria][city]["Наиболее востребованные компетенции"]=top_
		return data_info		
			
