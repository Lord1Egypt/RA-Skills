# Nodes in Syncfusion React Diagram

## Table of Contents
- [Node Fundamentals](#node-fundamentals)
- [Creating Nodes](#creating-nodes)
- [Positioning and Sizing](#positioning-and-sizing)
- [Node Appearance and Style](#node-appearance-and-style)
- [getNodeDefaults Pattern](#getnodedefaults-pattern)
- [Runtime Node Operations](#runtime-node-operations)
- [Expand and Collapse](#expand-and-collapse)
- [Node Events](#node-events)
- [Advanced Properties](#advanced-properties)
- [Troubleshooting](#troubleshooting)

---

## Node Fundamentals

Every node has four core properties:

| Property | Purpose | Default |
|----------|---------|---------|
| `id` | Unique identifier — must start with a letter | auto-generated |
| `offsetX` / `offsetY` | Center position on the canvas | `0` / `0` |
| `width` / `height` | Size in pixels | `100` / `100` |
| `style` | Fill, stroke, opacity | theme default |

> Nodes are stacked in the order they are added — later nodes appear on top. Use `zIndex` to override this.

---

## Creating Nodes

### Via the `nodes` collection (declarative)

```tsx
import * as React from 'react';
import { DiagramComponent, NodeModel } from '@syncfusion/ej2-react-diagrams';

const nodes: NodeModel[] = [
  {
    id: 'node1',
    offsetX: 250,
    offsetY: 200,
    width: 120,
    height: 60,
    style: { fill: '#6BA5D7', strokeColor: 'white' },
    annotations: [{ content: 'Step 1' }]
  },
  {
    id: 'node2',
    offsetX: 450,
    offsetY: 200,
    width: 120,
    height: 60,
    style: { fill: '#357BD2', strokeColor: 'white' },
    annotations: [{ content: 'Step 2' }]
  }
];

export default function App() {
  return (
    <DiagramComponent id="diagram" width={'100%'} height={'400px'} nodes={nodes} />
  );
}
```

### Via interactive drawing tool

Use `DiagramTools.DrawOnce` or `DiagramTools.ContinuousDraw` to let users draw nodes on the canvas:

```tsx
import { DiagramComponent, DiagramTools } from '@syncfusion/ej2-react-diagrams';
import { useRef } from 'react';

export default function App() {
  const diagramRef = useRef<DiagramComponent>(null);

  return (
    <DiagramComponent
      id="diagram"
      width={'100%'}
      height={'500px'}
      ref={diagramRef}
      created={() => {
        const diagram = diagramRef.current!;
        diagram.drawingObject = { shape: { type: 'Basic', shape: 'Rectangle' } };
        diagram.tool = DiagramTools.ContinuousDraw;
        diagram.dataBind();
      }}
    />
  );
}
```

---

## Positioning and Sizing

`offsetX` and `offsetY` define the **center** of the node (default pivot is `{x: 0.5, y: 0.5}`).

```tsx
// Node centered at (300, 200)
const node: NodeModel = {
  id: 'box',
  offsetX: 300,  // horizontal center
  offsetY: 200,  // vertical center
  width: 120,
  height: 60
};
```

### Changing the pivot point

The `pivot` property controls which point of the node `offsetX`/`offsetY` refers to:

```tsx
// offsetX/offsetY now refers to the top-left corner
const node: NodeModel = {
  id: 'box',
  offsetX: 100, offsetY: 100,
  width: 120, height: 60,
  pivot: { x: 0, y: 0 }   // top-left
  // pivot: { x: 0.5, y: 0.5 }  // center (default)
  // pivot: { x: 1, y: 1 }      // bottom-right
};
```

### Rotation

```tsx
const node: NodeModel = {
  id: 'rotated',
  offsetX: 300, offsetY: 200,
  width: 120, height: 60,
  rotateAngle: 45   // degrees clockwise
};
```

### Stack order (z-index)

```tsx
// node1 appears on top of node2 even though added later
const nodes: NodeModel[] = [
  { id: 'node1', offsetX: 260, offsetY: 260, width: 100, height: 100, zIndex: 2 },
  { id: 'node2', offsetX: 250, offsetY: 250, width: 100, height: 100, zIndex: 1 }
];
```

---

## Node Appearance and Style

### Basic style properties

```tsx
const node: NodeModel = {
  id: 'styled',
  offsetX: 250, offsetY: 250,
  width: 140, height: 60,
  style: {
    fill: '#6BA5D7',         // background color
    strokeColor: '#2D6099',  // border color
    strokeWidth: 2,          // border thickness
    strokeDashArray: '5 3',  // dashed border: "dashLen gapLen"
    opacity: 0.85            // 0 (transparent) to 1 (solid)
  }
};
```

### Visibility

```tsx
// Hide a node without removing it
const node: NodeModel = { id: 'hidden', visible: false, /* ... */ };
```

### Corner radius (for rectangle-like shapes)

```tsx
const node: NodeModel = {
  id: 'rounded',
  shape: { type: 'Basic', shape: 'Rectangle', cornerRadius: 12 }
};
```

### Shadow effect

Enable via `NodeConstraints` then configure with the `shadow` property:

```tsx
import { NodeConstraints } from '@syncfusion/ej2-react-diagrams';

const node: NodeModel = {
  id: 'shadow-node',
  offsetX: 300, offsetY: 200,
  width: 140, height: 60,
  constraints: NodeConstraints.Default | NodeConstraints.Shadow,
  shadow: {
    color: 'rgba(0,0,0,0.4)',
    angle: 45,        // shadow direction in degrees
    distance: 8,      // shadow offset in pixels
    opacity: 0.6
  }
};
```

### Linear gradient fill

```tsx
import { GradientModel } from '@syncfusion/ej2-react-diagrams';

const gradient: GradientModel = {
  type: 'Linear',
  x1: 0, y1: 0,   // start point (% of node size)
  x2: 100, y2: 0, // end point
  stops: [
    { color: '#ffffff', offset: 0 },
    { color: '#6BA5D7', offset: 100 }
  ]
};

const node: NodeModel = {
  id: 'gradient-node',
  style: { gradient: gradient }
};
```

### Radial gradient fill

```tsx
const gradient: GradientModel = {
  type: 'Radial',
  cx: 50, cy: 50,  // center of outer circle (% of node)
  fx: 30, fy: 30,  // focal point of inner circle
  r: 50,           // radius
  stops: [
    { color: '#ffffff', offset: 0 },
    { color: '#357BD2', offset: 100 }
  ]
};
```

### Storing custom data on a node

Use `addInfo` to attach arbitrary metadata to a node:

```tsx
const node: NodeModel = {
  id: 'task1',
  addInfo: { priority: 'High', assignee: 'Alice', dueDate: '2026-04-01' }
};

// Read it back:
const info = diagram.nodes[0].addInfo as { priority: string };
```

---

## getNodeDefaults Pattern

`getNodeDefaults` runs for every node before rendering. Use it to apply consistent styling without repeating properties on every node definition:

```tsx
<DiagramComponent
  id="diagram"
  width={'100%'}
  height={'500px'}
  nodes={nodes}
  getNodeDefaults={(node: NodeModel): NodeModel => {
    // Apply to all nodes
    node.width = node.width ?? 140;
    node.height = node.height ?? 50;
    node.style = {
      fill: '#1565C0',
      strokeColor: 'white',
      strokeWidth: 1
    };
    return node;
  }}
/>
```

> Values set in `getNodeDefaults` take higher priority in rendering. Individual node properties can override them by being set explicitly.

### Data-driven defaults (org-chart pattern)

```tsx
getNodeDefaults={(node: NodeModel): NodeModel => {
  const data = node.data as { role: string; name: string };
  const roleColors: Record<string, string> = {
    Director: '#B71C1C',
    Manager: '#1565C0',
    Lead: '#2E7D32',
  };
  node.width = 140;
  node.height = 50;
  node.style = {
    fill: roleColors[data?.role] ?? '#455A64',
    strokeColor: 'white'
  };
  node.annotations = [{ content: data?.name, style: { color: 'white' } }];
  return node;
}}
```

---

## Runtime Node Operations

### Add a single node

```tsx
const diagramRef = useRef<DiagramComponent>(null);

const addNode = () => {
  const newNode: NodeModel = {
    id: 'dynamic1',
    offsetX: 300, offsetY: 300,
    width: 120, height: 50,
    annotations: [{ content: 'New Node' }]
  };
  diagramRef.current!.add(newNode);
};
```

### Remove a node

```tsx
const removeNode = () => {
  const node = diagramRef.current!.getObject('dynamic1') as NodeModel;
  diagramRef.current!.remove(node);
};
```

### Add multiple nodes at once

```tsx
const nodes: NodeModel[] = [
  { id: 'n1', offsetX: 100, offsetY: 200 },
  { id: 'n2', offsetX: 250, offsetY: 200 },
  { id: 'n3', offsetX: 400, offsetY: 200 }
];

diagramRef.current!.addElements(nodes);
```

### Update node properties at runtime

```tsx
// Direct property mutation + dataBind to sync
const updateNode = () => {
  const node = diagramRef.current!.nodes[0];
  node.style.fill = 'orange';
  node.width = 180;
  diagramRef.current!.dataBind();  // required to reflect changes
};
```

### Clone (copy + paste) a node

```tsx
const cloneNode = () => {
  const diagram = diagramRef.current!;
  diagram.select([diagram.nodes[0]]);
  diagram.copy();
  diagram.paste();  // pastes at a slight offset from original
};
```

### Find connected connectors

```tsx
// inEdges: connectors ending at this node
// outEdges: connectors starting at this node
const node = diagram.nodes[0];
const outConnector = diagram.getObject(node.outEdges[0]);
const inConnector = diagram.getObject(node.inEdges[0]);
```

---

## Expand and Collapse

Expand/collapse icons appear on nodes that have outgoing connectors (`outEdges`). They are used in hierarchical layouts to toggle child visibility.

```tsx
import { DiagramComponent, HierarchicalTree, DataBinding, Inject } from '@syncfusion/ej2-react-diagrams';

<DiagramComponent
  id="diagram"
  width={'100%'} height={'500px'}
  layout={{ type: 'HierarchicalTree' }}
  dataSourceSettings={{ id: 'id', parentId: 'parentId', dataManager: items }}
  getNodeDefaults={(node: NodeModel) => {
    node.width = 120; node.height = 50;
    // Show expand/collapse toggle icons
    node.expandIcon = {
      shape: 'Minus',  // shown when node is expanded
      width: 15, height: 15
    };
    node.collapseIcon = {
      shape: 'Plus',   // shown when node is collapsed
      width: 15, height: 15
    };
    return node;
  }}
>
  <Inject services={[HierarchicalTree, DataBinding]} />
</DiagramComponent>
```

**Available icon shapes:** `None`, `Minus`, `Plus`, `ArrowUp`, `ArrowDown`, `ArrowLeft`, `ArrowRight`, `Template`, `Path`

> Icons only appear on nodes that have `outEdges` (i.e. nodes that are parents in the layout). They have no effect on leaf nodes.

### Set initial collapsed state

```tsx
// Start with node collapsed (children hidden)
const node: NodeModel = {
  id: 'parent',
  isExpanded: false   // true = expanded (default)
};
```

---

## Node Events

All events are set as props on `DiagramComponent`. Use `args.state` to differentiate `'Changing'` (preventable) from `'Changed'` (completed).

### Click

```tsx
<DiagramComponent
  click={(args: IClickEventArgs) => {
    if (args.actualObject instanceof Node) {
      console.log('Node clicked:', (args.actualObject as NodeModel).id);
    }
  }}
/>
```

### Selection change

```tsx
selectionChange={(args: ISelectionChangeEventArgs) => {
  if (args.state === 'Changed') {
    console.log('Selected nodes:', args.newValue);
  }
  // Prevent selection:
  // if (args.state === 'Changing') args.cancel = true;
}}
```

### Position change (drag)

```tsx
positionChange={(args: IDraggingEventArgs) => {
  if (args.state === 'Completed') {
    const node = args.source as NodeModel;
    console.log(`Moved to: ${node.offsetX}, ${node.offsetY}`);
  }
  // Prevent drag:
  // if (args.state === 'Progress') args.cancel = true;
}}
```

### Size change (resize)

```tsx
sizeChange={(args: ISizeChangeEventArgs) => {
  if (args.state === 'Completed') {
    console.log('New size:', args.newValue);
  }
  // Prevent resize:
  // if (args.state === 'Progress') args.cancel = true;
}}
```

### Rotate change

```tsx
rotateChange={(args: IRotationEventArgs) => {
  if (args.state === 'Completed') {
    console.log('New angle:', (args.source as NodeModel).rotateAngle);
  }
}}
```

### Collection change (add/remove)

```tsx
collectionChange={(args: ICollectionChangeEventArgs) => {
  if (args.state === 'Changed') {
    console.log('Nodes changed');
  }
  // Prevent add/remove:
  // if (args.state === 'Changing') args.cancel = true;
}}
```

### Mouse enter / leave (hover highlight)

```tsx
const diagramRef = useRef<DiagramComponent>(null);

mouseEnter={(args: MouseEventArgs) => {
  (args.actualObject as NodeModel).style.fill = '#FFF9C4';
  diagramRef.current!.dataBind();
}}
mouseLeave={(args: MouseEventArgs) => {
  (args.actualObject as NodeModel).style.fill = '#6BA5D7';
  diagramRef.current!.dataBind();
}}
```

---

## Advanced Properties

| Property | Type | Description |
|----------|------|-------------|
| `visible` | `boolean` | Show/hide node without removing it |
| `zIndex` | `number` | Stack order; higher = in front |
| `rotateAngle` | `number` | Clockwise rotation in degrees |
| `pivot` | `{x, y}` | Reference point for offset/rotation (0–1) |
| `constraints` | `NodeConstraints` | Enable/disable drag, resize, select, shadow, etc. |
| `isExpanded` | `boolean` | Initial expand/collapse state in tree layouts |
| `expandIcon` / `collapseIcon` | `IconShapeModel` | Toggle icons for hierarchy layouts |
| `addInfo` | `any` | Custom metadata attached to the node |
| `inEdges` | `string[]` | Read-only: IDs of connectors ending at this node |
| `outEdges` | `string[]` | Read-only: IDs of connectors starting from this node |
| `tooltip` | `DiagramTooltipModel` | Tooltip shown on hover |

---

## Troubleshooting

**Node not visible after adding**
- Check `offsetX`/`offsetY` are within the diagram `width`/`height`
- Ensure `visible` is not `false`
- Verify `style.opacity` is not `0`

**Runtime property change not reflected**
- Call `diagramRef.current!.dataBind()` after mutating node properties directly

**`getNodeDefaults` overwriting individual node styles**
- Use conditional logic in `getNodeDefaults`: only set properties that aren't already defined (`node.width = node.width ?? 140`)

**Expand/collapse icons not appearing**
- Icons only render when a node has `outEdges` — the node must have at least one connector starting from it
- Inject `HierarchicalTree` (or the relevant layout module) when using hierarchical layouts

**Related docs:**
- Shapes → [shapes-and-styles.md](shapes-and-styles.md)
- Connectors → [connectors.md](connectors.md)
- Annotations → [labels-and-annotations.md](labels-and-annotations.md)
- Ports → [ports.md](ports.md)
- Layouts → [layouts.md](layouts.md)
