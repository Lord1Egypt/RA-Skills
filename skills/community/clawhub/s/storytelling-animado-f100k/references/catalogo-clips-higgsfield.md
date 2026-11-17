# Catálogo de clips animados de Higgsfield (explainer presets)

Verificado contra el MCP de Higgsfield el **2026-08-09**. 25 entradas en el catálogo,
**24 usables** (la 25 es basura de test, ver abajo).

Cada preset es un **estilo visual**. Se resuelve a una imagen de referencia de estilo con
`resolve_explainer_preset(preset_id)` → devuelve `media_id`. Ese `media_id` se pasa como
referencia de estilo en **todas** las generaciones del mismo video para que los clips
parezcan una sola pieza.

Verificado en vivo: `Claymotion` (`1de0f39e…`) → `media_id: 38f89354-b528-4d8a-bbae-b169a0eded9e`.

---

## Regla dura: UN preset por video

Mezclar estilos dentro del mismo reel rompe la ilusión de que los clips pertenecen a la
misma pieza y los delata como generados. Se elige uno en el Paso 5 y todos los clips salen
de ese `media_id`.

---

## Los 24 presets por familia

### Editorial / motion graphics
Para datos, números, procesos, comparaciones. Se siente premium y de marca.

| Preset | ID | Cuándo la historia lo pide |
|---|---|---|
| Editorial Motion Graphics | `56fc6472-33b7-45dc-83ff-80c71d40aec6` | Historia de negocio, cifras, "el dato que me rompió la cabeza" |
| Dynamic Motion Design | `de3bd354-69d3-4311-8f4e-6cd1e945bbc1` | Energía alta, ritmo rápido, momentos de caos |
| Poster Vector | `8014a730-3092-4f3a-b880-0321ae1d207d` | Declaraciones fuertes, manifiestos, un solo concepto por clip |
| Isometric Flat Vector | `c109eddb-1a79-478a-afd5-273bd0b205e5` | Sistemas, procesos, "cómo funciona por dentro" |

### Cartoon / dibujo
Para el error propio, la torpeza, lo autocrítico. Baja la guardia de quien mira.

| Preset | ID | Cuándo la historia lo pide |
|---|---|---|
| Stickman Cartoon | `237dd06c-3729-4895-9672-1c623c4266e0` | El error que yo también cometí. Rápido de leer, cero pretensión |
| Hand Drawn | `402635b8-7363-4172-ac78-7ffa9b999c94` | Íntimo, de cuaderno personal |
| 2D Illustrator | `5a1ae304-c541-4f11-9784-595e0f2c3d2b` | Editorial ilustrado, personaje con carácter |
| Pastel Flat 2D | `d0708b4f-a134-40f7-9884-9ad830904e71` | Suave, emocional, sin filo. Temas sensibles |
| Whiteboard Doodle | `b347d852-98fc-4013-92b7-6b0219fb21be` | Explicar un mecanismo. Se lee como "te lo dibujo" |

### Ilustración narrativa
Para el pasado, el recuerdo, la fábula. Es la familia más fuerte para storytelling puro.

| Preset | ID | Cuándo la historia lo pide |
|---|---|---|
| Watercolor Chronicle | `0029f935-be9e-46c7-a5d8-a4e0f81d49c8` | El recuerdo, "hace tres años yo…". Nostalgia sin cursilería |
| Fairy Tale & Myth | `de5b38ca-9134-4987-9d7a-d5e9085f0480` | Parábola, moraleja, el villano arquetípico |
| Vintage Documentary | `23df630a-c4f4-4f2f-b774-6ae1cd972614` | Autoridad, "esto pasó de verdad", archivo |

### Craft / matérico
Textura física. Rompe patrón brutal en un feed de talking-heads.

| Preset | ID | Cuándo la historia lo pide |
|---|---|---|
| Claymotion | `1de0f39e-c602-4b00-b54a-38440c7f63f7` | Simpático y tangible. El más versátil de la familia |
| Paper Diorama | `83d276f6-e3aa-49b8-82f2-1a0bb7d0a370` | Escenas con profundidad, "el mundo donde pasó" |
| 3D Papercraft | `bb90786e-fa06-4911-884b-c576dcd20bef` | Objetos y productos con volumen |
| Paper collage | `bc3c6f53-762e-4806-84f0-37a85e278835` | Recortes, mezcla de fuentes, caos ordenado |
| Mixed Media | `80e4dd7b-cd65-42d4-b191-b58d62558602` | Collage con foto real + trazo. Muy editorial |
| Fluffy Toy | `1fde6c92-721b-4824-b490-4ea75ad0665f` | Ternura deliberada. Temas duros contados suave |

### 3D
Para escala, objetos, "el interior de".

| Preset | ID | Cuándo la historia lo pide |
|---|---|---|
| Colorful 3D | `30948d66-76b1-4c8e-884a-1854e08e91df` | Alegre, saturado, producto |
| Studio 3D | `ab43dacd-6bee-4f8e-98b7-c4ff678bfdbd` | Limpio, fondo neutro, foco en un objeto |
| 3D Mix | `daa250fe-c353-4d26-8ab2-fc1c4ec777a4` | Escenas 3D variadas |
| Low Poly | `3e4bfd81-fbd8-4587-886d-296cbe48d152` | Geométrico, sistemas, mapas |
| Mannequin | `32356614-40f8-42b2-8a57-2f7b30cfb473` | Figura humana sin rostro. Sirve para "una persona cualquiera" sin casting |

### Retro
| Preset | ID | Cuándo la historia lo pide |
|---|---|---|
| Pixel Art | `730d436b-c0d2-4346-a7e9-3d9a80065f30` | Videojuego, niveles, "subir de nivel", nostalgia noventera |

---

## El preset basura

`pppppppppp` (`4edac834-6ec0-4b0a-9bfc-d2cafbe0c8f6`) es una prueba que quedó publicada en
el catálogo del proveedor. **Nunca ofrecerlo.** Si algún día el conteo del MCP sube, revisar
si entraron presets nuevos reales antes de asumir que el catálogo creció.

---

## Los 10 workflows de Higgsfield (contexto, no se usan aquí)

Para no confundirlos con los presets. Estos son flujos completos, no estilos:

`faceless-channel-video` · `ugc-flow` · `ugc-product-flow` · `ugc-saas-flow` ·
`ugc-try-on-flow` · `ugc-tutorial-flow` · `ugc-unboxing-flow` ·
`youtube-thumbnail-generator` · `character-sheet` · `brandkit`

**`faceless-channel-video` es el vecino directo de esta skill**: hace el video entero animado
con voz en off, sin cámara. Si la historia no necesita tu cara, esa es la ruta y esta skill
sobra. Se carga con `get_workflow_instructions({workflow: "faceless-channel-video"})`.

---

## Cómo re-verificar este catálogo

```
get_explainer_presets()
```
Devuelve `id`, `title`, `aspect`, `image`, `video_url` y un `prompt` de una línea por preset.
El `video_url` es un preview real: útil para enseñarle a alguien cómo se ve un estilo antes
de quemar créditos.
