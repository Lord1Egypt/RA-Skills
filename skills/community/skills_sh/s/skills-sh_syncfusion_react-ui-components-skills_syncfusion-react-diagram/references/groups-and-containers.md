# Groups and Containers in Syncfusion React Diagram

## Table of Contents
- [Groups vs Containers](#groups-vs-containers)
- [Creating Groups](#creating-groups)
- [Group Runtime Operations](#group-runtime-operations)
- [Managing Group Children at Runtime](#managing-group-children-at-runtime)
- [Creating Containers](#creating-containers)
- [Container Headers](#container-headers)
- [Container Padding](#container-padding)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## Groups vs Containers

| Feature | Group | Container |
|---|---|---|
| Type | Regular node with `children[]` | Node with `shape.type = 'Container'` |
| Visible boundary | No explicit border by default | Always has a visible bounding box |
| Header support | No built-in header | Optional title via `shape.header` |
| Child layout | Children positioned manually | Children use `margin` for internal layout |
| Auto-sizing | Grows to fit children | Grows to fit children + padding |
| Use case | Selecting/moving related nodes together | Labelled container boxes (e.g. UML packages, swimlane cells) |

Choose **Groups** when nodes need to move/resize together without a visible frame.
Choose **Containers** when a visible boundary with an optional title is needed.

---

## Creating Groups

A group is a node with a `children` array of child node IDs. Child nodes must be defined **before** the group in the `nodes` array.

### Declarative Group Definition

```tsx
import { useRef } from 'react';
import { DiagramComponent, NodeModel } from '@syncfusion/ej2-react-diagrams';

const nodes: NodeModel[] = [
  {
    id: 'node1',
    offsetX: 100, offsetY: 100,
    width: 100, height: 80,
    annotations: [{ content: 'Node 1' }],
    style: { fill: '#6BA5D7', strokeColor: 'white' },
  },
  {
    id: 'node2',
    offsetX: 250, offsetY: 100,
    width: 100, height: 80,
    annotations: [{ content: 'Node 2' }],
    style: { fill: '#357BD2', strokeColor: 'white' },
  },
  {
    // Group node — must come AFTER its children in the array
    id: 'group1',
    children: ['node1', 'node2'],   // IDs of children
    style: { strokeWidth: 2, strokeColor: '#888' },
    padding: { left: 10, right: 10, top: 10, bottom: 10 },
  },
];

export default function App() {
  const diagramRef = useRef<DiagramComponent>(null);
  return (
    <DiagramComponent
      id="container"
      ref={diagramRef}
      width="100%" height="500px"
      nodes={nodes}
    />
  );
}
```

### Group with Connectors as Children

Connectors can also be part of a group, so they move with the group:

```tsx
import { useRef } from 'react';
import { DiagramComponent, ConnectorModel, NodeModel } from '@syncfusion/ej2-react-diagrams';

const connectors: ConnectorModel[] = [
  { id: 'c1', type: 'Orthogonal', sourceID: 'node1', targetID: 'node2' },
];

const nodes: NodeModel[] = [
  { id: 'node1', offsetX: 100, offsetY: 100, width: 100, height: 80 },
  { id: 'node2', offsetX: 300, offsetY: 100, width: 100, height: 80 },
  {
    id: 'group1',
    children: ['node1', 'node2', 'c1'],  // connector included
    style: { strokeWidth: 0 },           // hide group border
  },
];

export default function App() {
  const diagramRef = useRef<DiagramComponent>(null);
  return (
    <DiagramComponent
      id="container"
      ref={diagramRef}
      width="100%" height="500px"
      nodes={nodes}
      connectors={connectors}
    />
  );
}
```

---

## Group Runtime Operations

### Group Selected Nodes

Programmatically group whatever is currently selected:

```tsx
const diagramRef = useRef<DiagramComponent>(null);

function groupSelected() {
  diagramRef.current?.group();
}

// Ensure nodes are selected first:
function selectAndGroup() {
  const n1 = diagramRef.current?.getObject('node1') as NodeModel;
  const n2 = diagramRef.current?.getObject('node2') as NodeModel;
  diagramRef.current?.select([n1, n2]);
  diagramRef.current?.group();
}
```

### Ungroup at Runtime

```tsx
function ungroupSelected() {
  // Select the group first, then ungroup
  const grp = diagramRef.current?.getObject('group1') as NodeModel;
  diagramRef.current?.select([grp]);
  diagramRef.current?.unGroup();
}
```

### Add a Pre-defined Group at Runtime

```tsx
const newGroup: NodeModel = {
  id: 'group2',
  children: ['node3', 'node4'],
};
diagramRef.current?.add(newGroup);
```

### Add Multiple Groups at Once

```tsx
const elements: NodeModel[] = [
  { id: 'n3', offsetX: 400, offsetY: 100, width: 100, height: 80 },
  { id: 'n4', offsetX: 540, offsetY: 100, width: 100, height: 80 },
  { id: 'grp2', children: ['n3', 'n4'], padding: { left: 8, right: 8, top: 8, bottom: 8 } },
];
diagramRef.current?.addElements(elements);
```

> The `collectionChange` event fires for each element added via `addElements`.

---

## Managing Group Children at Runtime

### Add a Child to an Existing Group

```tsx
const group = diagramRef.current?.getObject('group1') as NodeModel;
const child = diagramRef.current?.getObject('node5') as NodeModel;
diagramRef.current?.addChildToGroup(group, child);
```

### Remove a Child from a Group

```tsx
const group = diagramRef.current?.getObject('group1') as NodeModel;
const child = diagramRef.current?.getObject('node2') as NodeModel;
diagramRef.current?.removeChildFromGroup(group, child);
```

> After removing, the child node remains on the canvas as an independent node.

---

## Creating Containers

Containers use `shape.type = 'Container'` and list children by ID. Child nodes use `margin` to position themselves inside the container.

```tsx
const nodes: NodeModel[] = [
  {
    id: 'child1',
    margin: { left: 40, top: 30 },  // position relative to container top-left
    width: 110, height: 60,
    style: { fill: '#357BD2', strokeColor: 'white' },
    annotations: [{ content: 'Component A', style: { color: 'white' } }],
  },
  {
    id: 'child2',
    margin: { left: 200, top: 100 },
    width: 110, height: 60,
    style: { fill: '#6BA5D7', strokeColor: 'white' },
    annotations: [{ content: 'Component B', style: { color: 'white' } }],
  },
  {
    id: 'container1',
    width: 380, height: 220,
    offsetX: 250, offsetY: 200,
    shape: {
      type: 'Container',
      children: ['child1', 'child2'],
    },
    style: {
      fill: '#E9EEFF',
      strokeColor: '#2546BB',
      strokeWidth: 1,
    },
  },
];
```

---

## Container Headers

Add a visible title bar to a container using `shape.header`:

```tsx
{
  id: 'container1',
  width: 380, height: 250,
  offsetX: 250, offsetY: 200,
  shape: {
    type: 'Container',
    header: {
      annotation: {
        content: 'Authentication Module',
        style: { fontSize: 14, bold: true, color: 'white' },
      },
      height: 40,
      style: { fill: '#3c63ac', strokeColor: '#30518f' },
    },
    children: ['child1', 'child2'],
  },
  style: { fill: 'white', strokeColor: '#30518f', strokeDashArray: '4 4' },
}
```

| Header Property | Type | Description |
|---|---|---|
| `annotation.content` | string | Title text displayed in the header |
| `annotation.style` | TextStyleModel | Font size, bold, color, italic |
| `height` | number | Header bar height in pixels |
| `style.fill` | string | Header background color |
| `style.strokeColor` | string | Header border color |

> Double-click the header area to edit the title inline.

---

## Container Padding

Use the `padding` property on either groups or containers to add spacing between the boundary and children:

```tsx
{
  id: 'group1',
  children: ['node1', 'node2'],
  padding: { left: 15, right: 15, top: 15, bottom: 15 },
}
```

For containers, padding also affects where the auto-resize boundary stops — ensuring children have breathing room within the container frame.

---

## Best Practices

- **Child declaration order**: Always define child nodes/connectors before the group or container node in the `nodes` array.
- **Use `padding`** on groups/containers to prevent children from sitting flush against the boundary.
- **Use `margin` for container children** (not `offsetX`/`offsetY`) — container children are positioned relative to the container, not the canvas.
- **Avoid nesting too deeply**: Group-inside-group-inside-container creates complex selection/move behaviors. Keep nesting to 2 levels maximum.
- **Style group borders**: By default, a group has a visible dashed border. Set `style: { strokeWidth: 0 }` to make it invisible if you only need logical grouping.

---

## Troubleshooting

**Children not appearing inside the group/container**
→ Ensure child node IDs in `children[]` match existing node IDs exactly (case-sensitive).
→ Declare children **before** the group in the `nodes` array.

**Container children misplaced after drag**
→ Container children use `margin` for positioning — do not set `offsetX`/`offsetY` directly on children of a `Container` node.

**Group does not auto-resize around children**
→ Groups do resize to fit children. If children appear outside, verify that the children's `offsetX`/`offsetY` values are realistic relative to the group.

**`addChildToGroup` has no effect**
→ Retrieve the group via `diagram.getObject(id)` before calling the method. The group reference must be a live object from the diagram model.

**Ungrouping does not remove the group node**
→ `unGroup` dissolves the group and removes the group container — children remain on the canvas individually. If the group appears to persist, check for a second nested group.
