---
name: reel-faceless-f100k
description: "Convierte un tema en un Reel 9:16 faceless (30-90 s) donde la usuaria GRABA la voz pero nunca sale en cámara. Escribe el guion con gancho, retención y cierre de venta, arma el teleprompter, recibe la nota de voz por Telegram, saca los tiempos (transcripción por API si hay llave, o estimados) y el Clip Director decide por gancho el visual de cada tramo (B-roll cinemático IA, card de dato, pixel-meme; mezcla obligatoria). Genera los clips con Higgsfield (con ✅ de créditos), renderiza las cards a PNG con Chromium y junta los clips en orden en un solo video mudo con ffmpeg concat. Entrega ese video + la voz + las cards + el plan para montar la voz y el texto en CapCut o Edits. Activar con 'hazme un reel faceless de X', 'video faceless sin mi cara', 'explainer faceless', 'convierte este tema en video sin grabarme en cámara', 'reel solo con mi voz'. NO para talking-head con su cara, VSL (broll-vsl-formula100k) ni carruseles."
argument-hint: "<tema | ruta-guion.md> [--duracion=30..90] [--estetica=cyberpunk|calido|minimalista]"
allowed-tools: "Bash, Read, Write, Edit, AskUserQuestion, mcp__higgsfield__generate_video, mcp__higgsfield__generate_image, mcp__higgsfield__job_status, mcp__higgsfield__media_upload, mcp__higgsfield__media_confirm, mcp__higgsfield__balance"
metadata: {"version": "1.0.0", "aspect_ratio": "9:16", "output": "REEL_FACELESS.mp4", "openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Onboarding (brew, HyperFrames, mlx-whisper) NO aplica: sáltalo.
> - La voz llega por Telegram como nota de voz o audio. Guárdala en la carpeta del reel como `voz.ogg`/`voz.mp3`. Nunca generes ni clones la voz.
> - Tiempos (Paso 3): si hay `GROQ_API_KEY` u `OPENAI_API_KEY`, transcribe con la API de Whisper pidiendo marcas de tiempo por palabra. Si no, reparte los tramos por el teleprompter a ≈2,5 palabras por segundo y marca el plan como «tiempos estimados».
> - Clip Director en este servidor: cada tramo lleva un clip `broll` de Higgsfield que forma la base continua. Usa tramos de segundos enteros entre 4 y 15 (el mínimo de Seedance 2.0 es 4 s) para que ningún clip haya que recortarlo. Las `card` se escriben como HTML de 1080×1920 y se renderizan a PNG con Chromium; los `pixel` salen con `generate_image`. Cards y pixel se entregan como PNG para poner encima en su tramo. La regla de mezcla se cuenta sumando cards y pixel.
> - Todos los clips con el MISMO modelo, resolución (720p por defecto), `aspect_ratio: "9:16"` y `generate_audio: false`, para que el concat funcione sin re-codificar. Costo total estimado (tramos × precio) → ✅ antes del primer lote; lotes de máximo 8.
> - Paso 5 recortado: solo junta los clips en orden con `ffmpeg -f concat -safe 0 -i lista.txt -c copy base.mp4`. Nada de escalar, overlays, colorkey ni mezclar audio. Entrega `base.mp4` (mudo) + la voz + los PNG + `plan.json` con los tiempos, y explícale cómo poner la voz y los PNG encima en CapCut o Edits.
> - Sin créditos de Higgsfield: entrega guion, teleprompter, `plan.json` con el prompt de cada tramo y las cards en PNG. Dilo en la primera línea.
> - Si `base.mp4` pesa más de 50 MB (límite de Telegram), avisa y manda los clips por link o a 720p.

---

# Reel Faceless F100K — Explainer 9:16 con voz del usuario, sin cámara

Convierte un tema en un Reel vertical faceless: El usuario **graba la voz** pero **nunca sale en
cámara**. El video se construye 100% con visuales generados por IA — B-roll cinemático, cards
kinéticas y pixel-memes — que el **Clip Director** elige por gancho y sincroniza sobre su voz.

El principio (igual que el "Higgsfield Explainer" pero con ADN F100K): escala el contenido de
El usuario sin depender de su cara. El diferencial no es generar (eso ya se domina) sino **dirigir**.

---

## Cuándo activar

- El usuario dice "hazme un reel faceless de X", "video sin mi cara", "explainer faceless",
  "convierte este tema en video sin grabarme", "reel solo con mi voz".
- Tiene un tema (o un guion ya escrito) y quiere el video terminado sin ponerse frente a cámara.

## NO activar para

- Talking-head con su cara → `motion-reels-f100k` (9:16) / `editor-video-formula100k`
- VSL o video largo con avatar → `broll-vsl-formula100k`
- Carruseles → `carrusel-render-formula100k`
- Stories fullscreen → `historias-a-imagenes-nanobanana`
- Clips de apoyo sobre un video de YouTube ya grabado → `editor-video-formula100k` (modo
  clips de apoyo, que usa este mismo Clip Director)

---

## Onboarding — Auto-install (NO aplica en este servidor: sáltalo y lee el bloque 🦞)

```bash
# 1. Node.js v22+
node --version 2>/dev/null | grep -qE "v2[2-9]|v[3-9][0-9]" || {
  echo "⚠ Node.js v22+ requerido. Instalando..."
  brew install node@22 && brew link node@22 --force
}

# 2. HyperFrames CLI + ecosistema
command -v hyperframes &>/dev/null || npm install -g hyperframes
node -e "require('@hyperframes/core')" 2>/dev/null || npm install @hyperframes/core
node -e "require('@hyperframes/engine')" 2>/dev/null || npm install @hyperframes/engine
node -e "require('@hyperframes/producer')" 2>/dev/null || npm install @hyperframes/producer
hyperframes doctor      # Chrome y FFmpeg deben aparecer con ✓

# 3. Sistema
command -v ffmpeg &>/dev/null || brew install ffmpeg
command -v uv &>/dev/null || brew install uv    # para mlx-whisper
```

**Verificar créditos Higgsfield antes de generar:**

```
mcp__higgsfield__balance()
```

Si el balance es 0 o insuficiente → activar **degradación** (ver `reference/clip-director.md`
§6): todos los `broll`/`pixel` caen a `card` (HyperFrames, local, gratis). Avisar al usuario.

---

## Pipeline (6 pasos)

### Paso 1 — Tema → guion + teleprompter

Definir `$DEST`:

```bash
SLUG="tema-en-kebab"        # derivar del tema
DEST="entregables/$(date +%F)_${SLUG}"
mkdir -p "$DEST/assets"
```

Escribir el guion siguiendo el ADN de `guionizacion-formula100k`:
- Estructura de las 33 (elegir según el tema), **gancho** verbal en los primeros 3 s.
- **Retención**: intriga, cliffhangers, ritmo.
- **Español neutro** (tú/tienes/aquí — nunca vos/tenés/acá).
- **Cierre que vende FÓRMULA 100K** (CTA suave a la comunidad).
- Longitud según `--duracion` (30–90 s ≈ 75–225 palabras a ritmo de reel).

Guardar:
- `$DEST/guion.md` — guion completo con marcas de estructura.
- `$DEST/teleprompter.txt` — SOLO lo que el usuario dirá, limpio, para leer de corrido.

Mostrar el guion y confirmar el gancho con el usuario antes de que grabe (el gancho carga el 80%
de la retención).

### Paso 2 — El usuario graba la voz

Pedirle que grabe leyendo `teleprompter.txt` y guarde el audio como `$DEST/voz.mp3` (o pasar
la ruta si ya lo grabó). Verificar:

```bash
ffprobe -v error -show_entries format=duration -of default=nokey=1:noprint_wrappers=1 "$DEST/voz.mp3"
```

> Nunca generar la voz con IA ni clon. El usuario graba — esa es la regla de esta skill.

### Paso 3 — Transcripción word-level (en este servidor: API o tiempos estimados, lee el bloque 🦞)

```bash
ffmpeg -i "$DEST/voz.mp3" -vn -acodec mp3 -ar 16000 -ac 1 -y /tmp/faceless_audio.mp3

uvx --from mlx-whisper mlx_whisper /tmp/faceless_audio.mp3 \
  --model mlx-community/whisper-large-v3-mlx \
  --language es --word-timestamps True \
  --output-format json --output-dir /tmp

python3 - << 'EOF'
import json
data = json.load(open('/tmp/faceless_audio.json'))
words = [{'text': w['word'].strip(), 'start': w['start'], 'end': w['end']}
         for seg in data['segments'] for w in seg.get('words', [])]
json.dump(words, open('DEST_PLACEHOLDER/transcript.json','w'), ensure_ascii=False, indent=2)
print(f"Transcripción: {len(words)} palabras")
EOF
```

(Sustituir `DEST_PLACEHOLDER` por `$DEST`.) Alternativa si `uvx` falla:
`npx hyperframes transcribe /tmp/faceless_audio.mp3 --model small --language es`.

### Paso 4 — Clip Director (modo `full`, formato `9:16`)

Seguir `reference/clip-director.md` al pie:

1. Segmentar `transcript.json` en bloques de 3-6 s.
2. **Clasificar** cada bloque por gancho → `visual_type` (`broll`/`card`/`pixel`), respetando
   la **regla de mezcla** (≥2 tipos distintos, ninguno >60%).
3. Mostrar el plan como tabla y confirmar con el usuario (o ajustar):

```
t=00:00–00:04  broll   "concepto: el error que todas cometen"   [cinemático]
t=00:04–00:08  card    "3 razones" (Chapter)
t=00:08–00:12  broll   "yo pasé de X a Y"                        [avatar]
t=00:12–00:15  pixel   remate cultura pop
...
```

4. **Generar los assets:**
   - `broll` → Higgsfield `generate_video` `aspect_ratio="9:16"`, lotes de ≤8, poll
     `job_status(sync:true)`, declinar presets, anti-NSFW. Descargar: `curl -L "<url>" -o "$DEST/assets/segNN.mp4"`.
   - `card` → HyperFrames full-frame 1080×1920 fondo `#FF00FF`, `hyperframes render --format mp4 -o "$DEST/assets/segNN.mp4"`.
   - `pixel` → `recursos-pixel-formula100k` o `generate_image` pixel-art; si no hay, degradar a `card`.
5. Escribir `$DEST/plan.json` con el contrato del Clip Director, llenando `asset_path` de cada
   segmento (ruta relativa a `$DEST/`, ej. `assets/seg0.mp4`).

**Texto kinético de énfasis (opcional pero recomendado):** generar overlays de palabras clave
con HyperFrames (chroma `#FF00FF`, reglas `motion-reels-f100k`) → renderizar a
`$DEST/overlays.mp4`. `compose_faceless.sh` los compone automáticamente si el archivo existe.
NO son subtítulos completos — solo palabras-fuerza.

### Paso 5 — Composición (recortada en este servidor: solo concat, lee el bloque 🦞)

```bash
bash "$(dirname "$0")/scripts/compose_faceless.sh" "$DEST"
```

Ensambla los assets por segmento a la línea de tiempo de la voz (escala/crop a 1080×1920,
loop+trim a la duración del segmento), superpone `overlays.mp4` con `colorkey=0xFF00FF` si
existe, y mezcla `voz.mp3` (+ `musica.mp3` a volumen bajo si existe). Salida:
`$DEST/REEL_FACELESS.mp4`.

### Paso 6 — Verificar y entregar

```bash
# manda el resultado por Telegram
```

Checklist:
- [ ] Duración del video ≈ duración de la voz (sin colas mudas).
- [ ] Mezcla de `visual_type` respeta la regla (≥2 tipos, ninguno >60%).
- [ ] Gancho visual fuerte en los primeros 3 s.
- [ ] Texto kinético son palabras-fuerza, NO subtítulos.
- [ ] La voz del usuario se oye clara sobre la música.
- [ ] Cierre vende F100K.

Mostrar ruta final + tabla del plan.

---

## Errores y fallbacks

| Error | Acción |
|-------|--------|
| `mcp__higgsfield__balance` = 0 | Degradar: `broll`/`pixel` → `card` (ver `reference/clip-director.md` §6) |
| `NSFW content detected` | Simplificar prompt (quitar oscuridad/intimidad), reintentar; si reincide, segmento → `card` |
| `concurrent job limit` | Nunca >8 jobs a la vez; esperar el lote |
| Higgsfield sugiere preset | Declinar con `declined_preset_id` |
| `uvx` no encontrado | `brew install uv` y reintentar; o `npx hyperframes transcribe` |
| Whisper alucina | Re-correr con `--temperature 0.2` o modelo `medium` |
| `hyperframes render` falla | `hyperframes lint` + `validate`; verificar `data-track-index` únicos y `window.__timelines` registrado |
| `--format webm` | Usar `--format mp4` — VP9 sale sin alpha real |
| Overlay no se limpia (residuo magenta) | `colorkey` (RGB) no `chromakey` (YCbCr); `0xFF00FF:0.3:0.1` |
| Video final negro tras overlay | Fuente y overlay al mismo fps; el script ya fuerza `fps=30,format=yuv420p` |
| Audio de voz muy ruidoso / no transcribe | Pedir regrabar el tramo; no inventar timestamps |

---

## Estructura de archivos generados

```
$DEST/                                  (FORMULA100K/RECURSOS VIDEOS/YYYY-MM-DD_slug/)
├── guion.md               ← guion completo con estructura
├── teleprompter.txt       ← solo lo que el usuario dice
├── voz.mp3                ← voz grabada por el usuario (input)
├── musica.mp3            ← (opcional) música de fondo
├── transcript.json        ← word-level normalizado
├── plan.json              ← Clip Director: segmentos + visual_type + asset_path
├── overlays.mp4          ← (opcional) texto kinético, chroma #FF00FF
├── assets/
│   ├── seg0.mp4           ← B-roll / card / pixel por segmento
│   ├── seg1.mp4
│   └── ...
└── REEL_FACELESS.mp4      ← OUTPUT FINAL (1080×1920, voz del usuario)
```

---

## Relación con otras skills

| Aspecto | reel-faceless-f100k | motion-reels-f100k | broll-vsl-formula100k |
|---------|--------------------|--------------------|-----------------------|
| Cara del usuario | ✗ Nunca (faceless) | ✅ Talking-head | ✅ 80% avatar |
| Video base | Ninguno (se genera todo) | Video grabado | Ninguno (solo clips) |
| Voz | Grabada por el usuario | Del video grabado | N/A (solo B-roll) |
| Salida | Reel 9:16 completo | Reel 9:16 + overlays | Catálogo de clips 16:9 |
| Motor de clips | **Clip Director** (compartido) | HyperFrames overlays | Higgsfield 80/20 |
