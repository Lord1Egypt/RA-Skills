# Connectors in Syncfusion React Diagram

## Table of Contents
- [Connector Fundamentals](#connector-fundamentals)
- [Creating Connectors](#creating-connectors)
- [Connector Types](#connector-types)
- [Connecting Nodes](#connecting-nodes)
- [Connecting via Ports](#connecting-via-ports)
- [Decorator Customization](#decorator-customization)
- [Connector Style](#connector-style)
- [getConnectorDefaults Pattern](#getconnectordefaults-pattern)
- [Runtime Connector Operations](#runtime-connector-operations)
- [Line Routing](#line-routing)
- [Connector Events](#connector-events)
- [Advanced Properties](#advanced-properties)
- [Troubleshooting](#troubleshooting)

---

## Connector Fundamentals

Connectors are lines/arrows that link two points, nodes, or ports. Three things uniquely describe a connector:

| Concern | Properties |
|---------|-----------|
| **Endpoints** | `sourcePoint`/`targetPoint` (coordinates) or `sourceID`/`targetID` (node IDs) |
| **Path type** | `type`: `Straight` \| `Orthogonal` \| `Bezier` |
| **Appearance** | `style`, `sourceDecorator`, `targetDecorator` |

> **ID rules:** Connector IDs must start with a letter. No spaces, underscores, or special characters.

---

## Creating Connectors

### Freestanding connector (point-to-point)

```tsx
import { DiagramComponent, ConnectorModel } from '@syncfusion/ej2-react-diagrams';

const connectors: ConnectorModel[] = [
  {
    id: 'c1',
    sourcePoint: { x: 100, y: 100 },
    targetPoint: { x: 300, y: 250 }
  }
];

export default function App() {
  return (
    <DiagramComponent id="diagram" width={'100%'} height={'400px'} connectors={connectors} />
  );
}
```

### Node-to-node connector

```tsx
const connectors: ConnectorModel[] = [
  {
    id: 'c1',
    sourceID: 'node1',   // matches a node's id
    targetID: 'node2',   // matches a node's id
    type: 'Orthogonal'
  }
];
```

---

## Connector Types

Choose the `type` property based on the visual style you need:

| Type | Description | Best for |
|------|-------------|---------|
| `Straight` | Direct line between endpoints | Simple relationships, entity diagrams |
| `Orthogonal` | Right-angle path (default routing) | Flowcharts, org charts, structured diagrams |
| `Bezier` | Smooth curved path | Mind maps, creative diagrams |

### Straight connector

```tsx
const connector: ConnectorModel = {
  id: 'straight1',
  type: 'Straight',
  sourcePoint: { x: 100, y: 100 },
  targetPoint: { x: 300, y: 200 }
};
```

### Orthogonal connector

Routes through right angles automatically. The diagram engine calculates the path to avoid overlapping nodes when `LineRouting` is enabled.

```tsx
const connector: ConnectorModel = {
  id: 'ortho1',
  type: 'Orthogonal',
  sourceID: 'nodeA',
  targetID: 'nodeB',
  // Optional: explicit segments override auto-routing
  segments: [
    { type: 'Orthogonal', direction: 'Right', length: 80 },
    { type: 'Orthogonal', direction: 'Bottom', length: 100 }
  ]
};
```

### Bezier connector

```tsx
const connector: ConnectorModel = {
  id: 'bezier1',
  type: 'Bezier',
  sourcePoint: { x: 100, y: 200 },
  targetPoint: { x: 400, y: 200 },
  // Optional: control points for curvature
  segments: [
    {
      type: 'Bezier',
      point1: { x: 200, y: 100 },  // first control point
      point2: { x: 300, y: 300 }   // second control point
    }
  ]
};
```

### Corner radius (Orthogonal only)

Rounds the corners on orthogonal connectors for a softer look:

```tsx
const connector: ConnectorModel = {
  id: 'rounded',
  type: 'Orthogonal',
  sourceID: 'nodeA',
  targetID: 'nodeB',
  cornerRadius: 10   // pixels
};
```

Apply globally via `getConnectorDefaults`:

```tsx
getConnectorDefaults={(obj: ConnectorModel) => {
  obj.type = 'Orthogonal';
  obj.cornerRadius = 8;
  return obj;
}}
```

---

## Connecting Nodes

### Basic node-to-node connection

```tsx
import { DiagramComponent, NodeModel, ConnectorModel } from '@syncfusion/ej2-react-diagrams';

const nodes: NodeModel[] = [
  { id: 'start', offsetX: 150, offsetY: 150, width: 120, height: 50,
    shape: { type: 'Flow', shape: 'Terminator' },
    annotations: [{ content: 'Start' }] },
  { id: 'process', offsetX: 150, offsetY: 280, width: 120, height: 50,
    shape: { type: 'Flow', shape: 'Process' },
    annotations: [{ content: 'Process' }] }
];

const connectors: ConnectorModel[] = [
  { id: 'c1', sourceID: 'start', targetID: 'process', type: 'Orthogonal' }
];
```

### Restricting incoming/outgoing connections

Remove `InConnect` to prevent incoming connections to a node; remove `OutConnect` to block outgoing connections:

```tsx
import { NodeConstraints } from '@syncfusion/ej2-react-diagrams';

const node: NodeModel = {
  id: 'sourceOnly',
  // This node can only be a source — no connectors can point TO it
  constraints: NodeConstraints.Default & ~NodeConstraints.InConnect
};
```

---

## Connecting via Ports

Use `sourcePortID` and `targetPortID` to anchor connectors at specific named ports on nodes instead of the node center.

```tsx
import { NodeModel, ConnectorModel, PointPortModel, PortVisibility } from '@syncfusion/ej2-react-diagrams';

const nodes: NodeModel[] = [
  {
    id: 'node1',
    offsetX: 150, offsetY: 150, width: 100, height: 100,
    ports: [
      { id: 'rightPort', offset: { x: 1, y: 0.5 },
        visibility: PortVisibility.Visible,
        shape: 'Circle', style: { fill: '#366F8C' } }
    ]
  },
  {
    id: 'node2',
    offsetX: 350, offsetY: 150, width: 100, height: 100,
    ports: [
      { id: 'leftPort', offset: { x: 0, y: 0.5 },
        visibility: PortVisibility.Visible,
        shape: 'Circle', style: { fill: '#366F8C' } }
    ]
  }
];

const connectors: ConnectorModel[] = [
  {
    id: 'portConnector',
    sourceID: 'node1',
    targetID: 'node2',
    sourcePortID: 'rightPort',   // connect from right side of node1
    targetPortID: 'leftPort',    // connect to left side of node2
    type: 'Straight'
  }
];
```

### Change port connection at runtime

```tsx
const diagramRef = useRef<DiagramComponent>(null);

const reconnect = () => {
  const connector = diagramRef.current!.connectors[0];
  connector.sourcePortID = 'bottomPort';
  connector.targetPortID = 'topPort';
  diagramRef.current!.dataBind();
};
```

---

## Decorator Customization

Decorators are the shapes at the source and target ends (arrows, circles, diamonds, etc.).

### Available decorator shapes

`None` | `Arrow` | `OpenArrow` | `Circle` | `Square` | `Diamond` | `IndentedArrow` | `OutdentedArrow` | `DoubleArrow` | `Custom`

### Common decorator configurations

```tsx
const connector: ConnectorModel = {
  id: 'c1',
  sourcePoint: { x: 100, y: 150 },
  targetPoint: { x: 350, y: 150 },

  // No arrow at source end
  sourceDecorator: { shape: 'None' },

  // Styled arrow at target end
  targetDecorator: {
    shape: 'Arrow',
    width: 12,
    height: 12,
    style: {
      fill: '#2196F3',
      strokeColor: '#2196F3'
    }
  }
};
```

### Circle source + custom target

```tsx
const connector: ConnectorModel = {
  id: 'c2',
  type: 'Straight',
  sourcePoint: { x: 100, y: 100 },
  targetPoint: { x: 300, y: 200 },
  sourceDecorator: { shape: 'Circle' },
  targetDecorator: {
    shape: 'Custom',
    pathData: 'M0,0 L10,5 L0,10 Z'   // SVG path for custom arrowhead
  }
};
```

### Diamond decorator (typical for class diagrams)

```tsx
targetDecorator: { shape: 'Diamond', width: 14, height: 14 }
```

---

## Connector Style

### Stroke properties

```tsx
const connector: ConnectorModel = {
  id: 'styled',
  sourcePoint: { x: 100, y: 100 },
  targetPoint: { x: 300, y: 200 },
  style: {
    strokeColor: '#1565C0',    // line color
    strokeWidth: 2,            // line thickness
    strokeDashArray: '8 4',    // dashed: "dashLen gapLen"
    opacity: 0.8               // 0–1
  }
};
```

### Dashed line patterns

| Pattern | `strokeDashArray` |
|---------|------------------|
| Solid | (omit / empty string) |
| Dashed | `'8 4'` |
| Dotted | `'2 3'` |
| Long dash | `'12 4'` |
| Dash-dot | `'8 3 2 3'` |

---

## getConnectorDefaults Pattern

`getConnectorDefaults` runs for every connector before rendering. Use it to enforce a consistent style across all connectors without repeating properties:

```tsx
<DiagramComponent
  id="diagram"
  width={'100%'} height={'500px'}
  nodes={nodes}
  connectors={connectors}
  getConnectorDefaults={(obj: ConnectorModel): ConnectorModel => {
    obj.type = 'Orthogonal';
    obj.cornerRadius = 8;
    obj.targetDecorator = { shape: 'Arrow', width: 10, height: 10 };
    obj.style = { strokeColor: '#455A64', strokeWidth: 1.5 };
    return obj;
  }}
/>
```

### Org-chart / layout defaults (minimal decorators)

```tsx
getConnectorDefaults={(obj: ConnectorModel): ConnectorModel => {
  obj.type = 'Orthogonal';
  obj.targetDecorator = { shape: 'None' };   // no arrows in org charts
  obj.style = {
    strokeColor: '#6BA5D7',
    strokeWidth: 2
  };
  return obj;
}}
```

---

## Runtime Connector Operations

### Add a connector

```tsx
const diagramRef = useRef<DiagramComponent>(null);

const addConnector = () => {
  const newConnector: ConnectorModel = {
    id: 'dynamic1',
    sourceID: 'nodeA',
    targetID: 'nodeC',
    type: 'Orthogonal'
  };
  diagramRef.current!.add(newConnector);
};
```

### Remove a connector

```tsx
const removeConnector = () => {
  const connector = diagramRef.current!.getObject('dynamic1');
  diagramRef.current!.remove(connector);
};
```

### Add multiple connectors at once

```tsx
const batch: ConnectorModel[] = [
  { id: 'c1', sourcePoint: { x: 80, y: 80 }, targetPoint: { x: 150, y: 150 } },
  { id: 'c2', type: 'Orthogonal', sourcePoint: { x: 170, y: 170 }, targetPoint: { x: 300, y: 300 } }
];
diagramRef.current!.addElements(batch);
```

### Update connector properties at runtime

```tsx
const updateConnector = () => {
  const c = diagramRef.current!.connectors[0];
  c.style.strokeColor = '#E53935';
  c.style.strokeWidth = 3;
  c.targetDecorator.style.fill = '#E53935';
  c.sourcePoint.x = 150;
  diagramRef.current!.dataBind();  // required to reflect changes
};
```

### Clone a connector

```tsx
const cloneConnector = () => {
  const diagram = diagramRef.current!;
  diagram.select([diagram.connectors[0]]);
  diagram.copy();
  diagram.paste();
};
```

---

## Line Routing

Line routing automatically re-routes orthogonal connectors around nodes so they don't overlap.

### Enable line routing

Inject `LineRouting` and add its constraint to the diagram:

```tsx
import { Diagram, DiagramComponent, LineRouting, DiagramConstraints } from '@syncfusion/ej2-react-diagrams';

// Inject the module (outside the component, once)
Diagram.Inject(LineRouting);

export default function App() {
  return (
    <DiagramComponent
      id="diagram"
      width={'100%'} height={'600px'}
      nodes={nodes}
      connectors={connectors}
      constraints={DiagramConstraints.Default | DiagramConstraints.LineRouting}
    />
  );
}
```

### Disable routing on a specific connector

```tsx
import { ConnectorConstraints } from '@syncfusion/ej2-react-diagrams';

const connector: ConnectorModel = {
  id: 'manual',
  sourceID: 'nodeA', targetID: 'nodeB',
  type: 'Orthogonal',
  // Opt this connector out of auto-routing
  constraints: ConnectorConstraints.Default & ~ConnectorConstraints.InheritLineRouting
};
```

### Avoid line overlapping

Prevents multiple orthogonal connectors from stacking on top of each other. Requires `LineRouting`:

```tsx
import { Diagram, DiagramComponent, LineRouting, AvoidLineOverlapping, DiagramConstraints } from '@syncfusion/ej2-react-diagrams';

Diagram.Inject(LineRouting, AvoidLineOverlapping);

<DiagramComponent
  constraints={
    DiagramConstraints.Default |
    DiagramConstraints.LineRouting |
    DiagramConstraints.AvoidLineOverlapping
  }
/>
```

> `AvoidLineOverlapping` only works with `Orthogonal` connectors and requires `LineRouting` to be active.

---

## Connector Events

All events are props on `DiagramComponent`. Use `args.state` to differentiate `'Changing'` (cancelable) from `'Changed'` (completed).

### Click

```tsx
import { IClickEventArgs, Connector } from '@syncfusion/ej2-react-diagrams';

<DiagramComponent
  click={(args: IClickEventArgs) => {
    if (args.actualObject instanceof Connector) {
      console.log('Connector clicked:', (args.actualObject as ConnectorModel).id);
    }
  }}
/>
```

### Connection change (connector endpoint changed)

Fires when a connector's source or target is changed by dragging its endpoint onto a different node/port.

```tsx
connectionChange={(args: IConnectionChangeEventArgs) => {
  if (args.state === 'Changed') {
    console.log('New target:', args.connector.targetID);
  }
  // Prevent the reconnection:
  // if (args.state === 'Changing') args.cancel = true;
}}
```

### Segment change (connector path reshaping)

Fires when a user drags a segment of an editable connector.

```tsx
segmentChange={(args: ISegmentChangeEventArgs) => {
  if (args.state === 'Completed') {
    console.log('Segments updated');
  }
}}
```

### Position change (connector drag)

```tsx
positionChange={(args: IDraggingEventArgs) => {
  if (args.state === 'Completed') {
    console.log('Connector moved');
  }
  // Prevent drag: if (args.state === 'Progress') args.cancel = true;
}}
```

### Collection change (connector added/removed)

```tsx
collectionChange={(args: ICollectionChangeEventArgs) => {
  if (args.state === 'Changed') {
    console.log('Connector collection changed');
  }
  // Prevent: if (args.state === 'Changing') args.cancel = true;
}}
```

---

## Advanced Properties

| Property | Type | Description |
|----------|------|-------------|
| `type` | `'Straight' \| 'Orthogonal' \| 'Bezier'` | Connector path style |
| `segments` | `ConnectorSegmentModel[]` | Manual path segment definitions |
| `sourceDecorator` | `DecoratorModel` | Shape at the source end |
| `targetDecorator` | `DecoratorModel` | Shape at the target end |
| `cornerRadius` | `number` | Rounds orthogonal connector corners |
| `sourceID` / `targetID` | `string` | Connect to nodes by ID |
| `sourcePortID` / `targetPortID` | `string` | Connect to specific ports by ID |
| `sourcePoint` / `targetPoint` | `PointModel` | Freestanding endpoint coordinates |
| `constraints` | `ConnectorConstraints` | Enable/disable edit, select, drag, routing |
| `bridgeSpace` | `number` | Gap size when bridge (arc) is drawn over crossing connectors |
| `addInfo` | `any` | Custom metadata attached to the connector |
| `tooltip` | `DiagramTooltipModel` | Tooltip shown on hover |
| `annotations` | `PathAnnotationModel[]` | Text labels along the connector path |

---

## Troubleshooting

**Connector not connecting to a node**
- Confirm `sourceID`/`targetID` match the exact `id` values of the target nodes
- Check that `NodeConstraints.InConnect` / `OutConnect` are not removed from the node

**Port connection not working**
- Ensure the `id` values in `sourcePortID`/`targetPortID` match ports defined in the node's `ports` array
- Verify ports have `visibility: PortVisibility.Visible` if you need them shown

**Orthogonal connector not routing around nodes**
- Inject `LineRouting` via `Diagram.Inject(LineRouting)` (not inside the component)
- Add `DiagramConstraints.LineRouting` to the `constraints` prop on `DiagramComponent`

**Runtime style change not reflecting**
- Call `diagramRef.current!.dataBind()` after mutating connector properties directly

**`AvoidLineOverlapping` not working**
- Check that `LineRouting` is also injected and its constraint is enabled
- This feature only applies to `Orthogonal` connectors

**Related docs:**
- Ports → [ports.md](ports.md)
- Labels on connectors → [labels-and-annotations.md](labels-and-annotations.md)
- Bezier details → see `connector-bezier.md` in docs/
- Connector segments → see `connector-segments.md` in docs/
