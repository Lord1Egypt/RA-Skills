# Ports in Syncfusion React Diagram

## Table of Contents
- [Port Fundamentals](#port-fundamentals)
- [Creating Ports](#creating-ports)
- [Port Positioning](#port-positioning)
- [Port Appearance](#port-appearance)
- [Port Constraints](#port-constraints)
- [Drawing Connectors from Ports](#drawing-connectors-from-ports)
- [Port Drag](#port-drag)
- [Automatic Port Creation](#automatic-port-creation)
- [Port Tooltip](#port-tooltip)
- [Runtime Port Operations](#runtime-port-operations)
- [Port Events](#port-events)
- [Advanced Properties](#advanced-properties)
- [Troubleshooting](#troubleshooting)

---

## Port Fundamentals

Ports are named connection points on a node. Connectors attached to ports remain fixed to those exact positions even when a node is moved, rotated, or resized. This ensures predictable, professional layouts.

| Connection Type | How endpoints bind | When to use |
|----------------|-------------------|-------------|
| Node-to-node | Auto-finds shortest boundary path | Simple diagrams |
| Port-to-port | Fixed at named port positions | Technical diagrams, flowcharts |

> **ID rules:** Port IDs must start with a letter. No spaces, underscores, or special characters.

---

## Creating Ports

### Declarative (at initialization)

```tsx
import { DiagramComponent, NodeModel, PortVisibility } from '@syncfusion/ej2-react-diagrams';

const nodes: NodeModel[] = [
  {
    id: 'node1',
    offsetX: 250, offsetY: 250,
    width: 100, height: 100,
    ports: [
      { id: 'topPort',    offset: { x: 0.5, y: 0 }, visibility: PortVisibility.Visible },
      { id: 'rightPort',  offset: { x: 1,   y: 0.5 }, visibility: PortVisibility.Visible },
      { id: 'bottomPort', offset: { x: 0.5, y: 1 }, visibility: PortVisibility.Visible },
      { id: 'leftPort',   offset: { x: 0,   y: 0.5 }, visibility: PortVisibility.Visible }
    ]
  }
];
```

### Connect via ports

```tsx
const connectors: ConnectorModel[] = [
  {
    id: 'c1',
    sourceID: 'node1', targetID: 'node2',
    sourcePortID: 'rightPort',
    targetPortID: 'leftPort',
    type: 'Orthogonal'
  }
];
```

---

## Port Positioning

The `offset` property uses fractional `{x, y}` values (0–1) relative to the node's bounds:
- `(0, 0)` = top-left corner
- `(1, 1)` = bottom-right corner
- `(0.5, 0.5)` = center

### Standard port positions

```tsx
ports: [
  { id: 'top',    offset: { x: 0.5, y: 0   }, visibility: PortVisibility.Visible },
  { id: 'right',  offset: { x: 1,   y: 0.5 }, visibility: PortVisibility.Visible },
  { id: 'bottom', offset: { x: 0.5, y: 1   }, visibility: PortVisibility.Visible },
  { id: 'left',   offset: { x: 0,   y: 0.5 }, visibility: PortVisibility.Visible }
]
```

### Alignment and margin

Fine-tune position beyond offset using `horizontalAlignment`, `verticalAlignment`, and `margin`:

```tsx
ports: [{
  id: 'topLeftOuter',
  offset: { x: 0, y: 0 },
  visibility: PortVisibility.Visible,
  horizontalAlignment: 'Left',    // 'Left' | 'Center' | 'Right'
  verticalAlignment: 'Top',       // 'Top' | 'Center' | 'Bottom'
  margin: { left: 50 }   // push outside node boundary
}]
```

---

## Port Appearance

```tsx
import { PortVisibility } from '@syncfusion/ej2-react-diagrams';

ports: [{
  offset: { x: 1, y: 0.5 },
  visibility: PortVisibility.Visible,
  shape: 'Circle',          // 'Circle' | 'Square' | 'X' | 'Custom'
  width: 12,
  height: 12,
  style: {
    fill: '#366F8C',
    strokeColor: '#1a3b50',
    strokeWidth: 2,
    opacity: 0.9,
    strokeDashArray: '2 2'
  }
}]
```

### Port visibility options

| `PortVisibility` | When shown |
|-----------------|-----------|
| `Hidden` | Never (default) |
| `Visible` | Always |
| `Hover` | On mouse hover |
| `Connect` | When a connector thumb hovers over the node |

### Custom port shape

```tsx
ports: [{
  offset: { x: 0.5, y: 1 },
  visibility: PortVisibility.Visible,
  shape: 'Custom',
  pathData: 'M50 10 L60 40 L90 40 L65 60 L75 90 L50 70 L25 90 L35 60 L10 40 L40 40 Z',
  width: 20,
  height: 20
}]
```

### Update port appearance at runtime

```tsx
const port = diagramRef.current!.nodes[0].ports[0];
port.style.fill = 'yellow';
port.style.opacity = 1;
port.width = 20;
port.height = 20;
diagramRef.current!.dataBind();
```

---

## Port Constraints

| Constraint | Behavior |
|-----------|---------|
| `None` | All behaviors disabled |
| `Draw` | User can draw connectors from this port |
| `InConnect` | Accepts incoming connectors |
| `OutConnect` | Accepts outgoing connectors |
| `Drag` | Port can be dragged to reposition |
| `ToolTip` | Shows tooltip on hover |

```tsx
import { PortConstraints, PortVisibility } from '@syncfusion/ej2-react-diagrams';

ports: [{
  id: 'p1',
  offset: { x: 1, y: 0.5 },
  visibility: PortVisibility.Visible,
  // Enable draw + tooltip; disable incoming connections
  constraints: PortConstraints.Draw | PortConstraints.ToolTip | PortConstraints.OutConnect
}]
```

---

## Drawing Connectors from Ports

Enable `PortConstraints.Draw` to allow users to interactively draw connectors from a port:

```tsx
import { DiagramComponent, NodeModel, PortVisibility, PortConstraints } from '@syncfusion/ej2-react-diagrams';

const nodes: NodeModel[] = [
  {
    id: 'node1',
    offsetX: 250, offsetY: 250,
    width: 100, height: 100,
    ports: [{
      id: 'rightPort',
      offset: { x: 1, y: 0.5 },
      visibility: PortVisibility.Visible,
      constraints: PortConstraints.Default | PortConstraints.Draw
    }]
  }
];
```

### Change default drawn connector type

```tsx
<DiagramComponent
  nodes={nodes}
  getConnectorDefaults={(connector) => {
    connector.type = 'Bezier';   // default drawn connectors will be Bezier
    return connector;
  }}
/>
```

---

## Port Drag

Allow users to drag ports to reposition them on the node:

```tsx
ports: [{
  offset: { x: 1, y: 0.5 },
  visibility: PortVisibility.Visible,
  constraints: PortConstraints.Default | PortConstraints.Drag
}]
```

---

## Automatic Port Creation

Let users Ctrl+click to create/remove ports dynamically anywhere on a node:

```tsx
import { DiagramComponent, DiagramConstraints, NodeConstraints } from '@syncfusion/ej2-react-diagrams';

<DiagramComponent
  constraints={DiagramConstraints.Default | DiagramConstraints.AutomaticPortCreation}
  nodes={[
    {
      id: 'node1',
      offsetX: 200, offsetY: 200,
      width: 100, height: 100,
      // Disable built-in InConnect/OutConnect to use only auto-created ports
      constraints: NodeConstraints.Default & ~(NodeConstraints.InConnect | NodeConstraints.OutConnect)
    }
  ]}
/>
```

> Ctrl+click on an **unconnected** port removes it. Connected ports cannot be removed this way.

---

## Port Tooltip

```tsx
import { PortConstraints, PortVisibility } from '@syncfusion/ej2-react-diagrams';

ports: [{
  id: 'tooltipPort',
  offset: { x: 1, y: 0.5 },
  visibility: PortVisibility.Visible,
  constraints: PortConstraints.Default | PortConstraints.ToolTip,
  tooltip: { content: 'Connect here' }
}]
```

---

## Runtime Port Operations

### Add ports

```tsx
import { PointPortModel, PortVisibility } from '@syncfusion/ej2-react-diagrams';

const newPorts: PointPortModel[] = [
  { id: 'port1', offset: { x: 0, y: 0.5 }, visibility: PortVisibility.Visible },
  { id: 'port2', offset: { x: 1, y: 0.5 }, visibility: PortVisibility.Visible }
];

diagramRef.current!.addPorts(diagramRef.current!.nodes[0], newPorts);
```

### Remove ports

```tsx
const ports = [{ id: 'port1' }, { id: 'port2' }];
diagramRef.current!.removePorts(diagramRef.current!.nodes[0], ports);
```

### Update port position

```tsx
diagramRef.current!.nodes[0].ports[0].offset = { x: 0.5, y: 0 };
diagramRef.current!.dataBind();
```

### Change connection direction

```tsx
diagramRef.current!.nodes[0].ports[0].connectionDirection = 'Top';
// Options: 'Auto' | 'Left' | 'Right' | 'Top' | 'Bottom'
```

### Read in/out edges of a port

`inEdges` and `outEdges` are read-only arrays of connector IDs:

```tsx
const port = diagramRef.current!.nodes[0].ports[0];
console.log('Incoming connectors:', port.inEdges);
console.log('Outgoing connectors:', port.outEdges);
```

---

## Port Events

| Event | Description |
|-------|-------------|
| `click` | Port was clicked |
| `elementDraw` | User started drawing a connector from the port |
| `positionChange` | Port dragged to new position |
| `connectionChange` | Connector connected/disconnected from port |

```tsx
import {
  IClickEventArgs, IElementDrawEventArgs,
  IDraggingEventArgs, IConnectionChangeEventArgs,
  Connector
} from '@syncfusion/ej2-react-diagrams';

<DiagramComponent
  click={(args: IClickEventArgs) => {
    console.log('Clicked element:', args.actualObject);
  }}
  elementDraw={(args: IElementDrawEventArgs) => {
    // Prevent connectors drawn from connector ports
    if (args.state === 'Start' && args.source instanceof Connector) {
      args.cancel = true;
    }
  }}
  positionChange={(args: IDraggingEventArgs) => {
    if (args.state === 'Completed') {
      console.log('Port moved');
    }
  }}
  connectionChange={(args: IConnectionChangeEventArgs) => {
    if (args.state === 'Changed') {
      console.log('Port connection changed');
    }
  }}
/>
```

---

## Advanced Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | `string` | Unique port identifier (letter-first, no underscores) |
| `offset` | `PointModel` | Fractional `{x, y}` position on node |
| `shape` | `'Circle' \| 'Square' \| 'X' \| 'Custom'` | Visual shape |
| `pathData` | `string` | SVG path for `'Custom'` shape |
| `width` / `height` | `number` | Port size in pixels |
| `style` | `ShapeStyleModel` | fill, strokeColor, strokeWidth, opacity |
| `visibility` | `PortVisibility` | When port is shown |
| `constraints` | `PortConstraints` | Interaction capabilities |
| `connectionDirection` | `'Auto' \| 'Left' \| 'Right' \| 'Top' \| 'Bottom'` | Allowed connector flow direction |
| `horizontalAlignment` | `string` | Horizontal alignment at offset point |
| `verticalAlignment` | `string` | Vertical alignment at offset point |
| `margin` | `MarginModel` | Spacing around port |
| `tooltip` | `DiagramTooltipModel` | Hover tooltip |
| `addInfo` | `any` | Custom metadata |
| `inEdges` | `string[]` (read-only) | IDs of incoming connectors |
| `outEdges` | `string[]` (read-only) | IDs of outgoing connectors |

---

## Troubleshooting

**Port not visible**
- Set `visibility: PortVisibility.Visible` explicitly (default is `Hidden`)
- For hover-only visibility use `PortVisibility.Hover`

**Connector won't attach to specific port**
- Confirm `sourcePortID`/`targetPortID` exactly match the port's `id`
- Ensure port has `PortConstraints.InConnect` or `OutConnect` enabled

**Drawn connectors start from wrong point**
- Verify port has `PortConstraints.Draw` enabled
- Remove `NodeConstraints.InConnect`/`OutConnect` if you want only port-based connections

**Runtime port change not reflecting**
- Always call `diagramRef.current!.dataBind()` after modifying port properties

**Auto-created port won't delete**
- Ports with active connector attachments cannot be removed via Ctrl+click

**Related docs:**
- Connectors → [connectors.md](connectors.md)
- Labels → [labels-and-annotations.md](labels-and-annotations.md)
- Interaction → [interaction-and-tools.md](interaction-and-tools.md)
