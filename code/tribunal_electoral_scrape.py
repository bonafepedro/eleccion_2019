#Author: Josías Gómez
#Date: 2023/03/07



from bs4 import BeautifulSoup as bs
import itertools
import string
import pandas as pd
import asyncio
import httpx

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
    
    #Para hacer las consultas a la API hay que definir los cargos y los circuitos. Los cargos fueron definidos en una variable
    #global más arriba. En el caso de los circuitos se presentan diferentes casos que condicionan el request.
    #Se detecto que existen seis casos. La de número que van respectivamente de 1-9, 10-99 y 99-400, por un lado. Por el otro,
    #se suma la presencia de una letra para cada caso anteriormente definido. Por ello quedan conformados seis casos posibles.
    
    
    #Se crea una lista con letras
    lett = list(string.ascii_uppercase)[0:17]
    
    #Se definen las listas con los tres casos numéricos
    circuito_numeros_1 = [i for i in range(1,10)]
    circuito_numeros_2 = [i for i in range(10,100)]
    circuitos_numeros_3 = [i for i in range(100,401)]
    
    #Luego se generan los casos de número + letra
    casos_1 = list(itertools.product(circuito_numeros_1,lett))
    casos_2 = list(itertools.product(circuito_numeros_2,lett))
    casos_3 = list(itertools.product(circuitos_numeros_3,lett))
    
    #Finalmente se crean las listas con número + letra. El paso anterior podría haberse evitado, pero a fines de legibilidad se 
    #obtó por separalos
    circuito_numero_y_letras_1 = [str(caso[0])+caso[1] for caso in casos_1]
    circuito_numero_y_letras_2 = [str(caso[0])+caso[1] for caso in casos_2]
    circuito_numero_y_letras_3 = [str(caso[0])+caso[1] for caso in casos_3]
    
    #Se generan los iteradores que combinan circuitos + cargos
    iter_1 = list(itertools.product(circuito_numeros_1,cargos))
    iter_2 = list(itertools.product(circuito_numero_y_letras_1,cargos))
    iter_3 = list(itertools.product(circuito_numeros_2,cargos))
    iter_4 = list(itertools.product(circuito_numero_y_letras_2,cargos))
    iter_5 = list(itertools.product(circuitos_numeros_3,cargos))
    iter_6 = list(itertools.product(circuito_numero_y_letras_3,cargos))
    
    #Finalmente se definen los diferentes paquetes de links que harán las requests necesarias considerando cada caso
    links_1 = [f'https://www.justiciacordoba.gob.ar/Estatico/JEL/Escrutinios/ReportesEleccion20190512/Resultados/E20190512_C{i[0]}%20%20%20%20_{i[1]}_0.htm' for i in iter_1]
    links_2 = [f'https://www.justiciacordoba.gob.ar/Estatico/JEL/Escrutinios/ReportesEleccion20190512/Resultados/E20190512_C{i[0]}%20%20%20_{i[1]}_0.htm' for i in iter_2]
    links_3 = [f'https://www.justiciacordoba.gob.ar/Estatico/JEL/Escrutinios/ReportesEleccion20190512/Resultados/E20190512_C{i[0]}%20%20%20_{i[1]}_0.htm' for i in iter_3]
    links_4 = [f'https://www.justiciacordoba.gob.ar/Estatico/JEL/Escrutinios/ReportesEleccion20190512/Resultados/E20190512_C{i[0]}%20%20_{i[1]}_0.htm' for i in iter_4]
    links_5 = [f'https://www.justiciacordoba.gob.ar/Estatico/JEL/Escrutinios/ReportesEleccion20190512/Resultados/E20190512_C{i[0]}%20%20_{i[1]}_0.htm' for i in iter_5]
    links_6 = [f'https://www.justiciacordoba.gob.ar/Estatico/JEL/Escrutinios/ReportesEleccion20190512/Resultados/E20190512_C{i[0]}%20_{i[1]}_0.htm' for i in iter_6]
    
    
    
    return list(itertools.chain(links_1,links_2,links_3,links_4,links_5))

def get_line(response):
    return [i.text for i in bs(response.text).select('tr td') if i.text != '']

#Considerando que se realizarán unas ~7k requests (400+400*16), se decide definir la función get_data como una
#función asíncrona, es decir, que cuando por x razón la request se demore se ejecutará otra en el tiempo que la pimera
#está "cargando"

async def get_data():
    
    #se define un timeout mayor que el default para evitar que se rompa el código
    timeout = httpx.Timeout(30.0)
    
    datos = []
    
    #se toman los casos de la función circuitos
    links = circuitos()
    
    #se define un cliente async y se crea una lista de tareas por cada link provisto
    async with httpx.AsyncClient() as client:

        task = [client.get(link,timeout=timeout) for link in links]
        for response_future in asyncio.as_completed(task):
            response = await response_future
            dato = get_line(response)
            datos.append(dato)

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
