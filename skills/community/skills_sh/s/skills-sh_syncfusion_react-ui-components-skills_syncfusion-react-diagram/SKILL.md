---
name: syncfusion-react-diagram
description: Create and customize visual diagrams in React using Syncfusion Diagrams. Trigger for requests involving React component setup, nodes and connectors, flowcharts, org charts, process diagrams, BPMN or UML models, layout algorithms, swimlanes, symbol palettes, and interactive diagram visualization features.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Syncfusion React Diagram

The Syncfusion React Diagram component enables building rich, interactive diagrams including flowcharts, organizational charts, BPMN process flows, UML diagrams, mind maps, and network diagrams. It renders using SVG and supports extensive customization through nodes, connectors, ports, annotations, layouts, and data binding.

## Table of Contents
- [When to Use This Skill](#when-to-use-this-skill)
- [Component Overview](#component-overview)
- [Documentation and Navigation Guide](#documentation-and-navigation-guide)
  - [Getting Started](#getting-started)
  - [Nodes](#nodes)
  - [Connectors](#connectors)
  - [Labels and Annotations](#labels-and-annotations)
  - [Ports](#ports)
  - [Shapes and Styles](#shapes-and-styles)
  - [BPMN Diagrams](#bpmn-diagrams)
  - [UML Diagrams](#uml-diagrams)
  - [Layouts](#layouts)
  - [Swimlanes](#swimlanes)
  - [Groups and Containers](#groups-and-containers)
  - [Symbol Palette](#symbol-palette)
  - [Data Binding](#data-binding)
  - [Interaction and Tools](#interaction-and-tools)
  - [Serialization and Export](#serialization-and-export)
  - [Diagram Settings](#diagram-settings)
- [Quick Start Example](#quick-start-example)
- [Common Patterns](#common-patterns)
- [Module Injection Reference](#module-injection-reference)
- [Key Props](#key-props)

## When to Use This Skill

Use this skill when users need to:

- **Build flowcharts** representing processes, decision trees, or workflows
- **Create org charts** from hierarchical or flat data sources
- **Model BPMN diagrams** with activities, events, gateways, and flows
- **Draw UML diagrams** including class diagrams and sequence diagrams
- **Visualize mind maps** or radial layouts from data
- **Design network/entity diagrams** with nodes and relationship connectors
- **Implement swimlane diagrams** with lanes and phases
- **Drag and drop shapes** from a symbol palette onto a canvas
- **Bind data** to automatically generate diagram structure
- **Serialize and restore** diagram state as JSON
- **Export or print** diagram content as image/SVG

## Important: API Verification Required
 
**API Verification Required**: Always verify API class names, properties, and signatures by reading reference files (`references/*.md`) BEFORE generating code examples. Do not assume or infer class names.

## Component Overview

The Diagram component is built around:

- **Nodes** — Graphical shapes (rectangles, circles, flow shapes, custom) placed on the canvas
- **Connectors** — Lines/arrows linking nodes or freestanding points
- **Annotations** — Text labels attached to nodes or connectors
- **Ports** — Named connection points on nodes for precise connector anchoring
- **Layouts** — Automatic arrangement algorithms (hierarchical, org-chart, mindmap, radial, flowchart)
- **Symbol Palette** — Sidebar of draggable shape symbols
- **Module System** — Opt-in feature modules (`Inject` directive) to keep bundle size lean

All diagram elements are rendered using **SVG** for crisp, resolution-independent graphics.

## Documentation and Navigation Guide

### Getting Started

📄 **Read:** [references/getting-started.md](references/getting-started.md)

**When to read:**
- First-time setup of the Diagram component
- Installing packages, CSS imports, and theme configuration
- Creating a minimal `DiagramComponent`
- Understanding the `Inject` module system
- Next.js or Preact integration

**Covers:**
- npm install and dependencies
- Vite/CRA project setup
- CSS theme import paths
- Basic `DiagramComponent` with `nodes` and `connectors`
- Module injection with `<Inject services={[...]} />`
- Next.js and Preact usage notes

---

### Nodes

📄 **Read:** [references/nodes.md](references/nodes.md)

**When to read:**
- Adding, positioning, and sizing nodes
- Customizing node appearance (fill, stroke, shadow)
- Working with node shapes (Flow, Basic, Path, Image, HTML)
- Handling node events (click, drag, resize)
- Expanding/collapsing nodes at runtime
- Setting default node properties via `getNodeDefaults`

**Covers:**
- Creating nodes via `nodes` collection
- `offsetX`/`offsetY`, `width`/`height` positioning
- Adding/removing nodes at runtime (`diagram.add`, `diagram.remove`)
- Style properties (fill, strokeColor, opacity, gradient)
- `getNodeDefaults` pattern for consistent styling
- Node expand/collapse with `expandIcon`/`collapseIcon`
- Node interaction events

---

### Connectors

📄 **Read:** [references/connectors.md](references/connectors.md)

**When to read:**
- Drawing lines/arrows between nodes or freestanding points
- Choosing connector type (Straight, Orthogonal, Bezier)
- Configuring connector segments and routing
- Customizing decorator (arrow) shapes
- Setting `sourceID`/`targetID` to link nodes
- Setting `getConnectorDefaults` for consistent styling

**Covers:**
- Connector types: `Straight`, `Orthogonal`, `Bezier`
- `sourcePoint`/`targetPoint` for freestanding connectors
- `sourceID`/`targetID` for node-to-node connections
- Multiple segment configuration
- Bezier control points and segment edit orientation
- Arrow/decorator customization
- Connector events and interaction
- `getConnectorDefaults` pattern

---

### Labels and Annotations

📄 **Read:** [references/labels-and-annotations.md](references/labels-and-annotations.md)

**When to read:**
- Adding text labels to nodes or connectors
- Styling annotation text (font, color, bold, alignment)
- Making labels draggable or editable
- Positioning labels relative to nodes/connectors
- Handling label-specific events

**Covers:**
- `annotations` array on nodes and connectors
- Label `content`, `style`, `offset`, `alignment`
- Node labels vs. connector labels
- Label interaction (edit on double-click, drag)
- Label appearance (background, border, padding)
- Label events

---

### Ports

📄 **Read:** [references/ports.md](references/ports.md)

**When to read:**
- Creating named connection points on nodes
- Controlling where connectors attach to a node
- Styling and positioning ports
- Restricting connector connections to specific ports
- Handling port interaction events

**Covers:**
- Port types and `ports` array on nodes
- Port positioning (`offset`, `alignment`)
- Port appearance (shape, fill, stroke)
- Connecting connectors to specific ports via `sourcePortID`/`targetPortID`
- Port interaction and visibility options
- Port events

---

### Shapes and Styles

📄 **Read:** [references/shapes-and-styles.md](references/shapes-and-styles.md)

**When to read:**
- Choosing the right shape type (Flow, Basic, Path, Image, HTML, Native SVG)
- Applying fill colors, gradients, and stroke styles
- Customizing node appearance with CSS or themes
- Understanding shape property structure

**Covers:**
- `shape.type` options: `Flow`, `Basic`, `Path`, `Image`, `HTML`, `Native`
- Flowchart shape values (Terminator, Process, Decision, etc.)
- Basic shape values (Rectangle, Ellipse, Diamond, etc.)
- Style properties: `fill`, `strokeColor`, `strokeWidth`, `strokeDashArray`, `opacity`
- Linear and radial gradients
- Shadow effect
- CSS class-based styling

---

### BPMN Diagrams

📄 **Read:** [references/bpmn-diagrams.md](references/bpmn-diagrams.md)

**When to read:**
- Modeling business process flows using BPMN notation
- Using BPMN-specific shapes (activities, events, gateways)
- Drawing sequence flows, message flows, associations
- Adding data objects, data sources, text annotations, and groups

**Covers:**
- `BpmnDiagrams` module injection
- BPMN shape type: `shape.type = 'Bpmn'`
- Activities: Task types, Subprocess, Expanded Subprocess
- Events: Start, End, Intermediate events and their triggers
- Gateways: Exclusive, Parallel, Inclusive, Complex
- Flows: Sequence, Message, Association
- Data objects and data sources
- BPMN groups and text annotations

---

### UML Diagrams

📄 **Read:** [references/uml-diagrams.md](references/uml-diagrams.md)

**When to read:**
- Building UML class diagrams with attributes and methods
- Modeling relationships (association, generalization, dependency)
- Creating UML sequence diagrams with lifelines and messages
- Working with classifiers (class, interface, enumeration, collaboration)

**Covers:**
- UML class diagram shapes (`shape.type = 'UmlClassifier'`)
- Classifier types: Class, Interface, Enumeration, Collaboration
- Attributes, operations, and members syntax
- UML relationship connector types
- UML sequence diagram (`shape.type = 'UmlActivity'`)
- Lifelines, messages, and fragments

---

### Layouts

📄 **Read:** [references/layouts.md](references/layouts.md)

**When to read:**
- Automatically arranging nodes in a tree, hierarchy, or radial pattern
- Creating org charts driven by parent-child data
- Building mind maps from data sources
- Configuring flowchart layouts with decision/process shapes
- Customizing layout spacing, orientation, and alignment

**Covers:**
- `HierarchicalTree` — top-down/left-right tree layouts
- `OrganizationalChart` — classic org chart with `getNodeDefaults`/`getConnectorDefaults`
- `MindMap` — branching mind map layout
- `RadialTree` — circular radial layout
- `Flowchart` layout (automatic flow arrangement)
- `ComplexHierarchicalTree` for multi-parent hierarchies
- `layout` property: `type`, `orientation`, `margin`, `horizontalSpacing`, `verticalSpacing`
- `LayoutAnimation` module
- Layout events

---

### Swimlanes

📄 **Read:** [references/swimlanes.md](references/swimlanes.md)

**When to read:**
- Creating multi-lane process diagrams
- Adding phases to represent timeline or stages
- Configuring swimlane headers and orientation
- Placing child nodes inside lanes
- Using swimlane shapes from the symbol palette

**Covers:**
- Swimlane `shape.type = 'SwimLane'`
- Lanes and phases configuration
- Header text, size, and orientation
- Child nodes inside lanes
- Swimlane palette integration
- Swimlane interaction (add/remove lanes)

---

### Groups and Containers

📄 **Read:** [references/groups-and-containers.md](references/groups-and-containers.md)

**When to read:**
- Grouping multiple nodes for collective movement/selection
- Adding/removing children from groups at runtime
- Using container nodes to visually bound child nodes
- Configuring padding, fit-to-children behavior

**Covers:**
- Group node `shape.type = 'Group'` and `children` array
- Grouping/ungrouping nodes via diagram methods
- Adding children at runtime
- Container node configuration
- Padding and auto-fit behavior for containers

---

### Symbol Palette

📄 **Read:** [references/symbol-palette.md](references/symbol-palette.md)

**When to read:**
- Adding a drag-and-drop shape sidebar to your diagram app
- Defining custom symbol sets (palettes)
- Customizing palette icon size, search behavior, and accordion
- Handling `symbolDragEnter`/`symbolDrop` events

**Covers:**
- `SymbolPaletteComponent` setup alongside `DiagramComponent`
- Defining `palettes` with symbol arrays
- `getSymbolInfo` for display customization
- Palette accordion: expanding/collapsing groups
- Search functionality
- Symbol preview size configuration
- Palette events

---

### Data Binding

📄 **Read:** [references/data-binding.md](references/data-binding.md)

**When to read:**
- Generating diagrams automatically from JSON or remote data
- Mapping `id` and `parentId` fields for hierarchy
- Using `DataManager` for remote or filtered data
- Customizing node appearance based on data properties (`setNodeTemplate`)
- Connecting to a PostgreSQL or external data source

**Covers:**
- `dataSourceSettings` property
- `id`, `parentId` field mapping
- `DataManager` with local arrays or remote URLs
- `getNodeDefaults` and `setNodeTemplate` for data-driven styling
- PostgreSQL data source integration
- Rendering org charts from flat JSON data

---

### Interaction and Tools

📄 **Read:** [references/interaction-and-tools.md](references/interaction-and-tools.md)

**When to read:**
- Enabling/disabling node and connector interactions (drag, resize, select)
- Switching diagram tool modes (pointer, draw, pan)
- Configuring diagram constraints
- Adding custom keyboard commands or toolbar actions
- Implementing undo/redo
- Setting up context menus or user handles

**Covers:**
- `DiagramConstraints`, `NodeConstraints`, `ConnectorConstraints`
- `tool` property: `DiagramTools.Default`, `ZoomPan`, `DrawOnce`
- Selection, drag, resize, rotate interactions
- `commands` for keyboard shortcuts
- Undo/Redo (`UndoRedo` module)
- Context menu (`DiagramContextMenu` module)
- User handles for custom action buttons on nodes
- `Snapping` module and snap settings

---

### Serialization and Export

📄 **Read:** [references/serialization-and-export.md](references/serialization-and-export.md)

**When to read:**
- Saving and restoring diagram state as JSON
- Exporting the diagram as PNG, JPEG, or SVG
- Printing diagram content
- Importing Visio (.vsdx) files
- Migrating from EJ1 diagram format

**Covers:**
- `diagram.saveDiagram()` and `diagram.loadDiagram(json)`
- `PrintAndExport` module injection
- Export settings: format, region, margin, background
- Print dialog and options
- Visio file import (`visio.md`)
- EJ1 serialization compatibility (`Ej1Serialization` module)

---

### Diagram Settings

📄 **Read:** [references/diagram-settings.md](references/diagram-settings.md)

**When to read:**
- Managing diagram layers (visibility, locking, ordering)
- Enabling virtualization for performance with large diagrams
- Configuring grid lines, snapping, and rulers
- Setting page size, orientation, and margins
- Configuring scroll behavior and limits
- Adding tooltips to diagram elements
- Using the Overview component for minimap navigation
- Enabling localization or RTL support
- Understanding accessibility features

**Covers:**
- Layers: add, lock, set visibility, active layer
- `Virtualization` module for large diagrams
- Grid lines: dots, lines, snap settings
- Ruler configuration
- `scrollSettings`: `scrollLimit`, `minZoom`, `maxZoom`
- `pageSettings`: size, orientation, background, multiplePage
- Tooltip on nodes and connectors
- `OverviewComponent` minimap setup
- Localization and RTL
- ARIA and keyboard accessibility

---

## Quick Start Example

### Minimal Flowchart

```tsx
import { DiagramComponent, NodeModel, ConnectorModel, Inject, UndoRedo } from '@syncfusion/ej2-react-diagrams';

const nodes: NodeModel[] = [
  { id: 'start', offsetX: 300, offsetY: 80, width: 140, height: 50,
    shape: { type: 'Flow', shape: 'Terminator' }, annotations: [{ content: 'Start' }] },
  { id: 'process', offsetX: 300, offsetY: 180, width: 140, height: 50,
    shape: { type: 'Flow', shape: 'Process' }, annotations: [{ content: 'Process' }] },
  { id: 'end', offsetX: 300, offsetY: 290, width: 140, height: 50,
    shape: { type: 'Flow', shape: 'Terminator' }, annotations: [{ content: 'End' }] },
];
const connectors: ConnectorModel[] = [
  { id: 'c1', sourceID: 'start', targetID: 'process' },
  { id: 'c2', sourceID: 'process', targetID: 'end' },
];

export default function App() {
  return (
    <DiagramComponent id="diagram" width={'100%'} height={'500px'}
      nodes={nodes} connectors={connectors}
      getConnectorDefaults={(obj) => { obj.type = 'Orthogonal'; return obj; }}>
      <Inject services={[UndoRedo]} />
    </DiagramComponent>
  );
}
```

CSS import: `@import '@syncfusion/ej2-react-diagrams/styles/material.css';` and peer CSS for `ej2-base`, `ej2-popups`, `ej2-splitbuttons`, `ej2-navigations`.

---

## Common Patterns

### Pattern 1: Org Chart from Data Source

```tsx
import { DiagramComponent, HierarchicalTree, DataBinding, Inject } from '@syncfusion/ej2-react-diagrams';
import { DataManager } from '@syncfusion/ej2-data';

const data = [
  { Name: 'CEO' },
  { Name: 'CTO', ReportingPerson: 'CEO' },
  { Name: 'Dev Lead', ReportingPerson: 'CTO' },
];

export default function App() {
  return (
    <DiagramComponent id="diagram" width={'100%'} height={'500px'}
      dataSourceSettings={{ id: 'Name', parentId: 'ReportingPerson', dataManager: new DataManager(data) }}
      layout={{ type: 'OrganizationalChart' }}
      getNodeDefaults={(node) => { node.width = 120; node.height = 40; return node; }}
      getConnectorDefaults={(obj) => { obj.type = 'Orthogonal'; return obj; }}>
      <Inject services={[DataBinding, HierarchicalTree]} />
    </DiagramComponent>
  );
}
```

### Pattern 2: Save and Load Diagram State

Use `diagramInstance.saveDiagram()` to serialize to JSON string; `diagramInstance.loadDiagram(json)` to restore. Inject `UndoRedo` for history support. For full examples see [references/serialization-and-export.md](references/serialization-and-export.md).

### Pattern 3: Diagram with Symbol Palette

Render `SymbolPaletteComponent` alongside `DiagramComponent`. Define palettes with shape arrays, set `symbolHeight`/`symbolWidth`, and users can drag shapes onto the canvas. For full examples see [references/symbol-palette.md](references/symbol-palette.md).

---

## Module Injection Reference

Inject only the modules your diagram uses: `<Inject services={[HierarchicalTree, DataBinding, UndoRedo]} />`

| Module | Purpose |
|--------|---------|
| `HierarchicalTree` | Tree and org chart layouts |
| `MindMap` | Mind map layout |
| `RadialTree` | Radial/circular layout |
| `ComplexHierarchicalTree` | Multi-parent hierarchies |
| `DataBinding` | Data source integration |
| `UndoRedo` | Undo/redo history |
| `Snapping` | Grid snapping |
| `PrintAndExport` | Export & print |
| `BpmnDiagrams` | BPMN shapes |
| `LayoutAnimation` | Animated layouts |
| `DiagramContextMenu` | Right-click context menu |
| `ConnectorBridging` | Bridge overlapping connectors |
| `ConnectorEditing` | Edit connector segments |
| `Ej1Serialization` | Load EJ1 diagram JSON |

---

## Key Props

| Prop | Type | Description |
|------|------|-------------|
| `nodes` | `NodeModel[]` | Array of node definitions |
| `connectors` | `ConnectorModel[]` | Array of connector definitions |
| `layout` | `LayoutModel` | Automatic layout configuration |
| `dataSourceSettings` | `DataSourceModel` | Data source for auto-generated diagrams |
| `getNodeDefaults` | `(node) => NodeModel` | Default properties for all nodes |
| `getConnectorDefaults` | `(obj) => ConnectorModel` | Default properties for all connectors |
| `setNodeTemplate` | `(node) => DiagramElement` | Custom template rendering for nodes |
| `tool` | `DiagramTools` | Active interaction tool mode |
| `snapSettings` | `SnapSettingsModel` | Grid and snap configuration |
| `scrollSettings` | `ScrollSettingsModel` | Scroll limits and zoom bounds |
| `pageSettings` | `PageSettingsModel` | Page size, orientation, background |
| `constraints` | `DiagramConstraints` | Enable/disable diagram-level interactions |
| `width` | `string` | Diagram canvas width (e.g., `'100%'`) |
| `height` | `string` | Diagram canvas height (e.g., `'600px'`) |

## Related Components

- [Chart](../implementing-charts/) - Data-driven charts and graphs
- [Kanban](../implementing-kanban/) - Kanban board visualization
- [Data Grid](../../grids/implementing-data-grids/) - Tabular data display
