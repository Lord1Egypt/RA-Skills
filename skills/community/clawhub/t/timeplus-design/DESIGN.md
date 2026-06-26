---
version: alpha
name: Timeplus Console
description: The design system for the Timeplus Console — clean, professional, and functional, with subtle pink accents for primary actions and high-contrast neutral text.
colors:
  # Gray scale — primary UI colors (light mode)
  gray-100: "#120F1A" # paragraph / primary text
  gray-200: "#231F2B" # heading text, secondary button text
  gray-300: "#3A3741" # input labels, non-button icons
  gray-400: "#514E58" # disabled secondary button text
  gray-500: "#7D7B82" # disabled input text
  gray-600: "#B5B4B8" # clickable outlines, placeholder text
  gray-700: "#DAD9DB" # non-clickable outlines, dividers, disabled button bg
  gray-800: "#ECECED" # table row hover, disabled input bg
  gray-900: "#F7F6F6" # page background
  white: "#FFFFFF"    # container bg, table row bg, on-accent text
  # Accent — pink
  pink-400: "#B83280" # link text, primary button hover
  pink-500: "#D53F8C" # primary button bg, toggle ON
  # Destructive — red
  red-400: "#751025"  # delete primary button hover
  red-500: "#D12D50"  # delete actions, error states, error text
typography:
  h1:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: 600
    lineHeight: 1.4
  h2:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: 600
    lineHeight: 1.4
  h3:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 600
    lineHeight: 1.4
  body:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
  button:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: 600
    lineHeight: 1.0
  label:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.4
  input-value:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.4
rounded:
  sm: 4px    # default radius for everything
  full: 9999px # pill shapes (toggle track)
spacing:
  1: 4px
  2: 8px
  3: 12px
  4: 16px
  5: 20px
  6: 24px
  8: 32px
components:
  button-primary:
    backgroundColor: "{colors.pink-500}"
    textColor: "{colors.white}"
    typography: "{typography.button}"
    rounded: "{rounded.sm}"
    height: 32px
    padding: 16px
  button-primary-hover:
    backgroundColor: "{colors.pink-400}"
    textColor: "{colors.white}"
  button-primary-disabled:
    backgroundColor: "{colors.gray-700}"
    textColor: "{colors.gray-500}"
  button-secondary:
    backgroundColor: "{colors.white}"
    textColor: "{colors.gray-200}"
    borderColor: "{colors.gray-600}"
    typography: "{typography.button}"
    rounded: "{rounded.sm}"
    height: 32px
    padding: 16px
  button-secondary-hover:
    backgroundColor: "{colors.gray-900}"
    textColor: "{colors.gray-200}"
  button-secondary-disabled:
    backgroundColor: "{colors.gray-700}"
    textColor: "{colors.gray-400}"
  button-destructive:
    backgroundColor: "{colors.red-500}"
    textColor: "{colors.white}"
    typography: "{typography.button}"
    rounded: "{rounded.sm}"
    height: 32px
    padding: 16px
  button-destructive-hover:
    backgroundColor: "{colors.red-400}"
    textColor: "{colors.white}"
  input:
    backgroundColor: "{colors.white}"
    textColor: "{colors.gray-100}"
    borderColor: "{colors.gray-600}"
    typography: "{typography.input-value}"
    rounded: "{rounded.sm}"
    height: 40px
    padding: 12px
  input-focused:
    borderColor: "{colors.gray-300}"
  input-error:
    borderColor: "{colors.red-500}"
    textColor: "{colors.gray-100}"
  input-disabled:
    backgroundColor: "{colors.gray-800}"
    textColor: "{colors.gray-500}"
  toggle-track-off:
    backgroundColor: "{colors.gray-600}"
    rounded: "{rounded.full}"
    width: 36px
    height: 20px
  toggle-track-on:
    backgroundColor: "{colors.pink-500}"
    rounded: "{rounded.full}"
    width: 36px
    height: 20px
  card:
    backgroundColor: "{colors.white}"
    borderColor: "{colors.gray-700}"
    rounded: "{rounded.sm}"
    padding: 24px
  table-row:
    backgroundColor: "{colors.white}"
    textColor: "{colors.gray-100}"
  table-row-hover:
    backgroundColor: "{colors.gray-800}"
  link:
    textColor: "{colors.pink-400}"
---

## Overview

The Timeplus Console design language is **clean, professional, and functional**.
It favors clarity over decoration: minimal visual clutter, hierarchy carried by
typography and spacing rather than color, and a single warm pink accent reserved
for primary actions. The result reads like a focused engineering tool — calm
neutral surfaces, high-contrast text, and predictable, consistent component
patterns across the entire application.

Use this file as the source of truth when generating any Timeplus Console UI.
The tokens in the front matter are normative — use the exact values. The prose
below explains *why* each value exists and how to apply it.

## Colors

The palette is a nine-step neutral gray scale plus a single pink accent and a
single red for destructive intent. Color is used sparingly; most of the
interface is built from grays.

**Gray scale (UI foundation).** Runs from near-black ink to a warm off-white
page background.

- **gray-100 (#120F1A):** Primary/paragraph text.
- **gray-200 (#231F2B):** Heading text and secondary button labels.
- **gray-300 (#3A3741):** Input field labels and non-button (static) icons. Also the focused input border.
- **gray-400 (#514E58):** Disabled secondary-button text.
- **gray-500 (#7D7B82):** Disabled input text and disabled-primary-button text.
- **gray-600 (#B5B4B8):** Clickable outlines (button/input borders) and placeholder text.
- **gray-700 (#DAD9DB):** Non-clickable outlines, dividers, card borders, and disabled-button background.
- **gray-800 (#ECECED):** Table row hover and disabled input background.
- **gray-900 (#F7F6F6):** The page background — never pure white.
- **white (#FFFFFF):** Container/card backgrounds, table rows, and text on colored buttons.

**Pink accent (interaction).** The only "brand" color, used to mark the single
primary action and the ON state of controls.

- **pink-500 (#D53F8C):** Primary button background, toggle ON.
- **pink-400 (#B83280):** Link text and primary-button hover.

**Red (destructive).** Reserved exclusively for deletion, errors, and validation
failures — never decorative.

- **red-500 (#D12D50):** Delete actions, error borders, error text.
- **red-400 (#751025):** Destructive-primary-button hover.

## Typography

**Inter, exclusively.** One typeface across the whole application; never mix
families. Two weights carry everything: Regular (400) for content and
Semi-Bold (600) for headings and controls.

```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

| Token       | Weight | Size | Line height | Use case |
|-------------|--------|------|-------------|----------|
| `h1`        | 600    | 18px | 1.4 | Main page titles |
| `h2`        | 600    | 14px | 1.4 | Section headings |
| `h3`        | 600    | 12px | 1.4 | Subsection headings |
| `body`      | 400    | 14px | 1.5 | Body text, descriptions |
| `button`    | 600    | 14px | 1.0 | All button labels |
| `label`     | 400    | 12px | 1.4 | Form field labels |
| `input-value` | 400  | 14px | 1.4 | Form field content |

Headings use gray-200; body text uses gray-100. Never render text smaller than
12px.

## Layout

The page sits on a warm off-white background (gray-900). Content lives inside
white cards/containers with a 1px gray-700 border and a 4px radius. Spacing
follows a 4px-based scale (`spacing.1`–`spacing.8`).

- **Container padding:** 24px (`spacing.6`) on all sides — the standard.
- **Gap between sections:** 24px (`spacing.6`).
- **Gap between form fields:** 16px (`spacing.4`).
- **Tight/internal spacing:** 4–8px (`spacing.1`–`spacing.2`).

```
┌─ Page background (gray-900 #F7F6F6) ───────────────────────┐
│                                                            │
│   ┌─ Container (white, 1px gray-700, 4px radius) ───────┐  │
│   │   padding: 24px                                     │  │
│   │   H1 page title (18px Semi-Bold, gray-200)          │  │
│   │   …content…                                         │  │
│   └─────────────────────────────────────────────────────┘ │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Elevation & Depth

This system is **flat**. There are no shadows. Depth and separation are
communicated entirely through 1px borders and the contrast between the
gray-900 page background and white surfaces. Do not introduce box-shadows,
glows, or layered drop shadows — borders do the work.

## Shapes

A single border radius governs the entire UI: **4px (`rounded.sm`)** on
buttons, inputs, cards, and containers. The only exception is the toggle
switch, whose track is a full pill (`rounded.full`) with a circular knob.
Never use a radius larger than 4px on rectangular elements.

## Components

All component tokens are defined in the front matter. Key specs and states:

**Buttons** — 32px tall, 4px radius, Inter Semi-Bold 14px, 16px horizontal
padding (8px for icon-only). Icons are 16×16 with an 8px gap, colored to match
the label.

- *Primary:* pink-500 bg / white text → hover pink-400 → disabled gray-700 bg, gray-500 text.
- *Secondary:* white bg / gray-200 text / 1px gray-600 border → hover gray-900 bg → disabled gray-700 bg, gray-400 text.
- *Destructive primary:* red-500 bg / white text → hover red-400.
- *Destructive secondary:* white bg / red-500 text / 1px gray-600 border → hover gray-900 bg.

**Text inputs** — 40px tall, 4px radius, 12px horizontal padding; label is
12px gray-300 with an 8px bottom gap. Required fields append a red-500 `*`.
States: default (1px gray-600), focused (1px gray-300), error (1px red-500 +
red-500 label), disabled (gray-800 bg, gray-500 text).

**Toggle switch** — 36×20 pill track, 14px circular knob inset 3px. OFF:
gray-600 track; ON: pink-500 track; knob is white (gray-600 when disabled).

**Cards / containers** — white bg, 1px gray-700 border, 4px radius, 24px padding.

**Tables** — 32px min row height; white rows with gray-800 hover; header text is
gray-200 Semi-Bold 12px; cell padding 8px 12px; 1px gray-700 row divider.

**Links** — pink-400 text, underline on hover, no underline at rest.

**Dividers** — 1px gray-700 line, no border.

**Icons** — 16×16 inside buttons, ~20×20 standalone; static icons gray-300,
clickable icons match their text, destructive icons red-500.

Full CSS and React implementations for every component live in
[`references/components.md`](references/components.md).

## Do's and Don'ts

**Do**

- ✅ Use the Inter font family exclusively.
- ✅ Use a 4px border radius consistently (pill only for the toggle).
- ✅ Use pink-500 (#D53F8C) for the single primary action.
- ✅ Use red-500 (#D12D50) only for destructive actions and errors.
- ✅ Maintain 24px container padding.
- ✅ Use gray-200 for headings and gray-100 for body text.
- ✅ Provide a visible focus state (2px pink-500 outline, 2px offset).

**Don't**

- ❌ Mix font families.
- ❌ Use shadows — the system is flat; separate with borders.
- ❌ Use a radius larger than 4px on rectangular elements.
- ❌ Use colors outside the defined palette.
- ❌ Make buttons shorter than 32px.
- ❌ Use text smaller than 12px.
