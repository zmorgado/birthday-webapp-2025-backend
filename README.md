# 🎉 Backend de Aplicación Web de Cumpleaños

Una API REST desarrollada con FastAPI para gestionar confirmaciones de asistencia (RSVP) para eventos de cumpleaños. 

## 📋 Descripción

Este backend proporciona funcionalidades para:
- 📝 Registro de confirmaciones de asistencia (RSVP)
- 🍽️ Confirmación separada para cena y fiesta
- 👨‍💼 Panel de administración protegido con contraseña
- 🗄️ Almacenamiento persistente en base de datos PostgreSQL

## 🚀 Características

- **API REST con FastAPI**: Framework moderno y rápido para Python
- **Base de datos PostgreSQL**: Almacenamiento con SQLAlchemy ORM
- **Autenticación básica**: Panel de administración protegido
- **CORS configurado**: Permite conexiones desde el frontend
- **Dockerizado**: Despliegue con contenedores
- **Scripts de prueba**: Herramientas para insertar, consultar y eliminar datos

## 🛠️ Tecnologías Utilizadas

- **FastAPI**: Framework web para APIs
- **SQLAlchemy**: ORM para manejo de base de datos
- **PostgreSQL**: Base de datos relacional
- **Uvicorn**: Servidor ASGI
- **Docker**: Containerización
- **python-dotenv**: Gestión de variables de entorno

## 📁 Estructura del Proyecto

```
birthday-webapp-2025-backend/
├── main.py              # Aplicación principal FastAPI
├── models.py            # Modelos de base de datos
├── config.py            # Configuración de la aplicación
├── requirements.txt     # Dependencias de Python
├── Dockerfile          # Configuración de Docker
├── .env                # Variables de entorno (no incluir en git)
└── tests/              # Scripts de prueba
    ├── insert_rsvp_rows.py    # Insertar datos de prueba
    ├── retrieve_data.py       # Consultar datos
    └── delete_rsvp_rows.py    # Eliminar todos los datos
```

## 🔧 Instalación y Configuración

### Prerrequisitos
- Python 3.11+
- PostgreSQL
- Docker (opcional)

### Instalación Local

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd birthday-webapp-2025-backend
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En macOS/Linux
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   ```bash
   # Crear archivo .env con:
   DATABASE_URL=postgresql://usuario:contraseña@host:puerto/base_datos
   ADMIN_PASSWORD=tu_contraseña_admin
   ```

5. **Ejecutar la aplicación**
   ```bash
   python -m uvicorn main:app --reload
   ```

### Instalación con Docker

1. **Construir la imagen**
   ```bash
   docker build -t birthday-webapp-backend .
   ```

2. **Ejecutar el contenedor**
   ```bash
   docker run -p 8000:8000 --env-file .env birthday-webapp-backend
   ```

## 📊 Modelo de Datos

### Tabla RSVP
- `id` (Integer): Clave primaria autoincremental
- `name` (String): Nombre del invitado
- `dinner_confirmed` (Boolean): Confirmación para la cena
- `party_confirmed` (Boolean): Confirmación para la fiesta
- `timestamp` (DateTime): Fecha y hora de registro

## 🔌 Endpoints de la API

### Público

#### `GET /`
- **Descripción**: Verificación de salud de la API
- **Respuesta**: `{"message": "API is running"}`

#### `POST /rsvp`
- **Descripción**: Enviar confirmación de asistencia
- **Cuerpo de la petición**:
  ```json
  {
    "name": "Nombre del Invitado",
    "dinner_confirmed": true,
    "party_confirmed": false
  }
  ```
- **Respuesta**: `{"message": "RSVP submitted successfully"}`

### Administración (Protegido)

#### `GET /admin`
- **Descripción**: Obtener todas las confirmaciones
- **Autenticación**: HTTP Basic (usuario: cualquiera, contraseña: ADMIN_PASSWORD)
- **Respuesta**: Array de objetos RSVP

## 🧪 Scripts de Prueba

En el directorio `tests/` se encuentran scripts útiles para desarrollo:

- **`insert_rsvp_rows.py`**: Inserta 30 registros de prueba
- **`retrieve_data.py`**: Muestra todos los registros RSVP
- **`delete_rsvp_rows.py`**: Elimina todos los registros

Ejecutar con:
```bash
python tests/nombre_del_script.py
```

## 🌐 CORS

La aplicación está configurada para permitir peticiones desde:
- `https://cumplepelusa.vercel.app`

Para desarrollo local, considerá agregar `http://localhost:3000` u otros orígenes necesarios.

## 🔒 Seguridad

- Panel de administración protegido con HTTP Basic Authentication
- Variables de entorno para datos sensibles
- Usuario no privilegiado en contenedor Docker

## 🚀 Despliegue

La aplicación está lista para desplegarse en plataformas como:

- AWS
- Google Cloud Platform
- Azure

Asegurate de configurar las variables de entorno `DATABASE_URL` y `ADMIN_PASSWORD` en tu plataforma.

Fue deployado como caso de estudio en las 3 plataformas, resultando exitosamente. 

Mi recomendación personal es Google Cloud Run o Azure Container Apps usando el Dockerfile por la facilidad del despliege y la omisión de configuraciónes, además del "escalado a cero" que impacta directamente en el precio final.
