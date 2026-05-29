# ProyectoWeb backend
Proyecto pagina web depilacion laser
# Bella Piel - Sistema Web de Depilación Láser

## Descripción del sistema

Bella Piel es una aplicación web desarrollada para la gestión de pacientes y citas de una clínica de depilación láser diodo. El sistema permite registrar pacientes, agendar citas, administrar estados de citas y enviar correos automáticos de confirmación mediante Mailjet SMTP.

## Tecnologías utilizadas

### Frontend

* Vue 3
* JavaScript
* Vite
* CSS

### Backend

* Flask
* Flask-CORS
* Flask-Session
* Python

### Base de Datos

* MySQL
* AlwaysData

### Servicios en la nube

* Render
* Vercel
* Mailjet SMTP


## Arquitectura del sistema

El proyecto utiliza una arquitectura cliente-servidor:

Frontend (Vue 3)
↓
Fetch API
↓
Backend Flask
↓
MySQL AlwaysData
↓
Mailjet SMTP


## Endpoints principales

### Login

POST /login

### Obtener pacientes

GET /pacientes

### Agregar pacientes

POST /pacientes

### Obtener citas

GET /citas

### Agregar citas

POST /citas

### Actualizar estado de citas

POST /citas/actualizar-estado

### Eliminar citas

POST /citas/eliminar


## Seguridad implementada

* Variables de entorno (.env)
* Validación de datos
* Manejo de sesiones con Flask-Session
* CORS configurado
* Separación frontend/backend
* Protección de credenciales


## Plataformas utilizadas

| Servicio      | Plataforma |
| ------------- | ---------- |
| Frontend      | Vercel     |
| Backend       | Render     |
| Base de datos | AlwaysData |
| Correos       | Mailjet    |


## Autor

Daniela Campos
