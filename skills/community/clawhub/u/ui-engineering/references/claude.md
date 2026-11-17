---
name: ui-spec-claude
description: Detailed engineering specification for implementing Claude's (Anthropic) warm, human-centric, serif-based design system.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Claude (Anthropic)

## 1. Engineering Context
**Mental Model**: "The Warm Paper".
Claude's design is the antithesis of the cold, blue/black tech aesthetic. It feels like a high-quality printed book or a warm letter. It uses serif fonts, earthy tones (Sand, Stone), and soft rounded corners to convey safety, helpfulness, and humanity.

**Key Traits**:
- **Serif Headings**: A distinct move away from the all-sans trend.
- **Warmth**: No pure white (`#FFF`) backgrounds. Everything is slightly tinted (Sand).
- **Restraint**: Minimal shadows, minimal layers.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS.
- **Typography**: Explicit loading of high-quality Serif web fonts.
- **Markdown**: `react-markdown` with extensive typography plugin customization to match the "prose" feel.

## 3. Design Tokens

### 3.1 Colors (Earthy Tones)
- **Bg Page**: `#FAF9F6` (Alabaster / Warm White).
- **Bg Surface**: `#FFFFFF` (Cards).
- **Text Main**: `#141413` (Near Black, but warmer).
- **Text Secondary**: `#605F5B` (Stone Gray).
- **Accent Primary**: `#D97757` (Terracotta / Burnt Orange).
- **Accent Secondary**: `#D4C5B0` (Biscuit).
- **Border**: `#E6E4DD` (Warm Gray).

### 3.2 Typography
- **Headings**: `Tiémpos Headline` or `Lora` or `Merriweather`.
- **Body**: `Söhne` or `Inter` (Clean Sans for readability).
- **Style**:
    - **H1**: Serif, Font Weight 400 (Regular), Tight tracking.
    - **Body**: Sans, Line Height 1.6 (Relaxed).

## 4. Component Recipes

### The "Conversation Bubble" (Human vs AI)
- **User**: `bg-[#F0EEE6]` (Warm Gray), `text-[#141413]`. Rounded-[8px].
- **Claude**: `bg-transparent`. Serif H2/H3s inside.

### The "Artifact" (Side Panel)
- **Bg**: `bg-white` border-l `border-[#E6E4DD]`.
- **Shadow**: `shadow-xl` (Soft, spread out).
- **Header**: `bg-[#FAF9F6] border-b border-[#E6E4DD]`.

### The "Input Area"
- **Container**: `bg-white border border-[#E6E4DD] rounded-[12px] shadow-sm`.
- **Focus**: `ring-2 ring-[#D97757]/20 border-[#D97757]`.
- **Icon**: Thin, refined stroke icons.

## 5. Interaction Patterns
- **Gentle Fade**: Transitions are slow and soft (`duration-300 ease-in-out`).
- **Streaming**: Text appears smoothly, but without the "retro" cursor flashing of OpenAI. It just flows.
