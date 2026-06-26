# Getting Started with Image Editor

## Table of Contents
- [Installation](#installation)
- [CSS Setup](#css-setup)
- [Basic Component](#basic-component)
- [Initialization](#initialization)

## Installation

The Syncfusion React Image Editor is available as an npm package. Install it using your preferred package manager.

### Using npm

```bash
npm install @syncfusion/ej2-react-image-editor --save
```

### Vite Setup

Create a new React application with Vite for faster development:

```bash
npm create vite@latest my-app -- --template react
cd my-app
npm run dev
```

Then install the Image Editor package:

```bash
npm install @syncfusion/ej2-react-image-editor --save
```

## CSS Setup

Add the required CSS files to your `src/App.css` for styling the Image Editor and its dependencies:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-splitbuttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-image-editor/styles/tailwind3.css";
```

Import this CSS file in your `App.tsx`:

```tsx
import './App.css';
```

## Basic Component

Here's a minimal setup for the Image Editor:

```tsx
import { ImageEditorComponent } from '@syncfusion/ej2-react-image-editor';
import React from 'react';
import './App.css';

function App() {
  return (
    <div id="container">
      <ImageEditorComponent width="550px" height="350px" />
    </div>
  );
}

export default App;
```

## Initialization

To initialize the Image Editor with an image on component creation, use the `created` event:

```tsx
import { ImageEditorComponent } from '@syncfusion/ej2-react-image-editor';
import { Browser } from '@syncfusion/ej2-base';
import React from 'react';
import './App.css';

function App() {
  let imgObj: ImageEditorComponent;

  function imageEditorCreated(): void {
    // Detect device and load appropriate image
    if (Browser.isDevice) {
      imgObj.open('https://ej2.syncfusion.com/react/documentation/image-editor/images/flower.jpeg');
    } else {
      imgObj.open('https://ej2.syncfusion.com/react/documentation/image-editor/images/bridge.jpeg');
    }
  }

  return (
    <div id="container">
      <ImageEditorComponent
        ref={(img) => { imgObj = img }}
        width="550px"
        height="350px"
        created={imageEditorCreated}
      />
    </div>
  );
}

export default App;
```

## Running the Application

Start your development server:

```bash
npm run dev
```

The application will compile and serve at `http://localhost:5173` (for Vite).

## Key Properties in Setup

| Property | Purpose |
|----------|---------|
| `width` | Sets the canvas width (e.g., "550px", "100%") |
| `height` | Sets the canvas height (e.g., "350px", "100%") |
| `toolbar` | Customize toolbar items (default: all built-in items) |
| `created` | Event fired when component is ready |
| `ref` | Access component instance for method calls |

## Next Steps

- Open images using the [opening-saving-images.md](./opening-saving-images.md) reference
- Apply transformations with [transform-rotate-flip.md](./transform-rotate-flip.md)
- Add annotations with [text-annotations.md](./text-annotations.md), [shape-annotations.md](./shape-annotations.md), or [freehand-drawing.md](./freehand-drawing.md)
