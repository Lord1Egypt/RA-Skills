# Overview Component in Blazor Diagram

## Table of Contents
- [Overview](#overview)
- [Required Namespace](#required-namespace)
- [How to Create an Overview](#how-to-create-an-overview)
- [Key Properties](#key-properties)
- [Zoom and Pan Interactions](#zoom-and-pan-interactions)
- [Constraints](#constraints)
- [Common Gotchas](#common-gotchas)

---

## Overview

The [`SfDiagramOverviewComponent`](https://help.syncfusion.com/cr/blazor/Syncfusion.Blazor.Diagram.Overview.SfDiagramOverviewComponent.html) provides a **miniature bird's-eye view** of the entire diagram content. It is especially useful for large or complex diagrams where navigating the main canvas is difficult.

Key capabilities:
- Shows a real-time thumbnail of the full diagram
- Highlights the current viewport with a red rectangular indicator
- Allows panning the main diagram by dragging the viewport rectangle
- Allows zooming by resizing the viewport rectangle
- Supports click-to-navigate and draw-to-zoom interactions

---

## Required Namespace

> **⚠️ `SfDiagramOverviewComponent` is in a separate namespace** from `SfDiagramComponent`.  
> You must add **both** `@using` directives:

```razor
@using Syncfusion.Blazor.Diagram
@using Syncfusion.Blazor.Diagram.Overview
```

> **⚠️ Forgetting `@using Syncfusion.Blazor.Diagram.Overview`** causes `CS0246: The type or namespace name 'SfDiagramOverviewComponent' could not be found`.

---

## How to Create an Overview

Link the `SfDiagramOverviewComponent` to its diagram via the **`SourceID`** property, which must match the `ID` attribute of the target `SfDiagramComponent`:

```razor
@using Syncfusion.Blazor.Diagram
@using Syncfusion.Blazor.Diagram.Overview

<!-- ✅ The diagram must have an ID set -->
<SfDiagramComponent ID="mainDiagram"
                    Width="100%"
                    Height="500px"
                    Nodes="@_nodes"
                    Connectors="@_connectors" />

<!-- ✅ SourceID must match the diagram's ID exactly -->
<SfDiagramOverviewComponent SourceID="mainDiagram"
                             Width="300px"
                             Height="150px" />
```

> **⚠️ `SfDiagramComponent.ID` is required** — if `ID` is not set on the diagram, `SourceID` cannot link to it and the overview will not display anything.

---

## Key Properties

| Property | Type | Description |
|---|---|---|
| `SourceID` | `string` | **Required.** Must match the `ID` of the linked `SfDiagramComponent` |
| `Width` | `string` | CSS width of the overview panel (e.g. `"300px"`, `"100%"`) |
| `Height` | `string` | CSS height of the overview panel (e.g. `"150px"`) |
| `Constraints` | `DiagramOverviewConstraints` | Controls which interactions are enabled (zoom, pan, draw focus, tap focus) |

---

## Zoom and Pan Interactions

The viewport rectangle (red outline) in the overview supports four interactions:

| Interaction | Effect on Main Diagram |
|---|---|
| **Drag** the rectangle | Pans the diagram to the dragged region |
| **Resize** the rectangle | Zooms the diagram in or out |
| **Click** a position | Navigates the diagram's viewport to that point |
| **Click-and-drag** a new region | Navigates and zooms to the drawn area |

---

## Constraints

Use the `Constraints` property with the `DiagramOverviewConstraints` enum to enable or disable individual interaction behaviours:

| Value | Description |
|---|---|
| `DiagramOverviewConstraints.None` | Disables all interactions |
| `DiagramOverviewConstraints.Zoom` | Enables zooming by resizing the viewport rectangle |
| `DiagramOverviewConstraints.Pan` | Enables panning by dragging the viewport rectangle |
| `DiagramOverviewConstraints.DrawFocus` | Enables zooming to a newly drawn rectangle |
| `DiagramOverviewConstraints.TapFocus` | Enables panning to a tapped point |
| `DiagramOverviewConstraints.Default` | Enables all interactions (Zoom + Pan + DrawFocus + TapFocus) |

### Disable a specific constraint (flag arithmetic)

```razor
<!-- ✅ Disable only Zoom, keep everything else enabled -->
<SfDiagramOverviewComponent
    SourceID="mainDiagram"
    Height="150px"
    Constraints="DiagramOverviewConstraints.Default &~ DiagramOverviewConstraints.Zoom" />
```

```razor
<!-- ✅ Enable only Pan -->
<SfDiagramOverviewComponent
    SourceID="mainDiagram"
    Height="150px"
    Constraints="DiagramOverviewConstraints.Pan" />
```

```razor
<!-- ✅ Disable all interactions (read-only thumbnail) -->
<SfDiagramOverviewComponent
    SourceID="mainDiagram"
    Height="150px"
    Constraints="DiagramOverviewConstraints.None" />
```

---

## Common Gotchas

- **`SfDiagramOverviewComponent` is in `Syncfusion.Blazor.Diagram.Overview`** — forgetting `@using Syncfusion.Blazor.Diagram.Overview` causes `CS0246`. Both `@using` directives are required
- **`SourceID` must exactly match the `ID` attribute on `SfDiagramComponent`** — a mismatch (case-sensitive) means the overview renders empty
- **`SfDiagramComponent.ID` must be explicitly set** — the component does not auto-generate an ID usable by `SourceID`; you must set it manually (e.g. `ID="myDiagram"`)
- **`DiagramOverviewConstraints` enum is in `Syncfusion.Blazor.Diagram.Overview` namespace** — if only `Syncfusion.Blazor.Diagram` is imported, the enum is not resolvable
- **Use flag negation (`&~`) to remove a single constraint** — assigning a single flag replaces all constraints; use `Default &~ FlagToRemove` to disable one while keeping the rest
- **Overview is a separate component rendered outside `SfDiagramComponent`** — do not nest `SfDiagramOverviewComponent` inside `SfDiagramComponent` markup
