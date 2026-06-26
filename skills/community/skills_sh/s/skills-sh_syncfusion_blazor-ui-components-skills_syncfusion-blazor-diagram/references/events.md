# Diagram Events in Blazor Diagram

## Table of Contents
- [Overview](#overview)
- [Lifecycle Events](#lifecycle-events)
  - [NodeCreating / ConnectorCreating](#nodecreating--connectorcreating)
- [Click and Keyboard Events](#click-and-keyboard-events)
- [Mouse Interaction Events](#mouse-interaction-events)
  - [MouseEnter / MouseLeave / MouseHover](#mouseenter--mouseleave--mousehover)
- [Element Change Events](#element-change-events)
  - [CollectionChanging / CollectionChanged](#collectionchanging--collectionchanged)
  - [SourcePointChanging / SourcePointChanged](#sourcepointchanging--sourcepointchanged)
  - [TargetPointChanging / TargetPointChanged](#targetpointchanging--targetpointchanged)
  - [SegmentCollectionChange](#segmentcollectionchange)
  - [PropertyChanged](#propertychanged)
- [Drag-and-Drop Events](#drag-and-drop-events)
- [User Handle Events](#user-handle-events)
  - [FixedUserHandleClick](#fixedusershandleclick)
- [History (Undo/Redo) Events](#history-undoredo-events)
- [Auto-Scroll Events](#auto-scroll-events)
- [Events Quick-Reference Table](#events-quick-reference-table)
- [Common Gotchas](#common-gotchas)

---

## Overview

Subscribe to diagram events by binding event handlers in the `SfDiagramComponent` markup. All events follow standard Blazor event callback patterns.

---

## Lifecycle Events

### Created

Fires once after the diagram is fully rendered. Use it to perform post-render setup (e.g., programmatic selection):

```razor
<SfDiagramComponent @ref="_diagram" Created="OnCreated" />

@code {
    private void OnCreated(object args)
    {
        _diagram.Select(new ObservableCollection<IDiagramObject> { _diagram.Nodes[0] });
    }
}
```

### NodeCreating / ConnectorCreating

Fires for each node or connector as it is initialised. Use these events to apply **default properties** uniformly across all diagram elements without repeating setup in `OnInitialized`:

```razor
<SfDiagramComponent Nodes="@_nodes"
                    Connectors="@_connectors"
                    NodeCreating="OnNodeCreating"
                    ConnectorCreating="OnConnectorCreating" />

@code {
    private void OnNodeCreating(IDiagramObject obj)
    {
        // obj is always the raw IDiagramObject — cast to Node to access properties
        if (obj is Node node)
        {
            node.Style.Fill        = "#357BD2";
            node.Style.StrokeColor = "white";
            node.Style.Opacity     = 1;
        }
    }

    private void OnConnectorCreating(IDiagramObject obj)
    {
        if (obj is Connector connector)
        {
            connector.Style.StrokeColor = "black";
            connector.Style.StrokeWidth = 1;
            connector.TargetDecorator.Style.Fill        = "black";
            connector.TargetDecorator.Style.StrokeColor = "black";
        }
    }
}
```

> **⚠️ The parameter type is `IDiagramObject`, not `Node` or `Connector` directly.**  
> Always cast before accessing element-specific properties:
> ```csharp
> // ❌ Wrong — IDiagramObject has no Style property
> private void OnNodeCreating(IDiagramObject obj) { obj.Style.Fill = "red"; }
>
> // ✅ Correct — cast first
> private void OnNodeCreating(IDiagramObject obj)
> {
>     if (obj is Node node) { node.Style.Fill = "red"; }
> }
> ```

---

## Mouse Interaction Events

### MouseEnter / MouseLeave / MouseHover

Fire when the mouse pointer **enters**, **leaves**, or **hovers** over a node or connector. All three share the same `DiagramElementMouseEventArgs` argument type with `IDiagramObject?` elements:

```razor
<SfDiagramComponent MouseEnter="OnMouseEnter"
                    MouseLeave="OnMouseLeave"
                    MouseHover="OnMouseHover" />

@code {
    private void OnMouseEnter(DiagramElementMouseEventArgs args)
    {
        // ⚠️ args.Element is IDiagramObject? — you must cast to Node or Connector
        // args.Element — IDiagramObject? — the node or connector the pointer entered
        // args.ActualObject — IDiagramObject? — the actual object being hovered
        
        if (args.Element is Node node)
        {
            // ✅ Now you can access Node-specific properties
            Console.WriteLine($"Mouse entered node: {node.ID}");
            Console.WriteLine($"  Label: {node.Annotations?[0]?.Content}");
            Console.WriteLine($"  Position: ({node.OffsetX}, {node.OffsetY})");
        }
        else if (args.Element is Connector conn)
        {
            // ✅ Now you can access Connector-specific properties
            Console.WriteLine($"Mouse entered connector: {conn.ID}");
            Console.WriteLine($"  From {conn.SourceID} to {conn.TargetID}");
        }
    }

    private void OnMouseLeave(DiagramElementMouseEventArgs args)
    {
        // ⚠️ args.Element is IDiagramObject? — cast to access type-specific properties
        if (args.Element is Node node)
        {
            Console.WriteLine($"Mouse left node: {node.ID}");
        }
        else if (args.Element is Connector conn)
        {
            Console.WriteLine($"Mouse left connector: {conn.ID}");
        }
    }

    private void OnMouseHover(DiagramElementMouseEventArgs args)
    {
        // ⚠️ args.Element is IDiagramObject? — cast to access type-specific properties
        if (args.Element is Node node)
        {
            Console.WriteLine($"Hovering over node: {node.ID}");
            // Change appearance on hover
            node.Style.Opacity = 0.8;
        }
    }
}
```

| Event | Fires When |
|---|---|
| `MouseEnter` | Mouse pointer enters the boundary of a node or connector |
| `MouseLeave` | Mouse pointer exits the boundary of a node or connector |
| `MouseHover` | Mouse pointer is hovering over a node or connector |

> **⚠️ Critical:** All mouse event arguments contain `IDiagramObject?` elements.  
> You **must cast** to `Node` or `Connector` to access properties like `ID`, `Annotations`, or connector-specific properties.  
> Attempting to access type-specific properties without casting causes `CS1061` (member not found).

---

## Click and Keyboard Events

### Click

Fires when a user clicks a node, connector, or the canvas:

```razor
<SfDiagramComponent Click="OnClick" />

@code {
    private void OnClick(Syncfusion.Blazor.Diagram.ClickEventArgs args)
    {
        // ⚠️ args.Element is IDiagramObject? — you must cast to Node or Connector
        // args.Element — IDiagramObject? — the clicked element (null if canvas clicked)
        // args.ActualObject — IDiagramObject? — the actual object under the cursor
        // args.Position — DiagramPoint with click coordinates
        // args.Count — method returning int: 1 for single click, 2 for double click
        
        int count = args.Count;   // ✅ call Count as a property/method, assign to int first
        
        if (count == 1)
        {
            // Single click
            if (args.Element is Node node)
            {
                // ✅ Now you can access Node-specific properties
                Console.WriteLine($"Clicked node: {node.ID}");
                Console.WriteLine($"  Label: {node.Annotations?[0]?.Content}");
            }
            else if (args.Element is Connector conn)
            {
                // ✅ Now you can access Connector-specific properties
                Console.WriteLine($"Clicked connector: {conn.ID}");
                Console.WriteLine($"  Connects {conn.SourceID} to {conn.TargetID}");
            }
            else
            {
                Console.WriteLine($"Clicked canvas at ({args.Position?.X}, {args.Position?.Y})");
            }
        }
    }
}
```

> **⚠️ Critical:** `args.Element` is `IDiagramObject?`, not `Node` or `Connector` directly.  
> You **must cast** to access type-specific properties. Attempting to access properties without casting causes `CS1061` (member not found).

> **⚠️ `ClickEventArgs` name collision:** If your page also uses `@using Syncfusion.Blazor.Navigations` (or Buttons),  
> `ClickEventArgs` becomes ambiguous. Always qualify it:
> ```csharp
> // ✅ Use the fully qualified type in the handler signature
> private void OnClick(Syncfusion.Blazor.Diagram.ClickEventArgs args) { }
> ```

> **⚠️ `args.Count` is NOT an `int` field** — it is a **method/property** that returns an `int`.  
> Do NOT compare it directly with `==` inline without storing the result first:
> ```csharp
> // ❌ Wrong — CS0019: Operator '==' cannot be applied to operands of type 'method group' and 'int'
> if (args.Count == 2)
>
> // ✅ Correct — store result then compare
> int clickCount = args.Count;
> if (clickCount == 2) { /* double-click */ }
> ```

### Double-Click

> **⚠️ There is NO `OnDoubleClick` event and NO `DoubleClickEventArgs` type** in `SfDiagramComponent`.  
> Detect double-clicks via the `Click` event by reading `args.Count` as an `int`:

```razor
<SfDiagramComponent Click="OnClick" />

@code {
    private void OnClick(Syncfusion.Blazor.Diagram.ClickEventArgs args)
    {
        int clickCount = args.Count;   // store as int first
        if (clickCount == 2)
        {
            // Double-click
            var target = args.Element is Connector c ? $"Connector [{c.ID}]"
                       : args.Element is Node n       ? $"Node [{n.ID}]"
                       : "Canvas";
            Console.WriteLine($"Double-clicked: {target}");
        }
    }
}
```

### KeyDown / KeyUp

Fires when a key is pressed/released while the diagram has focus:

```razor
<SfDiagramComponent KeyDown="OnKeyDown" KeyUp="OnKeyUp" />

@code {
    private void OnKeyDown(KeyEventArgs args)
    {
        // ⚠️ args.Element is IDiagramObject? — you must cast to Node or Connector
        // args.Key — string — key name (e.g., "Delete", "Enter")
        // args.KeyCode — int — the actual key code pressed
        // args.KeyModifiers — ModifierKeys — modifier flags (Control, Shift, Alt)
        // args.Element — IDiagramObject? — the currently selected element (if any)
        
        if (args.Key == "Delete")
        {
            // Custom delete handling
            if (args.Element is Node node)
            {
                // ✅ Now you can access Node-specific properties
                Console.WriteLine($"Delete key pressed on node: {node.ID}");
            }
            else if (args.Element is Connector conn)
            {
                // ✅ Now you can access Connector-specific properties
                Console.WriteLine($"Delete key pressed on connector: {conn.ID}");
            }
        }
        else if (args.Key == "c" && args.KeyModifiers == ModifierKeys.Control)
        {
            // Custom copy handling
            Console.WriteLine("Ctrl+C pressed");
        }
    }

    private void OnKeyUp(KeyEventArgs args)
    {
        // Similar structure — args.Element must be cast to access type-specific properties
    }
}
```

> **⚠️ Critical:** `args.Element` is `IDiagramObject?`, not `Node` or `Connector` directly.  
> You **must cast** to access type-specific properties like `ID`, `Annotations`, or `SourceID`.  
> Attempting to access properties without casting causes `CS1061` (member not found).

---

## Element Change Events

### PositionChanging / PositionChanged

Fire when a node or connector is moved:

```razor
<SfDiagramComponent PositionChanging="OnPositionChanging"
                    PositionChanged="OnPositionChanged" />

@code {
    private void OnPositionChanging(Syncfusion.Blazor.Diagram.PositionChangingEventArgs args)
    {
        args.Cancel = true; // block the move
    }

    private void OnPositionChanged(Syncfusion.Blazor.Diagram.PositionChangedEventArgs args)
    {
        // ⚠️ args.Element is IDiagramObject? — you must cast to Node or Connector
        // args.Element  — IDiagramObject? — the node or connector being dragged
        // args.NewValue — DiagramSelectionSettings? — selector state after the move
        // args.OldValue — DiagramSelectionSettings? — selector state before the move

        if (args.Element is Node node)
        {
            // ✅ Now you can access Node-specific properties
            Console.WriteLine($"Node [{node.ID}] moved");
            Console.WriteLine($"  New position: ({node.OffsetX}, {node.OffsetY})");
            Console.WriteLine($"  Size: {node.Width} x {node.Height}");
            Console.WriteLine($"  Label: {node.Annotations?[0]?.Content}");
        }
        else if (args.Element is Connector connector)
        {
            // ✅ Now you can access Connector-specific properties
            Console.WriteLine($"Connector [{connector.ID}] moved");
            Console.WriteLine($"  Source: {connector.SourceID}, Target: {connector.TargetID}");
        }

        // Alternative: read position from the selector's bounding box
        if (args.NewValue != null)
        {
            Console.WriteLine($"Selection box after move:");
            Console.WriteLine($"  OffsetX: {args.NewValue.OffsetX}  OffsetY: {args.NewValue.OffsetY}");
            Console.WriteLine($"  Width: {args.NewValue.Width}    Height: {args.NewValue.Height}");
        }

        if (args.OldValue != null)
        {
            Console.WriteLine($"Selection box before move:");
            Console.WriteLine($"  OffsetX: {args.OldValue.OffsetX}  OffsetY: {args.OldValue.OffsetY}");
        }
    }
}
```

### `PositionChangedEventArgs` properties

| Property | Type | Description |
|---|---|---|
| `Element` | `IDiagramObject?` | The node or connector currently being dragged |
| `NewValue` | `DiagramSelectionSettings?` | The selector's state (position, size) **after** the drag operation |
| `OldValue` | `DiagramSelectionSettings?` | The selector's state (position, size) **before** the drag operation |

```csharp
// ✅ Pattern-match Element to get the specific node or connector
if (args.Element is Node n)
    Console.WriteLine($"Moved node: {n.ID}  new pos: ({n.OffsetX}, {n.OffsetY})");
else if (args.Element is Connector c)
    Console.WriteLine($"Moved connector: {c.ID}");

// ✅ Use NewValue / OldValue for the bounding-box of the selection
double deltaX = (args.NewValue?.OffsetX ?? 0) - (args.OldValue?.OffsetX ?? 0);
double deltaY = (args.NewValue?.OffsetY ?? 0) - (args.OldValue?.OffsetY ?? 0);
Console.WriteLine($"Moved by: ({deltaX}, {deltaY})");
```

> **⚠️ `args.NewValue` and `args.OldValue` are `DiagramSelectionSettings?`**, not a `Node` with `OffsetX`/`OffsetY` fields.  
> They represent the **selector bounding box**, not the individual node position.  
> To read the moved node's position, either cast `args.Element` as `Node`, or read from the `DiagramSelectionSettings`:
> ```csharp
> // ❌ Wrong — NewValue is DiagramSelectionSettings?, not a Node
> double x = args.NewValue.OffsetX; // compiles but is selector bbox, not node center
>
> // ✅ Correct — read node position from Element
> if (args.Element is Node n)
>     Console.WriteLine($"({n.OffsetX}, {n.OffsetY})");
>
> // ✅ Also correct — selector bbox from NewValue (null-safe)
> Console.WriteLine($"({args.NewValue?.OffsetX}, {args.NewValue?.OffsetY})");
> ```

### SizeChanging / SizeChanged

Fire when a node is resized:

```razor
<SfDiagramComponent SizeChanging="OnSizeChanging" SizeChanged="OnSizeChanged" />

@code {
    private void OnSizeChanging(Syncfusion.Blazor.Diagram.SizeChangingEventArgs args)
    {
        args.Cancel = true; // block resize
    }

    private void OnSizeChanged(Syncfusion.Blazor.Diagram.SizeChangedEventArgs args)
    {
        // ✅ args.Element is DiagramSelectionSettings — NOT Node.
        // Cast it and read the first resized node from its .Nodes collection.
        if (args.Element is DiagramSelectionSettings sel && sel.Nodes.Count > 0)
        {
            var node = sel.Nodes[0];
            double w = args.NewValue.Width;   // plain double — no ?? needed
            double h = args.NewValue.Height;  // plain double — no ?? needed
            Console.WriteLine($"Node [{node.ID}] resized to {Math.Round(w)} x {Math.Round(h)}");
        }
    }
}
```

> **⚠️ `SizeChangedEventArgs.Element` is typed as `DiagramSelectionSettings`**, not `Node`.  
> Pattern-matching `args.Element is Node n` always fails with `CS8121`.  
> Cast to `DiagramSelectionSettings` and read `.Nodes[0]` to get the resized node:
> ```csharp
> // ❌ Wrong — CS8121: DiagramSelectionSettings cannot match Node
> if (args.Element is Node n) { }
>
> // ✅ Correct — Element is DiagramSelectionSettings
> if (args.Element is DiagramSelectionSettings sel && sel.Nodes.Count > 0)
> {
>     var node = sel.Nodes[0];
>     double w = args.NewValue.Width;
>     double h = args.NewValue.Height;
> }
> ```

> **⚠️ `args.NewValue.Width` and `args.NewValue.Height` are plain `double`**, not `double?`.  
> Using `??` on them causes `CS0019`. Assign them directly:
> ```csharp
> // ❌ Wrong — CS0019
> double w = args.NewValue.Width ?? 0;
>
> // ✅ Correct
> double w = args.NewValue.Width;
> ```

### RotationChanging / RotationChanged

Fire when a node is rotated:

```razor
<SfDiagramComponent RotationChanging="OnRotationChanging"
                    RotationChanged="OnRotationChanged" />

@code {
    private void OnRotationChanging(Syncfusion.Blazor.Diagram.RotationChangingEventArgs args)
    {
        args.Cancel = true; // block rotation
    }

    private void OnRotationChanged(Syncfusion.Blazor.Diagram.RotationChangedEventArgs args)
    {
    }
}
```

### SelectionChanging / SelectionChanged

Fire when the selection set changes:

```razor
<SfDiagramComponent SelectionChanging="OnSelectionChanging"
                    SelectionChanged="OnSelectionChanged" />

@code {
    private void OnSelectionChanging(Syncfusion.Blazor.Diagram.SelectionChangingEventArgs args)
    {
        args.Cancel = true; // prevent selection change
    }

    private void OnSelectionChanged(Syncfusion.Blazor.Diagram.SelectionChangedEventArgs args)
    {
        // args.NewValue  — ObservableCollection<IDiagramObject>? — elements selected after the event
        // args.OldValue  — ObservableCollection<IDiagramObject>? — elements that were selected before
        // args.Type      — CollectionChangedAction (ObjectAdded / ObjectRemoved)
        // args.ActionTrigger — DiagramAction — what caused the selection change

        if (args.NewValue != null)
        {
            foreach (var obj in args.NewValue)
            {
                if (obj is Node node)
                    Console.WriteLine($"Newly selected node: {node.ID}");
                else if (obj is Connector conn)
                    Console.WriteLine($"Newly selected connector: {conn.ID}");
            }
        }

        if (args.OldValue != null)
        {
            foreach (var obj in args.OldValue)
            {
                if (obj is Node node)
                    Console.WriteLine($"Deselected node: {node.ID}");
            }
        }

        Console.WriteLine($"Change type: {args.Type}");             // ObjectAdded / ObjectRemoved
        Console.WriteLine($"Triggered by: {args.ActionTrigger}");   // DiagramAction enum value
    }
}
```

> **⚠️ `SelectionChangedEventArgs` name collision:** If your page also uses `@using Syncfusion.Blazor.Buttons`  
> (or other Syncfusion packages), `SelectionChangedEventArgs` becomes ambiguous. Always qualify it:
> ```csharp
> // ✅ Fully qualified
> private void OnSelectionChanged(Syncfusion.Blazor.Diagram.SelectionChangedEventArgs args) { }
> ```

### `SelectionChangedEventArgs` properties

| Property | Type | Description |
|---|---|---|
| `NewValue` | `ObservableCollection<IDiagramObject>?` | Elements that are selected **after** the event fires |
| `OldValue` | `ObservableCollection<IDiagramObject>?` | Elements that were selected **before** the event fired; empty if nothing was previously selected |
| `Type` | `CollectionChangedAction` | Whether items were **added** (`ObjectAdded`) or **removed** (`ObjectRemoved`) from the selection |
| `ActionTrigger` | `DiagramAction` | The actual cause of the selection change (e.g., user interaction, programmatic call) |

### Understanding IDiagramObject and Casting

> **⚠️ Critical:** `args.NewValue` contains **`IDiagramObject` items**, not `Node` or `Connector` directly.  
> `IDiagramObject` is an interface that both `Node` and `Connector` implement. To access element-specific properties like `ID`, `Annotations`, or connector-specific properties, you **must cast** to `Node` or `Connector`.

**Why casting is required:**
- `IDiagramObject` is a common interface for all diagram elements
- It provides only basic properties shared across all element types
- `Node` and `Connector` have type-specific properties not available on `IDiagramObject`
- Attempting to access these properties without casting causes `CS1061` (member not found) errors

**Complete working example with proper casting:**
```razor
<SfDiagramComponent SelectionChanged="OnSelectionChanged" />

@code {
    private void OnSelectionChanged(Syncfusion.Blazor.Diagram.SelectionChangedEventArgs args)
    {
        if (args?.NewValue?.Count > 0)
        {
            foreach (var item in args.NewValue)
            {
                if (item is Node selectedNode)
                {
                    // ✅ Now you can access Node-specific properties
                    var nodeId = selectedNode.ID;
                    var label = selectedNode.Annotations?[0]?.Content;
                    var offsetX = selectedNode.OffsetX;
                    var offsetY = selectedNode.OffsetY;
                    
                    Console.WriteLine($"Selected Node: ID={nodeId}, Label={label}, Position=({offsetX}, {offsetY})");
                }
                else if (item is Connector selectedConnector)
                {
                    // ✅ Now you can access Connector-specific properties
                    var connectorId = selectedConnector.ID;
                    var sourceNode = selectedConnector.SourceID;
                    var targetNode = selectedConnector.TargetID;
                    
                    Console.WriteLine($"Selected Connector: ID={connectorId}, From={sourceNode} To={targetNode}");
                }
            }
        }
    }
}
```

**Common pitfalls:**
```csharp
// ❌ Wrong — IDiagramObject has no ID property (well, it does via interface, but shows confusion)
// More importantly, you can't access Node/Connector-specific props like Annotations
foreach (var item in args.NewValue)
{
    Console.WriteLine(item.ID); // May compile but incorrect intent
    var label = item.Annotations[0].Content; // ❌ CS1061 — Annotations not on IDiagramObject
}

// ✅ Correct — always cast first
foreach (var item in args.NewValue)
{
    if (item is Node node)
        Console.WriteLine($"Node {node.ID}: {node.Annotations?[0]?.Content}");
    else if (item is Connector conn)
        Console.WriteLine($"Connector {conn.ID}");
}
```

```csharp
// ✅ Iterate args.NewValue directly — it is ObservableCollection<IDiagramObject>
if (args.NewValue != null)
{
    foreach (var obj in args.NewValue)
    {
        if (obj is Node node)        Console.WriteLine($"Added to selection: {node.ID}");
        else if (obj is Connector c) Console.WriteLine($"Added to selection: {c.ID}");
    }
}

// ✅ Check what triggered the change
Console.WriteLine($"Type: {args.Type}");                // ObjectAdded / ObjectRemoved
Console.WriteLine($"Trigger: {args.ActionTrigger}");    // DiagramAction enum value
```

### CollectionChanging / CollectionChanged

`CollectionChanging` fires **before** a node or connector is added or removed (cancellable).  
`CollectionChanged` fires **after** the collection has been updated:

```razor
<SfDiagramComponent CollectionChanging="OnCollectionChanging"
                    CollectionChanged="OnCollectionChanged" />

@code {
    private void OnCollectionChanging(Syncfusion.Blazor.Diagram.CollectionChangingEventArgs args)
    {
        // args.Cancel = true — prevent the add/remove
        args.Cancel = true;
    }
}
```

---

### CollectionChanged

Fires when a node or connector is **added to or removed from** the diagram at runtime:

```razor
<SfDiagramComponent CollectionChanged="OnCollectionChanged" />

@code {
    private void OnCollectionChanged(Syncfusion.Blazor.Diagram.CollectionChangedEventArgs args)
    {
        // args.Action        — CollectionChangedAction — whether the element was added or removed
        // args.ActionTrigger — DiagramAction           — what caused the change (interaction, tool, etc.)
        // args.Element       — NodeBase?               — the node or connector that was added/removed/modified

        if (args.Action == CollectionChangedAction.Add)
        {
            if (args.Element is Node node)
                Console.WriteLine($"Node added: {node.ID}");
            else if (args.Element is Connector conn)
                Console.WriteLine($"Connector added: {conn.ID}");
        }
        else if (args.Action == CollectionChangedAction.Remove)
        {
            Console.WriteLine($"Element removed: {args.Element?.ID}");
        }

        Console.WriteLine($"Triggered by: {args.ActionTrigger}"); // DiagramAction enum value
    }
}
```

### `CollectionChangedEventArgs` properties

| Property | Type | Description |
|---|---|---|
| `Action` | `CollectionChangedAction` | The type of change — `Add` when an element is added, `Remove` when an element is removed |
| `ActionTrigger` | `DiagramAction` | The current action being performed (e.g., user interaction, drawing tool, programmatic call) |
| `Element` | `NodeBase?` | The actual node or connector that was added, removed, or modified — pattern-match as `Node` or `Connector` |

```csharp
// ✅ Pattern-match Element as Node or Connector — it is typed as NodeBase?
if (args.Element is Node n)
    Console.WriteLine($"Node [{n.ID}] — Action: {args.Action}  Trigger: {args.ActionTrigger}");
else if (args.Element is Connector c)
    Console.WriteLine($"Connector [{c.ID}] — Action: {args.Action}  Trigger: {args.ActionTrigger}");
```

> **⚠️ `args.Element` is typed as `NodeBase?`** — not `Node` or `Connector` directly.  
> Always null-check or pattern-match before accessing it:
> ```csharp
> // ❌ Wrong — Element is NodeBase?, not Node; direct cast throws InvalidCastException
> var node = (Node)args.Element;
>
> // ✅ Correct — safe pattern match
> if (args.Element is Node node) { Console.WriteLine(node.ID); }
> if (args.Element is Connector conn) { Console.WriteLine(conn.ID); }
> ```

---

### SourcePointChanging / SourcePointChanged

Fire when a connector's **source endpoint** is dragged:

```razor
<SfDiagramComponent SourcePointChanging="OnSourcePointChanging"
                    SourcePointChanged="OnSourcePointChanged" />

@code {
    private void OnSourcePointChanging(EndPointChangingEventArgs args)
    {
        // args.Cancel = true — block the source point change
        args.Cancel = true;
    }

    private void OnSourcePointChanged(EndPointChangedEventArgs args)
    {
        // args.Connector — the connector whose source point changed
        // args.NewValue  — DiagramPoint — new source point position
        // args.OldValue  — DiagramPoint — previous source point position
        Console.WriteLine($"Source moved to ({args.NewValue?.X}, {args.NewValue?.Y})");
    }
}
```

### TargetPointChanging / TargetPointChanged

Fire when a connector's **target endpoint** is dragged:

```razor
<SfDiagramComponent TargetPointChanging="OnTargetPointChanging"
                    TargetPointChanged="OnTargetPointChanged" />

@code {
    private void OnTargetPointChanging(EndPointChangingEventArgs args)
    {
        // args.Cancel = true — block the target point change
    }

    private void OnTargetPointChanged(EndPointChangedEventArgs args)
    {
        // args.Connector — the connector whose target point changed
        // args.NewValue  — DiagramPoint — new target point position
        // args.OldValue  — DiagramPoint — previous target point position
        Console.WriteLine($"Target moved to ({args.NewValue?.X}, {args.NewValue?.Y})");
    }
}
```

| Event pair | Args type (Changing) | Args type (Changed) | Has Cancel? |
|---|---|---|---|
| `SourcePointChanging` / `SourcePointChanged` | `EndPointChangingEventArgs` | `EndPointChangedEventArgs` | Yes |
| `TargetPointChanging` / `TargetPointChanged` | `EndPointChangingEventArgs` | `EndPointChangedEventArgs` | Yes |

> **⚠️ `SourcePointChanging`/`TargetPointChanging` use `EndPointChangingEventArgs`** — not `PositionChangingEventArgs`. These events fire only when the **connector endpoint** itself is dragged, not when the whole connector moves with a node.

---

### SegmentCollectionChange

Fires when a connector's **segment collection is modified** (e.g. segments added or removed during interaction):

```razor
<SfDiagramComponent SegmentCollectionChange="OnSegmentCollectionChange" />

@code {
    private void OnSegmentCollectionChange(SegmentCollectionChangeEventArgs args)
    {
        // args.Element  — the connector whose segments changed
        // args.NewValue — updated segment collection
        // args.Cancel = true — prevent the segment change
        Console.WriteLine($"Segment changed on connector: {(args.Element as Connector)?.ID}");
    }
}
```

---

### PropertyChanged

Fires when a **node or connector property** is modified at runtime (e.g. style, size, position set programmatically):

```razor
<SfDiagramComponent PropertyChanged="OnPropertyChanged" />

@code {
    private void OnPropertyChanged(Syncfusion.Blazor.Diagram.PropertyChangedEventArgs args)
    {
        // ⚠️ args.Element is IDiagramObject? — you must cast to Node or Connector
        // args.Element — IDiagramObject? — the node or connector whose property changed
        // args.PropertyName — string — the name of the property that changed
        // args.NewValue — object? — the new value of the property
        // args.OldValue — object? — the old value of the property
        
        if (args.Element is Node node)
        {
            Console.WriteLine($"Node [{node.ID}] property changed: {args.PropertyName}");
            Console.WriteLine($"  Old value: {args.OldValue}");
            Console.WriteLine($"  New value: {args.NewValue}");
            
            // Now you can access Node-specific properties
            if (args.PropertyName == "Style")
            {
                var fill = node.Style?.Fill;
                var stroke = node.Style?.StrokeColor;
                Console.WriteLine($"  Fill: {fill}, Stroke: {stroke}");
            }
        }
        else if (args.Element is Connector conn)
        {
            Console.WriteLine($"Connector [{conn.ID}] property changed: {args.PropertyName}");
            
            // Now you can access Connector-specific properties
            if (args.PropertyName == "TargetID")
            {
                Console.WriteLine($"  Connector now targets: {conn.TargetID}");
            }
        }
    }
}
```

> **⚠️ Critical:** `args.Element` is `IDiagramObject?`, not `Node` or `Connector` directly.  
> You **must cast** to access type-specific properties. Attempting to access properties like `Annotations` or `Style` on `IDiagramObject` causes `CS1061` (member not found).

---

### ConnectionChanging / ConnectionChanged

Fire when a connector's source or target endpoint is dragged to a new node or port:

```razor
<SfDiagramComponent ConnectionChanging="OnConnectionChanging"
                    ConnectionChanged="OnConnectionChanged" />

@code {
    private void OnConnectionChanging(Syncfusion.Blazor.Diagram.ConnectionChangingEventArgs args)
    {
        args.Cancel = true; // prevent the connection change
    }

    private void OnConnectionChanged(Syncfusion.Blazor.Diagram.ConnectionChangedEventArgs args)
    {
        // args.Connector       — Connector?              — the connector whose endpoint changed
        // args.ConnectorAction — DiagramElementAction    — whether the source or target end moved
        // args.NewValue        — ConnectionObject?       — new source/target node or port after the change
        // args.OldValue        — ConnectionObject?       — previous source/target node or port before the change

        if (args.Connector != null)
            Console.WriteLine($"Connector: {args.Connector.ID}");

        // Distinguish source-end change from target-end change
        Console.WriteLine($"Endpoint changed: {args.ConnectorAction}"); // DiagramElementAction enum

        // NewValue — what the endpoint is NOW connected to
        if (args.NewValue != null)
        {
            Console.WriteLine($"New NodeID:  {args.NewValue.NodeID}");   // node the endpoint landed on
            Console.WriteLine($"New PortID:  {args.NewValue.PortID}");   // port, if any
        }

        // OldValue — what the endpoint WAS connected to
        if (args.OldValue != null)
        {
            Console.WriteLine($"Old NodeID:  {args.OldValue.NodeID}");
            Console.WriteLine($"Old PortID:  {args.OldValue.PortID}");
        }
    }
}
```

### `ConnectionChangedEventArgs` properties

| Property | Type | Description |
|---|---|---|
| `Connector` | `Connector?` | The connector whose source or target endpoint was changed |
| `ConnectorAction` | `DiagramElementAction` | Indicates which endpoint moved — source end or target end |
| `NewValue` | `ConnectionObject?` | The **current** (after) source or target — holds `NodeID` and `PortID` of the new connection |
| `OldValue` | `ConnectionObject?` | The **previous** (before) source or target — holds `NodeID` and `PortID` of the old connection |

```csharp
// ✅ Check which endpoint changed
if (args.ConnectorAction == DiagramElementAction.ConnectorSourceEnd)
    Console.WriteLine("Source endpoint was moved.");
else if (args.ConnectorAction == DiagramElementAction.ConnectorTargetEnd)
    Console.WriteLine("Target endpoint was moved.");

// ✅ Read NodeID / PortID from ConnectionObject (null-safe)
string newNode = args.NewValue?.NodeID ?? "(none)";
string newPort = args.NewValue?.PortID ?? "(none)";
string oldNode = args.OldValue?.NodeID ?? "(none)";
Console.WriteLine($"Reconnected: {oldNode} → {newNode}  (port: {newPort})");
```

> **⚠️ `args.NewValue` and `args.OldValue` are `ConnectionObject?`**, not `Node`.  
> They do **not** have `OffsetX`/`OffsetY`. Access node and port identity via `.NodeID` and `.PortID`:
> ```csharp
> // ❌ Wrong — ConnectionObject has no OffsetX
> double x = args.NewValue.OffsetX;
>
> // ✅ Correct — read NodeID and PortID
> string nodeId = args.NewValue?.NodeID ?? string.Empty;
> string portId = args.NewValue?.PortID ?? string.Empty;
> ```

---

### TextChanged

Fires after inline text editing completes:

```razor
<SfDiagramComponent TextChanged="OnTextChanged" />

@code {
    private void OnTextChanged(TextChangeEventArgs args)
    {
        // ⚠️ args.Element is IDiagramObject? — you must cast to Node or Connector
        // args.Element — IDiagramObject? — the node or connector being edited
        // args.Annotation — Annotation? — the specific annotation being edited
        // args.NewValue — string? — updated text
        // args.OldValue — string? — previous text
        
        if (args.Element is Node node)
        {
            // ✅ Now you can access Node-specific properties
            Console.WriteLine($"Node [{node.ID}] text changed");
            Console.WriteLine($"  Old text: '{args.OldValue}'");
            Console.WriteLine($"  New text: '{args.NewValue}'");
            Console.WriteLine($"  Annotation ID: {args.Annotation?.ID}");
        }
        else if (args.Element is Connector connector)
        {
            // ✅ Now you can access Connector-specific properties
            Console.WriteLine($"Connector [{connector.ID}] text changed");
            Console.WriteLine($"  From '{args.OldValue}' to '{args.NewValue}'");
            Console.WriteLine($"  Source: {connector.SourceID}, Target: {connector.TargetID}");
        }
    }
}
```

> **⚠️ `TextChangedEventArgs` does NOT exist** — using it causes `CS0246`.  
> The correct event args type is **`TextChangeEventArgs`** (no `d`):
> ```csharp
> // ❌ Wrong — CS0246: TextChangedEventArgs not found
> private void OnTextChanged(TextChangedEventArgs args) { }
>
> // ✅ Correct
> private void OnTextChanged(TextChangeEventArgs args) { }
> ```

> **⚠️ Critical:** `args.Element` is `IDiagramObject?`, not `Node` or `Connector` directly.  
> You **must cast** to access type-specific properties. Attempting to access properties without casting causes `CS1061` (member not found).

---

## Drag-and-Drop Events

These fire when symbols are dragged from the **SymbolPalette** into the diagram. All use `IDiagramObject` elements that must be cast:

```razor
<SfDiagramComponent DragStart="OnDragStart"
                    Dragging="OnDragging"
                    DragLeave="OnDragLeave"
                    DragDrop="OnDragDrop" />

@code {
    private void OnDragStart(Syncfusion.Blazor.Diagram.DragStartEventArgs args)
    {
        // ⚠️ args.Element is IDiagramObject? — cast to Node or Connector
        if (args.Element is Node node)
        {
            // Modify the node before it's added
            node.Width = 300;
            node.Height = 300;
            node.Style.Fill = "#FF5722";
        }
        else if (args.Element is Connector conn)
        {
            conn.Style.StrokeWidth = 3;
        }
    }

    private void OnDragging(DraggingEventArgs args)
    {
        // ⚠️ args.Element is IDiagramObject? — the element being dragged
        if (args.Element is DiagramSelectionSettings selector)
        {
            Console.WriteLine($"Dragging at position: ({args.Position?.X}, {args.Position?.Y})");
        }
    }

    private void OnDragLeave(DragLeaveEventArgs args)
    {
        // ⚠️ args.Element is IDiagramObject? — element leaving the diagram
        if (args.Element is Node node)
            Console.WriteLine($"Node [{node.ID}] left the diagram");
    }

    private void OnDragDrop(DropEventArgs args)
    {
        // ⚠️ args.Element is IDiagramObject? — the dropped node
        // args.Target is IDiagramObject? — the target node/connector if dropped on one
        // args.Position — drop location
        // args.Cancel = true — reject the drop
        
        if (args.Element is Node droppedNode)
        {
            Console.WriteLine($"Dropped node: {droppedNode.ID}");
            
            if (args.Target is Node targetNode)
                Console.WriteLine($"  Dropped on node: {targetNode.ID}");
        }
    }
}
```

> **⚠️ Critical:** All drag-drop event arguments contain `IDiagramObject?` elements.  
> You **must cast** to `Node` or `Connector` to access properties like `ID`, `Width`, `Height`, `Style`, or connector-specific properties.
> Attempting to access type-specific properties without casting causes `CS1061` (member not found).

> **⚠️ `DragStartEventArgs` is ambiguous** when `Syncfusion.Blazor.Popups` (or other packages that expose `DragStartEventArgs`) is also referenced.  
> Always qualify it as `Syncfusion.Blazor.Diagram.DragStartEventArgs`:
> ```csharp
> // ❌ Wrong — CS0104: ambiguous reference between Diagram and Popups
> private void OnDragStart(DragStartEventArgs args) { }
>
> // ✅ Correct — fully qualified
> private void OnDragStart(Syncfusion.Blazor.Diagram.DragStartEventArgs args) { }
> ```

> **⚠️ `DragEnterEventArgs` does NOT exist** in `Syncfusion.Blazor.Diagram`.  
> There is **no `DragEnter` event** on `SfDiagramComponent` that receives a `DragEnterEventArgs`.  
> The available drag events on `SfDiagramComponent` are: `DragStart`, `Dragging`, `DragLeave`, `DragDrop` — all for **SymbolPalette** drag-and-drop only.  
> For tracking when a node is **being moved** (internal drag), use `PositionChanged`.

```csharp
// ❌ Wrong — DragEnterEventArgs does not exist
private void OnDragEnter(DragEnterEventArgs args) { }

// ❌ Wrong — OnPositionChange does not exist on SfDiagramComponent
<SfDiagramComponent OnPositionChange="OnPositionChange" />

// ✅ Correct — use PositionChanged
<SfDiagramComponent PositionChanged="OnPositionChanged" />

private void OnPositionChanged(PositionChangedEventArgs args)
{
    if (args.Element is Node n)
        Console.WriteLine($"Node {n.ID} moved to ({n.OffsetX}, {n.OffsetY})");
}
```

---

## User Handle Events

### FixedUserHandleClick

Fires when a fixed user handle (custom action button) on a selected element is clicked. The event argument contains the clicked handle and the element it belongs to:

```razor
<SfDiagramComponent FixedUserHandleClick="OnFixedUserHandleClick">
    <DiagramSelectionSettings>
        <!-- User handles configured here -->
    </DiagramSelectionSettings>
</SfDiagramComponent>

@code {
    private void OnFixedUserHandleClick(FixedUserHandleClickEventArgs args)
    {
        // ⚠️ args.Element is IDiagramObject? — you must cast to Node or Connector
        // args.Element — IDiagramObject? — the node or connector with the clicked handle
        // args.FixedUserHandle — FixedUserHandle? — the handle that was clicked
        
        if (args.Element is Node node)
        {
            // ✅ Now you can access Node-specific properties
            Console.WriteLine($"User handle clicked on node: {node.ID}");
            Console.WriteLine($"  Handle name: {args.FixedUserHandle?.Name}");
            Console.WriteLine($"  Node label: {node.Annotations?[0]?.Content}");
            
            // Perform custom action based on handle name
            if (args.FixedUserHandle?.Name == "clone")
            {
                // Clone the node
                Console.WriteLine("  Cloning node...");
            }
            else if (args.FixedUserHandle?.Name == "delete")
            {
                // Delete the node
                Console.WriteLine("  Deleting node...");
            }
        }
        else if (args.Element is Connector connector)
        {
            // ✅ Now you can access Connector-specific properties
            Console.WriteLine($"User handle clicked on connector: {connector.ID}");
            Console.WriteLine($"  Handle name: {args.FixedUserHandle?.Name}");
            Console.WriteLine($"  Connects {connector.SourceID} to {connector.TargetID}");
        }
    }
}
```

> **⚠️ Critical:** `args.Element` is `IDiagramObject?`, not `Node` or `Connector` directly.  
> You **must cast** to access type-specific properties like `ID`, `Annotations`, or `SourceID`.  
> Attempting to access type-specific properties without casting causes `CS1061` (member not found).

---

## History (Undo/Redo) Events

### HistoryChanged

Fires after any undo/redo action:

```razor
<SfDiagramComponent HistoryChanged="OnHistoryChanged" />

@code {
    private void OnHistoryChanged(HistoryChangedEventArgs args)
    {
        // args.Action — HistoryChangedAction (Undo, Redo, etc.)
        // args.RedoStack / UndoStack — stacks after the change
    }
}
```

---

## Auto-Scroll Events

### OnAutoScrollChange

Fires when auto-scroll activates as an element is dragged near the canvas edge:

```razor
<SfDiagramComponent OnAutoScrollChange="OnAutoScrollChange">
    <ScrollSettings EnableAutoScroll="true" />
</SfDiagramComponent>

@code {
    private void OnAutoScrollChange(AutoScrollChangeEventArgs args)
    {
        args.Cancel = true; // stop auto-scroll
        args.Delay = new TimeSpan(0, 0, 0, 1, 0); // delay before scrolling
    }
}
```

---

## Events Quick-Reference Table

| Event | Fires When | Args Type | Has Cancel? |
|-------|-----------|-----------|-------------|
| `Created` | Diagram fully rendered | `object` | No |
| `NodeCreating` | Each node is initialised | `IDiagramObject` | No |
| `ConnectorCreating` | Each connector is initialised | `IDiagramObject` | No |
| `Click` | Mouse click on element or canvas | `ClickEventArgs` | No |
| `KeyDown` / `KeyUp` | Key pressed/released | `KeyEventArgs` | No |
| `MouseEnter` | Pointer enters a node or connector | `DiagramElementMouseEventArgs` | No |
| `MouseLeave` | Pointer exits a node or connector | `DiagramElementMouseEventArgs` | No |
| `MouseHover` | Pointer hovers over a node or connector | `DiagramElementMouseEventArgs` | No |
| `PositionChanging` / `PositionChanged` | Node/connector moved | `PositionChangingEventArgs` / `PositionChangedEventArgs` | Yes (Changing) |
| `SizeChanging` / `SizeChanged` | Node resized | `SizeChangingEventArgs` / `SizeChangedEventArgs` | Yes (Changing) |
| `RotationChanging` / `RotationChanged` | Node rotated | `RotationChangingEventArgs` / `RotationChangedEventArgs` | Yes (Changing) |
| `SelectionChanging` / `SelectionChanged` | Selection changes | `SelectionChangingEventArgs` / `SelectionChangedEventArgs` | Yes (Changing) |
| `CollectionChanging` / `CollectionChanged` | Node or connector added/removed | `CollectionChangingEventArgs` / `CollectionChangedEventArgs` | Yes (Changing) |
| `SourcePointChanging` / `SourcePointChanged` | Connector source endpoint dragged | `EndPointChangingEventArgs` / `EndPointChangedEventArgs` | Yes (Changing) |
| `TargetPointChanging` / `TargetPointChanged` | Connector target endpoint dragged | `EndPointChangingEventArgs` / `EndPointChangedEventArgs` | Yes (Changing) |
| `ConnectionChanging` / `ConnectionChanged` | Connector reconnected to new node/port | `ConnectionChangingEventArgs` / `ConnectionChangedEventArgs` | Yes (Changing) |
| `SegmentCollectionChange` | Connector segment collection modified | `SegmentCollectionChangeEventArgs` | Yes |
| `PropertyChanged` | Node or connector property modified at runtime | `PropertyChangedEventArgs` | No |
| `TextChanged` | Inline annotation editing completed | `TextChangeEventArgs` | No |
| `DragStart` / `Dragging` / `DragLeave` / `DragDrop` | Symbol palette drag operations | Various | Yes (DragDrop) |
| `FixedUserHandleClick` | Fixed user handle clicked | `FixedUserHandleClickEventArgs` | No |
| `HistoryChanged` | Undo/Redo action | `HistoryChangedEventArgs` | No |
| `OnAutoScrollChange` | Auto-scroll during drag | `AutoScrollChangeEventArgs` | Yes |

---

## Common Gotchas

- **⚠️ `IDiagramObject` casting is required in MOST events** — Many event arguments (PropertyChanged, DragStart, Dragging, DragLeave, DragDrop, PositionChanged, TextChanged, MouseEnter, MouseLeave, MouseHover, Click, KeyDown, KeyUp, FixedUserHandleClick) expose `Element`, `Target`, or `Targets` as `IDiagramObject?`, which is an **interface**, not a concrete type. To access type-specific properties like `Node.Annotations`, `Node.OffsetX`, or `Connector.SourceID`, **you MUST cast** using pattern matching: `if (args.Element is Node node) { var ann = node.Annotations; }`. Attempting to access type-specific properties directly on `IDiagramObject` causes `CS1061` ("member not found on interface type"). See each event section for complete casting examples.
- **`Created` fires once** — do not register one-time initialization logic in `OnAfterRenderAsync` if it depends on fully rendered nodes; use `Created` instead
- **`Changing` events with `Cancel = true`** block the action without triggering the corresponding `Changed` event
- **There is NO `OnDoubleClick` event** — double-clicks are detected via the `Click` event by reading `args.Count` as an `int` and comparing it: `int c = args.Count; if (c == 2) { ... }`
- **`DoubleClickEventArgs` does NOT exist** — attempting to use it will cause a compile error; use `Syncfusion.Blazor.Diagram.ClickEventArgs` from the `Click` event instead
- **The correct event attribute name is `Click`** (not `Clicked`) when binding in markup — using `Clicked` causes `InvalidOperationException: does not have a property matching the name 'Clicked'`
- **`args.Count` is a method/property returning `int`** — comparing it directly with `== int` inline without storing it first causes `CS0019` ("method group" error); always store: `int count = args.Count;`
- **`ClickEventArgs` is ambiguous** when multiple Syncfusion packages are used — qualify it as `Syncfusion.Blazor.Diagram.ClickEventArgs`
- **`SelectionChangedEventArgs` is ambiguous** when `Syncfusion.Blazor.Buttons` is referenced — qualify it as `Syncfusion.Blazor.Diagram.SelectionChangedEventArgs`
- **`SelectionChangedEventArgs.NewValue` is `ObservableCollection<IDiagramObject>?`** — it is a nullable collection of `IDiagramObject`, NOT a `DiagramSelectionSettings`. Iterate it with `foreach` and pattern-match each element as `Node` or `Connector`. Also available: `OldValue` (previously selected items), `Type` (`CollectionChangedAction` — `ObjectAdded`/`ObjectRemoved`), and `ActionTrigger` (`DiagramAction` — the cause of the change)
- **`IDiagramObject` items in `SelectionChangedEventArgs.NewValue` MUST be cast to access type-specific properties** — `IDiagramObject` is an interface; to access `Node` properties like `Annotations`, `OffsetX`, or `Connector` properties like `SourceID`, pattern-match first: `if (item is Node node) { var annotations = node.Annotations; }`. Attempting to access type-specific properties without casting causes `CS1061` (member not found)
- **`SizeChangedEventArgs.Element` is also `DiagramSelectionSettings`**, not `Node` — `args.Element is Node n` causes `CS8121`. Cast it correctly: `if (args.Element is DiagramSelectionSettings sel && sel.Nodes.Count > 0) { var node = sel.Nodes[0]; }`
- **`CollectionChangedEventArgs.Element` is typed as `NodeBase?`** — never cast it directly to `Node`; use `is Node n` / `is Connector c` pattern matching. `Action` (`CollectionChangedAction`) tells you whether the element was added or removed; `ActionTrigger` (`DiagramAction`) tells you what caused the change
- **`DragEnterEventArgs` does NOT exist** — there is no `DragEnter` event on `SfDiagramComponent`; use `PositionChanged` to track node movement
- **`OnPositionChange` does NOT exist** as an event attribute on `SfDiagramComponent` — using it causes `InvalidOperationException: does not have a property matching the name 'OnPositionChange'`. The correct attribute name is `PositionChanged`
- **`PositionChangedEventArgs.NewValue` and `OldValue` are `DiagramSelectionSettings?`**, not `Node` — they expose the **selector bounding box** (`OffsetX`, `OffsetY`, `Width`, `Height`), not the individual node center. To get the moved node's position, pattern-match `args.Element is Node n` and read `n.OffsetX` / `n.OffsetY` directly. Always null-check: `args.NewValue?.OffsetX`
- **`PositionChangedEventArgs.Element` is `IDiagramObject?`** — pattern-match as `Node` or `Connector` before accessing type-specific members; accessing it without a null check or cast causes `NullReferenceException`
- **`ConnectionChangedEventArgs.NewValue` and `OldValue` are `ConnectionObject?`**, not `Node` — they carry only `NodeID` and `PortID` strings identifying the connected node/port. Do not attempt to read `OffsetX`/`OffsetY` from them. Use `ConnectorAction` (`DiagramElementAction`) to distinguish whether the source or target endpoint was moved, and null-check before reading: `args.NewValue?.NodeID`
- **`ConnectionChangedEventArgs.Connector` is `Connector?`** — null-check before accessing it; it holds the connector whose endpoint changed, not the node
- **`DragDrop` / `DragLeave` / `DragStart` / `Dragging` events only fire for SymbolPalette symbols** — internal node moves use `PositionChanged`
- **`args.NewValue.Width` and `args.NewValue.Height` in `SizeChangedEventArgs` are plain `double`** (not `double?`) — assign them directly: `double w = args.NewValue.Width;`. Using `??` on them causes `CS0019` ("operator `??` cannot be applied to `double` and `int`")
- **`HistoryChanged` fires for both user actions and programmatic changes** — check `args.Action` to differentiate
- **`TextChangedEventArgs` does NOT exist** — causes `CS0246`. The correct type is **`TextChangeEventArgs`** (no `d`): `private void OnTextChanged(TextChangeEventArgs args) { }`
- **`DragStartEventArgs` is ambiguous** when `Syncfusion.Blazor.Popups` is also referenced — causes `CS0104`. Always qualify: `Syncfusion.Blazor.Diagram.DragStartEventArgs`
- **`NodeCreating` and `ConnectorCreating` parameter type is `IDiagramObject`** — not `Node` or `Connector`. Always cast: `if (obj is Node node) { ... }`. Accessing `.Style` directly on `IDiagramObject` causes `CS1061`
- **`MouseEnter`, `MouseLeave`, `MouseHover` all use `DiagramElementMouseEventArgs`** — access the hovered element via `args.Element` and pattern-match as `Node` or `Connector`
- **`SourcePointChanging`/`TargetPointChanging` use `EndPointChangingEventArgs`**, not `PositionChangingEventArgs` — these events fire only when the connector endpoint itself is dragged, not when the whole connector moves
- **`CollectionChanging` is the cancellable counterpart to `CollectionChanged`** — set `args.Cancel = true` in `CollectionChanging` to block the add/remove. `CollectionChanged` has no cancel
- **`SegmentCollectionChange` is cancellable** — set `args.Cancel = true` to block segment modifications; cast `args.Element` as `Connector` to identify which connector changed
- **`PropertyChanged` fires for programmatic changes as well as user interactions** — check `args.Element is Node` or `args.Element is Connector` to identify what changed
