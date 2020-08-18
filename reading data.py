# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 11:35:47 2020

@author: Leandro.Eleuterio
"""

# Enem Analysis 

from ftplib import FTP
import pandas as pd


pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 35)

# laoding Enem data
#Location data FTP
ftp_connection = FTP('geoftp.ibge.gov.br')
ftp_connection.login() 
ftp_connection.cwd('/organizacao_do_territorio/estrutura_territorial/localidades')
ftp_connection.retrlines('LIST') 
ftp_connection.cwd('Geomedia_MDB')
ftp_connection.retrlines('LIST') 
#downloaded manually as I don't have a certificate to automaticly connect and query data on a access file stored in a ftp

dim_location = pd.read_excel(r'C:\Users\leandro.eleuterio\Desktop\Enem\BR_Localidades_2010_v1.xlsx')

#Exams Results Data ZIP File
dataset = pd.read_csv(r'C:\Users\leandro.eleuterio\Desktop\Enem\Microdados Enem 2017\DADOS\MICRODADOS_ENEM_2017.csv', delimiter=';', encoding='ISO-8859-1')

dim_student = dataset.iloc[:,:dataset.columns.get_loc('IN_TREINEIRO')+1]
dim_school = dataset.iloc[:,dataset.columns.get_loc('IN_TREINEIRO')+1:dataset.columns.get_loc('TP_SIT_FUNC_ESC')+1]
dim_handcap = dataset.iloc[:,dataset.columns.get_loc('TP_SIT_FUNC_ESC')+1:dataset.columns.get_loc('IN_OUTRA_DEF')+1]
dim_med_cond = dataset.iloc[:,dataset.columns.get_loc('IN_OUTRA_DEF')+1:dataset.columns.get_loc('IN_ESTUDA_CLASSE_HOSPITALAR')+1]
dim_special_cond = dataset.iloc[:,dataset.columns.get_loc('IN_ESTUDA_CLASSE_HOSPITALAR')+1:dataset.columns.get_loc('IN_NOME_SOCIAL')+1]
dim_exam_local = dataset.iloc[:,dataset.columns.get_loc('IN_NOME_SOCIAL')+1:dataset.columns.get_loc('SG_UF_PROVA')+1]
fact_score_obj = dataset.iloc[:,dataset.columns.get_loc('SG_UF_PROVA')+1:dataset.columns.get_loc('TX_GABARITO_MT')+1]
fact_score_essay = dataset.iloc[:,dataset.columns.get_loc('TX_GABARITO_MT')+1:dataset.columns.get_loc('NU_NOTA_REDACAO')+1]
dim_socio_economic = dataset.iloc[:,dataset.columns.get_loc('NU_NOTA_REDACAO')+1:dataset.columns.get_loc('Q027')+1]

dim_student = dim_student.join(fact_score_obj[['TP_PRESENCA_CN', 'TP_PRESENCA_CH','TP_PRESENCA_LC','TP_PRESENCA_MT']])
fact_score_essay = fact_score_essay.join(dim_student[['NU_INSCRICAO']])
fact_score_obj = fact_score_obj.join(dim_student[['NU_INSCRICAO']])
fact_score_obj = fact_score_obj.drop(['TP_PRESENCA_CN', 'TP_PRESENCA_CH','TP_PRESENCA_LC','TP_PRESENCA_MT'], axis=1)

del dataset

#Demographic Data

dim_cities = pd.read_csv(r'C:\Users\leandro.eleuterio\Desktop\Enem\cidades.csv', delimiter=',')
#---------------------------------------------------------------------------------------------------------------------------------#

#           ----------------------------- Analyse on dim_student proposed -----------------------------------------------
print(dim_student.describe())
print(dim_student.dtypes)
print(dim_student.columns)
# Imputation check: we are missing values for some rows in the following columns: NU_IDADE,TP_ESTADO_CIVIL, CO_MUNICIPIO_NASCIMENTO, CO_UF_NASCIMENTO, TP_ENSINO
# NU_IDADE should be on user dimension has some null values might require imputation
# TP_ESTADO_CIVIL should be on user dimension
# User LOWEST LEVEL OF GRANULARITY = NU_INSCRICAO
# Location LOWEST LEVEL OF GRANULARITY = CO_MUNICIPIO_RESIDENCIA
# It doesnt seem to have a school dimension as I did not found any school ID here.
# We can drop NU_ANO, date is valided, all values are from 2017 (ad hoc analysis on 2017 data)
dim_student = dim_student.drop('NU_ANO', axis=1)
# we can drop the following columns, will come from local hierachie from CO_MUNICIPIO_RESIDENCIA
dim_student = dim_student.drop('CO_UF_RESIDENCIA', axis=1)
dim_student = dim_student.drop('NO_MUNICIPIO_RESIDENCIA', axis=1)
dim_student = dim_student.drop('SG_UF_RESIDENCIA', axis=1)
# TP_COR_RACA should be on user dimension
# TP_NACIONALIDADE should be on user dimension
# CO_MUNICIPIO_NASCIMENTO should be on user dimension
# we can drop the following columns  will come from local hiarechy from CO_MUNICIPIO_NASCIMENTO
dim_student = dim_student.drop('CO_UF_NASCIMENTO', axis=1)
dim_student = dim_student.drop('NO_MUNICIPIO_NASCIMENTO', axis=1)
dim_student = dim_student.drop('SG_UF_NASCIMENTO', axis=1)

# TP_ST_CONCLUSAO should be on user dimension
# TP_ANO_CONCLUIU should be on user dimension
# TP_ESCOLA should be on user dimension
# TP_ENSINO has some null values might require imputation (its where do you concluded or plant to conclue your degree) should be on user dimension
# prefix TP seems to indicate that Column named TP are classifications.


#           ----------------------------- Analyse on dim_school -----------------------------------------------
print(dim_school.describe())
print(dim_school.dtypes)
print(dim_school.columns)
# CO_ESCOLA seems to be the school ID but is missing for a few users should be in dim schoool might require imputation;
# CO_MUNICIPIO_ESC is missing for a few users but should be in dim schoool;
# CO_UF_ESC is missing for a few users but should be in dim schoool;
# TP_DEPENDENCIA_ADM_ESC is missing for a few users but should be in dim schoool;
# TP_LOCALIZACAO_ESC is missing for a few users but should be in dim schoool;
dim_school_id = dim_school.drop_duplicates()
dim_school_id = dim_school_id.reset_index()
dim_school_id = dim_school_id.drop('index', axis=1)
dim_school_id['id_school'] = dim_school_id.index
dim_school = pd.merge(dim_school, dim_school_id, on=list(dim_school.columns))
fact_score_obj = fact_score_obj.join(dim_school[['id_school']])
fact_score_essay = fact_score_essay.join(dim_school[['id_school']])
del dim_school
dim_school = dim_school_id
del dim_school_id

#           ----------------------------- Analyse on dim_handcap -----------------------------------------------
#dim_handcap can be part of user dimension or be a dimension of its on.
print(dim_handcap.describe())
print(dim_handcap.dtypes)
print(dim_handcap.columns)
dim_handcap_id = dim_handcap.drop_duplicates()
dim_handcap_id = dim_handcap_id.reset_index()
dim_handcap_id = dim_handcap_id.drop('index', axis=1)
dim_handcap_id['id_handcap'] = dim_handcap_id.index
dim_handcap = pd.merge(dim_handcap, dim_handcap_id, on=list(dim_handcap.columns))
fact_score_obj = fact_score_obj.join(dim_handcap[['id_handcap']])
fact_score_essay = fact_score_essay.join(dim_handcap[['id_handcap']])
del dim_handcap
dim_handcap = dim_handcap_id
del dim_handcap_id

#           ----------------------------- Analyse on dim_med_cond -----------------------------------------------
#dim_med_cond can be part of user dimension or be a dimension of its on.
print(dim_med_cond.describe())
print(dim_med_cond.dtypes)
print(dim_med_cond.columns)
dim_med_cond_id = dim_med_cond.drop_duplicates()
dim_med_cond_id = dim_med_cond_id.reset_index()
dim_med_cond_id = dim_med_cond_id.drop('index', axis=1)
dim_med_cond_id['id_med_cond'] = dim_med_cond_id.index
dim_med_cond = pd.merge(dim_med_cond, dim_med_cond_id, on=list(dim_med_cond.columns))
fact_score_obj = fact_score_obj.join(dim_med_cond[['id_med_cond']])
fact_score_essay = fact_score_essay.join(dim_med_cond[['id_med_cond']])
del dim_med_cond
dim_med_cond = dim_med_cond_id
del dim_med_cond_id

#           ----------------------------- Analyse on dim_special_cond -----------------------------------------------
#dim_special_cond can be part of user dimension or be a dimension of its on.
print(dim_special_cond.describe())
print(dim_special_cond.dtypes)
print(dim_special_cond.columns)
dim_special_cond_id = dim_special_cond.drop_duplicates()

dim_special_cond_id = dim_special_cond_id.reset_index()
dim_special_cond_id = dim_special_cond_id.drop('index', axis=1)
dim_special_cond_id['id_special_cond'] = dim_special_cond_id.index
dim_special_cond = pd.merge(dim_special_cond, dim_special_cond_id, on=list(dim_special_cond.columns))
fact_score_obj = fact_score_obj.join(dim_special_cond[['id_special_cond']])
fact_score_essay = fact_score_essay.join(dim_special_cond[['id_special_cond']])
del dim_special_cond
dim_special_cond = dim_special_cond_id
del dim_special_cond_id


#           ----------------------------- Analyse on dim_exam_local -----------------------------------------------
print(dim_exam_local.describe())
print(dim_exam_local.dtypes)
print(dim_exam_local.columns)
dim_exam_local_id = dim_exam_local.drop_duplicates()
dim_exam_local_id = dim_exam_local_id.reset_index()
dim_exam_local_id = dim_exam_local_id.drop('index', axis=1)
dim_exam_local_id['id_exam_local'] = dim_exam_local_id.index
dim_exam_local = pd.merge(dim_exam_local, dim_exam_local_id, on=list(dim_exam_local.columns))
fact_score_obj = fact_score_obj.join(dim_exam_local[['id_exam_local']])
fact_score_essay = fact_score_essay.join(dim_exam_local[['id_exam_local']])
del dim_exam_local
dim_exam_local = dim_exam_local_id
del dim_exam_local_id


#           ----------------------------- Analyse on dim_socio_economic -----------------------------------------------
print(dim_socio_economic.describe())
print(dim_socio_economic.dtypes)
print(dim_socio_economic.columns)
dim_socio_economic_id = dim_socio_economic.drop_duplicates()

dim_socio_economic_id = dim_socio_economic_id.reset_index()
dim_socio_economic_id = dim_socio_economic_id.drop('index', axis=1)
dim_socio_economic_id['id_social_economic'] = dim_socio_economic_id.index
dim_socio_economic = pd.merge(dim_socio_economic, dim_socio_economic_id, on=list(dim_socio_economic.columns))
fact_score_obj = fact_score_obj.join(dim_socio_economic[['id_social_economic']])
fact_score_essay = fact_score_essay.join(dim_socio_economic[['id_social_economic']])
del dim_socio_economic
dim_socio_economic = dim_socio_economic_id
del dim_socio_economic_id

#           ----------------------------- Analyse on dim_location -----------------------------------------------
print(dim_location.describe()) 
print(dim_location.dtypes)
print(dim_location.columns)
#ID seems to be the lowest level of granularity for local 
#This seems to be the location hiearachiy.
#i'm not sure im gonna need CD_ prefixed columns, I think I won't, I can check that on pbi.


#           ----------------------------- Analyse on dim_cities -----------------------------------------------
print(dim_cities.describe()) 
print(dim_cities.dtypes)
print(dim_cities.columns)
#check if Código maches location.ID and dim_student.CO_MUNICIPIO_RESIDENCIA
# População_estimada_pessoas_2019 to be added at dim_location

dim_location = dim_location.groupby(['NM_MUNICIPIO', 'CD_GEOCODMU','NM_MESO','NM_UF']).agg({'LONG': 'last', 'LAT': 'last'}).reset_index()
dim_location = pd.merge(dim_cities, dim_location, left_on=dim_cities['Código'], right_on= dim_location['CD_GEOCODMU'])

#ADDED ESSAY SCORE ON MAIN SCORE DATAFRAME
fact_score_obj = fact_score_obj.join(fact_score_essay['NU_NOTA_REDACAO'])
#-------------------------------------------------------------------------------------------------------------------------------  #
#Saving outputfiles

dim_student.to_csv(path_or_buf=r'C:\Users\leandro.eleuterio\Desktop\Enem\Output\dim_student.csv')
dim_school.to_csv(path_or_buf=r'C:\Users\leandro.eleuterio\Desktop\Enem\Output\dim_school.csv')
dim_handcap.to_csv(path_or_buf=r'C:\Users\leandro.eleuterio\Desktop\Enem\Output\dim_handcap.csv')
dim_med_cond.to_csv(path_or_buf=r'C:\Users\leandro.eleuterio\Desktop\Enem\Output\dim_med_cond.csv')
dim_special_cond.to_csv(path_or_buf=r'C:\Users\leandro.eleuterio\Desktop\Enem\Output\dim_special_cond.csv')
dim_exam_local.to_csv(path_or_buf=r'C:\Users\leandro.eleuterio\Desktop\Enem\Output\dim_exam_local.csv')
fact_score_obj.to_csv(path_or_buf=r'C:\Users\leandro.eleuterio\Desktop\Enem\Output\fact_score_obj.csv')
fact_score_essay.to_csv(path_or_buf=r'C:\Users\leandro.eleuterio\Desktop\Enem\Output\fact_score_essay.csv')
dim_socio_economic.to_csv(path_or_buf=r'C:\Users\leandro.eleuterio\Desktop\Enem\Output\dim_socio_economic.csv')
dim_location.to_csv(path_or_buf=r'C:\Users\leandro.eleuterio\Desktop\Enem\Output\dim_location.csv')

state_names = dim_location.NM_UF
state_names.to_csv(r'C:\Users\leandro.eleuterio\Desktop\Enem\Output\state_names.csv',  encoding='ISO-8859-1')

dic = dim_student.dtypes
dic = dic.append(dim_school.dtypes)
dic = dic.append(dim_handcap.dtypes)
dic = dic.append(dim_med_cond.dtypes)
dic = dic.append(dim_special_cond.dtypes)
dic = dic.append(dim_exam_local.dtypes)
dic = dic.append(fact_score_obj.dtypes)
dic = dic.append(fact_score_essay.dtypes)
dic = dic.append(dim_socio_economic.dtypes)
dic = dic.append(dim_location.dtypes)

dic = dic.reset_index()

dic = dic.rename(columns={'index': 'field', 0 : 'dtype',})
dic.to_csv(path_or_buf=r'C:\Users\leandro.eleuterio\Desktop\Enem\Output\data_dictionary.csv')

