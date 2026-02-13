# Configuración para ejecutar la aplicación Streamlit

## 📋 Requisitos Previos

1. Python 3.8 o superior instalado
2. Cuenta de Google Cloud con acceso a Google Sheets API
3. Git para clonar/desplegar el repositorio

## 🔐 Configuración de Google Cloud

### Paso 1: Crear un proyecto en Google Cloud Console

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto
3. Activa estas APIs:
   - Google Sheets API
   - Google Drive API

### Paso 2: Crear credenciales de servicio

1. Dirígete a "Credenciales" en la consola de Google Cloud
2. Crea una nueva credencial seleccionando "Cuenta de Servicio"
3. Completa los detalles básicos
4. Descarga la clave JSON
5. Renombra el archivo a `credentials.json` y colócalo en la carpeta del proyecto

### Paso 3: Compartir Google Sheets con la cuenta de servicio

1. Abre el archivo JSON descargado
2. Copia el email de la cuenta de servicio (campo "client_email")
3. En tus Google Sheets, comparte el documento con ese email

## 🚀 Instalación y Ejecución Local

### 1. Clonar o descargar el repositorio
```bash
git clone <tu-repositorio>
cd automatizada
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación
```bash
streamlit run app.py
```

La aplicación se abrirá en tu navegador en `http://localhost:8501`

## 🌐 Desplegar en Streamlit Cloud

### Opción 1: Desde GitHub (Recomendado)

1. Sube tu repositorio a GitHub
2. Ve a [Streamlit Cloud](https://share.streamlit.io/)
3. Haz clic en "New app"
4. Selecciona tu repositorio y rama
5. Selecciona `app.py` como archivo principal
6. Haz clic en "Deploy"

### Opción 2: Configurar secretos en Streamlit Cloud

Después de desplegar, ve a los Settings de tu aplicación y añade:

1. Copia el contenido completo del archivo `credentials.json`
2. En "Secrets", añade:
```toml
[secrets]
google_credentials = """
{
  "type": "service_account",
  "project_id": "tu-project-id",
  ...
}
"""
```

Luego actualiza el `app.py` para usar:
```python
import json
import streamlit as st
creds_dict = json.loads(st.secrets["google_credentials"])
```

## 📁 Uso de Archivos de URLs

### Opción 1: Archivo Excel (.xlsx) ✨ **RECOMENDADO**

Crea un archivo Excel con las URLs en una columna:

```
| URLs de Google Sheets |
|----------------------|
| https://docs.google.com/spreadsheets/d/1aBcDeFgHiJkLmNoPqRsTuVwXyZ123456/edit |
| https://docs.google.com/spreadsheets/d/e/2PACX-1vRtmL2ZeNzRJSApaCwn6ilV715IoSyoijjQ_TvPESVQ8geCOUqT0kTwjxMGQAm0s3CdnahmuCGj97kf/pubhtml |
```

### Opción 2: Archivo de Texto (.txt)

Archivo de texto con una URL por línea:

```
https://docs.google.com/spreadsheets/d/1aBcDeFgHiJkLmNoPqRsTuVwXyZ123456/edit
https://docs.google.com/spreadsheets/d/e/2PACX-1vRtmL2ZeNzRJSApaCwn6ilV715IoSyoijjQ_TvPESVQ8geCOUqT0kTwjxMGQAm0s3CdnahmuCGj97kf/pubhtml
```

### Opción 3: Pegar URLs Directamente

Directamente en la interfaz usando el campo de texto.

### 📌 Formatos de URL Soportados

✅ **URL estándar:**
```
https://docs.google.com/spreadsheets/d/{ID}/edit
```

✅ **URL de publicación (pubhtml):**
```
https://docs.google.com/spreadsheets/d/e/{ID}/pubhtml
```

## ✨ Características

- ✅ Carga múltiples Google Sheets
- ✅ Actualización manual con botón "Actualizar"
- ✅ Filtrado y búsqueda de datos
- ✅ Gráficos interactivos (línea, barras, dispersión, área)
- ✅ Estadísticas descriptivas
- ✅ Descarga de datos como CSV
- ✅ Visualización de múltiples hojas en cada Sheet
- ✅ Caché eficiente para optimizar rendimiento

## 📊 Tipos de Gráficos Disponibles

- 📈 Línea (con marcadores)
- 📊 Barras
- 🔵 Dispersión (scatter)
- 📈 Área

## 🔧 Configuración Avanzada

- **Caché de datos**: 60 segundos (ajustable en el código)
- **Actualizaciones**: Botón manual para forzar actualización
- **Filtros personalizados**: Búsqueda por columna
- **Descarga**: Exporta datos filtrados como CSV

## ⚠️ Notas Importantes

- Los datos se actualizan en caché cada 60 segundos
- Haz clic en "Actualizar" para forzar una actualización inmediata
- Requiere conexión a internet para acceder a Google Sheets
- La autenticación con Google es obligatoria

## 🐛 Solución de Problemas

### Error: "credentials.json no encontrado"
→ Descarga el archivo de credenciales de Google Cloud y cópialo a la carpeta del proyecto

### Error: "Permiso denegado"
→ Asegúrate de haber compartido el Google Sheet con el email de la cuenta de servicio

### Error: "NotFoundError: Failed to execute 'removeChild' on 'Node'"
→ Este error fue resuelto optimizando el manejo de caché y eliminando time.sleep()
→ Usa la versión actualizada del código

### Los datos no se actualizan
→ Haz clic en el botón "🔄 Actualizar" para forzar una actualización
→ O espera 60 segundos para que el caché expire automáticamente

### Problemas de conexión a Google Sheets
→ Verifica que la cuenta de servicio tenga acceso al Sheet
→ Revisa las credenciales en Google Cloud Console

## 📞 Soporte

Para más información sobre:
- **Streamlit**: https://docs.streamlit.io/
- **Google Sheets API**: https://developers.google.com/sheets/api
- **Streamlit Cloud**: https://docs.streamlit.io/deploy/streamlit-cloud

## 🎯 Próximas mejoras

- [ ] Actualización automática basada en webhooks
- [ ] Más tipos de gráficos
- [ ] Exportación a otros formatos
- [ ] Almacenamiento de reportes

