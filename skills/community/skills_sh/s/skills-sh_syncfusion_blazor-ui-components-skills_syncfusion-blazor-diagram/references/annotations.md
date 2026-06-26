# Annotations in Blazor Diagram

## Table of Contents
- [Overview](#overview)
- [Node Annotations](#node-annotations)
- [Connector Annotations](#connector-annotations)
- [Annotation Position and Alignment](#annotation-position-and-alignment)
- [Annotation Style](#annotation-style)
- [Multiple Annotations](#multiple-annotations)
- [Add / Remove / Update at Runtime](#add--remove--update-at-runtime)
- [Inline Editing](#inline-editing)
- [Common Gotchas](#common-gotchas)

---

## Overview

Annotations are text labels attached to nodes or connectors. They support positioning, alignment, font styling, and runtime editing. Each node/connector can have multiple annotations.

- **Node annotations:** Use `ShapeAnnotation`
- **Connector annotations:** Use `PathAnnotation`

---

## Node Annotations

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
            OffsetX = 200, OffsetY = 200,
            Width = 120, Height = 60,
            Style = new ShapeStyle { Fill = "#6495ED", StrokeColor = "white" },
            Annotations = new DiagramObjectCollection<ShapeAnnotation>
            {
                new ShapeAnnotation { Content = "Process Step" }
            }
        });
    }
}
```

---

## Connector Annotations

```razor
connectors.Add(new Connector
{
    ID = "conn1",
    SourceID = "node1", TargetID = "node2",
    Type = ConnectorSegmentType.Orthogonal,
    Annotations = new DiagramObjectCollection<PathAnnotation>
    {
        new PathAnnotation
        {
            Content = "Yes",
            Offset = 0.5  // position along the path (0=source, 1=target, 0.5=middle)
        }
    }
});
```

---

## Annotation Position and Alignment

**Node annotation positioning via `Offset` (fraction of node width/height):**

| Offset | Position |
|--------|----------|
| `(0.5, 0.5)` | Center (default) |
| `(0.5, 0)` | Top center |
| `(0.5, 1)` | Bottom center |
| `(0, 0.5)` | Left center |
| `(1, 0.5)` | Right center |

```razor
new ShapeAnnotation
{
    Content = "Label",
    Offset = new DiagramPoint { X = 0.5, Y = 0 },  // top center
    HorizontalAlignment = HorizontalAlignment.Center,
    VerticalAlignment = VerticalAlignment.Bottom,
    Margin = new DiagramThickness { Top = 5 }
}
```

**Connector annotation positioning via `Offset` (0 to 1 along the path):**
```razor
new PathAnnotation
{
    Content = "Flow Label",
    Offset = 0.5,           // middle of connector
    Alignment = AnnotationAlignment.Center
}
```

---

## Annotation Style

```razor
new ShapeAnnotation
{
    Content = "Styled Label",
    Style = new TextStyle
    {
        FontSize = 14,
        Bold = true,
        Italic = false,
        Color = "#333333",
        TextDecoration = TextDecoration.Underline,
        TextAlign = TextAlign.Center
    }
}
```

---

## Multiple Annotations

A node can have many annotations at different positions:

```razor
Annotations = new DiagramObjectCollection<ShapeAnnotation>
{
    new ShapeAnnotation
    {
        Content = "Title",
        Offset = new DiagramPoint { X = 0.5, Y = 0 },
        VerticalAlignment = VerticalAlignment.Bottom
    },
    new ShapeAnnotation
    {
        Content = "Subtitle",
        Offset = new DiagramPoint { X = 0.5, Y = 1 },
        VerticalAlignment = VerticalAlignment.Top,
        Style = new TextStyle { FontSize = 10, Color = "#888" }
    }
}
```

---

## Add / Remove / Update at Runtime

**Add annotation at runtime:**
```csharp
_diagram.Nodes[0].Annotations.Add(new ShapeAnnotation
{
    Content = "New Label",
    Offset = new DiagramPoint { X = 0.5, Y = 0.5 }
});
```

**Remove annotation:**
```csharp
_diagram.Nodes[0].Annotations.RemoveAt(0);
```

**Update annotation text:**
```csharp
_diagram.BeginUpdate();
_diagram.Nodes[0].Annotations[0].Content = "Updated Text";
await _diagram.EndUpdateAsync();
```

---

## Inline Editing

Users can double-click an annotation to edit it inline (enabled by default).

**Disable editing for a specific annotation:**
```razor
new ShapeAnnotation
{
    Content = "Read Only",
    Constraints = AnnotationConstraints.ReadOnly
}
```

> **⚠️ `AllowEditing` does NOT exist** on `ShapeAnnotation` or `PathAnnotation`.  
> Inline editing is **on by default** — no property is needed to enable it.  
> To **disable** editing, set `Constraints = AnnotationConstraints.ReadOnly`.

**Handle annotation edit events:**
```razor
<SfDiagramComponent TextChanged="OnTextChanged" />

@code {
    private void OnTextChanged(TextChangeEventArgs args)
    {
        // args.OldValue — text before editing
        // args.NewValue — text after editing
        Console.WriteLine($"Changed from '{args.OldValue}' to '{args.NewValue}'");
    }
}
```

---

## Common Gotchas

- **Node uses `ShapeAnnotation`, connector uses `PathAnnotation`** — using the wrong type causes no label to show
- **Annotation ID must be unique** and must not start with a number or contain underscores/spaces
- **Default position is center** (`Offset = (0.5, 0.5)` for nodes, `Offset = 0.5` for connectors)
- **`HorizontalAlignment` and `VerticalAlignment`** control which side of the offset point the text is anchored to
- **`PathAnnotation.Offset`** is a `double` (0–1), not a `DiagramPoint` like `ShapeAnnotation.Offset`
- **Inline editing is enabled by default** — use `AnnotationConstraints.ReadOnly` to prevent it
- **`AllowEditing` does NOT exist** on `ShapeAnnotation` or `PathAnnotation` — this property will cause a compile error. Editing is on by default; use `AnnotationConstraints.ReadOnly` to opt out
