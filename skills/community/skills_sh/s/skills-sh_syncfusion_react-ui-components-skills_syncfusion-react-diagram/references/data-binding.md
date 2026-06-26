# Data Binding in Syncfusion React Diagram

## Table of Contents
- [Data Binding Overview](#data-binding-overview)
- [Required Setup](#required-setup)
- [dataSourceSettings Reference](#datasourcesettings-reference)
- [Local Data Binding](#local-data-binding)
- [Remote Data Binding](#remote-data-binding)
- [doBinding — Customizing Node Appearance from Data](#dobinding--customizing-node-appearance-from-data)
- [setNodeTemplate — Rich Visual Templates](#setnodetemplate--rich-visual-templates)
- [Separate Node and Connector Data Sources](#separate-node-and-connector-data-sources)
- [PostgreSQL / External Database](#postgresql--external-database)
- [CRUD Operations](#crud-operations)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## Data Binding Overview

Data binding in the Syncfusion React Diagram automatically generates nodes and connectors from a structured data source. Instead of defining each node manually, provide a JSON array (or remote URL) with parent–child relationships and the component builds the diagram.

When to use data binding:
- Rendering org charts or hierarchical structures from database data
- Displaying dynamic process flows where data changes at runtime
- Avoiding manual node/connector definition for large diagrams

Data binding always works **in combination with a layout** (e.g., `HierarchicalTree`, `OrganizationalChart`, `Flowchart`). The layout determines how auto-generated nodes are positioned.

---

## Required Setup

Inject `DataBinding` alongside the desired layout module:

```tsx
import {
  DiagramComponent, Inject,
  DataBinding, HierarchicalTree
} from '@syncfusion/ej2-react-diagrams';
import { DataManager } from '@syncfusion/ej2-data';

<Inject services={[DataBinding, HierarchicalTree]} />
```

---

## dataSourceSettings Reference

| Property | Type | Description |
|---|---|---|
| `id` | string | Field name in the data that uniquely identifies each record |
| `parentId` | string | Field name that points to the parent record's `id` |
| `dataSource` | DataManager \| object[] | The data collection (local array or DataManager) |
| `dataManager` | DataManager | Alternative to `dataSource` for DataManager instances |
| `root` | string | Value of the `id` field that is the root node (optional; auto-detected when omitted) |
| `doBinding` | function | Callback invoked per node to map data fields to node properties |
| `connectionDataSource` | ConnectionDataSourceModel | Separate data source for explicit connectors |
| `crudAction` | CrudActionModel | Endpoints for CRUD operations |
| `customFields` | string[] | Extra data fields to carry through to node's `data` property |

---

## Local Data Binding

Bind a client-side JSON array to the diagram. Each record represents a node; parent–child relationships are established through `id` / `parentId` mappings.

```tsx
import * as React from 'react';
import {
  DiagramComponent, Inject,
  DataBinding, HierarchicalTree,
  NodeModel, ConnectorModel
} from '@syncfusion/ej2-react-diagrams';
import { DataManager } from '@syncfusion/ej2-data';

const employeeData = [
  { Name: 'CEO',         fillColor: '#3DD94A' },
  { Name: 'VP-Eng',      Category: 'CEO' },
  { Name: 'VP-Sales',    Category: 'CEO' },
  { Name: 'Lead Dev',    Category: 'VP-Eng' },
  { Name: 'Sales Mgr',   Category: 'VP-Sales' },
];

export default function App() {
  return (
    <DiagramComponent
      id="container"
      width="100%" height="500px"
      dataSourceSettings={{
        id: 'Name',
        parentId: 'Category',
        dataManager: new DataManager(employeeData as JSON[]),
      }}
      layout={{ type: 'HierarchicalTree', horizontalSpacing: 30, verticalSpacing: 50 }}
      getNodeDefaults={(node: NodeModel) => {
        node.width = 100; node.height = 40;
        node.style = { fill: '#ffeec7', strokeColor: '#f5d897' };
        return node;
      }}
      getConnectorDefaults={(c: ConnectorModel) => {
        c.type = 'Orthogonal';
        (c.targetDecorator as any).shape = 'None';
        return c;
      }}
    >
      <Inject services={[DataBinding, HierarchicalTree]} />
    </DiagramComponent>
  );
}
```

**Data rules:**
- The root record has no `parentId` value (null or undefined).
- `id` values must be unique within the dataset.
- `parentId` must reference an existing `id`; orphaned references are ignored.

---

## Remote Data Binding

Fetch data from a REST endpoint using `DataManager` with a URL adapter:

```tsx
import { DataManager } from '@syncfusion/ej2-data';

<DiagramComponent
  dataSourceSettings={{
    id: 'Id',
    parentId: 'ParentId',
    dataSource: new DataManager({
      url: "[YOUR URL HERE]",
      crossDomain: true,
    }),
    doBinding: (nodeModel: NodeModel, data: any) => {
      nodeModel.annotations = [{ content: data.Label, style: { color: 'white' } }];
    },
  }}
  layout={{ type: 'OrganizationalChart' }}
  getNodeDefaults={(node: NodeModel) => {
    node.width = 80; node.height = 40;
    node.style = { fill: '#048785', strokeColor: 'transparent' };
    return node;
  }}
  getConnectorDefaults={(c: ConnectorModel) => {
    c.type = 'Orthogonal';
    (c.targetDecorator as any).shape = 'None';
    return c;
  }}
>
  <Inject services={[DataBinding, HierarchicalTree]} />
</DiagramComponent>
```

> Remote data binding fires the `dataLoaded` layout event when data finishes loading.

---

## doBinding — Customizing Node Appearance from Data

`doBinding` is called once per node during diagram initialization. Use it to map data fields directly to node model properties:

```tsx
dataSourceSettings={{
  id: 'Id',
  parentId: 'Team',
  dataManager: items,
  doBinding: (nodeModel: NodeModel, data: any, diagram: Diagram) => {
    // Set annotation content from data
    nodeModel.annotations = [{
      content: data.Role,
      style: { color: 'white', fontSize: 12 },
    }];

    // Conditionally style based on data
    if (data.Level === 'Executive') {
      nodeModel.style = { fill: '#c34444', strokeColor: 'white' };
    } else {
      nodeModel.style = { fill: '#3c63ac', strokeColor: 'white' };
    }
  },
}}
```

`doBinding` receives:
- `nodeModel` — the `NodeModel` being configured (mutable)
- `data` — the raw data record from the data source
- `diagram` — the diagram instance

---

## setNodeTemplate — Rich Visual Templates

For complex node visuals (image + text, multi-row cards), use `setNodeTemplate` instead of or in addition to `doBinding`:

```tsx
import {
  StackPanel, ImageElement, TextElement, Container
} from '@syncfusion/ej2-react-diagrams';

function setNodeTemplate(node: NodeModel): Container {
  const panel = new StackPanel();
  panel.width = 200;
  panel.height = 60;
  panel.orientation = 'Horizontal';
  panel.style.fill = 'skyblue';
  panel.cornerRadius = 8;

  const avatar = new ImageElement();
  avatar.width = 40;
  avatar.height = 40;
  avatar.margin = { left: 10, top: 10, right: 0, bottom: 0 };

  const nameLabel = new TextElement();
  nameLabel.content = (node.data as any).Name;
  nameLabel.style.color = 'white';
  nameLabel.margin = { left: 10, top: 5, right: 0, bottom: 0 };

  panel.children = [avatar, nameLabel];
  return panel;
}

<DiagramComponent setNodeTemplate={setNodeTemplate} ... />
```

`setNodeTemplate` must return a `Container` (e.g., `StackPanel`). Elements inside can be:
- `TextElement` — text labels
- `ImageElement` — images by URL or base64
- `PathElement` — SVG path shapes
- `NativeElement` — raw SVG content
- `DiagramElement` — general-purpose elements
- `HtmlElement` — embedded HTML

---

## Separate Node and Connector Data Sources

When connector relationships are stored separately (e.g., a junction table), use `connectionDataSource`:

```tsx

import { DataManager, ODataV4Adaptor } from '@syncfusion/ej2-data';

const nodeData = [
  { id: '1', label: 'Router' },
  { id: '2', label: 'Switch A' },
  { id: '3', label: 'Switch B' },
];

const connectorData = [
  { id: 'c1', sourceNodeId: '1', targetNodeId: '2' },
  { id: 'c2', sourceNodeId: '1', targetNodeId: '3' },
];

dataSourceSettings={{
  id: 'id',
  dataSource: new DataManager(nodeData as JSON[]),
  connectionDataSource: {
    id: 'id',
    sourceID: 'sourceNodeId',
    targetID: 'targetNodeId',
    dataManager: new DataManager(connectorData as JSON[]),
  },
}}
```

> When `connectionDataSource` is used, parent–child inferred connectors from `parentId` are overridden by the explicit connectors.

---


The diagram waits for the async fetch to complete before rendering. The `dataLoaded` event fires on completion.

---

## CRUD Operations

The diagram supports bidirectional CRUD sync — when users modify nodes (add, update, delete) via UI interactions, changes can be pushed back to the server.

```tsx
dataSourceSettings={{
  id: 'id',
  parentId: 'parentId',
  dataSource: items,
  crudAction: {
    read: 'https://api.example.com/nodes',
    create: 'https://api.example.com/nodes/create',
    update: 'https://api.example.com/nodes/update',
    destroy: 'https://api.example.com/nodes/delete',
    customFields: ['Role', 'Department'],  // extra fields to include in payloads
  },
  connectionDataSource: {
    id: 'id',
    sourceID: 'sourceNodeId',
    targetID: 'targetNodeId',
    crudAction: {
      read: 'https://api.example.com/connectors',
      create: 'https://api.example.com/connectors/create',
      update: 'https://api.example.com/connectors/update',
      destroy: 'https://api.example.com/connectors/delete',
    },
  },
}}
```

---

## Best Practices

- **Always match field names exactly**: `id` and `parentId` values in `dataSourceSettings` must match the actual property names in your data objects (case-sensitive).
- **Root record**: The root should have `parentId` as `null` or `undefined` — not an empty string.
- **Use `doBinding` for appearance**, `setNodeTemplate` for complex multi-element visuals.
- **Combine with layouts**: Data binding is meaningless without a layout — always set `layout.type` alongside `dataSourceSettings`.
- **Remote data**: Use `dataLoaded` event to trigger post-render customizations such as selecting a specific node or scrolling the viewport.
- **Custom fields**: List extra data properties in `crudAction.customFields` to ensure they are passed through to the node's `data` property and accessible in `doBinding`.

---

## Troubleshooting

**No nodes appear after data binding**
→ Verify `DataBinding` module is injected.
→ Check that `id` and `parentId` field names match your data exactly.
→ Confirm the root record has no `parentId` value.

**All nodes stack at the same position**
→ The layout type is not set — `dataSourceSettings` requires a `layout` prop to position nodes.

**`doBinding` not being called**
→ Confirm `DataBinding` is in the injected services array; without it, `doBinding` is never invoked.

**Remote data diagram appears empty**
→ Check network requests in browser DevTools for API errors (CORS, 4xx/5xx responses).
→ Ensure the `crossDomain: true` option is set in the DataManager configuration.

**`setNodeTemplate` returns `null`**
→ Always return a valid `Container` instance (e.g., `new StackPanel()`). Returning `null` or `undefined` causes nodes to render with no content.
