# Node Shapes in Blazor Diagram

## Table of Contents
- [Overview](#overview)
- [Basic Shapes](#basic-shapes)
- [Flow Shapes](#flow-shapes)
- [Text Shapes](#text-shapes)
- [Image Shapes](#image-shapes)
- [Path Shapes](#path-shapes)
- [HTML Template Shapes](#html-template-shapes)
- [SVG (Native) Shapes](#svg-native-shapes)
- [Choosing the Right Shape Type](#choosing-the-right-shape-type)

---

## Overview

Each `Node` can render different shape types using its `Shape` property. Set the appropriate shape class to control how the node looks.

---

## Basic Shapes

Use `BasicShape` for standard geometric shapes (rectangle, ellipse, triangle, etc.):

```razor
new Node
{
    ID = "node1", OffsetX = 200, OffsetY = 200,
    Width = 100, Height = 60,
    Shape = new BasicShape
    {
        Type = NodeShapes.Basic,
        Shape = NodeBasicShapes.Rectangle,
        CornerRadius = 10   // optional rounded corners
    },
    Style = new ShapeStyle { Fill = "#6BA5D7", StrokeColor = "white" }
}
```

Common `NodeBasicShapes` values:
`Rectangle`, `Ellipse`, `Triangle`, `RightTriangle`, `Parallelogram`, `Pentagon`, `Hexagon`, `Octagon`, `Star`, `Cross`, `Diamond`, `Cylinder`

---

## Flow Shapes

Use `FlowShape` for standard flowchart shapes (process, decision, terminator, etc.):

```razor
new Node
{
    ID = "decision",
    OffsetX = 300, OffsetY = 200,
    Width = 120, Height = 80,
    Shape = new FlowShape
    {
        Type = NodeShapes.Flow,
        Shape = NodeFlowShapes.Decision
    },
    Style = new ShapeStyle { Fill = "#FFD700", StrokeColor = "#B8860B" }
}
```

Common `NodeFlowShapes` values:
`Process`, `Decision`, `Terminator`, `PredefinedProcess`, `Document`, `MultiDocument`, `ManualInput`, `ManualOperation`, `Preparation`, `Data`, `Card`, `DirectData`, `SequentialData`, `Sort`, `Delay`, `Merge`

> **⚠️ `NodeFlowShapes.Database` does NOT exist** — using it causes `CS0117`.  
> Use `NodeFlowShapes.DirectData` or `NodeFlowShapes.Data` to represent a data store:
> ```csharp
> // ❌ Wrong — CS0117: NodeFlowShapes does not contain a definition for 'Database'
> Shape = NodeFlowShapes.Database
>
> // ✅ Correct alternatives
> Shape = NodeFlowShapes.DirectData   // cylinder-like data store shape
> Shape = NodeFlowShapes.Data         // parallelogram data shape
> ```

---

## Text Shapes

Use `TextShape` when you want a text-only node (no border or fill):

```razor
new Node
{
    ID = "label1",
    OffsetX = 200, OffsetY = 100,
    Width = 150, Height = 40,
    Shape = new TextShape
    {
        Content = "Section Title"
    },
    Style = new TextStyle
    {
        FontSize = 16,
        Bold = true,
        Color = "#333333"
    }
}
```

> Use annotations on regular nodes for simple labels; use `TextShape` when the text itself is the node.

---

## Image Shapes

Use `ImageShape` to display an image inside a node:

```razor
new Node
{
    ID = "img1",
    OffsetX = 200, OffsetY = 200,
    Width = 120, Height = 80,
    Shape = new ImageShape
    {
        Type       = NodeShapes.Image,
        Source     = "https://example.com/logo.png",
        // Source can also be a Base64 data URI: "data:image/png;base64,..."
        Scale      = DiagramScale.Meet,            // Meet | Slice | None
        ImageAlign = ImageAlignment.XMidYMid       // controls alignment within the node bounds
    }
}
```
> The correct property name is **`ImageAlign`**:
> ```csharp
> ImageAlign = ImageAlignment.XMidYMid
> ```

> **⚠️ `Stretch` does NOT exist** in the Syncfusion Blazor Diagram namespace.  
> Use `DiagramScale` (enum: `None`, `Meet`, `Slice`) for the `Scale` property.

```csharp
Scale = DiagramScale.Meet
```

---

## Path Shapes

Use `PathShape` to draw a custom shape using an SVG path:

```razor
new Node
{
    ID = "custom1",
    OffsetX = 200, OffsetY = 200,
    Width = 100, Height = 100,
    Shape = new PathShape
    {
        Type = NodeShapes.Path,
        Data = "M 0,50 L 50,0 L 100,50 L 50,100 Z"  // SVG path data
    },
    Style = new ShapeStyle { Fill = "#E88A1A", StrokeColor = "#C07013" }
}
```

---

## HTML Template Shapes

Use `HtmlShape` to render any Blazor/HTML content inside a node. Requires `@ref` on the diagram and use of templates:

```razor
<SfDiagramComponent Height="600px" @ref="_diagram" Nodes="@nodes">
    <DiagramTemplates>
        <NodeTemplate>
            @{
                var node = (context as Node);
                if (node?.Shape.Type == NodeShapes.HTML)
                {
                    <div style="padding:8px; background:#f5f5f5; border:1px solid #ddd;">
                        <strong>@node.Annotations?.FirstOrDefault()?.Content</strong>
                        <br />Custom HTML Content
                    </div>
                }
            }
        </NodeTemplate>
    </DiagramTemplates>
</SfDiagramComponent>

@code {
    // Node using HtmlShape
    nodes.Add(new Node
    {
        ID = "htmlNode",
        OffsetX = 300, OffsetY = 200,
        Width = 180, Height = 80,
        Shape = new Shape { Type = NodeShapes.HTML }
    });
}
```

> **Note:** HTML nodes are not included in diagram exports (PNG/JPEG). Use for interactive content only.

---

## SVG (Native) Shapes

Use `NativeShape` to embed raw SVG markup inside a node:

```razor
<SfDiagramComponent Height="600px" @ref="_diagram" Nodes="@nodes">
    <DiagramTemplates>
        <NodeTemplate>
            @{
                var node = (context as Node);
                if (node?.Shape.Type == NodeShapes.SVG)
                {
                   <svg><circle cx='50' cy='50' r='40' fill='#6BA5D7'/></svg>
                }
            }
        </NodeTemplate>
    </DiagramTemplates>
</SfDiagramComponent>
@code {
    // Node using NativeShape
    nodes.Add(new Node
    {
        ID = "svg1",
        OffsetX = 200, OffsetY = 200,
        Width = 100, Height = 100,
        Shape = new Shape() { Type = NodeShapes.SVG },
    });
}
```

---

## Choosing the Right Shape Type

| Goal | Shape Type |
|------|-----------|
| Standard geometric shapes | `BasicShape` |
| Flowchart diagrams | `FlowShape` |
| Text-only nodes | `TextShape` |
| Display images/logos | `ImageShape` |
| Custom SVG outlines | `PathShape` |
| Embedded HTML/Blazor content | `HtmlShape` |
| Raw SVG markup | `NativeShape` |
| BPMN process modeling | See [bpmn.md](bpmn.md) |
