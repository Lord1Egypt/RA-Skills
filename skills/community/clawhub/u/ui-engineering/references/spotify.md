---
name: ui-spec-spotify
description: Detailed engineering specification for implementing Spotify's dark-mode, energetic design system.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Spotify

## 1. Engineering Context
**Mental Model**: "The Stage".
Spotify is a dark theater. The content (Album Art) provides the color. The UI recedes into the background (Black/Gray). It uses opacity layers heavily to creating hierarchy without adding new colors.

**Key Traits**:
- **Dark Mode**: Native, unchanging dark mode.
- **Grids**: Album art grids.
- **Gradients**: Backgrounds adapt to the dominant color of the current album art.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS.
- **Color Extraction**: `colorthief` or `fast-average-color` (to generate background gradients from images).
- **Icons**: Enclose (Spotify's custom SVG set, thick strokes).

## 3. Design Tokens

### 3.1 Colors
- **Bg Page**: `#121212` (Not #000).
- **Bg Card**: `#181818` -> Hover `#282828`.
- **Brand**: `#1ED760` (Spotify Green - Vivid).
- **Text Main**: `#FFFFFF`
- **Text Sub**: `#B3B3B3` (Light Gray).

### 3.2 Typography
- **Font**: `Circular Std` / `Gotham` / `Montserrat`.
- **Style**: Geometric Sans. Large headings are `font-weight: 900`.

### 3.3 Shapes
- **Buttons**: `rounded-full` (Capsule).
- **Images**: `rounded-none` (Albums) or `rounded-full` (Artists).
- **Cards**: `rounded-[6px]`.

## 4. Component Recipes

### The "Play Button" (Green FAB)
The most iconic element.
- **Size**: `w-[56px] h-[56px]`
- **Shape**: `rounded-full`
- **Bg**: `bg-[#1ED760] hover:scale-105 hover:bg-[#1fdf64]`
- **Icon**: Black Triangle (filled).
- **Shadow**: `shadow-xl`.

### The "Music Card"
- **Container**: `bg-[#181818] p-4 rounded-md hover:bg-[#282828] transition-colors duration-300 ease-out group`
- **Image**: `w-full aspect-square shadow-lg mb-4 relative`
- **Play Overlay**: Green play button appears from bottom-right on group hover (`opacity-0 group-hover:opacity-100 translate-y-2 group-hover:translate-y-0`).

### The "Dynamic Gradient Background"
- **CSS**: `background: linear-gradient(to bottom, var(--extracted-color), #121212 400px)`
- **Placement**: Fixed at top, behind scrollable content.

## 5. Interaction Patterns
- **Sticky Header**: Opacity changes from 0 to 1 based on scroll position.
- **Lists**: Alternate row colors are NOT used. Alignment and whitespace define rows.
