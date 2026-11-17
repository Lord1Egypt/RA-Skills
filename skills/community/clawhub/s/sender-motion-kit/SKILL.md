---
name: sender-immersive-web-department
description: Skill de departamento completo (dirección creativa, motion, 3D, editorial, film, performance, QA y awards) para diseñar, construir y auditar webs inmersivas editoriales scroll-driven. Úsala al briefar, construir o auditar sitios premium con GSAP/Three.js/film-scrub, o al preparar submissions Awwwards.
---

# SKILL — Departamento de Web Inmersiva (Sender.cl)

Skill destilada de 23 rondas de producción real (sender-site v1→v23), del análisis de videos
YouTube (ScrollCraft/Nate Herk, technical-mickey, clones SOTD) y de repositorios públicos
(basementstudio/scrollytelling, gsap-video-export, cinematic-scroll-skill, awwwards-3d,
Truus.co-Awwward-Website, wibe-studio, drill-webgi). Formato inspirado en las agent-skills
de 2026: un solo archivo ejecutable por cualquier agente o humano del departamento.

## Roles del departamento (una persona-agente los cubre todos, en este orden)

1. **Dirección creativa** — concepto único que justifica CADA efecto (regla Awwwards: "effects w/o concept" pierde).
2. **Motion design** — storyboard de scroll antes de código: zonas calmadas/intensas, firmas de movimiento.
3. **3D / WebGL** — profundidad con presupuesto de GPU definido por dispositivo.
4. **Editorial / type** — jerarquía, pairing, i18n, contraste WCAG sobre media.
5. **Film / media** — pipeline de video (remaster, scrub, prompts de generación externa).
6. **Performance** — presupuestos duros y CI (Lighthouse CI, bundle budget).
7. **QA / Awards** — protocolo de capturas multi-breakpoint + playbook de submission.

## S0 · Proceso por ronda (no saltar pasos)

Documentos de control del departamento: `CHECKLIST.md` (gates de diseño/técnicos),
`TRACEABILITY.md` (pedido→entrega→herramienta→repo→commit→evidencia), `WORKFLOW.md`
(repos propios/externos, herramientas gratis, gates G0-G7, protocolo anti-cache).

1. Brief con datos REALES del cliente (nunca copy placeholder en producción).
2. Referencias: 2–4 videos YouTube + 2 repos SOTD-clone → extraer PATRONES, no copiar.
3. Sistema: paleta oficial + tipografías self-hosted + grid hairline + lenguaje de motion.
4. Construir en repo LAB separado si el cambio es de dirección; iterar en main si es refinamiento.
5. Auditar: LHCI en CI + capturas móvil / móvil-modo-escritorio / desktop.
6. Ship: Pages auto-deploy + marcador `?v=N` + entrada en STATE.md + scorecard.
7. Loop: el feedback del usuario define la siguiente ronda (capturas > opiniones).

## S1 · Backbone inmersivo de scroll (la firma del sitio)

- **El scroll es el transporte**: un film global (`#film-layer` fixed, `currentTime` ligado al
  progreso del documento) es el background de TODA la página; las secciones son hojas/ventanas
  sobre él. (P01 extendido; patrón ganador 2026: scroll-driven narrative > showcase estático, +1.8 pts.)
- **Scrub suave**: target+lerp en rAF (factor .12–.16) + throttle de escritura de `currentTime`
  (delta > .0022) + video con **keyframes densos** (`-g 8`) → seeks baratos, sin tirones.
- **Capítulos**: HUD fijo (progreso + ticks CH + nombre de sección con scramble-decode).
- **Respiraciones**: pausas de sólo-film entre actos (46vh desktop / 24vh móvil) con parallax interno.
- **Pins con propósito**: horizontal-track (proyectos), keynote por producto, ventana cine.
  En móvil/viewport angosto: DESPINAR y fluir (nada de 210vh vacíos).
- Patrones kit: P01 scrub pineado, P02 htrack, P04 stacked, P12 keynote 4-vistas, P14 zoom+rotate.

## S2 · Editorial y tipografía

- Pairing: grotesca geométrica display (Space Grotesk) + humanista moderna body (Manrope) +
  mono técnico (IBM Plex Mono) + serif SOLO como acento editorial (Fraunces: drop-cap, pull-quotes).
- **Self-hosted siempre** (woff2 latin en repo, `font-display: swap`): cero dependencia CDN,
  carga garantizada en redes malas. Nunca declarar fuentes sin `<link>`/`@font-face` real.
- Revelados: line-mask `clip-path inset` en leads/subtítulos; split-words manual en títulos
  (NO cambiar a SplitText sin manejar re-split del i18n en langchange).
- Superficies: hairlines (1px rgba blanco .10–.16) en vez de cajas; folios `NN / NN` por sección;
  agrupar tarjetas en UN panel con divisores internos (minimalismo = menos contenedores).
- Contraste sobre film: hojas oscuras semi-transparentes o `text-shadow` en ventanas sin fondo.

## S3 · 3D / WebGL con presupuesto

Prototipos de efectos viven en `sender-fx-lab` (repo dedicado): nunca se experimenta en produccion.

- 2026: 61% de SOTD Q1-2026 son inmersivos 3D (29/47 con Three.js); creatividad 3D promedia 8.7 vs 6.4 flat.
- Nuestra capa: globo wireframe + arcos de señal + partículas fly-through (`bg3d.js`, z bajo, op .45).
- **Prespuesto por dispositivo**: `matchMedia('(pointer: coarse), (max-width: 1100px)')` →
  sin loop Three.js, sin backdrop-filter, sin grain animado. El film cubre el rol inmersivo en móvil.
- Profundidad barata: perspective + rotateX/rotateY en hojas (scrub), tilt de titular con pointer
  (sólo puntero fino), scale .985→1 de entrada. WebGL pesado (shaders full-screen) = rechazado.

## S4 · Film y media (pipeline de calidad)

- Remaster de cualquier video de fondo: `hqdn3d=2:2:6:6 → scale lanczos 1080p → unsharp 5:5:0.35 →
  x264 CRF 18-20 -g 8 -keyint_min 8 -sc_threshold 0 -movflags +faststart`. (De 640×960@711kb/s a
  1080×1620 CRF20: el scrub pasa de bloqueado a cine.)
- Grado fílmico CSS: saturate/contrast/brightness + **grado por capítulo** (`[data-ch]` → filter).
- Grain SVG feTurbulence animado (overlay 5%) sólo puntero fino: disimula compresión.
- Slots provisorios = **monitores REC** (scanlines + viñeta + tag `● REC`): el placeholder se lee
  como lenguaje de rodaje; al llegar el video final se reemplaza el archivo y listo.
- El usuario genera los videos 3D externos: entregarle prompt camera-first (docs/video-prompts.md).

## S5 · Performance (presupuestos duros + CI gratis)

- Bundle main JS < 700 KB (three.js incluido); fonts ≤ 14 woff2 latin; videos scrub ≤ 4 MB.
- CI en cada push (`.github/workflows/audit.yml`, runners gratuitos): Lighthouse CI (2 runs,
  upload temporary-public-storage), html-validate, budget de bundle. PageSpeed API keyless = cuota
  compartida agotada → NO depender de ella; LHCI en CI es el reemplazo gratuito.
- Móvil: un solo video scrub activo; offscreen pause; `preload=metadata` en el resto; sin blur grande.
- Jank aceptable cero: si un efecto no mantiene 60fps en gama media, se corta o se degrada.

## S6 · Playbook Awwwards (datos 2026)

- Criterios: Design 40 / Usability 30 / Creativity 20 / Content 10; jurado ≥18, se descartan 3 outliers;
  HM ≥ 6.5; SOTD recientes 7.45–8.65; submission ~USD 65–75; elegible 3 meses; Developer Award si >7.
- Qué premia el jurado 2026: pensamiento espacial, novedad de INTERACCIÓN (no de layout),
  narrativas scroll-driven con checkpoints, post-procesado con tono, 60fps en hardware medio.
- Qué mata: jank, desktop-only, efectos sin concepto, >5 s de carga, móvil roto.
- Checklist pre-submission: LHCI a11y ≥ .85 / perf ≥ .7 móvil real; i18n completo; OG por sección;
  404 de marca; focus-trap en overlays; prefers-reduced-motion respetado en TODO; grabación móvil real.

## S7 · Toolchain gratuita (adoptar / rechazar con razón)

- Adoptado: GSAP 3.15 completo (SplitText/ScrollSmoother/MorphSVG gratis), Lenis, Three.js,
  ffmpeg-static (remasters), html-validate, LHCI, size budget bash.
- Referencia (estudio, no dependencia): basementstudio/scrollytelling, workeffortwaste/gsap-video-export
  (exportar GSAP a video para reels), MustBeSimo/cinematic-scroll-skill y tsogjavklann/awwwards-3d
  (formato skill), codebucks27/wibe-studio (Lenis+GSAP), ektogamat/drill-webgi (WEBGI).
- Rechazado: Locomotive (muerto), ScrollMagic (muerto), Vanta/Lottie (look genérico), React-only kits
  (sitio vanilla), shaders full-screen (presupuesto móvil), PageSpeed keyless (cuota).

## S8 · QA y protocolo de contraste con el usuario

- Breakpoints obligatorios de captura: móvil real, **móvil en "sitio de escritorio"** (viewport
  ~830–1350 CSS: los media móvil NO aplican → breakpoint 1100px espejo), desktop 1440.
- Cache-buster `?v=N` en cada entrega; el usuario NUNCA debe ver una versión vieja sin saberlo.
- Videos del usuario: pedir re-upload en litterbox/catbox (tmpfiles expira ~1 h).
- Cada round cierra con: link `?v=N`, tabla queja→fix, y pendientes del lado del usuario.
