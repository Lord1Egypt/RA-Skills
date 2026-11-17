---
name: ui-spec-shopify
description: Detailed engineering specification for implementing Shopify's "Polaris" design system (Merchant Admin, Accessibility).
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Shopify

## 1. Engineering Context
**Mental Model**: "The Merchant's Workbench".
Polaris is not for "shoppers"; it is for "business owners". It is dense, informative, and rock-solid. It prioritizes accessibility (A11y) above all else. It uses distinct "Cards" on a gray background to organize complex forms.

**Key Traits**:
- **polaris-icons**: A specific set of svg icons (1 point stroke).
- **The Magic Layout**: Sidebar navigation + Center content card stack.
- **Action Context**: "Save" bars appear at the top when forms are dirty.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS.
- **Icons**: `polaris-icons` (npm package).
- **Charts**: `Recharts` (Clean, simple line charts).

## 3. Design Tokens

### 3.1 Colors (Admin)
- **Bg Page**: `#F1F2F4` (Light Gray).
- **Bg Surface**: `#FFFFFF` (White Card).
- **Text**: `#303030` (Ink).
- **Subdued**: `#6D7175`.
- **Interactive**: `#008060` (Shopify Green - Primary Action).
- **Critical**: `#D82C0D`.

### 3.2 Typography
- **Font**: `Inter` (Shopify moved to Inter recently).
- **Weight**: `400` / `600`.
- **Readability**: High contrast always.

## 4. Component Recipes

### The "Admin Card"
- **Bg**: White.
- **Shadow**: `shadow-sm` (Subtle ring: `0 0 0 1px rgba(63, 63, 68, 0.05)`).
- **Corner**: `rounded-lg` (8px).
- **Section**: `border-b border-gray-200 p-4`.

### The "Resource List"
- **Layout**: Stack of items.
- **Item**: `p-4 border-b border-gray-100 hover:bg-gray-50 flex justify-between`.
- **Avatar**: Square rounded (`rounded-[4px]`) product thumbnail.

### The "Contextual Save Bar"
- **Position**: Fixed top (below header).
- **Bg**: `#202223` (Black).
- **Text**: White.
- **Animation**: Slide down when `isDirty === true`.

## 5. Interaction Patterns
- **Toast**: "Product saved" appears at bottom center.
- **Bulk Actions**: Selecting a checkbox in header reveals bulk action buttons.
