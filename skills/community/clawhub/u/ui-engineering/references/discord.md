---
name: ui-spec-discord
description: Detailed engineering specification for implementing Discord's cozy, community-focused design system.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Discord

## 1. Engineering Context
**Mental Model**: "Digital Living Room".
Discord is dense but cozy. It manages multiple columns of information (Serves -> Channels -> Chat -> Members) without feeling corporate. It achieves this through soft gray backgrounds and rounded, playful shapes.

**Key Traits**:
- **Cozy Layout**: Compact lists with 8px paddings.
- **Theme**: Customizable, but the default Dark Theme is iconic.
- **Avatars**: Circular, everywhere.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS
- **Virtualization**: `react-virtuality` (Chat lists are heavy).
- **Icons**: FaT (FontAwesome-ish) thick filled icons or Heroicons Solid.

## 3. Design Tokens

### 3.1 Colors (The Gray Spectrum)
Discord has a very specific hierarchy of grays.
- **Bg Server List**: `#202225` (Darkest)
- **Bg Sidebar**: `#2F3136`
- **Bg Chat**: `#36393F`
- **Bg Header**: `#36393F` with `border-b border-[#202225]`
- **Brand**: `#5865F2` (Blurple)
- **Green**: `#3BA55C` (Online)

### 3.2 Typography
- **Font**: `gg sans` (Custom) -> `Uni Sans` -> `Inter`.
- **Weight**: Bold headings, Medium UI text.
- **Sizes**: `16px` (Chat message), `14px` (Sidebar channel).

## 4. Component Recipes

### The "Server Icon" (Pill Navigation)
- **Container**: `w-[48px] h-[48px] rounded-[50%] bg-[#36393F] transition-all duration-200`
- **Hover**: `hover:rounded-[16px] hover:bg-[#5865F2]` (Circle to Squircle transition).
- **Active Indicator**: White pill on the left side (`h-[8px] hover:h-[20px] active:h-[40px]`).

### The "Channel Item"
- **Layout**: `flex items-center px-2 py-1 mx-2 rounded-[4px] text-gray-400 hover:bg-[#393C43] hover:text-gray-200`
- **Active**: `bg-[#393C43] text-white`
- **Icon**: Hash `#` icon (`text-gray-500`).

### The "Chat Bubble" (Cozy Mode)
- **Hover**: `hover:bg-[#32353B]` (The whole message row highlights).
- **Time**: Shows on hover only (in compact mode) or inline gray text.

## 5. Interaction Patterns
- **Modals**: Scale-up bounce animation (`scale-0` to `scale-100` with spring).
- **Popouts**: User profiles pop out from the side or avatar with a dark background and colored banner.
