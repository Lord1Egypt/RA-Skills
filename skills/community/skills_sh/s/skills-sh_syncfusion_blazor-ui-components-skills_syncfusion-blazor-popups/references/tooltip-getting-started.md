# Getting Started with Blazor Tooltip

This guide covers the complete setup process for adding Syncfusion Blazor Tooltip components to your Blazor applications, including both WebAssembly and Web App configurations.

## Prerequisites

Before starting, ensure your system meets the requirements:
- [System requirements for Blazor components](https://blazor.syncfusion.com/documentation/system-requirements)
- Visual Studio 2022, Visual Studio Code, or .NET CLI
- .NET SDK (latest version recommended)

## Installation Overview

The Tooltip component requires two NuGet packages:
1. **Syncfusion.Blazor.Popups** - Contains the Tooltip component
2. **Syncfusion.Blazor.Themes** - Provides styling themes

## WebAssembly App Setup

### Creating the Project

**Visual Studio:**
- Create a **Blazor WebAssembly App** via Microsoft Templates or Syncfusion Blazor Extension
- Follow [Blazor WASM App Getting Started](https://blazor.syncfusion.com/documentation/getting-started/blazor-webassembly-app) for detailed steps

**Visual Studio Code:**
```bash
dotnet new blazorwasm -o BlazorApp
cd BlazorApp
```

**.NET CLI:**
```bash
dotnet new blazorwasm -o BlazorApp
cd BlazorApp
```

### Installing NuGet Packages

**Visual Studio:**
- Open NuGet Package Manager: *Tools → NuGet Package Manager → Manage NuGet Packages for Solution*
- Search and install `Syncfusion.Blazor.Popups` and `Syncfusion.Blazor.Themes`

**Package Manager Console:**
```powershell
Install-Package Syncfusion.Blazor.Popups -Version {{ site.releaseversion }}
Install-Package Syncfusion.Blazor.Themes -Version {{ site.releaseversion }}
```

**Visual Studio Code / .NET CLI:**
```bash
dotnet add package Syncfusion.Blazor.Popups
dotnet add package Syncfusion.Blazor.Themes
dotnet restore
```

### Import Namespaces

Open `~/_Imports.razor` and add:

```razor
@using Syncfusion.Blazor
@using Syncfusion.Blazor.Popups
```

### Register Syncfusion Service

In `~/Program.cs`, register the Syncfusion Blazor service:

```csharp
using Microsoft.AspNetCore.Components.Web;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
using Syncfusion.Blazor;

var builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.RootComponents.Add<App>("#app");
builder.RootComponents.Add<HeadOutlet>("head::after");

builder.Services.AddScoped(sp => new HttpClient { BaseAddress = new Uri(builder.HostEnvironment.BaseAddress) });

// Register Syncfusion Blazor service
builder.Services.AddSyncfusionBlazor();

await builder.Build().RunAsync();
```

### Add Stylesheet and Script

In `~/index.html`, add theme stylesheet and script references:

```html
<head>
    ....
    <link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />
    <script src="_content/Syncfusion.Blazor.Core/scripts/syncfusion-blazor.min.js" type="text/javascript"></script>
</head>
```

**Available themes:**
- `bootstrap5.css` (recommended)
- `material.css`
- `fabric.css`
- `tailwind.css`
- `fluent.css`

## Web App Setup (Blazor Web App)

### Creating the Project

**Visual Studio:**
- Create a **Blazor Web App** using Visual Studio 2022
- Select appropriate **Interactive Render Mode** (Server, WebAssembly, or Auto)
- Choose **Interactivity Location** (Global or Per page/component)

**Visual Studio Code / .NET CLI:**
```bash
# Create Web App with Auto render mode
dotnet new blazor -o BlazorWebApp -int Auto
cd BlazorWebApp
```

### Installing NuGet Packages

**Important:** If using `WebAssembly` or `Auto` render modes, install packages in the **client project** (`.Client`).

**Visual Studio:**
- Open NuGet Package Manager
- Select the appropriate project (server or client)
- Install `Syncfusion.Blazor.Popups` and `Syncfusion.Blazor.Themes`

**.NET CLI (for Auto/WebAssembly mode):**
```bash
cd BlazorWebApp.Client
dotnet add package Syncfusion.Blazor.Popups
dotnet add package Syncfusion.Blazor.Themes
dotnet restore
```

### Import Namespaces

In the client project's `~/_Imports.razor`:

```razor
@using Syncfusion.Blazor
@using Syncfusion.Blazor.Popups
```

### Register Syncfusion Service

**For Auto or WebAssembly render modes**, register in BOTH projects:

**Server Project (`~/Program.cs`):**
```csharp
using Syncfusion.Blazor;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents()
    .AddInteractiveWebAssemblyComponents();

// Register Syncfusion Blazor service
builder.Services.AddSyncfusionBlazor();

var app = builder.Build();
// ... rest of configuration
```

**Client Project (`~/Program.cs`):**
```csharp
using Syncfusion.Blazor;

var builder = WebAssemblyHostBuilder.CreateDefault(args);

// Register Syncfusion Blazor service
builder.Services.AddSyncfusionBlazor();

await builder.Build().RunAsync();
```

### Add Stylesheet and Script

In `~/Components/App.razor`:

```html
<head>
    ....
    <link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />
</head>

<body>
    ....
    <script src="_content/Syncfusion.Blazor.Core/scripts/syncfusion-blazor.min.js" type="text/javascript"></script>
</body>
```

### Configure Render Mode

**If Interactivity Location is "Per page/component"**, add render mode directive at the top of your component:

```razor
@* For Auto render mode *@
@rendermode InteractiveAuto

@* OR for WebAssembly only *@
@rendermode InteractiveWebAssembly
```

## Basic Tooltip Implementation

### Simple Tooltip with Button

```razor
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfTooltip ID="Tooltip" Target="#btn" Content="@Content">
    <SfButton ID="btn" Content="Show Tooltip"></SfButton>
</SfTooltip>

@code
{
    string Content = "Lets go green & Save Earth !!";
}
```

**How it works:**
- `Target="#btn"` - Specifies which element triggers the tooltip
- `Content="@Content"` - Defines the tooltip text
- Tooltip appears on hover (default behavior)
- Component wraps the target element (Button)

### Multiple Tooltips Using Class Selector

```razor
@using Syncfusion.Blazor.Buttons
@using Syncfusion.Blazor.Popups

<SfTooltip ID="Tooltip" Target=".action-btn" Content="Click to perform action">
    <div id="container">
        <SfButton ID="btn1" CssClass="action-btn" Content="Save" title="Save your changes"></SfButton>
        <SfButton ID="btn2" CssClass="action-btn" Content="Cancel" title="Discard changes"></SfButton>
        <SfButton ID="btn3" CssClass="action-btn" Content="Delete" title="Remove permanently"></SfButton>
    </div>
</SfTooltip>
```

**How it works:**
- `Target=".action-btn"` - Selects all elements with the action-btn class (use class/ID selectors, NOT `[title]`)
- `Content="..."` - Provides explicit tooltip content for all matched elements
- Title attributes on elements provide semantic markup and browser fallback
- Single Tooltip component handles multiple targets with consistent styling

## Running the Application

**Visual Studio:**
- Press `Ctrl+F5` (Windows) or `⌘+F5` (macOS)

**.NET CLI:**
```bash
dotnet run
```

The application will launch in your default browser with the Tooltip component rendered.

## Important Notes

### GUID ID Limitation

⚠️ **Warning:** The Tooltip component cannot recognize target IDs that start with a digit when using GUIDs.

**❌ Won't work:**
```razor
<SfButton ID="123abc-guid" Content="Button"></SfButton>
```

**✅ Works:**
```razor
<SfButton ID="btn-123abc" Content="Button"></SfButton>
```

### Theme Options

You can reference themes via:

1. **Static Web Assets** (default):
   ```html
   <link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />
   ```

2. **CDN**:
   ```html
   <link href="https://cdn.syncfusion.com/blazor/{{ site.releaseversion }}/styles/bootstrap5.css" rel="stylesheet" />
   ```

3. **Custom Resource Generator (CRG)** - Generate custom themes with only required component styles

### Script Reference

The script is required for Tooltip functionality:
```html
<script src="_content/Syncfusion.Blazor.Core/scripts/syncfusion-blazor.min.js" type="text/javascript"></script>
```

Can also use CDN:
```html
<script src="https://cdn.syncfusion.com/blazor/{{ site.releaseversion }}/syncfusion-blazor.min.js" type="text/javascript"></script>
```

## Next Steps

Now that you have a basic Tooltip setup:

- **Customize content**: Read [content.md](content.md) to learn about HTML templates, RenderFragment, and rich content
- **Position tooltips**: Read [positioning.md](positioning.md) for positioning options and mouse trailing
- **Configure triggers**: Read [open-modes.md](open-modes.md) for click, hover, focus, and custom triggers
- **Style tooltips**: Read [customization-and-styling.md](customization-and-styling.md) for CSS customization
- **Ensure accessibility**: Read [accessibility.md](accessibility.md) for WCAG compliance

## Troubleshooting

**Tooltip doesn't appear:**
- Verify Target selector matches element ID or class
- Check that script reference is included
- Ensure Syncfusion service is registered
- Check browser console for errors

**Styling issues:**
- Verify theme stylesheet is loaded
- Check that CSS path is correct
- Clear browser cache

**NuGet package errors:**
- Run `dotnet restore`
- Check package version compatibility
- Ensure packages are installed in correct project (client vs server)
