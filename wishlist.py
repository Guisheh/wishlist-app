import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="🎅 Secret Santa Wishlist", page_icon="🎁")

st.title("🎁 Wishlist para el Secret Santa")
st.markdown("---")

# 2. Base de datos de Categorías (Lógica de "Especificar cada vez más")
categorias = {
    "Ropa": ["Remeras/Camisas", "Pantalones/Jeans", "Abrigos", "Ropa Interior/Medias", "Accesorios (Bufandas, Gorros)"],
    "Tecnología": ["Gadgets", "Periféricos PC", "Audio/Auriculares", "Accesorios Celular"],
    "Hobby/Ocio": ["Libros/Cómics", "Juegos de Mesa", "Artículos de Arte/Papelería", "Coleccionismo"],
    "Hogar/Cocina": ["Decoración", "Utensilios", "Tazas/Vasos", "Organizadores"],
    "Experiencias": ["Entradas Cine/Teatro", "Cenas/Desayunos", "Spa/Relax", "Cursos"],
    "Otros": ["Cualquier otra cosa"]
}

# 3. Inicializar el estado (Memoria temporal de la app)
if 'lista_regalos' not in st.session_state:
    st.session_state.lista_regalos = []

# --- BARRA LATERAL (Ingreso de Usuario) ---
with st.sidebar:
    st.header("👤 ¿Quién eres?")
    nombre_usuario = st.text_input("Ingresa tu nombre:")
    st.info("Ingresa tu nombre para empezar a agregar deseos a tu lista.")

# --- CUERPO PRINCIPAL ---

if nombre_usuario:
    st.subheader(f"Hola, {nombre_usuario}. ¡Arma tu lista!")
    
    # Formulario para agregar nuevo deseo
    with st.form("wish_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Nivel 1: Categoría General
            cat_seleccionada = st.selectbox("1. Elige un Rubro", options=list(categorias.keys()))
        
        with col2:
            # Nivel 2: Subcategoría (Dinámica según el rubro)
            sub_opciones = categorias[cat_seleccionada]
            sub_cat_seleccionada = st.selectbox("2. Especifica el tipo", options=sub_opciones)
            
        # Nivel 3: Detalles Específicos
        detalle = st.text_area("3. Detalles exactos (Talle, Color, Modelo, Link de referencia)", 
                               placeholder="Ej: Talle L, color azul marino. Si es posible, de la marca X...")
        
        # Botón de envío
        submitted = st.form_submit_button("➕ Agregar a mi lista")
        
        if submitted and detalle:
            nuevo_deseo = {
                "Nombre": nombre_usuario,
                "Rubro": cat_seleccionada,
                "Tipo": sub_cat_seleccionada,
                "Detalle": detalle
            }
            st.session_state.lista_regalos.append(nuevo_deseo)
            st.success("¡Deseo agregado!")
        elif submitted and not detalle:
            st.warning("Por favor, escribe algún detalle específico para ayudar a tu Santa.")

    # --- MOSTRAR LA LISTA ---
    st.markdown("---")
    st.subheader("📝 Lista Global de Deseos")
    
    if len(st.session_state.lista_regalos) > 0:
        df = pd.DataFrame(st.session_state.lista_regalos)
        
        # Mostramos una tabla interactiva
        st.dataframe(df, use_container_width=True)
        
        # Opción de descargar la lista en CSV (Excel)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar lista completa (CSV)",
            data=csv,
            file_name='wishlist_secret_santa.csv',
            mime='text/csv',
        )
        
        # Botón para limpiar lista (opcional)
        if st.button("Borrar toda la lista (Reiniciar)"):
            st.session_state.lista_regalos = []
            st.rerun()
            
    else:
        st.info("Aún no hay deseos cargados. ¡Sé el primero!")

else:
    st.write("👈 Por favor, ingresa tu nombre en la barra lateral para comenzar.")
