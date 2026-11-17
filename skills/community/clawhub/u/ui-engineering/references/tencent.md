---
name: ui-spec-tencent
description: Detailed engineering specification for implementing Tencent's (TDesign) comprehensive, inclusive enterprise design system.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Tencent

## 1. Engineering Context
**Mental Model**: "Universal Connection".
Tencent's design (via TDesign) is the standard for Chinese Enterprise software. It is neutral, clear, and inclusive. It avoids aggressive style in favor of clarity and data density. It is the "Toyota" of UI - reliable and standard.

**Key Traits**:
- **Tencent Blue**: The unifying color.
- **Modularity**: Distinct card-based layouts.
- **Compliance**: Accessibility-first (WCAG 2.0).

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS
- **Component Lib**: **TDesign** (Official React/Vue library) is the best reference.
- **Icons**: TDesign Icons (Stroke based).

## 3. Design Tokens

### 3.1 Colors (Tencent Blue)
- **Brand**: `#0052D9` (The Standard Blue).
- **Brand Hover**: `#003CAB`.
- **Bg**: `#F0F2F5` (Enterprise Gray).
- **Surface**: `#FFFFFF`.
- **Text**: `#000000` (90% opacity), `#000000` (60% opacity).

### 3.2 Typography
- **Font**: `PingFang SC`.
- **Number**: `DIN` (For financial/data display).

## 4. Component Recipes

### The "Data Card"
- **Bg**: `bg-white`
- **Radius**: `rounded-[2px]` or `rounded-[4px]` (Sharper than western apps).
- **Header**: Border-bottom separator.
- **Padding**: `p-6` (Generous internal spacing).

### The "Primary Button"
- **Bg**: `bg-[#0052D9] hover:bg-[#003CAB]`.
- **Radius**: `rounded-[3px]`.
- **Height**: `32px` (Small/Compact is common in dashboards).

### The "Navigation Menu" (Sidebar)
- **Bg**: `bg-[#242424]` (Dark Mode sidebar is common for contrast).
- **Item**: `text-gray-400 hover:text-white hover:bg-white/10`.
- **Active**: `bg-[#0052D9] text-white`.

## 5. Interaction Patterns
- **Feedback**: Every action has a Toast ("Operation Successful").
- **Loading**: Skeleton screens for data tables.
- **Breadcrumbs**: Explicit path navigation is mandatory for hierarchy.
