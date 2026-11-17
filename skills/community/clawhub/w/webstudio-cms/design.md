# Webstudio Design System

How Webstudio applies and manages design - tokens, CSS variables, states,
responsive, and output. Source: official docs (Design tokens, CSS variables,
States & selectors, Responsive design, Style panel).

## Design tokens vs CSS variables (two layers)

Webstudio treats reusability as two complementary layers:

- **Layer 1 - CSS variables** (bottom layer): individual variable names + values,
  one per color/size/etc. in your design system. Used throughout the site and inside
  Tokens. Syntax is standard CSS custom properties (`--gray-5`).
- **Layer 2 - Design tokens** (next layer): package up MULTIPLE styles into one
  reusable token (e.g. a `Card` token = padding + color + gap). Token style values
  should be defined as CSS variables so a change in one place propagates.

Use semantic token names (Card, Testimonial), not utility names (padding-medium).
Most tokens should be semantic; utility tokens are the minority.

## Why tokens instead of classes

Tokens let you mix-and-match freely (apply as many as you want, in any order, no
combo-class or breakpoint limits). They follow the Design Tokens Community Group
format, so they can be imported/exported between apps and (soon) synced with Figma.

## Creating & using tokens

- Every instance has a **Local** style source (unique to that instance, not reusable).
  Convert Local styles to a Token via the token menu.
- Add a new token by clicking the Style Sources input, typing a name, Enter.
- The token you're currently styling shows blue; applied property labels turn blue.
- Styling a token reflects across ALL instances using it.

### Importing tokens

Webstudio can import from the Design Tokens Community Group format or Figma
Variables API exports. Paste the JSON into the Builder. On name conflicts choose
Theirs (suffix), Ours (skip), or Merge. Review before applying, especially with
multiple modes/aliases.

### Advanced token techniques

- **Composition:** combine a base token + modifier tokens (e.g. "card" +
  "card-featured") to build variants.
- **Priority/cascade:** when multiple tokens set the same property, the RIGHTMOST
  token wins.
- **Local overrides:** to override a token on one instance, apply tokens then drag
  Local to the rightmost position and add overrides there (Local takes priority).
- **Resetting:** select the token, hover a property label, click reset (or
  Option+click) to remove it from that token.
- **Duplicating:** token menu > Duplicate to create variations.
- **Conflict on paste:** same name+styles auto-merge; same name+different styles get
  a numeric suffix. Use Commands (⌘+K) > "duplicate tokens" to find identical tokens.

## CSS variables

- Define in the Advanced section with `--name` syntax. Available on the instance
  they're defined on and its children.
- Use via autocomplete (search `--`, `var`, or the name). Display syntax is
  `var(--my-var)` but searching with `--` is faster; Webstudio handles conversion.
- A common pattern: generate a `<style>` tag via an HTML Embed expression that
  defines CSS variables, then consume them in style fields.
- Check **Craft** - the standard guideline with a library of expertly crafted CSS
  variables - before creating custom ones.

## States & selectors (interaction styling)

States (pseudo-classes) let you style on hover/focus/active; pseudo-elements target
`::before`/`::after` etc.

- Open the Style Sources dropdown (⌘+Enter / Ctrl+Enter).
- Select an instance, choose a state from the list, then every style applies only to
  that state. Click the tag to return to base.
- You can type ANY valid CSS pseudo-class as a custom selector, but prefer the
  predefined validated ones.

## Responsive design & breakpoints

- Style changes on one breakpoint cascade to it and all smaller ones.
- Create custom breakpoints with ANY media query condition (width, `prefers-color-
  scheme` for dark mode, `prefers-reduced-motion`, `orientation`).
- The canvas sizes to the extreme of the selected breakpoint so you catch edge
  issues. Check ALL breakpoints, not just desktop.
- Don't over-add breakpoints or mix min/max-width.

## Output & atomic CSS

- By default Tokens/styles are converted to **atomic styles** - much less CSS,
  faster loading.
- To get human-readable class names on export, disable Atomic CSS in Project
  Settings.
