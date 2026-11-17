---
name: radar-virales-f100k
description: "Módulo del Autopilot F100K que corre diariamente: caza el HECHO más reaccionable del día —un lanzamiento de IA, una movida de marketing de una marca grande, o un formato viral SIN cara— evitando a propósito reaccionar a creadores del mismo nicho (eso le entrega la audiencia a un competidor). Elige 1 ganador con scoring + filtro de exclusión, genera un guion de reacción listo para grabar con la voz del usuario donde ÉL es el intérprete del hecho, y envía todo por email. Usar cuando alguien diga: \"corre mi radar\", \"qué hay viral hoy\", \"dame el viral del día\", \"ejecutar radar diario\", \"qué puedo reaccionar hoy\", o cuando el schedule automático lo invoque. Requiere config en cerebro/f100k-config.json — si no existe, instruir a correr /rutina-maestra-formula100k primero."
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Config en `cerebro/f100k-config.json` (si falta, créala desde `USER.md` y confírmala por Telegram).
> - Carriles A y B (Tavily) = tu búsqueda web. Carril C (virales sin cara en TikTok) usa Apify: solo con `APIFY_TOKEN`; sin token, salta el carril C y avísalo.
> - El «Paso 5 — email con Gmail» se reemplaza por un mensaje de Telegram con el mismo contenido.
> - Muestra la línea de costo de Apify solo si Apify corrió de verdad.

---

# Skill: Radar Diario de Virales — Autopilot F100K

Cada mañana, este skill hace el trabajo de detective por ti: escanea TikTok y las noticias del día, elige EL viral más aprovechable para tu nicho, y te entrega un guion de reacción listo para grabar. Solo tienes que abrir el email y grabar.

---

## FASE 1 — CARGAR CONFIG

### Paso 1 — Leer config del usuario

```bash
cat cerebro/f100k-config.json
```

Si el archivo no existe o da error → detener y decir:
> "No encontré tu configuración del Autopilot. Corre `/rutina-maestra-formula100k` primero para hacer el setup inicial — toma ~3 minutos."

Extraer y guardar en memoria de trabajo:
- `niche` → nicho del usuario
- `keywords` → array de keywords de búsqueda
- `email` → destino del digest
- `voice_profile` → perfil de voz
- `radar_sources` → las 3 listas de queries de la FASE 2 (`ai_launches`, `brand_marketing`, `faceless_virals`)
- `radar_exclusion` → el filtro que descarta creadores del mismo nicho

**Si `radar_sources` o `radar_exclusion` no están en el config** (configs creados antes de la v1.1 del radar), NO detenerse: derivarlos en el momento a partir de `niche` y `keywords`, y avisar al usuario en una línea que se usaron valores derivados y que puede fijarlos corriendo `/rutina-maestra-formula100k` de nuevo.

- `ai_launches` → "lanzamiento inteligencia artificial [niche]", "nuevo modelo IA OpenAI Google Anthropic Meta", "nueva herramienta IA [niche]"
- `brand_marketing` → "campaña marketing viral marca grande", "caso de marketing empresa", "jugada marketing marca redes sociales"
- `faceless_virals` → "tendencia viral formato redes", "formato viral instagram tiktok", + 1 query armada con las `keywords` del usuario
- `radar_exclusion` → "DESCARTAR cualquier viral que sea un creador del MISMO nicho ([niche]) dando tips o educando — reaccionar a eso le entrega tu audiencia a un competidor. Solo se permite reaccionar a un creador de OTRO rubro y como CONTRASTE, nunca como autoridad a seguir."

⚠️ El nicho de la exclusión es el del **usuario que corre el radar**, no "marketing y creación de contenido". Una alumna nutricionista debe excluir nutricionistas, no marketers.

---

## FASE 2 — CAZA DE HECHOS (no de creadores)

> **PRINCIPIO RECTOR DEL RADAR (v1.1):** reaccionamos a **HECHOS, no a creadores.**
> Reaccionar a otro creador de tu nicho dándote tips le entrega tu audiencia (lo descubren y lo siguen, y te posiciona como comentarista de un par). En cambio, cuando el "personaje" del viral es una entidad sin cara —un lanzamiento de IA, una movida de una marca grande, un formato viral genérico— **no hay nadie a quién irse a seguir, y TÚ eres la intérprete.** El hecho es el gancho; tu opinión es el producto.
>
> Por eso este radar NO busca TikToks por keywords de nicho (eso trae competidores). Busca en **3 carriles de hechos**.

### Carril A — Lanzamientos de IA (Tavily)

Para cada query en `config.radar_sources.ai_launches`, lanzar `mcp__claude_ai_Tavily__tavily_search`:
```json
{
  "query": "[query] últimas 48 horas",
  "search_depth": "advanced",
  "max_results": 5
}
```
Busca: nuevos modelos, features, herramientas o cambios de IA que afecten cómo se crea contenido que vende.
Conservar: URL, título, snippet, fuente, fecha. → lista `ai_candidates`.

### Carril B — Movidas de marketing de marcas grandes (Tavily)

Para cada query en `config.radar_sources.brand_marketing`, lanzar `mcp__claude_ai_Tavily__tavily_search` (igual estructura).
Busca: campañas, casos o jugadas de marketing de empresas grandes (Coca-Cola, Nike, Duolingo, McDonald's, Netflix, etc.) que se puedan diseccionar con tu lente de venta.
Conservar igual. → lista `brand_candidates`.

### Carril C — Virales SIN cara/competidor (TikTok via Apify, filtrado duro)

Usar `mcp__apify__call-actor` con `clockworks~tiktok-scraper`. Para cada keyword en `config.radar_sources.faceless_virals`:
```json
{
  "searchQueries": ["[keyword]"],
  "resultsPerPage": 15,
  "shouldDownloadVideos": false,
  "shouldDownloadCovers": false
}
```
`waitSecs: 45`. Filtrar:
- Publicados en las últimas 48h (`createTime`)
- Views mínimo 100,000 (bajar a 50,000 si nada supera el umbral)
- **DESCARTAR DE ENTRADA** todo video que sea un creador educando/dando tips de marketing, creación de contenido, IA para creadores o monetización (aplicar `config.radar_exclusion`). Lo que queda son tendencias/formatos donde el protagonista NO es un competidor a seguir.

Conservar: URL, caption, views, likes, shares, autor, fecha. → lista `faceless_candidates`.

> **Nota:** Carril C es el de mayor riesgo de colar un competidor. Ante la duda sobre un candidato de TikTok, descártalo. Es preferible un día con ganador de Carril A o B que reaccionar a un par.

Consolidar `ai_candidates` + `brand_candidates` + `faceless_candidates` en `all_candidates`.

---

## FASE 3 — ELEGIR EL GANADOR DEL DÍA

### Paso 3A — FILTRO DE EXCLUSIÓN (eliminatorio, antes de puntuar)

Recorrer `all_candidates` y **eliminar** todo candidato que active `config.radar_exclusion`:
- ❌ Creador del MISMO nicho (marketing, creación de contenido, IA para creadores, monetización, redes) dando tips o educando → **fuera.** Reaccionar a esto le entrega tu audiencia a un competidor.
- ✅ Se conserva: lanzamientos/noticias de IA, movidas de marcas grandes, formatos virales sin cara, o creadores de OTRO rubro usables como contraste (ej. un chef, un atleta) — nunca como autoridad a seguir.

Si tras el filtro quedan 0 candidatos → ampliar Carril A/B con una query extra de IA/marca antes de rendirse. El radar diario casi siempre debe tener ganador de hecho/noticia.

### Paso 3B — Scoring y selección

Evaluar los candidatos sobrevivientes contra estos criterios:

| Criterio | Peso | Cómo evaluar |
|----------|------|--------------|
| Sin-competidor / autoridad propia | 35% | ¿El protagonista es un HECHO (IA, marca, formato) y no un creador a seguir? ¿el usuario queda como intérprete, no como comentarista de un par? Máximo si no hay nadie a quién irse a seguir. |
| Potencial de reacción / opinión | 30% | ¿Puede agregar una lectura que nadie está dando? ¿Genera debate? |
| Aplicabilidad a "crear contenido que vende" | 20% | ¿Se puede aterrizar en qué significa esto para que su audiencia venda con contenido? (ángulo F100K) |
| Frescura + viralidad | 15% | Publicado en últimas 24-48h · views/autoridad del medio |

Asignar puntuación del 1-10 a cada candidato y elegir el TOP 1.

Regla de desempate: preferir el de mayor puntaje en "Sin-competidor / autoridad propia" (criterio 1). Entre dos hechos igual de fuertes, gana el de Carril A (IA) o B (marca) sobre Carril C (TikTok).

Guardar en `winner`:
- título o caption (primeras 80 chars)
- URL
- métricas clave (views/fuente)
- tipo: "lanzamiento-ia" | "movida-marca" | "viral-sin-cara"
- razón de selección (1 línea — por qué deja al usuario como intérprete del hecho, no como comentarista de un par)

---

## FASE 4 — GENERAR GUION DE REACCIÓN

### Paso 4 — Escribir el guion con la voz del usuario

Escribir un guion de reacción de 45-60 segundos (máximo 120 palabras) usando la siguiente estructura:

```
[GANCHO VISUAL — 0-3s]
Referencia directa al viral. Opciones:
- "Acabo de ver esto y necesitaba compartirlo..."
- "Esto que está viral ahora mismo en [red] me hizo pensar algo importante..."
- "[Dato más impactante del viral] — y esto es lo que nadie está diciendo al respecto."

[CONTEXTO — 3-8s]
1-2 líneas: qué es el viral, de dónde viene, por qué está trending ahora.

[PERSPECTIVA ÚNICA — 8-45s]
3 puntos de vista propios. Estructura:
Punto 1: "Lo que esto confirma sobre [tema del nicho] es..."
Punto 2: "Lo que la mayoría está pasando por alto aquí es..."
Punto 3: "Lo que yo haría diferente / lo que aprendí de esto es..."
→ Usar voz del usuario: [voice_profile]
→ Conectar con el nicho: [niche]
→ Incluir marcas de acción donde aplique: [PAUSA], [SEÑALAR CÁMARA], [ZOOM IN], [MOSTRAR PANTALLA]

[CTA — 45-55s]
Pregunta de engagement que invite a comentar.
Patrón CTA ganador F100K:
"¿Tú qué opinas de esto? Comenta [PALABRA DE 1-2 SÍLABAS] y te cuento [promesa de valor extra]."
```

Reglas del guion:
- Español neutro (no argentino, no regional)
- Sonar como lo escribió el usuario (respetar `voice_profile`)
- Máximo 120 palabras
- NO mencionar a ningún creador por nombre sin contexto
- SÍ mencionar la fuente/plataforma (ej: "este video de TikTok", "este artículo de The Verge")

---

## FASE 5 — ENVIAR EMAIL DIGEST

### Paso 5 — Crear email con Gmail MCP

Usar `mcp__claude_ai_Gmail__create_draft` con:

**Para:** `config.email`

**Asunto:**
```
🔥 Radar F100K — [día abreviado, fecha] | [primeras 40 chars del título del viral]
```
Ejemplo: `🔥 Radar F100K — Jue 29 May | OpenAI lanzó algo que cambia todo para creadores`

**Cuerpo (plain text con separadores visuales):**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯  EL VIRAL DEL DÍA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Título o caption del viral]

📍 Fuente: [TikTok @autor / Nombre del medio]
👁️  [métricas: "X.XM views" o "publicado en [medio]"]
🔗 [URL]

POR QUÉ REACCIONAR A ESTO:
→ [Razón 1 — relevancia para el nicho]
→ [Razón 2 — perspectiva única que puedes agregar]
→ [Razón 3 — momentum actual del tema]


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎬  TU GUION — LISTO PARA GRABAR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[GANCHO VISUAL]
[texto]

[CONTEXTO]
[texto]

[TU PERSPECTIVA]
[texto de los 3 puntos]

[CTA]
[texto]


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡  NOTAS DE PRODUCCIÓN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Duración estimada: 45-55 segundos
Formato sugerido: cara a cámara + texto overlay del punto clave
Mejor hora para publicar: dentro de las próximas 6-12h (el viral está caliente ahora)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Autopilot F100K · fórmula100k.app
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Paso 6 — Confirmar en terminal

```
✅ Radar enviado a [config.email]
📊 Viral del día: [título, primeras 50 chars]
🕐 [hora actual]
💰 Costo Apify estimado: ~$0.40
```
