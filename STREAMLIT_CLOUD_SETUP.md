# 🔐 Guía de Configuración - Streamlit Cloud

## Problema

El app funciona pero no muestra los datos del Google Sheet. Aparece el mensaje:
> ⚠️ **Autenticación no configurada**

## Solución

Tienes **2 opciones** para que el app acceda a tus datos:

---

## Opción 1: Usar Streamlit Secrets (Recomendado) 🌐

### Pasos:

1. **Abre tu app en Streamlit Community Cloud**
   - Ve a: https://share.streamlit.io
   - Busca tu app `automatizada`
   - Haz clic en el menú (⋮) en la esquina superior derecha

2. **Accede a Settings → Secrets**
   - En la barra lateral izquierda, selecciona **Settings**
   - Selecciona **Secrets** en la siguiente pantalla

3. **Obtén tu archivo credentials.json**
   - Si ya tienes uno: Ve al paso 5
   - Si no lo tienes: Crea uno nuevo:
     - Ve a [Google Cloud Console](https://console.cloud.google.com/)
     - Crea un proyecto nuevo
     - Activa: **Google Sheets API** y **Google Drive API**
     - Crea una **Cuenta de Servicio** (Service Account)
     - Crea una **Clave JSON**
     - Descarga el archivo `credentials.json`

4. **Copia el contenido de credentials.json**
   - Abre tu archivo `credentials.json` con un editor de texto
   - Copia TODO su contenido

5. **Pega en Streamlit Secrets**
   - En el editor de texto de Secrets, pega:
   ```toml
   [google_service_account]
   type = "service_account"
   project_id = "tu-proyecto"
   private_key_id = "..."
   private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
   client_email = "tu-correo@proyecto.iam.gserviceaccount.com"
   client_id = "..."
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
   client_x509_cert_url = "..."
   ```

6. **Comparte el Sheet con la cuenta de servicio**
   - Abre tu Google Sheet
   - Haz clic en **Compartir** (esquina superior derecha)
   - Pega el email del `client_email` de credentials.json
   - Dale acceso de **Lector** o **Editor**

7. **Guarda y espera**
   - Haz clic en **Save** en Streamlit Secrets
   - La app se recargará automáticamente en 10 segundos
   - ¡Listo! Ya debería mostrar tus datos

---

## Opción 2: Convertir el Sheet a Público 🔓 (Más Simple)

### Pasos:

1. **Abre tu Google Sheet**

2. **Haz clic en Compartir** (esquina superior derecha)

3. **Configura el acceso:**
   - Haz clic en **Cambiar**
   - Selecciona **Cualquier persona con el link**
   - Selecciona **Lector** (no necesita editar)
   - Haz clic en **Compartir** o **Copiar link**

4. **Pega el link en el app**
   - Copia el link del sheet que aparece
   - En el app, pega en el campo "Pega las URLs de Google Sheets"
   - ¡Listo! Los datos deberían aparecer al instante

---

## ¿Cuál elegir?

| Criterio | Secrets | Público |
|----------|---------|---------|
| **Seguridad** | ✅ Alta | ⚠️ Baja |
| **Facilidad** | ⚠️ Media | ✅ Muy fácil |
| **Privacidad** | ✅ Privado | ❌ Público |
| **Compartir datos** | ❌ No | ✅ Sí |
| Recomendado para: | Datos empresariales | Datos públicos |

---

## ¿Sigue sin funcionar?

### Checklist:

- [ ] ¿Copiaste correctamente el contenido de credentials.json en Secrets?
- [ ] ¿El formato TOML es correcto (sin comillas extras)?
- [ ] ¿Le compartiste el Sheet a la cuenta de servicio?
- [ ] ¿Esperaste 10 segundos después de guardar?
- [ ] ¿Recargaste el navegador (F5)?

### Si usas Sheet Público:

- [ ] ¿El link comienza con `https://docs.google.com/spreadsheets/d/`?
- [ ] ¿El Sheet tiene datos (no está vacío)?
- [ ] ¿Está configurado como "Cualquier persona con el link"?

---

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en Streamlit Community Cloud (pestaña "Logs")
2. Verifica que el email de la cuenta de servicio sea correcto
3. Comparte el Sheet con `Lector` mínimo

¡Listo! 🎉
