## 📋 Formatos Soportados

### 1. Archivo Excel (.xlsx)

Puedes crear un archivo Excel con una columna que contenga las URLs de Google Sheets:

| URLs de Google Sheets |
|----------------------|
| https://docs.google.com/spreadsheets/d/1aBcDeFgHiJkLmNoPqRsTuVwXyZ123456/edit |
| https://docs.google.com/spreadsheets/d/e/2PACX-1vRtmL2ZeNzRJSApaCwn6ilV715IoSyoijjQ_TvPESVQ8geCOUqT0kTwjxMGQAm0s3CdnahmuCGj97kf/pubhtml |

El archivo puede tener múltiples columnas, pero las URLs deben estar en al menos una de ellas.

### 2. Archivo de Texto (.txt)

Crea un archivo de texto con una URL por línea:

```
https://docs.google.com/spreadsheets/d/1aBcDeFgHiJkLmNoPqRsTuVwXyZ123456/edit
https://docs.google.com/spreadsheets/d/e/2PACX-1vRtmL2ZeNzRJSApaCwn6ilV715IoSyoijjQ_TvPESVQ8geCOUqT0kTwjxMGQAm0s3CdnahmuCGj97kf/pubhtml
```

### 3. Pegar URLs Directamente

Pegue las URLs directamente en el campo de texto en la interfaz.

### 4. Formatos de URL Soportados

✅ **URL estándar:**
```
https://docs.google.com/spreadsheets/d/{ID}/edit
```

✅ **URL de publicación (pubhtml):**
```
https://docs.google.com/spreadsheets/d/e/{ID}/pubhtml
```

✅ **Cualquier variante** que contenga el ID correcto

## 🔐 Notas Importantes

1. **Credenciales JSON**: Necesitas un archivo `credentials.json` con credenciales de Google Cloud
2. **Permisos**: El sheet debe estar compartido con el email de la cuenta de servicio
3. **URLs públicas**: Las URLs de publicación (pubhtml) también funcionan si el sheet está publicado

## 📊 Estructuras de Datos Soportadas

La aplicación carga todas las hojas del workbook automáticamente:
- Cada hoja se muestra en una pestaña separada
- Todos los datos se convierten a DataFrames de pandas
- Soporta números, texto, fechas y más
