---
name: ui-spec-flighty
description: Detailed engineering specification for implementing "Flighty Style" (Data Density, Dynamic Island, Live Status).
license: Public domain / Fair use for reference
---

# UI Engineering Spec: Flighty

## 1. Engineering Context
**Mental Model**: "The Live Board".
Flighty keeps the user informed before they even ask. It packs immense density into small cards without feeling cluttered. It loves "Live Activities" aesthetics: black backgrounds, glowing progress bars, and high-contrast data.

**Key Traits**:
- **Island UI**: Elements often look like the Dynamic Island (Pill shapes on black).
- **Proactive**: Statuses are large and color-coded (Green = On Time, Red = Delay).
- **Map Integration**: High-fidelity, dark mode vector maps are central.

## 2. Tech Stack Recommendations
- **Styling**: Tailwind CSS (Dark mode customization is key).
- **Maps**: `Mapbox GL JS` (Dark monochromatic theme).
- **Framework**: `Next.js` (for Server Components to deliver fast data).

## 3. Design Tokens

### 3.1 Colors (Cockpit Dark)
- **Bg**: `#000000` (True Black) or `#1C1C1E` (Apple Dark Gray).
- **Text**: `#FFFFFF`.
- **Status Green**: `#34C759` (Apple Human Interface Green).
- **Status Red**: `#FF3B30` (Apple Human Interface Red).
- **Status Orange**: `#FF9500` (Apple Human Interface Orange).

### 3.2 Typography
- **Font**: `SF Pro Rounded` (or `Nunito` for web).
- **Weight**: Heavy for Data, Regular for labels.
- **Numbers**: Monospaced features (`tnum`) enabled for countdowns.

## 4. Component Recipes

### The "Live Pill" (Dynamic Island Style)
- **Container**: `bg-black rounded-full px-4 py-2 flex items-center justify-between`.
- **Content**: Left: "SFO", Right: "JFK".
- **Center**: Plane icon on a progress track (`w-full h-1 bg-gray-800 rounded-full`).

### The "Flight Card"
- **Bg**: `#1C1C1E`.
- **Corner**: `rounded-2xl`.
- **Data**: Three columns (Dep, Status, Arr).
- **Typography**: Giant time (`text-4xl font-bold`).
- **Highlight**: Status text is colored (`text-green-500`).

### The "Vector Map"
- **Style**: Dark mode.
- **Path**: Geodesic curved lines (Great circle).
- **Plane**: Real-time icon on the path.

## 5. Interaction Patterns
- **Haptic**: Web Vibration API for critical status changes.
- **Progress**: Countdowns update every second.
- **Expand**: Clicking a flight card expands it to a full-screen detailed view.
