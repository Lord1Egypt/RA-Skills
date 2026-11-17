---
name: ui-spec-rauno
description: Detailed engineering specification for implementing Rauno Freiberg's "Invisible Craft" aesthetic (Physics & Flow).
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Rauno Freiberg (Invisible Craft)

## 1. Engineering Context
**Mental Model**: "Digital Physics".
This style treats UI elements as physical objects with mass, friction, and inertia. It is not about "animating" (A to B); it is about "simulating". The user's cursor is a force. The UI reacts to that force.

**Key Traits**:
- **Rubber Banding**: Elements stretch when pulled.
- **Inertia**: Scrolling and dragging have momentum.
- **Invisible Details**: Highlights that follow the cursor, borders that glow only near the mouse.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS + CSS Modules.
- **Physics**: `framer-motion` (Springs are mandatory) or `react-spring`.
- **Gesture**: `use-gesture` (for dragging logic).
- **Canvas**: Often uses small Canvas elements for performant particle/ray tracing effects.

## 3. Design Tokens

### 3.1 Colors (Deep & Subtle)
- **Bg**: `#000000` or very deep gray `#0A0A0A`.
- **Border**: `rgba(255,255,255,0.08)` (Barely visible).
- **Glow**: `rgba(255,255,255,0.4)` (Only appears on interaction).
- **Text**: Sub/antialiased gray `#888`. High contrast only for active data.

### 3.2 Typography
- **Font**: `Inter` featuring `cv05` (Humanist geometric) or custom variable fonts.
- **Size**: Small, precise (13px - 14px).
- **Tracking**: Slightly tight `tracking-[-0.01em]`.

## 4. Component Recipes

### The "Magnetic Button"
A button that pulls towards the cursor when you get close.
- **Logic**: Calculate distance between cursor and button center. Map to x/y translate.
- **Spring**: `stiffness: 150, damping: 15`.
- **Visual**: Minimal text, no background until hover.

### The "Spotlight Card"
- **Bg**: Black.
- **Overlay**: A radial gradient that tracks `clientX/Y` on `mousemove`.
- **Border**: Use `mask-image` to make the border visible *only* under the spotlight gradient.

### The "Fluid Slider"
- **Feel**: The handle should have "weight". If you drag fast and let go, it might overshoot slightly (if configured for playfulness) or snap instantly (if for precision).
- **Sound**: Subtle tick sound on value change.

## 5. Interaction Patterns
- **Gesture-driven**: Swipe to archive, pull to refresh.
- **Persistence**: Remembers scroll position and state perfectly.
- **No Layout Shift**: Dimensions are calculated ahead of time.
