# SOP — de reference video / YouTube a efecto desplegado

## A · Cuando llega un VIDEO de resultado (puente tmpfiles)
1. **Ingesta**: link viewer tmpfiles → grep `class="download"` → curl del `/dl/<token>/…` → validar magic `ftyp`.
2. **Extracción**: `ffmpeg-static` fps=1–2 scale=420 → frames en `/home/user/fx-frames/`.
3. **Análisis visual**: leer frames; clasificar gramática de tomas (exploded / macro / turntable / flight-map / keynote…).
4. **Mapeo**: elegir sección o slot del sitio; buscar patrón en `patterns.md` (si no existe, se crea numerado).
5. **Implementación**: HTML/CSS/JS + i18n ES/EN + marca ▸PROVISORIO si es placeholder + STATE.md.
6. **Deploy**: commit → push → Actions → curl de marcadores en prod.
7. **Contraste (lo que pediremos siempre)**: tabla de 3 columnas —
   *Pedido* (texto del usuario) · *Esperado* (lo que el patrón promete) · *Observado* (lo que el video/link del usuario muestra) → delta y acción.

## B · Cuando llega un LINK de YouTube (técnica explicada)
1. `fetch_page` del video (si 403/privado → `web_search` del título para resumen/transcripción).
2. Extraer lista de técnicas con timestamps.
3. Contrastar cada técnica contra `patterns.md` + `resources.md`: **adoptar / adaptar / descartar** con motivo de una línea.
4. Si adopta: implementar en rama de efecto aislada (un commit), verificar en prod, documentar patrón nuevo aquí.
5. Actualizar `resources.md` si aparece lib/repo nuevo (veredicto de una línea).

## C · Criterios de aceptación de un efecto nuevo
- Se percibe en móvil gama media sin jank (scrub ≤ 0.4, un video activo a la vez).
- Respeta `prefers-reduced-motion`.
- No rompe el copy (regla: cada claim una vez).
- Suma a Design+Usability (70% del score), no solo a Creativity.
