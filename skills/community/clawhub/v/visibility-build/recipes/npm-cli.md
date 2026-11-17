---
id: npm-cli
kind: asset
unlocks: [npm-cli, homebrew-tap]
source: https://docs.npmjs.com/cli/v11/configuring-npm/package-json, https://docs.npmjs.com/trusted-publishers, https://docs.npmjs.com/generating-provenance-statements (loaded 2026-11-08)
---
Note: the catalog's `npm-cli` platform row requires this asset or a `public-api` to wrap; `homebrew-tap` also requires the `npm-cli` asset.

## Smallest version
A CLI that wraps the product's public API: `<cli> login` saves the user's API key, then 2-4 commands map 1:1 to the most-used endpoints and print JSON or a short table. No new server features.

## Scaffold
`npm init -y`, then hand-write `bin/<cli>.js`. No official CLI template on the npm pages loaded.

## Fields the listings check
- `name`, `version`, `description`, `license`, `repository` (public, must match the publishing GitHub repo case-sensitively for provenance), `homepage`, `keywords`.
- `bin`: `{ "<cli>": "bin/<cli>.js" }`; each bin file "starts with `#!/usr/bin/env node`".
- `files`: narrow the tarball (default is everything).
- `engines`: advisory only.
- `publishConfig`: publish-time overrides (e.g. `access`).
- Trusted publisher (npmjs.com package settings -> Trusted Publisher -> GitHub Actions): Organization or user, Repository, Workflow filename (e.g. `publish.yml`), optional Environment name. Not validated on save; a new configuration must publish successfully within 2 days or it expires.
- Workflow: `permissions: id-token: write`; npm CLI >= 11.5.1 and Node >= 22.14.0; provenance is generated automatically for a public package from a public repo (no `--provenance` flag needed). Without trusted publishing: `npm publish --provenance` (+ `--access public` for a first publish).

## Steps
claude: write `bin/<cli>.js` with the shebang; `login` prompts for the key and writes it to a user config file with 0600 permissions (or reads `<CLI>_API_KEY` env); never echo the key
claude: one command per chosen endpoint, `--json` output flag, non-zero exit on API error
claude: fill package.json fields above; add `.github/workflows/publish.yml` (on tag `v*`, `permissions: id-token: write, contents: read`, checkout, setup-node with `registry-url: https://registry.npmjs.org`, Node 24, `npm ci`, `npm publish`)
human: npm account with 2FA; if the package does not exist yet, whether trusted publishing can do the first publish is not stated on the page (unconfirmed): do the first `npm publish --access public` by hand if needed
human: add the Trusted Publisher on the package settings page
approve: push the `v*` tag so Actions publishes
claude: `npm view <name>` shows the version; package page shows provenance

## Delegate
Command tests -> mattpocock-skills:tdd.

## Verify locally
`npm pack --dry-run` (tarball contents), `npm link && <cli> login && <cli> <command>` against a test key.
