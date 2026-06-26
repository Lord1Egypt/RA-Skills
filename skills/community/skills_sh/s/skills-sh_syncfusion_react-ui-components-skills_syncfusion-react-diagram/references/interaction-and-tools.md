# Interaction and Tools

## Table of Contents
- [Overview](#overview)
- [Selection](#selection)
- [Drag and Resize](#drag-and-resize)
- [Tool Modes](#tool-modes)
- [Drawing Tools](#drawing-tools)
- [Constraints](#constraints)
- [Commands](#commands)
- [Undo and Redo](#undo-and-redo)
- [Context Menu](#context-menu)
- [User Handles](#user-handles)
- [Fixed User Handles](#fixed-user-handles)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## Overview

The Syncfusion React Diagram component provides a rich set of interaction capabilities. Users can select, drag, resize, rotate, and connect diagram elements through mouse and keyboard. The `tool` property on `DiagramComponent` controls which interaction modes are active. Constraints (bitwise flags) enable/disable specific behaviors per element or diagram-wide.

Required module injections for specific features:
```tsx
import { DiagramComponent, Inject, UndoRedo, DiagramContextMenu, ConnectorEditing } from '@syncfusion/ej2-react-diagrams';

<DiagramComponent ...>
  <Inject services={[UndoRedo, DiagramContextMenu, ConnectorEditing]} />
</DiagramComponent>
```

---

## Selection

### Single and Multiple Selection

Click an element to select it — previous selections are cleared. Hold **Ctrl** and click to add to the selection. Drag a rubber-band rectangle to select multiple elements.

```tsx
import { DiagramComponent, NodeModel } from '@syncfusion/ej2-react-diagrams';

let diagramInstance: DiagramComponent;
const nodes: NodeModel[] = [
  { id: 'n1', offsetX: 100, offsetY: 100, width: 80, height: 60 },
  { id: 'n2', offsetX: 250, offsetY: 100, width: 80, height: 60 },
];

function App() {
  return (
    <DiagramComponent
      id="container"
      ref={(diagram) => (diagramInstance = diagram)}
      width="100%"
      height="600px"
      nodes={nodes}
      created={() => {
        // Programmatic single selection
        diagramInstance.select([diagramInstance.nodes[0]]);

        // Select all
        diagramInstance.selectAll();

        // Clear selection
        diagramInstance.clearSelection();
      }}
    />
  );
}
```

### Rubber-Band Selection Mode

Control whether rubber-band selection requires elements to be fully or partially inside the rectangle:

```tsx
<DiagramComponent
  id="container"
  width="100%"
  height="600px"
  // CompleteIntersect | PartialIntersect
  selectedItems={{ rubberBandSelectionMode: 'CompleteIntersect' }}
/>
```

### Toggle Selection

Allow click-to-deselect behavior:

```tsx
<DiagramComponent
  id="container"
  width="100%"
  height="600px"
  nodes={nodes}
  selectedItems={{ canToggleSelection: true }}
/>
```

### Get Selected Items

```tsx
const selectedNodes     = diagramInstance.selectedItems.nodes;
const selectedConnectors = diagramInstance.selectedItems.connectors;
```

### Selection Events

| Event | Trigger |
|---|---|
| `selectionChange` | When selection changes |
| `click` | When an element is clicked |

---

## Drag and Resize

### Drag

Click and drag any selected element to move it. Dragging one element in a multi-selection moves all selected elements together.

Event: `positionChange` fires while dragging.

### Resize

Eight resize thumbs appear around the selector. Drag a corner thumb to resize; the opposite corner stays fixed.

Event: `sizeChange` fires while resizing.

### Maintain Aspect Ratio

```tsx
import { NodeConstraints } from '@syncfusion/ej2-react-diagrams';

const nodes: NodeModel[] = [{
  id: 'n1',
  offsetX: 250, offsetY: 250,
  width: 100, height: 100,
  constraints: NodeConstraints.Default | NodeConstraints.AspectRatio,
}];
```

### Customize Resize Thumb Size

```tsx
<DiagramComponent
  id="container"
  width="100%"
  height="600px"
  nodes={nodes}
  selectedItems={{ handleSize: 20 }}
/>
```

### Rotation

A rotate handle appears above the selector. Drag it in a circular direction to rotate the node around its pivot point (default: center `{x: 0.5, y: 0.5}`).

### Restrict Drag/Drop in Negative Axis

Prevent elements from being dragged into negative coordinate areas:

```tsx
import { DiagramConstraints } from '@syncfusion/ej2-react-diagrams';

<DiagramComponent
  id="container"
  width="100%"
  height="600px"
  constraints={DiagramConstraints.Default | DiagramConstraints.RestrictNegativeAxisDragDrop}
/>
```

---

## Tool Modes

Set the active interaction mode with the `tool` property using `DiagramTools`:

| Tool | Behavior |
|---|---|
| `DiagramTools.Default` | Select + multi-select |
| `DiagramTools.SingleSelect` | Single element selection only |
| `DiagramTools.MultipleSelect` | Multi-select via rubber-band |
| `DiagramTools.ZoomPan` | Pan the diagram view |
| `DiagramTools.DrawOnce` | Draw one element then return to select mode |
| `DiagramTools.ContinuousDraw` | Keep drawing until deactivated |
| `DiagramTools.None` | Disable all interaction |

**Precedence (highest → lowest):** ContinuousDraw → DrawOnce → ZoomPan → MultipleSelect → SingleSelect → None

```tsx
import { DiagramTools } from '@syncfusion/ej2-react-diagrams';

// Pan only
<DiagramComponent tool={DiagramTools.ZoomPan} ... />

// Allow panning while still enabling selection
<DiagramComponent tool={DiagramTools.SingleSelect | DiagramTools.ZoomPan} ... />
```

---

## Drawing Tools

Use drawing tools to create nodes and connectors interactively at runtime.

### Draw a Shape Node

```tsx
import { DiagramTools, BasicShapeModel, NodeModel } from '@syncfusion/ej2-react-diagrams';

let diagramInstance: DiagramComponent;

function App() {
  return (
    <DiagramComponent
      id="container"
      ref={(diagram) => (diagramInstance = diagram)}
      width="100%"
      height="600px"
      created={() => {
        const node: BasicShapeModel = { type: 'Basic', shape: 'Rectangle' };
        diagramInstance.drawingObject = { shape: node } as NodeModel;
        diagramInstance.tool = DiagramTools.ContinuousDraw;
        diagramInstance.dataBind();
      }}
    />
  );
}
```

### Draw a Connector

```tsx
import { ConnectorModel, DiagramTools } from '@syncfusion/ej2-react-diagrams';

created={() => {
  const connector: ConnectorModel = { id: 'c1', type: 'Orthogonal' };
  diagramInstance.drawingObject = connector;
  diagramInstance.tool = DiagramTools.DrawOnce;
  diagramInstance.dataBind();
}}
```

### Draw Polygon / Polyline / Freehand

```tsx
// Polygon node
diagramInstance.drawingObject = { shape: { type: 'Basic', shape: 'Polygon' } };
diagramInstance.tool = DiagramTools.DrawOnce;

// Polyline connector
diagramInstance.drawingObject = { id: 'c1', type: 'Polyline' } as ConnectorModel;

// Freehand connector
diagramInstance.drawingObject = { id: 'c1', type: 'Freehand' } as ConnectorModel;
```

> **Note:** To edit polyline/freehand segment thumbs, inject `ConnectorEditing` and enable `ConnectorConstraints.DragSegmentThumb`.

### Element Draw Event

```tsx
import { IElementDrawEventArgs } from '@syncfusion/ej2-react-diagrams';

<DiagramComponent
  ...
  elementDraw={(args: IElementDrawEventArgs) => {
    if (args.state === 'Completed') {
      console.log('Element drawn:', args.element);
    }
  }}
/>
```

---

## Constraints

Constraints are bitwise flags. Use `|` to enable and `& ~` to disable specific behaviors.

### Diagram Constraints

```tsx
import { DiagramConstraints } from '@syncfusion/ej2-react-diagrams';

// Disable page editing
<DiagramComponent
  constraints={DiagramConstraints.Default & ~DiagramConstraints.PageEditable}
/>

// Enable connector bridging
<DiagramComponent
  constraints={DiagramConstraints.Default | DiagramConstraints.Bridging}
/>

// Disable zoom + page editing together
<DiagramComponent
  constraints={DiagramConstraints.Default & ~(DiagramConstraints.PageEditable | DiagramConstraints.Zoom)}
/>
```

Key `DiagramConstraints` values:
| Value | Effect |
|---|---|
| `Zoom` | Enable/disable zoom |
| `PanX` / `PanY` | Horizontal / vertical pan |
| `Undo/redo` | History tracking |
| `PageEditable` | Allow content editing |
| `Bridging` | Connector bridge overlaps |
| `Virtualization` | Large diagram performance |
| `LineRouting` | Auto-route connectors |

### Node Constraints

```tsx
import { NodeConstraints } from '@syncfusion/ej2-react-diagrams';

const nodes: NodeModel[] = [{
  id: 'n1',
  offsetX: 200, offsetY: 200,
  // Disable rotate + resize
  constraints: NodeConstraints.Default & ~(NodeConstraints.Rotate | NodeConstraints.Resize),
}];

// Enable shadow
constraints: NodeConstraints.Default | NodeConstraints.Shadow

// Enable tooltip (also set tooltip property)
constraints: NodeConstraints.Default | NodeConstraints.Tooltip
```

### Connector Constraints

```tsx
import { ConnectorConstraints } from '@syncfusion/ej2-react-diagrams';

const connectors: ConnectorModel[] = [{
  id: 'c1', type: 'Orthogonal',
  sourcePoint: { x: 100, y: 100 }, targetPoint: { x: 300, y: 200 },
  // Lock endpoints
  constraints: ConnectorConstraints.Default & ~(ConnectorConstraints.DragSourceEnd | ConnectorConstraints.DragTargetEnd),
}];
```

### Selector Constraints

Control which resize/rotate handles appear on selection:

```tsx
import { SelectorConstraints } from '@syncfusion/ej2-react-diagrams';

// Hide rotation handle
<DiagramComponent
  selectedItems={{ constraints: SelectorConstraints.All & ~SelectorConstraints.Rotate }}
/>

// Hide all resize handles
<DiagramComponent
  selectedItems={{ constraints: SelectorConstraints.All & ~SelectorConstraints.ResizeAll }}
/>
```

### Boundary Constraints

Limit drag/drop to the page area:

```tsx
<DiagramComponent
  pageSettings={{ boundaryConstraints: 'Page', width: 800, height: 600 }}
/>
```

---

## Commands

Diagram provides programmatic commands for alignment, sizing, clipboard, grouping, ordering, zoom, and nudge.

### Alignment

```tsx
// Align selected nodes to the left of the selection boundary
diagramInstance.align('Left', diagramInstance.selectedItems.nodes, 'Selector');

// Other options: 'Right' | 'Center' | 'Top' | 'Bottom' | 'Middle'
```

### Distribution

```tsx
// Distribute nodes with equal spacing (right-to-left)
diagramInstance.distribute('RightToLeft', diagramInstance.selectedItems.nodes);
```

### Sizing

```tsx
// Make all selected nodes the same width as the first node
diagramInstance.sameSize('Width', diagramInstance.nodes);
// Options: 'Width' | 'Height' | 'Size'
```

### Clipboard

```tsx
diagramInstance.cut();   // Cut selected
diagramInstance.copy();  // Copy selected
diagramInstance.paste(); // Paste clipboard

// Paste specific nodes at defined positions
diagramInstance.paste([{ id: 'n1', offsetX: 400, offsetY: 100, width: 100 }]);
```

Keyboard shortcuts: **Ctrl+X**, **Ctrl+C**, **Ctrl+V**

### Grouping

```tsx
diagramInstance.group();   // Ctrl+G
diagramInstance.unGroup(); // Ctrl+Shift+U
```

### Z-Order

```tsx
diagramInstance.bringToFront();  // Ctrl+Shift+F
diagramInstance.sendToBack();    // Ctrl+Shift+B
diagramInstance.moveForward();   // Ctrl+]
diagramInstance.sendBackward();  // Ctrl+[
```

### Zoom and Fit

```tsx
// Zoom programmatically
diagramInstance.zoomTo({ type: 'ZoomIn', zoomFactor: 0.2, focusPoint: { x: 0.5, y: 0.5 } });
diagramInstance.zoomTo({ type: 'ZoomOut', zoomFactor: 0.2 });

// Fit entire diagram into view
diagramInstance.fitToPage({ mode: 'Page', region: 'Content', canZoomIn: false });
diagramInstance.fitToPage({ mode: 'Width', region: 'Content', canZoomIn: false });
```

### Nudge

```tsx
// Move selected elements 1px in a direction
diagramInstance.nudge('Up');
diagramInstance.nudge('Down');
diagramInstance.nudge('Left');
diagramInstance.nudge('Right');
```

Arrow keys move by 1px; **Shift+Arrow** moves by 5px.

### Bring Into View / Bring to Center

```tsx
import { Rect } from '@syncfusion/ej2-react-diagrams';

const bounds = diagramInstance.nodes[0].wrapper.bounds;
const rect   = new Rect(bounds.x, bounds.y, bounds.width, bounds.height);

diagramInstance.bringIntoView(rect);  // Scroll node into viewport
diagramInstance.bringToCenter(rect);  // Center node in viewport
```

### Custom Command Manager

Bind custom logic to keyboard shortcuts:

```tsx
import { CommandManager, Keys, KeyModifiers } from '@syncfusion/ej2-react-diagrams';

const commandManager: CommandManager = {
  commands: [{
    name: 'customClone',
    canExecute: () => diagramInstance.selectedItems.nodes.length > 0,
    execute: () => { diagramInstance.copy(); diagramInstance.paste(); },
    gesture: { key: Keys.G, keyModifiers: KeyModifiers.None },
  }],
};

<DiagramComponent commandManager={commandManager} ... />
```

### Built-in Keyboard Shortcuts Reference

| Shortcut | Action |
|---|---|
| Ctrl+A | Select all |
| Ctrl+Z / Ctrl+Y | Undo / Redo |
| Ctrl+C / Ctrl+V / Ctrl+X | Copy / Paste / Cut |
| Ctrl+G / Ctrl+Shift+U | Group / Ungroup |
| Delete | Delete selected |
| F2 | Start label edit |
| Esc | Stop label edit |
| Ctrl+R / Ctrl+L | Rotate CW / CCW |
| Ctrl+H / Ctrl+J | Flip horizontal / vertical |
| Ctrl++ / Ctrl+- | Zoom in / out |

---

## Undo and Redo

Requires the `UndoRedo` module to be injected.

### Basic Usage

```tsx
import { UndoRedo } from '@syncfusion/ej2-react-diagrams';

<DiagramComponent ...>
  <Inject services={[UndoRedo]} />
</DiagramComponent>

// Programmatic undo/redo
diagramInstance.undo();  // Ctrl+Z
diagramInstance.redo();  // Ctrl+Y
```

### Group Multiple Actions into One Undo Step

```tsx
diagramInstance.startGroupAction();

// Make several changes
diagramInstance.nodes[0].style.fill = 'red';
diagramInstance.nodes[1].style.fill = 'blue';
diagramInstance.dataBind();

diagramInstance.endGroupAction();
// Now a single Ctrl+Z undoes both changes together
```

### Limit History Stack Size

```tsx
<DiagramComponent
  historyManager={{ stackLimit: 20 }}
  ...
>
  <Inject services={[UndoRedo]} />
</DiagramComponent>
```

### Prevent Specific Actions from Being Recorded

```tsx
diagramInstance.historyManager.canLog = (entry) => {
  // Returning entry.cancel = true prevents the entry from being logged
  if (entry.type === 'PositionChanged') {
    entry.cancel = true;
  }
  return entry;
};
```

### Check Undo/Redo Availability

```tsx
const canUndo = diagramInstance.historyManager.canUndo;
const canRedo = diagramInstance.historyManager.canRedo;

// Clear all history
diagramInstance.clearHistory();

// Retrieve stacks
const undoStack = diagramInstance.getHistoryStack(true);   // undo
const redoStack  = diagramInstance.getHistoryStack(false);  // redo
```

### History Change Event

```tsx
import { IHistoryChangeArgs } from '@syncfusion/ej2-react-diagrams';

<DiagramComponent
  historyChange={(args: IHistoryChangeArgs) => {
    console.log('History changed:', args.change);
  }}
  ...
>
  <Inject services={[UndoRedo]} />
</DiagramComponent>
```

---

## Context Menu

Requires the `DiagramContextMenu` module. Also add `@syncfusion/ej2-navigations` CSS to your styles.

### Enable Default Context Menu

```tsx
import { DiagramContextMenu, Inject } from '@syncfusion/ej2-react-diagrams';

<DiagramComponent
  contextMenuSettings={{ show: true }}
  ...
>
  <Inject services={[DiagramContextMenu]} />
</DiagramComponent>
```

### Custom Context Menu Items

```tsx

import { useRef } from 'react';
import {DiagramComponent, DiagramContextMenu, DiagramMenuEventArgs, Inject, NodeModel } from '@syncfusion/ej2-react-diagrams';

const nodes: NodeModel[] = [
  {
    id: 'node1',
    offsetX: 100, offsetY: 200,
    width: 60, height: 60,
  },
];

export default function App() {
  const diagramRef = useRef<DiagramComponent>(null);
  return (
     <DiagramComponent
     ref={diagramRef}
     nodes={nodes}
     width={1000}
     height={500}
  contextMenuSettings={{
    show: true,
    showCustomMenuOnly: true, // hide default items
    items: [
      {
        text: 'Fill Color',
        id: 'fill',
        target: '.e-elementcontent',
        iconCss: 'e-icons e-paint-bucket',
        items: [
          { id: 'red',  text: 'Red'  },
          { id: 'blue', text: 'Blue' },
        ],
      },
      { text: 'Clone', id: 'clone', target: '.e-elementcontent', iconCss: 'e-icons e-copy' },
    ],
  }}
  contextMenuClick={(args: DiagramMenuEventArgs) => {
    const diagram = diagramRef.current;
    if (!diagram) return;
    const node = diagram.selectedItems.nodes![0];
    if (!node) return;
    if (args.item.text === 'Red')   { node.style!.fill = 'red';  diagram.dataBind(); }
    if (args.item.text === 'Blue')  { node.style!.fill = 'blue'; diagram.dataBind(); }
    if (args.item.id  === 'clone')  { diagram.copy(); diagram.paste(); }
  }}

>
  <Inject services={[DiagramContextMenu]} />
</DiagramComponent>
  );
}
```

### Conditionally Hide Menu Items

```tsx
import { DiagramBeforeMenuOpenEventArgs } from '@syncfusion/ej2-react-diagrams';

contextMenuOpen={(args: DiagramBeforeMenuOpenEventArgs) => {
  const node      = diagramInstance.selectedItems.nodes[0];
  const connector = diagramInstance.selectedItems.connectors[0];
  if (node || connector) {
    args.hiddenItems = ['selectAll'];
  } else {
    args.hiddenItems = ['applyFill', 'applyStroke'];
  }
}}
```

### Context Menu Events

| Event | Description |
|---|---|
| `contextMenuBeforeItemRender` | Fires before each menu item renders (use for templates) |
| `contextMenuOpen` | Fires when menu opens (use to hide/show items) |
| `contextMenuClick` | Fires when a menu item is clicked |

---

## User Handles

User handles are icons that appear around a selected element for quick actions.

### Define User Handles

```tsx

import { useRef } from 'react';
import { DiagramComponent, NodeModel, UserHandleModel } from '@syncfusion/ej2-react-diagrams';

const nodes: NodeModel[] = [
  {
    id: 'node1',
    offsetX: 100, offsetY: 200,
    width: 60, height: 60,
  },
];
const userHandles: UserHandleModel[] = [{
  name: 'clone',
  pathData: 'M0 0 L100 0 L100 80 L0 80 Z',  // SVG path
  offset: 1,
  side: 'Bottom',
  horizontalAlignment: 'Left',
  verticalAlignment: 'Bottom',
  margin: { left: 5, bottom: 5 },
  tooltip: { content: 'Clone Node' },
  // Appearance
  size: 30,
  borderWidth: 2,
  borderColor: '#6BA5D7',
  backgroundColor: '#fff',
  pathColor: '#6BA5D7',
  visible: true,
}];
export default function App() {
  const diagramRef = useRef<DiagramComponent>(null);
  return (
    <DiagramComponent
      selectedItems={{ userHandles }}
      ref={diagramRef}
      width={1000}
      height={500}
      nodes={nodes}
      onUserHandleMouseDown={(args) => {
        const diagram = diagramRef.current;
        if (args.element.name === 'clone') {
          diagram.copy();
          diagram.paste();
        }
      }}

    />
  );
}


```

### Alignment Options

| `offset` | `side` | Position |
|---|---|---|
| 0 | Left | Top-left corner |
| 1 | Bottom | Bottom-right area |
| 0.5 | Top | Top-center |

### Selectively Disable for Nodes or Connectors

```tsx
const userHandles: UserHandleModel[] = [
  { name: 'nodeOnly',      ..., disableConnectors: true },
  { name: 'connectorOnly', ..., disableNodes: true      },
  { name: 'both',          ...                          },
];
```

### User Handle Events

| Event | Description |
|---|---|
| `onUserHandleMouseDown` | Mouse button pressed on handle |
| `onUserHandleMouseUp` | Mouse button released on handle |
| `onUserHandleMouseEnter` | Mouse enters handle region |
| `onUserHandleMouseLeave` | Mouse leaves handle region |
| `click` | Handle clicked |

---

## Fixed User Handles

Fixed user handles are permanently visible on specific nodes or connectors regardless of selection state.

```tsx

import { useRef } from 'react';
import { DiagramComponent, NodeModel } from '@syncfusion/ej2-react-diagrams';
const nodes: NodeModel[] = [{
  id: 'n1',
  offsetX: 250, offsetY: 250,
  width: 100, height: 100,
  fixedUserHandles: [{
    id: 'colorHandle',
    pathData: 'M0 0 L100 0 L100 80 L0 80 Z',
    width: 20, height: 20,
    offset: { x: 1, y: 0 },     // top-right corner
    margin: { left: 20 },
    fill: 'white',
    handleStrokeColor: '#6BA5D7',
    iconStrokeColor: '#6BA5D7',
    cornerRadius: 4,
    tooltip: { content: 'Change color' },
  }],
}];
export default function App() {
  const diagramRef = useRef<DiagramComponent>(null);
  return (
<DiagramComponent
  nodes={nodes}
  ref={diagramRef}
  width={1000}
  height={500}
  fixedUserHandleClick={(args) => {
      const diagram = diagramRef.current;
    if (args.fixedUserHandle.id === 'colorHandle') {
      args.element.style.fill = '#6BA5D7';
      diagram.dataBind();
    }
  }}

/>
  );
}
```

> **Tip:** Each `fixedUserHandle` id must be unique across the diagram.

---

## Best Practices

- **Inject only needed modules** — each service (UndoRedo, DiagramContextMenu, ConnectorEditing) adds overhead; inject only what your diagram uses.
- **Use `startGroupAction` / `endGroupAction`** when making batch programmatic changes so users can undo them in a single step.
- **Set `stackLimit`** to cap history size in applications with heavy editing to prevent memory growth.
- **Use `showCustomMenuOnly: true`** when implementing a fully custom context menu to avoid conflicts with default items.
- **Set `disableNodes` / `disableConnectors`** on user handles to avoid showing irrelevant actions for an element type.
- **Apply constraints at the element level** (node/connector) rather than globally when possible to preserve selective interactivity.
- **Use `boundaryConstraints: 'Page'`** to prevent users from accidentally moving content outside the visible area.

---

## Troubleshooting

**Undo/Redo not working:**
- Ensure `UndoRedo` is injected via `<Inject services={[UndoRedo]} />`.
- Check that `DiagramConstraints.Default` is set (it includes undo/redo by default); verify it hasn't been removed.

**Context menu not appearing:**
- Inject `DiagramContextMenu` and set `contextMenuSettings={{ show: true }}`.
- Add the navigations CSS import: `@import "~@syncfusion/ej2-navigations/styles/material.css"`.

**User handles not visible:**
- Define handles in `selectedItems.userHandles` — they only show when an element is selected.
- For always-visible handles, use `fixedUserHandles` on the node/connector definition.

**Drawing tool reverts to select after one draw:**
- `DiagramTools.DrawOnce` is intended for single draws. Use `DiagramTools.ContinuousDraw` to keep drawing.

**Resize handles not showing:**
- Check `SelectorConstraints` — `SelectorConstraints.ResizeAll` must be included.
- Verify node-level `NodeConstraints.Resize` is not disabled.

**Cannot connect to a port:**
- Check `PortConstraints.InConnect` / `PortConstraints.OutConnect` are enabled on the port.
- Ensure `NodeConstraints.InConnect` / `NodeConstraints.OutConnect` are set on the target/source node.
