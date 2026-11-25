# Recipe-catalog starter

A copyable implementation of the pattern described in
`../../references/recipe-catalog-pattern.md`. Read that file first — this is the
"stop describing it, start from it" companion.

## Adopting this

1. Copy this directory into your project, e.g. as `bin/screenshot/`.
2. Replace the example entries in `recipes.ts` with your own scenes.
3. If your app operates on a git repo, swap the `materializeFixture` TODO in
   `screenshot.ts` for [`git-scenarios`](https://github.com/gfargo/git-scenarios)
   instead of hand-rolled `git init`/`git commit` calls.
4. Fill in `themes.ts` if your app has multiple themes/presets — otherwise the
   single default in `resolveTheme` is fine as-is.
5. Wire up scripts in your `package.json`:

```json
{
  "scripts": {
    "screenshot": "tsx bin/screenshot/screenshot.ts",
    "screenshot:list": "tsx bin/screenshot/screenshot.ts --list",
    "screenshot:sync": "tsx bin/screenshot/syncScreenshots.ts"
  }
}
```

6. Only wire `syncScreenshots.ts` once you actually have a docs/site to publish
   into — until then, `captures/` is fine as the destination and this file can
   wait.

## What's here

| File | Role |
|---|---|
| `recipes.ts` | The catalog — a typed, declarative list of named scenes. Edit this most often. |
| `themes.ts` | Maps your app's theme/preset names to VHS terminal palettes. |
| `tape.ts` | Pure `recipe -> tape string` transform. Determinism rules live here once. |
| `screenshot.ts` | The driver: fixture -> tape -> `vhs` -> optimize -> cleanup. |
| `syncScreenshots.ts` | Copies an allow-listed subset of captures into a docs/site asset folder. |

## Requirements

- `vhs` and `gifsicle` on `PATH` (see the main skill's Setup section).
- A TS runner (`tsx`, `ts-node`, or compile with `tsc` first) — the files use
  only Node built-ins otherwise, no extra dependencies required.

## Deliberately not included

- Any specific fixture-builder implementation — that's app-specific. Use
  `git-scenarios` for git-based apps; write your own for anything else.
- CI wiring — add a workflow that runs `npm run screenshot` on release once
  this is working locally.
