# 🚀 Gemini Cloud IDE: La Estación de Trabajo Inteligente

[![Status](https://img.shields.io/badge/Status-Active-brightgreen)]()
[![Backend](https://img.shields.io/badge/Backend-FastAPI-blue)]()
[![Frontend](https://img.shields.io/badge/Frontend-Monaco--Editor-orange)]()
[![Infrastructure](https://img.shields.io/badge/Infra-Docker-blueviolet)]()

**Gemini Cloud IDE** es un entorno de desarrollo integrado (IDE) basado en la web, diseñado para reemplazar Visual Studio Code local con una estación de trabajo potente, ligera y accesible desde cualquier lugar. Optimizado para el uso intensivo de **Gemini CLI** y la gestión directa de servidores VPS.

---

## ✨ Características Principales

- **💻 Monaco Editor Core:** La misma experiencia de edición de código que VS Code, con resaltado de sintaxis nativo y atajos de teclado (Ctrl+S para guardar).
- **🐚 Terminal PTY Real:** Consola interactiva integrada basada en `xterm.js` conectada a un pseudoterminal en el VPS. Ideal para ejecutar comandos bash y `gemini-cli`.
- **📂 Explorador de Archivos:** Navegación fluida por el sistema de archivos del servidor con capacidad de lectura y escritura en tiempo real.
- **🔒 Seguridad Industrial:** Protegido por **Traefik** con capa de autenticación básica (Basic Auth) para garantizar que solo tú accedas a tu código.
- **🐳 Docker Native:** Despliegue en segundos mediante contenedores, asegurando un entorno aislado y reproducible.
- **📱 Interfaz Web Responsive:** Diseñado para funcionar en escritorio y tablets, convirtiendo cualquier dispositivo en tu estación de trabajo.

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
| :--- | :--- |
| **Backend** | Python 3.11 + FastAPI + WebSockets |
| **Frontend** | Vanilla JS + Monaco Editor + Xterm.js |
| **Proxy** | Traefik |
| **Contenedores** | Docker & Docker Compose |

---

## 🚀 Instalación y Despliegue

### Requisitos Previos
- Docker y Docker Compose instalados.
- Un servidor VPS (Recomendado: Hostinger/Ubuntu).
- Traefik configurado como proxy inverso (opcional, pero incluido en el compose).

### Despliegue en Producción (VPS)

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/selvaggiesteban/gemini.git
   cd gemini
   ```

2. **Configurar la autenticación:**
   Edita el archivo `docker-compose.yml` y actualiza tu hash de contraseña en la etiqueta de Traefik:
   ```yaml
   - "traefik.http.middlewares.gemini-auth.basicauth.users=admin:TU_HASH_AQUÍ"
   ```

3. **Levantar el entorno:**
   ```bash
   docker compose up -d
   ```

4. **Acceso:**
   Abre tu navegador en `http://gemini.tu-dominio.com` e ingresa tus credenciales.

---

## 📂 Estructura del Proyecto

```text
.
├── backend/
│   ├── app/
│   │   └── main.py       # API FastAPI y lógica de WebSockets PTY
│   └── requirements.txt  # Dependencias de Python
├── frontend/
│   └── public/
│       └── index.html    # Interfaz de usuario (Monaco + Terminal)
├── docker-compose.yml    # Orquestación de servicios
└── README.md             # Documentación oficial
```

---

## 🛡️ Seguridad

Este IDE tiene acceso completo al sistema de archivos donde se despliega. Es **CRÍTICO** mantener las credenciales de acceso seguras y no exponer el puerto interno `8000` directamente a internet. Utiliza siempre el proxy con autenticación incluido.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Siéntete libre de abrir un *Issue* o enviar un *Pull Request* para mejorar la estación de trabajo.

---

## ⚖️ Licencia

Este proyecto está bajo la Licencia MIT.

---

> **Creado por Esteban Selvaggi**  
> *Transformando servidores en estaciones de trabajo inteligentes.*  
> [selvaggiesteban.dev](https://selvaggiesteban.dev)
