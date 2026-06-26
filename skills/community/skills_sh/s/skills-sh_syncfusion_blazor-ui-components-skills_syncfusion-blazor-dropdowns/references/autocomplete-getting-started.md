# Getting Started with Syncfusion Blazor AutoComplete

## Table of Contents
- [Installation](#installation)
- [Project Setup](#project-setup)
- [Basic Implementation](#basic-implementation)
- [CSS & Themes](#css--themes)
- [Initial Configuration](#initial-configuration)

## Installation

The Syncfusion Blazor AutoComplete component is part of the **DropDowns** package. Install it along with the Themes package for styling.

### Step 1: Install NuGet Packages

**Using Visual Studio NuGet Package Manager:**
```
Install-Package Syncfusion.Blazor.DropDowns
Install-Package Syncfusion.Blazor.Themes
```

**Using .NET CLI:**
```bash
dotnet add package Syncfusion.Blazor.DropDowns
dotnet add package Syncfusion.Blazor.Themes
dotnet restore
```

### Step 2: Register Syncfusion Services

Register the Syncfusion Blazor service in your `Program.cs`:

```csharp
using Syncfusion.Blazor;

var builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.RootComponents.Add<App>("#app");

builder.Services
    .AddScoped(sp => new HttpClient { BaseAddress = new Uri(builder.HostEnvironment.BaseAddress) })
    .AddSyncfusionBlazor();  // Register Syncfusion services

await builder.Build().RunAsync();
```

## Project Setup

### Setup for Visual Studio

1. Create a new **Blazor WebAssembly App** in Visual Studio
2. Go to **Tools → NuGet Package Manager → Manage NuGet Packages for Solution**
3. Search for and install:
   - `Syncfusion.Blazor.DropDowns`
   - `Syncfusion.Blazor.Themes`
4. Register services in `Program.cs` (see above)

### Setup for Visual Studio Code

1. Create a new Blazor WebAssembly project:
   ```bash
   dotnet new blazorwasm -o BlazorApp
   cd BlazorApp
   ```

2. Install packages:
   ```bash
   dotnet add package Syncfusion.Blazor.DropDowns
   dotnet add package Syncfusion.Blazor.Themes
   dotnet restore
   ```

3. Register services in `Program.cs`

### Setup for .NET CLI

Create and configure a Blazor WebAssembly app:
```bash
dotnet new blazorwasm -o MyBlazorApp
cd MyBlazorApp
dotnet add package Syncfusion.Blazor.DropDowns
dotnet add package Syncfusion.Blazor.Themes
dotnet restore
```

## CSS & Themes

### Add Theme CSS

Include the Syncfusion theme CSS in your `index.html` (in the `<head>` section):

```html
<link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />
```

**Available Themes:**
- `bootstrap5.css` - Bootstrap 5
- `tailwind.css` - Tailwind CSS
- `fluent2.css` - Microsoft Fluent 2
- `material3.css` - Material Design 3
- `fluent.css` - Microsoft Fluent
- `highcontrast.css` - High Contrast

Choose the theme that matches your application design.

### Add Syncfusion Script

Add the Syncfusion Blazor scripts to the end of `index.html` (before `</body>`):

```html
<script src="_content/Syncfusion.Blazor.Core/scripts/syncfusion-blazor.min.js"></script>
```

## Basic Implementation

### Minimal Example with Local Data

Create a simple AutoComplete component with a list of strings:

```blazor
@page "/autocomplete-demo"
@using Syncfusion.Blazor.DropDowns

<h3>AutoComplete Demo</h3>

<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@CountryData" 
                Placeholder="Select a country">
</SfAutoComplete>

@code {
    private List<string> CountryData = new()
    {
        "Austria",
        "Brazil",
        "Canada",
        "Denmark",
        "Egypt",
        "Finland",
        "Germany",
        "Hungary"
    };
}
```

### Example with Objects

For more complex scenarios, bind to objects and map fields:

```blazor
@page "/autocomplete-objects"
@using Syncfusion.Blazor.DropDowns

<h3>AutoComplete with Objects</h3>

<SfAutoComplete TValue="string" TItem="Country" 
                DataSource="@Countries"
                Placeholder="Select a country">
    <AutoCompleteFieldSettings Value="CountryName"></AutoCompleteFieldSettings>
</SfAutoComplete>

@code {
    public class Country
    {
        public string CountryName { get; set; }
        public string CountryCode { get; set; }
    }

    private List<Country> Countries = new()
    {
        new Country { CountryName = "Austria", CountryCode = "AT" },
        new Country { CountryName = "Brazil", CountryCode = "BR" },
        new Country { CountryName = "Canada", CountryCode = "CA" }
    };
}
```

## Initial Configuration

### Common Initial Properties

**Enable Filtering:**
```blazor
<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Items"
                AllowFiltering="true">
</SfAutoComplete>
```

**Add Placeholder & Clear Button:**
```blazor
<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Items"
                Placeholder="Type to search..."
                ShowClearButton="true">
</SfAutoComplete>
```

**Set Read-Only State:**
```blazor
<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Items"
                ReadOnly="true">
</SfAutoComplete>
```

**Disable Component:**
```blazor
<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Items"
                Enabled="false">
</SfAutoComplete>
```

### Handling Value Changes

Respond to user selections:

```blazor
<SfAutoComplete TValue="string" TItem="string" 
                DataSource="@Items"
                @bind-Value="SelectedValue">
    <AutoCompleteEvents TValue="string" TItem="string"
                        ValueChange="@OnValueChange">
    </AutoCompleteEvents>
</SfAutoComplete>

<p>Selected: @SelectedValue</p>

@code {
    private string SelectedValue;
    private List<string> Items = new() { "Option1", "Option2", "Option3" };

    private void OnValueChange(ChangeEventArgs<string, string> args)
    {
        Console.WriteLine($"Selected value: {args.Value}");
    }
}
```

## Next Steps

- **Data Binding:** See [data-binding.md](data-binding.md) for binding local and remote data
- **Filtering:** See [filtering-and-search.md](filtering-and-search.md) for search and filter options
- **Customization:** See [templates-and-styling.md](templates-and-styling.md) for styling and templates
- **Advanced:** See [advanced-features.md](advanced-features.md) for events, virtualization, and more
