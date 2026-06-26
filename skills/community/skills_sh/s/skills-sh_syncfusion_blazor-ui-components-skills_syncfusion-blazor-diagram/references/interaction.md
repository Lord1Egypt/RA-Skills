# Interaction in Blazor Diagram

## Table of Contents
- [Overview](#overview)
- [Selection](#selection)
- [Drag and Drop](#drag-and-drop)
- [Resize and Rotate](#resize-and-rotate)
- [Zoom and Pan](#zoom-and-pan)
- [BringIntoView and BringIntoCenter](#bringintoview-and-bringintocenter)
- [FitToPage Command](#fittopage-command)
- [Nudge Command](#nudge-command)
- [Z-Order Commands](#z-order-commands)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Command Manager (Custom Keyboard Shortcuts)](#command-manager-custom-keyboard-shortcuts)
- [Snapping](#snapping)
- [Alignment, Spacing, and Sizing Commands](#alignment-spacing-and-sizing-commands)
- [Undo and Redo](#undo-and-redo)
- [Clipboard Operations](#clipboard-operations)
- [Programmatic Transform (Drag, Rotate, Scale)](#programmatic-transform-drag-rotate-scale)
- [Group and Ungroup](#group-and-ungroup)
- [Inline Text Editing](#inline-text-editing)
- [Pan (Programmatic Scroll)](#pan-programmatic-scroll)
- [Utility Methods](#utility-methods)
- [Batch Updates (BeginUpdate / EndUpdateAsync)](#batch-updates-beginupdate--endupdateasync)
- [Adding Multiple Elements (AddDiagramElementsAsync)](#adding-multiple-elements-adddiagramelementsasync)
- [User Handles](#user-handles)
- [Drawing Tool](#drawing-tool)
- [Common Gotchas](#common-gotchas)

---

## Overview

The Blazor Diagram provides rich user interactions: select, drag, resize, rotate, zoom, pan, keyboard shortcuts, snapping, undo/redo, and more.

---

## Selection

**Single selection:** Click any node or connector.

**Multi-selection:** Ctrl+Click or rubber-band drag on empty area.

**Programmatic selection:**
```csharp
// Select a node
_diagram.Select(new ObservableCollection<IDiagramObject> { _diagram.Nodes[0] });

// Clear selection
_diagram.ClearSelection();
```

**Selection events:**
```razor
<SfDiagramComponent SelectionChanging="OnSelectionChanging"
                    SelectionChanged="OnSelectionChanged" />

@code {
    private void OnSelectionChanging(SelectionChangingEventArgs args)
    {
        args.Cancel = true; // prevent selection
    }

    private void OnSelectionChanged(Syncfusion.Blazor.Diagram.SelectionChangedEventArgs args)
    {
        // ⚠️ args.NewValue contains IDiagramObject items — you must cast to Node or Connector
        // args.NewValue — ObservableCollection<IDiagramObject>? — newly selected elements
        // args.OldValue — ObservableCollection<IDiagramObject>? — previously selected elements
        
        if (args?.NewValue?.Count > 0)
        {
            foreach (var item in args.NewValue)
            {
                if (item is Node selectedNode)
                {
                    var nodeId = selectedNode.ID;
                    var label = selectedNode.Annotations?[0]?.Content;
                    Console.WriteLine($"Selected Node: {nodeId} - {label}");
                }
                else if (item is Connector selectedConnector)
                {
                    var connectorId = selectedConnector.ID;
                    Console.WriteLine($"Selected Connector: {connectorId}");
                }
            }
        }
    }
}
```

> **⚠️ Critical:** `args.NewValue` is `ObservableCollection<IDiagramObject>?`, not `ObservableCollection<Node>` or `ObservableCollection<Connector>`.  
> You **must cast each item** to `Node` or `Connector` to access type-specific properties like `Annotations`, `OffsetX`, or connector-specific properties.  
> See the [SelectionChanged event section](./events.md#selectionchanging--selectionchanged) in Events documentation for the complete reference and more examples.

---

## Drag and Drop

Users drag nodes/connectors by default. Disable per-element:
```razor
new Node
{
    Constraints = NodeConstraints.Default & ~NodeConstraints.Drag
}
```

**Drag events:**
```razor
<SfDiagramComponent PositionChanging="OnPositionChanging"
                    PositionChanged="OnPositionChanged" />

@code {
    private void OnPositionChanging(PositionChangingEventArgs args)
    {
        args.Cancel = true; // prevent the move
    }

    private void OnPositionChanged(PositionChangedEventArgs args)
    {
        // ⚠️ args.Element is IDiagramObject? — you must cast to Node or Connector
        // args.NewValue — DiagramSelectionSettings? — bounding box of selector (not individual element position)
        // args.OldValue — DiagramSelectionSettings? — previous bounding box
        
        if (args?.Element is Node node)
        {
            // Moved node — access node properties directly
            Console.WriteLine($"Node moved: {node.ID}");
            Console.WriteLine($"  New position: ({node.OffsetX}, {node.OffsetY})");
            Console.WriteLine($"  Label: {node.Annotations?[0]?.Content}");
        }
        else if (args?.Element is Connector connector)
        {
            // Moved connector
            Console.WriteLine($"Connector moved: {connector.ID}");
            Console.WriteLine($"  Connects {connector.SourceID} to {connector.TargetID}");
        }
    }
}
```

---

## Resize and Rotate

Users can resize (drag handles) and rotate (rotation handle) selected nodes.

**Disable resize or rotate per node:**
```razor
new Node
{
    Constraints = NodeConstraints.Default
        & ~NodeConstraints.Resize
        & ~NodeConstraints.Rotate
}
```

**Size change events:**
```razor
<SfDiagramComponent SizeChanging="OnSizeChanging" SizeChanged="OnSizeChanged" />
```

---

## Zoom and Pan

**Mouse/trackpad:** Ctrl+Scroll to zoom, scroll/middle-drag to pan.

**Programmatic zoom:**
```csharp
// Zoom in to a point
_diagram.Zoom(1.2, new DiagramPoint { X = 300, Y = 300 });

// Fit entire diagram in view
_diagram.FitToPage();

// Reset zoom
_diagram.ResetZoom();
```

**Disable pan via toolbar (use FitToPage instead):**
```razor
<SfDiagramComponent InteractionController="@DiagramInteractions.ZoomPan" />
// or
<SfDiagramComponent InteractionController="@DiagramInteractions.Default" />
```

---

## BringIntoView and BringIntoCenter

Scroll the viewport to make a specific rectangular region visible or centered, without changing the zoom level.

**BringIntoView** — adjusts the scroll position so the region is visible within the viewport:
```csharp
// DiagramRect(double x, double y, double width, double height)
DiagramRect bound = new DiagramRect(950, 650, 500, 500);
_diagram.BringIntoView(bound);
```

**BringIntoCenter** — scrolls and centers the viewport on the specified region:
```csharp
DiagramRect bound = new DiagramRect(950, 650, 500, 500);
_diagram.BringIntoCenter(bound);
```

> **Tip:** Use `node.OffsetX - node.Width / 2` and `node.OffsetY - node.Height / 2` to compute the `DiagramRect` from a node's position and size.

---

## FitToPage Command

Adjusts the zoom level and scroll position so that all diagram content (or a specified region) fits within the viewport.

```csharp
// Default — fits all content with default options
_diagram.FitToPage();

// With FitOptions
var options = new FitOptions()
{
    Mode = FitMode.Both,                  // FitMode.Width, FitMode.Height, or FitMode.Both
    Region = DiagramRegion.Content,       // DiagramRegion.Content or DiagramRegion.PageSettings
    CanZoomIn = false                     // true allows zooming IN for small content; default false
};
_diagram.FitToPage(options);
```

**FitMode values:**
| Value | Behavior |
|-------|----------|
| `FitMode.Width` | Fits diagram width to viewport |
| `FitMode.Height` | Fits diagram height to viewport |
| `FitMode.Both` | Fits both dimensions (default) |

**DiagramRegion values:**
| Value | Behavior |
|-------|----------|
| `DiagramRegion.Content` | Fits to the bounding box of all content |
| `DiagramRegion.PageSettings` | Fits to the configured page size |

> ⚠️ `FitMode.Page` does **NOT** exist — see Common Mistakes in SKILL.md.  
> ⚠️ `FitToPageAsync()` does **NOT** exist — `FitToPage()` is synchronous.

---

## Nudge Command

Moves selected elements in a specified direction by a given number of pixels.

```csharp
// Move selected elements 50px to the left
_diagram.Nudge(Direction.Left, 50);

// Move 10px to the right
_diagram.Nudge(Direction.Right, 10);

// Move 1px up (default delta when omitted)
_diagram.Nudge(Direction.Top);

// Move 1px down
_diagram.Nudge(Direction.Bottom);
```

**Direction enum values:**
| Value | Movement |
|-------|----------|
| `Direction.Left` | Move left |
| `Direction.Right` | Move right |
| `Direction.Top` | Move up |
| `Direction.Bottom` | Move down |

> **Note:** Arrow keys also nudge selected elements by 1px by default when the diagram has keyboard focus.  
> **Tip:** Call `_diagram.Select(...)` first to programmatically set the selection before nudging.

---

## Z-Order Commands

Control which elements appear in front of or behind others. **You must select the target element first.**

```csharp
// Select the node to reorder
_diagram.Select(new ObservableCollection<IDiagramObject>() { _diagram.Nodes[0] });

// Move to the front (top of z-stack — drawn last, appears on top)
_diagram.BringToFront();

// Move one step forward (increase z-order by 1)
_diagram.BringForward();

// Move one step backward (decrease z-order by 1)
_diagram.SendBackward();

// Move to the back (bottom of z-stack — drawn first, appears behind all others)
_diagram.SendToBack();
```

> ⚠️ All z-order methods are **synchronous** and operate on the **currently selected** elements.  
> Always call `_diagram.Select(...)` before calling a z-order method.

---

## Command Manager (Custom Keyboard Shortcuts)

Use `CommandManager` to define custom keyboard shortcuts or override built-in ones. It is a **child component** nested inside `SfDiagramComponent`.

**Razor markup:**
```razor
<SfDiagramComponent @ref="@_diagram" Height="600px" Nodes="@_nodes">
    <CommandManager Commands="@_command" Execute="@CommandExecute" CanExecute="@CanExe">
    </CommandManager>
</SfDiagramComponent>
```

**Code-behind:**
```csharp
private DiagramObjectCollection<KeyboardCommand> _command = new()
{
    new KeyboardCommand()
    {
        Name = "CustomGroup",
        Gesture = new KeyGesture() { Key = DiagramKeys.G, Modifiers = ModifierKeys.Control }
    },
    new KeyboardCommand()
    {
        Name = "CustomUngroup",
        Gesture = new KeyGesture() { Key = DiagramKeys.U, Modifiers = ModifierKeys.Control }
    }
};

// Must set args.CanExecute = true to allow the command to fire
private void CanExe(CommandKeyArgs args)
{
    args.CanExecute = true;
}

// Perform the action when the shortcut is triggered
private void CommandExecute(CommandKeyArgs args)
{
    if (args.Gesture.Modifiers == ModifierKeys.Control && args.Gesture.Key == DiagramKeys.G)
        _diagram.Group();

    if (args.Gesture.Modifiers == ModifierKeys.Control && args.Gesture.Key == DiagramKeys.U)
    {
        var selector = _diagram.SelectionSettings;
        if (selector.Nodes.Count > 0 && selector.Nodes[0] is NodeGroup ng && ng.Children.Length > 0)
            _diagram.Ungroup();
    }
}
```

**Key types:**
- `DiagramKeys` — keyboard key values (e.g., `DiagramKeys.G`, `DiagramKeys.Delete`, `DiagramKeys.F2`)
- `ModifierKeys` — modifier keys (e.g., `ModifierKeys.Control`, `ModifierKeys.Shift`, `ModifierKeys.Alt`)
- `KeyGesture` — combines a `Key` and optional `Modifiers`
- `CommandKeyArgs` — event args for both `Execute` and `CanExecute` callbacks

**Override or disable built-in shortcuts:**
```csharp
// Add a command with the same gesture as a built-in shortcut
new KeyboardCommand()
{
    Name = "DisableDelete",
    Gesture = new KeyGesture() { Key = DiagramKeys.Delete }
}

// In Execute — do nothing to effectively disable it
private void CommandExecute(CommandKeyArgs args)
{
    if (args.Gesture.Key == DiagramKeys.Delete)
        return; // built-in delete is suppressed
}
```

---

## Keyboard Shortcuts

Built-in keyboard shortcuts (active when diagram has focus):

| Shortcut | Action |
|----------|--------|
| Ctrl+Z | Undo |
| Ctrl+Y | Redo |
| Ctrl+C | Copy |
| Ctrl+V | Paste |
| Ctrl+X | Cut |
| Delete | Delete selected |
| Ctrl+A | Select all |
| Arrow keys | Move selected by 1px |
| Shift+Arrow | Move selected by 5px |
| Ctrl+Shift+B | Send to back |
| Ctrl+Shift+F | Bring to front |

**Custom keyboard shortcuts:**
```razor
<SfDiagramComponent KeyDown="OnKeyDown" />

@code {
    private void OnKeyDown(KeyEventArgs args)
    {
        // ⚠️ args.Element is IDiagramObject? — you must cast to Node or Connector
        // args.Element — the element with keyboard focus (selected element)
        // args.Key — the key that was pressed
        
        if (args.Key == "Delete")
        {
            // Handle delete for specific element types
            if (args.Element is Node node)
            {
                Console.WriteLine($"Delete key pressed on node: {node.ID}");
                // custom delete logic for nodes
            }
            else if (args.Element is Connector connector)
            {
                Console.WriteLine($"Delete key pressed on connector: {connector.ID}");
                // custom delete logic for connectors
            }
        }
        else if (args.Key == "F2" && args.Element is Node focusedNode)
        {
            // F2 key to edit node label
            Console.WriteLine($"Edit node: {focusedNode.ID}");
        }
    }
}
```

---

## Snapping

Snap nodes to grid lines or to other elements for precise alignment. Use `SnapConstraints` to control which snapping features are active.

### SnapConstraints Overview

There are two types of snapping controls:

1. **Show*** flags — display grid lines on the canvas:
   - `ShowHorizontalLines` — show horizontal grid lines
   - `ShowVerticalLines` — show vertical grid lines
   - `ShowLines` — show both horizontal and vertical grid lines (equivalent to `ShowHorizontalLines | ShowVerticalLines`)

2. **SnapTo*** flags — enable snapping behavior to grid:
   - `SnapToHorizontalLines` — snap objects to horizontal grid lines
   - `SnapToVerticalLines` — snap objects to vertical grid lines
   - `SnapToLines` — snap objects to both grid line types (equivalent to `SnapToHorizontalLines | SnapToVerticalLines`)
   - `SnapToObject` — snap objects to other objects on the diagram

3. **Convenience flags:**
   - `None` — disable all snapping and hide grid lines
   - `All` — enable all snapping and display all grid lines

### SnapConstraints Reference Table

| Constraint | Purpose | Display | Snap Behavior |
|-----------|---------|---------|---------------|
| `None` | Disable all snapping | No grid lines | No snapping |
| `ShowHorizontalLines` | Display horizontal grid | Horizontal lines | No snapping |
| `ShowVerticalLines` | Display vertical grid | Vertical lines | No snapping |
| `ShowLines` | Display all grid lines | Horizontal + vertical | No snapping |
| `SnapToHorizontalLines` | Snap to horizontal grid | No lines (hidden) | Horizontal snapping |
| `SnapToVerticalLines` | Snap to vertical grid | No lines (hidden) | Vertical snapping |
| `SnapToLines` | Snap to all grid lines | No lines (hidden) | Horizontal + vertical snapping |
| `SnapToObject` | Snap to other elements | No grid lines | Object-to-object snapping |
| `All` | Snap to all targets | All grid lines | Horizontal + vertical + objects |

### Common Configurations

**Show grid but don't snap (guide mode):**
```razor
<SfDiagramComponent>
    <SnapSettings Constraints="SnapConstraints.ShowLines">
        <HorizontalGridLines LineColor="#e0e0e0" LineDashArray="2,2" LineIntervals="@lineIntervals" />
        <VerticalGridLines LineColor="#e0e0e0" LineDashArray="2,2" LineIntervals="@lineIntervals" />
    </SnapSettings>
</SfDiagramComponent>

@code {
    double[] lineIntervals = { 1, 9, 0.25, 9.75, 0.25, 9.75, 0.25, 9.75, 0.25, 9.75 };
}
```

**Snap to grid AND show grid lines:**
```razor
<SfDiagramComponent>
    <SnapSettings Constraints="SnapConstraints.ShowLines | SnapConstraints.SnapToLines">
        <HorizontalGridLines LineColor="#e0e0e0" LineDashArray="2,2" LineIntervals="@lineIntervals" />
        <VerticalGridLines LineColor="#e0e0e0" LineDashArray="2,2" LineIntervals="@lineIntervals" />
    </SnapSettings>
</SfDiagramComponent>

@code {
    double[] lineIntervals = { 1, 9, 0.25, 9.75, 0.25, 9.75, 0.25, 9.75, 0.25, 9.75 };
}
```

**Snap to horizontal grid lines only:**
```razor
<SfDiagramComponent>
    <SnapSettings Constraints="SnapConstraints.ShowHorizontalLines | SnapConstraints.SnapToHorizontalLines">
        <HorizontalGridLines LineColor="#e0e0e0" LineDashArray="2,2" LineIntervals="@lineIntervals" />
    </SnapSettings>
</SfDiagramComponent>

@code {
    double[] lineIntervals = { 1, 9, 0.25, 9.75, 0.25, 9.75, 0.25, 9.75, 0.25, 9.75 };
}
```

**Snap to vertical grid lines only:**
```razor
<SfDiagramComponent>
    <SnapSettings Constraints="SnapConstraints.ShowVerticalLines | SnapConstraints.SnapToVerticalLines">
        <VerticalGridLines LineColor="#e0e0e0" LineDashArray="2,2" LineIntervals="@lineIntervals" />
    </SnapSettings>
</SfDiagramComponent>

@code {
    double[] lineIntervals = { 1, 9, 0.25, 9.75, 0.25, 9.75, 0.25, 9.75, 0.25, 9.75 };
}
```

**Snap to objects only (no grid):**
```razor
<SfDiagramComponent>
    <SnapSettings Constraints="SnapConstraints.SnapToObject" />
</SfDiagramComponent>
```

**Snap to both grid AND objects with grid visible:**
```razor
<SfDiagramComponent>
    <SnapSettings Constraints="SnapConstraints.ShowLines | SnapConstraints.SnapToLines | SnapConstraints.SnapToObject">
        <HorizontalGridLines LineColor="#e0e0e0" LineDashArray="2,2" LineIntervals="@lineIntervals" />
        <VerticalGridLines LineColor="#e0e0e0" LineDashArray="2,2" LineIntervals="@lineIntervals" />
    </SnapSettings>
</SfDiagramComponent>

@code {
    double[] lineIntervals = { 1, 9, 0.25, 9.75, 0.25, 9.75, 0.25, 9.75, 0.25, 9.75 };
}
```

**Enable all snapping features (convenience flag):**
```razor
<SfDiagramComponent>
    <SnapSettings Constraints="SnapConstraints.All">
        <HorizontalGridLines LineColor="#e0e0e0" LineDashArray="2,2" LineIntervals="@lineIntervals" />
        <VerticalGridLines LineColor="#e0e0e0" LineDashArray="2,2" LineIntervals="@lineIntervals" />
    </SnapSettings>
</SfDiagramComponent>

@code {
    double[] lineIntervals = { 1, 9, 0.25, 9.75, 0.25, 9.75, 0.25, 9.75, 0.25, 9.75 };
}
```

**Disable all snapping:**
```razor
<SfDiagramComponent>
    <SnapSettings Constraints="SnapConstraints.None" />
</SfDiagramComponent>
```

### Snap Distance

Configure how close an object must be to a grid line or another object before snapping is triggered:

```razor
<SfDiagramComponent>
    <SnapSettings Constraints="SnapConstraints.ShowLines | SnapConstraints.SnapToLines" 
                  SnapDistance="10">
        <HorizontalGridLines LineColor="#e0e0e0" LineDashArray="2,2" LineIntervals="@lineIntervals" />
        <VerticalGridLines LineColor="#e0e0e0" LineDashArray="2,2" LineIntervals="@lineIntervals" />
    </SnapSettings>
</SfDiagramComponent>

@code {
    double[] lineIntervals = { 1, 9, 0.25, 9.75, 0.25, 9.75, 0.25, 9.75, 0.25, 9.75 };
}
```

> **Default:** `SnapDistance = 5` pixels — when an object is within 5 pixels of a snap target, it snaps into place.

### Combining Constraints

Use the bitwise OR operator (`|`) to combine multiple constraints:

```csharp
// Show grid lines AND snap to grid AND snap to objects
var constraints = SnapConstraints.ShowLines 
                | SnapConstraints.SnapToLines 
                | SnapConstraints.SnapToObject;

// Equivalent to:
var constraints = SnapConstraints.All;

// Show only horizontal grid and snap only horizontally
var constraints = SnapConstraints.ShowHorizontalLines 
                | SnapConstraints.SnapToHorizontalLines;
```

### Common Gotchas

- **⚠️ `SnapObjectDistance` does NOT exist** on `SnapSettings` — causes `InvalidOperationException: does not have a property matching the name 'SnapObjectDistance'`.  
  The correct property name is **`SnapDistance`**:
  ```razor
  @* ❌ Wrong — SnapObjectDistance does not exist *@
  <SnapSettings SnapObjectDistance="5" />

  @* ✅ Correct *@
  <SnapSettings SnapDistance="5" />
  ```

- **Grid lines don't display without `ShowLines` or `ShowHorizontalLines`/`ShowVerticalLines`** — snapping works invisibly if you omit the `Show*` flags. Include them to visualize the grid.

- **`SnapToLines` alone doesn't show grid lines** — it enables snapping but hides the grid visual. Pair it with `ShowLines` to display the grid: `ShowLines | SnapToLines`.

- **Grid line configuration is optional** — you can enable snapping without configuring `HorizontalGridLines` and `VerticalGridLines`; the component uses default grid intervals. Customize them to match your design requirements.

---

## Alignment, Spacing, and Sizing Commands

Programmatic commands to organize selected elements:

```csharp
// Align selected nodes
_diagram.SetAlign(AlignmentOptions.Left);   // align left
_diagram.SetAlign(AlignmentOptions.Right);  // align right
_diagram.SetAlign(AlignmentOptions.Top);    // align top
_diagram.SetAlign(AlignmentOptions.Bottom); // align bottom
_diagram.SetAlign(AlignmentOptions.Center); // align center
_diagram.SetAlign(AlignmentOptions.Middle); // align middle

// Distribute spacing evenly
_diagram.SetDistribute(DistributeOptions.Left);         // distribute left
_diagram.SetDistribute(DistributeOptions.Right);        // distribute right
_diagram.SetDistribute(DistributeOptions.Top);          // distribute top
_diagram.SetDistribute(DistributeOptions.Bottom);       // distribute bottom
_diagram.SetDistribute(DistributeOptions.Middle);       // distribute middle
_diagram.SetDistribute(DistributeOptions.Center);       // distribute center
_diagram.SetDistribute(DistributeOptions.BottomToTop);  // distribute bottomToTop
_diagram.SetDistribute(DistributeOptions.RightToLeft);  // distribute rightToLeft

// Same size
_diagram.SetSameSize(SizingMode.Width);   // same width as first selected
_diagram.SetSameSize(SizingMode.Height);  // same height
_diagram.SetSameSize(SizingMode.Both);    // same width AND height
```

---

## Undo and Redo

```csharp
// Undo last action
_diagram.Undo();

// Redo
_diagram.Redo();

// Check state
bool canUndo = _diagram.HistoryManager.CanUndo;
bool canRedo = _diagram.HistoryManager.CanRedo;

// Clear entire undo/redo history
_diagram.ClearHistory();
```

**History change event:**
```razor
<SfDiagramComponent HistoryChanged="OnHistoryChanged" />

@code {
    private void OnHistoryChanged(HistoryChangedEventArgs args)
    {
        // args.Action — the history action taken
    }
}
```

**Custom history entries:**
```csharp
// Add a custom entry to the undo/redo history
_diagram.AddHistoryEntry(new HistoryEntryBase { /* custom data */ });
```

**Grouped undo/redo (treat multiple actions as one unit):**
```csharp
// Start grouping — all actions between Start and End are undone/redone together
_diagram.StartGroupAction();

_diagram.Delete(selectedNodes);
nodes.Add(new Node { ID = "newNode", OffsetX = 200, OffsetY = 200 });

// End grouping — completes the transaction
_diagram.EndGroupAction();

// Now a single Undo() reverts ALL operations above as one step
_diagram.Undo();
```

> ⚠️ Always pair `StartGroupAction()` with `EndGroupAction()`. An unmatched start will leave the history in an inconsistent state.

---

## Clipboard Operations

**Copy, Cut, Paste, Delete** operate on the currently selected elements:

```csharp
// Copy selected elements to clipboard
_diagram.Copy();

// Cut selected elements (removes from diagram, places in clipboard)
_diagram.Cut();

// Paste from clipboard (offset from original position)
_diagram.Paste();

// Paste from a specific collection of cloned elements
DiagramObjectCollection<NodeBase> clones = new DiagramObjectCollection<NodeBase>();
clones.Add((Node)_diagram.Nodes[0].Clone());
_diagram.Paste(clones);

// Delete selected elements
_diagram.Delete();

// Delete specific elements
var toDelete = new DiagramObjectCollection<NodeBase> { _diagram.Nodes[0], _diagram.Connectors[0] };
_diagram.Delete(toDelete);
```

---

## Programmatic Transform (Drag, Rotate, Scale)

Move, rotate, and scale diagram objects programmatically without user interaction:

```csharp
// Drag a node 50px right and 30px down
Node node = _diagram.Nodes[0] as Node;
_diagram.Drag(node, 50, 30);

// Rotate a node 45 degrees clockwise around its center
bool success = _diagram.Rotate(node, 45);

// Rotate around a custom pivot point
bool rotated = _diagram.Rotate(node, 90, new DiagramPoint { X = 100, Y = 100 });

// Scale a node to double its size around its center
DiagramPoint center = new DiagramPoint { X = node.OffsetX, Y = node.OffsetY };
bool scaled = _diagram.Scale(node, 2.0, 2.0, center);
```

> ⚠️ `Rotate()` and `Scale()` return `bool` — `true` if boundary constraints are satisfied, `false` otherwise.

---

## Group and Ungroup

```csharp
// Group currently selected nodes and connectors into a NodeGroup
_diagram.Group();

// Ungroup the selected NodeGroup (disperses its children)
_diagram.Ungroup();

// Add a child to an existing group programmatically
NodeGroup parentGroup = _diagram.Nodes[0] as NodeGroup;
Node newChild = new Node { ID = "child1", Width = 80, Height = 50 };
await _diagram.AddChildAsync(parentGroup, newChild);

// Remove a child from a group
_diagram.RemoveChild(parentGroup, newChild);
```

---

## Inline Text Editing

Start text editing mode programmatically for an annotation:

```csharp
// Edit the first annotation of a node
_diagram.StartTextEdit(_diagram.Nodes[0]);

// Edit a specific annotation by its ID
_diagram.StartTextEdit(_diagram.Nodes[0], "annotationId");
```

> ⚠️ `StartTextEdit()` is synchronous. The annotation must not have `AnnotationConstraints.ReadOnly` set.

---

## Pan (Programmatic Scroll)

```csharp
// Pan 100px to the right and 50px down
_diagram.Pan(100, 50);

// Pan with a focused point (center of the pan movement)
_diagram.Pan(100, 50, new DiagramPoint { X = 400, Y = 300 });
```

---

## Utility Methods

```csharp
// Retrieve a node or connector by its ID
IDiagramObject obj = _diagram.GetObject("node1");
if (obj is Node node) { /* ... */ }

// Get the bounding rectangle of all diagram content
DiagramRect bounds = _diagram.GetPageBounds();

// Get bounds with a custom origin offset
DiagramRect customBounds = _diagram.GetPageBounds(100, 50);

// Clear ALL diagram elements (nodes, connectors, swimlanes)
_diagram.Clear();
```

---

## Batch Updates (BeginUpdate / EndUpdateAsync)

Use `BeginUpdate()` / `EndUpdateAsync()` to batch multiple property changes and apply them in a single render pass for better performance. While locked, the diagram suspends visual updates until `EndUpdateAsync()` is awaited.

```csharp
// Lock diagram rendering
_diagram.BeginUpdate();

// Make multiple changes without intermediate re-renders
_diagram.Nodes[0].OffsetX = 300;
_diagram.Nodes[0].OffsetY = 200;
_diagram.Nodes[1].Style.Fill = "#FF0000";
_diagram.Connectors[0].Style.StrokeColor = "blue";

// Unlock and apply all changes at once
await _diagram.EndUpdateAsync();
```

> ⚠️ `EndUpdate()` (synchronous, no Async suffix) does **NOT** exist — always use `await _diagram.EndUpdateAsync()`.  
> Always pair every `BeginUpdate()` with an `EndUpdateAsync()`. Unmatched calls leave the diagram locked.

---

## Adding Multiple Elements (AddDiagramElementsAsync)

Add a collection of nodes, connectors, and groups to the diagram in a single async operation. This is more efficient than adding elements one by one.

```csharp
// Build a collection of nodes and connectors
var elements = new DiagramObjectCollection<NodeBase>();

elements.Add(new Node
{
    ID = "node1",
    OffsetX = 100, OffsetY = 100,
    Width = 120, Height = 60,
    Style = new ShapeStyle { Fill = "#6BA5D7", StrokeColor = "white" }
});
elements.Add(new Node
{
    ID = "node2",
    OffsetX = 300, OffsetY = 100,
    Width = 120, Height = 60,
    Style = new ShapeStyle { Fill = "#6BA5D7", StrokeColor = "white" }
});
elements.Add(new Connector
{
    ID = "connector1",
    SourceID = "node1",
    TargetID = "node2",
    Type = ConnectorSegmentType.Orthogonal
});

// Add all elements at once
await _diagram.AddDiagramElementsAsync(elements);
```

> **Note:** `AddDiagramElementsAsync` accepts `DiagramObjectCollection<NodeBase>` — both `Node` and `Connector` inherit from `NodeBase`. Passing `null` performs no operation.

---

## User Handles

Custom action buttons that appear on selected elements:

```razor
@using System.Collections.ObjectModel
@using Syncfusion.Blazor.Diagram

<SfDiagramComponent @ref="_diagram" Height="500px"
                    Nodes="@_nodes"
                    Connectors="@_connectors"
                    SelectionSettings="@_selectedModel"
                    GetCustomTool="GetCustomTool">
</SfDiagramComponent>

@code
{
    private SfDiagramComponent _diagram;
    private DiagramObjectCollection<Node> _nodes { get; set; }
    private DiagramObjectCollection<Connector> _connectors { get; set; }
    // Defines diagram's SelectionSettings.
    private DiagramSelectionSettings _selectedModel = new DiagramSelectionSettings();
    private DiagramObjectCollection<UserHandle> _userHandles = new DiagramObjectCollection<UserHandle>();

    protected override void OnInitialized()
    {
        _nodes = new DiagramObjectCollection<Node>();
        _connectors = new DiagramObjectCollection<Connector>();
        InitDiagramModel();
    }

    private InteractionControllerBase GetCustomTool(DiagramElementAction action, string id)
    {
        return id == "clone" ? new CloneTool(_diagram) : new DeleteTool(_diagram);
    }

    private class DeleteTool : InteractionControllerBase
    {
        private SfDiagramComponent _diagram;
        public DeleteTool(SfDiagramComponent diagram) : base(diagram) { _diagram = diagram; }
        public override void OnMouseUp(DiagramMouseEventArgs args)
        {
            _diagram.Delete();
            base.OnMouseUp(args);
        }
    }

    private class CloneTool : DragController
    {
        private SfDiagramComponent _diagram;
        public CloneTool(SfDiagramComponent diagram) : base(diagram) { _diagram = diagram; }
        public override void OnMouseDown(DiagramMouseEventArgs args)
        {
            _diagram.Copy();
            _diagram.Paste();
            base.OnMouseDown(args);
        }
    }

    private void InitDiagramModel()
    {
        Node node = new Node()
        {
            ID = "Node1",
            OffsetX = 300,
            OffsetY = 200,
            Width = 100,
            Height = 100,
            Style = new ShapeStyle() { Fill = "#6495ED", StrokeColor = "none" },
            Annotations = new DiagramObjectCollection<ShapeAnnotation>()
            {
                new ShapeAnnotation() { Content = "Node" }
            }
        };
        _nodes.Add(node);

        Connector connector = new Connector()
        {
            ID = "Connector1",
            SourcePoint = new DiagramPoint() { X = 500, Y = 150 },
            TargetPoint = new DiagramPoint() { X = 600, Y = 250 },
            Type = ConnectorSegmentType.Orthogonal,
            Annotations = new DiagramObjectCollection<PathAnnotation>()
            {
                new PathAnnotation(){ Content = "Connector" }
            }
        };
        _connectors.Add(connector);
        UserHandle cloneHandle = new UserHandle()
        {
            Name = "clone",
            PathData = "M60.3,18H27.5c-3,0-5.5,2.4-5.5,5.5v38.2h5.5V23.5h32.7V18z M68.5,28.9h-30c-3,0-5.5,2.4-5.5,5.5v38.2c0,3,2.4,5.5,5.5,5.5h30c3,0,5.5-2.4,5.5-5.5V34.4C73.9,31.4,71.5,28.9,68.5,28.9z M68.5,72.5h-30V34.4h30V72.5z",
            Offset = 0,
            Side = Direction.Right,
            Visible = true,
            VisibleTarget = VisibleTarget.Node | VisibleTarget.Connector
        };
        UserHandle deleteHandle = new UserHandle()
        {
            Name = "delete",
            PathData = "M0.54700077,2.2130003 L7.2129992,2.2130003 7.2129992,8.8800011 C7.2129992,9.1920013 7.1049975,9.4570007 6.8879985,9.6739998 6.6709994,9.8910007 6.406,10 6.0939997,10 L1.6659999,10 C1.3539997,10 1.0890004,9.8910007 0.87200136,9.6739998 0.65500242,9.4570007 0.54700071,9.1920013 0.54700077,8.8800011 z M2.4999992,0 L5.2600006,0 5.8329986,0.54600048 7.7599996,0.54600048 7.7599996,1.6660004 0,1.6660004 0,0.54600048 1.9270014,0.54600048 z",
            Offset = 1,
            Side = Direction.Bottom,
            VisibleTarget = VisibleTarget.Node | VisibleTarget.Connector,
            Visible = true
        };
        _userHandles = new DiagramObjectCollection<UserHandle>()
        {
            cloneHandle, deleteHandle
        };
        _selectedModel = new DiagramSelectionSettings()
        {
            //Enable userhandle for selected model.
            Constraints = SelectorConstraints.UserHandle,

            UserHandles = _userHandles
        };
    }
}
```

**FixedUserHandleClick event:**

Handle user handle clicks with type-safe Node/Connector casting:

```razor
<SfDiagramComponent @ref="_diagram" Height="500px"
                    Nodes="@_nodes"
                    SelectionSettings="@_selectedModel"
                    FixedUserHandleClick="OnFixedUserHandleClick">
</SfDiagramComponent>

@code {
    private void OnFixedUserHandleClick(FixedUserHandleClickEventArgs args)
    {
        // ⚠️ args.Element is IDiagramObject? — you must cast to Node or Connector
        // args.Element — the element (node or connector) whose user handle was clicked
        // args.FixedUserHandle — details of the handle that was clicked
        
        if (args?.Element is Node node)
        {
            Console.WriteLine($"User handle clicked on Node: {node.ID}");
            Console.WriteLine($"  Handle name: {args.FixedUserHandle?.Name}");
            Console.WriteLine($"  Node label: {node.Annotations?[0]?.Content}");
            
            // Perform action based on handle name
            if (args.FixedUserHandle?.Name == "clone")
            {
                _diagram.Copy();
                _diagram.Paste();
            }
            else if (args.FixedUserHandle?.Name == "delete")
            {
                _diagram.Delete();
            }
        }
        else if (args?.Element is Connector connector)
        {
            Console.WriteLine($"User handle clicked on Connector: {connector.ID}");
            Console.WriteLine($"  Handle name: {args.FixedUserHandle?.Name}");
            Console.WriteLine($"  Connects {connector.SourceID} to {connector.TargetID}");
            
            // Perform connector-specific actions
            if (args.FixedUserHandle?.Name == "delete")
            {
                _diagram.Delete();
            }
        }
    }
}
```

> **⚠️ Critical:** `args.Element` is `IDiagramObject?`, not a concrete `Node` or `Connector`.  
> Always cast using pattern matching: `if (args.Element is Node node) { ... }`.  
> Attempting to access type-specific properties without casting causes `CS1061` (member not found).

---

## Drawing Tool

Let users draw nodes or connectors by clicking and dragging:

```razor
<SfDiagramComponent @ref="_diagram"
                    InteractionController="DiagramInteractions.DrawOnce"
                    DrawingObject="@drawingObj" />

@code {
    IDiagramObject drawingObj = new Node
    {
        Shape = new FlowShape { Type = NodeShapes.Flow, Shape = NodeFlowShapes.Process }
    };

    // Switch to draw connector mode:
    private void DrawConnector()
    {
        _diagram.InteractionController = DiagramInteractions.DrawOnce;
        _diagram.DrawingObject = new Connector { Type = ConnectorSegmentType.Orthogonal };
    }
}
```

---

## Common Gotchas

- **⚠️ Event args with `IDiagramObject` properties require casting** — Many events expose `Element`, `Target`, or other properties as `IDiagramObject?` (interface type, not concrete). To access type-specific properties like `Node.Annotations` or `Connector.SourceID`, **you must cast** using pattern matching: `if (args.Element is Node node)`. See [Events documentation](./events.md#common-gotchas) for comprehensive coverage of all events with complete casting examples.
- **Selection is enabled by default** — use `NodeConstraints` to restrict it per node
- **Rubber-band selection** requires clicking and dragging on the empty canvas (not on a node)
- **`FitToPage()`** must be called after the diagram renders — use `OnAfterRenderAsync` or the `Created` event; it is **synchronous** (no `await`)
- **Z-order methods** (`BringToFront`, `SendToBack`, etc.) require the target to be **selected first** via `_diagram.Select(...)`
- **`CommandManager`** must be a **child component** of `SfDiagramComponent`, not a sibling — `CanExecute` must set `args.CanExecute = true` or the command won't fire
- **Undo/redo tracks all state changes** — use `BeginUpdate()`/`EndUpdateAsync()` to group changes into a single undo step
- **User handles appear only when an element is selected** — set `Visible = true` to show them by default
- **`InteractionController = DiagramInteractions.DrawOnce`** switches to draw mode for one element, then reverts; use `ContinuesDraw` to keep drawing
- **`SnapObjectDistance` does NOT exist** on `SnapSettings` — causes `InvalidOperationException`. Use `SnapDistance` instead: `<SnapSettings SnapDistance="5" />`
