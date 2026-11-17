---
name: transcripcion-youtube-formula100k
description: "Convierte videos de YouTube en batches de guiones virales con FÓRMULA 100K. Usar SIEMPRE que alguien comparta una URL de YouTube y quiera extraer ideas, guiones o contenido de ese video. También con: \"transcribe este video\", \"sácame ideas de este YouTube\", \"convierte este video en guiones\", \"quiero hacer un batch de scripts de este video\", \"repurposea este video\", \"dame guiones basados en este video\", o cualquier variación que combine una URL de YouTube con intención de crear contenido nuevo. Obtiene la transcripción (Supadata, web o pegada por la usuaria) y aplica los frameworks de guionización de FÓRMULA 100K para producir varios guiones validados de un solo video."
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - `yt-transcript-mcp` no está en este servidor. Para la transcripción, en este orden: Supadata con `SUPADATA_API_KEY` si existe; tu herramienta web si el video tiene transcripción pública; o pídele a la usuaria que la pegue (YouTube → «Mostrar transcripción» → copiar).
> - Tu búsqueda web es Tavily por Composio: `composio execute TAVILY_SEARCH -d '{"query":"…","max_results":5}'` (sección 2 del puente). Con eso verificas la viralidad.
> - Los guiones del batch van a `guiones/` y se mandan por Telegram: resumen en el chat y el `.md` como documento.

---

# Skill: Transcripción YouTube → Batch de Guiones FORMULA 100K

Convierte cualquier video largo de YouTube en un batch de guiones cortos virales, aplicando los frameworks de FORMULA 100K.

---

## MCPs REQUERIDOS

| MCP | URL de conexión | Para qué |
|-----|----------------|----------|
| **yt-transcript-mcp** (principal) | `https://yt-transcript-mcp--alex2zimmermann-ux.run.tools` | Transcripción completa del video |
| **Tavily** (ya conectado) | disponible | Verificación de viralidad (búsqueda de referencias reales) |

> Si el usuario no tiene `yt-transcript-mcp` conectado, indicarle que lo agregue en **Settings → Connectors** con la URL de arriba.

---

## FLUJO COMPLETO (seguir en orden)

### FASE 1 — Extraer la transcripción del video

**Para videos de hasta ~20 minutos:** usar `get_transcript` con la URL de YouTube.

**Para videos largos (+20 min):** usar `get_transcript_summary` que divide el video en chunks de 5 minutos — mucho más manejable para análisis.

```
Herramienta: get_transcript  →  parámetro url: [URL del video]
Herramienta: get_transcript_summary  →  parámetro url: [URL del video], chunk_minutes: 5
```

**Tip de idioma:** si el video está en inglés pero el usuario crea contenido en español, extraer con `language: "en"` y luego adaptar al español en los guiones.

> ⚠️ **Si yt-transcript-mcp no está disponible**, pedir al usuario que:
> 1. Conecte el MCP (instrucciones en la sección de arriba), o
> 2. Pegue la transcripción manualmente desde YouTube (botón "..." → "Mostrar transcripción")

---

### FASE 2 — Analizar y mapear el contenido

Una vez obtenida la transcripción, extraer:

1. **Tema central del video** — en una oración simple
2. **Subtemas o bloques de contenido** — listar todos los puntos o ideas que cubre el video (si se usó `get_transcript_summary`, cada chunk es un bloque)
3. **Datos, historias o ejemplos únicos** — momentos con alto potencial viral (stats, anécdotas, revelaciones, puntos de controversia)
4. **Perfil del rubro/audiencia** — si el usuario no lo indicó, preguntar: *"¿Cuál es tu rubro o a quién va dirigido tu contenido?"*
5. **Búsqueda de contexto adicional** — usar `search_transcript` (de yt-transcript-mcp) para encontrar momentos clave si el video es muy largo

Presentar el análisis así:

```
📹 VIDEO: [título o tema]
⏱️ Duración estimada: [si está disponible]

🗂️ BLOQUES DE CONTENIDO DETECTADOS:
1. [bloque 1]
2. [bloque 2]
...

💡 MOMENTOS CON POTENCIAL VIRAL:
- [dato/historia/revelación 1]
- [dato/historia/revelación 2]
...

🎯 RUBRO APLICADO: [rubro del usuario]
```

---

### FASE 3 — Proponer ideas de guiones (pre-batch)

Generar una lista de **8 a 12 ideas de guiones** derivadas del video, una por bloque o momento potencial.

Para cada idea indicar:
- El **ángulo** (qué aspecto del video convierte en contenido propio)
- La **estructura sugerida** de FORMULA 100K (ver índice de estructuras abajo)
- El **objetivo** (viralidad, autoridad, ventas, engagement, educación)

Formato:

```
IDEA #1
Ángulo: [descripción del ángulo]
Estructura sugerida: [nombre de estructura]
Objetivo: [viralidad / autoridad / ventas / engagement / educación]

IDEA #2
...
```

Luego preguntar:
> *"¿Quieres que desarrolle TODOS los guiones en batch, o prefieres elegir cuáles primero?"*

---

### FASE 4 — Producir el batch de guiones

**Si el usuario pide batch completo:** desarrollar todos los guiones en secuencia.  
**Si elige algunos:** desarrollar solo los seleccionados.

Para **cada guion**, seguir el proceso completo de la skill `guionizacion-formula100k`:

1. Evaluar si la idea pasa los 9 criterios de idea ganadora
2. Aplicar la estructura elegida
3. Ejecutar verificación de viralidad (buscar referencia real con Tavily)
4. Desarrollar sistema de ganchos (verbal + visual + textual)
5. Escribir el guion completo

Ver detalle de cada paso en: `references/proceso-guion.md`

---

### FASE 5 — Entregar el batch organizado

Al finalizar todos los guiones, presentarlos así:

```
═══════════════════════════════════
BATCH DE GUIONES — [Tema del video]
Total: [N] guiones listos
═══════════════════════════════════

GUION #1 — [Ángulo]
Estructura: [nombre]
Objetivo: [objetivo]
───────────────────
[GANCHO VERBAL]: ...
[GANCHO VISUAL]: ...
[GANCHO TEXTUAL]: ...

[guion completo]

CTA: ...

═══════════════════════════════════

GUION #2 — ...
```

Terminar con:
> *"Tienes [N] guiones listos para grabar. ¿Quieres ajustar alguno, cambiar el tono, o agregar más basados en el mismo video?"*

---

## ÍNDICE DE ESTRUCTURAS (referencia rápida)

Para descripción completa de cada estructura, ver `../guionizacion-formula100k/references/estructuras.md` (vive en esa skill, no en esta).

| Objetivo | Estructuras recomendadas |
|----------|------------------------|
| Viralidad / alcance | 14, 15, 16, 18, 19, 20 |
| Autoridad | 1, 3, 7, 8, 33 |
| Ventas | 1, 2, 4, 5, 30, 31 |
| Engagement / comentarios | 8, 10, 11, 19, 30 |
| Storytelling | 4, 12, 13, 21, 22, 23 |
| Educación / valor | 9, 15, 17, 26, 28 |
| Comparación / debate | 10, 19, 29, 32 |

---

## REGLAS GENERALES

- Cada guion debe ser 100% original — no repetir frases del video original
- Adaptar el lenguaje al rubro del usuario, no al rubro del video fuente
- El video de YouTube es la **materia prima**, no el guion
- Si el video es en otro idioma, traducir y adaptar al español del usuario
- Priorizar momentos con datos concretos, historias o paradojas — tienen mayor potencial viral
- Nunca generar guiones genéricos: cada uno debe tener un ángulo específico y diferenciado

---

## DEPENDENCIAS

- **yt-transcript-mcp** (requerido) — transcripción del video (`get_transcript`, `get_transcript_summary`, `search_transcript`)
  → Conectar en Settings → Connectors: `https://yt-transcript-mcp--alex2zimmermann-ux.run.tools`
- **Tavily MCP** (ya conectado) — verificación de viralidad y búsqueda de referencias reales
- **Skill guionizacion-formula100k** — proceso de escritura de cada guion
- **Web search** — backup para verificación de viralidad

Ver instrucciones detalladas del proceso de guion en: `references/proceso-guion.md`

---

## MCPs OPCIONALES (mejoran el flujo)

Estos MCPs no son obligatorios pero potencian la skill si el usuario los tiene:

**`sfiorini/youtube-mcp`** (`https://youtube-mcp--sfiorini.run.tools`)
→ Complementa yt-transcript-mcp: permite buscar videos del mismo canal, ver estadísticas, listar playlists. Útil si el usuario quiere procesar varios videos de un mismo creador de referencia.

**`node2flow/instagram`**
→ Si el usuario quiere publicar directamente los guiones como reels desde Claude una vez grabados.

Ver detalles en: `references/mcps-opcionales.md`
