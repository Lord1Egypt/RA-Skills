# Getting Started with React Timeline

## Table of Contents
- [Installation and Setup](#installation-and-setup)
- [CSS Import Setup](#css-import-setup)
- [Creating a React Application](#creating-a-react-application)
- [Basic Timeline Component](#basic-timeline-component)
- [Adding Content to Timeline Items](#adding-content-to-timeline-items)
- [Container Height](#container-height)
- [Running the Application](#running-the-application)
- [Verifying Installation](#verifying-installation)

## Installation and Setup

### Dependencies

The Timeline component requires the following npm packages:

```
@syncfusion/ej2-react-layouts
@syncfusion/ej2-base
@syncfusion/ej2-layouts
@syncfusion/ej2-react-base
```

### Installing the Package

Install the Timeline component using npm:

```bash
npm install @syncfusion/ej2-react-layouts --save
```

This command automatically installs all required dependencies.

## CSS Import Setup

Add CSS references to your application. Import the required CSS files in your `App.tsx` or `App.jsx`:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-layouts/styles/tailwind3.css";
```

**Available Themes:**
- `tailwind3.css` (default, modern design)
- `bootstrap5.3.css` (Bootstrap styling)
- `fluent2.css` (Microsoft Fluent design)
- `material3.css` (Material design)

Choose based on your application's design system.

## Creating a React Application

### Using Vite (Recommended)

```bash
npm create vite@latest my-timeline-app -- --template react
cd my-timeline-app
npm run dev
```

For TypeScript:

```bash
npm create vite@latest my-timeline-app -- --template react-ts
cd my-timeline-app
npm run dev
```

### Using Create React App

```bash
npx create-react-app my-timeline-app
cd my-timeline-app
npm start
```

## Basic Timeline Component

### Importing Components

```tsx
import { TimelineComponent, ItemsDirective, ItemDirective } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';
import * as ReactDOM from 'react-dom/client';
import './App.css';
```

### Pattern 1: ItemsDirective and ItemDirective (JSX-Based)

```tsx
import { TimelineComponent, ItemsDirective, ItemDirective } from '@syncfusion/ej2-react-layouts';
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-layouts/styles/tailwind3.css';

function App() {
  return (
    <div id='timeline' style={{ height: '350px' }}>
      <TimelineComponent>
        <ItemsDirective>
          <ItemDirective />
          <ItemDirective />
          <ItemDirective />
          <ItemDirective />
        </ItemsDirective>
      </TimelineComponent>
    </div>
  );
}

export default App;
```

### Pattern 2: Items Array Property (Data-Driven)

```tsx
import { TimelineComponent, TimelineItemModel } from '@syncfusion/ej2-react-layouts';
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-layouts/styles/tailwind3.css';

function App() {
  const timelineItems: TimelineItemModel[] = [
    { content: 'Cart' },
    { content: 'Personal Info' },
    { content: 'Delivery Address' },
    { content: 'Payment' }
  ];

  return (
    <div id='timeline' style={{ height: '350px' }}>
      <TimelineComponent items={timelineItems} />
    </div>
  );
}

export default App;
```

**Pattern Selection Guide:**
- **ItemsDirective:** Use for static JSX-based timelines with individual control per item
- **items property:** Use for dynamic data from APIs, databases, or when items are managed in state

## Adding Content to Timeline Items

### String Content

Add text content to each timeline item:

```tsx
function App() {
  return (
    <div id='timeline' style={{ height: '330px' }}>
      <TimelineComponent>
        <ItemsDirective>
          <ItemDirective content='Shipped' />
          <ItemDirective content='Departed' />
          <ItemDirective content='Arrived' />
          <ItemDirective content='Out for Delivery' />
        </ItemsDirective>
      </TimelineComponent>
    </div>
  );
}
```

### Adding Opposite Content

Display secondary content on the opposite side:

```tsx
<TimelineComponent>
  <ItemsDirective>
    <ItemDirective content='Breakfast' oppositeContent='8:00 AM' />
    <ItemDirective content='Lunch' oppositeContent='1:00 PM' />
    <ItemDirective content='Dinner' oppositeContent='8:00 PM' />
  </ItemsDirective>
</TimelineComponent>
```

## Container Height

**Critical:** The TimelineComponent requires an explicit height. Set it via inline style:

```tsx
<div id='timeline' style={{ height: '330px' }}>
  <TimelineComponent>
    {/* Items */}
  </TimelineComponent>
</div>
```

Without height, the timeline will not render items vertically.

## Running the Application

After setting up your project and creating the App component:

```bash
npm run dev
```

Open your browser to the provided localhost URL (typically `url` for Vite or `url` for Create React App).

## Verifying Installation

Check that the timeline renders with:
- Vertical layout (default)
- 4 items displayed
- Each item has a dot indicator
- Items are connected by a vertical line

If items don't display, verify:
- CSS imports are in place
- Container has explicit height
- ItemsDirective wraps ItemDirective elements
