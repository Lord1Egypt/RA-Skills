# Swimlane in Blazor Diagram

## Table of Contents
- [Overview](#overview)
- [Creating a Swimlane](#creating-a-swimlane)
- [Swimlane Header](#swimlane-header)
- [Lanes](#lanes)
- [Phases](#phases)
- [Adding Nodes Inside Lanes](#adding-nodes-inside-lanes)
- [Swimlane Orientation](#swimlane-orientation)
- [Common Gotchas](#common-gotchas)

---

## Overview

Swimlanes visualize business processes divided by department or responsibility. Each swimlane contains lanes (horizontal/vertical divisions) and phases (time/process stages).

- **Lanes:** Horizontal or vertical divisions representing roles/departments
- **Phases:** Columns or rows representing stages of the process
- **Children:** Nodes placed inside lanes

---

## Creating a Swimlane

```razor
@using Syncfusion.Blazor.Diagram

<SfDiagramComponent Height="600px" Swimlanes="@swimlanes" NodeCreating="OnNodeCreating" />

@code {
    DiagramObjectCollection<Swimlane> swimlanes = new();

    protected override void OnInitialized()
    {
        swimlanes.Add(new Swimlane
        {
            ID = "swimlane1",
            OffsetX = 400, OffsetY = 300,
            Width = 600, Height = 200
        });
    }

    private void OnNodeCreating(IDiagramObject obj)
    {
        if (obj is Swimlane sl)
        {
            sl.Header.Style = new TextStyle { Fill = "#5b9bd5", StrokeColor = "#5b9bd5" };
            foreach (var phase in sl.Phases)
                phase.Style = new ShapeStyle { Fill = "#5b9bd5", StrokeColor = "#5b9bd5" };
            foreach (var lane in sl.Lanes)
                lane.Header.Style = new TextStyle { Fill = "#5b9bd5", StrokeColor = "#5b9bd5" };
        }
    }
}
```

> By default, a swimlane is created with one lane and one phase.

> **⚠️ Swimlane ID rules:** Must not start with a number or contain underscores/spaces.

---

## Swimlane Header

```razor
new Swimlane
{
    ID = "sl1",
    OffsetX = 400, OffsetY = 300,
    Width = 600, Height = 300,
    Header = new SwimlaneHeader
    {
        Annotation = new ShapeAnnotation { Content = "Order Process" },
        Style = new TextStyle { Fill = "#5b9bd5", StrokeColor = "#5b9bd5", Color = "white", Bold = true }
    }
}
```

---

## Lanes

Configure multiple lanes inside a swimlane:

```razor
new Swimlane
{
    ID = "sl1",
    OffsetX = 400, OffsetY = 300,
    Width = 600, Height = 400,
    Lanes = new DiagramObjectCollection<Lane>
    {
        new Lane
        {
            ID = "lane1",
            Header = new SwimlaneHeader
            {
                Annotation = new ShapeAnnotation { Content = "Sales" },
                Width = 30
            },
            Height = 130,
            Style = new ShapeStyle { Fill = "#E8F4FC" }
        },
        new Lane
        {
            ID = "lane2",
            Header = new SwimlaneHeader
            {
                Annotation = new ShapeAnnotation { Content = "Support" },
                Width = 30
            },
            Height = 130,
            Style = new ShapeStyle { Fill = "#F0FFF0" }
        }
    }
}
```

---

## Phases

Add phases (column/stage divisions) to the swimlane:

```razor
new Swimlane
{
    ID = "sl1",
    Width = 700, Height = 300,
    Phases = new DiagramObjectCollection<Phase>
    {
        new Phase
        {
            ID = "phase1",
            Header = new SwimlaneHeader
            {
                Annotation = new ShapeAnnotation { Content = "Phase 1" }
            },
            Width = 200,
            Style = new ShapeStyle { Fill = "#5b9bd5", StrokeColor = "#5b9bd5" }
        },
        new Phase
        {
            ID = "phase2",
            Header = new SwimlaneHeader
            {
                Annotation = new ShapeAnnotation { Content = "Phase 2" }
            },
            Width = 200
        }
    }
}
```

---

## Adding Nodes Inside Lanes

Place nodes inside lanes using the `Lane.Children` collection. Use `LaneOffsetX` and `LaneOffsetY` (relative to the lane's own coordinate space) to position each child node — do **not** use `OffsetX`/`OffsetY` or `ParentID` for lane children:

```razor
@code {
    DiagramObjectCollection<Swimlane> _swimlaneCollections = new DiagramObjectCollection<Swimlane>();

    protected override void OnInitialized()
    {
        // This node will appear inside lane1 of swimlane sl1
        _swimlaneCollections.Add(
                new Swimlane()
                {
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

> Use `LaneOffsetX`/`LaneOffsetY` to position child nodes relative to the lane's coordinate space — **not** `OffsetX`/`OffsetY`.

---

## Swimlane Orientation

```razor
new Swimlane
{
    Orientation = Orientation.Horizontal   // default
    // Orientation = Orientation.Vertical
}
```

- **Horizontal:** Lanes stack vertically, phases run left-to-right
- **Vertical:** Lanes stack horizontally, phases run top-to-bottom

---

## Common Gotchas

- **Swimlane ID must be unique** and must not start with a number or contain underscores/spaces
- **Swimlane elements cannot be added at runtime** using `AddDiagramElementsAsync` — define all lanes/phases in `OnInitialized`
- **Lane children use `Lane.Children`** — add nodes via `Lane.Children = new DiagramObjectCollection<Node> { ... }` with `LaneOffsetX`/`LaneOffsetY` for positioning; do **not** use `ParentID` or `OffsetX`/`OffsetY` for lane-child nodes
- **`NodeCreating` callback** is the right place to style swimlane headers, lanes, and phases
- **Default behavior:** One lane and one phase are created automatically when no lanes/phases are defined
- **Phases are optional** — a swimlane can work with only lanes and no phases
