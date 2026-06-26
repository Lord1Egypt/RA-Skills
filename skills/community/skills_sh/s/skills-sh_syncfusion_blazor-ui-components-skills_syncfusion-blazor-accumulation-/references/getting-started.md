## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation Steps](#installation-steps)
   - [Option 1: Using Visual Studio](#option-1-using-visual-studio)
   - [Option 2: Using Visual Studio Code](#option-2-using-visual-studio-code)
   - [Option 3: Using .NET CLI](#option-3-using-net-cli)
- [Configuration Steps](#configuration-steps)
   - [Step 1: Import Namespaces](#step-1-import-namespaces)
   - [Step 2: Register Syncfusion Services](#step-2-register-syncfusion-services)
   - [Step 3: Add Stylesheet and Scripts](#step-3-add-stylesheet-and-scripts)
- [Create Your First Accumulation Chart](#create-your-first-accumulation-chart)
   - [Basic Pie Chart Example](#basic-pie-chart-example)
   - [Run the Application](#run-the-application)
- [Adding Essential Features](#adding-essential-features)
   - [Add Chart Title](#add-chart-title)
   - [Enable Data Labels](#enable-data-labels)
   - [Enable Tooltips](#enable-tooltips)
   - [Enable Legend](#enable-legend)
- [Understanding Data Binding](#understanding-data-binding)
   - [Key Properties](#key-properties)
   - [Data Model Requirements](#data-model-requirements)
   - [Different Data Types](#different-data-types)
- [Complete Working Example](#complete-working-example)
- [Troubleshooting Common Issues](#troubleshooting-common-issues)
   - [Chart Not Rendering](#chart-not-rendering)
   - [Data Not Displaying](#data-not-displaying)
   - [Theme Not Applied](#theme-not-applied)
   - [Namespace Errors](#namespace-errors)
- [Next Steps](#next-steps)
- [See Also](#see-also)

# Getting Started with Blazor Accumulation Charts

This guide covers the complete setup and basic implementation of Syncfusion Blazor Accumulation Chart components in Blazor applications using Visual Studio, Visual Studio Code, or .NET CLI.

## Prerequisites

Before starting, ensure you have:
- [.NET SDK](https://dotnet.microsoft.com/download) (latest version recommended)
- [Visual Studio 2022](https://visualstudio.microsoft.com/vs/), [VS Code](https://code.visualstudio.com/), or .NET CLI
- [System requirements for Blazor components](https://blazor.syncfusion.com/documentation/system-requirements)
- Basic knowledge of Blazor and C#

## Installation Steps

### Option 1: Using Visual Studio

#### Step 1: Create Blazor Project

1. Open Visual Studio 2022
2. Create a new project → **Blazor WebAssembly App** or **Blazor Server App**
3. Choose .NET 6.0 or later
4. Name your project and select location
5. Click **Create**

You can also use the [Syncfusion Blazor Extension](https://blazor.syncfusion.com/documentation/visual-studio-integration/template-studio) for project templates.

#### Step 2: Install NuGet Packages

**Method A: NuGet Package Manager UI**
1. Right-click project → **Manage NuGet Packages**
2. Search for `Syncfusion.Blazor.Charts`
3. Install the latest version
4. Repeat for `Syncfusion.Blazor.Themes`

**Method B: Package Manager Console**
```powershell
Install-Package Syncfusion.Blazor.Charts
Install-Package Syncfusion.Blazor.Themes
```

---

### Option 2: Using Visual Studio Code

#### Step 1: Create Blazor Project

Open terminal (Ctrl+`) and run:

```bash
dotnet new blazorwasm -o MyAccumulationChartApp
cd MyAccumulationChartApp
```

For Blazor Server:
```bash
dotnet new blazorserver -o MyAccumulationChartApp
cd MyAccumulationChartApp
```

#### Step 2: Install NuGet Packages

In the integrated terminal:

```bash
dotnet add package Syncfusion.Blazor.Charts
dotnet add package Syncfusion.Blazor.Themes
dotnet restore
```

---

### Option 3: Using .NET CLI

#### Step 1: Verify .NET Installation

```bash
dotnet --version
```

#### Step 2: Create and Configure Project

```bash
# Create project
dotnet new blazorwasm -o MyAccumulationChartApp
cd MyAccumulationChartApp

# Install packages
dotnet add package Syncfusion.Blazor.Charts
dotnet add package Syncfusion.Blazor.Themes
dotnet restore
```

## Configuration Steps

### Step 1: Import Namespaces

Open `_Imports.razor` and add:

```csharp
@using Syncfusion.Blazor
@using Syncfusion.Blazor.Charts
```

This makes Syncfusion components available throughout your application.

---

### Step 2: Register Syncfusion Services

**For Blazor WebAssembly** (`Program.cs`):

```csharp
using Microsoft.AspNetCore.Components.Web;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
using Syncfusion.Blazor;

var builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.RootComponents.Add<App>("#app");
builder.RootComponents.Add<HeadOutlet>("head::after");

builder.Services.AddScoped(sp => 
    new HttpClient { BaseAddress = new Uri(builder.HostEnvironment.BaseAddress) });

// Register Syncfusion services
builder.Services.AddSyncfusionBlazor();

await builder.Build().RunAsync();
```

**For Blazor Server** (`Program.cs`):

```csharp
using Syncfusion.Blazor;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddRazorPages();
builder.Services.AddServerSideBlazor();

// Register Syncfusion services
builder.Services.AddSyncfusionBlazor();

var app = builder.Build();
// ... rest of configuration
```

---

### Step 3: Add Stylesheet and Scripts

**For Blazor WebAssembly** - Add to `wwwroot/index.html` inside `<head>`:

```html
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>My Accumulation Chart App</title>
    <base href="/" />
    
    <!-- Syncfusion theme stylesheet -->
    <link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />
    
    <!-- Syncfusion Blazor script -->
    <script src="_content/Syncfusion.Blazor.Core/scripts/syncfusion-blazor.min.js" 
            type="text/javascript"></script>
</head>
```

**For Blazor Server** - Add to `Pages/_Layout.cshtml` or `Pages/_Host.cshtml` inside `<head>`.

**Available Themes:**
- `bootstrap5.css` - Bootstrap 5 (recommended)
- `material.css` - Material Design
- `fluent.css` - Microsoft Fluent UI
- `tailwind.css` - Tailwind CSS
- `fabric.css` - Office Fabric
- `bootstrap5-dark.css` - Bootstrap 5 Dark Mode
- `material-dark.css` - Material Dark Mode

**Alternative: CDN Reference**
```html
<link href="https://cdn.syncfusion.com/blazor/23.1.36/styles/bootstrap5.css" rel="stylesheet" />
<script src="https://cdn.syncfusion.com/blazor/23.1.36/syncfusion-blazor.min.js"></script>
```

## Create Your First Accumulation Chart

### Basic Pie Chart Example

Create or open `Pages/Index.razor`:

```razor
@page "/"
@using Syncfusion.Blazor.Charts

<h3>Sales Distribution</h3>

<SfAccumulationChart>
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@SalesData" 
                                 XName="Product" 
                                 YName="Sales">
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
</SfAccumulationChart>

@code {
    public class ProductSales
    {
        public string Product { get; set; }
        public double Sales { get; set; }
    }

    public List<ProductSales> SalesData = new List<ProductSales>
    {
        new ProductSales { Product = "Product A", Sales = 35 },
        new ProductSales { Product = "Product B", Sales = 28 },
        new ProductSales { Product = "Product C", Sales = 22 },
        new ProductSales { Product = "Product D", Sales = 15 }
    };
}
```

### Run the Application

**Visual Studio:** Press `Ctrl+F5` or `F5`

**VS Code or CLI:** 
```bash
dotnet run
```

Then open browser to `https://localhost:5001` (or the displayed URL).

## Adding Essential Features

### Add Chart Title

```razor
<SfAccumulationChart Title="Sales Distribution by Product">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@SalesData" 
                                 XName="Product" 
                                 YName="Sales">
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
</SfAccumulationChart>
```

### Enable Data Labels

```razor
<SfAccumulationChart Title="Sales Distribution by Product">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@SalesData" 
                                 XName="Product" 
                                 YName="Sales">
            <!-- Enable data labels -->
            <AccumulationDataLabelSettings Visible="true" 
                                           Name="Product">
            </AccumulationDataLabelSettings>
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
</SfAccumulationChart>
```

### Enable Tooltips

```razor
<SfAccumulationChart Title="Sales Distribution by Product">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@SalesData" 
                                 XName="Product" 
                                 YName="Sales">
            <AccumulationDataLabelSettings Visible="true">
            </AccumulationDataLabelSettings>
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
    
    <!-- Enable tooltip -->
    <AccumulationChartTooltipSettings Enable="true">
    </AccumulationChartTooltipSettings>
</SfAccumulationChart>
```

### Enable Legend

```razor
<SfAccumulationChart Title="Sales Distribution by Product">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@SalesData" 
                                 XName="Product" 
                                 YName="Sales">
            <AccumulationDataLabelSettings Visible="true">
            </AccumulationDataLabelSettings>
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
    
    <AccumulationChartTooltipSettings Enable="true">
    </AccumulationChartTooltipSettings>
    
    <!-- Enable legend -->
    <AccumulationChartLegendSettings Visible="true">
    </AccumulationChartLegendSettings>
</SfAccumulationChart>
```

## Understanding Data Binding

### Key Properties

- **DataSource**: Your data collection (List, IEnumerable, etc.)
- **XName**: Property name for category labels (string)
- **YName**: Property name for numeric values (number)

### Data Model Requirements

Your data class must have:
1. A property for labels/categories (mapped to XName)
2. A property for numeric values (mapped to YName)

```csharp
public class ChartData
{
    public string Category { get; set; }  // For XName
    public double Value { get; set; }     // For YName
}
```

### Different Data Types

**With percentage data:**
```csharp
public List<MarketShare> MarketData = new List<MarketShare>
{
    new MarketShare { Company = "Company A", Share = 35.5 },
    new MarketShare { Company = "Company B", Share = 28.3 },
    new MarketShare { Company = "Company C", Share = 20.1 },
    new MarketShare { Company = "Others", Share = 16.1 }
};
```

**With integer counts:**
```csharp
public List<SurveyResult> Results = new List<SurveyResult>
{
    new SurveyResult { Option = "Yes", Count = 450 },
    new SurveyResult { Option = "No", Count = 280 },
    new SurveyResult { Option = "Maybe", Count = 170 }
};
```

## Complete Working Example

Here's a full-featured pie chart with all essential elements:

```razor
@page "/sales-chart"
@using Syncfusion.Blazor.Charts

<div class="container">
    <h2>Q4 2025 Sales Performance</h2>
    
    <SfAccumulationChart Title="Revenue Distribution by Product Line"
                         Height="450px"
                         Width="100%"
                         Background="transparent">
        
        <AccumulationChartSeriesCollection>
            <AccumulationChartSeries DataSource="@RevenueData" 
                                     XName="ProductLine" 
                                     YName="Revenue"
                                     Name="Revenue">
                
                <!-- Data labels with product names -->
                <AccumulationDataLabelSettings Visible="true" 
                                               Name="ProductLine"
                                               Position="Syncfusion.Blazor.Charts.AccumulationLabelPosition.Outside">
                    <AccumulationDataLabelConnector Length="20px">
                    </AccumulationDataLabelConnector>
                </AccumulationDataLabelSettings>
                
            </AccumulationChartSeries>
        </AccumulationChartSeriesCollection>
        
        <!-- Tooltip with currency formatting -->
        <AccumulationChartTooltipSettings Enable="true" 
                                          Format="${point.x}: <b>${point.y}M</b>">
        </AccumulationChartTooltipSettings>
        
        <!-- Legend positioned at bottom -->
        <AccumulationChartLegendSettings Visible="true" 
                                         Position="Syncfusion.Blazor.Charts.LegendPosition.Bottom">
        </AccumulationChartLegendSettings>
        
    </SfAccumulationChart>
</div>

@code {
    public class RevenueInfo
    {
        public string ProductLine { get; set; }
        public double Revenue { get; set; }
    }

    public List<RevenueInfo> RevenueData = new List<RevenueInfo>
    {
        new RevenueInfo { ProductLine = "Software", Revenue = 125.5 },
        new RevenueInfo { ProductLine = "Hardware", Revenue = 98.2 },
        new RevenueInfo { ProductLine = "Services", Revenue = 76.8 },
        new RevenueInfo { ProductLine = "Consulting", Revenue = 54.3 },
        new RevenueInfo { ProductLine = "Training", Revenue = 25.2 }
    };
}
```

## Troubleshooting Common Issues

### Chart Not Rendering

**Problem:** Blank page or no chart visible

**Solutions:**
1. Verify script reference in `index.html` or `_Host.cshtml`
2. Check that `AddSyncfusionBlazor()` is called in `Program.cs`
3. Ensure namespaces are imported in `_Imports.razor`
4. Check browser console for JavaScript errors

### Data Not Displaying

**Problem:** Chart renders but no data shown

**Solutions:**
1. Verify `DataSource` is not null or empty
2. Check `XName` and `YName` match your data class property names (case-sensitive)
3. Ensure YName property contains numeric values (not strings)
4. Check data initialization in `OnInitialized` or `OnInitializedAsync` if async

### Theme Not Applied

**Problem:** Chart has no styling or wrong theme

**Solutions:**
1. Verify stylesheet link in `<head>` section
2. Check theme file path: `_content/Syncfusion.Blazor.Themes/bootstrap5.css`
3. Try hard refresh (Ctrl+F5) to clear cache
4. Verify `Syncfusion.Blazor.Themes` package is installed

### Namespace Errors

**Problem:** `SfAccumulationChart` not recognized

**Solutions:**
1. Add `@using Syncfusion.Blazor.Charts` to page or `_Imports.razor`
2. Rebuild solution
3. Verify `Syncfusion.Blazor.Charts` NuGet package is installed

## Next Steps

Now that you have a basic accumulation chart working:

1. **Explore Chart Types** - Learn about doughnut, funnel, and pyramid charts
2. **Customize Data Labels** - Add formatting, positioning, and templates
3. **Style Your Charts** - Apply gradients, colors, and themes
4. **Add Interactivity** - Implement events, selection, and animations
5. **Optimize for Production** - Configure licensing and performance

## See Also

- [Syncfusion Blazor Documentation](https://blazor.syncfusion.com/documentation/accumulation-chart/getting-started)
- [API Reference](https://help.syncfusion.com/cr/blazor/Syncfusion.Blazor.Charts.SfAccumulationChart.html)
- [Live Demos](https://blazor.syncfusion.com/demos/chart/pie)
