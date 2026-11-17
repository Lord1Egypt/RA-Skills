---
name: ui-spec-paco
description: Detailed engineering specification for implementing Paco Coursey's "Radical Minimalism" aesthetic (Speed & Reduction).
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Paco Coursey (Radical Minimalism)

## 1. Engineering Context
**Mental Model**: "Zero Latency".
This style removes everything that isn't content. It is the visual equivalent of `O(1)` complexity. It prefers instant state changes over long transitions. It uses high-contrast monochrome to signal "Pro Tool".

**Key Traits**:
- **Reduction**: If a border can be removed, remove it. If a label isn't needed, delete it.
- **Speed**: Optimistic UI updates. 0ms delay.
- **Blur**: Heavy use of `backdrop-filter` to create "materials" without adding lines.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS (Utility first).
- **Components**: Radix UI (Headless, accessible base).
- **Icons**: Vercel/Geist Icons or custom SVG paths (1.5px stroke).

## 3. Design Tokens

### 3.1 Colors (Monochrome with Intent)
- **Bg**: `#FFFFFF` (Light) / `#000000` (Dark).
- **Text Main**: `#000000` / `#EDEDED`.
- **Text Sub**: `#888888` (Medium Gray).
- **Text Tertiary**: `#D4D4D4` (Light Gray - barely visible).
- **Selection**: `#0070F3` (Electric Blue) or `#F81CE5` (Magenta) - Only used for focus.

### 3.2 Typography
- **Font**: `Geist Sans` or `Inter`.
- **Weight**: Heavy reliance on `500` (Medium) for text, `400` (Regular) for body.
- **Numbers**: `font-variant-numeric: tabular-nums` (Alignment is god).

## 4. Component Recipes

### The "Command K" (CMDK)
The signature component.
- **Overlay**: `bg-black/20 backdrop-blur-[2px]`.
- **Dialog**: `bg-white dark:bg-[#0A0A0A] border border-gray-200 dark:border-gray-800 shadow-2xl rounded-xl`.
- **Input**: No border, massive focus ring removal.

### The "Toast" (Notification)
- **Position**: Bottom right.
- **Shape**: Small, black capsule.
- **Animation**: Slide up + scale (`y: 10 -> 0`, `scale: 0.95 -> 1`).
- **Content**: Concise text. "Copied." "Saved."

### The "Detail Hover"
- **Default**: Item is just text.
- **Hover**: Gray background `bg-gray-100 dark:bg-gray-900` rounded-[4px] appears instantly behind the text.

## 5. Interaction Patterns
- **Keyboard First**: Every UI action must be bindable.
- **Focus Rings**: Custom CSS focus rings (`ring-2 ring-blue-500 ring-offset-2`).
- **Tabular Data**: Lists start simple, reveal actions on hover.
