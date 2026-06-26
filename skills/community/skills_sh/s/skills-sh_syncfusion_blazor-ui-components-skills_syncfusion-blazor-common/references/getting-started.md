# Syncfusion Blazor Web App - Getting Started Reference

> **Applies to:** Syncfusion Blazor Components
> **Framework:** .NET 8, .NET 9, .NET 10 with Blazor Web App
> **Reference:** [Official Syncfusion Getting Started Documentation](https://blazor.syncfusion.com/documentation/getting-started/blazor-web-app)

**Purpose**: Quick reference guide for setting up and configuring Syncfusion Blazor components in a Blazor Web App project.

---

## Prerequisites

- .NET 8 or later SDK installed
- Visual Studio, Visual Studio Code, or .NET CLI

---

## Manual Project Setup Steps

### Step 1: Create Blazor Web App with Explicit .NET Version

**Using .NET CLI (Recommended):**
```bash
dotnet new blazor --name BlazorGridApp --framework net10.0 --interactivity Server
```

**CLI Parameters:**
- `--framework`: Specify target .NET version (e.g., `net8.0`, `net9.0`, `net10.0`, `net11.0`) - **REQUIRED to avoid using default SDK**
- `--interactivity`: Choose render mode (`Server`, `WebAssembly`, or `Auto`)
- `--all-interactive` (optional): Enable global interactivity instead of per-page

**Important Configuration:**
- **Always specify `--framework`** to ensure correct .NET version targeting
- Select appropriate **Interactive render mode** (Auto, Server, or WebAssembly)
- Configure **Interactivity location** (Global, Per page/component)

**Updating Existing Project to Different .NET Version:**
Edit the `.csproj` file's `<TargetFramework>` property:
```xml
<TargetFramework>net10.0</TargetFramework>
```

### Step 2: Install NuGet Packages

**NOTE**
- Install packages from [nuget.org](https://www.nuget.org/) and pick latest version. 
- **DON'T USE** Internal/local environment Nuget.config files
- **DON'T USE** Overall Syncfusion.Blazor.nupkg package and its assets.
- Use individual Nuget packages and refer assets from that package. 


Install the following NuGet packages into your project:

```
Syncfusion.Blazor.Grid
Syncfusion.Blazor.Themes
```

Or via .NET CLI:
```bash
dotnet add package Syncfusion.Blazor.Grid
dotnet add package Syncfusion.Blazor.Themes
```

**Important Notes:**
- For **WebAssembly** or **Auto** render modes: Install packages in the **client project**
- For **Server** render mode: Install in the main project
- All Syncfusion Blazor packages available at: [NuGet.org - Syncfusion.Blazor](https://www.nuget.org/packages?q=syncfusion.blazor)
- See [NuGet packages documentation](https://blazor.syncfusion.com/documentation/nuget-packages) for complete list

### Step 3: Add Import Namespaces

Edit `~/_Imports.razor` file in the client project:

```razor
@using Syncfusion.Blazor
@using Syncfusion.Blazor.Grids
```

### Step 4: Register Syncfusion® Blazor Service

Edit `Program.cs` file in your project:

```csharp
using Syncfusion.Blazor;

// ... other configuration

builder.Services.AddSyncfusionBlazor();

// ... rest of configuration
```

**Important:**
- For **WebAssembly** or **Auto** render modes: Register service in Program.cs of **both server AND client projects**
- For **Server** render mode: Register only in the main project

### Step 5: Add Stylesheet and Script Resources

Edit `App.razor` file and include theme and script resources:

```html
<link href="_content/Syncfusion.Blazor.Themes/fluent2.css" rel="stylesheet" />
<!-- Other content -->
<script src="_content/Syncfusion.Blazor.Core/scripts/syncfusion-blazor.min.js" type="text/javascript"></script>
```

**For .NET 10 or above**

```html
<link rel="stylesheet" href="@Assets["_content/Syncfusion.Blazor.Themes/fluent2.css"]" />
<!-- Other content -->
<script src="@Assets["_content/Syncfusion.Blazor.Core/scripts/syncfusion-blazor.min.js"]"></script>
```

**Alternative Theme Resource Methods:**
1. **Static Web Assets** (shown above) - Recommended
2. **CDN** - For cloud-hosted scenarios

### Step 6: Add Syncfusion® Blazor DataGrid Component

Add component to your razor page in `~/Components/Pages/*.razor`:

**Basic Grid (Minimal):**
```razor
@* If using Per page/component interactivity, add render mode here *@
@rendermode InteractiveServer

<SfGrid DataSource="@Orders" />

@code {
    public List<Order> Orders { get; set; }

    protected override void OnInitialized()
    {
        Orders = Enumerable.Range(1, 10).Select(x => new Order()
        {
            OrderID = 1000 + x,
            CustomerID = (new string[] { "ALFKI", "ANANTR", "ANTON", "BLONP", "BOLID" })[new Random().Next(5)],
            Freight = 2 * x,
            OrderDate = DateTime.Now.AddDays(-x),
        }).ToList();
    }

    public class Order
    {
        public int? OrderID { get; set; }
        public string? CustomerID { get; set; }
        public DateTime? OrderDate { get; set; }
        public double? Freight { get; set; }
    }
}
```

**Render Mode Notes:**
- Only add `@rendermode` if using **Per page/component** interactivity
- If using **Global** interactivity with Auto/WebAssembly, render mode already configured in `App.razor`
- Supported modes: `InteractiveAuto`, `InteractiveServer`, `InteractiveWebAssembly`

### Step 7: Run the Application

Press **Ctrl+F5** (Windows) or **⌘+F5** (macOS) to launch the application in your default browser.

---

## Render Mode Reference

**Interactive Render Modes Available:**
- `InteractiveAuto` - Client-side with fallback to server-side
- `InteractiveServer` - Server-side rendering only
- `InteractiveWebAssembly` - Client-side WebAssembly execution

**Interactivity Locations:**
- `Global` - All components use specified render mode (configured in App.razor)
- `Per page/component` - Specify render mode per component individually

---

## Common Configuration Scenarios

### Server-Side Rendering (Server)
```
Render mode: InteractiveServer
Interactivity: Global
Package location: Main project
Service registration: Program.cs (main project only)
```

### Client-Side WebAssembly
```
Render mode: InteractiveWebAssembly
Interactivity: Global
Package location: Client project
Service registration: Program.cs (both server and client)
```

### Hybrid (Auto)
```
Render mode: InteractiveAuto
Interactivity: Global or Per page/component
Package location: Client project
Service registration: Program.cs (both server and client)
```

---

## Available Themes

| Theme | CSS File |
|-------|----------|
| Fluent 2 *(default, recommended)* | `fluent2.css` |
| Fluent 2 Dark | `fluent2-dark.css` |
| Bootstrap 5 | `bootstrap5.css` |
| Bootstrap 5 Dark | `bootstrap5-dark.css` |
| Material 3 | `material3.css` |
| Material 3 Dark | `material3-dark.css` |
| Tailwind CSS 3 | `tailwind3.css` |
| Tailwind CSS 3 Dark | `tailwind3-dark.css` |
| High Contrast | `highcontrast.css` |

Reference the desired CSS file in `App.razor`:

```html
<link href="_content/Syncfusion.Blazor.Themes/fluent2.css" rel="stylesheet" />
```

