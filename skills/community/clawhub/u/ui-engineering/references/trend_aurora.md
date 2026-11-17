---
name: ui-spec-trend-aurora
description: Detailed engineering specification for implementing "Aurora SaaS" trend (Blur, Gradient, Clean).
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Aurora SaaS

## 1. Engineering Context
**Mental Model**: "The Morning Haze".
This is the dominant "Modern SaaS" look (often overlapping with Linear style but lighter/softer). It features moving colored blurs in the background, frosted glass cards, and crisp sans-serif type. It feels calm and "pro".

**Key Traits**:
- **Background Blurs**: CSS `filter: blur(100px)` on absolute positioned colored blobs.
- **Glass Cards**: `backdrop-filter: blur(10px)` with a white semi-transparent background.
- **Mesh Gradients**: Colors that flow into each other.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS.
- **Canvas**: `Whatamesh` or `Gradient.js` for performant animated mesh gradients.
- **Noise**: SVG noise overlay to reduce color banding.

## 3. Design Tokens

### 3.1 Colors (Ethereal)
- **Bg**: `#FFFFFF`.
- **Blobs**: `#FFD7E4` (Pink), `#E2E2FF` (Periwinkle), `#FFE4C4` (Peach).
- **Text**: `#111827` (Gray 900).
- **Secondary**: `#6B7280` (Gray 500).

### 3.2 Typography
- **Font**: `Inter` or `Plus Jakarta Sans`.
- **Weight**: Bold headings, Regular body.
- **Letter Spacing**: `-0.02em` (Tight).

## 4. Component Recipes

### The "Aurora Hero"
- **Background**: Three animated colored divs (`w-[500px] h-[500px] rounded-full mix-blend-multiply filter blur-[100px]`).
- **Foreground**: Clean H1 and CTA button.
- **Z-Index**: Blurs are `z-0`, content is `z-10`.

### The "Glass Feature Card"
- **Container**: `bg-white/40 backdrop-blur-xl border border-white/20`.
- **Shadow**: `shadow-xl shadow-indigo-100/20`.
- **Content**: Icon + Title + Description.

### The "Glow Button"
- **Bg**: Gradient.
- **Hover**: Shadow that matches the button color (`shadow-lg shadow-blue-500/30`).

## 5. Interaction Patterns
- **Float**: Elements gently bob up and down (`animate-float`).
- **Glew**: Borders that shine on hover (`mask-image` gradient).
