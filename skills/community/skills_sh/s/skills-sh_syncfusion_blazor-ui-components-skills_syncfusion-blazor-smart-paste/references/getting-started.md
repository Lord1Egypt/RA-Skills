# Syncfusion Blazor Smart Paste Button - Setup Guide

## Overview

The Syncfusion Blazor Smart Paste Button is a component that leverages AI to intelligently populate form fields from copied text, streamlining user input workflows.

## Prerequisites

Before getting started, ensure you have the following:

- **.NET SDK 8.0** or later
- **Visual Studio 2022** (version 17.0 or later) or Visual Studio Code
- **OpenAI** or **Azure OpenAI** account (for AI capabilities)
- Knowledge of Blazor Server Interactivity mode
- Refer to **System requirements for Syncfusion Blazor components**

### Important Notes

> **NOTE:** Syncfusion Blazor Smart Components support both OpenAI and Azure OpenAI and are compatible with Blazor Server Interactivity mode.

## Create a New Blazor Web App Server

Create a Blazor Web App using Visual Studio 2022 with:
- **Microsoft Templates** - Standard project templates
- **Syncfusion Blazor Extension** - For quick setup

Configure the app with the **Server interactive render mode**.

## Install NuGet Packages

### Syncfusion Smart Components and Themes

Install the following NuGet packages:

**Using NuGet Package Manager:**
```
Tools → NuGet Package Manager → Manage NuGet Packages for Solution
```

Search for and install:
- `Syncfusion.Blazor.SmartComponents`
- `Syncfusion.Blazor.Themes`

**Using Package Manager Console:**
```powershell
Install-Package Syncfusion.Blazor.SmartComponents -Version 33.1.44
Install-Package Syncfusion.Blazor.Themes -Version 33.1.44
```

### Optional: DataForm Component

For managing form input fields, install:
```powershell
Install-Package Syncfusion.Blazor.DataForm
```

## Register Syncfusion Blazor Service

### Update _Imports.razor

Open `~/Components/_Imports.razor` and add the following namespaces:

```razor
@using Syncfusion.Blazor
@using Syncfusion.Blazor.SmartComponents
```

### Update Program.cs

Register the Syncfusion Blazor service in `~/Program.cs`:

```csharp
using Microsoft.AspNetCore.Components;
using Microsoft.AspNetCore.Components.Web;
using Syncfusion.Blazor;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddRazorPages();
builder.Services.AddServerSideBlazor();
builder.Services.AddSyncfusionBlazor();

var app = builder.Build();
// ... rest of configuration
```
