import DB_Connect_and_Requexsts 
import Rest_API_HH_Connect_and_Requests

#prof_list
prof_list={'BA':'Бизнес аналитик','Dev1c':'Программист 1С','InternetMarket':'Интернет маркетолог','SMMManager':'SMM менеджер','SA':'Системный аналитик','WebDev':'Веб разработчик','WebDesign':'Веб дизайнер', 'ManagerProdj':'Менеджер проектов','SEO':'SEO'}
	
for i in range (len(prof_list)):
	#raw_prof_data	
	raw_prof_data=VacancyAnalyzer(prof_list.get(list(prof_list.keys())[i]))
	raw_prof_data.full_vacancies_collector()
	#prof_data
	prof_data=raw_prof_data.select_info_prof()

	db=DBHandler()
		
	db.create_table(list(prof_list.keys())[i])
		
	if db.length_tb(list(prof_list.keys())[i]) == 0:
		db.insert_data(list(prof_list.keys())[i])
	else:
		db.copy_data(list(prof_list.keys())[i])
		db.delete_data(list(prof_list.keys())[i])
		db.insert_data(list(prof_list.keys())[i])				
