# Blazor Localization and Globalization Guide

## Overview

**Globalization** combines internationalization (i18n) and localization (l10n):
- **Internationalization**: Parsing and formatting dates, times, numbers, and currencies
- **Localization**: Adding culture-specific customizations and translating UI text

The Syncfusion® Blazor UI components use American English (`en-US`) by default. Blazor relies on .NET globalization to parse and format numbers and dates based on the active culture.

---

## Localization of Syncfusion® Blazor Components

### Step 1: Adding Culture-Based .resx Files

Syncfusion® components can be localized using Resource `.resx` files. 

**To add resource files:**

1. Download default and culture-based resource files from the [GitHub repository](https://github.com/syncfusion/blazor-locale)
2. Copy the default `.resx` file (`SfResources.resx`) and culture-specific `.resx` files to the **Resources** folder
   - For .NET MAUI Blazor apps, create a **LocalizationResources** folder instead
3. Open the default resource file (`SfResources.resx`) in the Resource Editor
4. Set **Access Modifier** to **Public**

> **Note**: Update the localization files whenever upgrading Syncfusion® NuGet packages to prevent mismatches in localization strings.

### Step 2: Create and Register Localization Service

The `ISyncfusionStringLocalizer` interface acts as middleware between Syncfusion® Blazor UI components and resource files. It uses `ResourceManager` to provide culture-specific resources at runtime.

**Create a SyncfusionLocalizer class:**

```csharp
using Syncfusion.Blazor;

public class SyncfusionLocalizer : ISyncfusionStringLocalizer
{
    public string GetText(string key)
    {
        return this.ResourceManager.GetString(key);
    }

    public System.Resources.ResourceManager ResourceManager
    {
        get
        {
            // Replace the ApplicationNamespace with your application name.
            return ApplicationNamespace.Resources.SfResources.ResourceManager;

            // For .Net Maui Blazor App
            // return ApplicationNamespace.LocalizationResources.SfResources.ResourceManager;
        }
    }
}
```

**Register in Program.cs:**

```csharp
using Syncfusion.Blazor;

builder.Services.AddSyncfusionBlazor();
// Register the locale service to localize the SyncfusionBlazor components.
builder.Services.AddSingleton(typeof(ISyncfusionStringLocalizer), typeof(SyncfusionLocalizer));
```

> **Important**: For Blazor Web App using Interactive render mode (WebAssembly or Auto), register `SyncfusionLocalizer` and the Syncfusion® Blazor services in **both** Server and Client `Program.cs` files. For .NET MAUI Blazor apps, register in `MauiProgram.cs`.

---

## Setting Culture

### Statically Set the Culture

#### Blazor Web App and Blazor WASM App

**Using Blazor's Start Options:**

1. Add `autostart="false"` to the Blazor `<script>` tag in `~/Components/App.razor` (for Blazor Web Apps) or `wwwroot/index.html` (for WASM Standalone apps)

```html
<body>
    ...
    <script src="_framework/blazor.web.js" autostart="false"></script>
    ...
</body>
```

2. Add the script block below the Blazor `<script>` tag to start Blazor with a specific culture:

```html
<body>
    ...
    <script src="_framework/blazor.web.js" autostart="false"></script>
    <script>
        Blazor.start({
            webAssembly: {
                applicationCulture: 'de'
            }
        });
    </script>
    ...
</body>
```

**Using C# Code:**

```csharp
using System.Globalization;

CultureInfo.DefaultThreadCurrentCulture = new CultureInfo("de-DE");
CultureInfo.DefaultThreadCurrentUICulture = new CultureInfo("de-DE");
```

#### MAUI Blazor App

Set culture in `MauiProgram.cs`:

```csharp
using System.Globalization;

CultureInfo.DefaultThreadCurrentCulture = new CultureInfo("de-DE");
CultureInfo.DefaultThreadCurrentUICulture = new CultureInfo("de-DE");
```

---

### Dynamically Set the Culture

#### Blazor Web App and Blazor Standalone WASM App

**1. Configure in .csproj:**

```xml
<PropertyGroup>
    <BlazorWebAssemblyLoadAllGlobalizationData>true</BlazorWebAssemblyLoadAllGlobalizationData>
</PropertyGroup>
```

**2. Add JavaScript for culture persistence:**

```html
<script src="_framework/blazor.web.js"></script>
<script>
    window.cultureInfo = {
        get: () => window.localStorage['BlazorCulture'],
        set: (value) => window.localStorage['BlazorCulture'] = value
    };
</script>
```

**3. Configure in Program.cs:**

```csharp
using Microsoft.JSInterop;
using System.Globalization;

builder.Services.AddSyncfusionBlazor();
builder.Services.AddSingleton(typeof(ISyncfusionStringLocalizer), typeof(SyncfusionLocalizer));

var host = builder.Build();

// Setting culture of the application
var jsInterop = host.Services.GetRequiredService<IJSRuntime>();
var result = await jsInterop.InvokeAsync<string>("cultureInfo.get");
CultureInfo culture;
if (result != null)
{
    culture = new CultureInfo(result);
}
else
{
    culture = new CultureInfo("en-US");
    await jsInterop.InvokeVoidAsync("cultureInfo.set", "en-US");
}
CultureInfo.DefaultThreadCurrentCulture = culture;
CultureInfo.DefaultThreadCurrentUICulture = culture;

await builder.Build().RunAsync();
```

**4. Create a CultureSwitcher component:**

```razor
@using System.Globalization
@inject IJSRuntime JSRuntime
@inject NavigationManager NavigationManager

<select @bind="Culture">
    @foreach (var culture in supportedCultures)
    {
        <option value="@culture">@culture.DisplayName</option>
    }
</select>

@code {
    private CultureInfo[] supportedCultures = new[]
    {
        new CultureInfo("en-US"),
        new CultureInfo("de-DE"),
        new CultureInfo("fr-FR"),
        new CultureInfo("ar-AE"),
        new CultureInfo("zh-HK")
    };

    private CultureInfo Culture
    {
        get => CultureInfo.CurrentCulture;
        set
        {
            if (CultureInfo.CurrentCulture != value)
            {
                var js = (IJSInProcessRuntime)JSRuntime;
                js.InvokeVoid("cultureInfo.set", value.Name);
                NavigationManager.NavigateTo(NavigationManager.Uri, forceLoad: true);
            }
        }
    }
}
```

**5. Add CultureSwitcher to MainLayout.razor:**

```razor
<div class="page">
    ....
    <main>
        <div class="top-row px-4">
            <CultureSwitcher @rendermode="@InteractiveAuto" />
            ....
        </div>
    </main>
</div>
```

#### Blazor Server App and Blazor Web App (Interactive Server)

**1. Configure in Program.cs:**

```csharp
builder.Services.AddControllers();
builder.Services.AddSyncfusionBlazor();
builder.Services.AddLocalization();

var supportedCultures = new[] { "en-US", "de-DE", "fr-FR", "ar-AE", "zh-HK" };
var localizationOptions = new RequestLocalizationOptions()
    .SetDefaultCulture(supportedCultures[0])
    .AddSupportedCultures(supportedCultures)
    .AddSupportedUICultures(supportedCultures);

var app = builder.Build();
app.UseRequestLocalization(localizationOptions);

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
    app.UseHsts();
}
app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();
app.MapControllers();
app.MapBlazorHub();
app.MapFallbackToPage("/_Host");

app.Run();
```

**2. Set culture in App.razor:**

```razor
@using System.Globalization
@using Microsoft.AspNetCore.Localization

@code {
    [CascadingParameter]
    public HttpContext? HttpContext { get; set; }

    protected override void OnInitialized()
    {
        HttpContext?.Response.Cookies.Append(
            CookieRequestCultureProvider.DefaultCookieName,
            CookieRequestCultureProvider.MakeCookieValue(
                new RequestCulture(
                    CultureInfo.CurrentCulture,
                    CultureInfo.CurrentUICulture)));
    }
}
```

**3. Create a CultureController:**

```csharp
using Microsoft.AspNetCore.Localization;
using Microsoft.AspNetCore.Mvc;

[Route("[controller]/[action]")]
public class CultureController : Controller
{
    public IActionResult SetCulture(string culture, string redirectUri)
    {
        if (culture != null)
        {
            HttpContext.Response.Cookies.Append(
                CookieRequestCultureProvider.DefaultCookieName,
                CookieRequestCultureProvider.MakeCookieValue(
                    new RequestCulture(culture)));
        }
        return LocalRedirect(redirectUri);
    }
}
```

**4. Create a CultureSwitcher component:**

```razor
@using System.Globalization
@inject NavigationManager NavigationManager
@inject HttpClient Http

<p>
    <label>
        Select your locale:
        <select @bind="Culture">
            @foreach (var culture in supportedCultures)
            {
                <option value="@culture">@culture.DisplayName</option>
            }
        </select>
    </label>
</p>

@code {
    private CultureInfo[] supportedCultures = new[]
    {
        new CultureInfo("en-US"),
        new CultureInfo("de-DE"),
        new CultureInfo("fr-FR"),
        new CultureInfo("ar-AE"),
        new CultureInfo("zh-HK")
    };

    protected override void OnInitialized()
    {
        Culture = CultureInfo.CurrentCulture;
    }

    private CultureInfo Culture
    {
        get => CultureInfo.CurrentCulture;
        set
        {
            if (CultureInfo.CurrentCulture != value)
            {
                var uri = new Uri(NavigationManager.Uri)
                    .GetComponents(UriComponents.PathAndQuery, UriFormat.Unescaped);
                var cultureEscaped = Uri.EscapeDataString(value.Name);
                var uriEscaped = Uri.EscapeDataString(uri);

                NavigationManager.NavigateTo(
                    $"Culture/SetCulture?culture={cultureEscaped}&redirectUri={uriEscaped}",
                    forceLoad: true);
            }
        }
    }
}
```

**5. Add CultureSwitcher to MainLayout.razor:**

```razor
<div class="page">
    <div class="sidebar">
        <NavMenu />
    </div>

    <main>
        <div class="top-row px-4">
            <CultureSwitcher></CultureSwitcher>
            <a href="https://learn.microsoft.com/aspnet/core/" target="_blank">About</a>
        </div>

        <article class="content px-4">
            @Body
        </article>
    </main>
</div>
```

#### MAUI Blazor App

**1. Configure culture in App.xaml.cs:**

```csharp
using System.Globalization;

namespace LocalizationMauiBlazor
{
    public partial class App : Application
    {
        public App()
        {
            InitializeComponent();
            var language = Preferences.Get("language", "en-US");
            var culture = new CultureInfo(language);
            CultureInfo.DefaultThreadCurrentCulture = culture;
            CultureInfo.DefaultThreadCurrentUICulture = culture;
            MainPage = new MainPage();
        }
    }
}
```

**2. Create a CultureSwitcher component:**

```razor
@using System.Globalization
@inject NavigationManager NavigationManager

<select @bind="Culture">
    @foreach (var culture in supportedCultures)
    {
        <option value="@culture">@culture.DisplayName</option>
    }
</select>

@code {
    private CultureInfo[] supportedCultures = new[]
    {
        new CultureInfo("en-US"),
        new CultureInfo("de-DE"),
        new CultureInfo("fr-FR"),
        new CultureInfo("ar-AE"),
        new CultureInfo("zh-HK")
    };

    private CultureInfo Culture
    {
        get => CultureInfo.CurrentCulture;
        set
        {
            if (CultureInfo.CurrentCulture != value)
            {
                CultureInfo.DefaultThreadCurrentCulture = value;
                CultureInfo.DefaultThreadCurrentUICulture = value;
                Preferences.Set("language", value.Name);
                NavigationManager.NavigateTo(NavigationManager.Uri, forceLoad: true);
            }
        }
    }
}
```

**3. Add CultureSwitcher to MainLayout.razor:**

```razor
@inherits LayoutComponentBase

<div class="page">
    <div class="sidebar">
        <NavMenu />
    </div>

    <main>
        <div class="top-row px-4">
            <a href="https://learn.microsoft.com/aspnet/core/" target="_blank">About</a>
        </div>

        <article class="content px-4">
            <CultureSwitcher />
            @Body
        </article>
    </main>
</div>
```

---

## Globalization in Blazor

### Culture and UI Culture

The Blazor framework uses built-in .NET types from the `System.Globalization` namespace:

- **Culture** (`CultureInfo.CurrentCulture`): Determines the formatting of numbers, dates, and times
- **UI Culture** (`CultureInfo.CurrentUICulture`): Determines the language of the user interface and which `.resx` resources are used

### HTML Input Types and Culture

When working with HTML form fields, browser-native input types affect culture behavior:

**Consistent Across Browsers:**
- `date`
- `number`

**Inconsistently Supported (Less Reliable):**
- `datetime-local`
- `month`
- `week`

Blazor relies on the browser's handling of these input types, which ensures that user input is parsed and rendered according to their specific culture settings.

### Globalization Example

The following example shows how globalization affects rendered values by formatting dates and numbers according to the current culture:

```razor
@page "/"
@using System.Globalization

<ul>
    <li><b>CurrentCulture</b>: @CultureInfo.CurrentCulture</li>
    <li><b>CurrentUICulture</b>: @CultureInfo.CurrentUICulture</li>
</ul>

<h2>Rendered values</h2>

<ul>
    <li><b>Date</b>: @dt.ToLongDateString()</li>
    <li><b>Number</b>: @number.ToString("N2")</li>
</ul>

@code {
    private DateTime dt = DateTime.Now;
    private double number = 1999.69;
}
```

---

## Alternative: Localization Using Database

Instead of using `.resx` resource files, you can perform localization using a database. For details, refer to the [support article on database localization](https://support.syncfusion.com/kb/article/11465/how-to-perform-localization-using-database-instead-of-resource-files-in-blazor).

---

