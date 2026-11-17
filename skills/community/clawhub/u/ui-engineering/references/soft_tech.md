---
name: ui-spec-soft-tech
description: Detailed engineering specification for implementing the "Soft Tech" aesthetic (Claymorphism, Neumorphism, Pastels).
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Soft Tech

## 1. Engineering Context
**Mental Model**: "Marshmallow".
Soft Tech is an aesthetic often used in health, meditation, or "friendly" tech apps. It reacts against sharp edges and high contrast. Everything is soft, pillowy, and approachable. It often uses Claymorphism (3D inflated look) or Neumorphism.

**Key Traits**:
- **Super Round**: `rounded-3xl` or `rounded-full` everywhere.
- **Pastels**: High brightness, low saturation colors.
- **Inflated**: Elements look like they have air inside.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS + Custom Shadows.
- **3D**: `Spline` (often paired with 3D soft blobs).
- **Motion**: `react-spring` (Soft, bouncy physics).

## 3. Design Tokens

### 3.1 Colors (Pastel Dream)
- **Bg**: `#F0F4F8` (Cool White) or `#FFF5F5` (Warm White).
- **Surface**: `#FFFFFF`.
- **Primary**: `#8ECAE6` (Soft Blue), `#FFB7B2` (Soft Red), `#B5EAD7` (Soft Green).
- **Text**: `#4A5568` (Soft Blue-Gray), never pure Black.

### 3.2 Typography
- **Font**: `Nunito`, `Quicksand`, or `Varela Round`.
- **Weights**: Rounded terminals are essential.

## 4. Component Recipes

### The "Clay Card" (Claymorphism)
- **Bg**: `bg-white`.
- **Shape**: `rounded-[32px]`.
- **Shadow**: Two internal shadows to create volume + one drop shadow.
  ```css
  box-shadow: 
    inset 10px 10px 20px rgba(255,255,255,0.5), /* Highlight */
    inset -10px -10px 20px rgba(0,0,0,0.05),    /* Shading */
    10px 20px 30px rgba(0,0,0,0.05);            /* Drop */
  ```

### The "Soft Button"
- **Bg**: Pastel color gradient (top-left light, bottom-right dark).
- **Border**: No border.
- **Shadow**: Deep, soft colored shadow (`shadow-blue-200`).

## 5. Interaction Patterns
- **Squish**: Buttons scale down (`scale-95`) on click, like squeezing a foam ball.
- **Float**: Important elements gently float (`animate-bounce` slow) in place.
