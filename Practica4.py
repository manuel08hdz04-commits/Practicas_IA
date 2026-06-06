import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import random
import time

# =====================================
# CONFIGURACIÓN
# =====================================

st.set_page_config(
    page_title="Prim Visualizer",
    layout="wide"
)

st.title("🌳 Árbol Parcial Mínimo - Algoritmo de Prim")

# =====================================
# SESSION STATE
# =====================================

if "grafo" not in st.session_state:
    st.session_state.grafo = None

if "posiciones" not in st.session_state:
    st.session_state.posiciones = None

# =====================================
# GENERAR GRAFO
# =====================================

def generar_grafo(num_nodos):

    G = nx.Graph()

    letras = [chr(65+i) for i in range(num_nodos)]

    for nodo in letras:
        G.add_node(nodo)

    # Conectividad garantizada
    for i in range(num_nodos-1):

        G.add_edge(
            letras[i],
            letras[i+1],
            weight=random.randint(1,15)
        )

    # Aristas extras
    for _ in range(num_nodos):

        a = random.choice(letras)
        b = random.choice(letras)

        if a != b:

            G.add_edge(
                a,
                b,
                weight=random.randint(1,15)
            )

    return G

# =====================================
# DIBUJAR GRAFO
# =====================================

def dibujar_grafo(
    G,
    pos,
    visitados=None,
    mst_edges=None,
    actual=None
):

    if visitados is None:
        visitados = set()

    if mst_edges is None:
        mst_edges = []

    fig = go.Figure()

    # ----------------------
    # ARISTAS
    # ----------------------

    for edge in G.edges():

        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]

        color = "gray"
        ancho = 2

        for a, b in mst_edges:

            if (
                (edge[0] == a and edge[1] == b)
                or
                (edge[0] == b and edge[1] == a)
            ):

                color = "lime"
                ancho = 7

        fig.add_trace(
            go.Scatter(
                x=[x0,x1],
                y=[y0,y1],
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

    # ----------------------
    # NODOS
    # ----------------------

    x_nodes = []
    y_nodes = []
    colores = []
    textos = []

    for nodo in G.nodes():

        x,y = pos[nodo]

        x_nodes.append(x)
        y_nodes.append(y)

        color = "skyblue"

        if nodo in visitados:
            color = "green"

        if nodo == actual:
            color = "yellow"

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
            visible=False
        ),
        yaxis=dict(
            visible=False
        )
    )

    return fig

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

    if st.button("🎲 Generar nuevo grafo"):

        G = generar_grafo(cantidad)

        st.session_state.grafo = G

        st.session_state.posiciones = nx.spring_layout(
            G,
            seed=42
        )

# =====================================
# CREAR GRAFO INICIAL
# =====================================

if st.session_state.grafo is None:

    G = generar_grafo(cantidad)

    st.session_state.grafo = G

    st.session_state.posiciones = nx.spring_layout(
        G,
        seed=42
    )

G = st.session_state.grafo
pos = st.session_state.posiciones

nodos = list(G.nodes())

nodo_inicio = st.selectbox(
    "Nodo inicial",
    nodos
)

grafica = st.empty()

grafica.plotly_chart(
    dibujar_grafo(
        G,
        pos
    ),
    use_container_width=True
)

# =====================================
# ALGORITMO DE PRIM
# =====================================

if st.button("▶ Ejecutar Prim"):

    visitados = {nodo_inicio}

    mst_edges = []

    costo_total = 0

    tabla = st.empty()

    pasos = []

    while len(visitados) < len(G.nodes()):

        menor_peso = float("inf")
        mejor_arista = None

        for u in visitados:

            for v in G.neighbors(u):

                if v not in visitados:

                    peso = G[u][v]["weight"]

                    if peso < menor_peso:

                        menor_peso = peso
                        mejor_arista = (u,v)

        u,v = mejor_arista

        visitados.add(v)

        mst_edges.append((u,v))

        costo_total += menor_peso

        pasos.append(
            {
                "Origen": u,
                "Destino": v,
                "Peso": menor_peso,
                "Costo acumulado": costo_total
            }
        )

        grafica.plotly_chart(
            dibujar_grafo(
                G,
                pos,
                visitados,
                mst_edges,
                v
            ),
            use_container_width=True
        )

        tabla.table(pasos)

        time.sleep(1)

    grafica.plotly_chart(
        dibujar_grafo(
            G,
            pos,
            visitados,
            mst_edges
        ),
        use_container_width=True
    )

    st.success("Árbol Parcial Mínimo encontrado")

    st.success(
        f"Costo total del árbol = {costo_total}"
    )

    st.subheader("Aristas seleccionadas")

    for u,v in mst_edges:

        peso = G[u][v]["weight"]

        st.write(
            f"{u} → {v} (peso {peso})"
        )