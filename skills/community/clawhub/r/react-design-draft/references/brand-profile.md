# Brand Profile System

A four-layer brand configuration system that goes beyond simple color/font mapping. Supports user-defined brand files, project style scanning, and priority-based override resolution.

## Layer Architecture

```
┌─────────────────────────────────────────────────┐
│  Layer 1: Explicit Prompt                       │  ← User says "--palette economist-red"
│  (Highest priority, always wins)                │
├─────────────────────────────────────────────────┤
│  Layer 2: Brand DNA Auto-Detection              │  ← URL/keyword scan matches source
│  (Auto-applied when content source detected)    │
├─────────────────────────────────────────────────┤
│  Layer 3: User Brand Profile                    │  ← ~/.config/react-design-draft/brand.md
│  (Persistent user preferences)                  │
├─────────────────────────────────────────────────┤
│  Layer 4: Three-Dimension Auto-Selection        │  ← Layout × Style × Palette matching
│  (Lowest priority, default fallback)            │
└─────────────────────────────────────────────────┘
```

## User Brand Profile File

**Location**: `~/.config/react-design-draft/brand.md`

**Format**:
```markdown
---
# Brand Profile
# This file defines your default visual identity for design drafts
---

## Colors
- primary: #1B365D
- accent: #E3120B
- background: #FDFCFA
- text: #1D1D1B
- muted: #666666
- border: #E8E6DC

## Typography
- display-font: 方正小标宋简体, Noto Serif SC, serif
- body-font: Noto Sans SC, sans-serif
- mono-font: JetBrains Mono, monospace

## Layout Preferences
- max-width: 640px
- border-radius: 2px
- spacing-scale: 4px

## Brand Rules
- Single accent color only
- No rounded cards
- Serif for all headings
- Mobile-first

## Notes
- I prefer economist-style restraint
- Always use local fonts first
- My content is primarily for WeChat public account
```

## Four-Layer Application Rules

### Layer 1: Explicit Prompt (Highest)

When user explicitly specifies any dimension via `--layout`, `--style`, `--palette`, or `--brand`:

- **Always wins** over all other layers
- User knows what they want; respect it
- Example: `--palette dark` → use dark palette regardless of brand detection

### Layer 2: Brand DNA Auto-Detection

When content source is detected (see `content-layout-mapping.md` Brand DNA Registry):

- **Overrides** Layer 3 and Layer 4
- **Yields to** Layer 1 explicit prompts
- Applies full brand visual DNA: palette + fonts + layout traits
- Must inform user in Step 2: "Detected content from [Brand], applied [Brand] visual DNA"

### Layer 3: User Brand Profile

When `~/.config/react-design-draft/brand.md` exists:

- **Overrides** Layer 4 defaults
- **Yields to** Layer 1 and Layer 2
- Provides session defaults for palette, fonts, layout preferences
- Only applies dimensions that are defined in the file (partial override)

### Layer 4: Three-Dimension Auto-Selection (Lowest)

Default behavior when no other layer applies:

- Parse content structure → match Layout × Style × Palette
- See `content-layout-mapping.md` for full three-dimension system

## Project Style Scanning

When user references a sibling project as visual reference (e.g., "make it look like my other project"):

### Scan Targets

```
1. CSS files: *.css, *.module.css
2. Tailwind config: tailwind.config.*, tailwind.*.js
3. Design tokens: tokens.json, design-tokens.*.json, *.tokens.json
4. Theme files: theme.*, theme-*.css
5. Style guides: styleguide.*, styles.scss
```

### Extraction Logic

```
For each found file:
1. Extract primary color values (first 4 unique colors)
2. Extract font-family declarations (display + body + mono)
3. Extract spacing ratio (smallest non-zero margin/padding value = base unit)
4. Extract border-radius values (most frequent = default radius)
5. Merge into session brand configuration
```

### Merge Rules

- Scanned values create a **temporary Layer 2.5** (between Brand DNA and User Profile)
- Only dimensions found in scan are overridden
- Missing dimensions fall through to lower layers
- User is informed in Step 2: "Scanned visual DNA from [project], applied [N] style properties"

## Brand Configuration Resolution Example

```
Scenario: User provides an Economist article URL, has a brand.md, and says "--layout funnel"

Resolution:
1. --layout funnel          → Layer 1 wins: layout = funnel
2. Economist URL detected   → Layer 2 wins: palette = economist-red, fonts = 方正小标宋+汇文明朝体
3. brand.md exists          → Layer 3 partially applies: max-width = 640px (not overridden by L2)
4. Auto-selection           → Layer 4 fills remaining: style = editorial-infographic

Final: layout=funnel, style=editorial-infographic, palette=economist-red, fonts=方正小标宋+汇文明朝体, max-width=640px
```

## Guard Rails

1. **Never silently override user intent** — if Layer 1 and Layer 2 conflict, Layer 1 wins and inform user
2. **Always inform user of applied layers** in Step 2 Confirm & Advise:
   - "Applied Brand DNA: [Brand] (palette + fonts)"
   - "Applied User Profile: [N] properties from brand.md"
   - "Applied Project Scan: [N] properties from [project]"
3. **Partial application is fine** — if brand.md only defines colors, only colors are overridden
4. **Brand DNA is not a prison** — user can always override with `--style` or `--palette`
5. **When in doubt, ask** — if Layer 2 and Layer 3 conflict (different palettes), ask user which to prioritize
