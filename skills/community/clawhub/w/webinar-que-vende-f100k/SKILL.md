---
name: webinar-que-vende-f100k
description: "Use when someone asks to structure, write, optimize or audit a webinar, workshop, masterclass or live class that sells, or to turn it into slides. Arma el mapa de los 9 acuerdos minuto a minuto, valida el One Belief y el mecanismo, escribe las láminas una por una (texto en pantalla + lo que dices + nota) y entrega un HTML con todas las slides para presentar o copiar y pegar en Canva, Google Slides o Keynote. Entra por wizard de preguntas, por un brief + One Belief pegado, o por un webinar que ya existe. Triggers on \"arma mi webinar\", \"estructura mi workshop\", \"optimiza mi webinar\", \"audita mi masterclass\", \"hazme las slides de mi clase en vivo\", \"guion de mi webinar\", \"mi webinar no vende\", \"tengo mi brief y mi one belief\", \"clase de lanzamiento\"."
argument-hint: "[brief, archivo o \"wizard\"]"
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - No necesita herramientas externas: todo es texto + un HTML. Guarda la carpeta `webinar-<slug>/` en `entregables/webinars/`.
> - En Telegram el wizard va una pregunta por mensaje. Al terminar, manda `slides.html` como archivo y `guion.md` como texto o archivo.
> - No abras navegador para validar: valida el JSON del bloque `datos` con `python3 -c` o `node -e`.

---

# Webinar que vende — FÓRMULA 100K

Convierte una idea de clase en vivo (o un webinar que ya existe) en **un guion minuto a minuto y un deck lámina por lámina** construido con el método de los 9 acuerdos, y lo entrega en **un HTML** que sirve para presentar y para copiar cada lámina a la herramienta que la alumna use.

## Archivos de esta skill
- `references/metodo.md`: el método completo con el porqué de cada pieza (9 acuerdos, 10 factores, 4 vías, One Belief, cierre en 7 pasos, brecha, precio con crédito, errores). **Léelo entero antes del paso 3.**
- `references/estructuras.md`: las 3 estructuras minuto a minuto y **cuántas láminas lleva cada bloque**. Léelo en el paso 4.
- `references/wizard.md`: las preguntas del wizard, en orden, con qué hacer si responde «no sé». Léelo si entras por el modo A.
- `references/reglas-laminas.md`: cómo se escribe una lámina (texto en pantalla, guion hablado, nota, visual). Léelo en el paso 6.
- `assets/plantilla-slides.html`: el artifact final. Se copia y se rellena **solo** el bloque `<script id="datos">`.

## Reglas que no se rompen
1. **No inventes** testimonios, capturas, cifras, historias personales, garantías ni precios. Lo que falte va como `[por completar: qué falta]`: la plantilla lo pinta en rojo para que se vea.
2. **Tutea** y usa español neutro. Nada de voseo.
3. **Urgencia solo verdadera.** Si la alumna no tiene una razón real para actuar hoy, el acuerdo 9 se escribe con la urgencia honesta («el impulso se enfría») y nunca con un cupo o plazo inventado.
4. **Nichos clínicos** (salud mental, trastornos alimentarios, medicina): sin escasez, sin contadores, sin miedo a perder.
5. **La brecha:** la sesión entrega un resultado una vez; la oferta, el sistema que lo repite. Si una lámina resuelve de más, lo dices y propones moverla a «versión pro».
6. El **One Belief** se escribe con las mismas palabras exactas cada vez que aparece.

---

## Paso 0 · Detecta la entrada

Mira lo que te dieron (`$ARGUMENTS` y el mensaje):

| Si recibes… | Modo |
|---|---|
| Nada, o «wizard», o «no sé por dónde empezar» | **A · Wizard** |
| Un brief, un manual de negocio, un archivo de contexto (p. ej. `CONTEXTO_CONTENIDO.md`) y/o un One Belief | **B · Brief** |
| Láminas, un guion, un PDF, un link a un deck o la transcripción de un webinar que ya dio | **C · Optimizar** |

Si hay un `CONTEXTO_CONTENIDO.md` o un `CLAUDE.md` con su negocio en la carpeta de trabajo, léelo aunque no lo mencione: es modo B.

Dile en una línea qué modo usas y por qué. Si dudas entre dos, pregunta con `AskUserQuestion`.

## Paso 1 · Arma la ficha del webinar

La ficha es la única fuente de verdad del resto del trabajo. Campos:

```
oferta · público · formato (taller 90 / semanal 60 / lanzamiento) · duración · qué hacen en vivo
lo que se llevan hecho · precio de entrada · problema (en SUS palabras) · lo que ya intentaron
mecanismo · One Belief · solución (en qué es distinta) · analogías · historia propia real
casos reales (¿con captura?) · precio de la oferta y crédito · garantía · razón real de urgencia
objeciones (3) · bonos o regalos · fecha de cierre real (si hay)
```

- **Modo A:** sigue `references/wizard.md`, **una pregunta a la vez**. Usa `AskUserQuestion` cuando haya opciones; si no, pregunta en texto. Si responde «no sé», aplica lo que dice el wizard para esa pregunta (proponer 2-3 opciones y seguir), nunca te quedes trabada.
- **Modo B:** extrae del brief todo lo que puedas. Muestra la ficha como tabla con tres estados: ✅ lo tengo · 🟡 lo deduje (dile de dónde) · ❌ falta. Pregunta **solo** los ❌ que bloquean (mecanismo, One Belief si no vino, qué hacen en vivo, casos). El resto queda como `[por completar]`.
- **Modo C:** primero lee el webinar entero. Llena la ficha con lo que ya dice. Después corre el **marcador A1–A9** (paso 5) sobre lo que existe **antes** de proponer cambios, y muéstralo: por cada acuerdo, en qué lámina/minuto aparece hoy, con qué vías, y si está cerrado, débil o ausente. Recién después reestructuras.

## Paso 2 · Las dos compuertas

No se escriben láminas hasta que estas dos pasen. Son el 80 % del resultado.

**Compuerta del One Belief.** Revisa los 4 criterios (`references/metodo.md` § One Belief): corto · es una creencia sobre cómo funciona el mundo (no describe el producto) · si lo cree, comprar es la consecuencia lógica · se puede comprobar dentro de la sesión. Muestra ✅/❌ por criterio. Si falla alguno, propón **3 versiones** que sí pasen, cada una con el criterio que arregla, y que ella elija.

**Compuerta del mecanismo (acuerdo 3).** Pregúntate: ¿esto lo sabía ya su público? Si el mecanismo es «ser constante», «dar valor», «organizarse» o cualquier consejo genérico, **no pasa**. Propón 2-3 mecanismos con la forma «no es X (lo que cree), es Y (la razón que no conocía)», anclados en lo que ella ya dijo del problema. Si en el brief hay palabras literales de su público, úsalas.

## Paso 3 · Elige la estructura

Con la ficha, decide (y dile por qué en una línea):

- Gratis + 60 min → **clase semanal**.
- Gratis + 90 min → **masterclass de lanzamiento**.
- Pago bajo, o hacen algo con sus manos → **taller**. Si dura 60, taller compacto (ver `estructuras.md`).

Y anota qué acuerdos **se cierran solos** según lo que hacen en vivo:
- Hacen algo con sus manos → se cierran solos 5, 6 y 7.
- Solo miran → 5 y 6. Propón un momento de 5 min en que cada una haga una parte pequeña.
- Solo escuchan → ninguno. Propón convertir un bloque en práctica.

## Paso 4 · El mapa de acuerdos (guion minuto a minuto)

Lee `references/estructuras.md`. Entrega una tabla:

| Minuto | Bloque | Acuerdo(s) | Vías | Factor emocional | Lo que dices (frase literal) | Señal de cierre |
|---|---|---|---|---|---|---|

Reglas que aplicas mientras la llenas (el porqué está en `metodo.md`):
- A4 va en el gancho (00-08). A1 en el primer tercio. A3 antes del minuto 20 (taller) o del 25 (semanal).
- Cada acuerdo con **2 vías mínimo**; A3, A6, A7 y A8 con **3**. Nunca dos acuerdos seguidos con exactamente las mismas vías.
- Los **casos** se gastan en A6 y A8. Si sus casos son espectaculares o lejanos, pon al lado uno parecido a quien escucha, o una demostración.
- Elige **4-5 factores emocionales** y repítelos. Miedo a perder, una sola vez.
- One Belief: plantar (min 3) → abrir (con A3) → recordar (cuando ya tienen el resultado) → cobrar con giro («hoy no hiciste X, hiciste Y») → última lámina sola. **Mismas palabras.**
- Protege la celebración (A7): en el taller, mínimo 8 min. Incluye la **frase de rescate** para quien no terminó.
- Cierre en su orden: puente → stack → precio contra el costo de no hacerlo → garantía (y pides la acción) → objeciones → urgencia verdadera → identidad.

## Paso 5 · Auditoría (marcador A1–A9)

Antes de escribir láminas, audita el mapa. Muestra:

```
A1 ✅ min 09 · analogía + explicación
A2 🟡 min 13 · solo explicación → falta segunda vía
A3 ✅ …
…
Cierre: puente ✅ · stack ✅ · precio vs costo ✅ · garantía 🟡 [por completar] · …
One Belief: 4 apariciones, mismas palabras ✅
Faltan datos: historia propia real (A4), captura de un caso (A6), garantía
```

Arregla lo que dependa de ti. Lo que dependa de un dato que no tienes queda marcado y se lo listas al final. Pide el visto bueno del mapa **en una sola pregunta** antes del paso 6 (si está apurada y dice «sigue», sigue).

## Paso 6 · Las láminas, una por una

Lee `references/reglas-laminas.md`. Por cada lámina escribe:

- `n` · `bloque` · `min` · `acuerdo` (A1…A9, OB, C1…C7, o vacío)
- `titulo`: lo que se lee en grande. Máximo ~8 palabras.
- `pantalla`: el resto del texto visible, máximo ~20 palabras (o vacío).
- `dices`: lo que ella dice en voz alta, en su voz, en frases que se pueden leer en un teleprompter.
- `nota`: para ella: la señal de cierre que tiene que leer en el chat, o qué no hacer.
- `visual`: qué va en la lámina (captura real, dibujo, esquema, foto suya, nada). Nunca «captura inventada».

Cantidades: taller de 90 ≈ 32-40 láminas · semanal de 60 ≈ 20-26 · lanzamiento ≈ 40-50. Una idea por lámina.

## Paso 7 · El artifact

1. Crea la carpeta `webinar-<slug>/` en la carpeta de trabajo (slug = nombre corto del webinar, minúsculas y guiones).
2. Copia `assets/plantilla-slides.html` a `webinar-<slug>/slides.html`.
3. Reemplaza **solo** el contenido de `<script id="datos" type="application/json">…</script>` con un JSON válido:

```json
{
  "titulo": "Nombre del webinar",
  "oneBelief": "La frase exacta",
  "duracion": 90,
  "estructura": "Taller de 90 min",
  "colores": {"acento": "#E11D74", "fondo": "#0F172A"},
  "faltan": ["Historia propia real para A4", "Captura de un caso para A6"],
  "laminas": [
    {"n":1,"bloque":"Gancho","min":"00:00","acuerdo":"A4","titulo":"…","pantalla":"…","dices":"…","nota":"…","visual":"…"}
  ]
}
```

   - `colores` es opcional: si la alumna tiene colores de marca, úsalos; si no, borra la clave y queda el tema por defecto.
   - Escapa bien el JSON (comillas dobles dentro del texto → `\"`; si algún texto trae `</`, escríbelo `<\/` para no cerrar el `<script>`). Nada de comentarios dentro.
4. Escribe también `webinar-<slug>/guion.md` con la ficha, el mapa del paso 4, la auditoría del paso 5 y la lista de lo que falta.
5. Si puedes, abre `slides.html` en el navegador (`open` en Mac, `start` en Windows) y comprueba que carga, que se ven todas las láminas y que no hay errores en la consola. Si no puedes abrir un navegador, valida el JSON leyéndolo con el lenguaje que tengas disponible (`node -e`, `python3 -c`).

## Salida (lo que le dices al terminar)

```
Tu webinar está listo: webinar-<slug>/slides.html (N láminas) y guion.md.

Estructura: <cuál> · One Belief: «<frase>»
Se cierran solos: A5, A6, A7 · Los que escribimos: …

Antes de salir en vivo te falta:
- [lista de por completar, con en qué lámina va cada uno]

Cómo usar el archivo:
- Ábrelo con doble clic. Modo «Presentar»: flechas para avanzar, N para tus notas, F para pantalla completa.
- Modo «Copiar»: cada lámina tiene botones para copiar el título, el texto o tu guion. «Copiar todo» te da el esquema entero para pegarlo en Canva, Google Slides, Keynote o Gamma.
```

## Notas
- Si la alumna solo quiere **auditar** (modo C sin reescribir), para en el paso 5 y entrega el marcador + las 5 correcciones de mayor impacto, ordenadas.
- Si pide **solo el One Belief** o **solo el mecanismo**, corre únicamente la compuerta del paso 2.
- Si su oferta no está clara (no sabe qué vende, a quién ni qué problema resuelve), dilo: un webinar sin oferta no tiene qué cerrar. Proponle definir primero la oferta y ofrece seguir con lo mínimo (qué vende, a quién, por qué ahora).
- No generes imágenes con IA para testimonios ni capturas. Las láminas con `visual` de captura quedan con el marco vacío para que ella pegue la real.
- Si el webinar ya existe y ha funcionado, respeta lo que funciona: el marcador te dice qué tocar, no reescribas lo que ya cierra.
