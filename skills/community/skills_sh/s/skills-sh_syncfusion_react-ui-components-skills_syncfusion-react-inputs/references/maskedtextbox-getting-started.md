# Getting Started with React MaskedTextBox

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [CSS Setup](#css-setup)
- [Basic Implementation](#basic-implementation)
- [Setting a Mask](#setting-a-mask)
- [Running the Application](#running-the-application)

## Prerequisites

Create a React app using Vite (recommended for faster builds):

```bash
# JavaScript
npm create vite@latest my-app -- --template react
cd my-app
npm run dev

# TypeScript
npm create vite@latest my-app -- --template react-ts
cd my-app
npm run dev
```

## Installation

Install the Syncfusion inputs package that contains the MaskedTextBox:

```bash
npm install @syncfusion/ej2-react-inputs --save
```

## CSS Setup

Add CSS imports in `src/App.css`:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-inputs/styles/tailwind3.css";
```

Import `App.css` in `src/App.tsx`:

```tsx
import './App.css';
```

## Basic Implementation

### Functional Component

```tsx
import * as React from 'react';
import { MaskedTextBoxComponent } from '@syncfusion/ej2-react-inputs';
import './App.css';

export default function App() {
  return (
    <MaskedTextBoxComponent placeholder="Enter Name" />
  );
}
```

### Class Component

```tsx
import * as React from 'react';
import { MaskedTextBoxComponent } from '@syncfusion/ej2-react-inputs';
import './App.css';

export default class App extends React.Component<{}, {}> {
  public render() {
    return (
      <MaskedTextBoxComponent placeholder="Enter Name" />
    );
  }
}
```

## Setting a Mask

Use the `mask` property to enforce a specific input format. Without a mask, MaskedTextBox behaves as a plain text input.

### Functional Component

```tsx
import * as React from 'react';
import { MaskedTextBoxComponent } from '@syncfusion/ej2-react-inputs';
import './App.css';

export default function App() {
  return (
    <div>
      <label className="label">Enter the mobile number</label>
      <MaskedTextBoxComponent mask="000-000-0000" />
    </div>
  );
}
```

### Class Component

```tsx
import * as React from 'react';
import { MaskedTextBoxComponent } from '@syncfusion/ej2-react-inputs';
import './App.css';

export default class App extends React.Component<{}, {}> {
  public render() {
    return (
      <div>
        <label className="label">Enter the mobile number</label>
        <MaskedTextBoxComponent mask="000-000-0000" />
      </div>
    );
  }
}
```

## Floating Label

Use `floatLabelType` to control how the placeholder/label behaves:

```tsx
// Placeholder floats above when focused or filled
<MaskedTextBoxComponent
  mask="000-000-0000"
  placeholder="Phone Number"
  floatLabelType="Auto"
/>

// Label always floats above
<MaskedTextBoxComponent
  mask="000-000-0000"
  placeholder="Phone Number"
  floatLabelType="Always"
/>
```

## Running the Application

```bash
npm run dev
```

The application opens in the browser. The `_` character is the default prompt character showing available input positions.

> **Tip:** The `mask` property is the primary configuration — without it, MaskedTextBox behaves as a plain text input. Always set `mask` for format enforcement.
