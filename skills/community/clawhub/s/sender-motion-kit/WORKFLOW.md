# WORKFLOW — Repos, herramientas y flujo para cumplir los criterios de diseño

Regla de oro: **diseño primero** (gates G1-G4 evalúan sólo Design/Creativity/Content);
performance y optimización entran en G6, nunca antes de que el diseño esté aprobado visualmente.

## 1 · Repositorios propios (qué y para qué)

| Repo | Rol | Reglas |
|---|---|---|
| `sender-site` (main) | Producción + Pages auto-deploy | Único que toca el dominio público. Cada push = deploy + audit CI. Commits semánticos `feat/fix/docs(vNN)`. |
| `sender-site-lab` | Sandbox de dirección creativa | Prueba conceptos rompedores sin riesgo; `compara.html` con iframes A/B lado a lado. Se sincroniza DESPUÉS de cada round aprobado (nunca al revés; su `vendor/` es copia plana, no submodule). |
| `sender-web` | REDISEÑO NUEVO (repo independiente, estático sin bundler): web "Editorial Film" — cristianoleamiranda-dotcom.github.io/sender-web |
| `sender-fx-lab` | Repo EXCLUSIVO de efectos scroll/3D/film: demos aislados P01/P14/P15/P07/P06 con Pages propia (cristianoleamiranda-dotcom.github.io/sender-fx-lab). Todo efecto nuevo se prototipa aqui antes de tocar produccion. |
| `sender-motion-kit` | Cerebro del departamento | `SKILL.md` (skill completa), `CHECKLIST.md` (gates), `TRACEABILITY.md` (rendición de cuentas), `patterns.md` P01-P14, `awwwards-scorecard.md`, `resources.md`, `youtube-sop.md`, `toolchain.md`, `docs/video-prompts.md`. |
| `vendor/motion-kit` (submodule en main) | Patterns upstream versionados | checkout recursivo en CI. No copiar encima desde el lab. |

## 2 · Repositorios externos (adoptados / referencia / rechazados)

| Repo | Uso | Por qué |
|---|---|---|
| `greensock/gsap` 3.15 (npm) | ScrollTrigger, SplitText, ScrollSmoother, MorphSVG | 100% gratis desde 3.15; estándar SOTD |
| `three.js` (npm) | Globo wireframe + partículas (`bg3d.js`) diferido | Presupuesto GPU: sólo puntero fino y >1100px |
| `ffmpeg-static` (npm) | Remasters, Ken Burns, concat de capítulos, frames de QA | Pipeline de film local reproducible |
| `@lhci/cli` + `html-validate` (npx en CI) | Auditoría continua gratuita | Runners GitHub con Chrome; upload temporary-public-storage |
| `basementstudio/scrollytelling` | Referencia de arquitectura narrativa | Estudio, no dependencia |
| `workeffortwaste/gsap-video-export` | Exportar scrubs a reels de entrega | Deliverable de marketing |
| `MustBeSimo/cinematic-scroll-skill`, `tsogjavklann/awwwards-3d` | Precedentes del formato SKILL.md | Benchmark de skills 2026 |
| `codebucks27/wibe-studio`, `ektogamat/drill-webgi` | Referencia Lenis+GSAP / WEBGI | Inspiration pool |
| Rechazados: Locomotive, ScrollMagic (muertos), Lottie/Vanta (genérico), React-kits (sitio vanilla), shaders full-screen (presupuesto móvil), PageSpeed keyless (cuota 429) | — | Razones en `resources.md` |

## 3 · Herramientas online gratuitas
GitHub Actions (deploy + audit), GitHub Pages (hosting + sin X-Frame-Options → compara.html),
LHCI temporary-public-storage (reportes públicos temporales), litterbox/catbox (puente de videos
del usuario; tmpfiles.org PROHIBIDO: expira ~1 h), web_search/fetch_page (referentes y datos de
jurado), Arena.ai workspace (assets + ffmpeg + builds).

## 4 · Flujo por ronda (gates)
- **G0 Brief/assets**: request del usuario + assets reales (uploads) → STATE.md.
- **G1 Referencia**: 2 videos YouTube (SOP-B) + 2 repos SOTD-clone → patrones nuevos a `patterns.md`.
- **G2 Sistema de diseño**: CHECKLIST sección A completa ANTES de codificar (paleta, type, superficies, ritmo).
- **G3 Build lab** (si es dirección) o main (si es refinamiento) + `?v=N` + **tag BUILD visible**.
- **G4 A/B con usuario**: compara.html o link lab; decisión explícita del usuario.
- **G5 Merge/ship**: main + Pages + marcadores curl verificados (CSS/HTML/assets 200).
- **G6 Audit**: CI LHCI/html-validate/budget + capturas en 3 breakpoints (415 / 830 desktop-mode / 1440).
- **G7 Cierre**: TRACEABILITY.md fila nueva + scorecard + pendientes del usuario.

## 5 · Protocolo "los cambios no se reflejan" (anti-cache)
1. El sitio muestra `BUILD vNN` fijo abajo-izquierda: si no coincide con el último commit → cache del cliente.
2. Link de entrega siempre con `?v=NN`; hard-refresh en desktop; cerrar pestaña en móvil (78 pestañas = cache agresivo).
3. Evidencia por cada cambio: marcador curl en producción (selector/asset/byte-range 200) anotado en TRACEABILITY.
4. Si el usuario navega en "Sitio de escritorio" del Chrome: breakpoint 1100px espeja lo móvil (v22) — verificar en ambos modos.
