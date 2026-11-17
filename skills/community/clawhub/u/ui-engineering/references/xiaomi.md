---
name: ui-spec-xiaomi
description: Detailed engineering specification for implementing Xiaomi's HyperOS "Alive Design" aesthetic.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Xiaomi (HyperOS)

## 1. Engineering Context
**Mental Model**: "Organic Elasticity".
HyperOS is designed to feel alive. It rejects mechanical stiffness. The key is **G2 Curvature** (Continuous Curvature) which looks softer than standard rounded corners, and **Elastic Animation** (things bounce and stretch).

**Key Traits**:
- **G2 Squircles**: Smooth corners everywhere.
- **Blur**: "Mi Blur" - heavy, multicolored mesh blurs.
- **Magazine Layout**: deeply editorial typography scaling.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS
- **Shape**: Custom SVG Clip-paths for G2 Squircles (CSS border-radius is G1).
- **Animation**: `react-spring` (for that elastic feel).

## 3. Design Tokens

### 3.1 Colors (Nature Oriented)
- **Highlight**: `#FF6900` (Mi Orange).
- **Green**: `#38F66E` (Nature).
- **Blue**: `#3D86F5` (Ocean).
- **Bg**: `#F2F2F2` (Light Gray) or `#000000` (OLED Black).
- **Card**: `#FFFFFF` (Light) or `#1C1C1C` (Dark).

### 3.2 Typography
- **Font**: `MiSans` (Global).
- **Structure**: Complex weight variation. Headlines are thin/light (`300`), data is heavy (`600`).
- **Feature**: Supports very large font sizes for headers (48px+).

## 4. Component Recipes

### The "Control Center Widget"
- **Shape**: G2 Squircle (`rounded-[24px]` approximation).
- **Bg**: `bg-white/10 backdrop-blur-xl` (Glass).
- **Active**: `bg-[#3D86F5] text-white` (Solid color when on).
- **Slider**: Thick, vertical slider bars.

### The "Magazine Header"
- **Layout**: Large title, left aligned, lots of whitespace.
- **Font**: `MiSans` Light weight, huge size.
- **Subtitle**: Small gray text with a vertical divider bar.

### The "Bubble Notification"
- **Shape**: Pill with G2 corners.
- **Animation**: Expands from a small dot to full size with an elastic "pop".

## 5. Interaction Patterns
- **Damping**: High damping animations. When you let go of a scroll, it settles gently.
- **Haptics**: (If mobile) Heavy use of vibration feedback on dial/slider changes.
