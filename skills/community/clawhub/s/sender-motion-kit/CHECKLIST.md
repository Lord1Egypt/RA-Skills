# CHECKLIST — Criterios de diseño y técnicos (gate por ronda)

Formato: ✅ cumple · ⚠️ parcial/aceptado con deuda · ❌ no cumple. Evidencia = versión/commit.
Ninguna ronda se publica si hay ❌ en A/B/E-rojo. El diseño se evalúa ANTES que la performance (regla "diseño primero").

## A · DESIGN (peso Awwwards 40%)
- [x] Concepto único que justifica CADA efecto: el film ES la página (backbone scrubbed + hojas/ventanas) — v16/v17
- [x] Paleta oficial #ffffff / #1e73be / #494949 / #0085b2 sin temas ajenos — v2
- [x] Tipografía moderna self-hosted: Space Grotesk + Manrope + IBM Plex Mono + Fraunces (acento) — v20
- [x] Superficies minimalistas: hairlines y paneles agrupados, sin cajas sueltas ni rellenos — v18/v23
- [x] Fotografía REAL del cliente integrada en TODOS los slots y SIN REPETICIONES: 16 vistas únicas de stacks (recortes/grados reales por producto) — v29; cero imágenes de ejemplo
- [x] Cero placeholders visibles en producción — ✅ v26: badges y leyenda eliminados; prod stacks y prop con Ken Burns de fotos reales del cliente
- [x] Contraste AA sobre media: hojas oscuras / text-shadow en ventanas — v19/v21
- [x] Ritmo editorial: folios NN/NN, breaths, drop-cap Fraunces, pull-quotes, hairlines — v4/v17
- [x] Micro-detalles: hover duotono→color, scramble HUD, grado por capítulo, REC monitores — v18-v24
- [x] Hero compuesto sobre el film sin bloque sólido ni caja — v15/v21/v23

## B · USABILITY (30%)
- [x] i18n ES/EN completo (198 claves) con switch en nav — v9/v17
- [x] Navegación: anclas de capítulo + menú overlay con focus-trap + Esc — v16
- [x] Dossier overlay (tabla 15 familias) con foco devuelto — v17
- [x] WhatsApp FAB estilizado según marca — v3
- [x] prefers-reduced-motion respeta TODA animación (lm, grain, tilt, scrub, ring) — v16-v21
- [x] Breakpoints reales probados: 415 móvil · 830 "modo escritorio" · 1440 desktop — v22
- [x] Verificabilidad de build para el cliente: tag BUILD visible + cache-buster ?v=N — v25
- [x] 404 de marca + skip-link + alt descriptivos en fotos reales — v16/v24

## C · CREATIVITY (20%)
- [x] Scroll = transporte del film (scrub global + HUD CH + nombre de sección decode) — v17/v19
- [x] Scrub continuo: lerp rAF + throttle + keyframes densos (-g 8) — v21
- [x] Ken Burns global 1.10→1 + parallax depth + tilt rotateX de hojas — v18/v20
- [x] Capítulo de producto real (GoPro 11 Mini turntable) dentro del backbone — v24
- [x] Line-mask reveals + split-words manuales i18n-safe — v18
- [x] Interacción firma novedosa (jurado 2026): KNOB de sintonía arrastrable+teclado que gobierna scroll/espectro/film — v26
- [x] Capa 3D (globo wireframe + arcos + partículas) con presupuesto por dispositivo — v3/v21/v23.1

## D · CONTENT (10%)
- [x] Copy 100% real sender.cl, sin lorem — v2
- [x] Catálogo completo 15 familias (dossier) + 4 productos + 2 proyectos + exhibits A-C — v4/v17
- [x] Datos como diseño: 3.759 km, 60 m, 20+ años, frecuencias — v4
- [x] Contacto real (dirección, mail, wa.me) — v2

## E · TÉCNICO (rojo = bloqueante)
- [x] ROJO: deploy automático Pages en cada push + repos sincronizados (main/lab/kit) — v1-v24
- [x] ROJO: main bundle < 700 KB → 178.8 kB (three.js diferido) — v23.1
- [x] ROJO: a11y Lighthouse CI ≥ .85 (assert error-level en CI) — v23
- [x] ROJO: html-validate + budget de bundle en cada push — v23
- [x] Fuentes ≤ 14 woff2 latin self-hosted, font-display swap — v20
- [x] Videos scrub con faststart + keyframes densos; poster de respaldo; preloads LCP (poster+fonts); repo sin assets muertos (tx-hero/p-*/renders fuera) — v21-v28
- [ ] Perf Lighthouse headless ≥ .70 — ⚠️ DEUDA ACEPTADA 0.57-0.61 tras mitigaciones v28 (scope rAF sólo visible, content-visibility, fotos -30%, three diferido, preloads). Field móvil fluido verificado. Plan restante: sprites de poster por capítulo
- [x] og:image de marca + meta por sección + 404 — v24
- [x] Sin dependencia de CDN externa (fonts, libs bundlerizadas) — v20/v23.1

## F · PROCESO (skill S0)
- [x] Registro STATE.md por versión · traceabilidad TRACEABILITY.md · workflow WORKFLOW.md
- [x] Feedback del usuario cerrado con tabla queja→fix y link ?v=N
- [x] Assets del cliente versionados en repo (no hotlinks)
