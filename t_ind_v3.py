import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
#from collections import Counter

# Carga el conjunto de datos
movies_df = pd.read_csv('lowest_ranked_movies_data.csv')

def define_atrib(datos, atrib):
    keys = []
    values = []
    for index, row in datos.iterrows():
        # Campos a analizar
        movie_title = row['name']
        keys.append(movie_title)
        genres = row[atrib].split('|')
        values.append(genres)
        #actors = row['stars'].split('|')
    diccionario = dict(zip(keys, values))
    return diccionario

def grafo_relacion(diccionario):
    grafo = nx.Graph()
    for key in diccionario:
        #print(key)
        # Si no tenemos el nodo lo creeamos
        if not grafo.has_node(key): 
            grafo.add_node(key)
        generos = diccionario[key]
        for key_2 in diccionario:
            #print(key_2)
            if not grafo.has_node(key_2): 
                grafo.add_node(key_2)
            generos_peli2 = diccionario[key_2]
            if key != key_2 : # Si no es lo mismo
                for genero in generos:
                    if genero in generos_peli2:
                        # Añadimos la arista
                        grafo.add_edge(key, key_2) 
    
    return grafo

def visualiza(grafo):
    pos = nx.spring_layout(grafo)
    nx.draw(grafo, pos, with_labels=True, font_size=6, node_size=10,
             node_color='skyblue', font_color='black', font_weight='bold', 
             edge_color='gray', linewidths=0.1)
    plt.show() 

diccionario_atrib = define_atrib(movies_df, 'genre') 
#print(diccionario_atrib['Disaster Movie'])
gr = grafo_relacion(diccionario_atrib)

visualiza(gr)

# Calcularemos las comunidades

communities = nx.community.greedy_modularity_communities(gr)

def dic_comunidades(c, tam_comunidades):
    comunidades = {}
    for i , comm in enumerate(c):
        if len(comm) > tam_comunidades:
            comunidades[i] = list(comm)
    return comunidades


comunidades_mayor_2 = dic_comunidades(communities,2)

def analisis(dic_atributos, dic_comunidades):

    analisis_atrib = {}
    for i in dic_comunidades:
        ls_films = dic_comunidades[i]
        # La comunidad comparte todos los generos con lo que podemos coger cualquiera
        ls_genero = dic_atributos[ls_films[0]]
        #print(ls_genero)
        #print(dic_comunidades[i])
        """ Crearemos un diccionario 
            que tendrá de key el indice de la comunidad y de valor
            una tupla de genero y pelis asociadas al genero"""
        #analisis_atrib[i]= (ls_genero[0],ls_films)
        analisis_atrib[len(ls_films)] = ls_genero[0]
    return analisis_atrib

#print(analisis(diccionario_atrib, comunidades_mayor_2))

analizado = analisis(diccionario_atrib, comunidades_mayor_2)

#print(analizado.values())

print(analizado)

def visualiza_analisis(diccionario):

    numero_pelis = diccionario.keys()
    generos = diccionario.values()

    #generos = val[0]
    #cantidad_pelis = len(val[1])
    plt.bar(generos, numero_pelis)

    plt.xlabel('Generos')
    plt.ylabel('Numero de pelis comunidad')
    plt.title('Generos de las peliculas peor valoradas en IMDB')

    # Mostrar el gráfico
    plt.show()


visualiza_analisis(analizado)

def grafo_pelis_analizadas(dic_atrib, dic_analizado):

    g = nx.Graph()
    for analizar in dic_analizado:
        cont = 0
        ls_generos = dic_analizado[analizar]
        #print(ls_generos)
        ls_pelis = []
        for peli in dic_atrib:
            generos = dic_atrib[peli][0]
            #print(generos)
            if ls_generos == generos:
                ls_pelis.append(peli)
        #print(ls_pelis)
        for nodo in ls_pelis:
            if not g.has_node(nodo):
                g.add_node(nodo)
            for n in ls_pelis:
                if nodo != n:
                    if not g.has_edge(nodo, n):
                        g.add_edge(nodo, n)
        
        cont += 1
    
    return g

grafo_analisis = grafo_pelis_analizadas(diccionario_atrib, analizado)

visualiza(grafo_analisis)
