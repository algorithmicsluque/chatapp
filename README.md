# Aplicación de Chat con Kivy

Esta es una aplicación de chat moderna y responsive desarrollada con Kivy para Python.

## Características

- Interfaz de usuario moderna y responsive
- Lista de chats con avatares y mensajes no leídos
- Burbujas de chat con diseño moderno
- Simulación de respuestas automáticas
- Diseño optimizado para móviles
- Navegación entre pantallas
- Mock data para demostración

## Requisitos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Crear un entorno virtual (recomendado):
```bash
python -m venv venv
```

2. Activar el entorno virtual:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## Ejecutar la aplicación

Para ejecutar la aplicación, simplemente ejecuta:
```bash
python main.py
```

## Estructura del proyecto

- `main.py`: Archivo principal de la aplicación
- `chat.kv`: Archivo de estilos y diseño Kivy
- `requirements.txt`: Lista de dependencias del proyecto
- `README.md`: Este archivo con instrucciones

## Características de la UI

- Diseño responsive optimizado para móviles
- Burbujas de chat con esquinas redondeadas
- Avatares de usuario
- Indicadores de mensajes no leídos
- Campo de entrada de mensajes con botón de envío
- Scroll automático en la lista de chats y mensajes
- Paleta de colores moderna y profesional

## Personalización

Puedes personalizar la aplicación modificando:
- Los colores en el archivo `chat.kv`
- Los datos mock en `main.py`
- El tamaño de la ventana en la clase `MainApp`
- Los estilos de los widgets en `chat.kv` 