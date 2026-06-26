# Getting Started with Syncfusion Blazor Diagram

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Setup: Blazor Server App](#setup-blazor-server-app)
- [Setup: Blazor Web App (.NET 8+)](#setup-blazor-web-app-net-8)
- [Setup: Blazor WebAssembly](#setup-blazor-webassembly)
- [Setup: MAUI Blazor](#setup-maui-blazor)
- [Add the Diagram Component](#add-the-diagram-component)
- [Minimal Working Example](#minimal-working-example)
- [Troubleshooting](#troubleshooting)

---

## Overview

The Syncfusion Blazor Diagram component (`SfDiagramComponent`) enables interactive diagramming — flowcharts, org charts, mind maps, BPMN, UML, and custom diagrams. It supports Blazor Server, Blazor WebAssembly, Blazor Web App (.NET 8+), and MAUI Blazor.

---

## Installation

Install both the diagram and themes NuGet packages:

```bash
dotnet add package Syncfusion.Blazor.Diagram
dotnet add package Syncfusion.Blazor.Themes
```

Or via Visual Studio NuGet Package Manager, search for `Syncfusion.Blazor.Diagram`.

---

## Setup: Blazor Server App

**1. Register service in `Program.cs`:**
```csharp
using Syncfusion.Blazor;

builder.Services.AddSyncfusionBlazor();
```

**2. Import namespaces in `_Imports.razor`:**
```razor
@using Syncfusion.Blazor
@using Syncfusion.Blazor.Diagram
```

**3. Add theme CSS and script in `App.razor`:**
```html
<head>
    <link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />
</head>
<body>
    ...
    <script src="_content/Syncfusion.Blazor.Core/scripts/syncfusion-blazor.min.js"></script>
</body>
```

---

## Setup: Blazor Web App (.NET 8+)

**1. Register service in both `Program.cs` files (if using WebAssembly/Auto render mode):**

```csharp
// Server Program.cs
builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents()
    .AddInteractiveWebAssemblyComponents();
builder.Services.AddSyncfusionBlazor();
```

```csharp
// Client Program.cs (for WebAssembly/Auto render mode)
builder.Services.AddSyncfusionBlazor();
```

**2. Set render mode at the top of the component page:**
```razor
@rendermode InteractiveServer
@* or InteractiveWebAssembly / InteractiveAuto *@
```

> **When to use which render mode:**
> - `InteractiveServer` — default for most apps, real-time via SignalR
> - `InteractiveWebAssembly` — fully client-side, larger download
> - `InteractiveAuto` — starts as Server, switches to WASM after download

---

## Setup: Blazor WebAssembly

```csharp
// Program.cs
using Syncfusion.Blazor;
builder.Services.AddSyncfusionBlazor();
await builder.Build().RunAsync();
```

Add theme/script references in `wwwroot/index.html`:
```html
<head>
    <link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />
</head>
<body>
    <script src="_content/Syncfusion.Blazor.Core/scripts/syncfusion-blazor.min.js"></script>
</body>
```

---

## Setup: MAUI Blazor

See [getting-started-with-maui-app.md](https://blazor.syncfusion.com/documentation/diagram/getting-started-with-maui-app) for platform-specific MAUI setup. Key difference: use `MauiProgram.cs` for service registration.

---

## Add the Diagram Component

Add `SfDiagramComponent` to a `.razor` page:

```razor
<SfDiagramComponent Width="100%" Height="600px" />
```

Minimum required props: `Width` and `Height`.

---

## Minimal Working Example

A diagram with one node and one connector:

```razor
@using Syncfusion.Blazor.Diagram

<SfDiagramComponent Width="100%" Height="600px"
                    Nodes="@nodes"
                    Connectors="@connectors" />

@code {
    DiagramObjectCollection<Node> nodes = new();
    DiagramObjectCollection<Connector> connectors = new();

    protected override void OnInitialized()
    {
        nodes.Add(new Node
        {
            ID = "node1", OffsetX = 150, OffsetY = 150,
            Width = 120, Height = 50,
            Style = new ShapeStyle { Fill = "#6BA5D7", StrokeColor = "white" },
            Annotations = new DiagramObjectCollection<ShapeAnnotation>
            {
                new ShapeAnnotation { Content = "Start" }
            }
        });

        nodes.Add(new Node
        {
            ID = "node2", OffsetX = 350, OffsetY = 150,
            Width = 120, Height = 50,
            Style = new ShapeStyle { Fill = "#6BA5D7", StrokeColor = "white" },
            Annotations = new DiagramObjectCollection<ShapeAnnotation>
            {
                new ShapeAnnotation { Content = "End" }
            }
        });

        connectors.Add(new Connector
        {
            ID = "conn1",
            SourceID = "node1",
            TargetID = "node2",
            Type = ConnectorSegmentType.Orthogonal
        });
    }
}
```

---

## Available Themes

| CSS File | Theme |
|----------|-------|
| `bootstrap5.css` | Bootstrap 5 |
| `material.css` | Material Design |
| `fluent.css` | Fluent UI |
| `tailwind.css` | Tailwind CSS |
| `fabric.css` | Office Fabric |
| `material-dark.css` | Material Dark |

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Diagram not rendering | Verify `AddSyncfusionBlazor()` is called in `Program.cs` |
| Styles not applied | Check theme CSS link is inside `<head>` |
| Script errors | Ensure `syncfusion-blazor.min.js` is at end of `<body>` |
| Component not interactive | Add `@rendermode InteractiveServer` (Blazor Web App) |
| License warning | Call `SyncfusionLicenseProvider.RegisterLicense("key")` before `builder.Build()` |
| Node ID errors | Node/Connector IDs must not start with a number or contain underscores/spaces |
