import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import random
import time

# =====================================
# CONFIGURACIÓN
# =====================================

st.set_page_config(
    page_title="Kruskal Visualizer",
    layout="wide"
)

st.title("🌳 Árbol de Máximo y Mínimo Coste - Kruskal")

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

    # Garantizar conectividad
    for i in range(num_nodos - 1):

        G.add_edge(
            letras[i],
            letras[i+1],
            weight=random.randint(1,15)
        )

    # Conexiones extras
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
    mst_edges=None,
    actual=None
):

    if mst_edges is None:
        mst_edges = []

    fig = go.Figure()

    # -------------------
    # ARISTAS
    # -------------------

    for edge in G.edges():

        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]

        color = "gray"
        ancho = 2

        for a,b in mst_edges:

            if (
                (edge[0]==a and edge[1]==b)
                or
                (edge[0]==b and edge[1]==a)
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

    # -------------------
    # NODOS
    # -------------------

    x_nodes = []
    y_nodes = []
    colores = []
    textos = []

    for nodo in G.nodes():

        x,y = pos[nodo]

        x_nodes.append(x)
        y_nodes.append(y)

        color = "skyblue"

        if actual is not None:

            if nodo in actual:
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
# UNION FIND
# =====================================

def find(padre, nodo):

    if padre[nodo] != nodo:

        padre[nodo] = find(
            padre,
            padre[nodo]
        )

    return padre[nodo]


def union(padre, a, b):

    raizA = find(padre, a)
    raizB = find(padre, b)

    if raizA != raizB:

        padre[raizB] = raizA

        return True

    return False

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
# CREAR GRAFO
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

# =====================================
# OPCIONES
# =====================================

modo = st.radio(
    "Tipo de Árbol",
    [
        "Mínimo Coste",
        "Máximo Coste"
    ]
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
# KRUSKAL
# =====================================

if st.button("▶ Ejecutar Kruskal"):

    padre = {}

    for nodo in G.nodes():

        padre[nodo] = nodo

    mst_edges = []

    costo_total = 0

    pasos = []

    tabla = st.empty()

    # -------------------
    # Obtener aristas
    # -------------------

    aristas = []

    for u,v,data in G.edges(data=True):

        aristas.append(
            (
                data["weight"],
                u,
                v
            )
        )

    # -------------------
    # Ordenar
    # -------------------

    if modo == "Mínimo Coste":

        aristas.sort()

    else:

        aristas.sort(
            reverse=True
        )

    st.subheader("Aristas ordenadas")

    st.write(aristas)

    # -------------------
    # KRUSKAL
    # -------------------

    paso = 1

    for peso,u,v in aristas:

        if union(
            padre,
            u,
            v
        ):

            mst_edges.append(
                (u,v)
            )

            costo_total += peso

            accion = "Agregada"

        else:

            accion = "Ciclo - Descartada"

        pasos.append(
            {
                "Paso": paso,
                "Origen": u,
                "Destino": v,
                "Peso": peso,
                "Acción": accion,
                "Costo acumulado": costo_total
            }
        )

        grafica.plotly_chart(
            dibujar_grafo(
                G,
                pos,
                mst_edges,
                (u,v)
            ),
            use_container_width=True
        )

        tabla.table(pasos)

        time.sleep(0.8)

        paso += 1

        if len(mst_edges) == len(G.nodes()) - 1:
            break

    # -------------------
    # RESULTADO FINAL
    # -------------------

    grafica.plotly_chart(
        dibujar_grafo(
            G,
            pos,
            mst_edges
        ),
        use_container_width=True
    )

    st.success(
        f"Costo total del árbol: {costo_total}"
    )

    st.subheader("Aristas seleccionadas")

    for u,v in mst_edges:

        peso = G[u][v]["weight"]

        st.write(
            f"{u} ↔ {v}  (peso {peso})"
        )