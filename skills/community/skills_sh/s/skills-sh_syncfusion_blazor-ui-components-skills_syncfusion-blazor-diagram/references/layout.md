# Layout in Blazor Diagram

## Table of Contents
- [Overview](#overview)
- [Choosing a Layout Type](#choosing-a-layout-type)
- [Hierarchical Tree Layout](#hierarchical-tree-layout)
- [Organizational Chart Layout](#organizational-chart-layout)
- [Mind Map Layout](#mind-map-layout)
- [Radial Tree Layout](#radial-tree-layout)
- [Flowchart Layout](#flowchart-layout)
- [Force-Directed Tree Layout](#force-directed-tree-layout)
- [Complex Hierarchical Layout](#complex-hierarchical-layout)
- [Layout Spacing and Orientation](#layout-spacing-and-orientation)
- [Layout with Data Source](#layout-with-data-source)
- [NodeCreating and ConnectorCreating Callbacks](#nodecreating-and-connectorcreating-callbacks)
- [Layout Events](#layout-events)
- [Refresh Layout at Runtime (DoLayoutAsync)](#refresh-layout-at-runtime-dolayoutasync)
- [Common Gotchas](#common-gotchas)

---

## Overview

Automatic layouts arrange nodes and connectors algorithmically — no manual positioning needed. Define nodes/connectors (or use a data source), choose a layout type, and the diagram handles placement.

---

## Choosing a Layout Type

| Layout Type | Best For |
|-------------|----------|
| `HierarchicalTree` | Trees where nodes can have multiple parents |
| `OrganizationalChart` | Single-parent org charts, reporting hierarchies |
| `MindMap` | Mind maps (one root, branching outward) |
| `RadialTree` | Radial/circular tree structures |
| `Flowchart` | Automatic flowchart arrangement |
| `ForceDirectedLayout` | Network/graph layouts with natural spacing |
| `ComplexHierarchicalTree` | Large hierarchies with complex parent-child paths |

---

## Hierarchical Tree Layout

Nodes can have multiple parents. No root node required.

```razor
<SfDiagramComponent Height="600px"
                    Nodes="@nodes" Connectors="@connectors"
                    NodeCreating="OnNodeCreating"
                    ConnectorCreating="OnConnectorCreating">
    <Layout Type="LayoutType.HierarchicalTree"
            @bind-HorizontalSpacing="@hSpacing"
            @bind-VerticalSpacing="@vSpacing" />
</SfDiagramComponent>

@code {
    int hSpacing = 40, vSpacing = 40;

    private void OnNodeCreating(IDiagramObject obj)
    {
        var node = obj as Node;
        node.Width = 100; node.Height = 40;
        node.Style = new ShapeStyle { Fill = "#6BA5D7", StrokeColor = "none" };
    }

    private void OnConnectorCreating(IDiagramObject obj)
    {
        (obj as Connector).Type = ConnectorSegmentType.Orthogonal;
    }

    protected override void OnInitialized()
    {
        nodes = new DiagramObjectCollection<Node>
        {
            new Node { ID = "n1", Annotations = new() { new ShapeAnnotation { Content = "CEO" } } },
            new Node { ID = "n2", Annotations = new() { new ShapeAnnotation { Content = "Manager" } } },
            new Node { ID = "n3", Annotations = new() { new ShapeAnnotation { Content = "Developer" } } },
        };
        connectors = new DiagramObjectCollection<Connector>
        {
            new Connector { ID = "c1", SourceID = "n1", TargetID = "n2" },
            new Connector { ID = "c2", SourceID = "n2", TargetID = "n3" },
        };
    }
}
```

---

## Organizational Chart Layout

Single-parent hierarchy. Best for company org charts.

```razor
<SfDiagramComponent Height="600px" Nodes="@nodes" Connectors="@connectors"
                    NodeCreating="OnNodeCreating" ConnectorCreating="OnConnectorCreating">
    <Layout Type="LayoutType.OrganizationalChart"
            @bind-HorizontalSpacing="@hSpacing"
            @bind-VerticalSpacing="@vSpacing" />
</SfDiagramComponent>
```

To use with a **data source** (recommended for real org data):
```razor
<SfDiagramComponent ...>
    <DataSourceSettings ID="Id" ParentID="ParentId" DataSource="@orgData" />
    <Layout Type="LayoutType.OrganizationalChart"
            HorizontalSpacing="40" VerticalSpacing="40" />
</SfDiagramComponent>

@code {
    public class OrgItem
    {
        public string Id { get; set; }
        public string Name { get; set; }
        public string ParentId { get; set; }  // empty string = root node
    }

    List<OrgItem> orgData = new()
    {
        new OrgItem { Id = "1", Name = "CEO", ParentId = "" },
        new OrgItem { Id = "2", Name = "CTO", ParentId = "1" },
        new OrgItem { Id = "3", Name = "CFO", ParentId = "1" },
        new OrgItem { Id = "4", Name = "Dev Lead", ParentId = "2" },
    };
}
```

---

## Mind Map Layout

Radial layout from a single root node.

```razor
<SfDiagramComponent Height="600px" Nodes="@nodes" Connectors="@connectors"
                    NodeCreating="OnNodeCreating" ConnectorCreating="OnConnectorCreating">
    <Layout Type="LayoutType.MindMap"
            @bind-HorizontalSpacing="@hSpacing"
            @bind-VerticalSpacing="@vSpacing" />
</SfDiagramComponent>
```

> The **root node** is the node with no incoming connectors (no other node pointing to it).

---

## Radial Tree Layout

Arranges nodes in concentric circles from the root.

```razor
<Layout Type="LayoutType.RadialTree"
        HorizontalSpacing="30"
        VerticalSpacing="30" />
```

---

## Flowchart Layout

Auto-arranges flowchart nodes top-to-bottom.

```razor
<Layout Type="LayoutType.Flowchart"
        HorizontalSpacing="40"
        VerticalSpacing="40" />
```

---

## Force-Directed Tree Layout

Network-style layout — nodes repel each other and edges act as springs.

```razor
<Layout Type="LayoutType.ForceDirectedLayout"
        HorizontalSpacing="40"
        VerticalSpacing="40" />
```

Best for visualizing relationships where hierarchy doesn't matter.

---

## Complex Hierarchical Layout

Handles large trees with multiple root nodes and cross-hierarchy connections.

```razor
<Layout Type="LayoutType.ComplexHierarchicalTree"
        HorizontalSpacing="50"
        VerticalSpacing="50" />
```

---

## Layout Spacing and Orientation

```razor
<Layout Type="LayoutType.HierarchicalTree"
        @bind-HorizontalSpacing="@hSpacing"
        @bind-VerticalSpacing="@vSpacing"
        Orientation="LayoutOrientation.TopToBottom"
        HorizontalAlignment="HorizontalAlignment.Center"
        VerticalAlignment="VerticalAlignment.Center"
        Margin="@(new LayoutMargin { Left = 20, Top = 20 })" />
```

`LayoutOrientation` values: `TopToBottom` (default), `BottomToTop`, `LeftToRight`, `RightToLeft`

---

## Layout with Data Source

When binding a data source, the diagram auto-creates nodes and connectors:

```razor
<SfDiagramComponent Height="600px"
                    NodeCreating="OnNodeCreating"
                    ConnectorCreating="OnConnectorCreating">
    <DataSourceSettings ID="Id" ParentID="ParentId" DataSource="@data" />
    <Layout Type="LayoutType.HierarchicalTree"
            HorizontalSpacing="40" VerticalSpacing="40" />
</SfDiagramComponent>

@code {
    public class DataModel
    {
        public string Id { get; set; }
        public string Label { get; set; }
        public string ParentId { get; set; }
    }

    List<DataModel> data = new()
    {
        new DataModel { Id = "1", Label = "Root", ParentId = "" },
        new DataModel { Id = "2", Label = "Child A", ParentId = "1" },
        new DataModel { Id = "3", Label = "Child B", ParentId = "1" },
    };

    private void OnNodeCreating(IDiagramObject obj)
    {
        var node = obj as Node;
        node.Width = 120; node.Height = 50;
        node.Style = new ShapeStyle { Fill = "#6BA5D7", StrokeColor = "white" };
        // Access custom data fields:
        // var data = node.Data as DataModel;
    }

    private void OnConnectorCreating(IDiagramObject obj)
    {
        (obj as Connector).Type = ConnectorSegmentType.Orthogonal;
    }
}
```

---

## NodeCreating and ConnectorCreating Callbacks

These callbacks run for every node/connector when the layout renders. Use them to:
- Set default size and style
- Apply styles based on data
- Set connector segment types

```csharp
private void OnNodeCreating(IDiagramObject obj)
{
    var node = obj as Node;
    node.Width = 100;
    node.Height = 40;
    node.Style = new ShapeStyle { Fill = "#6BA5D7", StrokeWidth = 2, StrokeColor = "none" };
    node.Annotations[0].Style = new TextStyle { Color = "white", Bold = true };
}

private void OnConnectorCreating(IDiagramObject obj)
{
    var conn = obj as Connector;
    conn.Type = ConnectorSegmentType.Orthogonal;
    conn.CornerRadius = 5;
    conn.TargetDecorator = new DecoratorSettings
    {
        Style = new ShapeStyle { Fill = "#6CA0DC", StrokeColor = "#6CA0DC" }
    };
}
```

---

## Layout Events

```razor
<SfDiagramComponent @ref="_diagram" Width="100%" Height="600px" DataLoaded="@DataLoaded">
<Layout Type="LayoutType.OrganizationalChart" />
</SfDiagramComponent>

@code {
    private void DataLoaded(object args)
    {
        //Action to be performed.
    }
}
```

---

## Refresh Layout at Runtime (DoLayoutAsync)

Call `DoLayoutAsync()` to recalculate and reapply the current layout algorithm after programmatically adding nodes and connectors at runtime. This method updates the positions and arrangements of **all** diagram elements based on the configured layout settings.

### Example — Add nodes and connectors at runtime, then refresh layout

```razor
@using Syncfusion.Blazor.Diagram
@using Syncfusion.Blazor.Buttons

<SfDiagramComponent @ref="_diagram" Height="600px"
                    @bind-Nodes="@_nodes"
                    @bind-Connectors="@_connectors">
    <Layout Type="LayoutType.HierarchicalTree"
            HorizontalSpacing="40" VerticalSpacing="40">
        <LayoutMargin Top="20" Left="20" />
    </Layout>
</SfDiagramComponent>

<SfButton Content="Add Node" OnClick="@AddNodeAtRuntime" />

@code {
    private SfDiagramComponent _diagram;
    private DiagramObjectCollection<Node> _nodes = new();
    private DiagramObjectCollection<Connector> _connectors = new();
    private int _nodeCounter = 1;

    protected override void OnInitialized()
    {
        _nodes.Add(new Node
        {
            ID = "node1",
            Width = 120, Height = 50,
            Style = new ShapeStyle { Fill = "#6BA5D7", StrokeColor = "white" },
            Annotations = new DiagramObjectCollection<ShapeAnnotation>
            {
                new ShapeAnnotation { Content = "Root" }
            }
        });
    }

    private async Task AddNodeAtRuntime()
    {
        _nodeCounter++;
        string newId = $"node{_nodeCounter}";

        // Add a new node to the collection
        _nodes.Add(new Node
        {
            ID = newId,
            Width = 120, Height = 50,
            Style = new ShapeStyle { Fill = "#6BA5D7", StrokeColor = "white" },
            Annotations = new DiagramObjectCollection<ShapeAnnotation>
            {
                new ShapeAnnotation { Content = $"Node {_nodeCounter}" }
            }
        });

        // Connect the new node to its parent
        _connectors.Add(new Connector
        {
            ID = $"conn{_nodeCounter}",
            SourceID = "node1",
            TargetID = newId,
            Type = ConnectorSegmentType.Orthogonal
        });

        // Recalculate and apply the layout for all elements
        await _diagram.DoLayoutAsync();
    }
}
```

**Common use cases:**
- Adding or removing nodes at runtime when using automatic layouts (hierarchical, org chart, mind map, etc.)
- After programmatically updating parent-child relationships in the node/connector collections
- After bulk changes that affect the tree or graph structure

> **Note:** `DoLayoutAsync()` is async — always `await` it. It recalculates positions for **all** elements based on the current layout configuration.  
> When using **data binding** (`DataSourceSettings`) instead of manual node/connector collections, use `RefreshDataSourceAsync()` instead — see [data-binding.md](./data-binding.md#refresh-data-source).

---

## Common Gotchas

- **`NodeCreating`/`ConnectorCreating` are required for layouts** — without them nodes render with default 0-size
- **Root node must have an empty `ParentId`** when using data binding (not null, not missing — empty string `""`)
- **`@bind-HorizontalSpacing` vs `HorizontalSpacing`** — use `@bind-` for two-way binding when the value changes at runtime
- **OrganizationalChart requires single-parent** — each node can have only one parent; use `HierarchicalTree` for multi-parent
- **ForceDirectedLayout is non-deterministic** — result varies each render; not suitable for fixed layouts
- **MindMap root** is the node with no incoming connector, not necessarily the first node defined
