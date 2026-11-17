---
name: radar-tendencias-f100k
description: "Módulo del Autopilot F100K que detecta tendencias emergentes ANTES de que lleguen al pico, dando 24-72h de ventana para publicar primero. Corre junto al radar diario de lunes a viernes. Usar cuando alguien diga: \"qué está despegando en mi nicho\", \"detectar tendencias emergentes\", \"qué va a ser viral pronto\", \"ejecutar radar tendencias\", \"dame las tendencias del día\", o cuando el schedule automático lo invoque. Si no hay tendencia emergente real, NO envía email (sin spam). Requiere cerebro/f100k-config.json."
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - La config no vive en la carpeta oculta de la Mac: léela de `cerebro/f100k-config.json`. Si no existe, créala con el nicho y las palabras clave de `USER.md` y `cerebro/`, y confírmala por Telegram. No mandes a correr rutina-maestra.
> - Señal de TikTok con Apify (`clockworks~tiktok-scraper`) solo si hay `APIFY_TOKEN`. Sin token, detecta con búsqueda web y dilo en la primera línea.
> - Tu búsqueda web es Tavily por Composio: `composio execute TAVILY_SEARCH -d '{"query":"…","max_results":5}'` (sección 2 del puente).
> - La «FASE 5 — email de alerta» NO manda correo: la alerta va por Telegram con el mismo formato. Si no hay tendencia real y la automatización no pide informe diario, no mandes nada.

---

# Skill: Radar de Tendencias Emergentes — Autopilot F100K

La diferencia entre ser el primero y ser el décimo en hablar de algo es 48 horas. Este módulo detecta lo que está despegando AHORA en tu nicho para que publiques antes de la ola, no después.

---

## FASE 1 — CARGAR CONFIG

```bash
cat cerebro/f100k-config.json
```

Si no existe → detener e instruir a correr `/rutina-maestra-formula100k`.

Extraer: `niche`, `keywords`, `email`

---

## FASE 2 — DETECCIÓN DE TENDENCIAS (3 señales)

### Señal 1 — TikTok: volumen de publicación acelerado

Buscar con Apify `clockworks~tiktok-scraper` para cada keyword:
```json
{
  "searchQueries": ["[keyword]"],
  "resultsPerPage": 50,
  "shouldDownloadVideos": false
}
```

Analizar el patrón temporal de los resultados:
- Contar videos publicados en las últimas 6h vs los publicados entre 6h-48h atrás
- **Spike = últimas 6h tienen 3x o más el promedio de las 6h anteriores**
- También observar: ¿algún video reciente acumula shares anormalmente rápido para su antigüedad?

### Señal 2 — Noticias: velocidad de propagación

Tavily `mcp__claude_ai_Tavily__tavily_search`:
```json
{
  "query": "[niche keyword] [keyword2] últimas horas noticia",
  "search_depth": "advanced",
  "max_results": 10
}
```

Contar cuántas fuentes distintas cubren el mismo tema en las últimas 24h:
- 1-2 fuentes = noticia normal → ignorar
- 3-5 fuentes = tendencia emergente ⚠️
- 6+ fuentes = tendencia confirmada 🔥

### Señal 3 — Términos léxicos nuevos

Comparar los captions de TikTok de hoy con el vocabulario de búsquedas anteriores (de memoria de la sesión o del contexto disponible):
¿Han aparecido 2+ videos usando la misma frase o término nuevo que no es parte de `config.keywords`?
Si sí → micro-tendencia léxica (nuevo meme-format, nuevo término para algo conocido)

---

## FASE 3 — CLASIFICACIÓN

Clasificar cada hallazgo:

| Nivel | Criterio | Acción |
|-------|----------|--------|
| 🔥 CALIENTE | Tendencia confirmada (6+ fuentes O spike 5x+) | Email URGENTE — publicar HOY |
| ⚠️ DESPEGANDO | Tendencia emergente (3-5 fuentes O spike 3x) | Email — publicar en 24-48h |
| 👀 OBSERVAR | Señal débil (1-2 fuentes O novedad léxica) | Solo mencionar si hay otro nivel presente |

**Regla de silencio:** si solo hay señales nivel OBSERVAR o nada → NO enviar email. El silencio significa "nada urgente hoy". Confirmar en terminal:
```
🔇 Radar Tendencias: sin tendencias emergentes hoy. No se envió email.
```

---

## FASE 4 — GENERAR GUION EXPRESS

Si hay tendencia nivel CALIENTE o DESPEGANDO, generar un guion rápido de 30-45s para aprovechar la ventana:

```
[GANCHO — 0-3s]
Referencia directa a la tendencia: "¿Ya viste lo que está pasando con [tema]?"

[QUÉ ES — 3-10s]
Una oración: qué es la tendencia y por qué importa ahora.

[TU ÁNGULO — 10-35s]
Por qué esto importa para [niche] del usuario.
2 puntos concretos de perspectiva única.
Voz: [voice_profile]

[CTA — 35-45s]
"Comenta [PALABRA] si quieres que haga un video completo sobre esto."
```

---

## FASE 5 — EMAIL DE ALERTA (solo si nivel ≥ DESPEGANDO)

Usar `mcp__claude_ai_Gmail__create_draft`:

**Para:** `config.email`

**Asunto:**
- Si CALIENTE: `🔥 URGENTE — tendencia confirmada en tu nicho: [tema]`
- Si DESPEGANDO: `⚠️ Tendencia emergente detectada — [tema] | Autopilot F100K`

**Cuerpo:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[🔥 CALIENTE / ⚠️ DESPEGANDO] — [TEMA EN MAYÚSCULAS]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ventana para publicar primero: [HOY MISMO / próximas 24-48h]

QUÉ ESTÁ PASANDO:
[2-3 líneas explicando la tendencia con datos concretos]

EVIDENCIA:
→ [Fuente 1 con URL]
→ [Fuente 2 con URL]
→ TikTok: [X] videos nuevos en las últimas [Y] horas sobre este tema

ÁNGULO PARA TU NICHO ([niche del usuario]):
[Sugerencia concreta de cómo conectar esta tendencia con tu contenido]


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎬  GUION EXPRESS — 30-45 SEGUNDOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[GANCHO]
[texto]

[QUÉ ES]
[texto]

[TU ÁNGULO]
[texto]

[CTA]
[texto]


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰  Actúa rápido — las tendencias tienen ventana corta.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Autopilot F100K · fórmula100k.app
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
