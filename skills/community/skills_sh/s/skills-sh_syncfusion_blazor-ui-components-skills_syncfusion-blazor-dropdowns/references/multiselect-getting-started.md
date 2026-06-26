# Getting Started with MultiSelect Dropdown

## Table of Contents
- [Installation](#installation)
- [Service Registration](#service-registration)
- [Basic Implementation](#basic-implementation)
- [Theme Application](#theme-application)
- [Minimal Working Example](#minimal-working-example)
- [Troubleshooting](#troubleshooting)

## Installation

### Step 1: Install NuGet Package

The MultiSelect Dropdown component is part of the `Syncfusion.Blazor.DropDowns` package. Install it via .NET CLI:

```bash
dotnet add package Syncfusion.Blazor.DropDowns
```

Or via Package Manager:

```powershell
Install-Package Syncfusion.Blazor.DropDowns
```

For a specific version:
```bash
dotnet add package Syncfusion.Blazor.DropDowns --version 25.1.35
```

### Step 2: Import Namespace

Add the required namespaces to your `_Imports.razor` file:

```csharp
@using Syncfusion.Blazor
@using Syncfusion.Blazor.DropDowns
```

This makes all dropdown components available globally in your Blazor application.

## Service Registration

Add Syncfusion Blazor services in your `Program.cs` before building the app:

```csharp
// For Blazor Server
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddRazorComponents();
builder.Services.AddSyncfusionBlazor();  // Add this line
var app = builder.Build();
```

```csharp
// For Blazor WebAssembly
var builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.Services.AddSyncfusionBlazor();  // Add this line
await builder.Build().RunAsync();
```

**Why this is needed:** Syncfusion services register required dependencies and configuration for all components.

## Basic Implementation

### Minimal Component Usage

```csharp
<SfMultiSelect TValue="string[]" 
               TItem="ItemData"
               DataSource="@Items">
    <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
</SfMultiSelect>

@code {
    private List<ItemData> Items { get; set; } = new();

    protected override void OnInitialized()
    {
        Items = new List<ItemData>
        {
            new() { ID = "1", Name = "Option 1" },
            new() { ID = "2", Name = "Option 2" },
            new() { ID = "3", Name = "Option 3" }
        };
    }

    public class ItemData
    {
        public string ID { get; set; }
        public string Name { get; set; }
    }
}
```

**What's happening:**
- `SfMultiSelect` - The main component with generic type parameters
- `TValue="string[]"` - Type of selected values (array of strings)
- `TItem="ItemData"` - Type of each item in the data source
- `DataSource` - Collection of items to display
- `MultiSelectFieldSettings` - Maps data properties to dropdown fields

### Understanding Generic Parameters

**`TItem`** - The type of objects in your data source
```csharp
public class Employee { public string Name { get; set; } }
// Then: TItem="Employee"
```

**`TValue`** - The type of selected values (array or collection)
```csharp
// String array: TValue="string[]"
// List of strings: TValue="List<string>"
// Complex type array: TValue="Employee[]"
// Note: MultiSelect always returns a collection of values
```

## Theme Application

### Add Theme CSS

Add the theme stylesheet to your main layout file (`App.razor` or `Layout.razor`):

```html
<!-- In the <head> section -->
<link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />
<script src="_content/Syncfusion.Blazor.Core/scripts/syncfusion-blazor.min.js"></script>
```

### Available Themes

| Theme | CSS File | Best For |
|-------|----------|----------|
| Bootstrap 5 | `bootstrap5.css` | Bootstrap-based projects |
| Material | `material.css` | Material Design consistency |
| Fluent | `fluent.css` | Microsoft Office look |
| Tailwind | `tailwind.css` | Tailwind CSS projects |
| Fabric | `fabric.css` | Office Fabric style |

### Dark Mode

For dark mode support, add the dark theme CSS:

```html
<link href="_content/Syncfusion.Blazor.Themes/bootstrap5-dark.css" rel="stylesheet" />
```

**Choose the appropriate dark variant:** `{theme-name}-dark.css`

### Project Type Considerations

**Blazor Server** - Add theme in `App.razor` `<head>`  
**Blazor WebAssembly** - Add theme in `wwwroot/index.html` `<head>`  
**Blazor Web App** - Add theme in `App.razor` or layout component

## Minimal Working Example

Complete, copy-paste-ready example:

```razor
@page "/multiselect-demo"
@using Syncfusion.Blazor.DropDowns

<div style="margin: 20px;">
    <h3>MultiSelect Dropdown Demo</h3>
    
    <SfMultiSelect TValue="string[]"
                   TItem="Fruit"
                   DataSource="@FruitList"
                   Placeholder="Select fruits"
                   AllowFiltering="true">
        <MultiSelectFieldSettings Text="Name" Value="ID"></MultiSelectFieldSettings>
    </SfMultiSelect>
    
    <div style="margin-top: 20px;">
        <p><strong>Selected:</strong> @string.Join(", ", SelectedFruits ?? Array.Empty<string>())</p>
    </div>
</div>

@code {
    private List<Fruit> FruitList { get; set; } = new();
    private string[] SelectedFruits { get; set; } = Array.Empty<string>();

    protected override void OnInitialized()
    {
        FruitList = new List<Fruit>
        {
            new Fruit { ID = "1", Name = "Apple" },
            new Fruit { ID = "2", Name = "Banana" },
            new Fruit { ID = "3", Name = "Cherry" },
            new Fruit { ID = "4", Name = "Date" },
            new Fruit { ID = "5", Name = "Elderberry" }
        };
    }

    public class Fruit
    {
        public string ID { get; set; }
        public string Name { get; set; }
    }
}
```

**To add two-way binding:**

```csharp
// Add to SfMultiSelect:
@bind-Value="SelectedFruits"

// The SelectedFruits list updates automatically when user selects items
```

## Troubleshooting

### Issue: Component not rendering

**Cause:** Service not registered or namespace not imported

**Solution:**
1. Verify `builder.Services.AddSyncfusionBlazor()` in `Program.cs`
2. Confirm `@using Syncfusion.Blazor.DropDowns` in `_Imports.razor`
3. Rebuild solution

### Issue: Styling looks wrong or broken

**Cause:** Theme CSS not loaded

**Solution:**
1. Check theme CSS link in `App.razor` or layout
2. Verify file path: `_content/Syncfusion.Blazor.Themes/{theme}.css`
3. Clear browser cache and rebuild
4. Check browser console for 404 errors

### Issue: JavaScript not working (interaction fails)

**Cause:** JS interop script not loaded

**Solution:**
1. Ensure `syncfusion-blazor.min.js` is referenced
2. Verify script is in `<body>` or at end of layout
3. Check network tab in browser dev tools
4. Verify CDN/file path is correct

### Issue: GenericType errors in compilation

**Cause:** Incorrect `TValue` or `TItem` generic types

**Solution:**
1. `TValue` must be an array or collection type (e.g., `string[]`, `List<string>`)
2. `TItem` must match your data source object type
3. Ensure field mappings exist: `Text` and `Value` properties in `MultiSelectFieldSettings`
4. Example: `TValue="string[]"` and `TItem="Employee"` where `Employee` has `ID` and `Name` properties

### Issue: DataSource is null or empty

**Cause:** Data not initialized before rendering

**Solution:**
```csharp
protected override async Task OnInitializedAsync()  // Use async if fetching data
{
    // Initialize your list here
    Items = await FetchDataFromApi();  // or create static list
}
```

### Issue: Selected values not binding

**Cause:** Wrong binding syntax or type mismatch

**Solution:**
1. Use `@bind-Value="YourListProperty"`
2. Ensure property is `List<string>` or matching `TValue`
3. Initialize property in `@code`: `private List<string> Selected = new();`

## Next Steps

- **Configure data** → See [Data Binding](data-binding.md)
- **Add features** → See [Features and Selection](features-and-selection.md)
- **Enable filtering** → See [Filtering and Grouping](filtering-and-grouping.md)
- **Customize look** → See [Customization and Styling](customization-and-styling.md)
