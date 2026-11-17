---
name: storytelling-animado-f100k
description: "Convierte una historia cruda (una anécdota, el caso de una clienta, un error propio) en un reel 9:16 de 45-90s listo para grabar: elige el molde narrativo, escribe el guion legible, decide qué beats se ganan un clip animado y los genera con los presets explainer de Higgsfield (Claymotion, Stickman Cartoon, Editorial Motion Graphics, Watercolor Chronicle, Pixel Art y más). Entrega GUION.md + clips + MANIFEST.md sincronizado por keyword. Activar cuando alguien diga 'hazme un reel de storytelling', 'te cuento lo que me pasó y arma el video', 'cuéntalo como historia', 'quiero contar el caso de mi alumna', 'narrativa con clips animados', 'un reel donde cuento esto'. NO usar para guiones que no son historia (guionizacion-formula100k) ni para YouTube largo."
allowed-tools: "Bash, Read, Write, Edit, AskUserQuestion, Skill, mcp__higgsfield__get_explainer_presets, mcp__higgsfield__resolve_explainer_preset, mcp__higgsfield__generate_image, mcp__higgsfield__generate_video, mcp__higgsfield__generate_image_batch, mcp__higgsfield__generate_video_batch, mcp__higgsfield__jobs_wait, mcp__higgsfield__job_status, mcp__higgsfield__show_generation_by_ids, mcp__higgsfield__models_explore, mcp__higgsfield__balance, mcp__claude_ai_Higgsfield__get_explainer_presets, mcp__claude_ai_Higgsfield__resolve_explainer_preset, mcp__claude_ai_Higgsfield__generate_image, mcp__claude_ai_Higgsfield__generate_video, mcp__claude_ai_Higgsfield__generate_image_batch, mcp__claude_ai_Higgsfield__generate_video_batch, mcp__claude_ai_Higgsfield__jobs_wait, mcp__claude_ai_Higgsfield__job_status, mcp__claude_ai_Higgsfield__show_generation_by_ids, mcp__claude_ai_Higgsfield__models_explore, mcp__claude_ai_Higgsfield__balance"
delegates-to: ["storytelling-f100k", "guionizacion-formula100k", "editor-video-formula100k"]
metadata: {"version": "1.0.0", "mcp-required": ["higgsfield"], "openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Los clips animados salen de los presets explainer del plugin de Higgsfield: solo si está conectado. El plan de clips y el costo total se aprueban con ✅ antes de generar.
> - Las preguntas con opciones van por Telegram, numeradas. Las previews de presets se mandan como links.
> - Sin Higgsfield: entrega GUION.md + la tabla de beats con el prompt de cada clip.
> - La composición final (`editor-video-formula100k`) no corre en este servidor: entrega GUION.md, clips y MANIFEST.md en `entregables/storytelling/` para editarlos en la compu.

---

# Storytelling Animado — FÓRMULA 100K

Recibe una historia en bruto y devuelve una carpeta lista para grabar y editar: el guion, los
clips animados que la historia necesita, y el MANIFEST que los sincroniza.

**Esta skill no graba ni compone.** Termina donde empieza `editor-video-formula100k`.

---

## 🧭 ANCLAJE DE RUBRO (leer PRIMERO — manda sobre cualquier ejemplo de esta skill)

Esta skill enseña un **método narrativo**. El método es agnóstico de industria: sirve igual
para fisioterapia, repostería, formulación cosmética, finanzas o jardinería. Los ejemplos
escritos aquí y en los referenciales son ilustraciones **del método**, nunca del tema.

**Antes de escribir nada:**

1. Identifica el **RUBRO real** de la persona (de su Segundo Cerebro, de su perfil, o
   pregúntaselo en una línea). Decláralo: *"Rubro: ___"*.
2. Toda la historia, los objetos de la escena, el villano, las cifras y el vocabulario salen
   de **ESE** rubro.
3. Si el rubro **no** es marketing, redes, creación de contenido o negocios digitales →
   queda **PROHIBIDO** ese vocabulario (algoritmo, engagement, embudo, lead magnet, alto
   ticket, escalar tu negocio, posicionarte como referente), salvo que la persona lo escriba
   primero.
4. Si el rubro es técnico o de oficio: **no borres el tecnicismo** para "simplificar". Úsalo
   y tradúcelo en su primera mención. El término preciso ES su autoridad.
5. Si faltan datos del negocio, dilo y usa marcadores (`[TU OFERTA]`, `[TU RESULTADO]`).
   **Nunca asumas que el rubro es marketing.**

---

## Cuándo activar

Cuando alguien trae **una historia** (algo que pasó, con personas y consecuencias) y quiere
un reel. Señales: "te cuento lo que me pasó", "quiero contar el caso de", "hazme un reel
narrativo", "cuéntalo como historia", "story con animación".

**Si todavía no tiene la historia** — "no sé qué contar", "estoy atascada", "ayúdame a
encontrar mi historia" — eso es `storytelling-f100k`, el coach: hace preguntas hasta sacarla
en sus propias palabras y no escribe nada por ella. Cuando salga de ahí con la historia en
crudo, vuelve aquí para producirla.

**Sobre el B-roll grabado:** `storytelling-f100k` enseña el hábito de grabar metraje real en
tres baldes (problema / proceso / payoff). Eso y esta skill son complementarios y no
compiten: **se filma lo que se puede filmar, se anima solo lo que no.** Si ya tiene clips
reales para un beat, ese beat no necesita clip generado.

## NO activar para

- Encontrar o destrabar la historia → `storytelling-f100k`
- Guion que no es historia — tips, lista, tutorial, opinión → `guionizacion-formula100k`
- Video 100% animado sin cámara → workflow `faceless-channel-video` de Higgsfield
  (`get_workflow_instructions({workflow: "faceless-channel-video"})`)
- YouTube largo → `guion-youtube-formula100k`
- Historias de Instagram (stories) → `guionizacion-historias-formula100k`
- Componer el video ya grabado → `editor-video-formula100k`
- Un anuncio pagado → `guionizacion-ads-formula100k`

---

## Referenciales obligatorios

Cargar ANTES de empezar. No es opcional:

1. `references/moldes-historia.md` — los 8 arcos narrativos y cómo se elige
2. `references/clips-de-apoyo.md` — la compuerta visual, los prompts, la receta de generación y el MANIFEST
3. `references/catalogo-clips-higgsfield.md` — los 24 presets con sus IDs

---

## Proceso

### Paso 1 — Intake

Máximo **5 preguntas**, una a la vez, con `AskUserQuestion` cuando haya opciones claras.
Lo que hay que sacar y que nadie da espontáneamente:

1. ¿Quién era y dónde estaba? (una escena, no un contexto)
2. ¿Qué se rompió, exactamente?
3. ¿Qué creías antes de que pasara?
4. ¿Qué viste que no habías visto?
5. ¿Qué se lleva quien mira esto?

Si ya vino todo en el mensaje inicial, no preguntes. **Nunca inventes el detalle que falta:**
si no sabes la escena, pregúntala o déjala como marcador.

### Paso 2 — Molde

Elegir el arco con la tabla de `moldes-historia.md` (la pregunta es *de quién es el costo*).
Declarar cuál elegiste y por qué en una línea. Si dudas entre dos, gana el que tenga una
escena concreta.

### Paso 3 — Guion

Escribir el guion siguiendo los beats del molde, con el tiempo objetivo de 45-90s.

**El gancho del segundo 1 pasa por LA APUESTA** — (Magnitud × Credibilidad) ÷ Costo — y se
construye en tríada: verbal (lo que dice), visual (lo que se ve) y textual (el header). Los
tres apuntan al mismo sitio o se anulan.

**Formato del `GUION.md`** — el guion limpio arriba, para leer de corrido frente a cámara.
Todo lo demás va abajo del marcador:

```markdown
# <título>

<solo lo que se dice frente a cámara, en párrafos cortos, sin acotaciones>

=== EXPLICACIÓN ===

- Molde: ...
- Por qué este gancho: ...
- Dónde cae el giro: ...
- Beats que se ganaron clip y por qué: ...
```

Para el **header** (las dos líneas que viven sobre su cara los primeros 8s), invocar
`guionizacion-formula100k` pidiendo 3 variantes de gancho textual y ofrecerlas con
`AskUserQuestion`. 3-5 palabras por línea, sentence case, nunca all caps.

Si el usuario tiene una skill de calibración de guion propia de su cuenta, pasarlo por ahí
antes de seguir al Paso 4.

### Paso 4 — Compuerta visual

Recorrer el guion beat por beat y aplicar la compuerta de `clips-de-apoyo.md`. Un beat se
gana un clip solo si es pasado, invisible, de escala imposible, metáfora, o es el giro.

Techos: **máximo 5 clips**, **máximo 6s cada uno**, **ninguno antes del segundo 5**, y el
giro siempre lleva uno.

Presentar la tabla propuesta y pedir aprobación con `AskUserQuestion` antes de gastar nada.
Si la historia solo se gana 2 clips, se hacen 2 — no se rellena.

### Paso 5 — Preset

Ofrecer **3 presets candidatos** del catálogo según el tono, con su `video_url` de preview
para que los vea sin gastar créditos. Elegir **uno solo** y resolverlo:

```
resolve_explainer_preset({ preset_id }) → media_id
```

Ese `media_id` va en todos los frames. **Nunca mezclar presets dentro del mismo video.**

### Paso 6 — Generar y armar la carpeta

1. **Preflight de créditos** con `get_cost: true` en imagen y video, multiplicar por el
   número de clips, comparar contra `balance()` y **decirle el total antes de disparar**.
2. Generar el frame de cada beat (`generate_image` con el `media_id` como referencia de
   estilo), luego animarlo (`generate_video`, `9:16`, 4-6s, **`generate_audio: false`**).
3. Descargar a `clips/clipNN.mp4`, numerados por orden de aparición en el guion.
4. Escribir el `MANIFEST.md` con el formato exacto de `clips-de-apoyo.md`, keywords
   **verbatim del guion**, 4-8 palabras, sin solapamientos.

**Salida:**

```
<carpeta del proyecto>/YYYY-MM-DD_<slug>/
├── GUION.md
├── MANIFEST.md
└── clips/clip01.mp4 …
```

**Preguntar dónde guardar** la primera vez y recordarlo para las siguientes. No inventar una
ruta ni asumir que existe una carpeta de proyectos: si no la hay, proponer
`entregables/storytelling/` y confirmar.

Cerrar diciendo qué sigue: graba la toma, y después
`/render <carpeta>/YYYY-MM-DD_<slug>/ <ruta del .mov>`.

---

## Reglas duras

1. **Nunca inventar un dato, una cifra ni una cita.** Si la historia trae un número, se
   verifica o se cuenta sin número. Un caso sin cifra es creíble; uno con cifra inventada
   quema a la creadora entera.
2. **Nunca identificar a una clienta o alumna** sin permiso explícito. "Una alumna", nunca
   el @.
3. **Un solo giro.** Si la historia tiene dos, el segundo es otro reel.
4. **Los clips son apoyo, no el video.** Si al final los clips cuentan la historia mejor que
   la toma a cámara, el formato correcto era `faceless-channel-video` y hay que decirlo.
5. **Sin texto dentro de los clips.** El texto vive en el header, sobre la cara.
6. **No quemar créditos sin aprobación explícita** del plan de clips y del costo total.
7. **La historia manda sobre el catálogo.** Si ningún preset le queda al tono, se dice y se
   entrega el guion solo. No se fuerza un estilo que no encaja.

---

## Gotchas

- **`resolve_explainer_preset` verificado el 2026-08-09**: `preset_id` → `media_id` reusable.
  Si algún día deja de devolverlo, el plan B está en `clips-de-apoyo.md` §8.
- **El preset `pppppppppp` es basura de test** del proveedor. Nunca ofrecerlo.
- **`generate_audio: false` siempre.** Los clips van bajo su voz; el audio nativo mete ruido
  y cuesta más. En `kling3_0` el parámetro es `sound: "off"`.
- **El rol de la referencia de estilo en `generate_image` no se adivina** — varía por modelo.
  Consultar `models_explore({action:"get", model_id})` y leer `medias[].roles`.
- **`use_unlim` se omite.** Si el servidor devuelve `unlim_choice`, esa pregunta es para
  la persona, no una decisión propia.
- **Keyword que no se dice = cue descartado en silencio.** Elegir sustantivos concretos que
  sobrevivan a la improvisación, no conectores.
- **Dos B-roll solapados rompen el render.** Mínimo 8 segundos de guion entre keywords.
