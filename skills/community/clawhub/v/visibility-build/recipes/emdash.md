---
id: emdash
kind: platform
unlocks: [emdash]
source: https://github.com/emdash-cms/emdash/blob/main/packages/plugin-cli/README.md, https://github.com/emdash-cms/emdash/blob/main/skills/creating-plugins/references/publishing.md (loaded 2026-11-08 via gh api)
---
Note: the CLI README says publish/login are EXPERIMENTAL ("NSIDs and shapes will change while RFC 0001 is in flight; pin to an exact version") and "The plugin page remains unavailable until the listing is approved", so the catalog's `review: none` looks wrong.

## Smallest version
A sandboxed EmDash plugin with one route or hook that calls the product's public API (e.g. a block/route that fetches and renders the user's data, API key via plugin settings), with `allowedHosts` limited to the API host and `author.url` pointing to the product site (the backlink).

## Scaffold
`pnpm dlx @emdash-cms/plugin-cli init my-plugin` (interactive; collects publisher, author, security metadata; generates a workerd-backed Vitest host, AGENTS.md and a `skills/creating-plugins` skill). Non-interactive: `--yes --publisher did:plc:<id> --author-name "<name>" --security-email <email>`. Run project commands with `pnpm exec emdash-plugin`.

## Fields the listings check
`emdash-plugin.jsonc` (next to package.json, `$schema` `./node_modules/@emdash-cms/plugin-cli/schemas/emdash-plugin.schema.json`):
- `slug`, `publisher` (DID, e.g. `did:plc:...`; pinned after first publish; a handle pin resolves to a DID)
- `license`, `author: { name, url }` (or `authors: [...]`), `security: { email }` (or `url`; `securityContacts: [...]`)
- optional `name` (<=100 graphemes), `description` (<=140), `keywords` (<=64 each), `repo`, `version` (defaults to package.json)
- trust contract: `capabilities` (e.g. `content:read`), `allowedHosts`, `storage`
- `src/plugin.ts` default-exports a `SandboxedPlugin`; `emdash-plugin build` emits `dist/plugin.mjs`, `dist/manifest.json`, `dist/index.mjs`
- First publish needs `--license` and `--security-email`/`--security-url` if not in the manifest.

## Steps
claude: `init`, then write one route/hook calling the API; set `allowedHosts` to the API host only; `author.url` = product website
claude: `pnpm exec emdash-plugin validate` and the generated Vitest tests
human: have an Atmosphere (atproto/Bluesky) account, ideally a domain handle; `pnpm exec emdash-plugin login <handle-or-did>` (browser OAuth)
approve: `pnpm exec emdash-plugin publish` (writes profile + release records to your own PDS)
claude: `emdash-plugin info <handle-or-did> <slug> --watch` until the listing check passes and the listing is approved
claude: optional, `emdash-plugin release setup` to generate `.github/workflows/emdash-release.yml` for provenance-backed releases; approve: commit it

## Delegate
The scaffold ships its own `skills/creating-plugins` skill; use it. Tests -> mattpocock-skills:tdd.

## Verify locally
`pnpm exec emdash-plugin validate` passes, `pnpm exec emdash-plugin build` emits `dist/`, generated Vitest suite passes; `emdash-plugin dev` to run it (dev behavior not detailed in the README, unconfirmed).
