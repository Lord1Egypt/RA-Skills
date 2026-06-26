# Getting Started with Blazor ListBox

## Table of Contents
- [Installation](#installation)
- [Project Setup](#project-setup)
- [Basic Implementation](#basic-implementation)
- [First Example](#first-example)
- [Theme Setup](#theme-setup)
- [Next Steps](#next-steps)

## Installation

The **SfListBox** component is part of the Syncfusion DropDowns package. You need to install two NuGet packages:

### Using Visual Studio NuGet Manager

1. Open **Tools → NuGet Package Manager → Manage NuGet Packages for Solution**
2. Search for `Syncfusion.Blazor.DropDowns`
3. Click **Install** and select your project
4. Search for `Syncfusion.Blazor.Themes` and install

### Using .NET CLI

Run these commands in your terminal:

```bash
dotnet add package Syncfusion.Blazor.DropDowns
dotnet add package Syncfusion.Blazor.Themes
```

### Using Package Manager Console

```powershell
Install-Package Syncfusion.Blazor.DropDowns
Install-Package Syncfusion.Blazor.Themes
```

## Project Setup

### Step 1: Import Namespaces

Open `_Imports.razor` in your project root and add these imports:

```razor
@using Syncfusion.Blazor
@using Syncfusion.Blazor.DropDowns
```

### Step 2: Register Syncfusion Services

Edit `Program.cs` and register the Syncfusion Blazor service:

```csharp
using Syncfusion.Blazor;

// ... other code ...

var builder = WebAssemblyHostBuilder.CreateDefault(args);
// or: var builder = WebApplicationBuilder.CreateBuilder(args);

builder.Services.AddSyncfusionBlazor();

// ... rest of Program.cs ...
```

### Step 3: Add Theme Stylesheet and Script

Edit your `index.html` (for WebAssembly) or `Pages/_Host.cshtml` (for Server) and add these in the `<head>` section:

```html
<head>
    <!-- ... existing code ... -->
    
    <!-- Syncfusion Theme Stylesheet -->
    <link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />
    
    <!-- Syncfusion Blazor Script -->
    <script src="_content/Syncfusion.Blazor.Core/scripts/syncfusion-blazor.min.js" type="text/javascript"></script>
</head>
```

**Available Themes:**
- `bootstrap5.css` - Bootstrap 5 (modern, responsive)
- `material.css` - Material Design
- `fluent.css` - Microsoft Fluent UI
- `tailwind.css` - Tailwind CSS
- `fabric.css` - Office Fabric
- `material-dark.css` - Material Dark mode

## Basic Implementation

### Minimal ListBox Component

Create a new Razor component or edit an existing page (e.g., `Index.razor`):

```razor
@using Syncfusion.Blazor.DropDowns

<SfListBox TValue="string[]" DataSource="@Items" TItem="string"></SfListBox>

@code {
    public string[] Items = new string[] 
    { 
        "Apple", 
        "Banana", 
        "Orange", 
        "Mango", 
        "Grape",
        "Kiwi",
        "Pineapple"
    };
}
```

**What's Happening:**
- `SfListBox` - The main component
- `TValue="string[]"` - Type of selected values (array of strings)
- `TItem="string"` - Type of data source items
- `DataSource="@Items"` - Binds the data array to the component
- The component will display all items and allow selection

### ListBox with Object Data

When working with custom objects, use `ListBoxFieldSettings` to map properties:

```razor
@using Syncfusion.Blazor.DropDowns

<SfListBox TValue="string[]" DataSource="@Vehicles" TItem="VehicleData">
    <ListBoxFieldSettings Text="Text" Value="Id" />
</SfListBox>

@code {
    public List<VehicleData> Vehicles = new List<VehicleData>
    {
        new VehicleData { Text = "Hennessey Venom", Id = "Vehicle-01" },
        new VehicleData { Text = "Bugatti Chiron", Id = "Vehicle-02" },
        new VehicleData { Text = "McLaren F1", Id = "Vehicle-03" },
        new VehicleData { Text = "Ferrari Enzo", Id = "Vehicle-04" }
    };

    public class VehicleData
    {
        public string Text { get; set; }
        public string Id { get; set; }
    }
}
```

**Field Mapping Explanation:**
- `Text="Text"` - Displays the `Text` property in the list
- `Value="Id"` - Uses the `Id` property as the internal value
- When user selects "Hennessey Venom", the value "Vehicle-01" is selected

## First Example

Here's a complete working example with project setup:

**Program.cs:**
```csharp
using Syncfusion.Blazor;

var builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.RootComponents.Add<App>("#app");
builder.RootComponents.Add<HeadOutlet>("head::after");

builder.Services.AddScoped(sp => new HttpClient { BaseAddress = new Uri(builder.HostEnvironment.BaseAddress) });
builder.Services.AddSyncfusionBlazor();  // Register Syncfusion

await builder.Build().RunAsync();
```

**_Imports.razor:**
```razor
@using System.Net.Http
@using System.Net.Http.Json
@using Microsoft.AspNetCore.Components.Forms
@using Microsoft.AspNetCore.Components.Routing
@using Microsoft.AspNetCore.Components.Web
@using Microsoft.AspNetCore.Components.Web.Virtualization
@using Syncfusion.Blazor
@using Syncfusion.Blazor.DropDowns
```

**Pages/Index.razor:**
```razor
@page "/"

<div class="container">
    <h3>ListBox Component Example</h3>
    
    <label>Select your favorite sports:</label>
    <SfListBox TValue="string[]" DataSource="@Sports" TItem="string" Height="200px"></SfListBox>
</div>

@code {
    public string[] Sports = new string[]
    {
        "Cricket",
        "Football",
        "Tennis",
        "Basketball",
        "Baseball",
        "Golf",
        "Badminton",
        "Volleyball"
    };
}
```

**index.html:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ListBox Example</title>
    <base href="/" />
    
    <!-- Syncfusion Theme -->
    <link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />
    
    <!-- Bootstrap CSS for styling -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body>
    <div id="app"></div>

    <!-- Syncfusion Script -->
    <script src="_content/Syncfusion.Blazor.Core/scripts/syncfusion-blazor.min.js"></script>
    <script src="_framework/blazor.webassembly.js"></script>
</body>
</html>
```

**Run the Application:**
```bash
dotnet run
```

The ListBox will display your items, and you can select multiple by default.

## Theme Setup

### Bootstrap 5 (Default)

```html
<link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />
```

### Material Design

```html
<link href="_content/Syncfusion.Blazor.Themes/material.css" rel="stylesheet" />
```

### Fluent (Microsoft)

```html
<link href="_content/Syncfusion.Blazor.Themes/fluent.css" rel="stylesheet" />
```

### Tailwind CSS

```html
<link href="_content/Syncfusion.Blazor.Themes/tailwind.css" rel="stylesheet" />
```

### Dark Mode

```html
<link href="_content/Syncfusion.Blazor.Themes/bootstrap5-dark.css" rel="stylesheet" />
```

## Common Issues

### Issue: Component Not Rendering

**Cause:** Missing service registration or namespaces

**Solution:**
1. Check `Program.cs` has `builder.Services.AddSyncfusionBlazor();`
2. Check `_Imports.razor` has `@using Syncfusion.Blazor` and `@using Syncfusion.Blazor.DropDowns`
3. Check `index.html` has theme stylesheet and script references

### Issue: Styling Looks Wrong

**Cause:** Theme stylesheet not loaded

**Solution:**
1. Verify stylesheet path is correct: `_content/Syncfusion.Blazor.Themes/bootstrap5.css`
2. Check browser DevTools Network tab for 404 errors
3. Try a different theme to isolate the issue
4. Ensure script is also loaded: `_content/Syncfusion.Blazor.Core/scripts/syncfusion-blazor.min.js`

### Issue: Data Not Showing

**Cause:** Field mapping incorrect or data is null

**Solution:**
1. Verify `DataSource` property is populated with data
2. Check `Text` and `Value` in `ListBoxFieldSettings` match your object properties
3. Use the browser DevTools console to check for errors

## Next Steps

- **Ready to bind data?** Go to [Data Binding](data-binding.md) to learn different data sources
- **Need selection features?** Check [Selection & Modes](selection-and-modes.md)
- **Want advanced features?** See [Features & Interactions](features-and-interactions.md)
- **Customize appearance?** Read [Styling & Appearance](styling-and-appearance.md)
