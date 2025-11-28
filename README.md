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

### 1. Crear base de datos
sqlite3 database/keystore.db < database/schema.sql

### 2. Ejecutar sin Docker
pip install -r requirements.txt  
python app.py

### 3. Ejecutar con Docker
docker-compose up --build
 
