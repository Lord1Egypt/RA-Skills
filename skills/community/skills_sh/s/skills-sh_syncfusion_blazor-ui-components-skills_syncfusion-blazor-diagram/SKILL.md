---
name: syncfusion-blazor-diagram
description: Build and troubleshoot Syncfusion Blazor diagrams using SfDiagramComponent. Trigger for flowcharts, org charts, mind maps, BPMN, UML sequence, swimlanes, symbol palettes, nodes/connectors/ports/annotations, layouts, data binding, serialization (load/save), export/print, and collaborative editing questions. Provide Blazor + Syncfusion setup steps, configuration patterns, and sample snippets.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion Blazor Diagram

A comprehensive skill for building interactive diagrams with the Syncfusion Blazor Diagram component — flowcharts, organizational charts, mind maps, BPMN process diagrams, UML sequence diagrams, network diagrams, and more.

## When to Use This Skill

Use this skill when you need to:
- Create flowcharts, org charts, mind maps, or network diagrams in Blazor
- Work with `SfDiagramComponent`, nodes, connectors, or shapes
- Configure automatic layouts (hierarchical, radial, mind map, org chart, flowchart)
- Implement BPMN process diagrams with BPMN shapes
- Build swimlane diagrams for process modeling
- Add symbol palettes for drag-and-drop diagram building
- Bind diagram data from a collection or remote source
- Implement diagram interactions (selection, drag, resize, zoom, pan)
- Export diagrams to PNG/JPEG/SVG or print them
- Serialize and restore diagram state (save/load)
- Enable collaborative real-time editing
- Add UML sequence diagrams
- Handle diagram events, annotations, and ports

## Important: API Verification Required
 
**API Verification Required**: Always verify API class names, properties, and signatures by reading reference files (`references/*.md`) BEFORE generating code examples. Do not assume or infer class names.
⚠️ Before writing ANY code, review the **Common Mistakes** section directly below to avoid known invalid APIs and properties.


## Quick Start

```razor
@using Syncfusion.Blazor.Diagram

<SfDiagramComponent Width="100%" Height="600px" Nodes="@nodes" Connectors="@connectors" />

@code {
    DiagramObjectCollection<Node> nodes = new DiagramObjectCollection<Node>
    {
        new Node
        {
            ID = "node1", OffsetX = 150, OffsetY = 150,
            Width = 100, Height = 50,
            Style = new ShapeStyle { Fill = "#6BA5D7", StrokeColor = "white" },
            Annotations = new DiagramObjectCollection<ShapeAnnotation>
            {
                new ShapeAnnotation { Content = "Start" }
            }
        }
    };
    DiagramObjectCollection<Connector> connectors = new DiagramObjectCollection<Connector>
    {
        new Connector { ID = "conn1", SourceID = "node1", TargetID = "node2" }
    };
}
```

## Common Patterns

| Goal | Reference |
|------|-----------|
| First diagram setup | [references/getting-started.md](references/getting-started.md) |
| Add/configure nodes | [references/nodes.md](references/nodes.md) |
| Add/configure connectors | [references/connectors.md](references/connectors.md) |
| Use built-in shapes | [references/shapes.md](references/shapes.md) |
| Add text labels | [references/annotations.md](references/annotations.md) |
| Define connection points | [references/ports.md](references/ports.md) |
| Org charts / auto-layout | [references/layout.md](references/layout.md) |
| Swimlane diagrams | [references/swimlane.md](references/swimlane.md) |
| BPMN process diagrams | [references/bpmn.md](references/bpmn.md) |
| Drag-and-drop palette | [references/symbol-palette.md](references/symbol-palette.md) |
| Bind data to diagram | [references/data-binding.md](references/data-binding.md) |
| Selection, drag, zoom | [references/interaction.md](references/interaction.md) |
| Handle diagram events | [references/events.md](references/events.md) |
| Save and load diagrams | [references/serialization.md](references/serialization.md) |
| Export / print | [references/export-print.md](references/export-print.md) |
| CSS / theme styling | [references/styling.md](references/styling.md) |
| UML sequence diagrams | [references/uml-sequence.md](references/uml-sequence.md) |
| Real-time collaboration | [references/collaborative-editing.md](references/collaborative-editing.md) |
| Context menu, tooltips, rulers, localization | [references/advanced-features.md](references/advanced-features.md) |
| Miniature overview / bird's-eye navigation | [references/overview-component.md](references/overview-component.md) |

---

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- NuGet package installation (`Syncfusion.Blazor.Diagram`)
- Service registration and namespace imports
- Setup for Blazor Server, WebAssembly, MAUI
- CSS/theme configuration
- Minimal working diagram example

### Nodes
📄 **Read:** [references/nodes.md](references/nodes.md)
- Creating and configuring nodes
- Node types: basic, flow shape, path, image, HTML, native
- Node positioning, sizing, z-order
- Node style (fill, stroke, opacity)
- Expand/collapse children
- Node events and interaction

### Connectors
📄 **Read:** [references/connectors.md](references/connectors.md)
- Creating connectors between nodes or free-floating
- Segment types: straight, orthogonal, bezier
- Multiple segments per connector
- Arrows, line style, and decoration
- Connector interaction (bend, drag endpoints)
- Connector events

### Shapes
📄 **Read:** [references/shapes.md](references/shapes.md)
- Built-in basic shapes (rectangle, ellipse, triangle, etc.)
- Flow shapes (process, decision, terminator, etc.)
- Path shapes (custom SVG paths)
- Image and HTML content shapes
- Native SVG shapes
- Choosing the right shape type

### Annotations
📄 **Read:** [references/annotations.md](references/annotations.md)
- Adding text labels to nodes and connectors
- Annotation positioning and alignment
- Font, color, and style customization
- Inline editing of annotations
- Multiple annotations per element
- Annotation interaction events

### Ports
📄 **Read:** [references/ports.md](references/ports.md)
- Connection ports (fixed connection points on nodes)
- Dynamic ports (created at runtime)
- Port positioning (relative and absolute)
- Port appearance and visibility
- Restricting connections to specific ports

### Layout
📄 **Read:** [references/layout.md](references/layout.md)
- Automatic layout overview and when to use each type
- Hierarchical tree layout (top-down, left-right)
- Organizational chart layout
- Mind map layout
- Radial tree layout
- Flowchart layout
- Force-directed tree layout
- Complex hierarchical layout
- Layout spacing, margin, and orientation settings
- Layout events and callbacks
- `await DoLayoutAsync()` — refresh layout at runtime after adding/removing nodes

### Swimlane
📄 **Read:** [references/swimlane.md](references/swimlane.md)
- Creating swimlane diagrams
- Adding lanes and configuring lane properties
- Phase configuration (vertical/horizontal phases)
- Swimlane symbol palette integration
- Swimlane interactions

```razor
<SfDiagramComponent Height="600px" Swimlanes="@swimlanes" />

@code {
    DiagramObjectCollection<Swimlane> swimlanes = new();

    protected override void OnInitialized()
    {
        swimlanes.Add(new Swimlane
        {
            ID = "swimlane1",
            OffsetX = 400, OffsetY = 300,
            Width = 600, Height = 200,
            Lanes = new DiagramObjectCollection<Lane>()
            {
                new Lane(){
                Height = 100,
                Header = new SwimlaneHeader(){
                    Width = 30,
                    Annotation = new ShapeAnnotation(){ Content = "Consumer" }
                },
                Children = new DiagramObjectCollection<Node>()
                {
                    new Node(){Height = 50, Width = 50, LaneOffsetX = 250, LaneOffsetY = 30},
                }
                },
            }
        });
    }
}
```

### BPMN
📄 **Read:** [references/bpmn.md](references/bpmn.md)
- BPMN shape types (events, activities, gateways, data)
- BPMN event types (start, end, intermediate, boundary)
- BPMN activity types (task, subprocess, call activity)
- BPMN gateway types (exclusive, parallel, inclusive, etc.)
- BPMN connectors (sequence flow, message flow, association)
- Data objects and data stores
- Expanded sub-process
- BPMN text annotation

```razor
// Exclusive gateway (XOR)
nodes.Add(new Node
{
    ID = "gateway1", OffsetX = 300, OffsetY = 200, Width = 50, Height = 50,
    Shape = new BpmnGateway
    {
        GatewayType = BpmnGatewayType.Exclusive
    }
});
```

### Symbol Palette
📄 **Read:** [references/symbol-palette.md](references/symbol-palette.md)
- Setting up `SfSymbolPaletteComponent`
- Defining palette groups and symbols
- Custom symbols and stencils
- Drag-and-drop from palette to diagram
- Palette search and customization

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Binding diagram from a flat list or IEnumerable
- Hierarchical data binding (parent-child relationships)
- Remote data source integration
- Runtime CRUD: `await ReadDataAsync(query?)`, `await InsertDataAsync(data)`, `await UpdateDataAsync(keyField, data)`, `await DeleteDataAsync(keyField, value)`
- `await RefreshDataSourceAsync()` — reload all data and rebuild layout
- Mapping data fields to node/connector properties

### Interaction & Commands
📄 **Read:** [references/interaction.md](references/interaction.md)
- Selection: `Select(collection, multipleSelection?)`, `SelectAll()`, `UnSelect(obj)`, `ClearSelection()`
- Drag, resize, and rotate elements (user interaction + programmatic)
- Programmatic transforms: `Drag(obj, tx, ty)`, `Rotate(obj, angle, pivot?)`, `Scale(obj, sx, sy, pivot)`
- Zoom and pan: mouse wheel, toolbar, `Zoom(factor, focusPoint)`, `ResetZoom()`, `Pan(hOffset, vOffset, focusPoint?)`
- `BringIntoView(DiagramRect)` — scroll viewport to show a region
- `BringIntoCenter(DiagramRect)` — scroll viewport to center a region
- `FitToPage(FitOptions?)` — fit content to viewport (sync; `FitMode.Width/Height/Both`, `DiagramRegion.Content/PageSettings`)
- `Nudge(Direction, int?)` — move selected elements by pixels; default 1px; `Direction.Top/Bottom/Left/Right`
- Z-Order: `BringToFront()`, `BringForward()`, `SendBackward()`, `SendToBack()` — must `Select()` first
- Clipboard: `Copy()`, `Cut()`, `Paste(collection?)`, `Delete(collection?)`
- Group/Ungroup: `Group()`, `Ungroup()`, `AddChildAsync(group, child)`, `RemoveChild(group, child)`
- Inline text editing: `StartTextEdit(obj, annotationId?)`
- Keyboard shortcuts (built-in table) and `CommandManager` (custom/override shortcuts via child component)
- `CommandManager` uses `KeyboardCommand` + `KeyGesture` (`DiagramKeys` + `ModifierKeys`) + `CommandKeyArgs`
- Snapping to grid or objects
- Alignment, spacing, and sizing commands (`SetAlign`, `SetDistribute`, `SetSameSize` — all sync)
- User handles (custom action buttons on selection)
- Undo/redo: `Undo()`, `Redo()` (sync); `StartGroupAction()` / `EndGroupAction()` for batched undo steps
- History: `AddHistoryEntry(entry)`, `ClearHistory()`
- Utility: `GetObject(id)`, `GetPageBounds(x?, y?)`, `Clear()` (removes all elements)
- Batch updates: `BeginUpdate()` + `await EndUpdateAsync()` — group multiple changes into one render pass
- Add multiple elements: `await AddDiagramElementsAsync(DiagramObjectCollection<NodeBase>)`

### Events
📄 **Read:** [references/events.md](references/events.md)
- Diagram-level events (Created, Click, Drop)
- Node events (NodeCreating, PositionChanged, SizeChanged)
- Connector events (ConnectionChanged, SegmentChanged)
- Selection events (SelectionChanged)
- History change events (HistoryChanged for undo/redo)
- Event argument types and usage patterns

### Serialization
📄 **Read:** [references/serialization.md](references/serialization.md)
- Saving diagram state as JSON string
- Loading a diagram from saved JSON
- Custom serialization properties
- Partial diagram save and restore patterns

### Export & Print
📄 **Read:** [references/export-print.md](references/export-print.md)
- Exporting to PNG, JPEG, SVG formats
- Export region options (diagram, page, content)
- Scale and margin settings
- Print configuration
- Custom page size and orientation
- Fit diagram to single page on print

### Styling
📄 **Read:** [references/styling.md](references/styling.md)
- CSS class customization (`CssClass` property)
- Built-in themes (Material, Bootstrap, Fluent, Tailwind)
- Node and connector style properties
- Selection and hover styles
- Theme Studio customization
- CSS variable overrides

### UML Sequence Diagrams
📄 **Read:** [references/uml-sequence.md](references/uml-sequence.md)
- UML sequence diagram setup
- Lifelines and activation boxes
- Message types (synchronous, asynchronous, return, create, destroy)
- UML interaction shapes and connectors
- `await UpdateFromModelAsync()` — refresh diagram after programmatic model changes

### Collaborative Editing
📄 **Read:** [references/collaborative-editing.md](references/collaborative-editing.md)
- Setting up real-time collaborative diagram editing
- SignalR hub configuration
- Blazor Server and WASM app integration
- Handling real-time sync and conflict resolution
- Delta sync: `GetDiagramUpdates(HistoryChangedEventArgs)` + `await SetDiagramUpdatesAsync(updates)` — efficient change propagation

### Overview Component
📄 **Read:** [references/overview-component.md](references/overview-component.md)
- Adding `SfDiagramOverviewComponent` as a miniature thumbnail panel
- Linking the overview to the main diagram via `SourceID` / `ID`
- Controlling panel size with `Width` and `Height`
- Zoom and pan interactions (drag, resize, click, draw-region)
- Enabling or disabling interactions with `DiagramOverviewConstraints`
- Required `@using Syncfusion.Blazor.Diagram.Overview` namespace.

```razor
@using Syncfusion.Blazor.Diagram
@using Syncfusion.Blazor.Diagram.Overview
@using System.Collections.ObjectModel

<SfDiagramComponent ID="element"
                    Width="100%"
                    Height="500px">
</SfDiagramComponent>

<!-- Overview panel linked to the diagram above -->
<SfDiagramOverviewComponent Height="150px" SourceID="element" />
```

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Context menu (built-in and custom items)
- Tooltips for nodes, connectors, ports, user handles
- Programmatic tooltips: `await ShowTooltipAsync(obj)` / `await HideTooltipAsync(obj)` — requires `OpensOn = "Custom"`
- Gridlines and rulers
- Scroll settings and page settings
- Container and group nodes
- Flip (horizontal/vertical)
- Constraints (restricting behavior per element)
- Localization (static text translation)
- Accessibility (WCAG 2.1, keyboard navigation)
- Migration from classic to native diagram


### Common Mistakes

#### Annotation Editing

> **⚠️ `AllowEditing` does NOT exist** on `ShapeAnnotation` or `PathAnnotation`.  
> Inline editing is **on by default** — no property is needed to enable it.  
> To **disable** editing, set `Constraints = AnnotationConstraints.ReadOnly`:
> ```csharp
> // ❌ Wrong — CS0117: AllowEditing does not exist
> new ShapeAnnotation { Content = "Label", AllowEditing = false }
>
> // ✅ Correct — use AnnotationConstraints.ReadOnly to disable editing
> new ShapeAnnotation { Content = "Label", Constraints = AnnotationConstraints.ReadOnly }
> ```

#### EndUpdateAsync Method

> **⚠️ Always use `EndUpdateAsync()`** (async) — `EndUpdate()` (sync, non-async) does NOT exist and will cause a compile error.  
> Use `BeginUpdate()`/`EndUpdateAsync()` when changing multiple properties at once — `await` is required:
> ```csharp
> // ❌ Wrong — EndUpdate() does not exist
> diagram.BeginUpdate();
> // ... changes ...
> diagram.EndUpdate();
>
> // ✅ Correct — EndUpdateAsync is async
> diagram.BeginUpdate();
> // ... changes ...
> await diagram.EndUpdateAsync();
> ```

#### Click Event

> **⚠️ `ClickEventArgs` name collision:** If your page also uses `@using Syncfusion.Blazor.Navigations` (or Buttons),  
> `ClickEventArgs` becomes ambiguous. Always qualify it:
> ```csharp
> // ✅ Use the fully qualified type in the handler signature
> private void OnClick(Syncfusion.Blazor.Diagram.ClickEventArgs args) { }
> ```

> **⚠️ `args.Count` is NOT an `int` field** — it is a **method** that returns an `int`.  
> Do NOT compare it directly with `==` inline without storing the result first:
> ```csharp
> // ❌ Wrong — CS0019: Operator '==' cannot be applied to operands of type 'method group' and 'int'
> if (args.Count == 2)
>
> // ✅ Correct — store result then compare
> int clickCount = args.Count;
> if (clickCount == 2) { /* double-click */ }
> ```

#### SizeChanged Event

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

#### Selection Changed Event

> **⚠️ `SelectionChangedEventArgs` name collision:** If your page also uses `@using Syncfusion.Blazor.Buttons`  
> (or other Syncfusion packages), `SelectionChangedEventArgs` becomes ambiguous. Always qualify it:
> ```csharp
> // ✅ Fully qualified
> private void OnSelectionChanged(Syncfusion.Blazor.Diagram.SelectionChangedEventArgs args) { }
> ```

> **⚠️ `args.NewValue` is a `DiagramSelectionSettings` object — NOT a `Node`, NOT a collection:**  
> - Pattern-matching `args.NewValue is Node` always fails with `CS8121`  
> - Iterating `args.NewValue` as a collection fails — it is a single settings object  
> - The **only correct approach** is to read `_diagram.SelectionSettings.Nodes` / `.Connectors`:
> ```csharp
> // ❌ Wrong — CS8121: DiagramSelectionSettings cannot match Node
> if (args.NewValue is Node n) { }
>
> // ❌ Wrong — DiagramSelectionSettings is not IEnumerable
> foreach (var item in args.NewValue) { }
>
> // ✅ Correct — use SelectionSettings on the diagram reference
> foreach (var node in _diagram.SelectionSettings.Nodes)
>     Console.WriteLine(node.ID);
> foreach (var conn in _diagram.SelectionSettings.Connectors)
>     Console.WriteLine(conn.ID);
> ```

#### Text Changed Event

> **⚠️ `TextChangedEventArgs` does NOT exist** — using it causes `CS0246`.  
> The correct event args type is **`TextChangeEventArgs`** (no `d`):
> ```csharp
> // ❌ Wrong — CS0246: TextChangedEventArgs not found
> private void OnTextChanged(TextChangedEventArgs args) { }
>
> // ✅ Correct
> private void OnTextChanged(TextChangeEventArgs args) { }
> ```

#### Drag Start Event

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
> For tracking when a node is **being moved** (internal drag), use `PositionChanged`:
> ```csharp
> // ❌ Wrong — DragEnterEventArgs does not exist
> private void OnDragEnter(DragEnterEventArgs args) { }
>
> // ❌ Wrong — OnPositionChange does not exist on SfDiagramComponent
> <SfDiagramComponent OnPositionChange="OnPositionChange" />
>
> // ✅ Correct — use PositionChanged
> <SfDiagramComponent PositionChanged="OnPositionChanged" />
>
> private void OnPositionChanged(PositionChangedEventArgs args)
> {
>     if (args.Element is Node n)
>         Console.WriteLine($"Node {n.ID} moved to ({n.OffsetX}, {n.OffsetY})");
> }
> ```

#### Snap Distance

> **⚠️ `SnapObjectDistance` does NOT exist** on `SnapSettings` — using it causes `InvalidOperationException: does not have a property matching the name 'SnapObjectDistance'`.  
> The correct property name is **`SnapDistance`**:
> ```razor
> @* ❌ Wrong — SnapObjectDistance does not exist *@
> <SnapSettings SnapObjectDistance="5" />
>
> @* ✅ Correct *@
> <SnapSettings Constraints="SnapConstraints.SnapToObject" SnapDistance="5" />
> ```

#### Styling

> **⚠️ `CssClass` does NOT exist** on `SfDiagramComponent` — using it causes  
> `InvalidOperationException: Object of type 'SfDiagramComponent' does not have a property matching the name 'CssClass'`.  
> Wrap the component in a `<div>` with a scoping class instead:
> ```razor
> @* ❌ Wrong — CssClass does not exist on SfDiagramComponent *@
> <SfDiagramComponent CssClass="my-diagram" />
>
> @* ✅ Correct — use a wrapper div *@
> <div class="my-diagram">
>     <SfDiagramComponent ... />
> </div>
> ```

#### Phase Offset Property

> **⚠️ `Phase.Offset` does NOT exist** — using it causes a compile error.  
> Use **`Phase.Width`** to set the size of a phase in a swimlane:
> ```csharp
> // ❌ Wrong — Offset does not exist on Phase
> new Phase { ID = "ph1", Offset = 220 }
>
> // ✅ Correct — use Width
> new Phase { ID = "ph1", Width = 220 }
> ```

#### Lane Constraints Property

> **⚠️ `Lane.Constraints` does NOT exist** and **`LaneConstraints` enum does NOT exist**.  
> Individual lanes cannot have constraints set via a `Constraints` property.  
> To restrict swimlane-level interactions, use **`SwimlaneConstraints`** on the **`Swimlane`** object itself:
> ```csharp
> // ❌ Wrong — Lane.Constraints and LaneConstraints do not exist
> lane.Constraints = LaneConstraints.Default & ~LaneConstraints.ResizeEntries;
>
> // ✅ Correct — set constraints on the Swimlane object
> swimlane.Constraints = SwimlaneConstraints.Default & ~SwimlaneConstraints.Interaction;
> ```

#### FitMode.Page Value

> **⚠️ `FitMode.Page` does NOT exist** — using it causes `CS0117`.  
> The correct values for `FitMode` are **`FitMode.Width`** and **`FitMode.Height`**:
> ```csharp
> // ❌ Wrong — FitMode.Page does not exist
> new FitOptions { Mode = FitMode.Page }
>
> // ✅ Correct — use FitMode.Width or FitMode.Height
> new FitOptions { Mode = FitMode.Width, Region = DiagramRegion.Content }
> ```

#### LoadDiagram Method

> **⚠️ `SfDiagramComponent.LoadDiagram()` does NOT exist** — using it causes a compile error.  
> Use the async version **`LoadDiagramAsync()`** instead:
> ```csharp
> // ❌ Wrong — LoadDiagram() does not exist
> diagram.LoadDiagram(savedJson);
>
> // ✅ Correct — use LoadDiagramAsync
> await diagram.LoadDiagramAsync(savedJson);
> ```

#### FitToPageAsync Method

> **⚠️ `SfDiagramComponent.FitToPageAsync()` does NOT exist** — using it causes a compile error.  
> Use the non-async overload **`FitToPage()`** instead:
> ```csharp
> // ❌ Wrong — FitToPageAsync does not exist
> await diagram.FitToPageAsync(new FitOptions { Mode = FitMode.Width });
>
> // ✅ Correct — use FitToPage (synchronous)
> diagram.FitToPage(new FitOptions { Mode = FitMode.Width, Region = DiagramRegion.Content });
> ```

#### BasicShapes Enum

> **⚠️ `BasicShapes` does NOT exist** — use `NodeBasicShapes` instead:
> ```csharp
> // ❌ Wrong
> new BasicShape { Shape = BasicShapes.Rectangle }
>
> // ✅ Correct
> new BasicShape { Shape = NodeBasicShapes.Rectangle }
> ```

#### DiagramThickness Constructor

> **⚠️ `DiagramThickness` does NOT have a 4-argument constructor** — using it causes `CS1729: does not contain a constructor that takes 4 arguments`.  
> Use the **object initializer** syntax with named properties instead:
> ```csharp
> // ❌ Wrong — CS1729: no 4-argument constructor
> new DiagramThickness(20, 50, 20, 20)
>
> // ✅ Correct — use object initializer with named properties
> new DiagramThickness { Left = 20, Top = 50, Right = 20, Bottom = 20 }
>
> // ✅ Correct — set only the sides you need
> new DiagramThickness { Top = 50 }
> ```

#### ScrollSettings EnableAutoScroll Property

> **⚠️ `CanAutoScroll` does NOT exist** on `ScrollSettings` — using it causes `InvalidOperationException: does not have a property matching the name 'CanAutoScroll'`.  
> The correct property name is **`EnableAutoScroll`**:
> ```razor
> @* ❌ Wrong — CanAutoScroll does not exist *@
> <ScrollSettings CanAutoScroll="true" />
>
> @* ✅ Correct *@
> <ScrollSettings EnableAutoScroll="true" />
> ```

#### Zoom, Undo, and Redo Methods

> **⚠️ `ZoomAsync()`, `UndoAsync()`, and `RedoAsync()` do NOT exist** — using them causes a compile error.  
> Use the non-async overloads **`Zoom()`**, **`Undo()`**, and **`Redo()`** instead:
> ```csharp
> // ❌ Wrong — ZoomAsync, UndoAsync, RedoAsync do not exist
> await _diagram.ZoomAsync(1.2, new DiagramPoint { X = 300, Y = 300 });
> await _diagram.UndoAsync();
> await _diagram.RedoAsync();
>
> // ✅ Correct — use non-async overloads
> _diagram.Zoom(1.2, new DiagramPoint { X = 300, Y = 300 });
> _diagram.Undo();
> _diagram.Redo();
> ```

#### Overview Component Namespace

> **⚠️ `SfDiagramOverviewComponent` requires an additional `@using`** — it lives in `Syncfusion.Blazor.Diagram.Overview`, NOT in `Syncfusion.Blazor.Diagram`. Forgetting it causes `CS0246`:
> ```razor
> @* ❌ Wrong — SfDiagramOverviewComponent not found without the Overview namespace *@
> @using Syncfusion.Blazor.Diagram
>
> @* ✅ Correct — both namespaces required *@
> @using Syncfusion.Blazor.Diagram
> @using Syncfusion.Blazor.Diagram.Overview
> ```

> **⚠️ `SourceID` must exactly match the `ID` set on `SfDiagramComponent`** — the `ID` is NOT auto-generated; you must set it explicitly. A mismatch (including case) renders the overview empty:
> ```razor
> @* ❌ Wrong — ID not set on the diagram; SourceID has nothing to link to *@
> <SfDiagramComponent Width="100%" Height="500px" Nodes="@_nodes" />
> <SfDiagramOverviewComponent SourceID="myDiagram" Height="150px" />
>
> @* ✅ Correct — ID set on diagram, SourceID matches exactly *@
> <SfDiagramComponent ID="myDiagram" Width="100%" Height="500px" Nodes="@_nodes" />
> <SfDiagramOverviewComponent SourceID="myDiagram" Height="150px" />
> ```

> **⚠️ Do NOT nest `SfDiagramOverviewComponent` inside `SfDiagramComponent`** — the overview is a sibling component rendered outside the diagram markup.