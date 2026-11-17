---
name: ui-spec-geek-tui
description: Detailed engineering specification for implementing "Modern TUI Style" (Charm.sh, CLI, Terminal).
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Modern TUI

## 1. Engineering Context
**Mental Model**: "The Beautiful Terminal".
This is not "old DOS". It is the "Modern CLI" aesthetic popularized by Charm.sh. It uses true-color (16m colors), beautiful meshes of gradient text, and rounded "bubbles" inside a terminal window.

**Key Traits**:
- **Monospace**: *Everything* is monospace. Even the headers.
- **Black Background**: `#000000` or extremely dark purple/gray.
- **Gradient Text**: Text often has a horizontal gradient (Pink to Purple).

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS.
- **Font**: `JetBrains Mono` or `Fira Code` (with ligatures).
- **Icons**: `Nerd Fonts` (The standard for terminal icons).

## 3. Design Tokens

### 3.1 Colors (ANSI + Neon)
- **Bg**: `#131313` (Soft Black).
- **Selection**: `#262626`.
- **Charm Pink**: `#F25D94`.
- **Charm Purple**: `#A550DF`.
- **Charm Cyan**: `#61E2FF`.

### 3.2 Typography
- **Font**: `JetBrains Mono` (The gold standard).
- **Weight**: Varies, but usually `Regular` or `Bold`. `ExtraLight` looks bad in terminal.
- **Line Height**: `relaxed` (Terminal needs breathing room).

## 4. Component Recipes

### The "Bubble"
- **Container**: `border border-gray-700 rounded-xl p-4 bg-gray-900/50`.
- **Title**: `text-xs uppercase tracking-widest text-gray-500 mb-2`.
- **Content**: Monospace text.

### The "Gradient Command"
- **Visual**: `> npm install` where the text has `bg-clip-text text-transparent bg-gradient-to-r from-pink-500 to-purple-500`.
- **Cursor**: A solid block `|` or `_` that blinks exactly like a terminal.

### The "Help Footer"
- **Position**: Sticky bottom.
- **Style**: Flex row of `Key` + `Description`.
- **Key**: `text-gray-400 font-bold`. "ENTER".
- **Desc**: `text-gray-600`. "select".

## 5. Interaction Patterns
- **Keyboard Only**: Visible focus states (`ring-2 ring-purple-500`) are mandatory. Mouse is secondary.
- **Output Stream**: Content should appear line-by-line (`typewriter` effect).
