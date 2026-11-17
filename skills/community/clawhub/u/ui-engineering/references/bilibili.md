---
name: ui-spec-bilibili
description: Detailed engineering specification for implementing Bilibili's vibrant, Gen-Z, ACG-culture design system.
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Bilibili

## 1. Engineering Context
**Mental Model**: "The Playground".
Bilibili is high-energy. It mixes "Cute" (Pink) with "Tech" (Blue). The interface is dense, designed for high-speed information consumption (Bullet Chat). It features gamification elements (Badges, Levels) on every surface.

**Key Traits**:
- **Pink & Blue**: The definitive duo.
- **Density**: Columns of video cards (Waterfall).
- **Overlay**: Text over images (Bullet Chat).

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS / Less.
- **Grid**: Masonry Layout (`react-masonry-css`).
- **Video**: Custom Player with Danmaku (Bullet Chat) engine (`danmaku.js`).

## 3. Design Tokens

### 3.1 Colors (ACG Palette)
- **Primary Pink**: `#FB7299` (The "Little Pink" app).
- **Primary Blue**: `#23ADE5` (Tech/Level 6).
- **White**: `#FFFFFF`
- **Gray**: `#F4F5F7` (Background).
- **Text Main**: `#212121`.
- **Text Gray**: `#9499A0` (Key for secondary info like view counts).

### 3.2 Typography
- **Font**: `HarmonyOS Sans` / `PingFang SC`.
- **Style**: Rounded sans-serifs preferred.
- **Size**: Mobile-first sizing (`14px` titles, `12px` meta).

## 4. Component Recipes

### The "Video Card" (Waterfall)
- **Container**: `bg-white rounded-[6px] overflow-hidden shadow-sm hover:shadow-md`.
- **Image**: Aspect ratio `16:9` (Desktop) or `3:4` (Mobile).
- **Stats Overlay**: Gradient overlay at bottom of image (`bg-gradient-to-t from-black/60 to-transparent`) with white text icons (Play count, Danmaku count).

### The "Follow Button"
- **Bg**: `bg-[#FB7299] hover:bg-[#ff85a7]`.
- **Text**: `text-white`.
- **Shape**: `rounded-[4px]`.
- **Animation**: On click, morphs to Gray "Followed".

### The "Danmaku" (Bullet Chat)
- **Layer**: Absolute overlay on top of video canvas.
- **Text**: White text with black text-stroke (`text-shadow: 1px 1px 2px black`).
- **Motion**: Linear translation from Right to Left.

## 5. Interaction Patterns
- **Infinite Scroll**: The feed never ends.
- **Hover Autoplay**: Hovering a video card plays a muted preview (2x speed often).
- **Gamification**: Success = XP +1 animation popup.
