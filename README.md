# Configuración para ejecutar la aplicación Streamlit

## 📋 Requisitos Previos

1. Python 3.8 o superior instalado
2. Cuenta de Google Cloud con acceso a Google Sheets API

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

## 🚀 Instalación y Ejecución

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar la aplicación
```bash
streamlit run app.py
```

La aplicación se abrirá en tu navegador en `http://localhost:8501`

## 📁 Uso de Archivos de URLs

### Formato del archivo de texto:
Crea un archivo `.txt` con una URL de Google Sheets por línea:

```
https://docs.google.com/spreadsheets/d/1aBcDeFgHiJkLmNoPqRsTuVwXyZ123456/edit
https://docs.google.com/spreadsheets/d/2xYzAbCdEfGhIjKlMnOpQrStUvWxYz789012/edit
```

## ✨ Características

- ✅ Carga múltiples Google Sheets
- ✅ Actualización automática configurable
- ✅ Filtrado y búsqueda de datos
- ✅ Gráficos interactivos (línea, barras, dispersión, área)
- ✅ Estadísticas descriptivas
- ✅ Descarga de datos como CSV
- ✅ Visualización de múltiples hojas en cada Sheet

## 📊 Tipos de Gráficos Disponibles

- 📈 Línea (con marcadores)
- 📊 Barras
- 🔵 Dispersión (scatter)
- 📈 Área

## 🔧 Configuración Avanzada

- **Intervalo de actualización**: 10-300 segundos (personalizable)
- **Actualización automática**: Activable/desactivable por cada Sheet
- **Filtros personalizados**: Búsqueda por columna

## ⚠️ Notas Importantes

- Los datos se actualizan automáticamente cada X segundos si está habilitada la opción
- Requiere conexión a internet para acceder a Google Sheets
- La primera carga puede tardar más tiempo

## 🐛 Solución de Problemas

### Error: "credentials.json no encontrado"
→ Descarga el archivo de credenciales de Google Cloud y cópialo a la carpeta del proyecto

### Error: "Permiso denegado"
→ Asegúrate de haber compartido el Google Sheet con el email de la cuenta de servicio

### Los datos no se actualizan
→ Verifica que la opción "Actualizar automáticamente" esté habilitada en la barra lateral

## 📞 Soporte

Para más información sobre Streamlit: https://docs.streamlit.io/
Para más información sobre Google Sheets API: https://developers.google.com/sheets/api
