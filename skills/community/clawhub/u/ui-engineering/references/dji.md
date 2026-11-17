---
name: ui-spec-dji
description: Detailed engineering specification for implementing DJI's industrial, futuristic, and precise design system.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: DJI

## 1. Engineering Context
**Mental Model**: "The Cockpit".
DJI's design is about control. It is precise, high-contrast, and technical. The UI often mimics a Head-Up Display (HUD). Typography is small, uppercase, and monospaced. Backgrounds are dark gray or semi-transparent black.

**Key Traits**:
- **Technicality**: Lines, crosshairs, and data overlays.
- **Monochrome**: Shades of gray dominate to let the camera feed shine.
- **Sharpness**: 90-degree corners or very slight bevels.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS
- **Visualization**: `D3.js` or `Recharts` (Customized for HUD look).
- **Icons**: Thin-stroke SVG icons (1px stroke).

## 3. Design Tokens

### 3.1 Colors (Technical Gray)
- **Bg Dark**: `#1D1D1F` (Main UI background).
- **Bg Panel**: `rgba(0,0,0,0.6)` (Overlay panels).
- **Brand Blue**: `#0070D5` (Active state / Primary action).
- **Text**: `#E5E5E5` (Off-white softness).
- **Warning**: `#F5A623` (Critical flight info).

### 3.2 Typography
- **Font**: `DJI Sans` (Custom) -> `Roboto` -> `DIN`.
- **Style**:
    - **Labels**: `font-size: 10px`, `text-transform: uppercase`, `letter-spacing: 0.1em`.
    - **Values**: Monospaced numbers for changing data.

## 4. Component Recipes

### The "Status OSD" (On Screen Display)
- **Layout**: Top bar, transparent background.
- **Item**: icon + text value. `gap-2`.
- **Font**: `text-xs font-mono text-white shadow-sm` (Shadow ensures readability over video).

### The "Setting Toggle"
- **Container**: `bg-[#333]` rounded-[2px].
- **State**:
    - Off: `text-gray-400`
    - On: `bg-[#0070D5] text-white`
- **Shape**: Rectangular, sharp corners.

### The "Telemetry Graph"
- **Stroke**: 1px line width.
- **Fill**: Linear gradient from `rgba(0,112,213,0.3)` to transparent.
- **Grid**: Dotted lines (`border-dotted`).

## 5. Interaction Patterns
- **Immediate**: No bounce. Interactions are mechanical switch-like.
- **Sound**: Standard "beep" or "click" sounds on interaction (like camera shutter).
- **Warning**: Flashing Red/Yellow overlay for critical alerts.
