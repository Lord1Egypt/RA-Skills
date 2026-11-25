# Theme pack templates

Copy into an app only when the student asks for more than one look (or during "tidy themes").
One pack = one look with a light AND a dark version. The Light / Dark / Auto toggle works inside every pack.

| File | Goes to | What it is |
|---|---|---|
| `theme-packs.ts` | `src/lib/theme-packs.ts` | The registry: `{ id, label, preview, tokens: { light, dark } }`. First entry is the default. |
| `ThemePackPicker.tsx` | `src/components/settings/ThemePackPicker.tsx` | Settings > Appearance: pack cards with previews, plus Light / Dark / Auto. |
| `theme-packs.test.mjs` | `tests/theme-packs.test.mjs` | Fails if a pack lacks light or dark, forces a mode, or misses AA contrast. |

Generate the CSS and the pre-paint script from the same data so they cannot drift:
`node "${CLAUDE_PLUGIN_ROOT}/scripts/theme-packs.mjs" css packs.json --default <id>` and `... boot packs.json --default <id>`.
Put the boot script inline in `<head>` before any stylesheet-dependent paint (Next.js: `<script dangerouslySetInnerHTML>` in `layout.tsx`, `suppressHydrationWarning` on `<html>`).
