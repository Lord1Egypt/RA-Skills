---
name: syncfusion-blazor-common
description: Set up Syncfusion Blazor components — project creation, NuGet packages, service registration, script loading, bUnit testing, and localization & globalization configuration
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion Blazor Getting Started

Setup and configuration guide for Syncfusion Blazor components in Blazor Web Apps.

## When to Use

Use this skill when you need to:
- Set up a new Blazor project with Syncfusion Blazor components
- Create a Blazor Web App with specific .NET version targeting (net8.0, net9.0, net10.0, etc.)
- Add Syncfusion components (Grid, Button, etc.) with features based on context
- Optimize script loading with static assets or CDN
- Set up bUnit testing for Syncfusion components

## Quick Reference

- **Getting Started**: See [getting-started.md](references/getting-started.md) for full project setup steps
- **Scripts & CDN**: See [add-script-reference-and-cdn.md](references/add-script-reference-and-cdn.md) for script loading options
- **bUnit Testing**: See [bunit-setup.md](references/bunit-setup.md) for unit testing setup
- **Localization & Globalization**: See [localization-globalization.md](references/localization-globalization.md) for culture and localization setup

## Prerequisites

- .NET 8+ SDK
- Blazor Web App project
- Syncfusion account ([free trial](https://www.syncfusion.com/account/manage-trials/start-trials))
- NuGet package access

## 1. Getting Started

**Detailed guide**: [getting-started.md](references/getting-started.md)

### Quick Setup

1. Create Blazor Web App with your chosen render mode and explicit .NET version (e.g., `.NET 10`)
2. Install `Syncfusion.Blazor.Grid` + `Syncfusion.Blazor.Themes` NuGet packages. All individual packages are listed [here](https://blazor.syncfusion.com/documentation/nuget-packages)
3. Add `@using Syncfusion.Blazor` and relevant component namespaces to `_Imports.razor`
4. Register `builder.Services.AddSyncfusionBlazor()` in `Program.cs`
5. Add theme CSS and script references to `App.razor`
6. Use Syncfusion components in your pages

**Key Rule**: For Auto/WASM modes → register in **both** server and client projects
**Important**: Always specify the target .NET framework version when creating projects to ensure compatibility

### Quick Start Options

- **Blazor Playground**: Browser-based, no local install
- **Template Studio**: Pre-configured VS/VS Code project templates

## 2. Script References and CDN

**Detailed guide**: [add-script-reference-and-cdn.md](references/add-script-reference-and-cdn.md)

### Script Loading Options

| Method | Best For |
|--------|----------|
| **Static Web Assets** (Recommended) | Optimal performance, offline support |
| **CDN** | Cloud-hosted, quick setup |
| **Individual Scripts** | Minimal component usage |

## 3. bUnit Testing

**Detailed guide**: [bunit-setup.md](references/bunit-setup.md)

Unit test Syncfusion Blazor components with [bUnit](https://bunit.dev).

### Required Setup

Install `bunit` NuGet package, then register in each test:

```csharp
using var ctx = new TestContext();
ctx.Services.AddSyncfusionBlazor()
   .Replace(ServiceDescriptor.Transient<IComponentActivator, SfComponentActivator>());
ctx.Services.AddOptions();
```

### Test Pattern

1. `RenderComponent<TPage>()` → render
2. `FindComponent<SfButton>()` → locate
3. `.Click()` → interact
4. `MarkupMatches(...)` → assert

Works with xUnit and NUnit (use `Bunit.TestContext` for NUnit to avoid naming conflicts)

## 4. Localization and Globalization

**Detailed guide**: [localization-globalization.md](references/localization-globalization.md)

Configure multi-language support and culture-specific formatting for Syncfusion Blazor components.

### Key Concepts

- **Internationalization (i18n)**: Parsing and formatting dates, times, numbers, and currencies
- **Localization (l10n)**: Adding culture-specific customizations and translating UI text
- **Globalization**: Combines both i18n and l10n

### Quick Setup

1. Download and add culture-based `.resx` resource files from [GitHub](https://github.com/syncfusion/blazor-locale) - **ASK PERMISSION BEFORE DOWNLOAD THIS**
2. Create a `SyncfusionLocalizer` class implementing `ISyncfusionStringLocalizer`
3. Register in `Program.cs`:
   ```csharp
   builder.Services.AddSyncfusionBlazor();
   builder.Services.AddSingleton(typeof(ISyncfusionStringLocalizer), typeof(SyncfusionLocalizer));
   ```
4. Set culture statically or dynamically (server, WebAssembly, or MAUI apps)
5. Create a `CultureSwitcher` component for dynamic culture selection

