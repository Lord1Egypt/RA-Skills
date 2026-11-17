# MCPs Opcionales — Transcripción YouTube FORMULA 100K

Estos MCPs no son obligatorios para el flujo base, pero cada uno agrega una capa de potencia al proceso.

---

## 1. sfiorini/youtube-mcp
**URL:** `https://youtube-mcp--sfiorini.run.tools`  
**Uptime:** 99.9% | **Latencia:** 414ms

### Cuándo usarlo
- El usuario quiere analizar varios videos del mismo canal de referencia
- Quiere ver estadísticas del video (vistas, likes) para validar si el tema tiene tracción
- Quiere listar todos los videos de un canal para elegir cuál transcribir
- Quiere procesar una playlist completa

### Herramientas clave
- `videos_searchVideos` — buscar videos por tema en YouTube
- `videos_getVideo` — obtener título, descripción, stats de un video
- `channels_listVideos` — listar videos de un canal
- `playlists_getPlaylistItems` — obtener videos de una playlist

### Ejemplo de uso en el flujo
```
Usuario: "Quiero sacar guiones de los videos de Iman Gadzhi sobre ventas"
→ Usar videos_searchVideos para encontrar sus videos sobre ventas
→ Elegir los más vistos
→ Usar yt-transcript-mcp para transcribir cada uno
→ Batch de guiones
```

---

## 2. node2flow/instagram (Instagram Graph API)
**Cuándo usarlo:** cuando el usuario quiere publicar reels directamente desde Claude después de grabar los guiones.

**Importante:** solo funciona con cuentas Business o Creator de Instagram, no cuentas personales.

### Herramientas clave
- `publish_reel` — publicar un reel (requiere URL del video ya grabado)
- `publish_photo` — publicar imagen (para los ganchos textuales como carruseles)
- `hashtag_research` — buscar hashtags relevantes para el contenido

---

## 3. Tavily (ya conectado en el sistema)
Aunque está conectado por defecto, recordar sus usos específicos en este flujo:

- `tavily_search` — buscar referencias virales para verificación de viralidad
- `tavily_research` — investigar el tema del video para enriquecer los guiones con datos actuales
- `tavily_extract` — extraer artículos o páginas web como fuente adicional de datos para los guiones

---

## Combinación recomendada para flujo completo

```
yt-transcript-mcp  →  transcripción confiable
       +
Tavily             →  verificación de viralidad + contexto
       +
sfiorini/youtube   →  (opcional) selección inteligente de videos del canal
```
