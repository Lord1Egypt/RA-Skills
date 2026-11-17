---
name: radar-contenido-f100k
description: "Radar de contenido de FÓRMULA 100K: monta y corre un sistema que vigila Instagram y te avisa qué FORMATOS están despegando. Cosecha con Apify (búsquedas cortas convertidas a hashtags) y con los Reels guardados que la usuaria reenvía por Telegram; filtra cuentas pequeñas cuyas vistas multiplican sus seguidores; mira cada reel (capturas o análisis de video de Higgsfield) antes de anotarlo; describe la mecánica (no el tema) con anatomía de 4-6 pasos; y la anota en un registro de recurrencia. Una mecánica cruza el umbral cuando aparece en 2+ nichos sin relación. Usar cuando se diga: 'monta mi radar', 'corre mi radar de contenido', 'radar de formatos', 'qué formatos están despegando', 'busca storytelling en Instagram', 'agrega este reel al radar [link]', 'qué cruzó el umbral'. Nunca usa una sesión logueada. NO escribe guiones (guionizacion-formula100k), NO audita una cuenta entera (analizador-perfiles-formula100k), NO caza temas del día (radar-virales-f100k)."
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - **No hay Explorar ni guardados logueados en este servidor**: FASE 2 con Claude in Chrome, `scripts/cosecha.js` y `scripts/mirar.sh` no vienen en este paquete. El PASO 0 de instalación tampoco aplica: aquí solo comprueba `APIFY_TOKEN` y, si lo vas a usar, el plugin de Higgsfield.
> - Cosecha: Apify con las búsquedas cortas convertidas a hashtags (`apify~instagram-scraper`, `resultsType: "posts"`) y, para seguidores, `apify~instagram-profile-scraper` sobre los autores con +100K vistas. Calcula el ratio vistas ÷ seguidores igual que la skill. Canal = `apify:<hashtag>`. Di el costo antes y espera ✅.
> - Guardados: la usuaria te reenvía por Telegram los links de los Reels que guardó; entran por el modo AGREGAR 1 con `fuente: "guardados"`.
> - FASE 4 (compuerta visual, sigue siendo bloqueante): aquí no se bajan videos ni se sacan fotogramas. Para mirar un Reel usa, en este orden: capturas que mande la usuaria (inicio, medio y final); o el análisis por escenas de Higgsfield (`media_import_url` con el `videoUrl` de Apify → `video_analysis_create`, costo → ✅). La transcripción sale del actor de Apify (`includeTranscript`). Lo que no se pudo mirar **no entra** al registro.
> - Carpeta del radar: `informes/radar-contenido/` (`config.json`, `registro.json`, `corridas/`, `reportes/`). El reporte se manda por Telegram.
> - Con Apify puede ir en una automatización de OpenClaw (por ejemplo lunes y jueves) que entrega el reporte por Telegram; muestra la hora y el costo por corrida y espera ✅ antes de crearla.

---

# Radar de contenido · FÓRMULA 100K

Metodología FÓRMULA 100K. Un radar **no busca ideas**: vigila una señal en el tiempo y avisa cuando
**se repite**. Esta skill vigila **formatos**, es decir, cómo se arma un video, independiente del tema.

> **Formato ≠ tema.** «Vigilia con la hora en pantalla contra un rival» es un formato: sirve para una
> entrenadora y para una contadora. «Un estudiante en la biblioteca» es un tema. Se cataloga el esqueleto.

## Reglas de oro (no negociables)

1. **No inventar.** Cada mecánica sale de fotogramas observados. Si la corrida no encuentra nada real, no se anota nada. Mejor 0 que datos fabricados.
2. **El caption no es prueba.** Nada entra al registro sin que el video se haya mirado.
3. **La recurrencia manda.** Una mecánica cruza el umbral cuando aparece en **2 o más nichos distintos, de cuentas distintas**. Lo visto una vez espera.
4. **Solo leer.** Desde la sesión del usuario no se da like, no se guarda, no se comenta ni se sigue a nadie. Los videos se bajan para analizarlos, nunca para republicarlos.
5. **Pregunta, no supongas.** Handle, nicho y carpeta los da el usuario. Si una carpeta no existe, pregunta antes de crearla.

---

## PASO 0 · Comprobar la instalación (versión de escritorio: en este servidor solo comprueba `APIFY_TOKEN` y el plugin de Higgsfield)

Verifica en este orden y **para en el primer fallo**, explicando cómo arreglarlo:

| Qué | Cómo se comprueba | Si falta |
|---|---|---|
| Claude in Chrome | Las herramientas `mcp__claude-in-chrome__*` existen y `tabs_context_mcp` responde | Instalar la extensión «Claude» de la Chrome Web Store (v1.0.36+), entrar a Claude Code con `/login` (plan Pro, Max, Team o Enterprise), arrancar con `claude --chrome` o correr `/chrome` → «Enabled by default». No funciona en WSL. |
| Instagram abierto | En una pestaña nueva de instagram.com el texto NO trae «Regístrate» ni «Entrar» | El usuario inicia sesión en ese Chrome. Nunca escribas contraseñas. |
| yt-dlp | `yt-dlp --version` | Mac: `brew install yt-dlp` · Windows: `winget install yt-dlp` · o `pip install yt-dlp` |
| ffmpeg | `ffmpeg -version` | Mac: `brew install ffmpeg` · Windows: `winget install ffmpeg` |
| Python 3 + Pillow | `python3 -c "import PIL"` | `pip install pillow` |
| Whisper (opcional) | `whisper --help` | `pip install openai-whisper`. Sin él se trabaja solo con fotogramas |
| Apify (opcional) | Herramientas `mcp__apify__*` | Solo para cazar en perfiles sin abrir el navegador: `claude mcp add --transport http apify https://mcp.apify.com` (inicia sesión en Apify por el navegador; consume créditos de Apify) |

## PASO 1 · Configuración (primera vez)

Pregunta y guarda en `<carpeta>/config.json`:

- **Carpeta del radar.** Usa `informes/radar-contenido/`.
- **Handle del usuario** (`@tuhandle`), para leer sus guardados.
- **Su nicho**, en pocas palabras. Sirve para medir cuánto de lo cosechado cae en su propia burbuja.
- **Búsquedas cortas**: 6 a 9 frases de **2-3 palabras** según el tipo de mecánica que quiera vigilar. Para storytelling: «storytime», «mi historia», «te cuento», «historia real», «me pasó», «lo que viví», «mi experiencia». Una frase larga devuelve 0 sin avisar.
- **Filtro**: `minVistas` 100000 · `maxSeguidores` 1000000 · `minRatio` 20. Vistas ÷ seguidores es lo que prueba que el formato hizo el trabajo y no la audiencia.
- **Catálogo propio** (opcional): la lista de formatos que ya conoce, para no anotar como nuevo lo que ya tiene.

Crea `<carpeta>/registro.json` con la forma de `references/registro-ejemplo.json` si no existe.

---

## MODOS

| El usuario dice | Qué haces |
|---|---|
| «corre mi radar» · «baja por explorar» | **CORRIDA**: fases 2 → 6 |
| «qué cruzó el umbral» · «revisa el radar» | **REVISIÓN**: solo fase 6 sobre el registro |
| «agrega este reel al radar [link]» | **AGREGAR 1**: fases 4 → 5 con ese video |

## FASE 2 · Cosecha (versión de escritorio con Claude in Chrome: en este servidor NO se usa; cosecha con Apify como dice el bloque de arriba)

1. `tabs_context_mcp` y `tabs_create_mcp`; navega a `https://www.instagram.com/`.
2. Lee `scripts/cosecha.js` y pégalo entero con `javascript_tool`. Define `window.RX` y guarda todo en `localStorage`.
3. Llama, **una llamada por línea**:
   - `await RX.explorar(3)` → Explorar del usuario
   - `await RX.explorar(3, true)` → la variante no personalizada (se etiqueta aparte)
   - `await RX.buscar([...])` → **máximo 3 frases por llamada**
   - `await RX.seguidores(14)` → repetir hasta que devuelva `pedidos: 0`. Si aparece un 429, para y sigue más tarde.
   - `RX.candidatos(filtro)` → los que pasan el filtro, ordenados por ratio
4. **Guardados**: navega a `https://www.instagram.com/<tuhandle>/saved/all-posts/`, espera 4 s y extrae los shortcodes de `a[href*="/reel/"]`. Van directo a la fase 4 con `fuente: "guardados"`, sin filtro de ratio: el usuario ya los validó con su ojo.
5. Escribe el resultado en `<carpeta>/corridas/<AAAA-MM-DD>/cosecha.json`.

**Trampas medidas:**
- Las vistas **no están en el DOM**, pero la API que usa la web sí trae `play_count`. Contrasta 1 perfil con una captura de `/<usuario>/reels/`.
- La pestaña que usa Claude suele estar **oculta** y Chrome congela los temporizadores: nada de bucles con esperas. `cosecha.js` ya trabaja en tandas.
- `navigate` recarga la página y borra `window.*`. Después de navegar, vuelve a pegar `cosecha.js`: los datos siguen en `localStorage`.
- Una llamada de más de 45 s se corta.
- Si una tanda que antes daba resultados devuelve ceros, la sesión de Instagram se cayó: pide al usuario que vuelva a entrar.

## FASE 3 · Preselección

- Toma hasta **30** candidatos por ratio. Con un ratio bajo, Explorar lo deja pasar casi todo, porque solo trae virales.
- El caption sirve para **ordenar**, nunca para aceptar. Si dice «Comenta PALABRA» o «Escribe X y te lo mando», el engagement es del cebo: baja su prioridad.
- Escribe los shortcodes, uno por línea, en `<carpeta>/corridas/<fecha>/lista.txt`.

## FASE 4 · Compuerta visual (bloqueante; en este servidor no se corre `mirar.sh`: mira con capturas o con el análisis de video de Higgsfield)

```bash
bash scripts/mirar.sh <carpeta>/corridas/<fecha>/videos <carpeta>/corridas/<fecha>/lista.txt
```

Baja cada reel, arma una hoja de 16 fotogramas, agrupa las hojas en `lote1.jpg`, `lote2.jpg`… y transcribe si hay Whisper.
**Mira los lotes** (léelos como imagen) y cruza con la transcripción. **Tres salidas:**

- **Demuestra una mecánica** → entra.
- **No la demuestra** → descarte con motivo, aunque tenga millones.
- **No se pudo mirar** → no entra, y se reporta.

Descartes típicos: talking head plano con subtítulos (buena historia, nada que copiar del montaje); una cuenta que **enseña** un formato no es un ejemplo **del** formato. Whisper inventa palabras sobre música: si no hay voz, mandan los fotogramas.
Presupuesta que se cae 1 de cada 2.

## FASE 5 · Registro de recurrencia

Por cada video que entró, destila **sin el tema**:

- `nombre`, y una `descripcion` de 2-4 frases que diga cómo se arma
- `anatomia`: **4 a 6 pasos** en imperativo, solo los que se VEN en los fotogramas
- `proposito`: `viralizar` | `nutrir` | `vender`
- `tipo`: `montaje` (cómo se compone el cuadro) o `titular` (una plantilla de frase que viaja sobre montajes distintos, como «10/10 [categoría]»). Un titular se anota y se reporta aparte: no tiene anatomía de montaje.

Luego, en este orden:

1. **¿Ya está en el catálogo propio?** Compara por mecánica, no por nombre. Si está → `estado: "descartado"` con `duplica`. Igual se anota, para no evaluarlo cada semana.
2. **¿Ya está en el registro?** Si es la misma mecánica aunque cambien tema y nicho → **suma el avistamiento**, no crees una entrada nueva.
3. **Si es nueva** → entrada con `estado: "candidato"`.

**Guardias:**
- Un shortcode va a **una sola** mecánica.
- Si la cuenta ya está en los avistamientos de esa mecánica, **no suma nicho**: es el creador repitiendo su formato.
- Cada avistamiento lleva `shortcode, cuenta, nicho, vistas, seguidores, ratio, fuente, canal, fecha`.

## FASE 6 · Umbral y reporte

Una mecánica **cruza** cuando cumple TODO:
- `tipo: "montaje"` · `2+ nichos` de cuentas distintas · anatomía de 4-6 pasos y propósito.
- **Recomendado:** el 2º nicho viene de una **fuente distinta** a la del 1º. Dos veces en el mismo feed puede ser el algoritmo repitiéndose.
- Antes de declararlo, **vuelve a mirar cada avistamiento** contra la anatomía. Un conteo heredado puede traer avistamientos mal asignados. El ejemplo que se enseña es el que cumple TODOS los pasos, no el más viral.

Al cruzar: `estado: "publicado"`. Escribe `<carpeta>/reportes/<fecha>.md`:

```
📡 Radar de contenido — <fecha>
Embudo: <cosechados> → <pasan filtro> → <mirados> → <entraron>
Nuevas mecánicas: <lista con cuenta, ratio y 1 frase>
Avistamientos sumados: <lista>
✅ Cruzaron el umbral: <mecánica · nichos · ejemplo que cumple todos los pasos>
⏳ Esperando 2º nicho: <lista>
📰 Titulares detectados: <lista>
🫧 Burbuja por fuente: <% de lo anotado que cae en el nicho del usuario, por fuente>
🗑 Descartes: <n por motivo>
```

Si una fuente pasa del 40% de burbuja, dilo y propone sumar búsquedas de otros rubros la próxima corrida.
Para convertir una mecánica que cruzó en un guion, ofrece `adaptador-formatos-f100k` o `guionizacion-formula100k`, pasándoles la anatomía.

## Ritmo recomendado

- **Corrida**: 1 o 2 veces por semana. Con Apify puede ir en una automatización, con el costo aprobado.
- **Revisión**: una vez por semana, sobre el registro, sin navegador.
- Separar leer de promover evita declarar tendencia lo que se vio una sola vez.
