---
id: raycast-ext
kind: asset
unlocks: [raycast]
source: https://developers.raycast.com/basics/create-your-first-extension, https://developers.raycast.com/basics/prepare-an-extension-for-store, https://developers.raycast.com/information/manifest, https://developers.raycast.com/basics/publish-an-extension (loaded 2026-11-08)
---
## Smallest version
One or two commands that call the product's API: a `view` command that searches/lists the user's items, or a `no-view` command that performs the main action. API key comes from a required `password` preference. No separate configuration command.

## Scaffold
In Raycast run "Create Extension", pick a template (e.g. "Detail" or a list template), choose a folder; then `npm install && npm run dev`.

## Fields the listings check
- `package.json` manifest required: `name`, `title`, `description` (one short sentence), `icon`, `author` (your Raycast account username), `platforms` (restrict to what you support), `categories` (at least one, Title Case, case-sensitive). Store also wants `license: "MIT"`, latest `@raycast/api`, npm with `package-lock.json`.
- `commands[]`: `name`, `title` (`<verb> <noun>` or `<noun>`), `description`, `mode` (`view` | `no-view` | `menu-bar`).
- `preferences[]`: `name`, `title`, `description`, `type` (`password` for the key), `required: true`.
- Icon: 512x512 PNG, works in light and dark; default Raycast icon is rejected.
- Screenshots: up to 6 (3+ recommended), 2000x1250 PNG, captured with Raycast "Capture Window" + "Save to Metadata".
- `CHANGELOG.md` entries `## [Title] - {PR_MERGE_DATE}`; README at the root when setup (API token) is needed, media in `media/`.
- Not allowed: Keychain access, external analytics, opaque binaries.

## Steps
claude: scaffold, implement the command(s) with `getPreferenceValues()` for the key (API name unconfirmed on the pages loaded), fill manifest fields
claude: 512px icon, README explaining where to get the API key, CHANGELOG with `{PR_MERGE_DATE}`
claude: `npm run build` and `npm run lint` clean
human: capture screenshots with Capture Window -> Save to Metadata
approve: `npm run publish` (GitHub auth; opens a PR to raycast/extensions `main`), then answer review comments

## Verify locally
`npm run dev` (command works in Raycast with a test key), then `npm run build` completes without errors and `npm run lint` passes.
