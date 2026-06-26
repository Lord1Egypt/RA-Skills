# Getting Started with Predefined Dialogs

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Blazor WebAssembly App](#blazor-webassembly-app)
  - [Blazor Server App](#blazor-server-app)
  - [Blazor Web App](#blazor-web-app)
- [Setup Steps](#setup-steps)
- [Dialog Types](#dialog-types)
  - [Alert Dialog](#alert-dialog)
  - [Confirm Dialog](#confirm-dialog)
  - [Prompt Dialog](#prompt-dialog)
- [Complete Examples](#complete-examples)

---

## Overview

Syncfusion Blazor Predefined Dialogs provide three types of service-based dialogs that can be opened from anywhere in your Blazor application:

1. **Alert Dialog** - Display messages requiring user acknowledgment with an OK button
2. **Confirm Dialog** - Get boolean confirmation with OK and Cancel buttons
3. **Prompt Dialog** - Collect text input from users with OK and Cancel buttons

The predefined dialogs use a service-based architecture requiring two components:
- `SfDialogService` - Service registered in Program.cs for dialog invocation
- `SfDialogProvider` - Component added to layout for dialog rendering

---

## Prerequisites

**System Requirements:**
- [System requirements for Blazor components](https://blazor.syncfusion.com/documentation/system-requirements)
- .NET SDK installed (check version: `dotnet --version`)
- Visual Studio, Visual Studio Code, or .NET CLI

**Required NuGet Packages:**
- `Syncfusion.Blazor.Popups`
- `Syncfusion.Blazor.Themes`

---

## Installation

### Blazor WebAssembly App

#### Create Project

**Visual Studio:**
Create a Blazor WebAssembly App using Visual Studio via Microsoft Templates or Syncfusion Blazor Extension.

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

#### Install NuGet Packages

**Package Manager (Visual Studio):**
```powershell
Install-Package Syncfusion.Blazor.Popups -Version {{ site.releaseversion }}
Install-Package Syncfusion.Blazor.Themes -Version {{ site.releaseversion }}
```

**.NET CLI:**
```bash
dotnet add package Syncfusion.Blazor.Popups
dotnet add package Syncfusion.Blazor.Themes
dotnet restore
```

---

### Blazor Server App

#### Create Project

**Visual Studio:**
Create a Blazor Server App using the Blazor Web App template with Server interactivity.

**Visual Studio Code:**
```bash
dotnet new blazor -o BlazorApp -int Server
cd BlazorApp
```

**.NET CLI:**
```bash
dotnet new blazor -o BlazorApp -int Server
cd BlazorApp
```

#### Install NuGet Packages

Same commands as WebAssembly installation above.

---

### Blazor Web App

#### Create Project

**Visual Studio:**
Create a Blazor Web App using Visual Studio 2022 with appropriate Interactive render mode (Auto, WebAssembly, or Server) and Interactivity location (Global or Per page/component).

**Visual Studio Code / .NET CLI:**
```bash
dotnet new blazor -o BlazorWebApp -int Auto
cd BlazorWebApp
cd BlazorWebApp.Client  # For WebAssembly or Auto mode
```

#### Install NuGet Packages

**Important:** If using WebAssembly or Auto render modes, install NuGet packages in the **client project**.

Same installation commands as above.

---

## Setup Steps

### Step 1: Add Import Namespaces

Open `~/_Imports.razor` and add:

```razor
@using Syncfusion.Blazor
@using Syncfusion.Blazor.Popups
```

### Step 2: Register Syncfusion Services

Open `~/Program.cs` and register services:

**Blazor WebAssembly:**
```csharp
using Syncfusion.Blazor;
using Syncfusion.Blazor.Popups;

builder.Services.AddScoped(sp => new HttpClient { BaseAddress = new Uri(builder.HostEnvironment.BaseAddress) });
builder.Services.AddScoped<SfDialogService>();
builder.Services.AddSyncfusionBlazor();
await builder.Build().RunAsync();
```

**Blazor Server App:**
```csharp
using Syncfusion.Blazor;
using Syncfusion.Blazor.Popups;

builder.Services.AddRazorPages();
builder.Services.AddServerSideBlazor();
builder.Services.AddScoped<SfDialogService>();
builder.Services.AddSyncfusionBlazor();

var app = builder.Build();
```

**Blazor Web App (Server Project and Client Project):**

Server Project (`~/Program.cs`):
```csharp
using Syncfusion.Blazor;
using Syncfusion.Blazor.Popups;

builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents()
    .AddInteractiveWebAssemblyComponents();
builder.Services.AddScoped<SfDialogService>();
builder.Services.AddSyncfusionBlazor();

var app = builder.Build();
```

Client Project (`~/Program.cs`):
```csharp
using Syncfusion.Blazor;
using Syncfusion.Blazor.Popups;

var builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.Services.AddScoped<SfDialogService>();
builder.Services.AddSyncfusionBlazor();

await builder.Build().RunAsync();
```

### Step 3: Add Stylesheet and Script References

**WebAssembly App** - Add to `~/index.html`:
```html
<head>
    <link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />
    <script src="_content/Syncfusion.Blazor.Core/scripts/syncfusion-blazor.min.js" type="text/javascript"></script>
</head>
```

**Server App / Web App** - Add to `~/Components/App.razor`:
```html
<head>
    <link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />
</head>

<body>
    <script src="_content/Syncfusion.Blazor.Core/scripts/syncfusion-blazor.min.js" type="text/javascript"></script>
</body>
```

**Available Themes:**
- bootstrap5.css
- material.css
- fabric.css
- tailwind.css
- fluent.css
- bootstrap4.css

### Step 4: Add SfDialogProvider

Add `SfDialogProvider` in `MainLayout.razor`:

**WebAssembly App** (`~/MainLayout.razor`):
```razor
<Syncfusion.Blazor.Popups.SfDialogProvider/>
```

**Server App / Web App** (`~/Components/Layout/MainLayout.razor`):
```razor
<Syncfusion.Blazor.Popups.SfDialogProvider/>
```

**Important Notes:**
- Add `SfDialogProvider` **only once** in the application
- When added to `MainLayout.razor`, dialogs are available throughout the application
- When added to a specific page, dialogs are available only within that page

---

## Dialog Types

### Alert Dialog

An alert dialog displays messages requiring user acknowledgment with an **OK** button. When the user clicks OK, the dialog closes.

**Method:** `DialogService.AlertAsync(content, title, options)`

**Basic Example:**

```razor
@page "/alert-example"
@inject SfDialogService DialogService

<SfButton @onclick="ShowAlert">Show Alert</SfButton>

@code {
    private async Task ShowAlert()
    {
        await DialogService.AlertAsync("This is an alert message!");
    }
}
```

**With Title:**

```razor
private async Task ShowAlertWithTitle()
{
    await DialogService.AlertAsync(
        "Your changes have been saved successfully.",
        "Success"
    );
}
```

**Common Use Cases:**
- Display error messages
- Show warnings
- Confirm successful operations
- Display informational messages

---

### Confirm Dialog

A confirm dialog displays a message with **OK** and **Cancel** buttons and returns a boolean value based on user action:
- Clicking **OK** returns `true`
- Clicking **Cancel** returns `false`

**Method:** `DialogService.ConfirmAsync(content, title, options)` → Returns `Task<bool>`

**Basic Example:**

```razor
@page "/confirm-example"
@inject SfDialogService DialogService

<SfButton @onclick="ShowConfirm">Show Confirm</SfButton>
<p>Result: @result</p>

@code {
    private string result = "";
    
    private async Task ShowConfirm()
    {
        bool isConfirmed = await DialogService.ConfirmAsync(
            "Do you want to proceed?",
            "Confirmation"
        );
        
        result = isConfirmed ? "User clicked OK" : "User clicked Cancel";
    }
}
```

**Delete Confirmation Example:**

```razor
private async Task DeleteItem(int itemId)
{
    bool confirmed = await DialogService.ConfirmAsync(
        "Are you sure you want to delete this item? This action cannot be undone.",
        "Confirm Delete"
    );
    
    if (confirmed)
    {
        // Perform delete operation
        await DeleteItemFromDatabase(itemId);
    }
}
```

**Common Use Cases:**
- Confirm before delete operations
- Confirm before navigation away from unsaved changes
- Confirm before logout
- Get approval for critical actions

---

### Prompt Dialog

A prompt dialog collects text input from users with **OK** and **Cancel** buttons:
- Clicking **OK** returns the input string
- Clicking **Cancel** returns `null`

**Method:** `DialogService.PromptAsync(title, defaultValue, options)` → Returns `Task<string>`

**Basic Example:**

```razor
@page "/prompt-example"
@inject SfDialogService DialogService

<SfButton @onclick="ShowPrompt">Show Prompt</SfButton>
<p>User Input: @userInput</p>

@code {
    private string userInput = "";
    
    private async Task ShowPrompt()
    {
        string input = await DialogService.PromptAsync(
            "Enter your name:",
            ""
        );
        
        userInput = input ?? "User cancelled";
    }
}
```

**With Default Value:**

```razor
private async Task EditUsername()
{
    string currentUsername = "JohnDoe";
    
    string newUsername = await DialogService.PromptAsync(
        "Enter new username:",
        currentUsername
    );
    
    if (newUsername != null)
    {
        // Update username
        await UpdateUsername(newUsername);
    }
}
```

**Common Use Cases:**
- Collect usernames or email addresses
- Get search queries
- Prompt for simple configuration values
- Quick data entry

---

## Complete Examples

### Example 1: Complete Alert Implementation

```razor
@page "/alert-demo"
@inject SfDialogService DialogService

<div class="demo-section">
    <h3>Alert Dialog Demo</h3>
    
    <SfButton @onclick="ShowSuccessAlert">Success Alert</SfButton>
    <SfButton @onclick="ShowErrorAlert">Error Alert</SfButton>
    <SfButton @onclick="ShowWarningAlert">Warning Alert</SfButton>
</div>

@code {
    private async Task ShowSuccessAlert()
    {
        await DialogService.AlertAsync(
            "Your operation completed successfully!",
            "Success"
        );
    }
    
    private async Task ShowErrorAlert()
    {
        await DialogService.AlertAsync(
            "An error occurred while processing your request.",
            "Error"
        );
    }
    
    private async Task ShowWarningAlert()
    {
        await DialogService.AlertAsync(
            "This action may affect system performance.",
            "Warning"
        );
    }
}
```

### Example 2: Complete Confirm Implementation

```razor
@page "/confirm-demo"
@inject SfDialogService DialogService
@inject NavigationManager Navigation

<div class="demo-section">
    <h3>Confirm Dialog Demo</h3>
    
    <SfButton @onclick="ConfirmLogout">Logout</SfButton>
    <SfButton @onclick="ConfirmDelete">Delete Account</SfButton>
    
    <p>Status: @status</p>
</div>

@code {
    private string status = "";
    
    private async Task ConfirmLogout()
    {
        bool confirmed = await DialogService.ConfirmAsync(
            "Are you sure you want to logout?",
            "Confirm Logout"
        );
        
        if (confirmed)
        {
            status = "Logging out...";
            // Perform logout
        }
        else
        {
            status = "Logout cancelled";
        }
    }
    
    private async Task ConfirmDelete()
    {
        bool confirmed = await DialogService.ConfirmAsync(
            "This will permanently delete your account. Are you sure?",
            "Confirm Delete"
        );
        
        if (confirmed)
        {
            status = "Deleting account...";
            // Perform delete
        }
        else
        {
            status = "Delete cancelled";
        }
    }
}
```

### Example 3: Complete Prompt Implementation

```razor
@page "/prompt-demo"
@inject SfDialogService DialogService

<div class="demo-section">
    <h3>Prompt Dialog Demo</h3>
    
    <SfButton @onclick="PromptForName">Enter Name</SfButton>
    <SfButton @onclick="PromptForEmail">Enter Email</SfButton>
    
    <div class="results">
        <p>Name: @userName</p>
        <p>Email: @userEmail</p>
    </div>
</div>

@code {
    private string userName = "Not entered";
    private string userEmail = "Not entered";
    
    private async Task PromptForName()
    {
        string input = await DialogService.PromptAsync(
            "Please enter your name:",
            ""
        );
        
        if (input != null && !string.IsNullOrWhiteSpace(input))
        {
            userName = input;
        }
    }
    
    private async Task PromptForEmail()
    {
        string input = await DialogService.PromptAsync(
            "Please enter your email address:",
            ""
        );
        
        if (input != null && !string.IsNullOrWhiteSpace(input))
        {
            userEmail = input;
        }
    }
}
```

---

## Render Mode Configuration (Blazor Web App)

For Blazor Web Apps, configure the appropriate render mode based on your interactivity location:

**Global Interactivity:**
Render mode is configured in `App.razor` by default.

**Per Page/Component Interactivity:**
Add render mode at the top of your page/component:

```razor
@* For Auto mode *@
@rendermode InteractiveAuto

@* For WebAssembly mode *@
@rendermode InteractiveWebAssembly

@* For Server mode *@
@rendermode InteractiveServer
```

---

## Troubleshooting

### Dialog Not Showing

**Check:**
1. `SfDialogService` is registered in Program.cs
2. `SfDialogProvider` is added to MainLayout.razor
3. Syncfusion script reference is included
4. Service is injected in component: `@inject SfDialogService DialogService`

### Service Not Found Error

**Solution:**
Ensure both `AddScoped<SfDialogService>()` and `AddSyncfusionBlazor()` are registered in Program.cs.

For Blazor Web App with WebAssembly/Auto mode, register in **both** server and client projects.

### Theme Not Applied

**Solution:**
Verify the theme stylesheet link is correct and matches your installed Syncfusion.Blazor.Themes version.
