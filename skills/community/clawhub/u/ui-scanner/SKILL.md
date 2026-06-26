---
name: ui-scanner
description: Given a website URL, crawl and analyze its visual design system — identify design style, color system, typography, component styles, and UI patterns. Outputs a structured design specification document for UI generation. 
---

# UI Scanner — Website Design System Extraction

Given a website URL, automatically crawl the page and reverse-engineer its visual design system, outputting a structured design specification document.

## Use Cases 

Suitable for competitive design analysis, UI replication, design system reverse engineering, and style transfer.

## Usage

Provide a target website URL; the skill performs crawl → analyze → structured output. Result written to `{domain}_design.md`.

## Workflow

```
URL input → Page crawl → Visual element classification → Style extraction → Structured output → Write file
```

## Output Format

Output file uses standard YAML frontmatter + Markdown structure:

### Design Overview

```
---
version: alpha
name: {brand name}
description: {1-3 sentence brand visual style description, including base color, core tone, font scheme}
colors:
  primary: "{primary brand color HEX}"
  primary-active: "{primary hover/active HEX}"
  ink: "{darkest text color HEX}"
  body: "{body text color HEX}"
  body-strong: "{emphasis text color HEX}"
  muted: "{secondary text color HEX}"
  muted-soft: "{weakest text color HEX}"
  hairline: "{border color HEX}"
  hairline-soft: "{weak border color HEX}"
  hairline-strong: "{emphasis border color HEX}"
  canvas: "{page background HEX}"
  canvas-soft: "{weak background HEX}"
  surface-card: "{card background HEX}"
  surface-strong: "{emphasis surface HEX}"
  on-primary: "{text color on primary HEX}"
  semantic-error: "{error color HEX}"
  semantic-success: "{success color HEX}"
typography:
  display-mega:
    fontFamily: "{font stack}"
    fontSize: {px}
    fontWeight: {numeric}
    lineHeight: {numeric}
    letterSpacing: {px}
  display-lg: {same}
  display-md: {same}
  body-md: {same}
  body-sm: {same}
  caption: {same}
  code: {same}
  button: {same}
  nav-link: {same}
rounded:
  none: 0px
  sm: {px}
  md: {px}
  lg: {px}
  xl: {px}
  pill: {px}
spacing:
  xs: {px}
  sm: {px}
  base: {px}
  lg: {px}
  xl: {px}
  xxl: {px}
  section: {px}
components:
  top-nav: {common page component style map}
  button-primary: {backgroundColor, textColor, typography, rounded, padding, height}
  button-secondary: {same format}
  hero-band: {same}
  feature-card: {same}
  code-block: {if applicable}
  text-input: {if applicable}
  footer: {same}
---
```

### Analysis Dimensions

#### 1. Design Style Description

After crawling, assess from these dimensions:

- **Brand tone**: Warm/cool/neutral, pure white/cream/dark base
- **Visual language**: Skeuomorphic/flat/neumorphic/minimalist/editorial/magazine/tech
- **Brand color strategy**: Single/dual/multi-color system, restrained vs expansive usage
- **Depth rendering**: Shadow levels, borders, layering
- **Typography tone**: Weight strategy (bold brand / 400 magazine), letter spacing (tight/loose)
- **Code/technical rendering**: Code block style, monospace font strategy
- **UI texture**: Border radius strategy, edge treatment, card style

Output a 3-5 sentence description in the `description` field of the frontmatter.

#### 2. Color System

Extract the following color categories:

| Category | Description |
|----------|-------------|
| **Primary brand** | Main CTA and brand identity color |
| **Primary hover** | Primary hover/active variant |
| **Text scale** | 4-5 levels from darkest to lightest |
| **Border scale** | 2-3 levels of hairline/border colors |
| **Page background** | Canvas, card surface, emphasis surface hierarchy |
| **Semantic colors** | Error red / success green (if visible on page) |
| **Special colors** | Timeline, tags, auxiliary colors for special components |

Extract precise HEX values from CSS (inline/computed/CSS variables/design system).

#### 3. Typography

Extract the following typography levels:

| Level | Location |
|-------|----------|
| Display mega | H1 / Hero heading |
| Display lg/md/sm | Large/medium/small display text |
| Title md/sm | Heading text |
| Body md/sm | Body text |
| Caption | Auxiliary text |
| Code | Code areas |
| Button | Button text |
| Nav link | Navigation links |

Record: `fontFamily`, `fontSize`, `fontWeight`, `lineHeight`, `letterSpacing`.

#### 4. Spacing & Border Radius

| Dimension | Extraction Method |
|-----------|-------------------|
| Border radius | Buttons, cards, inputs, badges border-radius |
| Spacing | Paragraph gaps, grid gaps, section spacing |
| Page rhythm | Content area padding, section divider spacing |

#### 5. Component Styles

Extract styles for common visible components:

| Component | Extracted Properties |
|-----------|---------------------|
| Top nav | Height, background, text color, link style |
| Button primary | Background, text, radius, padding, height |
| Button secondary | Same as above |
| Feature card | Background, radius, padding |
| Pricing card | (If present) background, radius, padding |
| Text input | (If present) background, border, height, padding |
| Code block | Background, font, radius, padding |
| Footer | Background, text color, padding |
| Badge/Pill | Background, radius, text style |
| IDE mockup | (If applicable) pane colors, code area style |

#### 6. Design Guidelines

Output under the `## Design Guidelines` section:

- **Do list**: Verifiable specification points for the brand design system (color usage boundaries, font strategy, spacing rules, etc.)
- **Don't list**: Explicit prohibitions (don't introduce a second brand color, don't use pure white background, etc.)
- **Responsive breakpoints**: If inferable, record breakpoints and layout changes

## Extraction Method

1. Use `web_fetch` to get the page HTML
2. Extract style information from:
   - CSS in `<style>` tags
   - Inline `style` attributes
   - CSS variables `--var-name`
   - Computed style patterns (inferred from class names, Tailwind classes, etc.)
   - `@font-face` declarations
   - Design system files like `manifest.json` / design tokens
3. For information not directly accessible from HTML (e.g., hover colors), infer through industry conventions
4. All color values normalized to HEX format

## Notes

- If precise values cannot be extracted (e.g., design system rendered by JS), mark as `estimated` with reasoning
- Font stacks ordered by priority, first entry being the actual brand font
- Only output components visible on the page; do not construct components not present
- Information not accessible through static HTML (e.g., animation timings) should be marked as out of scope