# Connectors in Blazor Diagram

## Table of Contents
- [Overview](#overview)
- [Creating Connectors](#creating-connectors)
- [Connector Properties](#connector-properties)
- [Segment Types](#segment-types)
- [Decorators (Arrows)](#decorators-arrows)
- [Connector Style](#connector-style)
- [Add / Remove / Update at Runtime](#add--remove--update-at-runtime)
- [Common Gotchas](#common-gotchas)

---

## Overview

Connectors create links between nodes (or free-floating points) to show relationships and flows. They support multiple segment types, custom arrows, labels, and interactions.

---

## Creating Connectors

**Connect two nodes by ID:**
```razor
@using Syncfusion.Blazor.Diagram

<SfDiagramComponent Height="600px" Nodes="@nodes" Connectors="@connectors" />

@code {
    DiagramObjectCollection<Node> nodes = new();
    DiagramObjectCollection<Connector> connectors = new();

    protected override void OnInitialized()
    {
        nodes.Add(new Node { ID = "node1", OffsetX = 100, OffsetY = 150, Width = 100, Height = 50 });
        nodes.Add(new Node { ID = "node2", OffsetX = 300, OffsetY = 150, Width = 100, Height = 50 });

        connectors.Add(new Connector
        {
            ID = "conn1",
            SourceID = "node1",
            TargetID = "node2",
            Type = ConnectorSegmentType.Orthogonal
        });
    }
}
```

**Free-floating connector (point to point):**
```razor
connectors.Add(new Connector
{
    ID = "conn1",
    SourcePoint = new DiagramPoint { X = 100, Y = 100 },
    TargetPoint = new DiagramPoint { X = 300, Y = 200 },
    Type = ConnectorSegmentType.Straight
});
```

> **⚠️ Connector ID rules:** Must not start with a number or contain underscores/spaces.

---

## Connector Properties

| Property | Type | Description |
|----------|------|-------------|
| `ID` | string | Unique identifier (required) |
| `SourceID` | string | ID of source node |
| `TargetID` | string | ID of target node |
| `SourcePoint` | DiagramPoint | Source coordinate (when not connecting to a node) |
| `TargetPoint` | DiagramPoint | Target coordinate |
| `SourcePortID` | string | Connect to a specific port on the source node |
| `TargetPortID` | string | Connect to a specific port on the target node |
| `Type` | ConnectorSegmentType | Straight, Orthogonal, Bezier |
| `Segments` | DiagramObjectCollection | Custom segments |
| `Style` | ShapeStyle | Line color, width, dash |
| `SourceDecorator` | DecoratorSettings | Arrow/shape at source end |
| `TargetDecorator` | DecoratorSettings | Arrow/shape at target end |
| `Annotations` | DiagramObjectCollection\<PathAnnotation\> | Text labels on the connector |
| `Constraints` | ConnectorConstraints | Enable/disable behaviors |

---

## Segment Types

| Type | When to Use |
|------|-------------|
| `ConnectorSegmentType.Straight` | Direct line between points |
| `ConnectorSegmentType.Orthogonal` | Right-angle paths (default for flowcharts) |
| `ConnectorSegmentType.Bezier` | Smooth curves |

**Orthogonal connector (auto-routes around nodes):**
```razor
new Connector
{
    ID = "conn1",
    SourceID = "node1", TargetID = "node2",
    Type = ConnectorSegmentType.Orthogonal
}
```

**Bezier connector:**
```razor
new Connector
{
    ID = "conn1",
    SourceID = "node1", TargetID = "node2",
    Type = ConnectorSegmentType.Bezier
}
```

**Multiple segments (bend path):**
```razor
new Connector
{
    ID = "conn1",
    SourceID = "node1", TargetID = "node2",
    Type = ConnectorSegmentType.Orthogonal,
    Segments = new DiagramObjectCollection<ConnectorSegment>
    {
        new OrthogonalSegment { Direction = Direction.Right, Length = 70 },
        new OrthogonalSegment { Direction = Direction.Bottom, Length = 50 }
    }
}
```

---

## Decorators (Arrows)

Control the arrowhead shapes at both ends:

```razor
new Connector
{
    ID = "conn1",
    SourceID = "node1", TargetID = "node2",
    SourceDecorator = new DecoratorSettings
    {
        Shape = DecoratorShape.Circle,
        Style = new ShapeStyle { Fill = "#37909A", StrokeColor = "#37909A" }
    },
    TargetDecorator = new DecoratorSettings
    {
        Shape = DecoratorShape.Arrow,
        Style = new ShapeStyle { Fill = "#6f409f", StrokeColor = "#6f409f" }
    }
}
```

**Remove arrowhead:**
```razor
TargetDecorator = new DecoratorSettings { Shape = DecoratorShape.None }
```

**Custom path decorator:**
```razor
TargetDecorator = new DecoratorSettings
{
    Shape = DecoratorShape.Custom,
    PathData = "M 0,0 L 10,5 L 0,10 Z" // SVG path
}
```

Available `DecoratorShape` values: `Arrow`, `OpenArrow`, `Circle`, `Square`, `Diamond`, `Custom`, `None`

---

## Connector Style

```razor
new Connector
{
    Style = new ShapeStyle
    {
        StrokeColor = "#6f409f",
        StrokeWidth = 2,
        StrokeDashArray = "5,3",   // dashed line
        Opacity = 0.8
    }
}
```

---

## Add / Remove / Update at Runtime

**Add at runtime:**
```csharp
connectors.Add(new Connector
{
    ID = "newConn",
    SourceID = "node1",
    TargetID = "node3",
    Type = ConnectorSegmentType.Orthogonal
});
```

**Add with annotation at runtime:**
```csharp
var newConn = new Connector
{
    ID = "conn2",
    SourcePoint = new DiagramPoint { X = 100, Y = 100 },
    TargetPoint = new DiagramPoint { X = 300, Y = 200 },
    Annotations = new DiagramObjectCollection<PathAnnotation>
    {
        new PathAnnotation { Content = "Flow" }
    }
};
await _diagram.AddDiagramElementsAsync(new DiagramObjectCollection<NodeBase> { newConn });
```

**Remove at runtime:**
```csharp
connectors.Remove(connectors[0]);
```

**Update style at runtime:**
```csharp
_diagram.BeginUpdate();
_diagram.Connectors[0].Style.StrokeColor = "#FF0000";
await _diagram.EndUpdateAsync();
```

> **⚠️ Always use `EndUpdateAsync()`** (async) — `EndUpdate()` (sync, non-async) does NOT exist and will cause a compile error.

---

## Common Gotchas

- **`SourceID`/`TargetID` must match existing node IDs exactly** — otherwise the connector will be free-floating
- **Use `SourcePortID`/`TargetPortID`** to connect to specific ports instead of the nearest edge
- **Orthogonal segments** automatically route around nodes; straight segments do not
- **`PathAnnotation`** (not `ShapeAnnotation`) is used for connector labels
- **`ConnectorSegmentType.Bezier`** ignores manual segment definitions — control points are auto-calculated
- **Use `BeginUpdate()`/`EndUpdateAsync()`** when changing multiple connector properties at once — note `EndUpdateAsync()` is async (`await` required); `EndUpdate()` does not exist
