# Getting Started — App Type Variants

## Blazor Server App

### `Program.cs`

```csharp
using Syncfusion.Blazor;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddRazorComponents().AddInteractiveServerComponents();
builder.Services.AddSyncfusionBlazor();

var app = builder.Build();
app.MapRazorComponents<App>().AddInteractiveServerRenderMode();
app.Run();
```

### `App.razor` — Add stylesheets in `<head>`

```html
<head>
    ...
    <link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />
</head>
<body>
    ...
    <script src="_content/Syncfusion.Blazor.Core/scripts/syncfusion-blazor.min.js"></script>
</body>
```

### Page Component

No special render mode directive needed when interactivity is set globally. If per-page interactivity:

```razor
@rendermode InteractiveServer
```

---

## Blazor Web App (.NET 8+)

Supports multiple render modes. Setup requires **both** server and client projects.

### Server `Program.cs`

```csharp
using Syncfusion.Blazor;

builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents()
    .AddInteractiveWebAssemblyComponents();
builder.Services.AddSyncfusionBlazor();

app.MapRazorComponents<App>()
    .AddInteractiveServerRenderMode()
    .AddInteractiveWebAssemblyRenderMode()
    .AddAdditionalAssemblies(typeof(Client._Imports).Assembly);
```

### Client `Program.cs`

```csharp
using Syncfusion.Blazor;

var builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.Services.AddSyncfusionBlazor();
await builder.Build().RunAsync();
```

### App.razor (Server Project)

```html
<head>
    <link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />
</head>
<body>
    <Routes />
    <script src="_content/Syncfusion.Blazor.Core/scripts/syncfusion-blazor.min.js"></script>
</body>
```

### Render Mode on Page

```razor
@rendermode InteractiveAuto          @* Server first, then WASM *@
@rendermode InteractiveWebAssembly   @* Pure WASM *@
@rendermode InteractiveServer        @* Server-side *@
```

---

## Blazor MAUI App

### `MauiProgram.cs`

```csharp
using Syncfusion.Blazor;

public static class MauiProgram
{
    public static MauiApp CreateMauiApp()
    {
        var builder = MauiApp.CreateBuilder();
        builder
            .UseMauiApp<App>()
            .ConfigureFonts(fonts => { ... });

        builder.Services.AddMauiBlazorWebView();
        builder.Services.AddSyncfusionBlazor();
        return builder.Build();
    }
}
```

### `wwwroot/index.html`

```html
<head>
    <link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />
</head>
<body>
    <app>...</app>
    <script src="_content/Syncfusion.Blazor.Core/scripts/syncfusion-blazor.min.js"></script>
</body>
```

---

## License Key Registration

For production apps, register license in `Program.cs` before `builder.Build()`:

```csharp
Syncfusion.Licensing.SyncfusionLicenseProvider.RegisterLicense("YOUR-LICENSE-KEY");
```

Obtain a free community key or trial from https://www.syncfusion.com/sales/products.

---

## `_Imports.razor` (All Project Types)

```razor
@using Syncfusion.Blazor
@using Syncfusion.Blazor.Grids
```
