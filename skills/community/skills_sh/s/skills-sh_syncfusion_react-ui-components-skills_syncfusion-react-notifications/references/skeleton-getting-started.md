# Getting Started with Syncfusion React Skeleton

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Adding CSS References](#adding-css-references)
- [Basic Skeleton Setup](#basic-skeleton-setup)
- [Running the Application](#running-the-application)
- [Minimal Examples](#minimal-examples)

---

## Prerequisites

- React project created with Vite (recommended) or Create React App
- Node.js installed

Create a new Vite-based React app:

```bash
# TypeScript
npm create vite@latest my-app -- --template react-ts
cd my-app
npm run dev

# JavaScript
npm create vite@latest my-app -- --template react
cd my-app
npm run dev
```

---

## Installation

Install the Syncfusion notifications package, which includes `SkeletonComponent`:

```bash
npm install @syncfusion/ej2-react-notifications --save
```

> The `--save` flag adds the package to the `dependencies` section of `package.json`.

---

## Adding CSS References

Add the required CSS imports in `src/App.css`:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-notifications/styles/tailwind3.css";
```

Then import `App.css` in `src/App.tsx`:

```tsx
import './App.css';
```

---

## Basic Skeleton Setup

Add `SkeletonComponent` to your component. At minimum, provide a `height` for text-style skeletons:

```tsx
import { SkeletonComponent } from '@syncfusion/ej2-react-notifications';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <SkeletonComponent height="15px" />
  );
}
export default App;
```

For circle or square shapes, provide `width` (used as the dimension):

```tsx
import { SkeletonComponent } from '@syncfusion/ej2-react-notifications';
import * as React from 'react';

function App() {
  return (
    <SkeletonComponent shape="Circle" width="48px" />
  );
}
export default App;
```

---

## Running the Application

Start the development server:

```bash
npm run dev
```

The app opens in the browser. Skeleton placeholders render immediately with the default Wave shimmer animation.

---

## Minimal Examples

### Text line placeholder (default)
```tsx
<SkeletonComponent height="15px" width="80%" />
```

### Avatar placeholder
```tsx
<SkeletonComponent shape="Circle" width="48px" />
```

### Image placeholder
```tsx
<SkeletonComponent shape="Rectangle" width="100%" height="200px" />
```

### Small icon placeholder
```tsx
<SkeletonComponent shape="Square" width="32px" />
```

---

## Dimension Rules

| Shape | Width | Height |
|-------|-------|--------|
| `Text` (default) | Optional | Required |
| `Rectangle` | Required | Required |
| `Circle` | Required (used as diameter) | Not needed |
| `Square` | Required (used as side length) | Not needed |

> For `Circle` and `Square`, `width` is used as the single dimension. Height is ignored.
