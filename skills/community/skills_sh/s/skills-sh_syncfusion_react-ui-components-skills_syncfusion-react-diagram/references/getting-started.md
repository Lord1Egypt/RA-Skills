# Getting Started with Syncfusion React Diagram

## Table of Contents
- [Dependencies](#dependencies)
- [Installation](#installation)
- [CSS Theme Imports](#css-theme-imports)
- [Basic DiagramComponent Setup](#basic-diagramcomponent-setup)
- [Module Injection](#module-injection)
- [Core Diagram Elements](#core-diagram-elements)
- [Next.js Integration](#nextjs-integration)
- [Preact Integration](#preact-integration)
- [Troubleshooting](#troubleshooting)

---

## Dependencies

The Diagram component requires these peer packages (all installed automatically with the main package):

```
@syncfusion/ej2-react-diagrams
  ├── @syncfusion/ej2-base
  ├── @syncfusion/ej2-data
  ├── @syncfusion/ej2-navigations
  ├── @syncfusion/ej2-inputs
  ├── @syncfusion/ej2-popups
  ├── @syncfusion/ej2-buttons
  ├── @syncfusion/ej2-lists
  ├── @syncfusion/ej2-splitbuttons
  ├── @syncfusion/ej2-diagrams
  └── @syncfusion/ej2-react-base
```

---

## Installation

### Vite + React (recommended)

```bash
# Create project
npm create vite@latest my-app -- --template react-ts
cd my-app

# Install Syncfusion Diagram package
npm install @syncfusion/ej2-react-diagrams --save

npm run dev
```

### Create React App

```bash
npx create-react-app my-app --template typescript
cd my-app
npm install @syncfusion/ej2-react-diagrams --save
npm start
```

---

## CSS Theme Imports

Import CSS in your root stylesheet (`src/App.css` or `src/index.css`). Choose **one** theme:

### Material (standard)

```css
@import "../node_modules/@syncfusion/ej2-base/styles/material.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/material.css";
@import "../node_modules/@syncfusion/ej2-splitbuttons/styles/material.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/material.css";
@import "../node_modules/@syncfusion/ej2-react-diagrams/styles/material.css";
```

### Material 3

```css
@import "../node_modules/@syncfusion/ej2-base/styles/material3.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/material3.css";
@import "../node_modules/@syncfusion/ej2-splitbuttons/styles/material3.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/material3.css";
@import "../node_modules/@syncfusion/ej2-react-diagrams/styles/material3.css";
```

### Bootstrap 5

```css
@import "../node_modules/@syncfusion/ej2-base/styles/bootstrap5.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/bootstrap5.css";
@import "../node_modules/@syncfusion/ej2-splitbuttons/styles/bootstrap5.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/bootstrap5.css";
@import "../node_modules/@syncfusion/ej2-react-diagrams/styles/bootstrap5.css";
```

> **Import order matters** — base styles must come before component styles.

---

## Basic DiagramComponent Setup

### Minimal empty canvas

```tsx
import * as React from 'react';
import { DiagramComponent } from '@syncfusion/ej2-react-diagrams';
import './App.css';

export default function App() {
  return (
    <DiagramComponent
      id="diagram"
      width={'100%'}
      height={'500px'}
    />
  );
}
```

### Diagram with nodes and connectors

```tsx
import * as React from 'react';
import {
  DiagramComponent,
  NodeModel,
  ConnectorModel,
  Inject,
  UndoRedo
} from '@syncfusion/ej2-react-diagrams';
import './App.css';

const nodes: NodeModel[] = [
  {
    id: 'node1',
    offsetX: 200, offsetY: 150,
    width: 120, height: 50,
    annotations: [{ content: 'Node 1' }]
  },
  {
    id: 'node2',
    offsetX: 400, offsetY: 150,
    width: 120, height: 50,
    annotations: [{ content: 'Node 2' }]
  }
];

const connectors: ConnectorModel[] = [
  {
    id: 'connector1',
    sourceID: 'node1',
    targetID: 'node2'
  }
];

export default function App() {
  return (
    <DiagramComponent
      id="diagram"
      width={'100%'}
      height={'400px'}
      nodes={nodes}
      connectors={connectors}
    >
      <Inject services={[UndoRedo]} />
    </DiagramComponent>
  );
}
```

### Important: `id` must be unique and letter-first

```tsx
// ✅ Valid node IDs
id: 'start'
id: 'node1'
id: 'process-step'

// ❌ Invalid — starts with number or contains spaces
id: '1node'
id: 'my node'
```

---

## Module Injection

The Diagram component uses opt-in feature modules. Only inject what you use — this keeps bundle size minimal.

```tsx
import {
  DiagramComponent,
  Inject,
  // Add only the modules you need:
  UndoRedo,
  DataBinding,
  HierarchicalTree,
  MindMap,
  RadialTree,
  ComplexHierarchicalTree,
  LayoutAnimation,
  Snapping,
  PrintAndExport,
  BpmnDiagrams,
  ConnectorBridging,
  ConnectorEditing,
  DiagramContextMenu,
  Ej1Serialization
} from '@syncfusion/ej2-react-diagrams';

export default function App() {
  return (
    <DiagramComponent id="diagram" width={'100%'} height={'500px'}>
      {/* Only inject what your diagram actually uses */}
      <Inject services={[UndoRedo, Snapping]} />
    </DiagramComponent>
  );
}
```

**Module quick reference:**

| Module | When to inject |
|--------|---------------|
| `UndoRedo` | Ctrl+Z / Ctrl+Y support |
| `Snapping` | Grid snapping |
| `PrintAndExport` | Export to image/SVG, print |
| `DataBinding` | Render from data source |
| `HierarchicalTree` | Tree / org-chart layouts |
| `MindMap` | Mind map layouts |
| `RadialTree` | Radial circular layouts |
| `ComplexHierarchicalTree` | Multi-parent tree layouts |
| `LayoutAnimation` | Animated layout transitions |
| `BpmnDiagrams` | BPMN shape types |
| `DiagramContextMenu` | Right-click menu |
| `ConnectorBridging` | Arc bridges over crossing connectors |
| `ConnectorEditing` | Drag-to-reshape connector segments |
| `Ej1Serialization` | Load legacy EJ1 diagram JSON |

> Forgetting to inject a required module is the #1 cause of "feature not working" issues. Always check module injection first.

---

## Core Diagram Elements

Understanding the four building blocks helps you compose any diagram:

| Element | Purpose | Key Property |
|---------|---------|--------------|
| **Node** | Graphical shape (box, circle, flow shape) | `nodes` array |
| **Connector** | Line/arrow between nodes or points | `connectors` array |
| **Annotation** | Text label on a node or connector | `annotations` array on node/connector |
| **Port** | Named connection point on a node | `ports` array on node |

All elements use SVG rendering and are positioned via `offsetX`/`offsetY` coordinates from the canvas origin (top-left).

---

## Next.js Integration

Next.js requires the `'use client'` directive because `DiagramComponent` uses browser APIs.

### Installation

```bash
npx create-next-app@latest ej2-nextjs-diagram
cd ej2-nextjs-diagram
npm install @syncfusion/ej2-react-diagrams --save
```

### CSS import — add to `src/app/globals.css`

```css
@import "../../node_modules/@syncfusion/ej2-base/styles/material.css";
@import "../../node_modules/@syncfusion/ej2-popups/styles/material.css";
@import "../../node_modules/@syncfusion/ej2-splitbuttons/styles/material.css";
@import "../../node_modules/@syncfusion/ej2-navigations/styles/material.css";
@import "../../node_modules/@syncfusion/ej2-react-diagrams/styles/material.css";
```

### Component — `src/app/page.tsx`

```tsx
'use client'   // Required — DiagramComponent uses browser APIs
import { DiagramComponent, NodeModel, Inject, UndoRedo } from '@syncfusion/ej2-react-diagrams';

const nodes: NodeModel[] = [
  {
    id: 'start', offsetX: 200, offsetY: 150,
    width: 120, height: 50,
    annotations: [{ content: 'Start' }]
  }
];

export default function Home() {
  return (
    <DiagramComponent id="diagram" width={'100%'} height={'500px'} nodes={nodes}>
      <Inject services={[UndoRedo]} />
    </DiagramComponent>
  );
}
```

> Without `'use client'`, Next.js will throw a hydration error because `DiagramComponent` accesses `window` and `document`.

---

## Preact Integration

Preact is compatible with Syncfusion React components since it mirrors the React API.

```bash
npm init preact
cd my-project
npm install @syncfusion/ej2-react-diagrams --save
```

### CSS import — `src/style.css`

```css
@import "../node_modules/@syncfusion/ej2-base/styles/material3.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/material3.css";
@import "../node_modules/@syncfusion/ej2-splitbuttons/styles/material3.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/material3.css";
@import "../node_modules/@syncfusion/ej2-react-diagrams/styles/material3.css";
```

### Component — `src/index.jsx`

```jsx
import { render } from 'preact';
import { DiagramComponent, Inject, UndoRedo } from '@syncfusion/ej2-react-diagrams';

export default function App() {
  return (
    <DiagramComponent id="diagram" width={'100%'} height={'400px'}>
      <Inject services={[UndoRedo]} />
    </DiagramComponent>
  );
}

render(<App />, document.querySelector('#app'));
```

---

## Troubleshooting

**Diagram renders blank / no shapes visible**
- Ensure CSS is imported and the import path is correct (check `node_modules/` prefix)
- Confirm `id` prop is set on `DiagramComponent`
- Check that `nodes` array objects have valid `offsetX`/`offsetY` values

**"Module not found" / feature not working**
- Inject the required module via `<Inject services={[...]} />`
- Verify the module is imported from `@syncfusion/ej2-react-diagrams`

**Next.js hydration error**
- Add `'use client'` at the top of the file containing `DiagramComponent`

**TypeScript errors on `node.data`**
- Cast to the appropriate interface: `(node.data as MyDataType).propertyName`

**Node IDs causing issues**
- IDs must start with a letter, no spaces, no special characters (underscores are also disallowed)
- IDs must be unique across all nodes and connectors in the diagram

**Related docs:**
- Nodes → [nodes.md](nodes.md)
- Connectors → [connectors.md](connectors.md)
- Layouts → [layouts.md](layouts.md)
- Data Binding → [data-binding.md](data-binding.md)
