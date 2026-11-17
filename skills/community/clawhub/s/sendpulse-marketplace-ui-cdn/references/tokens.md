# Palette — lookup

Every colour the bundle paints is **baked in**: ~1400 selectors carry a literal value, which is why
only the other build can darken them (SKILL.md Step 5). This file is the lookup for the times you
genuinely need one of those values. Verified against the live CDN build **2026-08-25**;
`references/refresh.sh` is how you find out that has drifted.

**Reach for a semantic class before any hex** — `.text-danger`, `.bg-success`, `.color-primary`,
`.badge-status-success`, `.color-muted-link`. A literal colour belongs in app CSS only when no class
covers the case, and then it comes from this table — never from a screenshot, an eyedropper, or
another integration's stylesheet.

**These are the light values.** Dark is a separate server-rendered build of the same URL that
recolours the same selectors, so no value here survives into it. Never hand-write a dark palette
(Step 5).

| Token | Light | Notes |
|---|---|---|
| Primary (brand) | `#009fc1` | links, `.btn-primary`, `.label-primary`, `.text-primary` |
| Link hover | `#006075` | underlined on hover/focus |
| Ink / heading | `#023346` | `.color-muted-link`, `.btn-default` text |
| Muted grey | `#91a4a5` · `#465152` · `#777` | icons · badges · small text |
| Borders / rules | `#cdd4d4` | inputs, `hr`, `legend` |
| Surface grey | `#e1e8e8` (`.btn-default`) · `#e6ecec` (`.well`) · `#f8f9f9` | |
| Success | `#00b175`, text `#006532`, bg `#f2fff5` | |
| Danger | `.btn-danger` `#d94b4d` · `.text-danger` `#b2263f` · status dot `#f86850` | three reds by role — don't swap them |
| Warning | `#f0ad4e`, text `#ac6417`, bg `#fffdf4` | |
| Info | `#5bc0de`, text `#31708f`, bg `#f8fdff` | |

The font stack, the type scale, the radii and the control height are **not** here — they are in
SKILL.md Step 1, because unlike a colour there is no class that supplies them for you.

The 28 custom properties the bundle *references* and never defines are a different thing again, and
they are not lookup: copy `references/tokens.css` whole. Step 1 says why guessing them fails.
