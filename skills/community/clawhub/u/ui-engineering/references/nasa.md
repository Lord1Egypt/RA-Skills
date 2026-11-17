---
name: ui-spec-nasa
description: Detailed engineering specification for implementing NASA's "Public Science" aesthetic (Worm, USWDS, Space).
license: Public domain / Fair use for reference
---

# UI Engineering Spec: NASA

## 1. Engineering Context
**Mental Model**: "Public Future".
NASA balances two identities: The Government Agency (Accessibility, Clarity, USWDS) and The Frontier (Space, The Worm logo, Heroism). The design is accessible but awe-inspiring.

**Key Traits**:
- **The Worm**: The retro-futuristic red logo is the soul.
- **Dark Mode Default**: Space is dark. High quality imagery requires black backgrounds.
- **Data Density**: Mission control dashboards are dense but legible.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS.
- **System**: USWDS (United States Web Design System) tokens for accessibility.
- **Font**: `Inter` or `Helvetica Neue` (Clean, neutral). `Nasalization` (Optional for display).

## 3. Design Tokens

### 3.1 Colors (Earth & Space)
- **Bg**: `#000000` (Space) or `#1B1B1B` (Deep Grey).
- **Text**: `#FFFFFF`.
- **Worm Red**: `#E31937` (The iconic red).
- **Earth Blue**: `#0B3D91`.
- **Star White**: `#F1F1F1`.

### 3.2 Typography
- **Font**: `Helvetica Neue`.
- **Headings**: `Inter` Bold.
- **Numbers**: Monospace `DM Mono` for countdowns and telemetry.

## 4. Component Recipes

### The "Mission Countdown"
- **Container**: `bg-black border border-gray-800`.
- **Digits**: Huge Mono font (`text-5xl`).
- **Labels**: Tiny Uppercase (`T-MINUS`).
- **Status**: Glowing Green/Red dot (`animate-pulse`).

### The "Image of the Day"
- **Card**: Full width.
- **Image**: High-res, no overlay.
- **Caption**: Bottom left, subtle gradient overlay.
- **Download**: "Original Quality" link (Data is public domain).

### The "Worm Header"
- **Logo**: The "NASA" worm logo in Red.
- **Nav**: Simple White text, uppercase, tracking-wide.

## 5. Interaction Patterns
- **Zoom**: Deep zoom into high-res nebula images (OpenSeaDragon or similar).
- **Timeline**: Horizontal scrolling mission timelines.
