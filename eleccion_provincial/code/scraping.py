import requests
from bs4 import BeautifulSoup
import csv

# URL de la página web que contiene los resultados electorales
url = 'https://www.justiciacordoba.gob.ar/Estatico/JEL/Escrutinios/ReportesEleccion20190512/default.html'

# Obtener el contenido de la página web
response = requests.get(url)
html = response.content

# Crear un objeto BeautifulSoup a partir del contenido HTML
soup = BeautifulSoup(html, 'html.parser')

# Seleccionar la tabla de resultados para la sección capital y el cargo de gobernador
table = soup.find('table', {'id': 'grdResultadosCapitalGobernador'})

# Crear un archivo CSV para guardar los resultados
with open('resultados_gobernador_capital.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Escribir las columnas del archivo CSV
    writer.writerow(['Circuito', 'Mesa', 'Más votado', 'Votos'])

    # Iterar sobre las filas de la tabla y escribir los resultados en el archivo CSV
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) == 4:
            circuito = cells[0].get_text().strip()
            mesa = cells[1].get_text().strip()
            mas_votado = cells[2].get_text().strip()
            votos = cells[3].get_text().strip()
            writer.writerow([circuito, mesa, mas_votado, votos])
