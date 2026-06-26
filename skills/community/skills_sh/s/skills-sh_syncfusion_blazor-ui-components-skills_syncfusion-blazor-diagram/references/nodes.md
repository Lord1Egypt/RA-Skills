# Nodes in Blazor Diagram

## Table of Contents
- [Overview](#overview)
- [Creating Nodes](#creating-nodes)
- [Node Properties](#node-properties)
- [Positioning and Sizing](#positioning-and-sizing)
- [Node Style](#node-style)
- [Add / Remove / Update at Runtime](#add--remove--update-at-runtime)
- [Expand and Collapse](#expand-and-collapse)
- [Node Constraints](#node-constraints)
- [Common Gotchas](#common-gotchas)

---

## Overview

Nodes are graphical objects representing processes, entities, or data in a diagram. They can be basic shapes, flow shapes, images, HTML content, or custom SVG paths.

---

## Creating Nodes

Add nodes via the `Nodes` property of `SfDiagramComponent`:

```razor
@using Syncfusion.Blazor.Diagram

<SfDiagramComponent Height="600px" Nodes="@nodes" />

@code {
    DiagramObjectCollection<Node> nodes = new();

    protected override void OnInitialized()
    {
        nodes.Add(new Node
        {
            ID = "node1",
            OffsetX = 250, OffsetY = 250,
            Width = 100, Height = 100,
            Style = new ShapeStyle { Fill = "#6495ED", StrokeColor = "white" }
        });
    }
}
```

> **⚠️ Node ID rules:** Must not start with a number, must not contain underscores or spaces.

---

## Node Properties

| Property | Type | Description |
|----------|------|-------------|
| `ID` | string | Unique identifier (required) |
| `OffsetX` | double | X position of the pivot point |
| `OffsetY` | double | Y position of the pivot point |
| `Width` | double | Width of the node |
| `Height` | double | Height of the node |
| `Shape` | NodeShape | Shape type (basic, flow, path, image, etc.) |
| `Style` | ShapeStyle | Fill, stroke, opacity |
| `Annotations` | DiagramObjectCollection\<ShapeAnnotation\> | Text labels |
| `Ports` | DiagramObjectCollection\<PointPort\> | Connection points |
| `RotationAngle` | double | Rotation in degrees |
| `Pivot` | DiagramPoint | Pivot point (default: 0.5, 0.5 = center) |
| `ZIndex` | int | Stack order |
| `IsExpanded` | bool | Expand/collapse state |
| `Constraints` | NodeConstraints | Enable/disable behaviors |
| `AdditionalInfo` | Dictionary | Custom metadata |

---

## Positioning and Sizing

`OffsetX`/`OffsetY` position the node's **pivot point** (default: center):

```razor
// Node centered at (250, 250)
new Node { OffsetX = 250, OffsetY = 250, Width = 100, Height = 100 }
```

To position from **top-left corner**, set `Pivot = new DiagramPoint { X = 0, Y = 0 }`:

```razor
new Node
{
    OffsetX = 200, OffsetY = 200,
    Width = 100, Height = 100,
    Pivot = new DiagramPoint { X = 0, Y = 0 } // top-left is reference
}
```

| Pivot | Meaning |
|-------|---------|
| (0.5, 0.5) | Center (default) |
| (0, 0) | Top-left corner |
| (1, 1) | Bottom-right corner |

Rotation:
```razor
new Node { RotationAngle = 45 } // 45-degree rotation
```

---

## Node Style

```razor
new Node
{
    Style = new ShapeStyle
    {
        Fill = "#6BA5D7",
        StrokeColor = "#3A6BC4",
        StrokeWidth = 2,
        Opacity = 0.9,
        StrokeDashArray = "5,3",  // dashed border
        FillColor = "transparent" // use for outline-only
    }
}
```

---

## Add / Remove / Update at Runtime

**Add at runtime:**
```csharp
nodes.Add(new Node
{
    ID = "newNode",
    OffsetX = 400, OffsetY = 200,
    Width = 100, Height = 50
});
```

**Add with annotation at runtime (using `AddDiagramElementsAsync`):**
```csharp
@ref="_diagram"
...
var newNode = new Node { ID = "n2", OffsetX = 300, OffsetY = 300, Width = 100, Height = 60,
    Annotations = new DiagramObjectCollection<ShapeAnnotation>
    {
        new ShapeAnnotation { Content = "New Node" }
    }
};
await _diagram.AddDiagramElementsAsync(new DiagramObjectCollection<NodeBase> { newNode });
```

**Remove at runtime:**
```csharp
nodes.Remove(nodes[0]);
// or
nodes.RemoveAt(0);
```

**Update node properties at runtime (use BeginUpdate/EndUpdateAsync for performance):**
```csharp
_diagram.BeginUpdate();
_diagram.Nodes[0].Width = 150;
_diagram.Nodes[0].Style.Fill = "#FF6347";
await _diagram.EndUpdateAsync();
```

**Clone a node:**
```csharp
Node clone = nodes[0].Clone() as Node;
clone.ID = "clonedNode";
clone.OffsetX += 30;
clone.OffsetY += 30;
await _diagram.AddDiagramElementsAsync(new DiagramObjectCollection<NodeBase> { clone });
```

---

## Default Node Settings

Use the `NodeCreating` event to apply uniform default properties to every node as it is added to the diagram:

```razor
<SfDiagramComponent @ref="_diagram" Nodes="@nodes" NodeCreating="OnNodeCreating" />

@code {
    private void OnNodeCreating(IDiagramObject obj)
    {
        if (obj is Node node)
        {
            // Apply defaults only when the individual node hasn't set them
            node.Style ??= new ShapeStyle();
            if (node.Style.Fill == null)        node.Style.Fill        = "#dce8fc";
            if (node.Style.StrokeColor == null) node.Style.StrokeColor = "#3a7bd5";
            if (node.Style.StrokeWidth == 0)    node.Style.StrokeWidth  = 1.5;
        }
    }
}
```

> Use the **`NodeCreating`** event to set default node properties:
> ```razor
> <SfDiagramComponent NodeCreating="OnNodeCreating" />
> ```

---

## Expand and Collapse

Nodes can have child nodes expanded or collapsed using `IsExpanded`:

```razor
<SfDiagramComponent @ref="_diagram" Nodes="@nodes" NodeCreating="OnNodeCreating">
</SfDiagramComponent>

@code {
    private void OnNodeCreating(IDiagramObject obj)
    {
        if (obj is Node node)
        {
            node.IsExpanded = true;
        }
    }

    private void CollapseNode()
    {
        _diagram.Nodes[0].IsExpanded = false;
    }
}
```

For layout-based diagrams with expand/collapse buttons, see [references/layout.md](layout.md).

---

## Expand and Collapse Icons

Use `ExpandIcon` and `CollapseIcon` properties on a node to render interactive
toggle buttons. The icon shapes come from the **`DiagramExpandIcons`** and
**`DiagramCollapseIcons`** enums respectively.

> **⚠️ Use `DiagramExpandIcons` / `DiagramCollapseIcons` — NOT `DiagramElementShape`.**  
> `DiagramElementShape` does **not** apply to expand/collapse icons and will cause a compile error.

### Correct enum types

| Property | Shape enum |
|---|---|
| `DiagramExpandIcon.Shape` | `DiagramExpandIcons` |
| `DiagramCollapseIcon.Shape` | `DiagramCollapseIcons` |

### Available shapes

**`DiagramExpandIcons`**

| Value | Description |
|---|---|
| `DiagramExpandIcons.Minus` | Minus (−) symbol |
| `DiagramExpandIcons.ArrowUp` | Arrow pointing up |
| `DiagramExpandIcons.MultiplyText` | × symbol |
| `DiagramExpandIcons.None` | No icon |

**`DiagramCollapseIcons`**

| Value | Description |
|---|---|
| `DiagramCollapseIcons.Plus` | Plus (+) symbol |
| `DiagramCollapseIcons.ArrowDown` | Arrow pointing down |
| `DiagramCollapseIcons.MultiplyText` | × symbol |
| `DiagramCollapseIcons.None` | No icon |

### Applying icons via `NodeCreating` (recommended for layout diagrams)

```csharp
private void OnNodeCreating(IDiagramObject obj)
{
    if (obj is Node node)
    {
        node.IsExpanded = true;

        node.ExpandIcon = new DiagramExpandIcon
        {
            Shape  = DiagramExpandIcons.Minus,
            Width  = 20,
            Height = 20
        };

        node.CollapseIcon = new DiagramCollapseIcon
        {
            Shape  = DiagramCollapseIcons.Plus,
            Width  = 20,
            Height = 20
        };
    }
}
```

---

## Node Constraints

Control which interactions are allowed per node:

```razor
new Node
{
    Constraints = NodeConstraints.Default & ~NodeConstraints.Drag
    // Disables drag while keeping all other behaviors
}

// Common constraint values:
// NodeConstraints.None          — no interaction
// NodeConstraints.Default       — all interactions
// NodeConstraints.Select        — only selection
// ~NodeConstraints.Resize       — disable resize
// ~NodeConstraints.Rotate       — disable rotation
// ~NodeConstraints.Delete       — prevent deletion
```

---

## Common Gotchas

- **Node ID must be unique** — duplicate IDs cause rendering issues
- **ID must not start with a number** (e.g., use `"node1"` not `"1node"`)
- **ID must not contain underscores or spaces** — use hyphens or camelCase
- **Use `BeginUpdate()`/`EndUpdateAsync()`** when updating multiple properties at once for better performance
- **`OffsetX`/`OffsetY` reference the pivot** (center by default), not the top-left corner
- **Annotations are separate objects** — use `DiagramObjectCollection<ShapeAnnotation>`, not a plain string
- **`NodeDefaults` does NOT exist** on `SfDiagramComponent` — causes `InvalidOperationException: does not have a property matching the name 'NodeDefaults'`. Use the `NodeCreating` event to apply default properties to nodes instead
