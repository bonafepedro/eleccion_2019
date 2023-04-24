#Author: Josías Gómez
#Date: 2023/03/07



import requests 
from bs4 import BeautifulSoup as bs
import itertools
import string
import pandas as pd

cargos = ['CA2','CA3','CA4','CA5','CA7','CA8']

cookies = {
    'NLB_JusticiaCordoba': '402696384.47873.0000',
    'TS99ec4872027': '08bdf369a2ab200093cb7b56d5541b86ded7db8b2591d8850bd3eff74115959aeb0442a1a4fd0404082e830f65113000ef7423ef6b212402c69056296aeeb1b0a8f70be216f3a4526521ca3528ca12805c501b7568430d3309bf1b7723c5d345',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'es-AR,es;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Referer': 'https://www.justiciacordoba.gob.ar/Estatico/JEL/Escrutinios/ReportesEleccion20190512/Index.html',
    'Sec-Fetch-Dest': 'frame',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

def circuitos():
    num_1 = [i for i in range(15,100)]
    num_2 = [i for i in range(100,400)]
    
    lett = list(string.ascii_uppercase)[0:17]
    
    casos_1 = list(itertools.product(num_1,lett))
    casos_2 = list(itertools.product(num_2,lett))
    
    circuito_numeros_1 = [i for i in range(1,10)]
    circuito_numeros_2 = [i for i in range(10,15)]
    
    circuito_numero_y_letras_1 = []
    
    for caso in casos_1:
        circuito_numero_y_letras_1.append(str(caso[0])+caso[1])
    
    circuito_numero_y_letras_2 = []
    
    for caso in casos_2:
        circuito_numero_y_letras_2.append(str(caso[0])+caso[1])
        
    return circuito_numeros_1,circuito_numero_y_letras_1,circuito_numeros_2,circuito_numero_y_letras_2

def get_line(response):
    return [i.text for i in bs(response.text).select('tr td') if i.text != '']

def get_data():
    
    datos = []
    
    caso_1, caso_2, caso_3, caso_4 = circuitos()
    
    iter_1 = list(itertools.product(caso_1,cargos))
    iter_2 = list(itertools.product(caso_2,cargos))
    iter_3 = list(itertools.product(caso_3,cargos))
    iter_4 = list(itertools.product(caso_4,cargos))
    
    
    for i in iter_1:
        try: 
            response = requests.get(f'https://www.justiciacordoba.gob.ar/Estatico/JEL/Escrutinios/ReportesEleccion20190512/Resultados/E20190512_C{i[0]}%20%20%20_{i[1]}_0.htm',
                                        cookies=cookies,
                                        headers=headers,)
            response.raise_for_status()
            dato = get_line(response)
            datos.append(dato)
        except:
            next
    
    for i in iter_2:
        try: 
            response = requests.get(f'https://www.justiciacordoba.gob.ar/Estatico/JEL/Escrutinios/ReportesEleccion20190512/Resultados/E20190512_C{i[0]}%20%20_{i[1]}_0.htm',
                                        cookies=cookies,
                                        headers=headers,)
            response.raise_for_status()
            dato = get_line(response)
            datos.append(dato)
        except:
            next

    for i in iter_3:
        try: 
            response = requests.get(f'https://www.justiciacordoba.gob.ar/Estatico/JEL/Escrutinios/ReportesEleccion20190512/Resultados/E20190512_C{i[0]}%20%20_{i[1]}_0.htm',
                                        cookies=cookies,
                                        headers=headers,)
            response.raise_for_status()
            dato = get_line(response)
            datos.append(dato)
        except:
            next
    
    for i in iter_4:
        try: 
            response = requests.get(f'https://www.justiciacordoba.gob.ar/Estatico/JEL/Escrutinios/ReportesEleccion20190512/Resultados/E20190512_C{i[0]}%20_{i[1]}_0.htm',
                                        cookies=cookies,
                                        headers=headers,)
            response.raise_for_status()
            dato = get_line(response)
            datos.append(dato)
        except:
            next


    return datos


# recibe como input el resultado de la función get_data()
# en mi caso definí a info = get_data()

def data_parser_1(info):

    datos = []
    dato = {}
    
    ind1 = 7
    ind2 = 8
    ind3 = 9

    for i in range(len(info)-1):
        for j in range(int(len(info[i][7:-16])/3)):
        

            dato = {
                'titulo':info[i][0],
                'eleccion':info[i][1],
                'circuito':info[i][2],
                'candidato': info[i][3],
                'N°': info[i][ind1],
                'agrupacion': info[i][ind2] ,
                'votos':info[i][ind3]
            }
            
            datos.append(dato)
            
            ind1 += 3
            ind2 += 3
            ind3 += 3
        
        ind1 = 7
        ind2 = 8
        ind3 = 9
    return pd.DataFrame(datos)

def data_parser_2(info):

    datos = []
    dato = {}


    for i in range(len(info)-1):
        #for j in range(len(info[i][-15:-3])):
        

        dato = {
            'titulo':info[i][0],
            'eleccion':info[i][1],
            'circuito':info[i][2],
            'candidato': info[i][3],
            'vot valido':info[i][-15:-3][1],
            'vot nulo':info[i][-15:-3][3],
            'vot blanco':info[i][-15:-3][5],
            'total votantes': info[i][-15:-3][-3],
            'electores en padron': info[i][-15:-3][-1]
        }
        
        datos.append(dato)
        
    return pd.DataFrame(datos)