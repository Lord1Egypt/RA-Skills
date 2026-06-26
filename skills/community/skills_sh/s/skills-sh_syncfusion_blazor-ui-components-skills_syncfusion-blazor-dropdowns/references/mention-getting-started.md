# Getting Started with Blazor Mention Component

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Setup](#project-setup)
- [Import Namespaces](#import-namespaces)
- [Basic Implementation](#basic-implementation)
- [Target Element Configuration](#target-element-configuration)
- [Initial Data Binding](#initial-data-binding)

---

## Prerequisites

Ensure you have the following installed:
- **.NET SDK**: Latest stable version (check: `dotnet --version`)
- **Visual Studio** (2022+), **Visual Studio Code**, or **.NET CLI**
- **Blazor WebAssembly** or **Blazor Server** project template

### System Requirements
- Refer to [Syncfusion Blazor System Requirements](https://blazor.syncfusion.com/documentation/system-requirements) for detailed requirements

---

## Installation

### Step 1: Install NuGet Packages

The Mention component is part of the `Syncfusion.Blazor.DropDowns` NuGet package. Install both the component package and themes:

#### Using Package Manager Console
```csharp
Install-Package Syncfusion.Blazor.DropDowns -Version 27.1.50
Install-Package Syncfusion.Blazor.Themes -Version 27.1.50
```

#### Using .NET CLI
```bash
dotnet add package Syncfusion.Blazor.DropDowns -v 27.1.50
dotnet add package Syncfusion.Blazor.Themes -v 27.1.50
dotnet restore
```

> **Note:** Replace version number with the latest available from [NuGet](https://www.nuget.org/packages?q=syncfusion.blazor). Syncfusion releases monthly updates.

---

## Project Setup

### For Blazor WebAssembly

#### Create New Project (if needed)
```bash
dotnet new blazorwasm -o MentionApp
cd MentionApp
```

#### Register Syncfusion Service

Open `Program.cs` and add Syncfusion service registration:

```csharp
using Microsoft.AspNetCore.Components.Web;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
using Syncfusion.Blazor;

var builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.RootComponents.Add<App>("#app");
builder.RootComponents.Add<HeadOutlet>("head::after");

builder.Services.AddScoped(sp => new HttpClient { BaseAddress = new Uri(builder.HostEnvironment.BaseAddress) });

// ✅ Add this line
builder.Services.AddSyncfusionBlazor();

await builder.Build().RunAsync();
```

### For Blazor Server

#### Register Syncfusion Service

Open `Program.cs` and add:

```csharp
using Syncfusion.Blazor;

var builder = WebApplicationBuilder.CreateBuilder(args);

builder.Services.AddRazorPages();
builder.Services.AddServerSideBlazor();

// ✅ Add this line
builder.Services.AddSyncfusionBlazor();

var app = builder.Build();
// ... rest of configuration
```

---

## Import Namespaces

Open `~/_Imports.razor` at the root of your project and add these namespace imports:

```csharp
@using Syncfusion.Blazor
@using Syncfusion.Blazor.DropDowns
@using Syncfusion.Blazor.Data
```

---

## Basic Implementation

### Step 1: Add Theme Stylesheet

Open `~/index.html` (Blazor WASM) or `~/Pages/_Layout.cshtml` (Blazor Server) and add the theme stylesheet and script in the `<head>` section:

```html
<head>
    <!-- ... other head content ... -->
    
    <!-- ✅ Add Syncfusion theme stylesheet -->
    <link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />
    
    <!-- ✅ Add Syncfusion JavaScript -->
    <script src="_content/Syncfusion.Blazor.Core/scripts/syncfusion-blazor.min.js" type="text/javascript"></script>
</head>
```

### Available Themes
- `bootstrap5.css` - Bootstrap 5 theme (default)
- `material3.css` - Material Design 3
- `fluent2.css` - Microsoft Fluent Design 2
- `tailwind.css` - Tailwind CSS theme

### Step 2: Create Simple Mention Component

Create or edit a Blazor component file (e.g., `Pages/Index.razor`):

```razor
<SfMention TItem="PersonData" DataSource="@TeamMembers">
    <TargetComponent>
        <div id="commentBox" 
             placeholder="Type @ and tag someone" 
             contenteditable="true"
             style="min-height: 100px; border: 1px solid #ddd; padding: 8px; border-radius: 4px;">
        </div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    public class PersonData
    {
        public string Name { get; set; }
        public string Email { get; set; }
    }

    List<PersonData> TeamMembers = new List<PersonData>
    {
        new PersonData { Name = "Alice Johnson", Email = "alice@company.com" },
        new PersonData { Name = "Bob Smith", Email = "bob@company.com" },
        new PersonData { Name = "Carol White", Email = "carol@company.com" }
    };
}
```

**Result:** Type `@` in the div, then type a letter. The component displays matching suggestions and inserts selected names.

---

## Target Element Configuration

The `TargetComponent` defines where mentions appear. Supported targets:

### 1. Contenteditable Div (Recommended for Rich Text)
```razor
<TargetComponent>
    <div id="richText" 
         contenteditable="true" 
         placeholder="Type @ to mention...">
    </div>
</TargetComponent>
```
- Allows formatting, multiple mentions
- Best for collaborative editing, comments
- Use CSS to style as text area

### 2. Textarea Element
```razor
<TargetComponent>
    <textarea id="simpleComment" 
              placeholder="Type @ to mention..."
              style="width: 100%; min-height: 100px; padding: 8px; border: 1px solid #ddd;">
    </textarea>
</TargetComponent>
```
- Simple, plain text only
- Good for basic comment systems
- Works in older browsers

### 3. Input Field
```razor
<TargetComponent>
    <input id="quickMention" 
           type="text" 
           placeholder="Mention @user..." 
           style="width: 100%; padding: 8px; border: 1px solid #ddd;" />
</TargetComponent>
```
- Single-line mentions only
- Best for simple tagging (email fields, task assignment)
- Limits to one mention per input

### Using Target Property (Alternative)

Instead of `TargetComponent`, use the `Target` property with a CSS selector:

```razor
<textarea id="mentionTarget" placeholder="Type @ to tag..."></textarea>

<SfMention TItem="PersonData" 
           DataSource="@TeamMembers"
           Target="#mentionTarget">
    <ChildContent>
        <MentionFieldSettings Text="Name"></MentionFieldSettings>
    </ChildContent>
</SfMention>
```

---

## Initial Data Binding

### Inline List (Simple)
```razor
<SfMention TItem="string" DataSource="@SimpleList">
    <TargetComponent>
        <div id="tags" contenteditable="true"></div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text=""></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    List<string> SimpleList = new() { "Apple", "Banana", "Cherry" };
}
```

### Complex Object (With Multiple Fields)
```razor
<SfMention TItem="UserData" DataSource="@Users">
    <TargetComponent>
        <div id="userMention" contenteditable="true"></div>
    </TargetComponent>
    <ChildContent>
        <MentionFieldSettings Text="FullName" Value="UserId"></MentionFieldSettings>
    </ChildContent>
</SfMention>

@code {
    public class UserData
    {
        public int UserId { get; set; }
        public string FullName { get; set; }
        public string Department { get; set; }
    }

    List<UserData> Users = new()
    {
        new() { UserId = 1, FullName = "John Doe", Department = "Engineering" },
        new() { UserId = 2, FullName = "Jane Smith", Department = "Marketing" },
        new() { UserId = 3, FullName = "Mike Johnson", Department = "Sales" }
    };
}
```

**Key Fields:**
- `Text`: Display field in suggestion list and mention text
- `Value`: Internal identifier (optional, used in events)

---

## Running Your App

### Development Server
```bash
# For Blazor WASM
dotnet watch run

# or
dotnet run
```

Then open: `https://localhost:5001` (or shown port in terminal)

### Testing the Mention
1. Type `@` (or configured trigger character) in the target element
2. See filtered suggestions appear
3. Type to narrow results
4. Click or press Enter to select
5. Selected text inserts into target element

---

## Troubleshooting

### Issue: Mention component not appearing
- **Check:** NuGet packages installed (`Syncfusion.Blazor.DropDowns`)
- **Check:** Namespaces imported in `_Imports.razor`
- **Check:** Syncfusion service registered in `Program.cs`
- **Check:** Stylesheet and script included in `index.html` or `_Layout.cshtml`

### Issue: Suggestions not showing on `@`
- **Check:** DataSource is not empty
- **Check:** MentionFieldSettings has Text property specified
- **Check:** Target element is focused
- **Check:** Browser console for JavaScript errors

### Issue: Styles not applying
- **Check:** Theme stylesheet path correct: `_content/Syncfusion.Blazor.Themes/`
- **Check:** Correct theme file (bootstrap5.css, material3.css, etc.)
- **Check:** Clear browser cache (Ctrl+Shift+Del or Cmd+Shift+Delete)

---

## Next Steps

- **Add data binding:** See [Working with Data](../working-with-data.md) for local and remote data
- **Enhance filtering:** Explore [Filtering & Search](../filtering-and-search.md)
- **Customize display:** Learn [Customization](../customization.md) and [Templates](../templates.md)
- **Ensure accessibility:** Check [Accessibility](../accessibility.md)
