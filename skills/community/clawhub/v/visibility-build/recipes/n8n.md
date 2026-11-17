---
id: n8n
kind: platform
unlocks: [n8n]
source: https://docs.n8n.io/integrations/creating-nodes/build/n8n-node/, https://docs.n8n.io/integrations/creating-nodes/build/reference/verification-guidelines/, https://docs.n8n.io/integrations/creating-nodes/deploy/submit-community-nodes/, https://docs.npmjs.com/trusted-publishers (loaded 2026-11-08)
---
## Smallest version
An `n8n-nodes-<product>` package with one credential (the product's API key) and one node whose operations map to the 2-4 main API actions (create/get/list...), built declaratively from the existing API docs/OpenAPI. No trigger unless the product already has webhooks (triggers must be programmatic style).

## Scaffold
`npm create @n8n/node@0.56.2`; CLI `n8n-node` subcommands: `new`, `build`, `dev`, `lint`, `release` (`release` uses release-it: build, lint, changelog, git tag, GitHub release, npm publish after `npm login` -- a local publish, which verification no longer accepts).

## Fields the listings check
- `package.json`: `name` starts with `n8n-nodes-` or `@<scope>/n8n-nodes-`; `keywords` include `n8n-community-node-package`; nodes and credentials listed under the `n8n` attribute; `license` MIT; `repository` URL matches the public GitHub repo.
- Verification: built with the n8n-node tool; not a duplicate of an existing node; no Logic/Flow-control nodes; one third-party service per package; no runtime/external dependencies; no env var or file access (data via node parameters); TypeScript; English only UI and docs; README with usage, example workflows, auth details.
- Provenance: since 2026-05-01 all verified nodes must be published from a GitHub Actions workflow with a provenance statement; no publishing from a local machine.
- `usableAsTool: true` on the node description so it works as an AI agent tool: only from a 2025 community forum post, not on an official page (unconfirmed); same post says self-hosted needs `N8N_COMMUNITY_PACKAGES_ALLOW_TOOL_USAGE=true` (unconfirmed).
- Demo video stage ("Awaiting video") in the Creator Portal: community posts only (unconfirmed).
- Review: up to four weeks.

## Steps
approve: `npm create @n8n/node@0.56.2` (downloads the scaffold); write the credential (API key header) and the node operations from the OpenAPI/docs
claude: set package.json fields above; remove any runtime dependencies
claude: add `.github/workflows/publish.yml` (tag trigger, `permissions: id-token: write, contents: read`, Node 24, `npm ci`, `npm run build`, `npm publish`) per npm trusted publishing
claude: `npm run lint` (n8n-node lint) and `npm run build`
human: npm account; configure the npm Trusted Publisher for the repo + workflow filename (first publish of a new package may need to be manual; unconfirmed)
approve: push and tag so Actions publishes with provenance
approve: `npx @n8n/scan-community-package@0.43.0 n8n-nodes-<product>` (downloads the scanner); it passes against the published package
human: sign in at https://creators.n8n.io/nodes and submit for verification
human: record the uncut demo on self-hosted n8n if the portal asks: install the exact version, add the credential, run each operation, use it as an AI agent tool

## Delegate
Operation tests -> mattpocock-skills:tdd.

## Verify locally
`npm run dev` (n8n-node dev; starts a local n8n with the node loaded, per the CLI list) and run each operation with a test key; `npm run lint` clean.
