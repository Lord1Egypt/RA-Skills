# Styling in Blazor Diagram

## Table of Contents
- [Node and Connector Styles](#node-and-connector-styles)
- [Annotation Text Style](#annotation-text-style)
- [CSS Class Override](#css-class-override)
- [Key CSS Classes Reference](#key-css-classes-reference)
- [Common Gotchas](#common-gotchas)

---

## Node and Connector Styles

Use `ShapeStyle` to style nodes and connectors programmatically:

```razor
new Node
{
    Style = new ShapeStyle
    {
        Fill = "#6495ED",
        StrokeColor = "#2c3e50",
        StrokeWidth = 2,
        StrokeDashArray = "5,2",  // dashed border
        Opacity = 0.85
    }
}

new Connector
{
    Style = new ShapeStyle
    {
        StrokeColor = "#e74c3c",
        StrokeWidth = 2,
        StrokeDashArray = "4,2"
    }
}
```

**ShapeStyle properties:**

| Property | Type | Description |
|----------|------|-------------|
| `Fill` | string | Background fill color (hex, rgb, named) |
| `StrokeColor` | string | Border/line color |
| `StrokeWidth` | double | Border/line thickness in pixels |
| `StrokeDashArray` | string | Dash pattern (e.g., `"5,3"`) |
| `Opacity` | double | 0.0 (transparent) to 1.0 (opaque) |
| `Gradient` | `GradientBrush` | Linear or radial gradient fill |

**Gradient fill example:**
```razor
new Node
{
    Style = new ShapeStyle
    {
        Gradient = new LinearGradientBrush
        {
            X1 = 0, Y1 = 0, X2 = 0, Y2 = 1,
            GradientStops = new DiagramObjectCollection<GradientStop>
            {
                new GradientStop { Color = "#ffffff", Offset = 0 },
                new GradientStop { Color = "#6495ED", Offset = 100 }
            }
        }
    }
}
```

---

## Annotation Text Style

```razor
new ShapeAnnotation
{
    Style = new TextStyle
    {
        Color = "#ffffff",
        FontSize = 14,
        FontFamily = "Segoe UI",
        Bold = true,
        Italic = false,
        TextDecoration = TextDecoration.None,  // or Underline, LineThrough
        Fill = "transparent",    // annotation background
        StrokeColor = "none"
    }
}
```

---

## CSS Class Override

`SfDiagramComponent` does **not** have a `CssClass` property. To scope CSS overrides to a single diagram instance, wrap it in a `<div>` with a custom class and target `.e-diagram` and its child classes beneath that wrapper:

```razor
<div class="my-diagram">
    <SfDiagramComponent Width="100%" Height="600px" Nodes="@nodes" />
</div>

<style>
    /* Canvas background */
    .my-diagram .e-diagram {
        background-color: #f0f4f8;
    }

    /* Selection border */
    .my-diagram .e-diagram-border {
        stroke: #3498db !important;
        stroke-width: 2px !important;
    }

    /* Resize handles */
    .my-diagram .e-diagram-resize-handle {
        fill: white !important;
        stroke: #3498db !important;
    }
</style>
```
---

## Key CSS Classes Reference

Override these classes globally or scoped under your wrapper `div` class:

| CSS Class | Target |
|-----------|--------|
| `.e-diagram` | Diagram canvas background |
| `.e-diagram-border` | Selection bounding box border |
| `.e-diagram-endpoint-handle` | Connector endpoint handle |
| `.e-diagram-endpoint-handle.e-connected` | Endpoint handle when connected |
| `.e-diagram-endpoint-handle.e-disabled` | Endpoint handle when port is disabled |
| `.e-diagram-bezier-handle` | Bezier control point handle |
| `.e-diagram-bezier-line` | Bezier tangent line |
| `.e-diagram-ortho-segment-handle` | Orthogonal segment thumb |
| `.e-diagram-bezier-segment-handle` | Bezier/Straight segment handle |
| `.e-diagram-resize-handle` | Node resize corner handle |
| `.e-diagram-rotate-handle` | Node rotation handle |
| `.e-diagram-pivot-line` | Pivot line from node to rotate handle |
| `.e-diagram-first-selection-indicator` | First selected element highlight |
| `.e-diagram-selection-indicator` | All selected elements highlight |
| `.e-diagram-highlighter` | Hover highlight on connectors/ports |
| `.e-diagram-helper` | Alignment guide/helper lines |
| `.e-diagram-thin-grid` | Thin grid lines |
| `.e-diagram-thick-grid` | Thick grid lines |
| `.e-diagram .e-diagram-text-edit` | Inline annotation text editing box |
| `.e-diagram-text-edit::selection` | Text selection color in edit mode |
| `.e-symbolpalette .e-symbol-hover:hover` | Symbol palette item hover state |
| `.e-symbolpalette .e-symbol-selected` | Symbol palette item selected state |
| `.e-symbol-draggable` | Symbol palette item background |
| `.e-diagram .e-ruler` | Ruler background and font |
| `.e-diagram .e-ruler-overlap` | Corner overlap area of horizontal and vertical rulers |
| `.overviewresizer` | Overview component resize handle |

### Example: Customize selection border and rotate handle

```html
<style>
    .e-diagram-border {
        stroke: #3498db;
        stroke-width: 2px;
    }

    .e-diagram-rotate-handle {
        fill: #3498db;
        stroke: #2c3e50;
    }

    .e-diagram-resize-handle {
        fill: white;
        opacity: 1;
        stroke: #3498db;
    }
</style>
```

### Example: Customize diagram background and grid

```html
<style>
    .e-diagram {
        background-color: #1a1a2e;
    }

    .e-diagram-thin-grid {
        stroke: #2a2a4a;
    }

    .e-diagram-thick-grid {
        stroke: #3a3a6a;
    }
</style>
```

---

## Common Gotchas

- **`ShapeStyle.Fill`** applies to nodes only — connectors use `StrokeColor` for their line color
- **`!important` may be needed** for CSS class overrides that conflict with Syncfusion's default specificity
- **`CssClass` does NOT exist** on `SfDiagramComponent` — causes `InvalidOperationException`. Wrap the component in a `<div class="my-diagram">` and scope styles beneath that class instead
- **CSS classes apply globally** unless scoped under a wrapper `<div>` with a custom class around `SfDiagramComponent`
- **Gradient fills** require both `X1/Y1` (start) and `X2/Y2` (end) coordinates as 0–1 fractions of the element
- **`TextStyle.Fill`** controls the annotation label's background, not the node's fill; set it to `"transparent"` unless you need a colored label box
- **Themes (Bootstrap, Material, etc.)** are loaded via the `SyncfusionBlazorThemes` CSS link — switching themes changes many default diagram colors automatically
