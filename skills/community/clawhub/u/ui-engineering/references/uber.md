---
name: ui-spec-uber
description: Detailed engineering specification for implementing Uber's "Base Web" design system (Movement, Maps, Black/White).
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Uber

## 1. Engineering Context
**Mental Model**: "The Logistics Map".
Uber's design is purely functional. It facilitates movement. It is strict, high-contrast, and deeply integrated with map interfaces. It avoids decoration. The "Safety Blue" is the only color that matters besides Black/White.

**Key Traits**:
- **Move Sans**: The custom font is geometric but friendly.
- **Map Layer**: The UI is often a "drawer" floating over a map.
- **Efficiency**: Buttons are large, touch targets are massive.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS (or Uber's Styletron if strictly adhering, but Tailwind is preferred for this output).
- **Map**: `Mapbox GL JS` or `Google Maps API` (Dark mode customized).
- **Drawer**: `react-spring-bottom-sheet` (Critical for the mobile feel).

## 3. Design Tokens

### 3.1 Colors (Movement)
- **Bg**: `#FFFFFF` (Day) / `#000000` (Night - True Black).
- **Text**: `#000000` / `#FFFFFF`.
- **Primary**: `#000000` (The "Black" car).
- **Secondary**: `#F6F6F6` (Gray background).
- **Safety Blue**: `#276EF1` (Links, Info, Trust).

### 3.2 Typography
- **Font**: `Uber Move` (Proprietary) or `Inter` / `Gellix` (Close alternatives).
- **Weight**: Bold headings, Medium body.
- **Size**: Large. `18px` body text is common for readability in motion.

## 4. Component Recipes

### The "Floating Panel" (Drawer)
- **Position**: Fixed bottom (Mobile) or Top Left float (Desktop).
- **Shadow**: `shadow-[0_-4px_16px_rgba(0,0,0,0.08)]`.
- **Corner**: `rounded-t-xl` (Mobile) or Square (Desktop).

### The "Ride Option"
- **Layout**: Flex row.
- **Icon**: Car illustration (Right profile).
- **Text**: "UberX" (Bold) + Price (Right aligned).
- **Sub**: "4 min away" (Gray).
- **Selection**: Thick black border on select.

### The "Big Input"
- **Bg**: `#F6F6F6`.
- **Border**: None (until focus).
- **Height**: `56px` (Tall).
- **Text**: `text-lg`.
- **Icon**: Square black dot (Pickup) / Square circle (Dropoff).

## 5. Interaction Patterns
- **Map State**: UI elements fade out when map is interacted with.
- **Route Line**: The "Pulse" animation on the route line represents waiting time.
