# Brand kit — token vocabulary & intake

The studio's brand tokens. Every client site sets these once; every build
references them **by name, never raw hex/font**. Tokens map to **named Elementor
custom globals** (the `update-global-colors` / `update-global-typography` tools
write `custom_colors` / `custom_typography`, merged by `_id`).

## Color tokens (8 named custom globals)

| token `_id` | title | role |
|---|---|---|
| `brand` | Brand | primary brand color — buttons, links, emphasis |
| `accent` | Accent | secondary highlight |
| `heading` | Heading | heading text color |
| `text` | Text | body text color |
| `bg` | Background | page background |
| `surface` | Surface | card / section panel background |
| `muted` | Muted | secondary / subtle text, captions |
| `border` | Border | hairlines, dividers, card borders |

If a client supplies fewer than 8, derive and state it: `surface` = a light tint of
`bg`; `muted` = `text` at ~60% contrast; `border` = `text` at ~12% / a light grey.

## Typography tokens (2 named custom globals)

| token `_id` | title | role |
|---|---|---|
| `heading-font` | Heading Font | headings |
| `body-font` | Body Font | body / UI |

## Type scale (applied per-widget by recipes — not a global object)

| step | size (px, desktop) | typical use |
|---|---|---|
| h1 | 48 | hero title |
| h2 | 36 | section title |
| h3 | 28 | card title |
| h4 | 22 | sub-heading |
| body-lg | 18 | lead paragraph |
| body | 16 | default text |
| small | 14 | captions, labels |

Defaults: heading weight 700, heading line-height 1.15; body weight 400, body
line-height 1.6. Scale down ~15–20% on mobile.

## Logo

Record the logo media id / URL in the intake record. Header recipes use the Site
Logo widget (Pro/UAE) or a Heading fallback.

## Intake template (fill one per client)

```json
{
  "client": "Acme",
  "colors": {
    "brand": "#1A56DB",
    "accent": "#F59E0B",
    "heading": "#0F172A",
    "text": "#334155",
    "bg": "#FFFFFF",
    "surface": "#F8FAFC",
    "muted": "#64748B",
    "border": "#E2E8F0"
  },
  "fonts": { "heading-font": "Rubik", "body-font": "Inter" },
  "logo": "https://acme.example/logo.svg"
}
```

## Applying it (MCP tool shapes)

`update-global-colors` — one entry per color token:

```json
{ "colors": [
  { "_id": "brand",   "title": "Brand",      "color": "#1A56DB" },
  { "_id": "accent",  "title": "Accent",     "color": "#F59E0B" },
  { "_id": "heading", "title": "Heading",    "color": "#0F172A" },
  { "_id": "text",    "title": "Text",       "color": "#334155" },
  { "_id": "bg",      "title": "Background",  "color": "#FFFFFF" },
  { "_id": "surface", "title": "Surface",    "color": "#F8FAFC" },
  { "_id": "muted",   "title": "Muted",      "color": "#64748B" },
  { "_id": "border",  "title": "Border",     "color": "#E2E8F0" }
] }
```

`update-global-typography` — one entry per font token:

```json
{ "typography": [
  { "_id": "heading-font", "title": "Heading Font",
    "typography_font_family": "Rubik",
    "typography_font_weight": "700",
    "typography_line_height": { "size": 1.15, "unit": "em" } },
  { "_id": "body-font", "title": "Body Font",
    "typography_font_family": "Inter",
    "typography_font_weight": "400",
    "typography_line_height": { "size": 1.6, "unit": "em" } }
] }
```

Then `get-global-settings` to confirm the 8 colors + 2 fonts are present by name.

## The discipline

After intake, bind widget colors to these globals (or use the recorded token value
when a recipe sets a value directly). Never introduce an ad-hoc hex/font mid-build —
that breaks brand consistency and the recipe library.
