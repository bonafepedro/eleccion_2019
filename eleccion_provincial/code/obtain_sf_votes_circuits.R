library(sf)
library(dplyr)
library(tidyverse)
library(mapview)
library(readxl)

#circuitos ciudad
# circuitos <- st_read("CircuitosElectorales/Unir_entidades_a_CircuitosElectorales.shp")
# votos <- read_csv("votos2019.csv")
# 
# circuitos$lon <- st_coordinates(circuitos)[,1]
# circuitos$lat <- st_coordinates(circuitos)[,2]
# circuitos <- circuitos %>%  st_set_geometry(NULL)
# 
# circuitos_votos <- left_join(circuitos, votos, by = c("circuito" = "CIRCUITO_NUEVO"))
# 
# circuitos_votos <- circuitos_votos %>% 
#   st_as_sf(crs= 4326, coords = c("lon", "lat"))
# 
# write.csv(circuitos_votos, "circuitos_votos.csv")
# circuitos_votos <- st_as_sf(circuitos_votos, crs= 4326)
# st_write(circuitos_votos, "circuitos_votos2019.shp", delete_layer = T)


#circuitos provincia

circuitos_provincia <- st_read("circuitos_electorales_AR/geojson/CORDOBA.geojson")
mapview::mapview(circuitos_provincia)

#Localidades provincia
localidades_comunas <- st_read("personas_por_municipio/SOC_MYC_personas_2010.shp")
localidades_comunas <- st_transform(localidades_comunas, crs = 4326)
mapview(localidades_comunas)

#Circuito al que pertenece cada localidad
localidad_circuito <- st_join(localidades_comunas, circuitos_provincia, join = st_within)

circuitos_provincia_nuevo <- st_read("circuitos_provincia/circuito_04.shp")
mapview(circuitos_provincia_nuevo)


#resultados elecotrales por circuito
circuitos_votos <- read_excel("resultados_electorales/data_parser_1.xlsx")
#circuitos_votos <- xlsx::read.xlsx("resultados_electorales/data_parser_1.xlsx", encoding="UTF-8")
circuitos_votos2 <- read_xlsx("resultados_electorales/data_parser_2.xlsx")

eleccion_gobernador <- circuitos_votos %>% 
  filter(candidato == "Gobernador y Vicegobernador")


elec_gob2 <- circuitos_votos2 %>% 
  filter(candidato == "Gobernador y Vicegobernador" & titulo == "TRIBUNAL ELECTORAL PROVINCIAL AD HOC") %>% 
  select(c("circuito", "vot valido", "vot nulo" , "total votantes" , "electores en padron"))


eleccion_gobernador1 <- left_join(eleccion_gobernador, elec_gob2, by = "circuito")


# Separar código de circuito y completar con ceros
eleccion_gobernador1$codigo_circuito <- str_extract(eleccion_gobernador1$circuito, "\\d+\\w*")
circuitos_provincia_nuevo$codigo_circuito <- gsub("^0+", "", circuitos_provincia_nuevo$circuito)
circuitos_provincia$codigo_circuito <- gsub("^0+", "", circuitos_provincia$circuito)


eleccion_gobernador1 <- eleccion_gobernador1 %>%
  mutate(seccional = str_extract(codigo_circuito, "\\d+"))

#eleccion_gobernador1$codigo_circuito <- gsub(".*?(\\d+[A-Z]).*", "\\1", eleccion_gobernador1$circuito)
#eleccion_gobernador1$codigo_circuito <- as.character(eleccion_gobernador1$codigo_circuito)
#eleccion_gobernador1$codigo_circuito <- str_pad(eleccion_gobernador1$codigo_circuito, width = 5, side = "left", pad = "0")

#me quedo solo con el interior
#eleccion_gobernador2 <- eleccion_gobernador1 %>%
#  filter(seccional > 14)

eleccion_gobernador_circuitosgit <- left_join(eleccion_gobernador1, circuitos_provincia, by = "codigo_circuito")
eleccion_gobernador_circuitos_cne <- left_join(eleccion_gobernador1, circuitos_provincia_nuevo, by = "codigo_circuito")



circuitos_vacios_git <- eleccion_gobernador_circuitosgit %>% 
  filter(is.na(eleccion_gobernador_circuitosgit$coddepto))

circuitos_vacios_cne <- eleccion_gobernador_circuitos_cne %>% 
  filter(is.na(eleccion_gobernador_circuitos_cne$gid))


circuitos_vacios_asignar <- unique(circuitos_vacios_git$codigo_circuito)

# eleccion_gobernador2 <- eleccion_gobernador2 %>% filter(!circuito %in% c("Circuito 4E    - NUESTRO HOGAR III",
#                                                                          "Circuito 5I    - COLINAS DEL SUR",
#                                                                          "Circuito 4F    - CIUDAD OBISPO ANGELELLI",
#                                                                          "Circuito 5H    - VILLA BOEDO",
#                                                                          "Circuito 223   - CANDELARIA NORTE",
#                                                                          "Circuito 13O   - CHACHAPOYAS",
#                                                                          "Circuito 10M   - AMPLIACION CABILDO",
#                                                                          "Circuito 11L   - COUNTRYS DEL OESTE",
#                                                                          "Circuito 12I   - CIUDAD DE MIS SUE�OS",
#                                                                          "Circuito 11M   - VALLE ESCONDIDO"))
# 


eleccion_gobernador_circuitosgit <- eleccion_gobernador_circuitosgit %>% filter(!circuito.x %in% c("Circuito 223   - CANDELARIA NORTE")) # lo elimino porq no encuentro ese circuito

ambul <- circuitos_provincia_nuevo %>% filter(codigo_circuito == "260")
la_puerta <- circuitos_provincia_nuevo %>% filter(codigo_circuito == "205")
#candelaria <- circuitos_provincia_nuevo %>% filter(codigo_circuito == "223") -> ESTE CIRCUITO NO EXISTE
nuestro_hogar3 <- circuitos_provincia_nuevo %>% filter(codigo_circuito == "4E")
O13 <- circuitos_provincia_nuevo %>% filter(codigo_circuito == "13O")
m10 <- circuitos_provincia_nuevo %>% filter(codigo_circuito == "10M")
L11 <- circuitos_provincia_nuevo %>% filter(codigo_circuito == "11L")
H5 <- circuitos_provincia_nuevo %>% filter(codigo_circuito == "5H")
I5 <- circuitos_provincia_nuevo %>% filter(codigo_circuito == "5I")
F4 <- circuitos_provincia_nuevo %>% filter(codigo_circuito == "4F")
I12 <- circuitos_provincia_nuevo %>% filter(codigo_circuito == "12I")
M11 <- circuitos_provincia_nuevo %>% filter(codigo_circuito == "11M")

#ambul1 <- circuitos_provincia %>% filter(circuito == 00260)
ambul <- ambul %>% 
  rbind(la_puerta, nuestro_hogar3, O13, m10, L11, H5, I5, F4, I12, M11) %>% 
  select(c("geometry", "circuito", "codigo_circuito")) %>% 
  mutate(coddepto = 0)

#ambul$circuito <- str_pad(ambul$circuito, width = 5, side = "left", pad = "0")
  

circuitos_provincia <- circuitos_provincia %>% 
  rbind(ambul) # me reconoce solo el orden de las columnas que cosa hermosa

#circuitos_provincia <- ifelse(circuitos_provincia$circuito == "0260", "00260", circuitos_provincia$circuito)

#circuitos_provincia <- ifelse(circuitos_provincia$circuito == "0223", "00223", circuitos_provincia$circuito)

eleccion_gobernador_circuitosgit <- left_join(eleccion_gobernador_circuitosgit, circuitos_provincia, by = "codigo_circuito")

circuitos_vacios_asignar <- unique(circuitos_vacios$codigo_circuito)




#st as sf los circuitos y los votos
eleccion_gobernador_circuitosgit <- eleccion_gobernador_circuitosgit %>% 
  st_as_sf(crs = 4326)
mapview(eleccion_gobernador_circuitosgit)


eleccion_gobernador_circuitosgit <- eleccion_gobernador_circuitosgit %>% 
  rename("total_votantes"= "total votantes")
eleccion_gobernador_circuitosgit <- eleccion_gobernador_circuitosgit %>% 
  rename("total_electores"= "electores en padron")

#agrego la columna porcentaje de votos del circuito obtenida por c/partido

eleccion_gobernador_circuitosgit$total_votantes <- as.character(eleccion_gobernador_circuitosgit$total_votantes)
eleccion_gobernador_circuitosgit$total_votantes <- gsub("\\D", "", eleccion_gobernador_circuitosgit$total_votantes)
eleccion_gobernador_circuitosgit$total_votantes <- as.numeric(eleccion_gobernador_circuitosgit$total_votantes)

eleccion_gobernador_circuitosgit$votos <- as.character(eleccion_gobernador_circuitosgit$votos)
eleccion_gobernador_circuitosgit$votos <- gsub("\\D", "", eleccion_gobernador_circuitosgit$votos)
eleccion_gobernador_circuitosgit$votos <- as.numeric(eleccion_gobernador_circuitosgit$votos)

eleccion_gobernador_circuitosgit$total_electores <- as.character(eleccion_gobernador_circuitosgit$total_electores)
eleccion_gobernador_circuitosgit$total_electores <- gsub("\\D", "", eleccion_gobernador_circuitosgit$total_electores)
eleccion_gobernador_circuitosgit$total_electores <- as.numeric(eleccion_gobernador_circuitosgit$total_electores)



eleccion_gobernador_circuitosgit <- eleccion_gobernador_circuitosgit %>%
  group_by(codigo_circuito, agrupacion) %>%
  mutate(porcentaje_votos = round(as.numeric(votos)  / as.numeric(total_votantes), 3)*100)




st_write(eleccion_gobernador_circuitosgit, "output/resultados_circuitos_PROVINCIA.shp", delete_layer = T)

#circuitos que faltan datos

circuitos_faltantes <- anti_join(circuitos_provincia, eleccion_gobernador_circuitosgit, by ="codigo_circuito")


circuitos_faltantes_asignar <- unique(circuitos_faltantes$codigo_circuito)

circuitos_faltantes_asignar <- list(circuitos_faltantes_asignar)
write.csv(circuitos_faltantes_asignar, "output/circuitos_faltantes_codigos.csv")


circuitos_faltantes <- circuitos_faltantes %>% 
  st_as_sf(crs = 4326)

st_write(circuitos_faltantes, "output/circuitos_faltantes_capa.xlsx", delete_layer = T)



# #writexl::write_xlsx(eleccion_gobernador1, "resultados_electorales/resultados_circuitos.xlsx")
# 
# circuitos_faltantes1 <- circuitos_faltantes %>%
#   filter(circuito == "zonagris" | circuito == "sindatos")
# 
# 
# circuitos_faltantes_valid <- st_make_valid(circuitos_faltantes1)
# circuitos_faltantes_invalid <- circuitos_faltantes1[!st_is_valid(circuitos_faltantes1),]
# 
# 
# circuitos_faltantes_valid <- st_make_valid(circuitos_faltantes1)
# circuitos_faltantes_invalid <- circuitos_faltantes_valid[!st_is_valid(circuitos_faltantes_valid),]
# 
# circuitos_provincia_nuevo_valid <- st_make_valid(circuitos_provincia_nuevo)
# 
# 
# # identificar las filas con geometrías esféricas
# spherical_rows <- st_is_spherical(circuitos_provincia_nuevo)
# 
# # filtrar las filas con geometrías esféricas
# circuitos_provincia_nuevo <- my_sf[!spherical_rows, ]
# 
# mapview(circuitos_faltantes1)
# 
# 
# interseccion <- st_intersection(circuitos_provincia_nuevo_valid, circuitos_faltantes_valid)
