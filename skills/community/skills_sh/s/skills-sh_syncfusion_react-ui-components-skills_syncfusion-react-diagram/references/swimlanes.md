# Swimlanes in Syncfusion React Diagram

## Table of Contents
- [Swimlane Overview](#swimlane-overview)
- [Creating a Swimlane](#creating-a-swimlane)
- [Swimlane Orientation](#swimlane-orientation)
- [Headers](#headers)
- [Lanes](#lanes)
- [Phases](#phases)
- [Adding Children to Lanes](#adding-children-to-lanes)
- [Runtime Operations](#runtime-operations)
- [Swimlane Palette](#swimlane-palette)
- [Swimlane Interaction](#swimlane-interaction)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## Swimlane Overview

Swimlanes are specialized diagram nodes that organize process activities into distinct lanes representing departments, roles, or responsibility areas. They are ideal for:

- Cross-functional process flows (order fulfillment, onboarding)
- BPMN-style pool/lane diagrams
- Any workflow where "who does what" must be visible

A swimlane node has this structure:

```
SwimLane node
├── header          (swimlane title)
├── phases[]        (vertical/horizontal dividers across all lanes)
└── lanes[]
    ├── lane header (lane label — e.g. "Customer", "Finance")
    └── children[]  (nodes placed inside the lane)
```

> Connectors **cannot** be added directly to a swimlane. They must be added to the diagram, not to lane children.

---

## Creating a Swimlane

Set `shape.type` to `'SwimLane'` on any node. The minimal configuration requires at least one lane:

```tsx
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { DiagramComponent, NodeModel } from '@syncfusion/ej2-react-diagrams';

const nodes: NodeModel[] = [
  {
    id: 'swimlane1',
    shape: {
      type: 'SwimLane',
      orientation: 'Horizontal',
      header: {
        annotation: { content: 'ONLINE PURCHASE STATUS' },
        height: 50,
        style: { fontSize: 11 },
      },
      lanes: [
        {
          id: 'laneCustomer',
          height: 100,
          header: {
            annotation: { content: 'CUSTOMER' },
            width: 50,
            style: { fontSize: 11 },
          },
        },
        {
          id: 'laneStore',
          height: 100,
          header: {
            annotation: { content: 'STORE' },
            width: 50,
            style: { fontSize: 11 },
          },
        },
      ],
      phases: [
        { id: 'phase1', offset: 170, header: { annotation: { content: 'Order' } } },
        { id: 'phase2', offset: 320, header: { annotation: { content: 'Ship' } } },
      ],
      phaseSize: 20,
    },
    offsetX: 350,
    offsetY: 250,
    height: 250,
    width: 500,
  },
];

export default function App() {
  return (
    <DiagramComponent id="container" width="100%" height="600px" nodes={nodes} />
  );
}
```

> **ID constraints:** Swimlane IDs must not contain spaces, underscores, or start with numbers or special characters.

---

## Swimlane Orientation

| Orientation | Lane layout | Header position |
|---|---|---|
| `Horizontal` (default) | Lanes stack top-to-bottom | Left side |
| `Vertical` | Lanes stack left-to-right | Top |

```tsx
shape: {
  type: 'SwimLane',
  orientation: 'Vertical',   // or 'Horizontal'
  ...
}
```

---

## Headers

The swimlane header provides the overall title. Configure it via `shape.header`:

```tsx
header: {
  annotation: { content: 'SALES PROCESS' },
  height: 60,              // height for Horizontal orientation
  style: {
    fontSize: 14,
    fontStyle: 'Bold',
    fill: '#0078d4',
    color: 'white',
  },
}
```

### Dynamic Header Update

```tsx
const diagramRef = useRef<DiagramComponent>(null);

function updateHeader() {
  const node = diagramRef.current?.nodes[0];
  if (node) {
    (node.shape as any).header.style.fill = 'darkblue';
    diagramRef.current?.dataBind();
  }
}
```

### Inline Header Editing

Double-click the header label to edit it in place. The diagram raises the standard annotation edit events during this interaction.

---

## Lanes

Each lane in `lanes[]` represents a row (Horizontal) or column (Vertical) of the swimlane.

### Lane Properties

| Property | Type | Description |
|---|---|---|
| `id` | string | Unique identifier (required) |
| `height` | number | Height of the lane (Horizontal mode) |
| `width` | number | Width of the lane (Vertical mode) |
| `header` | HeaderModel | Lane label configuration |
| `style` | ShapeStyleModel | Fill color, stroke, etc. |
| `children` | NodeModel[] | Nodes pre-placed inside the lane |

### Lane with Styled Header

```tsx
lanes: [
  {
    id: 'laneFinance',
    height: 120,
    header: {
      annotation: {
        content: 'Finance',
        style: { fill: 'white', color: '#333' },
      },
      width: 60,
      style: { fill: '#e8f4fd', fontSize: 12 },
    },
    style: { fill: '#f0f8ff' },
  },
]
```

### Adding Lanes Dynamically

```tsx
import { SwimlaneModel } from '@syncfusion/ej2-react-diagrams';

diagramRef.current?.addLanes(
  diagramRef.current.getObject('swimlane1'),
  [{ id: 'newLane', height: 100, header: { annotation: { content: 'New Dept' } } }], 1
);
```

### Removing a Lane

```tsx
const swimlane = diagramRef.current?.getObject('swimlane1');
const lane = (swimlane?.shape as SwimlaneModel)?.lanes?.[0];
diagramRef.current?.removeLane(swimlane, lane);
```

---

## Phases

Phases divide the swimlane into time-based or process-based stages (columns in Horizontal, rows in Vertical). They span **across all lanes**.

### Phase Properties

| Property | Type | Description |
|---|---|---|
| `id` | string | Unique identifier |
| `offset` | number | Position of the phase divider in pixels from origin |
| `header` | HeaderModel | Phase label |
| `style` | ShapeStyleModel | Visual styling |

```tsx
phases: [
  { id: 'p1', offset: 150, header: { annotation: { content: 'Phase 1: Initiate' } } },
  { id: 'p2', offset: 300, header: { annotation: { content: 'Phase 2: Execute' } } },
  { id: 'p3', offset: 450, header: { annotation: { content: 'Phase 3: Close' } } },
],
phaseSize: 30,   // height of the phase header strip
```

### Adding a Phase at Runtime

```tsx
const swimlane = diagramRef.current?.getObject('swimlane1');
diagramRef.current?.addPhases(swimlane, [
  { id: 'phase4', offset: 600, header: { annotation: { content: 'Phase 4: Review' } } },
]);
```

### Removing a Phase

```tsx
const swimlane = diagramRef.current?.getObject('swimlane1');
const phase = (swimlane?.shape as SwimlaneModel)?.phases?.[2]; // third phase
diagramRef.current?.removePhase(swimlane, phase);
```

---

## Adding Children to Lanes

Place nodes inside lanes by including them in `lane.children`. Each child is positioned relative to the lane's top-left corner.

```tsx
lanes: [
  {
    id: 'laneCustomer',
    height: 120,
    header: { annotation: { content: 'Customer' }, width: 50 },
    children: [
      {
        id: 'placeOrder',
        width: 100,
        height: 50,
        margin: { left: 60, top: 30 },
        annotations: [{ content: 'Place Order' }],
        style: { fill: '#dae8fc', strokeColor: '#6c8ebf' },
      },
      {
        id: 'receiveGoods',
        width: 100,
        height: 50,
        margin: { left: 200, top: 20 },
        annotations: [{ content: 'Receive Goods' }],
        style: { fill: '#dae8fc', strokeColor: '#6c8ebf' },
      },
    ],
  },
]
```

Connectors between children are added to the **diagram** (not the lane):

```tsx
const connectors: ConnectorModel[] = [
  { id: 'c1', sourceID: 'placeOrder', targetID: 'receiveGoods', type: 'Orthogonal' },
];

<DiagramComponent ... nodes={nodes} connectors={connectors} />
```

### Adding a Child Node to a Lane at Runtime

```tsx
import { NodeModel } from '@syncfusion/ej2-react-diagrams';

const newNode: NodeModel = {
  id: 'processReturn',
  width: 100,
  height: 50,
  offsetX: 400,
  offsetY: 60,
  annotations: [{ content: 'Process Return' }],
};

diagramRef.current?.addNodeToLane(newNode, 
  diagramRef.current.getObject('swimlane1'),
  'laneCustomer'
);
```

---

## Runtime Operations

| Operation | Method |
|---|---|
| Add lane | `diagram.addLanes(swimlane, [laneModel])` |
| Remove lane | `diagram.removeLane(swimlane, lane)` |
| Add phase | `diagram.addPhases(swimlane, [phaseModel])` |
| Remove phase | `diagram.removePhase(swimlane, phase)` |
| Add node to lane | `diagram.addNodeToLane(swimlane, laneId, node)` |
| Get swimlane object | `diagram.getObject(id)` |

---

## Swimlane Palette

Use the `SymbolPaletteComponent` to provide drag-and-drop swimlane templates. The `swimlane-palette.md` docs describe configuring swimlane symbols within the palette:

```tsx
import { SymbolPaletteComponent, PaletteModel } from '@syncfusion/ej2-react-diagrams';

const swimlanePalette: PaletteModel[] = [
  {
    id: 'swimlanes',
    title: 'Swimlanes',
    symbols: [
      {
        id: 'horizontalSwimlane',
        shape: {
          type: 'SwimLane',
          orientation: 'Horizontal',
          lanes: [{ id: 'lane1', height: 60 }, { id: 'lane2', height: 60 }],
          phases: [{ id: 'phase1', offset: 200 }],
          phaseSize: 20,
        },
        width: 300, height: 150,
      },
    ],
  },
];

<SymbolPaletteComponent palettes={swimlanePalette} width="100%" height="400px" />
```

---

## Swimlane Interaction

- **Select**: Click the swimlane header to select the entire swimlane.
- **Drag**: Drag the header to move the entire swimlane (all lanes and phases move together).
- **Resize**: Drag lane/phase borders to resize individual sections.
- **Edit header**: Double-click any header annotation to edit its text inline.
- **Add lane**: Right-click in the swimlane context menu → "Add Lane Before" / "Add Lane After".

### Constraints

Use `NodeConstraints` on the swimlane to lock interaction:

```tsx
import { NodeConstraints } from '@syncfusion/ej2-react-diagrams';

{
  id: 'swimlane1',
  constraints: NodeConstraints.Default & ~NodeConstraints.Drag,  // prevent dragging
  shape: { type: 'SwimLane', ... }
}
```

---

## Best Practices

- Keep lane IDs short and meaningful; they are referenced in runtime operations.
- Use `phaseSize` values of 20–40 for readable phase labels.
- For processes with many steps, use `orientation: 'Horizontal'` (wider swimlane) vs. `Vertical` (taller).
- Place connectors at the diagram level, not inside lanes — they cannot be children of a lane.
- Ensure `offsetX`/`offsetY` values for lane children are within the lane's dimensions to prevent misplacement.

---

## Troubleshooting

**Nodes inside a lane not visible**
→ Check that `offsetX`/`offsetY` of children are within the lane `width`/`height`. If out of bounds, they may render outside the visible lane area.

**Header editing not triggering**
→ Double-click must land exactly on the annotation text. Make sure `annotations` is set on the header.

**Connector from one lane to another not connecting**
→ Connectors between lane children must be defined at the diagram level (in the top-level `connectors` prop), not inside the lane.

**Phase not appearing**
→ Confirm `phaseSize` is > 0. If `phaseSize` is 0, the phase header strip renders with zero height and appears invisible.

**addLanes / addPhases not working at runtime**
→ Retrieve the swimlane object via `diagram.getObject(id)` rather than from `diagram.nodes[index]` — the shape reference must be live.
