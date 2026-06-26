# Symbol Palette in Syncfusion React Diagram

## Table of Contents
- [Symbol Palette Overview](#symbol-palette-overview)
- [Basic Setup](#basic-setup)
- [Defining Palette Symbols](#defining-palette-symbols)
- [Adding Connectors to Palette](#adding-connectors-to-palette)
- [Adding Group Nodes to Palette](#adding-group-nodes-to-palette)
- [Template-Based Symbols (HTML/SVG)](#template-based-symbols-htmlsvg)
- [Symbol Display Configuration](#symbol-display-configuration)
- [Palette Expansion Modes](#palette-expansion-modes)
- [Drag and Drop to Diagram](#drag-and-drop-to-diagram)
- [Palette Search](#palette-search)
- [Palette Events](#palette-events)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## Symbol Palette Overview

The `SymbolPaletteComponent` is a companion component to `DiagramComponent` that provides a gallery of reusable shapes, connectors, and templates. Users drag items from the palette and drop them onto the diagram canvas.

Key concepts:
- **Palette**: A named, collapsible group of symbols (e.g. "Flow Shapes", "Basic Shapes")
- **Symbol**: Any `NodeModel` or `ConnectorModel` used as a reusable template
- `SymbolPaletteComponent` is rendered **separately** from the diagram — typically in a sidebar

---

## Basic Setup

Install the same package used for the diagram:

```bash
npm install @syncfusion/ej2-react-diagrams
```

Import the required CSS (same as DiagramComponent):

```tsx
import '@syncfusion/ej2-react-diagrams/styles/material.css';
```

Minimal palette component:

```tsx
import * as React from 'react';
import {
  SymbolPaletteComponent,
  PaletteModel,
  NodeModel,
} from '@syncfusion/ej2-react-diagrams';

const basicShapes: NodeModel[] = [
  { id: 'Rectangle', shape: { type: 'Basic', shape: 'Rectangle' } },
  { id: 'Ellipse',   shape: { type: 'Basic', shape: 'Ellipse' } },
  { id: 'Triangle',  shape: { type: 'Basic', shape: 'Triangle' } },
];

const palettes: PaletteModel[] = [
  {
    id: 'basicShapes',
    title: 'Basic Shapes',
    expanded: true,
    symbols: basicShapes,
  },
];

export default function SymbolPalette() {
  return (
    <SymbolPaletteComponent
      id="symbolpalette"
      width="100%"
      height="700px"
      palettes={palettes}
      symbolHeight={60}
      symbolWidth={60}
    />
  );
}
```

---

## Defining Palette Symbols

Any `NodeModel` can be a palette symbol. Common shape types:

### Basic Shapes

```tsx
const basicShapes: NodeModel[] = [
  { id: 'Rectangle', shape: { type: 'Basic', shape: 'Rectangle' } },
  { id: 'Ellipse',   shape: { type: 'Basic', shape: 'Ellipse' } },
  { id: 'Hexagon',   shape: { type: 'Basic', shape: 'Hexagon' } },
  { id: 'Pentagon',  shape: { type: 'Basic', shape: 'Pentagon' } },
  { id: 'Diamond',   shape: { type: 'Basic', shape: 'Diamond' } },
];
```

### Flow Chart Shapes

```tsx
const flowShapes: NodeModel[] = [
  { id: 'Terminator', shape: { type: 'Flow', shape: 'Terminator' } },
  { id: 'Process',    shape: { type: 'Flow', shape: 'Process' } },
  { id: 'Decision',   shape: { type: 'Flow', shape: 'Decision' } },
  { id: 'Data',       shape: { type: 'Flow', shape: 'Data' } },
  { id: 'Document',   shape: { type: 'Flow', shape: 'Document' } },
  { id: 'PreDefinedProcess', shape: { type: 'Flow', shape: 'PreDefinedProcess' } },
];
```

### Palette with Multiple Groups

```tsx
const palettes: PaletteModel[] = [
  {
    id: 'flow',
    title: 'Flow Shapes',
    expanded: true,
    symbols: flowShapes,
    iconCss: 'e-ddb-icons e-flow',
  },
  {
    id: 'basic',
    title: 'Basic Shapes',
    expanded: false,        // collapsed by default
    symbols: basicShapes,
    iconCss: 'e-ddb-icons e-basic',
  },
];
```

---

## Adding Connectors to Palette

Connectors in a palette require explicit `sourcePoint` and `targetPoint` to give them a display size:

```tsx
import { ConnectorModel } from '@syncfusion/ej2-react-diagrams';

const connectorSymbols: ConnectorModel[] = [
  {
    id: 'Orthogonal',
    type: 'Orthogonal',
    sourcePoint: { x: 0, y: 0 },
    targetPoint: { x: 60, y: 60 },
    targetDecorator: { shape: 'Arrow', style: { strokeColor: '#757575', fill: '#757575' } },
    style: { strokeWidth: 1, strokeColor: '#757575' },
  },
  {
    id: 'Straight',
    type: 'Straight',
    sourcePoint: { x: 0, y: 0 },
    targetPoint: { x: 60, y: 60 },
    targetDecorator: { shape: 'Arrow' },
  },
  {
    id: 'Bezier',
    type: 'Bezier',
    sourcePoint: { x: 0, y: 0 },
    targetPoint: { x: 60, y: 60 },
    targetDecorator: { shape: 'None' },
    style: { strokeWidth: 2 },
  },
];

const palettes: PaletteModel[] = [
  {
    id: 'connectors',
    title: 'Connectors',
    expanded: true,
    symbols: connectorSymbols,
    iconCss: 'e-ddb-icons e-connector',
  },
];
```

---

## Adding Group Nodes to Palette

Define children **before** the group node in the symbols array:

```tsx
const groupNodes: NodeModel[] = [
  {
    id: 'childA',
    height: 50, width: 50,
    offsetX: 50, offsetY: 50,
    style: { fill: '#6BA5D7' },
  },
  {
    id: 'childB',
    height: 50, width: 50,
    offsetX: 110, offsetY: 110,
    style: { fill: '#357BD2' },
  },
  {
    id: 'groupTemplate',
    children: ['childA', 'childB'],
    padding: { left: 10, right: 10, top: 10, bottom: 10 },
  },
];
```

---

## Template-Based Symbols (HTML/SVG)

### HTML Symbol

```tsx
const htmlSymbols: NodeModel[] = [
  {
    id: 'htmlButton',
    shape: {
      type: 'HTML',
      content: '<div style="height:100%;width:100%;background:#0078d4;color:white;display:flex;align-items:center;justify-content:center;border-radius:4px;">Action</div>',
    },
  },
];
```

### Native SVG Symbol

```tsx
const svgSymbols: NodeModel[] = [
  {
    id: 'svgIcon',
    style: { fill: 'none' },
    shape: {
      type: 'Native',
      content: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#0078d4"/><text x="12" y="16" text-anchor="middle" fill="white" font-size="10">OK</text></svg>',
    },
  },
];
```

---

## Symbol Display Configuration

Control how symbols are rendered inside the palette:

| Property | Type | Description |
|---|---|---|
| `symbolHeight` | number | Height of each symbol cell in the palette |
| `symbolWidth` | number | Width of each symbol cell in the palette |
| `symbolMargin` | MarginModel | Spacing around each symbol (left, right, top, bottom) |
| `symbolPreview` | SymbolPreviewModel | Size of the drag preview shown while dragging |

```tsx
<SymbolPaletteComponent
  palettes={palettes}
  symbolHeight={80}
  symbolWidth={80}
  symbolMargin={{ left: 12, right: 12, top: 12, bottom: 12 }}
  symbolPreview={{ height: 100, width: 100 }}
/>
```

### Custom Tooltip on Symbols

Use `getSymbolInfo` to configure tooltip text for each symbol:

```tsx
<SymbolPaletteComponent
  palettes={palettes}
  getSymbolInfo={(symbol: NodeModel) => ({
    fit: true,
    tooltip: (symbol as any).id + ' shape',
  })}
/>
```

---

## Palette Expansion Modes

| Mode | Behavior |
|---|---|
| `'Single'` | Only one palette group can be expanded at a time |
| `'Multiple'` | Multiple groups can be expanded simultaneously |

```tsx
<SymbolPaletteComponent
  expandMode="Multiple"
  palettes={palettes}
/>
```

---

## Drag and Drop to Diagram

The palette works with the diagram automatically — no extra wiring needed for basic drag-and-drop. When a symbol is dropped on the diagram, the diagram raises the `drop` event.

### Customizing Dropped Nodes via `drop` Event

Intercept the drop to override properties of the placed node:

```tsx
import { IDropEventArgs, NodeModel } from '@syncfusion/ej2-react-diagrams';

<DiagramComponent
  drop={(args: IDropEventArgs) => {
    const droppedNode = args.element as NodeModel;
    if (droppedNode && droppedNode.shape) {
      // Customize size after drop
      droppedNode.width = 120;
      droppedNode.height = 60;
    }
  }}
  ...
/>
```

### Connecting Dropped Nodes to a Layout

After dropping a node in a hierarchical layout, create a connector to attach it:

```tsx
import { randomId } from '@syncfusion/ej2-react-diagrams';
<DiagramComponent
drop={(args: IDropEventArgs) => {
  setTimeout(() => {
    const dropped = args.element as NodeModel;
    const parent = args.target as NodeModel;
    if (parent?.id) {
      diagramRef.current?.add({
        id: 'conn_' + randomId(),
        sourceID: parent.id,
        targetID: dropped.id,
        type: 'Orthogonal',
      });
      diagramRef.current?.doLayout();
    }
  }, 100);
}}
...
/>
```

---

## Palette Search

Enable symbol search to let users filter palette items by name:

```tsx
<SymbolPaletteComponent
  enableSearch={true}
  palettes={palettes}
  symbolHeight={60}
  symbolWidth={60}
/>
```

The search bar appears at the top of the palette. Filtering matches against symbol IDs.

---

## Palette Events

| Event | Fires When |
|---|---|
| `paletteSelectionChange` | User clicks a symbol in the palette |

```tsx
import { SymbolPaletteComponent } from "@syncfusion/ej2-react-diagrams";
<SymbolPaletteComponent
  paletteSelectionChange={(args) => {
    console.log('Selected symbol:', args.newValue);
  }}
  palettes={palettes}
/>
```

The `drop` event for palette items fires on the `DiagramComponent`, not the palette.

---

## Best Practices

- Keep `symbolHeight` / `symbolWidth` consistent across all palette groups for a clean grid layout.
- Set `symbolMargin` to at least 8px to prevent symbols from crowding each other.
- For connector symbols, always specify `sourcePoint` and `targetPoint` — without them the connector renders as a zero-length dot.
- Define group node children before the group itself in `symbols[]`, just as with diagram `nodes[]`.
- Use `getSymbolInfo` to add meaningful tooltips when palette symbols look similar (e.g., different flow shapes).
- Keep palette palettes focused — 5–15 symbols per palette group is easier to scan than 30+.

---

## Troubleshooting

**Symbols not appearing in the palette**
→ Verify `symbols` array items have unique `id` values.
→ Check that `expanded: true` is set on at least one palette group — collapsed palettes appear empty until opened.

**Connector symbol shows as a dot**
→ Connectors require `sourcePoint` and `targetPoint` set with non-zero distances.

**Drag preview looks wrong**
→ Use `symbolPreview` to set a size that matches your intended dropped node dimensions.

**Dropped node has wrong size**
→ Intercept the `drop` event on `DiagramComponent` and set `width`/`height` there.

**Group template not dragging correctly**
→ Children must be defined before the group node in the `symbols[]` array. The palette renders the entire group as a single draggable unit.

**Search not finding symbols**
→ By default, search matches symbol `id` strings. Name your symbols with descriptive IDs (e.g., `'decisionDiamond'` not `'node3'`) to make search useful.
