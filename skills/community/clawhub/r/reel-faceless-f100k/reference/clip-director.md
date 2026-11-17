# Clip Director — Motor compartido de generación de clips por gancho

Este es el **cerebro reutilizable**. No es un script: es la lógica que el agente sigue
leyendo el transcript para decidir, segmento por segmento, qué visual generar. Lo consumen
dos skills:

- `reel-faceless-f100k` en **modo `full`** (los clips SON el video, 9:16).
- `editor-video-formula100k` en **modo `support`** (clips de apoyo sobre la toma del usuario, 16:9).

---

## 1. Contrato

**Entrada:**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `transcript` | array `{text, start, end}` | palabras con timestamps (word-level) |
| `formato` | `9:16` \| `16:9` | portrait (full) u horizontal (support) |
| `modo` | `full` \| `support` | `full` = los clips llenan el frame y el timeline; `support` = clips de apoyo anclados por keyword |

**Salida:** `plan` = array de segmentos:

```json
{
  "start": 0.0,
  "end": 3.0,
  "visual_type": "broll",
  "prompt": "prompt de Higgsfield (broll/pixel) o texto de la card (card)",
  "asset_path": "assets/seg0.mp4",
  "keyword": null
}
```

- `visual_type` ∈ `broll` | `card` | `pixel`
- `prompt`: prompt en inglés para Higgsfield (`broll`/`pixel`) o el texto/estructura de la card (`card`)
- `asset_path`: ruta relativa al asset generado. Se llena **después** de generar (vacío en la propuesta inicial)
- `keyword`: en modo `support`, la frase **verbatim** del transcript donde se ancla el clip (8-15 palabras); en modo `full` es `null` (se usa `start`/`end`)

---

## 2. Clasificación por gancho

Segmentar el transcript en bloques de 3-6 s (o por unidad de sentido). Para cada bloque,
detectar la **intención** y asignar `visual_type`. La tabla es generosa: NO esperes la frase
literal.

| Intención del segmento | `visual_type` | Señales (no requieren literalidad) |
|------------------------|---------------|-------------------------------------|
| Concepto / narrativa / aspiracional / autoridad | `broll` | afirmaciones, storytelling, "imagina", "el problema es", transformación, credibilidad, "yo hice X" |
| Dato / cifra / comparación / enumeración / definición | `card` | números (K/M/%/$), "antes/ahora", "3 razones", "la clave es", listas, pasos |
| Remate / chiste / cultura pop / punchline | `pixel` | humor, referencia pop, cierre de sección con gracia, ironía |

### Regla de mezcla (anti-monotonía) — OBLIGATORIA

En un reel de 30–90 s: **≥2 `visual_type` distintos** y **ninguno domina >60%** de los
segmentos.

- Si el guion es 100% conceptual → convertir el **dato más claro** en `card` y el **remate
  más fuerte** en `pixel`.
- Un reel que sale 100% `broll` está mal clasificado: siempre hay al menos un dato o un remate.

---

## 3. Receta `broll` — Higgsfield cinemático

Motor: `mcp__higgsfield__generate_video`. Mismo patrón que `broll-vsl-formula100k` (media
upload/confirm + generate + poll `job_status` sync, lotes de 8, declinar presets, anti-NSFW).

```python
mcp__higgsfield__generate_video(
    model="seedance_2_0",
    prompt="<prompt_completo>",
    aspect_ratio="9:16",      # modo full → "9:16"; modo support → "16:9"
    duration=5,
    resolution="1080p",
    genre="<action|epic|drama|comedy>",
    medias=[{"value": "<media_id>", "role": "image"}]   # SOLO si el segmento es sobre el usuario
)
```

- **Con avatar** (segmento sobre el usuario, su logro, su historia): subir foto de
  `cerebro/fotos` (media_upload → PUT → media_confirm), pasar
  `medias`, y cerrar el prompt con `, character inspired by the reference image provided,
  maintain facial features from reference`. Descripción de persona:
  la descripción física de la usuaria sacada de SUS fotos (nunca un ejemplo fijo).
- **Cinemático puro** (concepto abstracto: sistemas, IA, tiempo, datos): sin `medias`, sin
  mención de persona.

**Estructura de prompt por estética** (copiar de `broll-vsl-formula100k` Paso 5): cyberpunk
(default, azul eléctrico #00BFFF), cálido (ámbar/golden hour, nicho femenino), minimalista
(blanco-gris-negro). Cerrar siempre con `9:16 cinematic composition, 5-second continuous
motion` (o `16:9` en support).

**Anti-NSFW** (de `broll-vsl-formula100k`): evitar `noir` + macro + oscuridad; nada de
"emerges from complete darkness" (usar "appears in a dimly lit environment"); géneros seguros
`action`/`epic`/`drama`/`comedy`. Si un prompt es rechazado: simplificar, quitar
oscuridad/intimidad, ampliar a plano general.

---

## 4. Receta `card` — HyperFrames kinético

Motor: HyperFrames CLI + GSAP (mismo stack que `motion-reels-f100k`). Reusar los templates
Comparison / Chapter / Quote / Kinetic de esa skill.

- **Fondo:** `#FF00FF` (magenta, para chromakey). NUNCA verde, NUNCA transparent.
- **Modo `full`:** la card ocupa **todo el frame** 1080×1920 — centrada, grande, sin zona
  segura (no hay cara que evitar). El fondo magenta se reemplaza en composición por el B-roll
  contiguo o un fondo de color/gradiente.
- **Modo `support`:** la card es un **overlay** en zona segura — usar `SAFE_CARD_CSS` de
  `motion-reels-f100k` (bottom: 250px) para no tapar la cara del usuario.
- Animación: entrada `gsap.from()` / `fromTo()` + salida `gsap.to()` 0.5-0.6 s antes del
  final (reglas de `motion-reels-f100k`). ⚠ Nunca `opacity:0` en CSS + `.from({opacity:0})`:
  usar `fromTo` (lección confirmada F100K).
- Mapear la intención a template: comparación/antes-ahora → Comparison; enumeración/pasos →
  Chapter; definición/cita → Quote; palabra-fuerza → Kinetic Word.
- Render: `hyperframes render --format mp4 -o <asset>.mp4` (NUNCA `--format webm`: VP9 sale
  sin alpha real).

---

## 5. Receta `pixel` — meme / pixel-art

Motor preferido: `recursos-pixel-formula100k` si está disponible en el entorno. Si no:

```python
mcp__higgsfield__generate_image(
    prompt="<concepto> in 32-bit pixel art style, retro game aesthetic, on a solid #FF00FF magenta background, no text",
    ...
)
```

- Se usa para remates/punchlines/cultura pop — momentos de humor o cierre con gracia.
- Sobre chroma magenta para poder componerlo; o como card-meme full-frame en modo `full`.
- SFX "pop" al aparecer (coherente con el editor).
- **Fallback:** si no hay créditos o el motor pixel no está, degradar este segmento a `card`
  (Kinetic Word con la palabra del remate).

---

## 6. Degradación elegante

Nunca fallar en seco. Antes de generar, verificar créditos con `mcp__higgsfield__balance`.

| Situación | Acción |
|-----------|--------|
| Sin créditos Higgsfield | Todos los `broll`/`pixel` caen a `card` (HyperFrames, gratis/local). Avisar al usuario. |
| Motor pixel no disponible | Segmento `pixel` → `card` (Kinetic Word). |
| Segmento sin clasificación clara | Default a `card`. |
| Audio no transcribible / muy ruidoso | Avisar y pedir regrabar ese tramo (no inventar timestamps). |
| Prompt Higgsfield rechazado por NSFW | Reformular (simplificar + quitar oscuridad); si reincide, ese segmento → `card`. |
| Se necesita apoyo pero sin generación | Cazar recurso real con `recursos-de-video-formula100k` en vez de generar. |
