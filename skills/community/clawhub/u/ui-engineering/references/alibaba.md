---
name: ui-spec-alibaba
description: Detailed engineering specification for implementing Alibaba's (Ant Design) robust, commerce-focused design system.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Alibaba

## 1. Engineering Context
**Mental Model**: "Certainty".
Alibaba's design (Ant Design) is built for complex systems and commerce. It prioritizes "Certainty" (Predictable interactions) and "Naturalness". It is robust, capable of handling complex forms and massive datasets.

**Key Traits**:
- **Ant Blue & Alibaba Orange**: Enterprise vs Commerce.
- **14px Standard**: The base font size is strictly 14px.
- **Grid**: 24-column layout system.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS (custom config to match Ant).
- **Component Lib**: **Ant Design** (React).
- **Charts**: G2 / AntV (Best in class data viz).

## 3. Design Tokens

### 3.1 Colors
- **Ant Blue**: `#1890FF` (Daybreak Blue).
- **Ali Orange**: `#FF5000` (Taobao/Marketing).
- **Success**: `#52C41A` (Polar Green).
- **Border**: `#D9D9D9`.
- **Divider**: `#F0F0F0`.

### 3.2 Typography
- **Font**: `Alibaba PuHuiTi` (Custom Sans) / `-apple-system`.
- **Size**: `14px` (Base). Small is `12px`.
- **Line Height**: `1.5715`.

## 4. Component Recipes

### The "Commerce Card" (Goods)
- **Image**: Square aspect ratio.
- **Price**: Key visual element.
    - Symbol: `text-xs`.
    - Integer: `text-xl font-bold`.
    - Decimal: `text-xs`.
    - Color: `#FF5000`.
- **Radius**: `rounded-[12px]`.

### The "Step Form"
- **Steps**: Horizontal progress bar with numbered circles.
- **Blue**: `#1890FF` for finished steps.
- **Gray**: `#000000` (25%) for pending.

### The "Search Bar" (Hero)
- **Shape**: `rounded-full` (Capsule).
- **Border**: `border-[2px] border-[#FF5000]`.
- **Button**: Right-aligned, `#FF5000` background, textual "Search".

## 5. Interaction Patterns
- **Empty States**: Illustrated playful mascots when no data is found.
- **Pagination**: Standard bottom-right pagination for tables.
- **Drawers**: Side-panel drawers for editing complex objects without leaving context.
