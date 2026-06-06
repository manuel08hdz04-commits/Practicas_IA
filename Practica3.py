'''import math
#Creación de diccionario
grafo = {
    'A': {'B': 4, 'C': 2},
    'B': {'A': 4, 'C': 1, 'D': 5},
    'C': {'A': 2, 'B': 1, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

#Creación de función que recibira un grafo y un nodo inicial
def dijkstra(grafo, inicio):

    distancias = {} #   Crea una tabla vacia

    visitados = set() #Guarda los nodos ya procesados

    #Inicializar distancias
    for nodo in grafo:
        distancias[nodo] = math.inf #Asigna un infinito a todas las distancias

    distancias[inicio] = 0 #Asigna un "0" al Nodo inicial

    #Mientras existan nodos sin visitar
    while len(visitados) < len(grafo):

        actual = None
    #Recorrer todos los nodos
        for nodo in grafo:
            #Ignora los ya visitados
            if nodo not in visitados:
                #Encuentra el nodo menor
                if actual is None:
                    #Guarda el nodo
                    actual = nodo
                #Comparar distancias "Este nodo es menor?"
                elif distancias[nodo] < distancias[actual]:
                    #Si, si es menor se convierte en el nuevo candidato
                    actual = nodo

        print("\n===================")
        print(f"Visitando nodo {actual}")
        print("===================")

        visitados.add(actual)
    #Revisa la distancia que hay entre el nodo visitado y sus vecinos
        for vecino, peso in grafo[actual].items():
            

            nueva_distancia = (
                distancias[actual] + peso
            )
            #Encontre una ruta con menos distnacia?
            if nueva_distancia < distancias[vecino]:

                print(
                    f"Actualizando {vecino}: "
                    f"{distancias[vecino]} -> "
                    f"{nueva_distancia}"
                )
                #Actualiza tabla
                distancias[vecino] = nueva_distancia

        print("\nDistancias actuales:")
        #Realiza un barrido entre nodos para mostras sus distancias
        for nodo in distancias:

            print(
                f"{nodo}: {distancias[nodo]}"
            )
    #Asignar distancias a los nodos
    return distancias

#LLamado a la función
resultado = dijkstra(grafo, 'A')

print("\nRESULTADO FINAL")
#Muestra el resultado
for nodo in resultado:

    print(
        f"{nodo}: {resultado[nodo]}"
    )'''
import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import random
import math
import time

# =====================================
# CONFIGURACIÓN
# =====================================

st.set_page_config(
    page_title="Dijkstra Visualizer",
    layout="wide"
)

st.title("🗺️ Visualizador del Algoritmo de Dijkstra")

# =====================================
# SESSION STATE
# =====================================

if "grafo" not in st.session_state:
    st.session_state.grafo = None

if "posiciones" not in st.session_state:
    st.session_state.posiciones = None

# =====================================
# GENERAR MAPA ALEATORIO
# =====================================

def generar_grafo(num_nodos):

    G = nx.Graph()

    letras = []

    for i in range(num_nodos):
        letras.append(chr(65 + i))

    for nodo in letras:
        G.add_node(nodo)

    # garantizar conectividad
    for i in range(num_nodos - 1):

        peso = random.randint(1, 15)

        G.add_edge(
            letras[i],
            letras[i + 1],
            weight=peso
        )

    # conexiones extras
    conexiones_extra = num_nodos

    for _ in range(conexiones_extra):

        a = random.choice(letras)
        b = random.choice(letras)

        if a != b:

            peso = random.randint(1, 15)

            G.add_edge(
                a,
                b,
                weight=peso
            )

    return G

# =====================================
# DIBUJAR GRAFO
# =====================================

def dibujar_grafo(
    G,
    pos,
    visitados=None,
    actual=None,
    destino=None,
    ruta=None
):

    if visitados is None:
        visitados = set()

    if ruta is None:
        ruta = []

    fig = go.Figure()

    # -------------------------
    # ARISTAS
    # -------------------------

    for edge in G.edges():

        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]

        color = "gray"
        ancho = 2

        if ruta:

            for i in range(len(ruta)-1):

                a = ruta[i]
                b = ruta[i+1]

                if (
                    (edge[0] == a and edge[1] == b)
                    or
                    (edge[0] == b and edge[1] == a)
                ):

                    color = "purple"
                    ancho = 6

        fig.add_trace(
            go.Scatter(
                x=[x0, x1],
                y=[y0, y1],
                mode="lines",
                line=dict(
                    width=ancho,
                    color=color
                ),
                hoverinfo="none",
                showlegend=False
            )
        )

        peso = G[edge[0]][edge[1]]["weight"]

        fig.add_trace(
            go.Scatter(
                x=[(x0+x1)/2],
                y=[(y0+y1)/2],
                mode="text",
                text=[str(peso)],
                showlegend=False
            )
        )

    # -------------------------
    # NODOS
    # -------------------------

    x_nodes = []
    y_nodes = []
    colores = []
    textos = []

    for nodo in G.nodes():

        x, y = pos[nodo]

        x_nodes.append(x)
        y_nodes.append(y)

        color = "skyblue"

        if nodo in visitados:
            color = "green"

        if nodo == actual:
            color = "yellow"

        if nodo == destino:
            color = "red"

        if nodo in ruta:
            color = "purple"

        colores.append(color)

        textos.append(nodo)

    fig.add_trace(
        go.Scatter(
            x=x_nodes,
            y=y_nodes,
            mode="markers+text",
            text=textos,
            textposition="middle center",
            marker=dict(
                size=40,
                color=colores
            ),
            showlegend=False
        )
    )

    fig.update_layout(
        height=700,
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font_color="white",
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            visible=False
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            visible=False
        )
    )

    return fig

# =====================================
# RECONSTRUIR RUTA
# =====================================

def reconstruir(predecesor, inicio, destino):

    ruta = []

    actual = destino

    while actual is not None:

        ruta.append(actual)

        actual = predecesor[actual]

    ruta.reverse()

    return ruta

# =====================================
# CONTROLES
# =====================================

col1, col2 = st.columns(2)

with col1:

    cantidad = st.slider(
        "Número de nodos",
        5,
        20,
        8
    )

with col2:

    if st.button("🎲 Generar nuevo mapa"):

        G = generar_grafo(cantidad)

        st.session_state.grafo = G

        st.session_state.posiciones = nx.spring_layout(
            G,
            seed=42
        )

# =====================================
# SI NO EXISTE MAPA
# =====================================

if st.session_state.grafo is None:

    G = generar_grafo(cantidad)

    st.session_state.grafo = G

    st.session_state.posiciones = nx.spring_layout(
        G,
        seed=42
    )

# =====================================
# GRAFO ACTUAL
# =====================================

G = st.session_state.grafo
pos = st.session_state.posiciones

nodos = list(G.nodes())

col1, col2 = st.columns(2)

with col1:

    inicio = st.selectbox(
        "Origen",
        nodos
    )

with col2:

    destino = st.selectbox(
        "Destino",
        nodos,
        index=min(1, len(nodos)-1)
    )

grafica = st.empty()

grafica.plotly_chart(
    dibujar_grafo(
        G,
        pos,
        destino=destino
    ),
    use_container_width=True
)

# =====================================
# EJECUTAR DIJKSTRA
# =====================================

if st.button("▶ Ejecutar Dijkstra"):

    distancias = {
        nodo: math.inf
        for nodo in G.nodes()
    }

    predecesor = {
        nodo: None
        for nodo in G.nodes()
    }

    visitados = set()

    distancias[inicio] = 0

    tabla = st.empty()

    while len(visitados) < len(G.nodes()):

        actual = None

        for nodo in G.nodes():

            if nodo not in visitados:

                if actual is None:

                    actual = nodo

                elif (
                    distancias[nodo]
                    <
                    distancias[actual]
                ):

                    actual = nodo

        visitados.add(actual)

        for vecino in G.neighbors(actual):

            peso = G[actual][vecino]["weight"]

            nueva = (
                distancias[actual]
                + peso
            )

            if nueva < distancias[vecino]:

                distancias[vecino] = nueva

                predecesor[vecino] = actual

        grafica.plotly_chart(
            dibujar_grafo(
                G,
                pos,
                visitados,
                actual,
                destino
            ),
            use_container_width=True
        )

        tabla.table(
            {
                "Nodo": list(distancias.keys()),
                "Distancia": list(distancias.values())
            }
        )

        time.sleep(0.7)

    ruta = reconstruir(
        predecesor,
        inicio,
        destino
    )

    grafica.plotly_chart(
        dibujar_grafo(
            G,
            pos,
            visitados,
            None,
            destino,
            ruta
        ),
        use_container_width=True
    )

    st.success(
        f"Ruta más corta: {' → '.join(ruta)}"
    )

    st.success(
        f"Costo total: {distancias[destino]}"
    )