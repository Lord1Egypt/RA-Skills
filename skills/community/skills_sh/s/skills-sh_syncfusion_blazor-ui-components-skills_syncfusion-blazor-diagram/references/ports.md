# Ports in Blazor Diagram

## Table of Contents
- [Overview](#overview)
- [Creating Ports](#creating-ports)
- [Port Positioning](#port-positioning)
- [Port Appearance](#port-appearance)
- [Connecting via Ports](#connecting-via-ports)
- [Port Visibility](#port-visibility)
- [Dynamic Ports](#dynamic-ports)
- [Port Constraints](#port-constraints)
- [Common Gotchas](#common-gotchas)

---

## Overview

Ports are fixed connection points on nodes. When a connector is attached to a port (instead of a node), it always connects at that exact point — even when the node is moved. Use ports when precise connection placement matters.

**Node-to-node connection:** Connector auto-routes to the nearest edge.
**Port-to-port connection:** Connector always connects at the specified port, regardless of node movement.

---

## Creating Ports

Add ports to a node's `Ports` collection using `PointPort`:

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
            Style = new ShapeStyle { Fill = "#6495ED", StrokeColor = "white" },
            Ports = new DiagramObjectCollection<PointPort>
            {
                new PointPort
                {
                    ID = "port1",
                    Offset = new DiagramPoint { X = 0.5, Y = 0 },  // top center
                    Visibility = PortVisibility.Visible,
                    Shape = PortShapes.Circle
                },
                new PointPort
                {
                    ID = "port2",
                    Offset = new DiagramPoint { X = 0.5, Y = 1 },  // bottom center
                    Visibility = PortVisibility.Visible,
                    Shape = PortShapes.Circle
                }
            }
        });
    }
}
```

> **⚠️ Port ID rules:** Must not start with a number or contain underscores/spaces.

---

## Port Positioning

Port `Offset` uses fractions of the node's width and height:

| Offset | Position |
|--------|----------|
| `(0.5, 0)` | Top center |
| `(0.5, 1)` | Bottom center |
| `(0, 0.5)` | Left center |
| `(1, 0.5)` | Right center |
| `(0, 0)` | Top-left corner |
| `(1, 0)` | Top-right corner |
| `(0, 1)` | Bottom-left corner |
| `(1, 1)` | Bottom-right corner |
| `(0.5, 0.5)` | Center |

---

## Port Appearance

```razor
new PointPort
{
    ID = "p1",
    Offset = new DiagramPoint { X = 1, Y = 0.5 },
    Visibility = PortVisibility.Visible,
    Shape = PortShapes.Circle,         // Circle, Square, Diamond, Custom
    Style = new ShapeStyle
    {
        Fill = "#37909A",
        StrokeColor = "white",
        StrokeWidth = 1
    },
    Width = 12,
    Height = 12
}
```

Available `PortShapes`: `Circle`, `Square`, `Diamond`, `Custom` (with `PathData`)

---

## Connecting via Ports

Use `SourcePortID` and `TargetPortID` on a connector to connect to specific ports:

```razor
connectors.Add(new Connector
{
    ID = "conn1",
    SourceID = "node1",
    SourcePortID = "port1",   // connect from port1 on node1
    TargetID = "node2",
    TargetPortID = "portA",   // connect to portA on node2
    Type = ConnectorSegmentType.Orthogonal
});
```

To connect from a port to a free point:
```razor
new Connector
{
    SourceID = "node1",
    SourcePortID = "port1",
    TargetPoint = new DiagramPoint { X = 400, Y = 300 }
}
```

---

## Port Visibility

Control when ports are shown:

```razor
new PointPort
{
    Visibility = PortVisibility.Visible     // always visible
    // PortVisibility.Hidden                // never visible
    // PortVisibility.Hover                 // show on mouse hover only (default)
    // PortVisibility.Connect               // show when connecting
}
```

---

## Dynamic Ports

Add ports to a node at runtime:

```csharp
_diagram.Nodes[0].Ports.Add(new PointPort
{
    ID = "dynPort",
    Offset = new DiagramPoint { X = 0.5, Y = 0.5 },
    Visibility = PortVisibility.Visible,
    Shape = PortShapes.Square
});
```

---

## Port Constraints

Control what a port allows:

```razor
new PointPort
{
    Constraints = PortConstraints.Default & ~PortConstraints.Draw
    // PortConstraints.None    — no connections allowed
    // PortConstraints.Draw    — allow drawing connectors from port
    // PortConstraints.Default — all interactions enabled
    // PortConstraints.InConnect — allow connecting only the target end of the connector
    // PortConstraints.OutConnect — allow connecting only the source end of the connector.
}
```

---

## Common Gotchas

- **Port ID must be unique per node** — duplicate port IDs cause connection issues
- **`PortVisibility.Hover` is default** — ports only show on hover; set `PortVisibility.Visible` to always display them
- **`SourcePortID`/`TargetPortID` must match an existing port ID** on the referenced node
- **Node-to-node vs port-to-port:** node connections auto-route; port connections stay fixed at the port position
- **Port `Offset` is relative to the node** (0–1), not the diagram canvas
