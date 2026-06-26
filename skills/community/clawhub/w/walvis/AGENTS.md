# Repository Guidelines

## Project Structure & Module Organization
This repository has four main areas:
- `web/`: Vite + React + TypeScript frontend for browsing WALVIS data.
- `skill/`: OpenClaw skill definition (`SKILL.md`) and supporting scripts in `skill/scripts/`.
- `hooks/openclaw/`: OpenClaw message hook (`handler.ts`, `HOOK.md`) for auto-save behavior.
- `contracts/walvis_seal/`: Move contract package for Seal access policy.

Supporting files:
- `templates/` for prompt/message templates.
- `bin/cli.js` for installer/setup CLI.
- `web/public/` for static web assets.

## Build, Test, and Development Commands
Run commands from repository root unless noted:
- `npm run dev:web`: start the web app locally (`web` Vite dev server).
- `npm run build:web`: type-check and build the web bundle.
- `npm run preview:web`: preview the built web app.
- `npm run deploy:web`: build and publish `web/dist` via Walrus site builder.

Web-only equivalents:
- `cd web && npm run dev`
- `cd web && npm run generate-routes` after adding/changing files in `web/src/routes/`.

## Coding Style & Naming Conventions
- Use TypeScript/ESM patterns already in the repo (`import`/`export`, async/await).
- Match existing style: 2-space indentation, single quotes, semicolons, trailing commas in multiline objects.
- React components: PascalCase file names in `web/src/components/` (for example `ItemCard.tsx`).
- Routes follow TanStack file-based naming (for example `space.$id.tsx`).
- Do not hand-edit generated files such as `web/src/routeTree.gen.ts`.

No ESLint/Prettier config is currently enforced; rely on `tsc` strict checks in `web/tsconfig.json`.

## Testing Guidelines
- There is currently no automated test framework or coverage gate configured.
- Minimum validation for changes: run `npm run build:web` and verify key flows in `npm run dev:web`.
- For UI changes, manually verify local mode (`http://localhost:5173`) and include screenshots in PRs.

## Commit & Pull Request Guidelines
- Follow conventional commit prefixes seen in history: `feat:`, `chore:` (use `fix:` when applicable).
- Keep commit titles imperative and specific (example: `feat: add local tag editing for space items`).
- PRs should include:
  - concise summary of changes,
  - impacted areas (`web`, `skill`, `hooks`, `contracts`),
  - verification steps/commands run,
  - screenshots for frontend updates,
  - linked issue or task when available.

## Security & Configuration Tips
- WALVIS is currently testnet-first; use testnet endpoints unless intentionally changing network behavior.
- Never commit API keys, wallet secrets, or local state from `~/.walvis/`.
