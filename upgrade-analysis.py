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
        atr = row[atrib]
        if (atr < 50):
            atr = "Presupuesto bajo"
        elif (atr > 50):
            atr = "Presupuesto medio"
        elif (atr > 100):
            atr = "Presupuesto alto"
        atrib_str = str(row[atrib])
        atr = atrib_str.split('|')
        values.append(atr)
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

diccionario__cert = define_atrib(movies_df, 'certification') 
dic_genre = define_atrib(movies_df, 'genre')

gr_cert = grafo_relacion(diccionario__cert)
gr_genre = grafo_relacion(dic_genre)

visualiza(gr_cert)
visualiza(gr_genre)

com_gr = nx.community.greedy_modularity_communities(gr_genre)
com_cert = nx.community.greedy_modularity_communities(gr_cert)


def dic_comunidades(c, tam_comunidades):
    comunidades = {}
    for i , comm in enumerate(c):
        if len(comm) > tam_comunidades:
            comunidades[i] = list(comm)
    return comunidades

comunidades_gr = dic_comunidades(com_gr,2)
comunidades_cert = dic_comunidades(com_cert, 6)


