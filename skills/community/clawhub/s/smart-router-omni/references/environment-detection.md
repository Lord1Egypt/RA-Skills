# Environment Detection

Use these signals to choose the routing mode.

## Stay in universal mode when

- the workspace only exposes general skill folders
- no OpenClaw-specific files, conventions, or memory layout are visible
- the task is generic and does not depend on OpenClaw runtime assumptions

## Switch to OpenClaw-aware mode when one or more of these are true

- visible OpenClaw-style skill inventory is present
- the user explicitly asks about OpenClaw
- the workspace contains OpenClaw memory or configuration structures such as:
  - `MEMORY.md`
  - `memory/`
  - `.openclaw/`
  - `bank/`
  - OpenClaw-oriented skill bundles
- the task involves browser, publish, memory, automation, or account-bound OpenClaw workflows

## OpenClaw-aware adjustments

- treat browser skills as dependency-sensitive
- treat publishing skills as platform-side execution skills
- treat memory skills as memory-only specialists, not generic fallbacks
- prefer installed specialists over broad generalists when the artifact is concrete
- prefer short chains for end-to-end OpenClaw tasks
