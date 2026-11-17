---
name: ui-spec-geek-primer
description: Detailed engineering specification for implementing "GitHub Primer Style" (Utility, Developer-First, Muted).
license: Public domain / Fair use for reference
---

# UI Engineering Spec: GitHub Primer

## 1. Engineering Context
**Mental Model**: "The Code Forge".
Design for work. It is reliable, high-contrast (but muted), and incredibly dense effectively. It uses distinct "Border Box" containers and color-coded status indicators (Merged Purple, Open Green, Closed Red).

**Key Traits**:
- **Rounded Borders**: `rounded-md` (6px) is the absolute standard.
- **Subtle Borders**: `border-gray-200` (Light) or `border-gray-800` (Dark).
- **Muted Backgrounds**: Use `bg-gray-50` for "read-only" or "header" contexts.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS (or `@primer/css` if using their actual library).
- **Icons**: `Octicons` (The official SVG set).
- **Font**: `Inter` or `System UI` (`-apple-system`).

## 3. Design Tokens

### 3.1 Colors (Productivity)
- **Bg**: `#FFFFFF` (Day) / `#0D1117` (Night).
- **Canvas Sub**: `#F6F8FA` (Day) / `#161B22` (Night).
- **Border**: `#D0D7DE` (Day) / `#30363D` (Night).
- **Accent**: `#0969DA` (Link Blue).
- **Success**: `#2DA44E` (Git Green).
- **Danger**: `#CF222E` (Delete Red).

### 3.2 Typography
- **Font**: `System UI`.
- **Code**: `SF Mono`, `Fira Code`.
- **Size**: Slightly smaller body (`14px`) to fit more code.

## 4. Component Recipes

### The "Repo Card"
- **Container**: `border border-border rounded-md p-4 bg-canvas`.
- **Header**: Icon (Book) + Text (Blue Link) + Badge (Public/Public).
- **Meta**: Flex row of small text (`text-xs text-muted`) showing Language color dot and Stars.

### The "File Tree"
- **Row**: `border-t border-border py-2 px-3 hover:bg-canvas-sub`.
- **Icon**: Folder (Blue) or File (Gray).
- **Commit**: Truncated gray text on the right.

### The "Flash Alert"
- **Container**: `rounded-md p-4 mb-4 border-l-4`.
- **Info**: `bg-blue-50 border-blue-200 text-blue-800 border-l-blue-500`.
- **Warn**: `bg-yellow-50 border-yellow-200 text-yellow-800 border-l-yellow-500`.

## 5. Interaction Patterns
- **Hover Badge**: Hovering a user avatar shows a "User Card" popover (`z-50`).
- **Keyboard**: Shortcuts ('g' then 'i' to go to issues) are mandatory for power users.
