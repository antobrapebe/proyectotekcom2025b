# KeyStore – Tienda de Licencias

Proyecto web simple basado en Flask + SQLite + Docker.

## Estructura

mi_pagina/
│── Dockerfile
│── docker-compose.yml
│── requirements.txt
│── app.py
│── .env
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   ├── script.js
│   └── img/ (agrega tus imágenes aquí)
│
├── database/
│   └── schema.sql
│
└── README.md

## Uso

## ¿En qué programa se ejecuta la imagen?

La imagen Docker se ejecuta con:

 Docker Desktop (Windows / Mac)
 Docker Engine (Linux)

No importa el IDE (VS Code, PyCharm, etc.).
Lo único necesario es Docker.

## ¿Cómo ejecutar tu imagen en otra PC?

Estos pasos funcionan en cualquier computadora:

## PASO 1 — Instalar Docker Desktop

🔗 https://www.docker.com/products/docker-desktop/

Solo instalar y abrirlo.
No se necesita nada más.

## PASO 2 — Abrir PowerShell / CMD / Terminal

Puede ser:

✔ Windows → PowerShell
✔ Mac → Terminal
✔ Linux → Terminal

## PASO 3 — Descargar la imagen desde GitHub

En cualquier PC, solo ejecutan:

docker pull ghcr.io/antobrapebe/proyectotekcom2025b:latest

Esto descarga la imagen.

## PASO 4 — Ejecutar la aplicación

La app corre en el puerto 5000:

docker run -p 5000:5000 ghcr.io/antobrapebe/proyectotekcom2025b:latest

✔ -p 5000:5000 expone el puerto
✔ Se abre en el navegador: http://localhost:5000/

