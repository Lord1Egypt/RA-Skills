# Advanced Features in Blazor Diagram

## Table of Contents
- [Groups](#groups)
- [Context Menu](#context-menu)
- [Tooltips](#tooltips)
- [Undo and Redo](#undo-and-redo)
- [Constraints](#constraints)
- [Grid Lines and Rulers](#grid-lines-and-rulers)
- [Scroll Settings](#scroll-settings)
- [Page Settings](#page-settings)
- [Container (Swimlane Equivalent)](#container)
- [Flip](#flip)
- [Localization](#localization)
- [Accessibility](#accessibility)
- [Common Gotchas](#common-gotchas)

---

## Groups

Group multiple nodes into a single unit using `NodeGroup`:

```razor
@code {
    protected override void OnInitialized()
    {
        // Child nodes must be declared before the group
        _nodes.Add(new Node { ID = "node1", OffsetX = 100, OffsetY = 100, Width = 100, Height = 100 });
        _nodes.Add(new Node { ID = "node2", OffsetX = 250, OffsetY = 100, Width = 100, Height = 100 });

        var group = new NodeGroup
        {
            Children = new string[] { "node1", "node2" }
        };
        _nodes.Add(group);
    }
}
```

**Programmatic group/ungroup:**
```csharp
// Group selected nodes
_diagram.SelectAll();
_diagram.Group();

// Ungroup selected group
_diagram.Ungroup();
```

**Group child node constraints** — to allow independent dragging of a child:
```razor
new Node
{
    ID = "child1",
    Constraints = NodeConstraints.Default  // full constraints apply within the group
}
```

---

## Context Menu

### Enable default context menu (copy, cut, paste, undo, redo, group):
```razor
<SfDiagramComponent>
    <ContextMenuSettings Show="true" />
</SfDiagramComponent>
```

### Add custom items alongside defaults:
```razor
<SfDiagramComponent>
    <ContextMenuSettings Show="true" ShowCustomMenuOnly="false" Items="@_items">
    </ContextMenuSettings>
</SfDiagramComponent>

@code {
    private List<ContextMenuItem> _items = new()
    {
        new ContextMenuItem
        {
            ID = "clone", Text = "Clone Node",
            IconCss = "e-icons e-copy"
        }
    };
}
```

### Handle context menu clicks:
```razor
<SfDiagramComponent ContextMenuItemClicked="OnMenuClick" />

@code {
    private void OnMenuClick(DiagramMenuClickEventArgs args)
    {
        if (args.Item.ID == "clone") { /* custom logic */ }
    }
}
```

---

## Tooltips

### Default interaction tooltips (drag/resize/rotate position data):
Shown automatically — no configuration needed.

### Custom tooltip on hover for a node:
```csharp
new Node
{
    Tooltip = new DiagramTooltip { Content = "My Node Info" },
    Constraints = NodeConstraints.Default | NodeConstraints.Tooltip
}
```

### Enable tooltip on the diagram globally:
```razor
<SfDiagramComponent Constraints="DiagramConstraints.Default | DiagramConstraints.Tooltip" />
```

### Programmatic tooltip control (Custom open mode)

Use `ShowTooltipAsync` and `HideTooltipAsync` to show/hide tooltips programmatically. The element's tooltip must have `OpensOn = "Custom"` — tooltips configured with automatic open modes are not affected.

```csharp
// Node configured with custom tooltip open mode
new Node
{
    ID = "node2",
    OffsetX = 240, OffsetY = 100,
    Tooltip = new DiagramTooltip { Content = "Custom tooltip", OpensOn = "Custom" },
    Constraints = NodeConstraints.Default | NodeConstraints.Tooltip
}

// Show tooltip programmatically
await _diagram.ShowTooltipAsync(_diagram.Nodes[1] as NodeBase);

// Hide tooltip programmatically
await _diagram.HideTooltipAsync(_diagram.Nodes[1] as NodeBase);
```

> **Note:** `ShowTooltipAsync` and `HideTooltipAsync` only work for elements with `OpensOn = "Custom"`. Elements with `OpensOn = "Auto"` or `OpensOn = "Hover"` are controlled by the browser and are not affected.

---

## Undo and Redo

```csharp
// Keyboard: Ctrl+Z / Ctrl+Y (built-in)

// Programmatic:
_diagram.Undo();
_diagram.Redo();

// Check availability:
bool canUndo = _diagram.HistoryManager.CanUndo;
bool canRedo = _diagram.HistoryManager.CanRedo;
```

### Group multiple changes into one undo step:
```csharp
_diagram.StartGroupAction();
// ... make multiple changes ...
_diagram.EndGroupAction();
// Now Ctrl+Z undoes all changes at once
```

---

## Constraints

Constraints use bitwise flags (`|` to add, `& ~` to remove).

### Diagram-level constraints:
```razor
<!-- Disable page editing but keep everything else -->
<SfDiagramComponent Constraints="DiagramConstraints.Default & ~DiagramConstraints.PageEditable" />

<!-- Enable auto-routing -->
<SfDiagramComponent Constraints="DiagramConstraints.Default | DiagramConstraints.Routing" />
```

**Key `DiagramConstraints` flags:**

| Flag | Effect |
|------|--------|
| `PageEditable` | Enable/disable editing the page |
| `Zoom` | Enable/disable zoom |
| `Pan` | Enable/disable pan |
| `UndoRedo` | Enable/disable undo/redo |
| `UserInteraction` | Enable/disable all user interaction |
| `Tooltip` | Enable/disable element tooltips |
| `Bridging` | Enable/disable connector bridging |
| `Routing` | Enable automatic connector routing |

### Node-level constraints:
```csharp
new Node
{
    // Remove drag and resize but keep selection
    Constraints = NodeConstraints.Default & ~NodeConstraints.Drag & ~NodeConstraints.Resize
}
```

### Connector-level constraints:
```csharp
new Connector
{
    // Prevent editing the connector path
    Constraints = ConnectorConstraints.Default & ~ConnectorConstraints.DragSegmentThumb
}
```

---

## Grid Lines and Rulers

### Show grid and snap to it:
```razor
<SfDiagramComponent>
    <SnapSettings Constraints="SnapConstraints.ShowLines | SnapConstraints.SnapToLines">
        <HorizontalGridLines LineColor="#e0e0e0" LineDashArray="2,2"
                             LineIntervals="@_intervals" />
        <VerticalGridLines LineColor="#e0e0e0" LineDashArray="2,2"
                           LineIntervals="@_intervals" />
    </SnapSettings>
</SfDiagramComponent>

@code {
    double[] _intervals = { 1, 9, 0.25, 9.75, 0.25, 9.75, 0.25, 9.75, 0.25, 9.75 };
}
```

### Show rulers:
```razor
<SfDiagramComponent>
    <RulerSettings ShowRulers="true" />
</SfDiagramComponent>
```

---

## Scroll Settings

```razor
<SfDiagramComponent>
    <ScrollSettings EnableAutoScroll="true"
                    AutoScrollPadding="@_padding"
                    @bind-ScrollLimit="@_scrollLimit">
    </ScrollSettings>
</SfDiagramComponent>

@code {
    ScrollLimitMode _scrollLimit = ScrollLimitMode.Diagram;
    DiagramMargin _padding = new DiagramMargin { Left = 30, Right = 30, Top = 30, Bottom = 30 };
}
```

**`ScrollLimitMode` options:**

| Value | Description |
|-------|-------------|
| `Infinity` | Unlimited scroll |
| `Diagram` | Limited to diagram bounds |
| `Limited` | Limited to `ScrollableArea` bounds |

---

## Page Settings

Configure the virtual page area inside the diagram canvas:

```razor
<SfDiagramComponent>
    <PageSettings Width="816" Height="1054"
                  MultiplePage="true"
                  Orientation="PageOrientation.Portrait"
                  ShowPageBreaks="true">
        <PageMargin Left="10" Right="10" Top="10" Bottom="10" />
    </PageSettings>
</SfDiagramComponent>
```

---

## Container

A `Container` is a boundary node that visually groups child nodes without the group behavior — children move freely within it:

```razor
<SfDiagramComponent @ref="@_diagram" Height="600px" Nodes="@_nodes">
</SfDiagramComponent>

@code
{
    private SfDiagramComponent _diagram;
    //Initialize the node collection
    private DiagramObjectCollection<Node> _nodes = new DiagramObjectCollection<Node>();

    protected override void OnInitialized()
    {
        Node node1 = new Node()
        {
            ID = "node1",
            Height = 60,
            Width = 100,
            OffsetX = 400,
            OffsetY = 300,
            Annotations = new DiagramObjectCollection<ShapeAnnotation>()
            {
                new ShapeAnnotation(){ Content = "Process"}
            }
        };
        Node node2 = new Node()
        {
            ID = "node2",
            Height = 60,
            Width = 100,
            OffsetX = 600,
            OffsetY = 300,
            Annotations = new DiagramObjectCollection<ShapeAnnotation>()
            {
                new ShapeAnnotation(){ Content = "Process"}
            }
        };
        Container container = new Container()
        {
            ID = "container",
            Height = 300, Width = 500, OffsetX = 500, OffsetY = 300,
            Children = new string[] { "node1", "node2" }
        };
        _nodes.Add(node1);
        _nodes.Add(node2);
        _nodes.Add(container);
    }
}
```

---

## Flip

Flip a node horizontally or vertically:

```csharp
new Node
{
    Flip = FlipDirection.Horizontal  // or Vertical, Both, None
}

// Programmatic flip:
node.Flip = FlipDirection.Vertical;
```

---

## Localization

Override default UI text (e.g., context menu labels):

```csharp
// In Program.cs:
builder.Services.AddSyncfusionBlazor();
// Provide custom locale JSON for the diagram component
// See: Syncfusion globalization documentation
```

---

## Accessibility

The diagram supports ARIA attributes and keyboard navigation:

- **Tab** — move focus between diagram elements
- **Enter** — select focused element
- **Arrow keys** — move selected element
- **Escape** — deselect / cancel editing
- ARIA roles are applied to nodes and connectors automatically

---

## Common Gotchas

- **Group children must be added to `Nodes` before the `NodeGroup`** — the group references children by ID; adding the group first causes a null-reference during render
- **`_diagram.Group()` requires selected nodes** — call `SelectAll()` or programmatically select nodes first
- **`DiagramConstraints.Routing`** enables auto-routing for all connectors; individual connectors can still override with `ConnectorConstraints`
- **`ScrollLimitMode.Infinity`** can cause performance issues with very large diagrams — use `Diagram` or `Limited` for bounded scroll
- **`StartGroupAction` / `EndGroupAction`** must always be paired — an unclosed group action causes all subsequent changes to be grouped indefinitely
- **Tooltips require `NodeConstraints.Tooltip`** on the individual node in addition to `DiagramConstraints.Tooltip` at the diagram level
