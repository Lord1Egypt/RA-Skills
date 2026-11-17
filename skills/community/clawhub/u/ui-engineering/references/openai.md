---
name: ui-spec-openai
description: Detailed engineering specification for implementing OpenAI's minimalist, utilitarian design system.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: OpenAI

## 1. Engineering Context (The "Why")
**Mental Model**: "The Blank Page".
OpenAI's design is utilitarian, confident, and radically simple. It disappears to let the "Intelligence" (Text) shine. It avoids decoration. It is Brutalist in its restraint but Modern in its typography.

**Key Traits**:
- **Contrast**: Stark Black and White.
- **Content-First**: Typography is the UI.
- **Structure**: Strict alignment, visible grids, thin borders.

## 2. Tech Stack Recommendations
- **Framework**: React / Next.js
- **Styling**: Tailwind CSS
    - *Why*: Utility-first matches the utilitarian design philosophy.
- **Animation**: CSS Transitions (Minimal)
    - *Why*: Motion should be fast (0.1s - 0.2s) and only for functional feedback.
- **Icons**: Lucide React or Heroicons (Outline)
    - *Configuration*: `strokeWidth={2}` (Slightly bolder stroke to match text).

## 3. Design Tokens (The "Physics")

### 3.1 Colors (Monochromatic)
```css
:root {
  /* Surfaces */
  --bg-page: #FFFFFF;
  --bg-surface: #FFFFFF;
  --bg-sider: #000000; /* For high contrast areas */

  /* Text */
  --text-primary: #000000;
  --text-secondary: #6E6E80; /* Neutral gray */
  --text-tertiary: #ACACBE;

  /* Borders */
  --border-light: #E5E5E5;
  --border-medium: #D1D5DB;

  /* Accents - Use Sparingly! */
  --brand-green: #10A37F; /* ChatGPT Green */
  --brand-purple: #7A64FF;
}

/* Dark Mode (Crucial) */
.dark {
  --bg-page: #343541;
  --text-primary: #FFFFFF;
  --text-secondary: #C5C5D2;
  --border-light: #4D4D4F;
}
```

### 3.2 Typography scales
**Font Family**: `Söhne` (Custom) -> `Inter` -> System Sans.
**Characteristics**: Geometric, legible, slightly humanist.

- **Prose**: `max-width: 65ch` (Optimal reading length).
- **Line-Height**: `1.6` (Generous for reading long stream of text).
- **Sizes**:
    - `text-sm` (14px) for UI controls.
    - `text-base` (16px) for conversation.

### 3.3 Shapes & Borders
- **Corner Radius**: `border-radius: 6px` (Small, tight corners). Not 8px, not 4px. 6px is the sweet spot.
- **Borders**: 1px solid borders are preferred over shadows. Shadows are rare.

## 4. Component Recipes

### The "Prompt Input"
The core interaction point.
- **Container**: `w-full max-w-3xl mx-auto`
- **Style**: `bg-white border border-gray-200 rounded-lg shadow-sm`
- **Shadow**: `shadow-[0_0_10px_rgba(0,0,0,0.05)]` (Very subtle glow)
- **Focus**: `ring-1 ring-black border-black` (High contrast latch)

### The "Action Button"
Minimalist button.
- **Primary**: `bg-[#10A37F] hover:bg-[#1a7f64] text-white rounded-[4px] px-3 py-2 text-sm font-medium transition-colors`
- **Secondary**: `bg-transparent border border-gray-300 text-gray-700 hover:bg-gray-50 rounded-[4px]`

### The "Avatar"
- **Shape**: Square with slightly rounded corners (`rounded-sm` or `rounded-[2px]`). NOT CIRCULAR.
- **Color**: Solid background color with white icon.

## 5. Interaction Patterns
- **Streaming Text**: Implementation of the "Typewriter Effect" is mandatory for AI responses.
- **Cursor**: A blinking block cursor (`|` or `█`) at the end of streaming text adds retro-futurism.
- **Speed**: All interactions are instant. No fade-in for pages.
