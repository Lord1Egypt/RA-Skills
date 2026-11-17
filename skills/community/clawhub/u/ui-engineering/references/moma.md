---
name: ui-spec-moma
description: Detailed engineering specification for implementing MoMA's (Museum of Modern Art) avant-garde, typographic identity.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: MoMA

## 1. Engineering Context
**Mental Model**: "The White Cube".
MoMA's digital presence mirrors its gallery space. It is a neutral, stark container for art. The "Interface" should essentially disappear, leaving only Type and Art. "Never touch the art" means no overlays, no weird filters on images.

**Key Traits**:
- **MoMA Sans**: The custom geometric sans is the identity.
- **Asymmetry**: Layouts are rarely centered. They use tension.
- **Big Type**: Headings are often massive and cut off (clipped) or tightly stacked.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS.
- **Grid**: CSS Grid (Critical for the "Masonry" feel).
- **Font**: `MoMA Sans` or `Franklin Gothic` (The classic alternative).

## 3. Design Tokens

### 3.1 Colors (Gallery)
- **Bg**: `#FFFFFF` (White) or `#000000` (Black).
- **Text**: `#000000` / `#FFFFFF`.
- **Accent**: None. The art provides the color.
- **Highlight**: Vivid yellow/pink only for "Membership" promos.

### 3.2 Typography
- **Font**: `MoMA Sans` (Geometric, wide).
- **Style**: All Caps for Navigation.
- **Scale**: `text-6xl` for headlines. `text-lg` for body text (Gallery labels).

## 4. Component Recipes

### The "Exhibition Poster" (Digital)
- **Layout**: Split screen.
- **Left**: Massive Typography, strictly grid aligned.
- **Right**: High-res Art, full bleed.
- **Scroll**: The text sticks, the art scrolls.

### The "Events Calendar"
- **List**: Brutalist distinct lines (`border-t-2 border-black`).
- **Date**: Huge numbers. `24` OCT.
- **Hover**: Inverts colors (Black bg, White text).

### The "Audio Guide"
- **Ui**: Minimal play button (Circle).
- **Progress**: A single thin line.
- **Context**: Text description below.

## 5. Interaction Patterns
- **Hover Reveal**: Hovering a text title reveals the artwork image behind it (z-index swap).
- **Snap**: Scroll snapping for "Rooms" or "Exhibitions".
