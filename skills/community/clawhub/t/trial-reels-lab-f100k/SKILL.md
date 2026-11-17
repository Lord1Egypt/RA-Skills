---
name: trial-reels-lab-f100k
description: "Convierte UN video (o UN guion) en 4 variantes de gancho A/B/C/D para publicar como TRIAL REELS de Instagram y descubrir con datos cuál gancho gana antes de tocar el grid. Usa la matriz forzada de 4 celdas (claim de texto / gancho visual / conflicto / prueba) para que el test enseñe algo, con el criterio de 300 ganchos virales observados y los patrones de tu cuenta si existen. Entrega los 4 overlays como PNG transparentes 1080×1920 + hoja de montaje con texto, posición y tiempos para ponerlos en tu editor, y el plan de publicación (5/día, 5 min entre subidas, regla de 48h, regla del 25%, Play A vs Play B, reciclaje a 60 días) con avisos por Telegram si los apruebas. En este agente no compone el video ni publica. Activar con: 'trial reels', 'testea este gancho', 'hazme 4 variantes de gancho', 'variantes ABCD de este reel', 'overlays de gancho para el editor', 'prueba este video antes de subirlo al grid'."
allowed-tools: "Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion"
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - **MODO VIDEO no corre aquí** (`analizar_base.py`, `render_variantes.py`, Whisper, `hyperframes render`, ffmpeg): no hay `VARIANTE_[A-D].mp4`. Si la usuaria manda un video, trabaja en MODO PACK y dile que monte cada overlay en su editor.
> - En vez del Paso 1-2: pídele por Telegram 1 captura del primer segundo del video (para el hairline, objeto en mano, zonas libres) y hasta qué segundo dura el gancho hablado (o el `.srt`). Si no hay video, el `hook_end` es 3.0 s.
> - Capa 1 del criterio: lee `cerebro/memoria/patterns_ig_<handle>.md` si existe (lo escribe `patron-ig-f100k`). Si no existe, dilo y sigue con la Capa 2. Nunca inventes patrones ni cifras.
> - Paso 5-6: `build_overlays.py` sí corre (solo Python). Luego renderiza cada `comp_[A-D]/index.html` a PNG 1080×1920 con Chromium headless, fondo transparente, con la animación adelantada (`window.__timelines['a']`.seek(1.0) o `.progress(1)`). Escribe tú `HOJA_MONTAJE.md` con texto, posición en píxeles, entrada/salida y el `por_que` de cada variante.
> - Celda B (visual) o D (prueba): el asset visual se genera con el plugin de Higgsfield (costo → ✅) o es la captura real que manda la usuaria. La cifra de la celda D tiene que ser suya y verificable.
> - Mutaciones (zoom/speed 1.02×): no se procesan aquí; van anotadas en la hoja para que las aplique en su editor.
> - Paso 7: corre `plan_publicacion.py` **sin** `--recordatorios` (no hay Apple Reminders). Los avisos de 48 h y del 25% se crean como automatización de OpenClaw que escribe por Telegram, solo con ✅. Las métricas para decidir el ganador llegan por Composio (IG profesional) o capturas; tú no publicas nada.

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

# Trial Reels Lab F100K

Instagram reparte los *trial reels* **solo a no-seguidores**. Grid y trial reels son sistemas separados: no hay penalización por contenido duplicado entre uno y otro. Eso convierte el gancho —la variable que más pesa y la que hoy se apuesta a ciegas— en algo que se puede **medir gratis antes de arriesgar el feed**.

Esta skill toma UN material y saca **4 variantes que difieren solo en los primeros 2-3 segundos visuales**, listas para publicar y comparar.

## Cuándo activar

- "hazme las variantes de gancho de este video" / "ABCD este reel"
- "quiero testear este gancho antes de subirlo"
- "genera los overlays de gancho para que el editor los monte"
- Cuando el usuario pasa un `.mov` grabado o un guion y menciona trial reels / testear / variantes

## NO activar para

- Escribir el guion desde cero → `guionizacion-formula100k`
- Editar el video completo (cortes, silencios, b-roll) → `editor-video-formula100k`
- Motion graphics a lo largo de TODO el reel → `motion-reels-f100k`
- Solo evaluar un gancho ya escrito → `evaluador-ganchos-formula100k`
- Anuncios pagados → `guionizacion-ads-formula100k`

## Los dos modos

| | MODO VIDEO | MODO PACK |
|---|---|---|
| **Entrada** | `.mov` / `.mp4` ya grabado | guion en texto (+ opcional: un frame de referencia) |
| **Salida** | 4 × `VARIANTE_[A-D].mp4` listos para subir | 4 × `overlay_[A-D].mov` con alfa + `HOJA_MONTAJE.md` |
| **Para quién** | el usuario sube directo | el editor los suelta encima mientras edita |
| **Se detecta por** | la ruta apunta a un archivo de video | no hay video, solo texto |

Si no queda claro cuál quiere, preguntar con `AskUserQuestion`. **Nunca asumir.**

---

## Onboarding (correr siempre al inicio)

```bash
command -v ffmpeg &>/dev/null || brew install ffmpeg
command -v hyperframes &>/dev/null || npm install -g hyperframes
hyperframes --version   # 0.7.x+

# Ubicar esta skill: cambia si se instaló suelta o vía el plugin F100K.
# Se usa find y NO globs: en zsh (shell por defecto de macOS) un patrón sin
# coincidencias aborta el comando y SKILL_DIR quedaría vacío.
SKILL_DIR=$(find skills -maxdepth 2 -type d -name trial-reels-lab-f100k 2>/dev/null | head -1)
echo "$SKILL_DIR"   # si sale vacío, la skill no está instalada donde se espera
```

En todos los comandos de abajo, `$SKILL_DIR` es esa ruta. Whisper solo hace falta en MODO VIDEO; el script lo resuelve solo vía `uvx mlx-whisper`.

---

## Flujo — MODO VIDEO

### Paso 1 · Analizar la base (en OpenClaw NO corre: mira el bloque 🦞 de arriba)

```bash
python3 "$SKILL_DIR"/scripts/analizar_base.py "<ruta/al/video.mov>"
```

Escribe `<carpeta_del_video>/TRIAL_REELS/analisis.json` con: duración, fps, resolución, transcript palabra por palabra, **`hook_end`** (dónde termina el gancho hablado) y 4 frames extraídos (`frame_00.png` … `frame_20.png`).

### Paso 2 · Mirar los frames

Leer los 4 PNG con la herramienta `Read`. **Obligatorio, no opcional.** Hay que ver de verdad:

- dónde está la cabeza y dónde queda el **hairline** (define el tope de los overlays superiores)
- si hay objeto en mano, si el cuerpo entra al cuadro, si la cámara está fija
- qué zonas del frame están vacías (ahí van los overlays)
- si ya hay texto quemado en el video (si lo hay, el overlay tiene que convivir o taparlo por completo)

Anotar esas observaciones: alimentan el Paso 4.

### Paso 3 · Cargar el criterio

Leer **`criterios-gancho.md`** de esta skill. Ahí está de dónde sale "lo que funciona" y —más importante— la **regla de honestidad** sobre qué números se pueden citar y cuáles están prohibidos.

### Paso 4 · Escribir las 4 variantes

Leer **`matriz-variantes.md`** y llenar la matriz forzada. Cada variante ocupa una celda distinta; **no se permiten dos variantes de la misma celda** — si las 4 son sinónimos, el test no enseña nada y la corrida fue en vano.

Escribir `TRIAL_REELS/variantes.json` con el esquema documentado en `matriz-variantes.md`.

### Paso 5 · Construir los overlays

```bash
python3 "$SKILL_DIR"/scripts/build_overlays.py "<carpeta>/TRIAL_REELS"
```

Genera una composición HyperFrames por variante en `TRIAL_REELS/comp_[A-D]/index.html`, con el pack tipográfico F100K copiado **dentro** de cada carpeta (Chrome bloquea `file://` absoluto).

**Checkpoint visual:** previsualizar antes de gastar render.

```bash
hyperframes preview "<carpeta>/TRIAL_REELS/comp_A" --frame 1.0
```

### Paso 6 · Renderizar y componer (en OpenClaw NO corre: mira el bloque 🦞 de arriba)

```bash
python3 "$SKILL_DIR"/scripts/render_variantes.py "<carpeta>/TRIAL_REELS" --modo video
```

Renderiza cada composición a `.mov` ProRes 4444 con **alfa real** y la compone sobre el video base con `overlay` directo. Salida: `VARIANTE_A.mp4` … `VARIANTE_D.mp4`.

### Paso 7 · Plan de publicación

```bash
python3 "$SKILL_DIR"/scripts/plan_publicacion.py "<carpeta>/TRIAL_REELS" --recordatorios
```

Escribe `PLAN_PUBLICACION.md` y crea los recordatorios reales en Apple Reminders (chequeo de 48h y control diario del 25%). Sin `--recordatorios` solo escribe el archivo.

---

## Flujo — MODO PACK

Igual que arriba pero **saltando los pasos 1 y 2** (no hay video que analizar) y con el paso 6 en modo pack:

1. Leer el guion. Identificar el gancho hablado (la primera frase, normalmente 2-4s).
2. Pasos 3 y 4 idénticos: criterio + matriz forzada.
3. En `variantes.json`, el campo `"base"` va en `null` y hay que fijar `"duracion_overlay"` a mano (por defecto 3.0s).
4. `build_overlays.py` igual.
5. Render en modo pack:

```bash
python3 "$SKILL_DIR"/scripts/render_variantes.py "<carpeta>/TRIAL_REELS" --modo pack
```

Produce `overlay_A.mov` … `overlay_D.mov` (ProRes 4444, alfa real, 1080×1920) y **`HOJA_MONTAJE.md`**: para cada variante, el texto exacto, el tratamiento, la posición en píxeles, el tiempo de entrada/salida y la nota de por qué esa variante existe. Eso es lo que recibe el editor.

6. Paso 7 igual.

---

## Reglas duras que la skill impone

Están detalladas en `reglas-publicacion.md`. Las que nunca se negocian:

- **Máximo 5 trial reels al día.** Más que eso arriesga shadowban.
- **5 minutos entre publicación y publicación** de las variantes de una misma tanda.
- **La misma caption en las 4 está bien** y no cuenta como duplicado. Lo único que debe cambiar son los primeros 2-3 segundos visuales.
- **Nunca subir el mismo archivo dos veces a trials** sin una mutación técnica (zoom 1.02× o speed 1.02×). Entre grid y trials sí se puede, son sistemas separados.
- **Regla de 48h y regla del 25%** para decidir cuándo empujar el ganador al grid — la skill las calcula y las agenda, pero la decisión de publicar es del usuario.

## Lo que esta skill NO hace

No publica en Instagram, no descarga métricas, no reescribe el cuerpo del video y no lleva registro de aprendizaje entre rondas. Si en el futuro se quiere el tracker (qué celda de la matriz gana más seguido en esta cuenta), es una fase 2 que necesita 3-4 rondas ya corridas para valer algo.

## Archivos de esta skill

| Archivo | Para qué |
|---|---|
| `criterios-gancho.md` | de dónde sale el criterio + regla de honestidad de datos |
| `matriz-variantes.md` | las 4 celdas obligatorias, plantillas y el esquema de `variantes.json` |
| `reglas-publicacion.md` | los límites de plataforma y las reglas de 48h / 25% / Play A vs B / 60 días |
| `scripts/analizar_base.py` | transcribe, detecta `hook_end`, extrae frames |
| `scripts/build_overlays.py` | arma las 4 composiciones HyperFrames |
| `scripts/render_variantes.py` | render alfa + composición ffmpeg (o pack) |
| `scripts/plan_publicacion.py` | cronograma + recordatorios |
| `fonts/` | pack tipográfico F100K (woff2 locales) |
