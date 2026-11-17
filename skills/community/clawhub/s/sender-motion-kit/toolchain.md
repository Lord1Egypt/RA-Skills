# Toolchain — herramientas que SE USARÁN (auditadas 2026-09-23)

## Sandbox Arena (por sesión; el sandbox se resetea entre mensajes)
| Herramienta | Versión verificada | Rol | Nota operativa |
|---|---|---|---|
| Node / npm | 20.20.2 / 10.8.2 | build Vite | `npm install` obligatorio cada sesión |
| Python + PIL | 3.13.14 / 12.3.0 | animatics frame-a-frame (P08) | siempre disponible |
| git | 2.47.3 | versionado | **re-setear identity cada sesión** (`agent@arena.local` / `Arena Agent`) |
| ffmpeg-static | vía `npm i --no-save` | cortes, Ken Burns, extracción de frames | no persiste; reinstalar cada sesión |
| Token GitHub | rotativo | push/API | mascar en toda salida; nunca escribirlo en archivos del repo |

## Build del sitio (sender-site)
| Lib | Versión | Rol |
|---|---|---|
| Vite | ^6 | bundler + dev |
| **GSAP** | **^3.15 (upgraded desde 3.12.5)** | ScrollTrigger scrub/pin + **SplitText, ScrollSmoother, MorphSVG ahora incluidos gratis** |
| Lenis | ^1.1.14 | smooth scroll (evaluar reemplazo por ScrollSmoother solo si hay jank medido) |
| three.js | ^0.186 | globo + arcos + partículas fly-through |

## CI/CD (GitHub Actions, repo sender-site)
checkout@v4 (submodules: recursive) → setup-node@20 → npm ci → npm run build →
configure-pages@v5 → upload-pages-artifact@3 → deploy-pages@v4. ~40 s por push.

## Puentes de archivos con el usuario (celular → sandbox)
1. **tmpfiles.org** (~60 min): viewer link → grep `class="download"` → curl `/dl/<token>/…` → validar magic `ftyp`/`89 50 4E 47`.
2. **Litterbox** (1–72 h) y **Catbox** (permanente): link directo, curl sin receta.
3. Arena attach rechaza .mp4 → nunca depender de attach.

## Lado usuario (producción de assets)
Veo 3.1 / Minimax H3 / **Seedance 2.5** con plantilla camera-first (docs/video-prompts.md) ·
Chrome mobile para screen-recordings de contraste · tmpfiles/litterbox para entrega.

## IA / orquestación
Arena Agent Mode (este chat) = equivalente a Claude Code / Antigravity de los tutoriales:
sandbox + tools + GitHub como puente persistente · multi-repo vía submodule (sender-motion-kit).

## Fuera de stack (decisión consciente)
Puppeteer/Lighthouse en sandbox (sin Chrome) → performance se valida con **field recordings**
del usuario + presupuesto de bundle (videos ≤8 MB, imágenes q4 ≤1600px) · React kits (stack vanilla) ·
Locomotive/ScrollMagic (redundantes/legado) · 21st.dev (key pagada).

## Próximas adopciones habilitadas por el upgrade GSAP 3.15
1. **SplitText oficial** en reemplazo del split-words casero (menos código, más robusto con i18n).
2. **MorphSVG** para morph del logo en preloader (momento memorable → Creativity 20%).
3. ScrollSmoother **solo** si una field recording muestra jank que Lenis no cubra.

---

## Herramientas que aparecían en los 4 videos YouTube (revisión 2026-09-23)
| Herramienta | Video(s) | Qué es | Costo real 2026 | ¿Entra a nuestro flujo? |
|---|---|---|---|---|
| Claude Opus 5.5 / Claude Code | 1 y 4 | modelo + CLI agente | Pro $20/mo, Max $100-200/mo, sin free tier | ❌ pago; **Arena Agent Mode ya es nuestro equivalente multi-modelo** |
| Google Antigravity (IDE agéntico) | 2 y 3 | VS Code fork multi-agente con browser integrado | free preview con cuota recortada (~20 req/día); tiers $20-$200; **solo desktop** | ❌ el usuario trabaja desde el celular; Arena+Actions cubren sandbox+deploy gratis |
| Gemini 3.8 Flash | 3 | modelo rápido | vía Antigravity/Google AI | 📖 referencia de velocidad; no aporta sobre nuestro stack |
| Runable | 3 | plataforma cloud de agentes (sponsor) | cloud pagado | ❌ GitHub Actions ya es nuestro runner cloud gratuito |
| **Seedance 2.5** | 4 | generación de video cinemático camera-first | según proveedor del usuario | ✅ **adoptado**: plantilla de prompt en docs/video-prompts.md; candidato para los 5 videos finales junto a Veo/Minimax |

## Conclusión "mejor opción" (multi-repo + multi-herramienta)
Combinación ganadora y $0: **Arena Agent Mode** (agente) + **GitHub** (persistencia + Pages +
Actions) + **sender-motion-kit** como submodule (conocimiento) + **tmpfiles/litterbox**
(puente celular) + **Veo/Minimax/Seedance** del usuario (footage). Las alternativas de los
videos (Antigravity, Claude Code, Cursor, Runable) son desktop-only y/o pagas: peores para
este proyecto donde el stakeholder opera desde Android.
