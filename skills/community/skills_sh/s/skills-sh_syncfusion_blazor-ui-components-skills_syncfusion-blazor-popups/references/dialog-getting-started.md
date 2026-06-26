# Getting Started with Blazor Dialog

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Setup](#project-setup)
- [Basic Implementation](#basic-implementation)
- [Setting Header and Content](#setting-header-and-content)
- [Controlling Visibility](#controlling-visibility)
- [First Dialog Example](#first-dialog-example)

## Prerequisites

Ensure you have:
- .NET 6.0 or later SDK installed
- Visual Studio, Visual Studio Code, or .NET CLI
- A Blazor WebAssembly or Blazor Server project created

## Installation

### Step 1: Install NuGet Packages

Install the Syncfusion Blazor Popups and Themes packages via NuGet Package Manager or Package Manager Console:

```powershell
Install-Package Syncfusion.Blazor.Popups -Version 28.1.33
Install-Package Syncfusion.Blazor.Themes -Version 28.1.33
```

Or using .NET CLI:

```bash
dotnet add package Syncfusion.Blazor.Popups --version 28.1.33
dotnet add package Syncfusion.Blazor.Themes --version 28.1.33
dotnet restore
```

> **Note:** Replace version number with your current Syncfusion release version. Check [NuGet packages](https://www.nuget.org/packages?q=syncfusion.blazor) for available versions.

## Project Setup

### Step 2: Add Namespaces

Open the **_Imports.razor** file in your project root and add the following namespaces:

```csharp
@using Syncfusion.Blazor
@using Syncfusion.Blazor.Popups
```

### Step 3: Register Syncfusion Service

Update your **Program.cs** file to register the Syncfusion Blazor service:

```csharp
using Syncfusion.Blazor;

var builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.RootComponents.Add<App>("#app");

// Add Syncfusion Blazor service
builder.Services.AddSyncfusionBlazor();

await builder.Build().RunAsync();
```

### Step 4: Add Theme Stylesheet and Script

In your **index.html** file (located in `wwwroot/`), add the theme stylesheet and Syncfusion script in the `<head>` section:

```html
<head>
    <meta charset="utf-8" />
    <title>Blazor Dialog</title>
    <base href="/" />
    <link rel="stylesheet" href="css/bootstrap/bootstrap.min.css" />
    
    <!-- Syncfusion Blazor Theme -->
    <link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />
    
    <link href="css/app.css" rel="stylesheet" />
</head>
<body>
    <div id="app"></div>

    <!-- Syncfusion Blazor Script -->
    <script src="_content/Syncfusion.Blazor.Core/scripts/syncfusion-blazor.min.js"></script>
    <script src="_framework/blazor.web.js"></script>
</body>
```

> **Available Themes:** bootstrap5, material3, tailwind, fluent2, highcontrast

## Basic Implementation

### Minimal Dialog

The simplest dialog requires only the `SfDialog` component:

```csharp
@using Syncfusion.Blazor.Popups

<SfDialog Width="250px">
    <DialogTemplates>
        <Content>This is a basic dialog with content</Content>
    </DialogTemplates>
</SfDialog>
```

This renders a dialog with default styles and behavior.

## Setting Header and Content

### Using Header Property

```csharp
<SfDialog Width="300px" Header="Welcome Dialog">
    <DialogTemplates>
        <Content>
            <p>Welcome to the Syncfusion Blazor Dialog component!</p>
        </Content>
    </DialogTemplates>
</SfDialog>
```

### Using Content Property

```csharp
<SfDialog Width="300px" 
          Header="Notification"
          Content="Your action was completed successfully!">
</SfDialog>
```

### Using DialogTemplates for Complex Content

```csharp
<SfDialog Width="400px">
    <DialogTemplates>
        <Header>
            <span>User Profile</span>
        </Header>
        <Content>
            <div class="user-info">
                <p><strong>Name:</strong> John Doe</p>
                <p><strong>Email:</strong> john@example.com</p>
            </div>
        </Content>
    </DialogTemplates>
</SfDialog>
```

## Controlling Visibility

### Using Visible Property

```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfButton OnClick="@ShowDialog">Open Dialog</SfButton>

<SfDialog Width="300px" 
          Header="Dialog Title" 
          @bind-Visible="IsDialogVisible">
    <DialogTemplates>
        <Content>Dialog content goes here</Content>
    </DialogTemplates>
</SfDialog>

@code {
    private bool IsDialogVisible { get; set; } = false;

    private void ShowDialog()
    {
        IsDialogVisible = true;
    }
}
```

### Using Events to Close Dialog

```csharp
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfButton OnClick="@ShowDialog">Open</SfButton>

<SfDialog @bind-Visible="IsDialogVisible" 
          Width="300px" 
          Header="Confirmation">
    <DialogTemplates>
        <Content>Do you want to continue?</Content>
    </DialogTemplates>
    <DialogButtons>
        <DialogButton Content="Yes" 
                      OnClick="@OnYesClick"
                      IsPrimary="true" />
        <DialogButton Content="No" 
                      OnClick="@OnNoClick" />
    </DialogButtons>
</SfDialog>

@code {
    private bool IsDialogVisible { get; set; } = false;

    private void ShowDialog() => IsDialogVisible = true;

    private void OnYesClick()
    {
        // Handle yes action
        IsDialogVisible = false;
    }

    private void OnNoClick() => IsDialogVisible = false;
}
```

## First Dialog Example

Here's a complete working example of a dialog with header, content, and buttons:

```csharp
@page "/dialog-example"
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<div class="control-section">
    <div>
        <SfButton OnClick="@OpenDialog">Open Dialog</SfButton>
    </div>

    <SfDialog Width="400px"
              Header="Welcome to Dialog"
              ShowCloseIcon="true"
              @bind-Visible="DialogVisible">
        <DialogTemplates>
            <Content>
                <p>This is your first Blazor Dialog component!</p>
                <p>You can customize the header, content, and buttons.</p>
            </Content>
        </DialogTemplates>
        <DialogButtons>
            <DialogButton Content="OK" 
                          IsPrimary="true"
                          OnClick="@CloseDialog" />
            <DialogButton Content="Cancel" 
                          OnClick="@CloseDialog" />
        </DialogButtons>
    </SfDialog>
</div>

@code {
    private bool DialogVisible { get; set; } = false;

    private void OpenDialog()
    {
        DialogVisible = true;
    }

    private void CloseDialog()
    {
        DialogVisible = false;
    }
}
```

**Output:** A dialog window appears with "Welcome to Dialog" header, descriptive content, and two buttons (OK and Cancel).

## Next Steps

- Customize templates with custom HTML and components (see **references/templates.md**)
- Handle dialog events like open and close (see **references/events.md**)
- Configure dialog behavior like dragging and resizing (see **references/dialog-behavior.md**)
- Apply custom styling and animations (see **references/advanced-customization.md**)
