sender-motion-kit
Repo hermano de sender-site · montado como git submodule en vendor/motion-kit del sitio.

Qué es
La capa de conocimiento del proyecto: patrones de motion probados, recursos gratuitos auditados, scorecard Awwwards y el SOP para convertir videos de YouTube/referencias en efectos desplegados. El sitio repo = producto; este repo = biblioteca de técnicas.

Arquitectura multi-repo del proyecto
sender-site (public, deploy GitHub Pages)
├── vendor/motion-kit  ← submodule → sender-motion-kit (este repo)
├── docs/              ← brief, video-prompts, STATE
└── public/assets/videos/ ← slots auto-detectados
sender-motion-kit (public, sin build)
├── patterns.md        ← 12 patrones scroll con snippet y ubicación en el sitio
├── resources.md       ← auditoría de repos/libs gratuitos (usa / referencia / no)
├── awwwards-scorecard.md ← criterios oficiales + autoevaluación ponderada
└── youtube-sop.md     ← flujo: link → frames → patrón → deploy → contraste
Regla: si un efecto se usa dos veces, vive aquí como patrón numerado antes de copiarse.

Cómo trabajar con varios repos a la vez (Arena + GitHub)
Cada chat de Arena = sandbox aislado; GitHub es el puente persistente.
Un sandbox puede clonar N repos simultáneos y commitear a cada uno por separado.
Submodule: git submodule add <url> vendor/motion-kit + en Actions actions/checkout@v4 with: submodules: recursive.
Alternativas según necesidad: subtree (copia vendida), repo de assets con Git LFS (videos >100 MB), o repo de design-system consumido por npm/pkg.
Skill del departamento
SKILL.md — skill completa (roles, proceso, motion, 3D, film, perf, playbook Awwwards 2026, toolchain, QA). Léela primero al briefar o auditar.