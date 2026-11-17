---
name: ui-spec-duolingo
description: Detailed engineering specification for implementing Duolingo's gamified, juicy design system.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Duolingo

## 1. Engineering Context
**Mental Model**: "Juicy Game".
Duolingo is tactile. Buttons feel like physical plastic keys. Everything bounces. There are no sharp corners. It is optimized for dopamine.

**Key Traits**:
- **3D Flat**: Flat design with a "side" to indicate depth.
- **Roundness**: `rounded-2xl` is the minimum.
- **Stroke**: Thick, colored outlines on illustrations.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS
- **Animation**: CSS Keyframes (Bounce) + Lottie (for characters).
- **Sound**: `use-sound` (Audio feedback is UI here).

## 3. Design Tokens

### 3.1 Colors (Candy Shop)
- **Feather Green**: `#58CC02` (Main)
- **Green Shadow**: `#58A700` (The "Dark Side" of the button)
- **Blue**: `#1CB0F6` / Shadow: `#1899D6`
- **Yellow**: `#FFC800` / Shadow: `#EBA500`
- **Red**: `#FF4B4B` / Shadow: `#EA2B2B`
- **Gray**: `#E5E5E5` / Shadow: `#CECECE` (Disabled)

### 3.2 Typography
- **Headings**: `Feather Bold` (Custom bubbly font) -> `Nunito` (Rounded).
- **Body**: `DIN Next Rounded` -> `Nunito`.
- **Color**: `#4B4B4B` (Eel - Dark Gray, never black).

## 4. Component Recipes

### The "Juicy Button" (3D Press)
This is the core interaction.
- **Structure**:
  ```css
  .btn {
    background-color: #58CC02;
    border-bottom: 4px solid #58A700; /* The depth */
    border-radius: 16px;
    color: white;
    text-transform: uppercase;
    font-weight: 800;
    transition: all 0.1s;
  }
  .btn:active {
    transform: translateY(2px);
    border-bottom-width: 0px; /* Pressed down */
    margin-bottom: 2px; /* Maintain layout */
  }
  ```

### The "Progress Bar"
- **Container**: `bg-[#E5E5E5] rounded-full h-[16px]`
- **Fill**: `bg-[#58CC02] rounded-full` with a lighter highlight streak at the top for "gloss".

### The "Card Selection"
- **Default**: `border-2 border-[#E5E5E5] shadow-[0_2px_0_#E5E5E5]`
- **Selected**: `bg-[#E2F7FF] border-[#1CB0F6] border-2 shadow-[0_2px_0_#1CB0F6] text-[#1CB0F6]`

## 5. Interaction Patterns
- **Correct Answer**: Bottom sheet slides up (Green). Sound "Ding".
- **Incorrect Answer**: Bottom sheet slides up (Red). Sound "Bonk".
- **Confetti**: Essential for completing tasks.
