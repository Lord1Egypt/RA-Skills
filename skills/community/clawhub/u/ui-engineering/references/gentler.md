---
name: ui-spec-gentler
description: Detailed engineering specification for implementing "Gentler Streak Style" (Organic, Compassionate, Soft Shapes).
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Gentler Streak

## 1. Engineering Context
**Mental Model**: "The Soft Path".
Health apps are usually aggressive (rings, numbers). Gentler uses blobs, waves, and organic paths to show that fitness is non-linear. It is compassionate software.

**Key Traits**:
- **Organic Shapes**: No sharp corners. Everything is `rounded-3xl` or amorphous blobs.
- **The Path**: A central visualization that is a flowing river/wave, not a bar chart.
- **Mascot**: Use of friendly, non-threatening characters (Yorhart).

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS.
- **Canvas**: `D3.js` or `VisX` (To draw the smooth activity path).
- **Animation**: `Lottie` (For the mascot animations).

## 3. Design Tokens

### 3.1 Colors (Compassion)
- **Bg**: `#FFF3E0` (Warm Peach) or `#F2F2F7` (Soft Gray).
- **Heart Range**: `#FF9F0A` (Orange - High), `#30D158` (Green - Optimal), `#0A84FF` (Blue - Rest).
- **Card**: White with low opacity `bg-white/80`.

### 3.2 Typography
- **Font**: `Nunito` or `Rounded Mplus 1c`.
- **Style**: Extremely round, approachable, informal.

## 4. Component Recipes

### The "Activity Path"
- **Visual**: A spline area chart (Streamgraph).
- **Gradient**: Vertical gradient indicating intensity zones.
- **Data Point**: A "You are here" dot that floats on the wave.

### The "Insight Card"
- **Bg**: Pastel colors (Soft Orange: `#FFEFD5`).
- **Icon**: 3D soft illustration.
- **Text**: "Take it easy today." (Empathetic copy).

### The "Action Blob"
- **Shape**: `rounded-full`.
- **Bg**: White.
- **Label**: Large emoji + Text label.
- **Interaction**: Squishes on press (`scale-90`).

## 5. Interaction Patterns
- **Haptic Delight**: very subtle ticks when moving along the path.
- **Language**: Use first-person, encouraging language ("You're doing great", "Rest is productive").
