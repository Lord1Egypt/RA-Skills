# Recursos gratuitos auditados (2026-09)
Veredicto: ✅ EN USO · 📖 REFERENCIA · ❌ DESCARTADO (motivo).

| Recurso | Tipo | Veredicto |
|---|---|---|
| GSAP + ScrollTrigger | motion engine | ✅ en uso. **Desde 2025 TODO GSAP es 100% gratis** (incl. SplitText, MorphSVG, ScrollSmoother) → candidatos a adoptar: SplitText oficial (reemplaza mi split-words casero), ScrollSmoother (reemplaza Lenis si da jank en Android gama media) |
| Lenis | smooth scroll 3KB | ✅ en uso (lerp .09 + sync ScrollTrigger) |
| three.js | WebGL | ✅ en uso (globo + arcos + partículas fly-through) |
| ffmpeg-static / PIL | tooling sandbox | ✅ en uso (cortes, Ken Burns, animatics) |
| Codrops / Tympanus | demos vanilla | 📖 referencia de patrones (mejor fit con nuestro stack vanilla) |
| awesome-immersive-storytelling (vaitko) | curated list | 📖 índice de libs scrollytelling |
| OpenDesign (nexu-io/open-design) | workspace + templates | 📖 de ahí: DESIGN.md, motion-frames (type-ring), HyperFrames highlighting (marker-sweep), flight-map prompt |
| Hyperplexed (YouTube) | breakdowns | 📖 tutoriales de interacciones award-style |
| GSAP Learning (YouTube) | tutoriales | 📖 fuente del método scrub/pin |
| Anime.js v4 | physics vanilla | ❌ duplica GSAP ya presente |
| Aceternity / Magic UI / React Bits | kits React+Tailwind | ❌ stack incompatible (somos vanilla+Vite) |
| 21st.dev | marketplace | ❌ install requiere key pagada |
| Locomotive Scroll | smooth scroll | ❌ redundante con Lenis |
| ScrollMagic | scroll legacy | ❌ legado |
| Vanta.js | fondos preset | ❌ poco control de marca |
| Lottie / Rive | exports de autor | ❌ nuestros videos son footage real scrubbed |

## Próximos candidatos (cuando lleguen tus links de YouTube)
SplitText oficial · ScrollSmoother · MorphSVG (logo morph en preloader) ·
View Transitions API para rutas · `content-visibility` en secciones largas.

---

## Análisis de los 4 videos YouTube enviados (2026-09-23, SOP-B)
| Video | Contenido | Veredicto por técnica |
|---|---|---|
| Da7ZuhyWACg — Claude Opus 5.5 (3D, Web Design, Animation) | test de agente IA para UI/3D/anim | ✅ valida nuestro flujo Arena+GitHub multi-repo (equivalente a Claude Code); ✅ cursor-reactive glow → P13 |
| DJMsXSr1jec — $10k AI 3D Websites in 10 min (Antigravity) | Apple-style 3D product pages | ✅ zoom/rotate scrub del media keynote → P14; ❌ splat/model-viewer: sin assets 3D reales de Sender |
| y1pM7bS6IY8 — Interactive 3D Website (Gemini 3.8 Flash) | sitio 3D interactivo con agente | ✅ principios ya cubiertos (sticky media, scrub); ❌ WebGL interactivo pesado: penaliza Usability 30% en gama media |
| mFgRGSOGNPM — $10k 3D Animated Websites (Claude Code + Seedance 2.5) | videos cinemáticos generados + build agente | ✅ plantilla de prompt Seedance/v3 camera-first → docs/video-prompts.md; ✅ workflow agente+repo = el nuestro |
Regla aplicada: se adopta solo lo que suma a Design+Usability (70% del score Awwwards);
lo 3D-interactivo pesado se descarta con motivo (performance móvil).
