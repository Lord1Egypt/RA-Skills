# Scorecard Awwwards — sender-site
Criterios oficiales (jurado ≥18 miembros, se descartan los 3 votos más alejados):
**Design 40% · Usability 30% · Creativity 20% · Content 10%.**
Honorable Mention ≥ 6.5 · SOTD recientes: 7.45–8.65.

## Autoevaluación ponderada (2026-09-23, v18 — spine cinemática)
| Criterio | Peso | Nota | Evidencia |
|---|---|---|---|
| Design | 40% | 8.6 | Spine de película global (film-layer scrubbed + HUD + 3 respiraciones); hojas vidrio-grafito minimal transparentes; tarjetas sin relleno agrupadas en paneles hairline; paleta oficial |
| Usability | 30% | 8.4 | i18n ES/EN 198/198; protocolo contraste (hojas oscuras + text-shadow en ventanas); dossier overlay (Esc, foco devuelto); anclas de capítulo; a11y base v16; offscreen-pause |
| Creativity | 20% | 9.0 | Scroll = transporte de la película: 1 viaje continuo con ventanas sin marco; tilt rotateX+scale de hojas; line-mask reveals; parallax depth; tilt 3D del titular; GoPro scrub |
| Content | 10% | 8.5 | Catálogo completo (15 familias en dossier), trayectoria EXHIBIT A–C, 4 productos, 2 proyectos, contacto real |
| **Ponderado** | | **≈ 8.6** | Rango SOTD reciente 7.45–8.65: zona alta |

## Autoevaluación histórica (2026-09-23, post v13.1)
| Criterio | Peso | Nota | Evidencia / deuda |
|---|---|---|---|
| Design | 40% | 8.0 | Sistema de marca coherente (DESIGN.md), capa editorial, zonas negro-cine; deuda: consistencia del menú overlay en landscape móvil |
| Usability | 30% | 7.5 | Lenis, nav, bilingüe, a11y base, videos preload metadata; deuda: **jank en Android gama media** (pins 100vh + 3 videos), sin focus-trap en menú, Lighthouse aún no corrido |
| Creativity | 20% | 8.2 | Firma doble: desarme scrubbed de apertura + productos keynote; lenguaje GoPro transversal |
| Content | 10% | 8.5 | Copy real sender.cl sin repeticiones, datos como exhibits, ES/EN |
| **Ponderado** | | **≈ 7.9** | Zona HM holgada; para SOTD hay que subir Usability a 8.5+ |

## Palancas para SOTD (en orden de impacto/precio)
1. Performance móvil: un solo video scrub activo a la vez (IntersectionObserver pausa el resto), `content-visibility`, sprites de poster.
2. Focus-trap + navegación por teclado del menú overlay.
3. SplitText oficial + will-change audit (menos layout thrash).
4. Página 404 de marca + OG por sección.
5. Un "momento memorable" extra: morph del logo en preloader (MorphSVG gratis).

## Benchmark 2026 (fuente: analisis Q1-2026 + jurado oficial)
- 61% de SOTD Q1-2026 son experiencias inmersivas 3D (23% en Q1-2024); 29/47 con Three.js.
- Narrativas scroll-driven puntuan +1.8 vs showcases estaticos (Web Almanac 2024-2026).
- Creatividad 3D promedia 8.7 vs 6.4 flat; el jurado premia novedad de interaccion, no de layout.
- Sender-site v23: narrativa film-scrub continua (scroll-driven ✓) + capa 3D ligera + editorial;
  posicion: hibrido editorial-inmersivo, zona SOTD con usabilidad movil cerrada (v21-v23).
