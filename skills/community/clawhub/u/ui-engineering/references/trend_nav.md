---
name: ui-spec-trend-nav
description: Detailed engineering specification for implementing "Neon Dashboard" trend (Cosmin Capitanu style, Dark, Analytics).
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Neon Dashboard

## 1. Engineering Context
**Mental Model**: "The Cockpit".
This style (popularized by designers like Cosmin Capitanu) is the "Dribbble Dashboard". It is almost always Dark Mode. It features deep shadows, floating cards, and extremely vibrant (neon) charts. It looks like a spaceship control panel.

**Key Traits**:
- **Deep Depth**: Cards have distinct drop shadows even in dark mode (`shadow-black/50`).
- **Vibrant Data**: Charts use gradients (purple to pink), not solid colors.
- **Sidebar**: Usually a semi-transparent or distinct dark column with glowing active states.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS.
- **Charts**: `Recharts` or `Nivo` (Must support gradient fills).
- **Icons**: `Feather Icons` with custom glow filters.

## 3. Design Tokens

### 3.1 Colors (Cyberpunk Admin)
- **Bg**: `#151521` (Deep Navy/Black).
- **Surface**: `#1E1E2D` (Lighter Navy).
- **Text**: `#FFFFFF`.
- **Text Muted**: `#92929F`.
- **Accent**: `#F64E60` (Red Neon), `#0BB783` (Green Neon), `#8950FC` (Purple Neon).

### 3.2 Typography
- **Font**: `Poppins` or `DM Sans` (Geometric).
- **Numbers**: Monospaced for data tables.

## 4. Component Recipes

### The "Neon Chart"
- **Line**: Not just a line, but a thick stroke with a drop shadow of its own color (`filter: drop-shadow(0 0 10px #8950FC)`).
- **Area**: Gradient fill fade to transparent.

### The "Status Card"
- **Bg**: `#1E1E2D`.
- **Icon**: `bg-[#8950FC]/20 text-[#8950FC] p-3 rounded-lg`.
- **Value**: White, Bold.
- **Indicator**: Tiny glowing dot.

### The "Active Sidebar Item"
- **Bg**: Gradient from left (`bg-gradient-to-r from-[#8950FC]/20 to-transparent`).
- **Border**: Left border 3px solid `#8950FC`.
- **Text**: White.

## 5. Interaction Patterns
- **Hover**: Table rows highlight (`bg-white/5`).
- **Loading**: Pulse skeletons are dark gray (`bg-white/10`).
