# Getting Started with ComboBox

This guide walks you through installing the Syncfusion Blazor ComboBox component and creating your first working example.

## Installation

### Step 1: Install NuGet Packages

The ComboBox component is part of the DropDowns package. Install both the component package and themes:

```bash
dotnet add package Syncfusion.Blazor.DropDowns
dotnet add package Syncfusion.Blazor.Themes
```

Or using Package Manager Console:
```powershell
Install-Package Syncfusion.Blazor.DropDowns
Install-Package Syncfusion.Blazor.Themes
```

### Step 2: Import Namespaces

Add the ComboBox namespace to your `_Imports.razor`:

```razor
@using Syncfusion.Blazor
@using Syncfusion.Blazor.DropDowns
```

### Step 3: Register Services

In `Program.cs`, register the Syncfusion services:

```csharp
builder.Services.AddSyncfusionBlazor();
```

### Step 4: Add Theme Stylesheet

Add the theme CSS link in your root layout file (`App.razor` or `_Layout.cshtml`):

```html
<!-- Choose one of these themes -->
<link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />
<!-- OR -->
<!-- <link href="_content/Syncfusion.Blazor.Themes/material.css" rel="stylesheet" /> -->
<!-- <link href="_content/Syncfusion.Blazor.Themes/fluent.css" rel="stylesheet" /> -->
<!-- <link href="_content/Syncfusion.Blazor.Themes/tailwind.css" rel="stylesheet" /> -->
```

Also add the Syncfusion script (usually at the end of the body):

```html
<script src="_content/Syncfusion.Blazor.Core/scripts/syncfusion-blazor.min.js"></script>
```

## Basic Implementation

### Example 1: Simple ComboBox with Local Data

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Country" TValue="string"
    Placeholder="Select a country"
    DataSource="@Countries">
    <ComboBoxFieldSettings Text="Name" Value="Code"></ComboBoxFieldSettings>
</SfComboBox>

@code {
    public class Country
    {
        public string Name { get; set; }
        public string Code { get; set; }
    }

    private List<Country> Countries = new()
    {
        new Country { Name = "United States", Code = "USA" },
        new Country { Name = "United Kingdom", Code = "UK" },
        new Country { Name = "Canada", Code = "CA" },
        new Country { Name = "Australia", Code = "AUS" }
    };
}
```

### Example 2: ComboBox with Value Binding

```razor
@using Syncfusion.Blazor.DropDowns

<div class="form-group">
    <label for="country">Select Country:</label>
    <SfComboBox @ref="ComboBoxRef" 
        ID="country"
        TItem="Country" 
        TValue="string"
        Placeholder="Choose a country"
        DataSource="@Countries"
        @bind-Value="@SelectedCountry">
        <ComboBoxFieldSettings Text="Name" Value="Code"></ComboBoxFieldSettings>
    </SfComboBox>
</div>

<div style="margin-top: 20px;">
    <p><strong>Selected:</strong> @SelectedCountry</p>
</div>

@code {
    private SfComboBox<Country, string> ComboBoxRef;
    private string SelectedCountry = "USA";

    public class Country
    {
        public string Name { get; set; }
        public string Code { get; set; }
    }

    private List<Country> Countries = new()
    {
        new Country { Name = "United States", Code = "USA" },
        new Country { Name = "United Kingdom", Code = "UK" },
        new Country { Name = "Canada", Code = "CA" }
    };
}
```

### Example 3: ComboBox with Primitive Types

When binding to simple string or integer lists:

```razor
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="string" TValue="string"
    Placeholder="Select a fruit"
    DataSource="@Fruits"
    @bind-Value="@SelectedFruit">
</SfComboBox>

<p>Selected: @SelectedFruit</p>

@code {
    private string SelectedFruit = "Apple";
    private List<string> Fruits = new() 
    { 
        "Apple", "Banana", "Orange", "Mango" 
    };
}
```

## Project Types

### Blazor Web App (.NET 8+)

If using the new Blazor Web App template, specify the render mode:

```razor
@rendermode InteractiveServer
@* or @rendermode InteractiveWebAssembly *@
@using Syncfusion.Blazor.DropDowns

<SfComboBox TItem="Country" TValue="string"
    Placeholder="Select a country"
    DataSource="@Countries">
    <ComboBoxFieldSettings Text="Name" Value="Code"></ComboBoxFieldSettings>
</SfComboBox>
```

### Blazor Server App

For Blazor Server, add services in `Program.cs`:

```csharp
builder.Services.AddSyncfusionBlazor();
```

### Blazor WebAssembly App

Ensure services are registered in `Program.cs`:

```csharp
var builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.Services.AddSyncfusionBlazor();
```

## Available Themes

Choose a theme that matches your application design:

- `bootstrap5.css` - Bootstrap 5 theme (default)
- `material.css` - Material Design theme
- `material-dark.css` - Material dark mode
- `fluent.css` - Microsoft Fluent UI
- `fluent-dark.css` - Fluent dark mode
- `tailwind.css` - Tailwind CSS theme
- `fabric.css` - Office Fabric theme

```html
<!-- Example: Using Material theme -->
<link href="_content/Syncfusion.Blazor.Themes/material.css" rel="stylesheet" />
```

## Troubleshooting Getting Started

**Problem: ComboBox not rendering**
- Check namespace import: `@using Syncfusion.Blazor.DropDowns`
- Verify theme CSS link is correct
- Ensure script link is loaded: `syncfusion-blazor.min.js`

**Problem: Data not showing**
- Verify `DataSource` is populated
- Check `ComboBoxFieldSettings` match your data properties
- For primitive types (string, int), omit the FieldSettings

**Problem: Styling looks off**
- Clear browser cache
- Check theme CSS matches your expectations
- Try different theme to verify it's a theme issue

## Next Steps

- **Data Binding**: Explore different data sources (remote, complex objects, observables)
- **Filtering**: Enable user filtering with `AllowFiltering`
- **Cascading**: Create dependent ComboBox chains
- **Templates**: Customize item appearance with templates
- **Validation**: Integrate with EditForm for form validation

---

*See also: [Data Binding](data-binding.md), [Filtering & Search](filtering.md), [Form Validation](events-and-validation.md)*
