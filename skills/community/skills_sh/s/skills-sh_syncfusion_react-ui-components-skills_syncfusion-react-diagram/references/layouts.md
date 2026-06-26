# Layouts in Syncfusion React Diagram

## Table of Contents
- [Layout Overview](#layout-overview)
- [Required Module Injection](#required-module-injection)
- [Hierarchical Tree Layout](#hierarchical-tree-layout)
- [Organizational Chart Layout](#organizational-chart-layout)
- [Mind Map Layout](#mind-map-layout)
- [Radial Tree Layout](#radial-tree-layout)
- [Flowchart Layout](#flowchart-layout)
- [Layout Configuration Properties](#layout-configuration-properties)
- [Layout Customization](#layout-customization)
- [Layout Events](#layout-events)
- [Refreshing Layout at Runtime](#refreshing-layout-at-runtime)
- [Troubleshooting](#troubleshooting)

---

## Layout Overview

Automatic layouts position nodes and connectors without requiring manual coordinate assignment. The `layout` prop on `DiagramComponent` activates a specific algorithm; nodes are repositioned every time the data or structure changes.

| Layout Type | Module | Use Case |
|---|---|---|
| `HierarchicalTree` | `HierarchicalTree` | Multi-parent trees, dependency graphs |
| `OrganizationalChart` | `HierarchicalTree` | Reporting hierarchies, org charts |
| `MindMap` | `MindMap` | Brainstorming, knowledge maps |
| `RadialTree` | `RadialTree` | Network relationships, circular hierarchies |
| `Flowchart` | `FlowchartLayout` | Process flows, decision trees |

All layout types also require `DataBinding` when using a data source.

---

## Required Module Injection

Inject the correct modules before using any layout. Missing injection causes the layout to silently fall back to manual positioning.

```tsx
import {
  DiagramComponent, Inject,
  HierarchicalTree, DataBinding,
  MindMap, RadialTree, FlowchartLayout, LayoutAnimation
} from '@syncfusion/ej2-react-diagrams';

// Hierarchical / Org Chart
<Inject services={[DataBinding, HierarchicalTree]} />

// Mind Map
<Inject services={[DataBinding, MindMap]} />

// Radial Tree
<Inject services={[DataBinding, RadialTree]} />

// Flowchart
<Inject services={[DataBinding, FlowchartLayout]} />

// Animated layouts (add LayoutAnimation alongside the layout module)
<Inject services={[DataBinding, HierarchicalTree, LayoutAnimation]} />
```

---

## Hierarchical Tree Layout

Arranges nodes in a tree structure that supports **multiple parent nodes** per child — suitable for matrix organizations or project dependency graphs.

### With Nodes and Connectors (manual)

```tsx
import * as React from 'react';
import {
  DiagramComponent, Inject, NodeModel, ConnectorModel,
  DataBinding, HierarchicalTree
} from '@syncfusion/ej2-react-diagrams';

const nodes: NodeModel[] = [
  { id: 'CEO' },
  { id: 'VP-Engineering' },
  { id: 'VP-Sales' },
  { id: 'Dev-Lead' },
];

const connectors: ConnectorModel[] = [
  { id: 'c1', sourceID: 'CEO', targetID: 'VP-Engineering' },
  { id: 'c2', sourceID: 'CEO', targetID: 'VP-Sales' },
  { id: 'c3', sourceID: 'VP-Engineering', targetID: 'Dev-Lead' },
];

export default function App() {
  return (
    <DiagramComponent
      id="container"
      width="100%" height="550px"
      nodes={nodes}
      connectors={connectors}
      layout={{ type: 'HierarchicalTree' }}
      getNodeDefaults={(node: NodeModel) => {
        node.annotations = [{ content: node.id }];
        node.width = 100; node.height = 40;
        return node;
      }}
      getConnectorDefaults={(c: ConnectorModel) => {
        c.type = 'Orthogonal'; return c;
      }}
    >
      <Inject services={[DataBinding, HierarchicalTree]} />
    </DiagramComponent>
  );
}
```

### With DataSource (recommended for dynamic data)

```tsx
import { DataManager, Query } from '@syncfusion/ej2-data';

const data = [
  { Name: 'Steve-Ceo' },
  { Name: 'Kevin-Manager', ReportingPerson: 'Steve-Ceo' },
  { Name: 'Peter-Manager', ReportingPerson: 'Steve-Ceo' },
  { Name: 'John-Dev', ReportingPerson: 'Kevin-Manager' },
];
const items = new DataManager(data as JSON[]);

<DiagramComponent
  layout={{ type: 'HierarchicalTree' }}
  dataSourceSettings={{ id: 'Name', parentId: 'ReportingPerson', dataSource: items }}
  getNodeDefaults={(node: NodeModel) => {
    node.annotations = [{ content: (node.data as any).Name }];
    node.width = 100; node.height = 40;
    return node;
  }}
  getConnectorDefaults={(c: ConnectorModel) => { c.type = 'Orthogonal'; return c; }}
>
  <Inject services={[DataBinding, HierarchicalTree]} />
</DiagramComponent>
```

---

## Organizational Chart Layout

Similar to `HierarchicalTree` but adds `getLayoutInfo` for subtree orientation, alignment, and **assistant nodes**.

### Basic Org Chart from DataSource

```tsx
<DiagramComponent
  layout={{ type: 'OrganizationalChart' }}
  dataSourceSettings={{ id: 'Id', parentId: 'Team', dataSource: items }}
  getNodeDefaults={(node: NodeModel) => {
    node.annotations = [{ content: (node.data as any).Role }];
    node.width = 100; node.height = 40;
    return node;
  }}
  getConnectorDefaults={(c: ConnectorModel) => { c.type = 'Orthogonal'; return c; }}
>
  <Inject services={[DataBinding, HierarchicalTree]} />
</DiagramComponent>
```

> Note: For organizational charts, set `layout.type` to `OrganizationalChart`. This layout is built on top of the `HierarchicalTree` module, so you must still inject the `HierarchicalTree` module for it to work correctly.

### Customizing Subtree Orientation with getLayoutInfo

```tsx
layout={{
  type: 'OrganizationalChart',
  getLayoutInfo: (node: Node, options: TreeInfo) => {
    if (!options.hasSubTree) {
      options.type = 'Center';      // Left | Right | Center | Balanced
      options.orientation = 'Horizontal'; // Horizontal | Vertical
    }
  }
}}
```

| `orientation` | `type` options | Visual result |
|---|---|---|
| `Horizontal` | `Left`, `Right`, `Center`, `Balanced` | Branches expand horizontally |
| `Vertical` | `Left`, `Right`, `Alternate` | Branches expand vertically |

### Assistant Nodes

Designate a child as an assistant (e.g., executive assistant) by moving them from `children` to `assistants`:

```tsx
getLayoutInfo: (node: Node | any, options: TreeInfo) => {
  if (node.data['Role'] === 'General Manager') {
    // Move first child to assistants
    (options.assistants as string[]).push((options.children as string[])[0]);
    (options.children as string[]).splice(0, 1);
  }
}
```

> Assistant nodes cannot have their own children.

---

## Mind Map Layout

Organizes data around a central root node with branches radiating outward. Requires the `MindMap` module.

```tsx
import { MindMap } from '@syncfusion/ej2-react-diagrams';

const data = [
  { id: 1, Label: 'Central Topic' },
  { id: 2, Label: 'Branch A', parentId: 1 },
  { id: 3, Label: 'Branch B', parentId: 1 },
  { id: 4, Label: 'Sub A1', parentId: 2 },
];
const items = new DataManager(data as JSON[]);

<DiagramComponent
  layout={{ type: 'MindMap', orientation: 'Horizontal' }}
  dataSourceSettings={{
    id: 'id', parentId: 'parentId', dataManager: items, root: String(1)
  }}
  getNodeDefaults={(node: NodeModel) => {
    node.annotations = [{ content: (node.data as any).Label }];
    node.width = 100; node.height = 40;
    return node;
  }}
  getConnectorDefaults={(c: ConnectorModel) => { c.type = 'Orthogonal'; return c; }}
>
  <Inject services={[DataBinding, MindMap]} />
</DiagramComponent>
```

### Controlling Branch Placement

Use `getBranch` to force branches to specific sides:

```tsx
layout={{
  type: 'MindMap',
  orientation: 'Horizontal',
  getBranch: (node: NodeModel) => {
    if ((node.data as any).id === 1) return 'Root';
    return 'Right'; // 'Left' | 'Right' | 'SubLeft' | 'SubRight'
  }
}}
```

---

## Radial Tree Layout

Places a root node at the center with children arranged in concentric circles by depth. Requires the `RadialTree` module.

```tsx
import { RadialTree } from '@syncfusion/ej2-react-diagrams';

<DiagramComponent
  layout={{ type: 'RadialTree', root: 'parent' }}
  dataSourceSettings={{ id: 'Id', parentId: 'ReportingPerson', dataSource: items }}
  getNodeDefaults={(node: NodeModel) => {
    node.height = 20; node.width = 20; return node;
  }}
  getConnectorDefaults={(c: ConnectorModel) => {
    (c.targetDecorator as any).shape = 'None';
    c.type = 'Straight'; return c;
  }}
>
  <Inject services={[DataBinding, RadialTree]} />
</DiagramComponent>
```

- Use `layout.root` to explicitly set the root node ID; otherwise the node with no incoming edges is used as root.
- `horizontalSpacing` / `verticalSpacing` control distance between concentric levels.

---

## Flowchart Layout

Renders process flows using standard flowchart shapes. Supports `Decision` nodes with configurable Yes/No branch directions.

```tsx
import { FlowchartLayout } from '@syncfusion/ej2-react-diagrams';

const flowData = [
  { id: '1', name: 'Start', shape: 'Terminator', color: '#6CA0DC' },
  { id: '2', name: 'Input', parentId: ['1'], shape: 'Parallelogram', color: '#6CA0DC' },
  { id: '3', name: 'Decision?', parentId: ['2'], shape: 'Decision', color: '#6CA0DC' },
  { id: '4', label: ['No'],  name: 'Process1', parentId: ['3'], shape: 'Process', color: '#6CA0DC' },
  { id: '5', label: ['Yes'], name: 'Process2', parentId: ['3'], shape: 'Process', color: '#6CA0DC' },
  { id: '6', name: 'End', parentId: ['4', '5'], shape: 'Terminator', color: '#6CA0DC' },
];

<DiagramComponent
  layout={{ type: 'Flowchart' }}
  dataSourceSettings={{ id: 'id', parentId: 'parentId', dataSource: new DataManager(flowData as JSON[]) }}
  getNodeDefaults={(node: NodeModel) => {
    node.width = 120; node.height = 50;
    if ((node.shape as any).shape === 'Decision') node.height = 80;
    return node;
  }}
  getConnectorDefaults={(c: ConnectorModel) => { c.type = 'Orthogonal'; return c; }}
>
  <Inject services={[DataBinding, FlowchartLayout]} />
</DiagramComponent>
```

### Decision Branch Direction

```tsx
layout={{
  type: 'Flowchart',
  flowchartLayoutSettings: {
    yesBranchDirection: 'SameAsFlow',  // LeftInFlow | RightInFlow | SameAsFlow
    noBranchDirection: 'LeftInFlow',
    yesBranchValues: ['Yes', 'Accept', 'True'],
    noBranchValues: ['No', 'Reject', 'False']
  }
}}
```

### Flowchart Orientation

```tsx
layout={{ type: 'Flowchart', orientation: 'LeftToRight' }}
// Default is 'TopToBottom'
```

---

## Layout Configuration Properties

| Property | Type | Description |
|---|---|---|
| `type` | string | Layout algorithm: `HierarchicalTree`, `OrganizationalChart`, `MindMap`, `RadialTree`, `Flowchart` |
| `orientation` | string | Flow direction: `TopToBottom` (default), `LeftToRight`, `BottomToTop`, `RightToLeft` |
| `horizontalSpacing` | number | Horizontal gap between nodes (pixels, default 30) |
| `verticalSpacing` | number | Vertical gap between nodes (pixels, default 30) |
| `margin` | object | `{ left, top, right, bottom }` — padding around entire layout |
| `bounds` | Rect | Constrains layout to a rectangular area: `new Rect(x, y, width, height)` |
| `horizontalAlignment` | string | `Left`, `Center`, `Right` — alignment within bounds |
| `verticalAlignment` | string | `Top`, `Center`, `Bottom` — alignment within bounds |
| `enableAnimation` | boolean | Animate expand/collapse transitions (default `true`) |
| `fixedNode` | string | Node ID that stays fixed while others reposition around it |
| `root` | string | Root node ID (RadialTree; auto-detected when omitted) |
| `getLayoutInfo` | function | Per-subtree customization callback (OrganizationalChart) |
| `getBranch` | function | Branch side assignment callback (MindMap) |

---

## Layout Customization

### Exclude a Node from Auto-Layout

Nodes can opt out of the layout algorithm and be placed manually:

```tsx
getNodeDefaults={(node: NodeModel) => {
  if ((node.data as any).Name === 'Annotation') {
    node.excludeFromLayout = true;
    node.offsetX = 50;
    node.offsetY = 50;
  }
  node.width = 100; node.height = 40;
  return node;
}}
```

### Fixed Node (Anchor During Expand/Collapse)

```tsx
layout={{ type: 'HierarchicalTree', fixedNode: 'Steve-Ceo' }}
```

The specified node holds its position while the surrounding tree reflows — useful during expand/collapse interactions.

### Layout Animation

Requires the `LayoutAnimation` module alongside the layout module:

```tsx
<Inject services={[DataBinding, HierarchicalTree, LayoutAnimation]} />

layout={{ type: 'HierarchicalTree', enableAnimation: true }}
```

### Expand/Collapse Icons

Add expand/collapse icons to nodes in hierarchical layouts:

```tsx
getNodeDefaults={(node: NodeModel) => {
  node.width = 100; node.height = 40;
  node.expandIcon = { shape: 'Plus', width: 15, height: 15, fill: 'lightgray', offset: { x: 0.5, y: 0.85 } };
  node.collapseIcon = { shape: 'Minus', width: 15, height: 15, offset: { x: 0.5, y: 0.85 } };
  return node;
}}
```

### Custom Node Templates (setNodeTemplate)

Use `setNodeTemplate` to render rich visual content inside layout nodes:

```tsx
import { StackPanel, ImageElement, TextElement, Container } from '@syncfusion/ej2-react-diagrams';

function setNodeTemplate(node: NodeModel): Container {
  const panel = new StackPanel();
  panel.width = 200; panel.height = 60;
  panel.orientation = 'Horizontal';
  panel.style.fill = 'skyblue';

  const img = new ImageElement();
  img.width = 40; img.height = 40;

  const text = new TextElement();
  text.content = (node.data as any).Name;
  text.style.color = 'white';

  panel.children = [img, text];
  return panel;
}

<DiagramComponent setNodeTemplate={setNodeTemplate} ... />
```

---

## Layout Events

| Event | Fires When | Common Use |
|---|---|---|
| `dataLoaded` | After data source populates the diagram | Post-load styling, initial state setup |
| `expandStateChange` | User clicks expand/collapse icon | Validate or cancel the state change |
| `animationComplete` | Layout animation finishes | Trigger follow-up actions after transition |
| `layoutUpdated` | Layout calculation starts or finishes | Show/hide loading indicators |

### expandStateChange Example

```tsx
<DiagramComponent
  expandStateChange={(args: IExpandStateChangeEventArgs) => {
    console.log('Expand state:', args.state);
    // args.cancel = true; // Prevent the change
  }}
  ...
/>
```

### animationComplete Example

```tsx
<DiagramComponent
  animationComplete={() => {
    console.log('Animation finished — safe to scroll or update UI');
  }}
  ...
/>
```

---

## Refreshing Layout at Runtime

After adding or removing nodes/connectors programmatically, recalculate the layout:

```tsx
const diagramRef = useRef<DiagramComponent>(null);

// Trigger after structural changes
diagramRef.current?.doLayout();
```

### Dynamic Parent-Child via Drag-and-Drop

Connect a dropped node to an existing parent using the `drop` event:

```tsx
drop={(args: IDropEventArgs) => {
  setTimeout(() => {
    const dropped = args.element as NodeModel;
    const newConnector: ConnectorModel = {
      id: 'con_' + randomId(),
      sourceID: (args.target as NodeModel).id,
      targetID: dropped.id,
    };
    diagramRef.current?.add(newConnector);
    diagramRef.current?.doLayout();
  }, 100);
}}
```

---

## Troubleshooting

**Layout not rendering / nodes piled up at origin**
→ Verify that the required module is injected (`HierarchicalTree`, `MindMap`, `RadialTree`, or `FlowchartLayout`).
→ Confirm `DataBinding` is injected when using `dataSourceSettings`.

**DataSource layout shows no nodes**
→ Ensure `id` and `parentId` in `dataSourceSettings` exactly match the property names in your data objects.
→ The root item should have no `parentId` value (null or undefined).

**Org chart orientation not applying**
→ `getLayoutInfo` is invoked per subtree; check the `hasSubTree` flag before setting orientation.

**Mind map branches all appear on one side**
→ Return `'Root'` from `getBranch` for the root node ID, then `'Left'` / `'Right'` for children.

**Flowchart Decision node not branching correctly**
→ Make sure connector `annotations[0].content` matches a value in `yesBranchValues` or `noBranchValues`.
→ Default yes values: `"Yes"`, `"True"`. Default no values: `"No"`, `"False"`.

**Layout animation not working**
→ Inject `LayoutAnimation` in addition to the layout module and set `enableAnimation: true` in the `layout` prop.
