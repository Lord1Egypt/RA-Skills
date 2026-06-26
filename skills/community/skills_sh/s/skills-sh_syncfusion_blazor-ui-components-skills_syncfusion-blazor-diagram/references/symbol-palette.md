# Symbol Palette in Blazor Diagram

## Table of Contents
- [Overview](#overview)
- [Setup](#setup)
- [Adding Nodes to Palette](#adding-nodes-to-palette)
- [Adding Connectors to Palette](#adding-connectors-to-palette)
- [Multiple Palette Groups](#multiple-palette-groups)
- [Linking Palette to Diagram](#linking-palette-to-diagram)
- [Custom Symbol Styling](#custom-symbol-styling)
- [Common Gotchas](#common-gotchas)

---

## Overview

The `SfSymbolPaletteComponent` displays groups of reusable nodes and connectors that users can drag and drop into a diagram. Useful for building diagram toolboxes (flowchart shapes, BPMN elements, network icons, etc.).

---

## Setup

Add the `SfSymbolPaletteComponent` alongside the diagram. Requires the `Syncfusion.Blazor.Diagram.SymbolPalette` namespace:

```razor
@using Syncfusion.Blazor.Diagram
@using Syncfusion.Blazor.Diagram.SymbolPalette

<div style="display: flex;">
    <div style="width: 200px;">
        <SfSymbolPaletteComponent @ref="_palette"
                                  Height="600px"
                                  Width="200px"
                                  SymbolWidth="60"
                                  SymbolHeight="60"
                                  Palettes="@palettes"
                                  SymbolMargin="@symbolMargin">
        </SfSymbolPaletteComponent>
    </div>
    <div style="flex: 1;">
        <SfDiagramComponent @ref="_diagram" Height="600px" Width="100%" />
    </div>
</div>

@code {
    SfSymbolPaletteComponent _palette;
    SfDiagramComponent _diagram;
    DiagramObjectCollection<Palette> palettes = new();
    SymbolMargin symbolMargin = new SymbolMargin { Left = 15, Right = 15, Top = 15, Bottom = 15 };
}
```

---

## Adding Nodes to Palette

```razor
@code {
    protected override void OnInitialized()
    {
        var flowShapes = new DiagramObjectCollection<NodeBase>();

        flowShapes.Add(new Node
        {
            ID = "Terminator",
            Shape = new FlowShape { Type = NodeShapes.Flow, Shape = NodeFlowShapes.Terminator },
            Style = new ShapeStyle { Fill = "#6495ED", StrokeColor = "#757575" }
        });

        flowShapes.Add(new Node
        {
            ID = "Process",
            Shape = new FlowShape { Type = NodeShapes.Flow, Shape = NodeFlowShapes.Process },
            Style = new ShapeStyle { Fill = "#6495ED", StrokeColor = "#757575" }
        });

        flowShapes.Add(new Node
        {
            ID = "Decision",
            Shape = new FlowShape { Type = NodeShapes.Flow, Shape = NodeFlowShapes.Decision },
            Style = new ShapeStyle { Fill = "#FFD700", StrokeColor = "#757575" }
        });

        palettes.Add(new Palette
        {
            Symbols = flowShapes,
            Title = "Flowchart Shapes",
            IsExpanded = true
        });
    }
}
```

---

## Adding Connectors to Palette

```razor
@code {
    protected override void OnInitialized()
    {
        var connectorSymbols = new DiagramObjectCollection<NodeBase>();

        connectorSymbols.Add(new Connector
        {
            ID = "StraightLine",
            Type = ConnectorSegmentType.Straight,
            SourcePoint = new DiagramPoint { X = 0, Y = 0 },
            TargetPoint = new DiagramPoint { X = 60, Y = 60 },
            TargetDecorator = new DecoratorSettings { Shape = DecoratorShape.OpenArrow }
        });

        connectorSymbols.Add(new Connector
        {
            ID = "OrthogonalLine",
            Type = ConnectorSegmentType.Orthogonal,
            SourcePoint = new DiagramPoint { X = 0, Y = 0 },
            TargetPoint = new DiagramPoint { X = 60, Y = 60 }
        });

        palettes.Add(new Palette
        {
            Symbols = connectorSymbols,
            Title = "Connectors",
            IsExpanded = true
        });
    }
}
```

---

## Multiple Palette Groups

Organize shapes into collapsible groups:

```razor
palettes = new DiagramObjectCollection<Palette>
{
    new Palette { Symbols = flowShapes, Title = "Flow Shapes", IsExpanded = true },
    new Palette { Symbols = basicShapes, Title = "Basic Shapes", IsExpanded = false },
    new Palette { Symbols = bpmnShapes, Title = "BPMN", IsExpanded = false },
    new Palette { Symbols = connectorSymbols, Title = "Connectors", IsExpanded = true }
};
```

---

## Linking Palette to Diagram

Link the palette to the diagram in `OnAfterRenderAsync` so drag-and-drop works:

```razor
<SfSymbolPaletteComponent @ref="_palette" />
<SfDiagramComponent @ref="_diagram" />

@code {
    protected override async Task OnAfterRenderAsync(bool firstRender)
    {
        if (firstRender)
        {
            _palette.Targets = new DiagramObjectCollection<SfDiagramComponent> { _diagram };
        }
    }
}
```

> **This step is required** — without setting `Targets`, dragging from palette to diagram will not work.

---

## Custom Symbol Styling

Override how symbols look in the palette using `SymbolInfo`:

```razor
<SfSymbolPaletteComponent SymbolWidth="60" SymbolHeight="60"
                          GetSymbolInfo="GetSymbolInfo"
                          Palettes="@palettes">
</SfSymbolPaletteComponent>

@code {
    private SymbolInfo GetSymbolInfo(IDiagramObject symbol)
    {
        return new SymbolInfo
        {
            Fit = true,         // scale symbol to fit the cell
            Description = new SymbolDescription
            {
                Text = (symbol as Node)?.ID ?? "",
                Overflow = SymbolTextOverflow.Clip,
                Wrap = SymbolLabelWrap.WrapWithOverflow
            }
        };
    }
}
```

---

## Common Gotchas

- **`_palette.Targets` must be set** in `OnAfterRenderAsync` — drag-and-drop won't work without it
- **Symbols use `DiagramObjectCollection<NodeBase>`** — not `DiagramObjectCollection<Node>`. Cast nodes/connectors as `NodeBase`
- **Symbol `ID` must be unique** across all palettes
- **`SymbolWidth`/`SymbolHeight`** control the size of symbols in the palette — not the size they drop as
- **`SymbolMargin`** adds padding around each symbol in the palette grid
- **Connectors in palette need `SourcePoint`/`TargetPoint`** defined even though they'll re-route when dropped
- **Namespace:** Palette requires `@using Syncfusion.Blazor.Diagram.SymbolPalette` in addition to `Syncfusion.Blazor.Diagram`
