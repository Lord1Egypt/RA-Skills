# Clips de apoyo: compuerta, prompt y generación

---

## 1. La compuerta visual

**Un beat no recibe un clip por ser importante. Lo recibe por ser imposible de filmar.**

Esta es la regla que separa esta skill de "meterle animaciones a un video". Un clip que
ilustra algo que tu cámara ya muestra no suma: resta, porque saca a la persona de tu cara
justo cuando estabas conectando.

Un beat se gana un clip **solo si cumple al menos uno**:

| Criterio | Ejemplo del método |
|---|---|
| **Pasado / recuerdo** | "hace tres años, sentada en esa mesa" — no existe ese metraje |
| **Interior o invisible** | lo que pasa dentro del cuerpo, dentro del sistema, dentro de su cabeza |
| **Escala imposible** | "de esto dependen 4.000 personas" |
| **Metáfora** | el villano, la trampa, el muro, la corriente que te arrastra |
| **Es EL giro** | el momento del vuelco se gana un clip aunque no cumpla los otros |

**No se ganan clip:** tu opinión, el CTA, la transición, la definición de un término, la
lista de tres cosas, y cualquier beat donde tu cara diciendo eso ya es suficiente.

### Techos duros

- **Máximo 5 clips** por reel de 45-90s. Con más, deja de ser tu historia y pasa a ser un
  video animado con una narradora encima.
- **Máximo 6s cada uno.** Un clip de apoyo que dura más se convierte en el video.
- **El giro siempre lleva clip.** Si sobra presupuesto de clips, se gasta ahí primero.
- **El primer clip nunca cae antes del segundo 5.** Los primeros segundos son tu cara y el
  header — el gancho lo cargas tú, no la animación.

Si la historia solo se gana 2 clips, se hacen 2. No se rellena para llegar a 5.

---

## 2. El preset

Se elige **uno solo** del `catalogo-clips-higgsfield.md` según el tono de la historia y se
resuelve una vez:

```
resolve_explainer_preset({ preset_id: "<id del catálogo>" })
→ { preset_id, name, media_id }
```

Ese `media_id` se pasa como referencia de estilo en **todos** los frames del video. Es lo
único que hace que los clips parezcan hermanos.

Antes de elegir por la persona, ofrecerle 3 presets candidatos con su `video_url` de preview
(viene en `get_explainer_presets`) para que vea el estilo sin gastar un crédito.

---

## 3. El frame de cada beat

Cada clip nace de una imagen fija y después se anima. Generar directo a video con solo texto
da resultados inconsistentes entre clips.

```
generate_image({ params: {
  model: "nano_banana_pro",
  prompt: "<prompt del beat>",
  aspect_ratio: "9:16",
  medias: [{ value: "<media_id del preset>", role: "<rol de referencia de estilo>" }]
}})
```

**El `role` no se adivina.** Los roles válidos varían por modelo. Consultar antes con:

```
models_explore({ action: "get", model_id: "nano_banana_pro" })
```
y leer `medias[].roles`. Si el rol correcto no está claro, el servidor lo autocorrige cuando
es inequívoco, pero conviene mirarlo una vez y dejarlo anotado.

### Cómo se escribe el prompt de un beat

Cuatro piezas, en este orden:

1. **Sujeto concreto.** Una persona, un objeto, una escena. Nunca un concepto suelto.
2. **Qué está pasando** — una sola acción, presente.
3. **Encuadre 9:16** — plano vertical, sujeto centrado o en tercio superior.
4. **Nada de estilo.** El estilo entra por el `media_id`, no por el texto. Si escribes
   "estilo claymation" además de pasar el `media_id` de Claymotion, compiten y sale peor.

**Sin texto dentro del clip.** El texto va en el header del MANIFEST, sobre tu cara, donde
se lee. El texto generado dentro de un clip de 4s a 9:16 casi siempre sale mal escrito o
ilegible, y en español se rompe más.

---

## 4. Animar el frame

```
generate_video({ params: {
  model: "seedance_2_0",
  prompt: "<movimiento, una sola frase>",
  aspect_ratio: "9:16",
  duration: 5,
  generate_audio: false,
  medias: [{ value: "<job_id o media_id del frame>", role: "start_image" }]
}})
```

**`generate_audio: false` es obligatorio.** Estos clips van debajo de tu voz. Un clip con
audio nativo mete ruido bajo tu narración y además cuesta más. Con `kling3_0` el parámetro
equivalente es `sound: "off"`.

El prompt de movimiento describe **una sola cosa que se mueve**. "La cámara se acerca lento
mientras la figura levanta la cabeza" está bien. Tres acciones simultáneas en 5 segundos
producen un clip confuso.

---

## 5. Créditos: preflight obligatorio

Antes de generar nada, sacar el costo real sin enviar el trabajo:

```
generate_image({ params: { ..., get_cost: true } })
generate_video({ params: { ..., get_cost: true } })
```

Multiplicar por el número de clips, comparar contra `balance()` y **decirle el total antes
de disparar**. Nunca quemar créditos sin que lo haya visto.

**Sobre `use_unlim`:** omitirlo. Si la cuenta tiene generaciones ilimitadas que cubren el
modelo, el servidor no envía nada y devuelve `unlim_choice` — esa es una pregunta para la persona,
no una decisión tuya. Nunca pasar `use_unlim: true` por iniciativa propia "para ahorrarle
créditos".

**Si el saldo no alcanza:** no fallar. Entregar `GUION.md` + `MANIFEST.md` con los prompts
listos y las filas de B-roll apuntando a archivos que aún no existen, y decirlo claro.
La persona genera después.

---

## 6. Descargar

Los clips terminados se bajan a la carpeta del proyecto:

```bash
curl -L "<url del resultado>" -o "$DEST/clips/clip01.mp4"
```

Numerados en orden de aparición en el guion, no en orden de generación.

---

## 7. El MANIFEST

Formato exacto que espera `editor-video-formula100k`. La keyword es **verbatim del guion**,
4-8 palabras, y tiene que ser algo que la persona realmente vaya a decir — el editor la resuelve
contra el transcript real, no contra el guion.

```markdown
# Reel — <título>

- **Video fuente:** <ruta al .mov grabado>
- **Fecha:** YYYY-MM-DD

## Header

- **Línea 1:** <gancho textual, 3-5 palabras>
- **Línea 2:** <3-5 palabras>

## Énfasis

| Keyword | Texto en caja blanca | Duración |
|---------|----------------------|----------|
| ...     | ...                  | 1.6      |

## B-roll

| Keyword                        | Archivo              | Duración | Estilo        |
|--------------------------------|----------------------|----------|---------------|
| sentada mirando ese número     | clips/clip01.mp4     | 5        | monitor-photo |
```

**Reglas de la keyword:**
- Verbatim. Si en el guion dice "ese número" y en cámara sale "esa cifra", el cue se descarta
  en silencio. Elegir frases que sobrevivan a la improvisación: sustantivos concretos, no
  conectores.
- Nunca dos entradas de B-roll solapadas en el tiempo. Con clips de 5s, dejar al menos 8
  segundos de guion entre keywords consecutivas.
- Sin acentos ni puntuación no importa: el editor normaliza.

---

## 8. Degradación

| Si falla… | Qué hacer |
|---|---|
| `resolve_explainer_preset` no devuelve `media_id` | Usar el campo `prompt` del preset (viene en `get_explainer_presets`) como prefijo de estilo en cada prompt de imagen. Sale menos consistente — avisarlo. |
| Saldo insuficiente | Entregar guion + MANIFEST + prompts. No generar. |
| Un clip sale mal | Regenerar solo ese frame. Nunca cambiar de preset a mitad de video. |
| La historia no se gana ningún clip | Decirlo. Entregar solo el guion y mandarla a `guionizacion-formula100k` si quiere otra capa. Es un resultado válido. |
