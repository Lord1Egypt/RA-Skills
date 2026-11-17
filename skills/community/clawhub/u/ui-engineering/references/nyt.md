---
name: ui-spec-nyt
description: Detailed engineering specification for implementing The New York Times' "Digital Heritage" design system.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: The New York Times

## 1. Engineering Context
**Mental Model**: "The Daily Paper".
The hallmark is **Hierarchy**. It is not about "designing boxes"; it is about organizing information density. It uses a complex mix of Blackletter (Logo), Serif (Headlines/Body), and Sans (UI) to guide the eye through dense text.

**Key Traits**:
- **Blackletter**: The masthead creates instant authority.
- **Lines**: Vertical and horizontal hairlines (`1px solid #E2E2E2`) separate every story.
- **Date**: The date is a central anchor element.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS.
- **Typography**: `Georgia` (System serif) is the classic web fallback, but `Cheltenham` (Headline) and `Imperial` (Body) are the branded choices.
- **Grid**: 5-column or 12-column heavy grid.

## 3. Design Tokens

### 3.1 Colors (Ink & Paper)
- **Bg**: `#FFFFFF`.
- **Text**: `#121212` (Ink Black).
- **Secondary**: `#5A5A5A` (Gray).
- **Links**: `#326891` (NYT Blue - discreet).
- **Live**: `#B22222` (Red - for "Breaking News").

### 3.2 Typography
- **Masthead**: `Chomsky` or `Engravers Old English`.
- **Headline**: `Cheltenham` (Bold, Condensed, Italic variations).
- **Body**: `Georgia` or `Imperial`.
- **Meta**: `Franklin Gothic` or `Arial` (Byline, Date, Section).

## 4. Component Recipes

### The "Story Card" (Standard)
- **Layout**: Thumbnail on Right (Desktop) or Top (Mobile).
- **Headline**: Serif, Bold, `text-xl tight-leading`.
- **Summary**: Serif, `text-sm text-gray-600`.
- **Byline**: Sans, `text-xs uppercase text-gray-400`.
- **Separator**: `border-b border-gray-200 pb-4 mb-4`.

### The "Live Briefing"
- **Indication**: Red badge "LIVE".
- **List**: Timestamped updates.
- **Time**: Bold Sans `12:05 PM`.
- **Content**: Serif Short text.

### The "Navigation Header"
- **Top**: Logo centered (Blackletter).
- **Sub**: Section links center-aligned, `border-t border-b border-black double-border`.

## 5. Interaction Patterns
- **Hover**: User underlines on links.
- **Reading Progress**: Subtle top bar on long reads.
- **Tooltips**: Definitions of complex terms on click.
