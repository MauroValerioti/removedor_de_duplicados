# MVCleaner: Elimina Imágenes y Videos Duplicados con un Solo Click

¿Tenés miles de fotos y videos duplicados, copias como `foto(1).jpg`, thumbnails, o videos casi idénticos con distinto nombre?  
**Este repositorio te resuelve ese problema sin necesidad de pagar, registrarte ni instalar software basura.**

---

## ¿Qué hace?

Este proyecto contiene **dos scripts en Python** (con sus .bat) que te permiten:

### `remove_duplicate_images.py`
- Detectar imágenes **visualmente duplicadas** (no importa el nombre, tamaño o compresión)
- Detectar archivos basura como `thumb.jpg`, `imagen(1).png`, etc.
- Mover todos los duplicados a una carpeta interna `__DUPLICATES`
- Generar un archivo `moved_images.txt` con el log completo

### `remove_video_duplicates.py`
- Detectar **videos duplicados** comparando contenido visual (keyframes en 10%, 50% y 90%)
- Funciona incluso si tienen nombres distintos o resoluciones diferentes
- Mueve duplicados a `__DUPLICATE_VIDEOS` sin borrarlos
- Genera un archivo `moved_videos.txt` con el log

---

## ¿Como funciona?

* Este script no se basa en nombre o tamaño de archivo.
* Para imágenes uso perceptual hashing (pHash), que compara visualmente los pixeles.
* Para videos uso OpenCV para capturar 3 keyframes y analizar su similitud visual con imagehash.
* Eso permite detectar duplicados aunque tengan distinta resolución, peso o nombre

## ¿Cómo usarlo?

### Opción 1 – Python ya instalado

1. Cloná o descargá este repositorio
2. Copiá el script que querés usar (por ejemplo, `remove_duplicate_images.py`) a la carpeta que quieras limpiar
3. Hacé doble clic en el `.bat` correspondiente  
4. ¡Listo! Los archivos duplicados se moverán automáticamente

---

### Opción 2 – No tenés Python instalado

> Coming soon: versión `.exe` portable sin dependencias  
> (Podés seguir usando los `.bat` si tenés Python instalado)

