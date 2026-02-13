import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os

# Configuración de la página
st.set_page_config(
    page_title="Reportes Google Sheets",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar session state
if "urls_cargadas" not in st.session_state:
    st.session_state.urls_cargadas = []
if "ultimo_intervalo" not in st.session_state:
    st.session_state.ultimo_intervalo = 60
if "auto_refresh_activos" not in st.session_state:
    st.session_state.auto_refresh_activos = {}

st.title("📊 Generador de Reportes Interactivos - Google Sheets")

# Verificar autenticación y mostrar instrucciones si es necesario
autenticacion_disponible = False
try:
    autenticacion_disponible = (
        "google_service_account" in st.secrets or 
        os.path.exists("credentials.json")
    )
except:
    pass

if not autenticacion_disponible:
    st.warning("⚠️ **Autenticación no configurada**")
    with st.expander("📝 Haz clic aquí para configurar las credenciales", expanded=False):
        st.markdown("""
        ### Opción 1: Streamlit Cloud 🌐 (Recomendado)
        1. Ve a tu app en [Streamlit Community Cloud](https://share.streamlit.io)
        2. Haz clic en el menú (⋮) → **Settings** 
        3. Selecciona **Secrets** en la barra lateral
        4. En el editor de texto, pega tu archivo `credentials.json` con este formato:
        ```
        [google_service_account]
        type = "service_account"
        project_id = "tu-proyecto"
        private_key_id = "..."
        private_key = "-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n"
        client_email = "tu-servicio@tu-proyecto.iam.gserviceaccount.com"
        client_id = "..."
        auth_uri = "https://accounts.google.com/o/oauth2/auth"
        token_uri = "https://oauth2.googleapis.com/token"
        auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
        client_x509_cert_url = "..."
        ```
        5. Haz clic en **Save**
        
        ### Opción 2: Convertir a Sheet Público 🔓
        1. Abre tu Google Sheet
        2. Haz clic en **Compartir** (esquina superior derecha)
        3. Selecciona **Cambiar** → **Cualquier persona con el link** → **Lector**
        4. Copia el link del sheet
        5. **¡Ya funciona sin credenciales!**
        """)

# Función para autenticar con Google Sheets
@st.cache_resource
def autenticar_google_sheets():
    """Autentica con Google Sheets usando credenciales de servicio o Streamlit Secrets"""
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets.readonly",
            "https://www.googleapis.com/auth/drive.readonly"
        ]
        
        # Método 1: Streamlit Secrets (para Streamlit Cloud)
        if "google_service_account" in st.secrets:
            try:
                creds_dict = st.secrets["google_service_account"]
                creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
                return gspread.authorize(creds)
            except Exception as e:
                st.error(f"Error al autenticar con Secrets: {e}")
                return None
        
        # Método 2: Archivo local (para desarrollo local)
        elif os.path.exists("credentials.json"):
            creds = Credentials.from_service_account_file(
                "credentials.json", scopes=scopes
            )
            return gspread.authorize(creds)
        
        # Método 3: No autenticado (solo para sheets públicas)
        else:
            return None
            
    except Exception as e:
        st.error(f"Error al autenticar: {e}")
        return None

# Función para cargar datos de Google Sheets con caché
@st.cache_data(ttl=60)
def cargar_datos_google_sheets(url):
    """Carga datos de un URL de Google Sheets"""
    try:
        gc = autenticar_google_sheets()
        sheet_id = extraer_id_sheet(url)
        
        if not sheet_id:
            st.error("URL inválida. Por favor, usa un URL de Google Sheets válido.")
            return None
        
        try:
            # Intentar acceso autenticado
            if gc is not None:
                sh = gc.open_by_key(sheet_id)
            else:
                # Acceso sin autenticación (solo sheets públicos)
                gc_public = gspread.Client(auth=None)
                sh = gc_public.open_by_key(sheet_id)
            
            # Cargar todas las hojas
            datos_hojas = {}
            for worksheet in sh.worksheets():
                datos = worksheet.get_all_records()
                if datos:
                    datos_hojas[worksheet.title] = pd.DataFrame(datos)
            
            if not datos_hojas:
                st.warning("⚠️ El sheet no tiene datos o está vacío")
                return None
            
            return datos_hojas
            
        except Exception as e:
            error_msg = str(e).lower()
            if "not found" in error_msg or "404" in error_msg:
                st.error("❌ Sheet no encontrado. Verifica que el ID sea correcto.")
            elif "permission" in error_msg or "unauthorized" in error_msg or "forbidden" in error_msg:
                st.error("""
                ❌ No tienes permiso para acceder a este sheet.
                
                **Opciones:**
                1. **Convertir a público**: Abre el sheet → Compartir → Selecciona "Cualquier persona con el link" → Copiable
                2. **Configurar Streamlit Secrets**: Ve a Streamlit dashboard → Settings → Secrets → Añade tu `credentials.json`
                3. **Compartir con la cuenta de servicio**: Acceso directo con correo de credenciales
                """)
            else:
                st.error(f"Error al cargar datos: {e}")
            return None
            
    except Exception as e:
        st.error(f"Error inesperado: {e}")
        return None

# Función para procesar un archivo con URLs
def procesar_archivo_urls(archivo):
    """Procesa un archivo Excel o de texto con URLs de Google Sheets"""
    try:
        # Si es un archivo Excel
        if archivo.name.endswith('.xlsx') or archivo.name.endswith('.xls'):
            import openpyxl
            df = pd.read_excel(archivo)
            # Buscar URLs en todas las columnas
            urls = []
            for col in df.columns:
                for val in df[col]:
                    if isinstance(val, str) and "docs.google.com/spreadsheets" in val.lower():
                        urls.append(val.strip())
            return urls if urls else []
        else:
            # Si es un archivo de texto
            contenido = archivo.read().decode("utf-8")
            urls = [url.strip() for url in contenido.split("\n") if url.strip() and "docs.google.com" in url.lower()]
            return urls
    except Exception as e:
        st.error(f"Error al procesar archivo: {e}")
        return []

# Función para extraer ID de diferentes formatos de URL
def extraer_id_sheet(url):
    """Extrae el ID del sheet de diferentes formatos de URL"""
    try:
        url = url.strip()
        # Formato estándar: /d/{ID}/
        if "/d/" in url and "/pubhtml" not in url:
            sheet_id = url.split("/d/")[1].split("/")[0].strip()
            if sheet_id:
                return sheet_id
        # Formato de publicación: /d/e/{ID}/pubhtml
        elif "/d/e/" in url:
            sheet_id = url.split("/d/e/")[1].split("/")[0].strip()
            if sheet_id:
                return sheet_id
        return None
    except:
        return None

# Barra lateral - Cargar URLs
st.sidebar.title("⚙️ Configuración")
st.sidebar.divider()

st.sidebar.subheader("1. Cargar URLs de Google Sheets")

# Detectar si estamos en Streamlit Cloud
es_streamlit_cloud = False
try:
    es_streamlit_cloud = "streamlit.app" in st.config.get_config_object().server.get("server_address", "")
except:
    pass

if es_streamlit_cloud:
    st.sidebar.info("📝 **En Streamlit Cloud**: Pega directamente tu link de Google Sheets")
    metodo_carga = "directo"
else:
    metodo_carga = st.sidebar.radio(
        "Elige el método de carga:",
        ["📥 Subir archivo Excel/Texto", "📝 Pegar URLs directamente"]
    )

urls_sheets = []

if metodo_carga == "📥 Subir archivo Excel/Texto" and not es_streamlit_cloud:
    archivo_cargado = st.sidebar.file_uploader(
        "Sube un archivo Excel (.xlsx) o texto (.txt) con URLs",
        type=["txt", "xlsx", "xls"]
    )
    if archivo_cargado:
        urls_sheets = procesar_archivo_urls(archivo_cargado)
        if urls_sheets:
            st.session_state.urls_cargadas = urls_sheets
            st.sidebar.success(f"✅ {len(urls_sheets)} URL(s) cargada(s)")
else:
    texto_urls = st.sidebar.text_area(
        "Pega las URLs de Google Sheets (una por línea):",
        height=100,
        placeholder="https://docs.google.com/spreadsheets/d/e/2PACX-1v.../pubhtml"
    )
    # Procesar URLs con validación robusta
    urls_items = texto_urls.split("\n")
    urls_sheets = []
    for url in urls_items:
        url_limpio = url.strip()
        if url_limpio and "google.com" in url_limpio.lower() and "spreadsheets" in url_limpio.lower():
            sheet_id = extraer_id_sheet(url_limpio)
            if sheet_id:
                urls_sheets.append(url_limpio)
    
    if urls_sheets:
        st.session_state.urls_cargadas = urls_sheets
        st.sidebar.success(f"✅ {len(urls_sheets)} URL(s) válida(s)")
    elif texto_urls.strip() and "google.com" in texto_urls.lower():
        st.sidebar.warning("⚠️ No se pudo extraer ID válido")

# Usar URLs guardadas en session state si existen
if not urls_sheets and st.session_state.urls_cargadas:
    urls_sheets = st.session_state.urls_cargadas

# Intervalo de actualización
st.sidebar.divider()
st.sidebar.subheader("2. Configuración de Actualización")
intervalo_actualizacion = st.sidebar.slider(
    "Intervalo de actualización (segundos)",
    min_value=30,
    max_value=300,
    value=60,
    step=10
)
st.session_state.ultimo_intervalo = intervalo_actualizacion

# Contenido principal
if urls_sheets:
    # Crear tabs para cada URL
    tabs = st.tabs([f"Sheet {i+1}" for i in range(len(urls_sheets))])
    
    for tab_idx, (tab, url) in enumerate(zip(tabs, urls_sheets)):
        with tab:
            st.subheader(f"Google Sheet #{tab_idx + 1}")
            st.caption(f"URL: {url[:60]}...")
            
            # Botón para limpiar caché y actualizar
            col1, col2 = st.columns([1, 2])
            
            with col1:
                if st.button(f"🔄 Actualizar", key=f"btn_{tab_idx}"):
                    st.cache_data.clear()
                    st.rerun()
            
            with col2:
                st.caption("Haz clic para forzar actualización de datos")
            
            # Cargar datos
            datos_hojas = cargar_datos_google_sheets(url)
            
            if datos_hojas:
                # Seleccionar hoja
                nombre_hoja = st.selectbox(
                    "Selecciona una hoja:",
                    list(datos_hojas.keys()),
                    key=f"sheet_select_{tab_idx}"
                )
                
                df = datos_hojas[nombre_hoja]
                
                # Mostrar información
                col1, col2, col3 = st.columns(3)
                col1.metric("📊 Filas", len(df))
                col2.metric("🏷️ Columnas", len(df.columns))
                col3.metric("🕐 Última actualización", datetime.now().strftime("%H:%M:%S"))
                
                st.divider()
                
                # Pestañas de visualización
                tab_vista, tab_datos, tab_analisis = st.tabs(["👁️ Vista Previa", "📋 Datos Completos", "📈 Análisis"])
                
                with tab_vista:
                    st.subheader("Vista Previa de Datos")
                    st.dataframe(df.head(10), use_container_width=True)
                
                with tab_datos:
                    st.subheader("Datos Completos")
                    
                    # Filtros de búsqueda
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        columna_filtro = st.selectbox(
                            "Filtrar por columna:",
                            df.columns,
                            key=f"col_filtro_{tab_idx}"
                        )
                    
                    with col2:
                        valor_filtro = st.text_input(
                            "Búsqueda:",
                            key=f"val_filtro_{tab_idx}"
                        )
                    
                    # Aplicar filtro
                    if valor_filtro:
                        df_filtrado = df[
                            df[columna_filtro].astype(str).str.contains(
                                valor_filtro, case=False, na=False
                            )
                        ]
                    else:
                        df_filtrado = df
                    
                    st.dataframe(df_filtrado, use_container_width=True)
                    
                    # Descargar datos
                    csv = df_filtrado.to_csv(index=False)
                    st.download_button(
                        label="📥 Descargar como CSV",
                        data=csv,
                        file_name=f"reporte_{nombre_hoja}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        key=f"download_{tab_idx}"
                    )
                
                with tab_analisis:
                    st.subheader("Análisis de Datos")
                    
                    # Obtener columnas numéricas
                    columnas_numericas = df.select_dtypes(include=['number']).columns.tolist()
                    
                    if columnas_numericas:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            col_x = st.selectbox(
                                "Eje X:",
                                df.columns,
                                key=f"col_x_{tab_idx}"
                            )
                        
                        with col2:
                            col_y = st.selectbox(
                                "Eje Y:",
                                columnas_numericas,
                                key=f"col_y_{tab_idx}"
                            )
                        
                        tipo_grafico = st.selectbox(
                            "Tipo de gráfico:",
                            ["Línea", "Barras", "Dispersión", "Área"],
                            key=f"tipo_graf_{tab_idx}"
                        )
                        
                        # Generar gráfico
                        try:
                            if tipo_grafico == "Línea":
                                fig = px.line(df, x=col_x, y=col_y, markers=True)
                            elif tipo_grafico == "Barras":
                                fig = px.bar(df, x=col_x, y=col_y)
                            elif tipo_grafico == "Dispersión":
                                fig = px.scatter(df, x=col_x, y=col_y)
                            else:  # Área
                                fig = px.area(df, x=col_x, y=col_y)
                            
                            fig.update_layout(height=500, template="plotly_white")
                            st.plotly_chart(fig, use_container_width=True)
                        except Exception as e:
                            st.error(f"Error al crear gráfico: {e}")
                        
                        # Estadísticas
                        st.subheader("📊 Estadísticas")
                        col1, col2, col3, col4 = st.columns(4)
                        
                        try:
                            col1.metric("Mínimo", f"{df[col_y].min():.2f}")
                            col2.metric("Máximo", f"{df[col_y].max():.2f}")
                            col3.metric("Promedio", f"{df[col_y].mean():.2f}")
                            col4.metric("Desv. Est.", f"{df[col_y].std():.2f}")
                        except Exception as e:
                            st.warning(f"Error al calcular estadísticas: {e}")
                    else:
                        st.info("No hay columnas numéricas para analizar.")
            else:
                st.error("No se pudieron cargar los datos. Verifica la URL y las credenciales.")
else:
    st.info("👈 Carga las URLs de Google Sheets en la barra lateral para comenzar.")

# Footer
st.divider()
st.caption("🔄 Los reportes se actualizan automáticamente según el intervalo configurado. Nota: Requiere autenticación con Google Cloud.")
