import datetime
import pymysql
import pymysql.cursors  

class DBHandler:
    #connection_string or conn_params
    connection_string={'host':'217.71.129.139', 'port':4146, 'user':'wk', 'password':'Ghjcnjnf', 'db':'workmapdb'}
   
    table_structure = ['region','quan_vacancy','average_salary','competition']

    def __init__(self, db_name='workmapdb'):
        
        self.db_name = db_name
        
        self.db_len = 0
        self.db_tables = []

        try:
            with pymysql.connect(**DBHandler.connection_string) as cnxn:

                cnxn.autocommit = True                
				#use_query
                sql_query = f"USE {self.db_name}"
                cnxn.execute(sql_query)

                for table in cursor.tables():
                    if table[1] == 'dbo':
                        self.db_len += 1
                        self.db_tables.append(table[2])
        except:
            print(f'Object DBHandler was successfull linked with {self.db_name} but database with the same name does not exist yet')

    def __len__(self):
        return self.db_len

    def __repr__(self):
        return f"Database `{self.db_name}` with {self.db_len} occupation tables: {self.db_tables}"

    def count_tables(self):
        pass


    def create_database(self):

		with pymysql.connect(**DBHandler.connection_string) as cnxn:
			
			cnxn.autocommit = True	
			#create_query
			sql_create_db_query = f"CREATE DATABASE {self.db_name}"
				
			try:
				cnxn.execute(sql_create_db_query)
			except pymysql.ProgrammingError:
				print(f'\nProbably the "{self.db_name}" database already exist...')


    def create_table(self,table_name):
        
		with pymysql.connect(**DBHandler.connection_string) as cnxn:
			
			cnxn.autocommit = True
			
			sql_use_db_query = f"USE {self.db_name}"
			cnxn.execute(sql_use_db_query)

			sql_create_table_query = \
						f"CREATE TABLE IF NOT EXISTS {table_name}\
					(id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,\
					{DBHandler.table_structure[0]} VARCHAR(255) NULL,\
					{DBHandler.table_structure[1]} INT NOT NULL,\
					{DBHandler.table_structure[2]} VARCHAR(255) NULL,\
					{DBHandler.table_structure[3]} VARCHAR(255) NULL)"
			try:
				cnxn.execute(sql_create_table_query)
			except pymysql.ProgrammingError:
				print(f'\nProbably the "self.db_name" structure already created...')
				
    def delete_data(self,table_name):
				
		with pymysql.connect(**DBHandler.connection_string) as cnxn:
			
			cnxn.autocommit = True		
						
			sql_use_db_query = f"USE {self.db_name}"
			cnxn.execute(sql_use_db_query)					
							
			sql_clear_collum = f"TRUNCATE TABLE {table_name}"
			
			try:
				cnxn.execute(sql_clear_collum)
			except pymysql.ProgrammingError:
				print(f'\nProbably the "{self.db_name}" structure already delete...')
				
				
	
    def copy_data(self, table_name):

		with pymysql.connect(**DBHandler.connection_string) as cnxn:
			
			cnxn.autocommit = True		
						
			sql_use_db_query = f"USE {self.db_name}"
			cnxn.execute(sql_use_db_query)		
			
			table_name_YMD = (str(table_name) + str(datetime.datetime.now().strftime("%Y%m%d")))
				
			sql_copy_table_query = \
						f"CREATE TABLE {table_name_YMD} SELECT * FROM {table_name}"						
			
			try:
				cnxn.execute(sql_copy_table_query)				
			except pymysql.ProgrammingError:
				print(f'\nProbably the "{self.db_name}" structure already copy...')
				
    def insert_data(self,table_name):
		
		with pymysql.connect(**DBHandler.connection_string) as cnxn:
			
			cnxn.autocommit = True		
			
			#use_query
			sql_use_db_query = f"USE {self.db_name}"
			cnxn.execute(sql_use_db_query)
			
			for i in prof_data[raw_prof_data.search_criteria]:
				row = prof_data[raw_prof_data.search_criteria][i]

				if prof_data[raw_prof_data.search_criteria][i]['Наиболее востребованные компетенции'] == 'нет данных':
					demanded_competencies = row['Наиболее востребованные компетенции']
				else:
					demanded_competencies = (', '.join(row['Наиболее востребованные компетенции']))
				sql_insert_table_query= f"INSERT INTO {table_name} (region, quan_vacancy, average_salary, competition)\
								VALUES \
								('{i}','{row['Количество вакансий']}','{row['Средняя заработная плата для начинающего специалиста']}','{demanded_competencies}')"
				cnxn.execute(sql_insert_table_query) 

    def length_tb(self, table_name):	
		with pymysql.connect(**DBHandler.connection_string) as cnxn:	
			cnxn.autocommit = True
			
			sql_use_db_query = f"USE {self.db_name}"
			cnxn.execute(sql_use_db_query)
			
			sql_query = \
							f"SELECT {DBHandler.table_structure[0]} FROM {table_name}"
			try:
				len_table=cnxn.execute(sql_query)	
				return len_table
			except pymysql.ProgrammingError:
				print(f'\nProbably the "{self.db_name}" structure already for count length of rows...')	
