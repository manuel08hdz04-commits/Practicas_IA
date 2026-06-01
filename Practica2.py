import streamlit as st #Librería para crear interfaz web
import plotly.graph_objects as go #Librería para dibujar graficos
import random #Numeros ramdom
import time

st.set_page_config( #Configuración de página
    page_title="Insertion Sort Visualizer",
    layout="wide"
)

st.title("🔢 Insertion Sort Visualizer")

#Memoria de Streamlit 
#Generación de lista vacia para almacenar todos los numeros
if "datos" not in st.session_state:
    st.session_state.datos = []

# -------------------------
# Función para dibujar barras
# -------------------------
def mostrar_barras(datos, actual=None, comparado=None):

    colores = []

    for i in range(len(datos)):

        if i == actual:
            colores.append("red")

        elif i == comparado:
            colores.append("orange")

        else:
            colores.append("blue")

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=list(range(len(datos))),  #Verifica el numero de datos dentro de la lista para generar un rango y generar una lista con esa cantidad
            y=datos, #Almacena los numeros insertados en la lista
            marker_color=colores,
            text=datos,
            textposition="outside"
        )
    )

    fig.update_layout(
        height=500,
        xaxis_title="Posición",
        yaxis_title="Valor",
        showlegend=False
    )

    grafica.plotly_chart(
        fig,
        use_container_width=True
    )

# -------------------------
# Entrada
# -------------------------

st.subheader("Agregar números")

col1, col2, col3 = st.columns(3)

with col1:
    #Crea la caja  donde escribiremos los numeros
    numero = st.number_input(
        "Número",
        step=1,
        value=0
    )

    if st.button("➕ Agregar"): 
        #Si el usuario presiona el botón agregar agrega el numero a la lista

        st.session_state.datos.append(
            int(numero)
        )

with col2:

    cantidad = st.number_input(
        "Cantidad aleatoria",
        min_value=5,
        max_value=50,
        value=10
    )

    if st.button("🎲 Generar"):

        st.session_state.datos = [

            random.randint(1, 100) #Generación de valores entre 1 y 100

            for _ in range(cantidad)
        ]

with col3:

    if st.button("🗑 Limpiar"):

        st.session_state.datos = []

# -------------------------
# Mostrar lista
# -------------------------

st.subheader("Datos")

st.write(st.session_state.datos) #Mostrar lista

grafica = st.empty()

if len(st.session_state.datos) > 0:

    mostrar_barras(
        st.session_state.datos
    )

# -------------------------
# Ordenamiento
# -------------------------

iteraciones = st.empty()
tiempo_info = st.empty()

if st.button("▶ Ejecutar Insertion Sort"):

    datos = st.session_state.datos.copy()

    contador = 0

    inicio = time.time()

    for i in range(1, len(datos)): #Recorre el arreglo
        #Asignr vlor a variable temporal
        temp = datos[i]

        j = i - 1 #Comparar posición

        while j >= 0 and datos[j] > temp: 

            contador += 1

            datos[j + 1] = datos[j]

            mostrar_barras(
                datos,
                actual=j,
                comparado=j + 1
            )

            iteraciones.info(
                f"Iteraciones: {contador}"
            )

            time.sleep(0.4)

            j -= 1

        datos[j + 1] = temp

        mostrar_barras(
            datos,
            actual=j + 1
        )

        time.sleep(0.4)

    fin = time.time()

    st.session_state.datos = datos

    mostrar_barras(datos)

    tiempo_info.success(
        f"Tiempo total: {round(fin - inicio,4)} segundos"
    )

    st.success(
        "✅ Ordenamiento completado"
    )