---
name: ui-spec-xiaohongshu
description: Detailed engineering specification for implementing Xiaohongshu's lifestyle-focused, collage-style design system.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Xiaohongshu (RED)

## 1. Engineering Context
**Mental Model**: "The Scrapbook".
Xiaohongshu is a digital lifestyle magazine. The key is the **Dual-Column Waterfall** layout. Images are vertical (3:4) to maximize mobile screen real estate. The aesthetics are "Real" and "Collage-like" (stickers, tags).

**Key Traits**:
- **Masonry Layout**: The defining grid structure.
- **Bubble Tags**: Interactive dots on images.
- **Roundness**: Soft, friendly cards (8px-12px).

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS
- **Layout**: CSS Multi-column (`column-count: 2`) or Masonry Grid.
- **Touch**: `react-use-gesture` (Swipeable galleries).

## 3. Design Tokens

### 3.1 Colors (Vibrant Red)
- **Brand Red**: `#FF2442` (Young, vibrant red. Not dark red).
- **Bg Page**: `#F5F8FA` (Cool light gray to make white cards pop).
- **Bg Card**: `#FFFFFF`.
- **Text Main**: `#333333`.
- **Text Hash**: `#13386C` (Hashtags are blue/navy).

### 3.2 Typography
- **Font**: `PingFang SC` / `San Francisco`.
- **Title**: `font-weight: 600`.
- **Emoji**: Titles often start or end with Emojis 🍓✨.

## 4. Component Recipes

### The "Note Card" (Feed Item)
- **Container**: `bg-white rounded-lg mb-2 overflow-hidden break-inside-avoid`.
- **Image**: Vertical aspect ratio is king.
- **Title**: `text-[14px] font-bold line-clamp-2 mt-2 px-2`.
- **User Row**: Flex row at bottom with Avatar (16px circle) and Name (10px gray) + Like Heart (gray outline).

### The "Image Tag" (Bubble)
Interactive tag *on* the image.
- **Shape**: Line with a dot at the end, or a bubble.
- **Bg**: `bg-black/50 backdrop-blur-sm text-white px-2 py-1 rounded-full text-xs`.
- **Animation**: Pulse animation on the dot anchor.

### The "Publish Button" (Center Tab)
- **Shape**: Large `rounded-[12px]` square or simple Plus icon.
- **Bg**: `#FF2442`.
- **Position**: Center of bottom tab bar.

## 5. Interaction Patterns
- **Swipe Gallery**: Horizontal swipe on the main image to see more photos without entering the post.
- **Double Tap**: Like (Heart animation in center of screen).
- **Stickers**: Layered pngs over images.
