---
id: github-action
kind: asset
unlocks: [github-marketplace-action]
source: https://docs.github.com/en/actions/how-tos/create-and-publish-actions/publish-in-github-marketplace, https://docs.github.com/en/actions/reference/workflows-and-actions/metadata-syntax (loaded 2026-11-08)
---
## Smallest version
A composite action that runs one API call (or the product's existing CLI) in CI with the user's key from a secret, e.g. "trigger a scan/deploy/upload via the API and fail the job on error". One input for the key, one or two inputs for parameters, one output.

## Scaffold
No official generator. Hand-write `action.yml` at the repo root; composite (`runs.using: 'composite'`) needs no build step. JavaScript actions use `node24` (or `node20`).

## Fields the listings check
- `action.yml`/`action.yaml`: `name` (required, unique across Marketplace actions, categories, GitHub users/orgs unless you own it), `description` (required), `author` (optional), `runs` (required: `using: 'composite'` + `steps`, or `'node24'`/`'node20'` + `main`, or `'docker'`).
- `inputs.<id>`: `description` (required), `required`, `default`, `deprecationMessage`; exposed as `INPUT_<NAME>`. Ids start with a letter or `_`.
- `outputs.<id>`: `description`; composite also needs `value` (e.g. `${{ steps.<step_id>.outputs.<name> }}`).
- `branding.icon` (Feather icon name), `branding.color` (`white`, `black`, `yellow`, `blue`, `green`, `orange`, `red`, `purple`, `gray-dark`).
- Marketplace: public repo; a single action metadata file at the root; owner accepted the GitHub Marketplace Developer Agreement; 2FA on; a primary category chosen at release. Published immediately, no GitHub review.

## Steps
claude: write `action.yml` (composite: one `run` step using `shell: bash` that calls the API with `${{ inputs.api-key }}`), `branding`, README with a usage snippet using `secrets.<NAME>`
claude: add `.github/workflows/test.yml` that runs `uses: ./` against a test key secret
human: add the test API key as a repo secret; enable 2FA; accept the Marketplace Developer Agreement
approve: push; open action.yml -> Draft a release -> check "Publish this Action to the GitHub Marketplace", pick a primary category, tag `v1.0.0`, Publish release
approve: move a `v1` major tag to that release (convention, not on the pages loaded, unconfirmed)

## Verify locally
The test workflow run passes with `uses: ./`; the release page shows "Everything looks good!" for the metadata before publishing.
