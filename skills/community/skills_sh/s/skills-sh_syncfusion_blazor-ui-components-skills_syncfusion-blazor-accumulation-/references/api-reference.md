---
title: Accumulation Chart API Reference
summary: Reference for enums, public methods, and critical usage notes for `SfAccumulationChart` and related types.
---

# Accumulation Chart API Reference

This document provides a concise reference for the public API surface of the Syncfusion Blazor `SfAccumulationChart` and commonly used related types. It covers enum values, public methods, important usage notes, and quick code examples.

## Common Enums

- `AccumulationType`
  - `Pie`
  - `Funnel`
  - `Pyramid`

- `AccumulationLabelPosition` (aka `AccumulationDataLabelSettings.Position`)
  - `Inside`
  - `Outside`

- `GroupMode`
  - `Value`    (group by value threshold)
  - `Point`    (group by point count)

- `LegendPosition`
  - `Top`
  - `Bottom`
  - `Left`
  - `Right`

- `ExportType`
  - `PNG`
  - `JPEG`
  - `SVG`
  - `PDF`

Notes: When specifying enum values in markup, use fully-qualified names if necessary (for example `Syncfusion.Blazor.Charts.AccumulationType.Pie`) in contexts where the namespace is ambiguous.

## Key Component Properties (summary)

- `AccumulationChartSeries.Type` (AccumulationType) — Pie, Funnel, Pyramid.
- `AccumulationChartSeries.InnerRadius` (string) — Inner radius for doughnut charts (e.g. "40%").
- `AccumulationChartSeries.Radius` (string) — Overall slice radius (e.g. "80%").
- `AccumulationChartSeries.GroupTo` (int or double) — Value or point count threshold used with `GroupMode`.
- `AccumulationChartSeries.GroupMode` (GroupMode) — `Value` or `Point`.
- `AccumulationDataLabelSettings.Visible` (bool) — Show/hide data labels.
- `AccumulationChartLegendSettings.Visible` (bool) — Show/hide legend.
- `AccumulationChartTooltipSettings.Enable` (bool) — Enable/disable tooltips.

## Theme Enum

The `SfAccumulationChart` component supports the `Theme` property which uses the `Syncfusion.Blazor.Theme` enum.

**IMPORTANT:** The enum name is `Theme`, NOT `AccumulationChartTheme`. Use it as `Theme="Syncfusion.Blazor.Theme.Material"` or `Theme="Theme.Material"` (with proper using directive).

```csharp
public enum Theme
{
    Material,
    Fabric,
    Bootstrap,
    Bootstrap4,
    HighContrastLight,
    MaterialDark,
    FabricDark,
    BootstrapDark,
    Bootstrap4Dark,
    HighContrast,
    Tailwind,
    TailwindDark,
    Bootstrap5,
    Bootstrap5Dark,
    Fluent,
    FluentDark,
    Material3,
    Material3Dark
}
```

**Usage Example:**
```razor
<SfAccumulationChart Title="Sales Distribution" Theme="Syncfusion.Blazor.Theme.Bootstrap5">
    <!-- chart content -->
</SfAccumulationChart>
```

## Public Methods

The `SfAccumulationChart` component exposes a small set of useful public methods. Typical usage calls these from code-behind or event handlers.

- `Task ExportAsync(ExportType type, string fileName, PdfPageOrientation? orientation = null, bool allowDownload = true)`
  - Exports the chart to the requested format. For `PDF`, `orientation` may be specified.
  - Example: `await chart.ExportAsync(ExportType.PNG, "chart.png");`

- `Task PrintAsync()`
  - Invokes the browser print dialog for the chart display area.
  - Example: `await chart.PrintAsync();`

- `void Refresh(bool shouldAnimate = true)`
  - Refreshes/redraws the chart. Pass `false` to skip animation.
  - Example: `chart.Refresh(false);`

- `Task SetAnnotationValueAsync(double annotationIndex, string content)`
  - Updates the content of an annotation at runtime.
  - Example: `await chart.SetAnnotationValueAsync(0, "Updated content");`

Notes: The component instance (for calling instance methods) is usually obtained by assigning `@ref` to the `SfAccumulationChart` in Razor markup.

## Critical Usage Notes and Gotchas

- Center labels apply only to Doughnut charts: `AccumulationChartCenterLabel` content is meaningful when `InnerRadius` is set (doughnut). Using center-label markup for non-doughnut series will have no effect.
- `GroupTo` semantics depend on `GroupMode`: when `GroupMode` is `Value`, `GroupTo` is treated as the numeric threshold to group smaller values into "Others"; when `Point`, it defines the point count to group.
- Data label `Position` must be set using the enum (e.g. `Syncfusion.Blazor.Charts.AccumulationLabelPosition.Outside`) if the context doesn't include the `Syncfusion.Blazor.Charts` namespace.
- Legend visibility toggling (`ToggleVisibility`) and click behavior are controlled by legend settings; ensure `ToggleVisibility` is enabled when you expect legend-item clicks to hide/show points.
- Exporting large charts or complex templates may increase memory usage in the browser; prefer vector formats (SVG/PDF) when high fidelity is required.

## Common Patterns and Examples

Basic pie chart

```razor
<SfAccumulationChart @ref="chart" Title="Sales">
  <AccumulationChartSeriesCollection>
    <AccumulationChartSeries DataSource="@SalesData" XName="Product" YName="Sales">
      <AccumulationDataLabelSettings Visible="true"/>
    </AccumulationChartSeries>
  </AccumulationChartSeriesCollection>
  <AccumulationChartLegendSettings Visible="true"/>
</SfAccumulationChart>

@code {
  SfAccumulationChart chart;
  List<object> SalesData = new List<object> { /* ... */ };
}
```

Doughnut with center label and export

```razor
<AccumulationChartSeries Type="Syncfusion.Blazor.Charts.AccumulationType.Pie" InnerRadius="40%" DataSource="@Data" XName="Category" YName="Value">
  <AccumulationDataLabelSettings Visible="true" Position="Syncfusion.Blazor.Charts.AccumulationLabelPosition.Outside" />
  <AccumulationChartCenterLabel Text="Total<br/>$1.2M" />
</AccumulationChartSeries>

@code {
  SfAccumulationChart chartRef;

  async Task ExportPng() {
    await chartRef.ExportAsync(ExportType.PNG, "doughnut.png");
  }
}
```

Grouping small slices

```razor
<AccumulationChartSeries GroupTo="5" GroupMode="Syncfusion.Blazor.Charts.GroupMode.Value" />
```

Zoom/interaction note: Accumulation charts are non-cartesian; pinch/zoom interactions available for Cartesian charts are not applicable to accumulation charts. Use selection, explosion, and tooltip settings for interactivity instead.

## Troubleshooting

- If labels overlap badly, enable smart labels (`AccumulationDataLabelSettings` with smart positioning) or move labels outside using `Position=Outside`.
- If center label does not appear, verify `Type=Pie` and `InnerRadius` is a non-empty percentage.
- If a fully-qualified enum compiles error, add `@using Syncfusion.Blazor.Charts` to your Razor file or use the full type name.
