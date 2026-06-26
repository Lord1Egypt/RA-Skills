# Virtual Desktop Browser Skill (Español)

Ejecuta **Chromium en modo no headless** en **Xvfb display virtual (fijo 1200x720x24)** y realiza automatización tipo humano con PyAutoGUI. Ideal para sitios con fuerte anti-bot como Xiaohongshu y X/Twitter.

[中文](../README.md) | [English](en.md) | [العربية](ar.md)

---

## Funciones

| Función | Descripción |
|---------|-------------|
| Display virtual | Xvfb servidor X independiente, 1200x720x24 |
| Navegador no-headless | Chromium con GUI en pantalla virtual |
| Simulación de ratón | Mover, clic (izq/der/medio/doble), arrastrar |
| Simulación de teclado | Entrada de texto, atajos, combinaciones |
| Scroll | Desplazamiento vertical y horizontal |
| Captura de pantalla | Pantalla completa o región, PNG Base64 |
| Coincidencia de imagen | Buscar plantillas en pantalla (OpenCV) |
| Color de píxel | Leer RGB en coordenadas |
| Gestión de ventanas | Enfocar ventana por título |
| Auto-asignación DISPLAY | Evita conflictos multi-sesión (:99 ~ :199) |
| Parada de emergencia | Ratón a esquina inferior derecha detiene todo |

---

## Instalación

### Dependencias del sistema (Ubuntu/Debian)

```bash
apt-get update
apt-get install -y xvfb chromium-browser \
  libnss3 libgconf-2-4 libxss1 libasound2 \
  libatk1.0-0 libatk-bridge2.0-0 libcups2 \
  libdrm2 libgbm1 libgtk-3-0 libxshmfence1 x11-utils
```

### Dependencias de Python

```bash
pip install -r requirements.txt
```

### Instalar skill

```bash
npx skills add https://github.com/NHZallen/virtual-desktop-browser-skill
```

---

## Referencia de Herramientas

### `browser_start(url=None, display=None)`

Iniciar Xvfb y Chromium.

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `url` | str (opcional) | URL inicial, por defecto about:blank |
| `display` | str (opcional) | Display X, ej. `:99`. Auto-asignado si se omite |

**Retorna:**
```json
{
  "status": "started",
  "display": ":99",
  "xvfb_pid": 12345,
  "chrome_pid": 12346,
  "resolution": "1200x720x24"
}
```

---

### `browser_stop()`

Cerrar Chromium y Xvfb, liberar recursos.

**Retorna:** `{ "status": "stopped" }`

---

### `browser_snapshot(region=None)`

Capturar pantalla virtual, retorna PNG Base64.

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `region` | tuple (opcional) | `(left, top, width, height)` |

**Retorna:**
```json
{
  "image_base64": "iVBORw0KGgo...",
  "width": 1200,
  "height": 720
}
```

---

### `browser_click(x, y, button='left', clicks=1, duration=0.5)`

Mover ratón y hacer clic.

| Parámetro | Tipo | Por defecto | Descripción |
|-----------|------|-------------|-------------|
| `x` | int | obligatorio | Coordenada X |
| `y` | int | obligatorio | Coordenada Y |
| `button` | str | `left` | `left` / `right` / `middle` |
| `clicks` | int | `1` | Número de clics |
| `duration` | float | `0.5` | Tiempo de movimiento (segundos) |

---

### `browser_type(text, interval=0.05, wpm=None)`

Escribir texto en el foco actual.

| Parámetro | Tipo | Por defecto | Descripción |
|-----------|------|-------------|-------------|
| `text` | str | obligatorio | Texto a escribir |
| `interval` | float | `0.05` | Intervalo entre teclas (segundos) |
| `wpm` | int (opcional) | — | Palabras por minuto (velocidad humana) |

---

### `browser_hotkey(keys, interval=0.05)`

Presionar combinación de teclas.

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `keys` | list[str] | Nombres de teclas, ej. `["ctrl", "c"]` |
| `interval` | float | Intervalo entre teclas (segundos) |

---

### `browser_scroll(clicks=1, direction='vertical', x=None, y=None)`

Desplazar con rueda del ratón.

| Parámetro | Tipo | Por defecto | Descripción |
|-----------|------|-------------|-------------|
| `clicks` | int | `1` | Cantidad (+arriba/izq, −abajo/der) |
| `direction` | str | `vertical` | `vertical` o `horizontal` |

---

### `browser_find_image(image_path, confidence=0.8)`

Buscar imagen plantilla en pantalla.

**Retorna:** `{ "found": true, "x": 100, "y": 200, "width": 50, "height": 50 }` o `{ "found": false }`

---

### `browser_get_pixel_color(x, y)`

Obtener color RGB del píxel.

**Retorna:** `{ "r": 255, "g": 255, "b": 255 }`

---

### `browser_activate_window(title_substring)`

Enfocar ventana por coincidencia parcial de título.

---

## Ejemplo: Explorar Xiaohongshu

```python
browser_start(url="https://www.xiaohongshu.com/explore")
time.sleep(3)
browser_scroll(clicks=-3)
browser_snapshot()
browser_stop()
```

---

## Seguridad

- **Failsafe:** Mover el ratón a la esquina inferior derecha (1199, 719) para detener

---

## Solución de Problemas

| Problema | Solución |
|----------|----------|
| `Missing: Xvfb` | `apt-get install -y xvfb` |
| `Missing: chromium-browser` | `apt-get install -y chromium-browser` |
| Error DISPLAY de PyAutoGUI | Confirmar que `browser_start()` fue llamado |
| Coincidencia de imagen falla | Usar imagen de alto contraste, bajar `confidence` |

---

## Autor

Creador: **Allen Niu**  
Licencia: MIT-0
