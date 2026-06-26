# ConvoAI Sample Repos

Use this registry when the user needs a sample app, a reference project structure, or a known
repository for ConvoAI integration work.

## Default Rule
- `sample-aligned` is the default implementation mode when a listed repo matches the user's stack or requested structure.
- `minimal-custom` may only be used if the user explicitly asks for a minimal demo or says not to follow the sample repo.
- Fall back to Shengwang doc fetching only when the repo does not cover the needed API detail or is not useful for the user's question.

## Alignment Rules
- Preserve sample env var names from the cloned repo's env template files unless the user explicitly asks to rename or normalize them.
- Preserve the sample repo's folder structure, dependency choices, and API shape by default.
- Preserve the key libraries and dependency pattern already present in the chosen sample repo unless the user explicitly asks for a different architecture.
- Apply a tight diff budget: change only what is required for the user's confirmed provider choices and requested functionality.
- Before editing code, state which sample repo is being followed, which env template files were inspected, and list the exact planned differences.

## Maintenance Rules
- Keep repo URLs here only. Other ConvoAI docs should link to this file instead of repeating URLs.
- Store repo root URLs only.
- Prefer HTTPS URLs by default.
- Keep descriptions short and stable. Store only the structural fields that must be preserved during implementation.

## Usage Workflow
1. Pick the row that matches the user's platform or implementation goal.
2. If a listed sample matches the quickstart or integration request, first let the user accept the default technical path (or explicitly ask for sample-aligned implementation), then clone that repo on demand into a temporary inspection path with `git clone --depth 1 <repo-url>`, and prefer the HTTPS URL by default.
3. Inspect the repo to confirm its current stack, folder map, entrypoints, env template files, and API surface.
4. Use the cloned repo's actual env template files as the source of truth for env naming.
5. Preserve the dependency and project pattern already present in the sample repo rather than inventing a fresh starter structure.
6. If the repo does not answer the question, fetch Shengwang docs for the missing API or product details.
7. Keep the implementation structurally close to the sample unless the user explicitly requests `minimal-custom`.
8. If the matching sample repo cannot be inspected in the current environment, stop and report that blocker instead of silently inventing a fresh starter structure.
9. Only copy or adapt code into the user's actual project after the user has explicitly asked for implementation in that workspace.

## Registry

| Sample | Repo URL | Default Stack | Backend Entrypoint | Frontend Entrypoint | Use When |
|--------|----------|---------------|--------------------|---------------------|----------|
| ConvoAI web quickstart | https://gitee.com/agoraio-community/conversational-ai-quickstart.git | Monorepo with Bun scripts, `web` on Next.js 16 + React 19 + TypeScript, and `server` on FastAPI/Python | `server/src/server.py` | `web/app/page.tsx` | The user wants a ConvoAI web app structure reference, starter layout, or frontend/backend shape that stays close to the official quickstart |
| ConvoAI native client apps | https://gitee.com/agoraio-community/conversational-ai-quickstart-native.git | Multi-platform monorepo: iOS, Android, Flutter, Windows, macOS. Each platform lives in its own subdirectory. Repo contains an `AGENTS.md` describing the directory layout per platform. Self-contained — each platform app calls ConvoAI REST API directly, no separate server needed. | N/A (no server) | See repo `AGENTS.md` for per-platform entrypoints | The user wants a ConvoAI native client (non-Web): Android, iOS, Flutter, Windows, or macOS. Clone this repo, read its `AGENTS.md` to locate the target platform directory, then inspect and align only that subdirectory. |
