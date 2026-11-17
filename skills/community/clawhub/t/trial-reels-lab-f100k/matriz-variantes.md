# La matriz forzada de 4 celdas

## Por qué existe

Si las 4 variantes son sinónimos de la misma idea —"3 apps de IA", "las 3 apps que uso", "3 herramientas de IA"— el test no enseña nada. Se gastan 4 publicaciones para descubrir cuál sinónimo suena mejor, que es ruido.

Cada variante debe **ocupar una celda distinta de la matriz**. Así, gane quien gane, la corrida deja una lección transferible al resto del contenido.

**Regla dura: una celda por variante. Nunca dos variantes de la misma celda.**

---

## Las 4 celdas

### A — CLAIM DE TEXTO
*El carrier lo lleva el texto en pantalla.*

Promesa concreta + número, 8-12 palabras, desde el frame 0. Es el **default en nichos de dinero** (66% de los virales de esos nichos lo hacen así).

- Declarar, no preguntar
- Número visible como texto grande, no dicho de pasada
- Vender el resultado, no la función ("editas en 4 minutos", no "Claude puede editar")
- Nunca texto-etiqueta ("Lista de formatos", "Tips de IA")

> `Edité este reel en 4 minutos sin tocar CapCut`
> `3 cosas que hago antes de grabar y nadie hace`

### B — GANCHO VISUAL
*El carrier lo lleva la imagen. El texto es secundario o no existe.*

Un overlay real ocupa el primer segundo: referencia de cultura pop, logo intervenido con símbolo emocional, captura de pantalla, objeto en mano.

Esta es **la celda de apuesta**, no la de default: en nichos de dinero el visual suele rendir menos. Pero es la más infrautilizada y la que más puede romper el techo cuando funciona. El trial reel es exactamente el lugar donde probar esto sin arriesgar el feed.

- Logo **intervenido**, nunca limpio (💔 ⚠️ ✓ ✗ ✨)
- Máximo 2 emojis
- Composición vertical: capa arriba + cara abajo
- Si no hay nada físico que mostrar, **no inventar atrezzo** — mejor cambiar de celda que forzar un prop irrelevante

> logo de CapCut + 💔 · `Terminé con CapCut`
> captura de la notificación de IG con ✗ encima

### C — CONFLICTO / NEGACIÓN
*Abre rompiendo algo: una creencia, una práctica común, una expectativa.*

Es la celda que más comentarios genera. Verbo de ruptura al frente.

- "Nadie…", "Deja de…", "Borré…", "Terminé con…", "Estás…"
- Señalar al espectador ("te señalo") sube comentarios
- No confundir con clickbait: la ruptura tiene que sostenerse en el cuerpo del video

> `Deja de subir historias todos los días`
> `Nadie está viendo tus reels y no es el algoritmo`

### D — PRUEBA / RESULTADO
*Abre con la evidencia, no con la promesa.*

Métrica en pantalla, captura de analytics, antes-después, resultado de un cliente. En nichos de dinero esta celda es la que más rinde cuando hay prueba real que mostrar.

- La cifra tiene que ser **real y verificable** — nunca inventar una métrica para el gancho
- Si no hay prueba real disponible, esta celda se reemplaza por una segunda variante de A con un ángulo claramente distinto, y **se anota el motivo** en `variantes.json`

> captura de tu mejor métrica real · `Este reel hizo [TU CIFRA REAL] vistas y duró 8 segundos`
> antes/después de la misma toma

---

## Qué NO debe cambiar entre variantes

Solo cambian **los primeros 2-3 segundos visuales**. Todo lo demás se queda idéntico:

- El cuerpo del video y el CTA — mismo archivo
- La caption — la misma en las 4, es seguro y no cuenta como duplicado
- El audio del cuerpo
- La música, si hay

Si cambian dos cosas a la vez, el resultado no dice cuál fue la que movió la aguja.

---

## Esquema de `variantes.json`

```json
{
  "proyecto": "2026-07-22_reel_edicion_4min",
  "modo": "video",
  "nicho": "negocios",
  "base": "/ruta/absoluta/al/video.mov",
  "hook_end": 3.2,
  "duracion_overlay": 3.2,
  "resolucion": [1080, 1920],
  "hairline_y": 780,
  "notas_frame": "Cabeza centrada, hairline ~780px. Zona libre inferior desde y=1200. Objeto (celular) en mano derecha desde 1.4s. Cámara fija.",
  "caption": "Texto de la caption, idéntico en las 4. Comenta EDITA y te mando la guía.",
  "variantes": [
    {
      "id": "A",
      "celda": "claim",
      "texto": "Edité este reel en 4 minutos\nsin tocar CapCut",
      "tratamiento": "claim",
      "posicion": "superior",
      "acento": "4 minutos",
      "mutacion": "none",
      "por_que": "Default del nicho: carrier textual con número, declarando.",
      "entrada": 0.0,
      "salida": 3.2
    },
    {
      "id": "B",
      "celda": "visual",
      "texto": "Terminé con CapCut",
      "tratamiento": "visual",
      "posicion": "superior",
      "asset": "assets/logo_capcut_roto.png",
      "emoji": "💔",
      "mutacion": "zoom",
      "por_que": "Apuesta: el carrier visual es la celda menos probada. Se prueba sin costo.",
      "entrada": 0.0,
      "salida": 3.2
    },
    {
      "id": "C",
      "celda": "conflicto",
      "texto": "Deja de editar tus reels\ncomo lo hacías en 2024",
      "tratamiento": "conflicto",
      "posicion": "superior",
      "acento": "Deja de",
      "mutacion": "speed",
      "por_que": "Celda de comentarios: verbo de ruptura al frente.",
      "entrada": 0.0,
      "salida": 3.2
    },
    {
      "id": "D",
      "celda": "prueba",
      "texto": "[TU CIFRA REAL] vistas",
      "subtexto": "y lo edité en 4 minutos",
      "tratamiento": "prueba",
      "posicion": "inferior",
      "asset": "assets/captura_metrica.png",
      "mutacion": "none",
      "por_que": "Métrica real de la cuenta, verificable.",
      "entrada": 0.0,
      "salida": 3.2
    }
  ]
}
```

### Campos

| Campo | Obligatorio | Notas |
|---|---|---|
| `modo` | sí | `"video"` o `"pack"` |
| `base` | solo modo video | ruta absoluta al `.mov`/`.mp4` |
| `hook_end` | solo modo video | lo calcula `analizar_base.py` |
| `duracion_overlay` | sí | en modo pack se fija a mano (por defecto 3.0) |
| `hairline_y` | recomendado | píxel del nacimiento del cabello, mirando el frame. Los overlays superiores apoyan su borde inferior ahí |
| `celda` | sí | `claim` · `visual` · `conflicto` · `prueba`. Las 4 distintas |
| `tratamiento` | sí | qué layout dibuja `build_overlays.py`. Coincide con `celda` salvo excepción justificada |
| `posicion` | sí | `superior` o `inferior`. **Nunca `centro`** |
| `acento` | no | fragmento del texto que va resaltado |
| `asset` | solo celdas visual/prueba | ruta relativa a `TRIAL_REELS/` |
| `mutacion` | sí | `none` · `zoom` (1.02×) · `speed` (1.02×). Solo hace falta si se republica el mismo archivo a trials |
| `por_que` | sí | una línea. Va a la hoja de montaje y al plan |

---

## Reglas de posición (validadas en producción)

- **Superior:** el **borde inferior** del overlay queda al ras del cabello. En un 9:16 del usuario el hairline está ~40-45% desde arriba. Flotando arriba en el vacío se ve desconectado — es un error que ya se corrigió una vez.
- **Inferior:** a la altura del pecho, `bottom: 520px` en 1080×1920. Nunca subir de la barbilla.
- **Centro: prohibido.** Tapa la cara.
- Dos overlays consecutivos no se solapan: `entrada_B > entrada_A + duración_A`.
- Los assets con transparencia (infografías, cutouts) **nunca van fullscreen**: los huecos dejan ver la cara a través y el resultado es caótico.
