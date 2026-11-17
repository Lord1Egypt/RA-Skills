---
name: tutorial-viral-f100k
description: "Orquesta un tutorial viral faceless (sin cara) de FÓRMULA 100K: de una idea o guion a un kit listo para montar. Fase 1 guion con marcas [PANTALLA]/[CARD]/[CTA]; Fase 2 brief de grabación (voz real + pantallas que graba la usuaria); Fase 3 genera cards, mockups y B-roll con Higgsfield o Gemini y capturas tipo tutorial en PNG; Fase 5 entrega GUION.md, BRIEF_GRABACION.md, MANIFEST.md (qué card entra en qué palabra) y un .zip de recursos por Telegram para montarlo en CapCut. En este agente no renderiza ni edita el video; opcional: un borrador juntando clips generados en Higgsfield. Activar cuando se diga: 'tutorial viral', 'explicación viral faceless', 'video sin cara', 'hazme un tutorial de X', 'video tipo screen recording con captions', '/tutorial <tema>'. NO usar para talking-head reels, carruseles, stories ni miniaturas."
allowed-tools: "Bash, Read, Write, Edit, AskUserQuestion, Skill"
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Fases 1, 2 y 3 corren igual. **La Fase 4 (`render_tutorial.py`, Remotion, corte de silencios, captions cinéticos quemados) no corre aquí** y los scripts no vienen en este paquete.
> - Fase 2: el brief va por Telegram. La usuaria NO te manda voz ni pantallas para renderizar: las graba y las monta ella en CapCut (u otro editor) con el kit que le entregas.
> - Fase 3: cards, títulos y CTA con el plugin de Higgsfield (`nano_banana_2`) o `GEMINI_API_KEY`; capturas de terminal/pasos/callouts con `capturas-tutorial-formula100k` (HTML → PNG con Chromium); capturas de webs sin login con tu navegador. B-roll animado con Higgsfield (video). Todo con costo total → ✅ → generar.
> - Si pide «un borrador sin grabar»: genera un clip de Higgsfield por beat del guion (mismo formato 9:16 y fps) y júntalos con `ffmpeg -f concat -safe 0 -i lista.txt -c copy borrador.mp4`. Nada más: sin subtítulos, sin overlays, sin mezclar voz.
> - Fase 5 en lugar de `BORRADOR_AUTO.mp4`: `GUION.md`, `BRIEF_GRABACION.md`, `MANIFEST.md` (qué card entra en qué palabra) y un `.zip` con `IA/` y `WEB/`, en `entregables/tutoriales/<fecha>_<slug>/` y por Telegram. Dile que los captions los saque con los subtítulos automáticos de su editor.
> - Recursos web: nunca stock ni imágenes de redes con sesión iniciada; si un recurso no se pudo verificar mirándolo, no entra al MANIFEST.

---

## 🧭 ANCLAJE DE RUBRO (leer PRIMERO — manda sobre cualquier ejemplo de esta skill)

Esta skill enseña un **método**. El método es agnóstico de industria: sirve igual para
formulación cosmética, nutrición, repostería, fisioterapia, finanzas o jabonería.
Los ejemplos escritos aquí abajo son ilustraciones **del método**, nunca del tema.

**Antes de escribir nada:**

1. Identifica el **RUBRO real** de la persona (léelo de su Segundo Cerebro, de su perfil o
   pregúntaselo en una línea si no está claro). Decláralo: *"Rubro: ___"*.
2. Todos los ejemplos, analogías, comparaciones, objeciones, métricas y vocabulario salen
   de **ESE** rubro.
3. Si el rubro **no** es marketing, redes sociales, creación de contenido, ventas online o
   negocios digitales → queda **PROHIBIDO** el vocabulario de ese mundo (reels, algoritmo,
   embudo, lead magnet, engagement, "publicar sin vender", "clientes de alto ticket",
   "escalar tu negocio", "posicionarte como referente"), salvo que la persona lo escriba primero.
4. Si el rubro es **técnico, científico o de oficio**: NO borres el tecnicismo para
   "simplificar". Úsalo y **tradúcelo en su primera mención**. El término preciso ES la
   autoridad de esa creadora; quitarlo borra justo lo que la diferencia.
5. Si no tienes datos suficientes del negocio, dilo y usa marcadores explícitos
   (`[TU OFERTA]`, `[TU RESULTADO]`). **Nunca asumas que el rubro es marketing.**

**El método viaja, el rubro no.** El mismo molde, vestido con rubros distintos:

| Rubro | El mismo molde |
|---|---|
| Cocina | "Así es mi cena favorita para no dormir con el azúcar alta." |
| Relaciones | "5 señales de que estás forzando una relación que ya no funciona." |
| Finanzas | "La principal causa de un divorcio no es una infidelidad." |
| Formulación cosmética | "El conservante decide si tu crema dura tres meses o te da una infección. No el aceite." |
| Jabonería | "Si tu jabón se pone blando a los dos días, no fue el aceite. Fue la sosa." |
| Fisioterapia | "Ese dolor de rodilla al bajar escaleras casi nunca nace en la rodilla." |
| Repostería | "Tu bizcocho se hunde en el centro por la temperatura, no por la harina." |
| Jardinería | "Tu planta no se está muriendo de sed. Se está ahogando." |

Mismo molde en todos; ninguno menciona reels ni embudos. Haz exactamente eso.

---

# Tutorial Viral Faceless — FÓRMULA 100K

Pipeline de extremo a extremo para producir tutoriales cortos virales **sin cara** (faceless): screen recording + cards generadas por IA + captions cinéticos automáticos + voz real del usuario. De una idea a un `BORRADOR_AUTO.mp4` listo para retoque en CapCut/Premiere.

La referencia de este diseño: un reel tutorial faceless con screen-recording, captions cinéticos y cards pop-in.

---

## Cuándo activar

Cuando el usuario:
- Pide un tutorial o explicación: "hazme un tutorial de X", "tutorial viral de X", "explicación faceless de X"
- Menciona video sin cara / screen recording: "video tipo screen recording con captions", "sin cara", "faceless"
- Usa atajos: `/tutorial <tema>` o `/tutorial-render <carpeta>`
- Quiere replicar el estilo de captions cinéticos a pantalla completa con cards pop-in

## NO activar para

- **Talking-head reels** (el usuario con su cara) → `editor-video-formula100k`
- **Carruseles** → `carrusel-render-formula100k`
- **Stories** → `historias-a-imagenes-nanobanana`
- **Miniaturas YouTube** → `miniatura-youtube-formula100k`
- **Publicar en IG** → `publicar-ig`

---

## Atajos conversacionales

- `/tutorial <tema>` → arranca desde Fase 1 (guion). Ejemplo: `/tutorial cómo usar Claude Code`
- `/tutorial-render <carpeta>` → salta directo a Fase 4 (re-render) con una carpeta ya existente que tenga `MANIFEST.md`, `captions.json` y `USER/voz.*`

---

## Convención `$DEST`

Todas las carpetas del proyecto viven en:

```
entregables/tutoriales/<fecha>_<slug>/
```

Ejemplos:
- `entregables/tutoriales/2026-06-18_como-usar-claude-code/`
- `entregables/tutoriales/2026-06-20_automatiza-con-ia/`

La skill crea la carpeta si no existe. El slug se genera del tema (minúsculas, guiones, sin tildes).

---

## Las 5 Fases (1 solo checkpoint humano)

```
FASE 1  Guion
FASE 2  Plan + Brief de grabación   ⏸ ÚNICO CHECKPOINT HUMANO
FASE 3  Generación de recursos
FASE 4  Ensamblaje + render
FASE 5  Entrega
```

---

### Fase 1 — Guion

Invocar la skill `guionizacion-formula100k` con estructura tutorial/explicación:
- Gancho del top 1% (primeros 3s retienen o pierden)
- Cuerpo con pasos o revelaciones (pace rápido, sin relleno)
- CTA final accionable

El guion lleva **marcas inline** que definen qué hace cada capa:

| Marca | Significado | Responsable |
|-------|-------------|-------------|
| `[PANTALLA: descripción]` | Captura o grabación de pantalla específica | el usuario graba |
| `[CARD: idea/concepto]` | Tarjeta visual, mockup o ilustración | Skill genera |
| `[CTA: texto]` | Tarjeta final de llamada a la acción | Skill genera |

Si el usuario trae un guion propio, la skill lo normaliza a este formato antes de continuar.

**Guardar como:** `$DEST/GUION.md`

---

### Fase 2 — Plan de recursos + Brief de grabación ⏸

Esta es la **única pausa humana** del pipeline.

La skill:
1. Separa el GUION.md en dos listas: "lo que YO genero" (CARD/CTA) vs "lo que TÚ grabas" (PANTALLA + voz)
2. Genera `$DEST/BRIEF_GRABACION.md` (ver plantilla abajo)
3. Crea la carpeta `$DEST/USER/` con instrucciones

Luego espera con `AskUserQuestion`: "¿Ya pegaste los archivos en `$DEST/USER/`? Cuando estén listos seguimos con la Fase 3."

El usuario entrega:
- `$DEST/USER/voz.m4a` (o `.wav`, `.mp3`) — su voz leyendo el guion completo de corrido
- `$DEST/USER/pantalla_01.mov`, `pantalla_02.mov`, … — grabaciones de pantalla mudas numeradas

---

### Plantilla de `BRIEF_GRABACION.md`

```markdown
# Brief de grabación — <título del video>

## 🎙️ Tu voz
Lee este guion completo de corrido y mándame el audio (un solo archivo):

<guion limpio para leer, sin las marcas [PANTALLA]/[CARD]/[CTA]>

→ Guarda como: voz.m4a (o el formato que tengas)

## 🖥️ Pantallas a grabar (mudas, sin narrar)
1. [~0:03–0:10] Abrir <herramienta> y escribir el prompt "<texto>"   (~7s)
2. [~0:11–0:18] Mostrar <resultado generándose>                       (~7s)
3. CAPTURA (screenshot): pantalla final del resultado

## 📦 Cómo mandármelo
Pega los archivos en: $DEST/USER/
```

Cada pantalla numerada incluye: qué mostrar, duración aproximada, y a qué línea del guion corresponde. La duración estimada es orientativa — el ensamblaje las ancla por keyword del transcript, no por timestamp.

---

### Fase 3 — Generación de recursos

Con el GUION.md en mano (antes de que el usuario grabe), la skill genera todos los assets IA:

| Recurso | Herramienta | Destino |
|---------|-------------|---------|
| Cards / títulos / mockups de texto | `banana` (Nano Banana / Gemini) con brandkit F100K | `$DEST/IA/` |
| Capturas UI y mockups de herramientas | `capturas-tutorial-formula100k` | `$DEST/IA/` |
| Ilustraciones y B-roll generado | Higgsfield (Seedance 2.0) | `$DEST/IA/` |
| Recursos web (B-roll de apoyo) | búsqueda web + descarga | `$DEST/WEB/` |

La skill puede arrancar Fase 3 en paralelo mientras el usuario graba (si el usuario lo indica). Por defecto espera la confirmación del checkpoint.

---

### Fase 4 — Ensamblaje + render (en OpenClaw NO corre: mira el bloque 🦞 de arriba)

Una vez que `$DEST/USER/voz.*` existe:

**Comando único:**
```bash
python3 skills/tutorial-viral-f100k/scripts/render_tutorial.py "$DEST" "$DEST/USER/voz.<ext>"
```

Reemplazar `<ext>` con la extensión real del archivo (`m4a`, `wav`, `mp3`).

Lo que hace internamente:

1. **Corte de silencios** (`cut_silences_and_fillers.py` del motor) — produce `_voz_cut.m4a` y `captions.json` (word-level timestamps). La voz es la fuente de verdad del timeline.
2. **MANIFEST.md → `cues.json`** (`manifest_to_cues.py`) — ancla los cues a keywords del transcript. Avisa si alguna keyword no aparece en el transcript.
3. **Setup de `public/`** — vincula `IA/`, `WEB/` y el audio cortado al template Remotion.
4. **Render** con composición `tutorial-faceless` → `$DEST/BORRADOR_AUTO.mp4` (1080×1920 @ 30fps).

Tiempo típico: ~3–5 min por minuto de audio en Apple Silicon.

---

### Fase 5 — Entrega

Outputs finales:

| Archivo | Descripción |
|---------|-------------|
| `$DEST/BORRADOR_AUTO.mp4` | Video renderizado listo para retoque |
| `$DEST/MANIFEST.md` | Cues keyword-based para iterar sin re-transcribir |
| `$DEST/captions.json` | Word-timestamps (fuente de verdad del timeline) |
| `$DEST/GUION.md` | Guion con marcas (referencia para iteración) |
| `$DEST/BRIEF_GRABACION.md` | Archivado para referencia futura |

La skill reporta duración del borrador y abre el archivo con `open "$DEST/BORRADOR_AUTO.mp4"`.

---

## El preset visual `tutorial-faceless`

1080×1920 @ 30fps. Capas de fondo a frente:

1. **Fondo** — clip de screen recording a pantalla completa (`object-fit: cover`) con tratamiento "monitor" (rotación leve + viñeta radial), **o** card/B-roll generado fullscreen cuando no hay pantalla, **o** negro `#0d0d0d` en los gaps.
2. **Tarjeta-gancho de apertura** (~2–4s iniciales) — título grande en bold con marca F100K, pop-in con spring. Gancho de retención del primer segundo.
3. **Captions cinéticos AUTO** — 1–2 palabras a la vez, Inter 800, trazo negro (`WebkitTextStroke`), spring por palabra, sincronizados con la voz vía `captions.json`. **Generados automáticamente del transcript — cero entrada manual.** Posición default: lower-third (para no tapar las cards centrales; configurable en MANIFEST).
4. **Cards / overlays pop-in** — capturas, mockups, ilustraciones ancladas a keywords. Como no hay cara que proteger, **pueden ocupar el centro** con rotación sutil + spring de entrada + SFX "pop".
5. **Tarjeta CTA final** — estilo "Comenta X / por DM".

**Reglas de oro:**
- Captions cinéticos cubren toda la narración (a diferencia de `editor-video-formula100k` que va sin subtítulos)
- Sentence case en captions y cards — nunca all caps quemado por defecto (salvo títulos de diseño)
- SFX "pop" dispara al aparecer cada card/overlay (reusa `pop.wav` del motor)
- Animar solo `transform` y `opacity` (principios Emil Kowalski)
- La voz es REAL — no hay TTS en este pipeline

---

## Esquema del MANIFEST.md faceless

Extiende el parser keyword-based existente (`manifest_to_cues.py`). Esqueleto mínimo:

```markdown
# Tutorial — <título corto>

- **Voz fuente:** USER/voz.m4a
- **Fecha:** 2026-06-18

## Tarjeta gancho

- **Archivo:** `IA/HOOK_<slug>.png`
- **Duración:** 3.0

## Fondo

| Keyword     | Archivo                    | Duración | Estilo    |
|-------------|----------------------------|----------|-----------|
| prompt      | USER/pantalla_01.mov       | 7.0      | monitor   |
| resultado   | USER/pantalla_02.mov       | 7.0      | monitor   |
| herramienta | IA/card_fullscreen_01.png  | 5.0      | fullscreen|

## Cards

| Keyword     | Archivo                     | Ancho | Duración | Posición | Rotación |
|-------------|-----------------------------|-------|----------|----------|----------|
| automatiza  | IA/card_automatiza.png      | 800   | 2.5      | center   | -2       |
| gratis      | IA/card_gratis.png          | 760   | 2.0      | center   | 1        |

## B-roll

| Keyword     | Archivo                     | Duración | Estilo     |
|-------------|-----------------------------|----------|------------|
| internet    | WEB/broll_ai_demo.mp4       | 3.0      | fullscreen |

## CTA

- **Archivo:** `IA/CTA_comenta.png`
- **Duración:** 4.0

## Captions

- **Estilo:** lower-third
- **Posición:** lower-third
- **Activar:** sí
```

### Diferencias con el MANIFEST del preset talking-head

| Sección | talking-head (`editor-video`) | tutorial-faceless (esta skill) |
|---------|-------------------------------|-------------------------------|
| `## Header` | Gancho textual 2 líneas sobre la cara | **No aplica** (reemplazado por `## Tarjeta gancho`) |
| `## Énfasis` | Caja blanca en zona inferior | **No aplica** (las cards toman el centro) |
| `## Overlays` | Tercio inferior, no tapa la cara | `## Cards` — pueden ir al centro |
| `## Subtítulos` | Desactivados | **Activados automáticamente** del transcript |
| `## Fondo` | No existe (es el video del usuario) | Segmentos de screen recording o cards fullscreen |
| `## Tarjeta gancho` | Sticker esquina superior | Card de apertura fullscreen (2–4s) |
| `## CTA` | No existe como sección propia | Tarjeta final dedicada |

---

## Estructura de archivos en `$DEST`

```
$DEST/
├── GUION.md                   ← guion con marcas [PANTALLA]/[CARD]/[CTA]
├── BRIEF_GRABACION.md         ← instrucciones de grabación para el usuario
├── MANIFEST.md                ← cues faceless (consumido por el render)
├── USER/                      ← archivos que entregal usuario
│   ├── voz.m4a
│   └── pantalla_01.mov ...
├── IA/                        ← cards, mockups, ilustraciones generadas
├── WEB/                       ← B-roll / recursos web
├── _voz_cut.m4a               ← voz cortada (sin silencios)
├── captions.json              ← word-timestamps (fuente de verdad del timeline)
├── cues.json                  ← input Remotion (regenerado en cada render)
└── BORRADOR_AUTO.mp4          ← OUTPUT FINAL
```

---

## Requisitos previos (en OpenClaw NO corre: mira el bloque 🦞 de arriba)

Esta skill **reutiliza el motor de `editor-video-formula100k`** (Node/ffmpeg/Whisper/Remotion). Si ya usas esa skill, no hay nada más que instalar.

Si es la primera vez en esta máquina:
```bash
bash skills/editor-video-formula100k/scripts/bootstrap.sh
```

Solo verificar sin instalar:
```bash
bash skills/editor-video-formula100k/scripts/bootstrap.sh --check
```

Requiere **Homebrew** instalado previamente en macOS. Si no lo tienes:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

---

## Iteración y re-render (en OpenClaw NO corre: mira el bloque 🦞 de arriba)

**Cambiar un cue del MANIFEST:**
1. Editar la fila en `$DEST/MANIFEST.md` (keyword, archivo, duración, posición)
2. Re-correr: `python3 skills/tutorial-viral-f100k/scripts/render_tutorial.py "$DEST" "$DEST/USER/voz.<ext>"`
   El corte se saltea si `_voz_cut.m4a` ya existe.

**Re-grabar solo la voz** (sin re-grabar las pantallas):
1. Reemplazar `$DEST/USER/voz.m4a` con el nuevo archivo
2. Borrar `$DEST/_voz_cut.m4a` y `$DEST/captions.json`
3. Re-correr el comando de render

**Cambiar posición de captions** (center ↔ lower-third):
1. Editar la sección `## Captions` del MANIFEST (`Posición: center`)
2. Re-correr el render

**Atajo conversacional de re-render:**
```
/tutorial-render entregables/tutoriales/2026-06-18_mi-tutorial/
```

---

## Errores frecuentes

| Error | Acción |
|-------|--------|
| `render_tutorial.py: voz no encontrada` | Verificar que el archivo exista en `$DEST/USER/` con el nombre exacto indicado |
| Keyword no aparece en transcript | Editar el MANIFEST con una palabra que sí esté en el transcript (ver `captions.json`) |
| `bootstrap.sh` reporta Homebrew faltante | Instalar Homebrew con el comando oficial y reintentar |
| `npm install` falla en Remotion | Correr `sudo chown -R $(whoami) ~/.npm` y reintentar |
| Captions desfasados de la voz | Drift de Whisper — raro; borrar `captions.json` y re-render fuerza re-transcripción |
| Pantalla dura menos que su segmento | El motor hace loop/hold del último frame; ajustar duración en MANIFEST si se ve raro |
