---
name: ui-spec-notion
description: Detailed engineering specification for implementing Notion's document-based, canvas-style design system.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Notion

## 1. Engineering Context
**Mental Model**: "The Endless Canvas".
Notion is a tool for thought. The UI mimics a clean piece of paper. Elements are not "contained" in boxes; they float on the page. Structure comes from whitespace, not borders.

**Key Traits**:
- **Emoji**: First-class citizen for identification.
- **Pastel**: Background highlights are soft pastels.
- **Serif/Sans Mix**: Using Serif for friendly headings.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS.
- **Editor**: Tiptap or ProseMirror (if building text editing).
- **Icons**: Lucide (functional) + Apple Emojis (content).

## 3. Design Tokens

### 3.1 Colors (Pastel Palette)
Notion doesn't use strong block colors. It uses text colors and background highlights.
- **Text Default**: `#37352F` (Not black. A warm dark gray).
- **Text Gray**: `#9B9A97`
- **Bg Default**: `#FFFFFF`
- **Bg Hover**: `#F1F1EF` (Key interaction color).
- **Highlights**:
    - Red: `#FFEBE9` (bg) / `#D44C47` (text)
    - Blue: `#E6F3F7` (bg) / `#337EA9` (text)
    - Yellow: `#FBF3DB` (bg) / `#CB912F` (text)

### 3.2 Typography
- **Headings**: `Inter` (Sans) or `Lyon-Text` (Serif).
- **Body**: `Inter`, `line-height: 1.5`, `color: #37352F`.
- **Mono**: `iA Writer Mono` or `SF Mono`.

## 4. Component Recipes

### The "Block Handle" (`::`)
The draggable handle that appears on hover.
- **Visibility**: `opacity-0 group-hover:opacity-100`
- **Icon**: Six-dot grid icon.
- **Color**: `#D3D1CB` hover `#37352F`.

### The "Select Menu"
- **Bg**: `bg-white`
- **Shadow**: `shadow-lg border border-gray-200`
- **Item**: `px-3 py-1.5 hover:bg-[#F1F1EF] rounded-[3px]`

### The "Callout Block"
- **Bg**: `bg-[#F1F1EF]` (Default gray bg).
- **Icon**: Left aligned Emoji.
- **Corner**: `rounded-[4px]`.
- **Padding**: `p-4`.

## 5. Interaction Patterns
- **Hover Reveal**: Many UI controls (delete, move, add) are hidden until hover to reduce cognitive load.
- **Slash Command**: The `/` key trigger is the primary interaction model.
