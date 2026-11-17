# Design Tokens for Production UI

A token system is what separates "styled with Tailwind" from "has a design system." Every value below should be declared once, in the CSS entrypoint's `:root` / `.dark` blocks (see `tailwind-v4-setup.md`), and referenced everywhere else by name — never by raw value in component code.

## Color: name by role, not by hue

Wrong: `bg-blue-500`, `text-gray-700` scattered through components — a rebrand means a project-wide search and replace, and nothing guarantees consistency.

Right: a fixed set of semantic roles, each mapped to a palette value:

| Role | Purpose |
|---|---|
| `background` / `foreground` | page base and default text |
| `card` / `card-foreground` | surfaces raised above the page |
| `primary` / `primary-foreground` | main brand action (primary buttons, active states) |
| `secondary` / `secondary-foreground` | lower-emphasis actions |
| `muted` / `muted-foreground` | de-emphasized text, disabled states, placeholders |
| `accent` / `accent-foreground` | hover/highlight states |
| `destructive` / `destructive-foreground` | delete, error, irreversible actions |
| `border` / `input` / `ring` | dividers, form field borders, focus rings |

This is also exactly shadcn/ui's default variable set (see `shadcn-setup.md`) — using the same names means shadcn components pick up your palette with zero per-component edits.

### Building the palette in OKLCH

Use OKLCH (`oklch(L% C H)`) instead of hex or HSL for token definitions. Lightness (`L`) is perceptually uniform across hues in OKLCH, so two colors with the same `L` value actually look equally light/dark to the eye — this matters for building a consistent step scale and for hitting predictable contrast ratios.

```css
:root {
  --primary: oklch(55% 0.22 265);        /* base brand hue */
  --primary-hover: oklch(48% 0.22 265);  /* darker, same chroma/hue for hover */
  --destructive: oklch(58% 0.24 27);     /* red, similar L to primary for balance */
  --muted-foreground: oklch(55% 0.01 285); /* low chroma = desaturated gray-ish */
}
```

Practical rule of thumb: keep hue (`H`) and chroma (`C`) roughly fixed within a color's family, and step only lightness (`L`) to generate hover/active/disabled variants. That keeps the whole family visually related instead of ad hoc.

### Contrast floor

Body text on background: **4.5:1 minimum** (WCAG AA). Large text (≥24px or ≥19px bold) and meaningful icons: **3:1 minimum**. Check every `foreground`/`background` pairing you define against this, not just the default black-on-white case — muted text and disabled states are where contrast violations hide.

## Typography

Two roles minimum, three if the product shows dense data:

- **Display** — headlines, hero text. Can have real personality; used with restraint (headings only, not body copy).
- **Body** — everything else: paragraphs, labels, UI text. Optimize for legibility at small sizes, not character.
- **Mono** (optional) — code, IDs, tabular numeric data where digit alignment matters.

```css
@theme {
  --font-display: "Geist", sans-serif;
  --font-sans: "Inter", sans-serif;
  --font-mono: "JetBrains Mono", monospace;
}
```

Type scale — define once, use consistently rather than picking arbitrary `text-*` sizes per component:

| Token | Size | Use |
|---|---|---|
| `text-xs` | 12px | captions, metadata |
| `text-sm` | 14px | secondary UI text, form labels |
| `text-base` | 16px | body default |
| `text-lg` | 18px | emphasized body |
| `text-xl`–`text-2xl` | 20–24px | section headings |
| `text-3xl`–`text-5xl` | 30–48px | page/hero headings |

Line height: tighter (`leading-tight`) for large display text, generous (`leading-relaxed`) for body paragraphs longer than ~2 lines.

## Spacing and radius

Stick to Tailwind's default spacing scale (4px base unit: `1` = 4px, `2` = 8px, `4` = 16px...) rather than inventing arbitrary pixel values — consistency compounds across a whole UI far more than any single spacing choice matters in isolation.

Radius as a named token so a single change (e.g. sharper vs. softer brand direction) propagates everywhere:

```css
@theme {
  --radius-sm: 0.375rem;
  --radius: 0.625rem;   /* default — cards, buttons, inputs */
  --radius-lg: 1rem;    /* large surfaces, modals */
  --radius-full: 9999px; /* pills, avatars */
}
```

## Elevation (shadow)

A small, ordered shadow scale communicates z-order without needing a design meeting every time:

```css
@theme {
  --shadow-xs: 0 1px 2px oklch(0% 0 0 / 0.05);
  --shadow-sm: 0 2px 8px oklch(0% 0 0 / 0.08);
  --shadow-md: 0 4px 16px oklch(0% 0 0 / 0.10);
  --shadow-lg: 0 8px 30px oklch(0% 0 0 / 0.14);
}
```

Use sparingly — reserve `shadow-md`/`shadow-lg` for genuinely floating elements (dropdowns, dialogs, popovers), not every card on the page.

## Layout patterns for production pages

**Landing / marketing page**: hero → social proof (logos or a stat) → feature grid (3 or 4 columns, collapsing to 1 on mobile) → deeper feature sections alternating text/visual sides → pricing (if applicable) → final CTA → footer with real link groups. See `examples/landing-page.tsx`.

**Dashboard / app shell**: fixed or collapsible sidebar (`Sidebar` component) + sticky topbar (breadcrumb or page title, search, user menu) + scrollable content region. Content region uses a consistent max-width and padding token, not per-page arbitrary values. See `examples/dashboard-layout.tsx`.

**Auth pages**: centered card on small viewports; split-screen (form + brand panel or illustration) on desktop is common but not mandatory — a plain centered card is equally production-valid and simpler to maintain. Always design the error and loading states, not just the happy path. See `examples/auth-page.tsx`.

## Checklist before moving to components

- [ ] Every color used in the mockup/plan maps to a named role, none are raw hex
- [ ] Type scale has ≤6 sizes in active use, not an ad hoc size per heading
- [ ] Spacing uses the default scale, no arbitrary `px-[13px]` values without a real reason
- [ ] Radius and shadow are tokens, reused consistently across similar surface types
- [ ] Dark mode variants defined for every token if the product needs dark mode at all
