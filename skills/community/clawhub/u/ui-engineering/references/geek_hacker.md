---
name: ui-spec-geek-hacker
description: Detailed engineering specification for implementing "Gwern / Tufte Style" (Information Density, Sidenotes, Raw).
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Hacker Minimalist

## 1. Engineering Context
**Mental Model**: "The Research Paper".
Optimized for reading 10,000 words. No sticky headers, no popups. Just pure typography and hyper-functional links. Inspired by Edward Tufte and Gwern.net.

**Key Traits**:
- **Sidenotes**: Notes live in the right margin, not the footer.
- **Semantic Zoom**: Hovering a link shows a preview of that target (Wikipedia style).
- **Serif Dominance**: High-quality book fonts.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS + `prose` plugin.
- **Layout**: CSS Grid (Main column + Sidebar column).
- **Font**: `Equity`, `Charter`, or `Crimson Text`.

## 3. Design Tokens

### 3.1 Colors (Paper)
- **Bg**: `#FFFAF0` (Floral White) or `#FBFBFB`.
- **Text**: `#111111` (Near Black).
- **Link**: `#AC0000` (Crimson) or `#0000EE` (Standard Blue).
- **Visited**: `#551A8B`. (Respecting visited state is key).

### 3.2 Typography
- **Font**: `Crimson Pro` or `Source Serif Pro`.
- **Measure**: 65-75 characters per line (max-width `prose`).
- **Sidenote**: Smaller size (`0.8rem`), sitting in the `col-start-2`.

## 4. Component Recipes

### The "Sidenote"
- **Desktop**: `absolute right-[-200px] w-[180px] text-sm text-gray-600`.
- **Mobile**: Hidden behind a toggle or converted to endnote.
- **Symbol**: A superscript number in text corresponding to the note.

### The "Definition Link"
- **Style**: Dashed underline.
- **Hover**: Shows a tooltip with the definition.

### The "Dropcap"
- **Visual**: First letter of the article is huge (`text-5xl float-left mr-2`).
- **Font**: Blackletter or ornate serif.

## 5. Interaction Patterns
- **No distractions**: No "Subscribe" modals.
- **Progress**: A subtle reading position indicator (optional).
- **Link Previews**: Essential for the "Wiki" feel.
