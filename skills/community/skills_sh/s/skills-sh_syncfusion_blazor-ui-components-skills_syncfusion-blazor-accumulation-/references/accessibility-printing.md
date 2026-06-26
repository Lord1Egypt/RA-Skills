## Table of Contents

- [Accessibility Overview](#accessibility-overview)
- [WAI-ARIA Attributes](#wai-aria-attributes)
   - [Adding Custom ARIA Labels](#adding-custom-aria-labels)
- [Keyboard Navigation](#keyboard-navigation)
   - [Keyboard Shortcuts](#keyboard-shortcuts)
   - [Enable Keyboard Navigation](#enable-keyboard-navigation)
   - [Focus Management](#focus-management)
- [Screen Reader Support](#screen-reader-support)
   - [Accessible Data Representation](#accessible-data-representation)
   - [Data Table Alternative](#data-table-alternative)
- [High Contrast Mode](#high-contrast-mode)
   - [High Contrast Themes](#high-contrast-themes)
   - [Custom High Contrast Colors](#custom-high-contrast-colors)
- [Right-to-Left (RTL) Support](#right-to-left-rtl-support)
   - [Enable RTL](#enable-rtl)
- [Mobile Accessibility](#mobile-accessibility)
   - [Touch-Optimized Settings](#touch-optimized-settings)
- [Printing](#printing)
   - [Basic Printing](#basic-printing)
   - [Print with Event Handling](#print-with-event-handling)
   - [Print Configuration](#print-configuration)
- [Image Export](#image-export)
   - [Export as PNG](#export-as-png)
   - [Export Types](#export-types)
   - [Export with Options](#export-with-options)
   - [Export Event](#export-event)
- [Localization](#localization)
   - [Basic Localization](#basic-localization)
   - [Custom Localization](#custom-localization)
- [Accessibility Testing](#accessibility-testing)
   - [Automated Testing Tools](#automated-testing-tools)
   - [Manual Testing Checklist](#manual-testing-checklist)
- [Best Practices](#best-practices)
   - [Content](#content)
   - [Visual Design](#visual-design)
   - [Interaction](#interaction)
   - [Documentation](#documentation)
- [See Also](#see-also)

# Accessibility and Printing

This guide covers accessibility features for inclusive data visualization and printing/export capabilities for Syncfusion Blazor Accumulation Charts.

## Accessibility Overview

Syncfusion Blazor Accumulation Charts comply with:
- **WCAG 2.2** (AA level)
- **Section 508**
- **ADA** standards
- **WAI-ARIA** patterns

**Supported accessibility features:**
- Screen reader support
- Keyboard navigation
- High contrast themes
- Right-to-left (RTL) support
- Mobile device accessibility
- Color contrast compliance

## WAI-ARIA Attributes

Charts automatically include appropriate ARIA attributes:

**Roles:**
- `img` - Chart container
- `button` - Interactive elements
- `region` - Chart areas

**Attributes:**
- `aria-label` - Descriptive labels
- `aria-hidden` - Hidden decorative elements
- `aria-pressed` - Legend toggle state

### Adding Custom ARIA Labels

```razor
<SfAccumulationChart Title="Sales Distribution"
                     AriaLabel="Sales distribution pie chart showing product sales percentages">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@Data" XName="Product" YName="Sales">
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
</SfAccumulationChart>
```

**Best practices:**
- Provide meaningful titles
- Include data summary in aria-label
- Describe chart type and purpose
- Mention key insights

## Keyboard Navigation

Full keyboard support for non-mouse users.

### Keyboard Shortcuts

| Windows | Mac | Action |
|---------|-----|--------|
| <kbd>Alt</kbd> + <kbd>J</kbd> | <kbd>⌥</kbd> + <kbd>J</kbd> | Focus chart |
| <kbd>Tab</kbd> | <kbd>Tab</kbd> | Next element |
| <kbd>Shift</kbd> + <kbd>Tab</kbd> | <kbd>⇧</kbd> + <kbd>Tab</kbd> | Previous element |
| <kbd>↓</kbd> | <kbd>↓</kbd> | Next data point (left) |
| <kbd>↑</kbd> | <kbd>↑</kbd> | Previous data point (right) |
| <kbd>↓</kbd> / <kbd>←</kbd> | <kbd>↓</kbd> / <kbd>←</kbd> | Previous legend item |
| <kbd>↑</kbd> / <kbd>→</kbd> | <kbd>↑</kbd> / <kbd>→</kbd> | Next legend item |
| <kbd>Enter</kbd> / <kbd>Space</kbd> | <kbd>Enter</kbd> / <kbd>Space</kbd> | Toggle series visibility |
| <kbd>ESC</kbd> | <kbd>Esc</kbd> | Close tooltip |
| <kbd>Ctrl</kbd> + <kbd>P</kbd> | <kbd>⌘</kbd> + <kbd>P</kbd> | Print chart |

### Enable Keyboard Navigation

```razor
<SfAccumulationChart EnableKeyboardNavigation="true">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@Data" XName="X" YName="Y">
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
</SfAccumulationChart>
```

### Focus Management

```razor
<SfAccumulationChart @ref="ChartRef">
</SfAccumulationChart>

@code {
    private SfAccumulationChart ChartRef;

    private async Task FocusChart()
    {
        // Programmatically focus the chart
        await ChartRef.FocusAsync();
    }
}
```

## Screen Reader Support

Charts provide meaningful content to screen readers.

### Accessible Data Representation

```razor
<SfAccumulationChart Title="Q4 Sales by Region"
                     AriaLabel="Pie chart showing Q4 2025 sales distribution across four regions">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@RegionData" 
                                 XName="Region" 
                                 YName="Sales"
                                 Name="Sales by Region">
            <AccumulationDataLabelSettings Visible="true" Name="Region">
            </AccumulationDataLabelSettings>
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
    <AccumulationChartLegendSettings Visible="true">
    </AccumulationChartLegendSettings>
</SfAccumulationChart>
```

**Screen reader announcements:**
- Chart title and type
- Series name and count
- Point categories and values
- Legend items
- Interaction feedback

### Data Table Alternative

Provide tabular data for screen readers:

```razor
<div role="region" aria-label="Sales data table">
    <table>
        <caption>Q4 Sales by Region</caption>
        <thead>
            <tr>
                <th>Region</th>
                <th>Sales ($M)</th>
                <th>Percentage</th>
            </tr>
        </thead>
        <tbody>
            @foreach (var item in RegionData)
            {
                <tr>
                    <td>@item.Region</td>
                    <td>@item.Sales</td>
                    <td>@item.Percentage%</td>
                </tr>
            }
        </tbody>
    </table>
</div>

<SfAccumulationChart Title="Q4 Sales by Region" aria-describedby="sales-table">
    <!-- chart configuration -->
</SfAccumulationChart>
```

## High Contrast Mode

Support for users with visual impairments.

### High Contrast Themes

```razor
<SfAccumulationChart Theme="Syncfusion.Blazor.Theme.HighContrast">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@Data" XName="X" YName="Y">
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
</SfAccumulationChart>
```

**Available high contrast themes:**
- `Syncfusion.Blazor.Theme.HighContrast` - Dark background, high contrast colors
- `Syncfusion.Blazor.Theme.HighContrastLight` - Light background, high contrast colors

### Custom High Contrast Colors

```razor
<AccumulationChartSeries Palettes="@HighContrastPalette">
</AccumulationChartSeries>

@code {
    private string[] HighContrastPalette = new string[]
    {
        "#FFFF00",  // Yellow
        "#00FFFF",  // Cyan
        "#FF00FF",  // Magenta
        "#00FF00",  // Lime
        "#FFFFFF"   // White
    };
}
```

**Design guidelines:**
- Minimum 4.5:1 contrast ratio (WCAG AA)
- 7:1 for enhanced contrast (WCAG AAA)
- Avoid color-only information encoding
- Provide pattern fills as alternatives

## Right-to-Left (RTL) Support

For Arabic, Hebrew, and other RTL languages.

### Enable RTL

```razor
<SfAccumulationChart EnableRtl="true">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@Data" XName="Category" YName="Value">
            <AccumulationDataLabelSettings Visible="true">
            </AccumulationDataLabelSettings>
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
    <AccumulationChartLegendSettings Visible="true">
    </AccumulationChartLegendSettings>
</SfAccumulationChart>
```

**RTL behavior:**
- Legend positioned on left by default
- Data labels mirrored
- Slice order reversed
- Text alignment adjusted

## Mobile Accessibility

Ensure touch-friendly and accessible on mobile devices.

### Touch-Optimized Settings

```razor
<SfAccumulationChart EnableAdaptiveUI="true" Height="350px">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@Data" XName="X" YName="Y">
            <AccumulationDataLabelSettings Visible="false">
            </AccumulationDataLabelSettings>
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
    <AccumulationChartTooltipSettings Enable="true">
    </AccumulationChartTooltipSettings>
    <AccumulationChartLegendSettings Visible="true" Position="Syncfusion.Blazor.Charts.LegendPosition.Bottom">
    </AccumulationChartLegendSettings>
</SfAccumulationChart>
```

**Mobile best practices:**
- Larger touch targets (44x44px minimum)
- Bottom-positioned legend
- Tooltips instead of data labels
- Simplified interactions

## Printing

Print charts directly from the browser.

### Basic Printing

```razor
<SfAccumulationChart @ref="ChartRef">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@Data" XName="Product" YName="Sales">
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
</SfAccumulationChart>

<button @onclick="PrintChart">Print Chart</button>

@code {
    private SfAccumulationChart ChartRef;

    private async Task PrintChart()
    {
        await ChartRef.PrintAsync();
    }
}
```

### Print with Event Handling

```razor
<SfAccumulationChart @ref="ChartRef">
    <AccumulationChartEvents OnPrintComplete="PrintCompleted">
    </AccumulationChartEvents>
    <!-- series configuration -->
</SfAccumulationChart>

@code {
    private void PrintCompleted()
    {
        Console.WriteLine("Print operation completed");
        // Log, notify user, etc.
    }
}
```

### Print Configuration

```razor
@code {
    private async Task PrintWithSettings()
    {
        // Configure print settings
        await ChartRef.PrintAsync();
        
        // Browser's print dialog opens with:
        // - Chart rendered at current size
        // - Background colors preserved
        // - High-resolution output
    }
}
```

## Image Export

Export charts as PNG, JPEG, SVG, or PDF.

### Export as PNG

```razor
<SfAccumulationChart @ref="ChartRef">
    <!-- chart configuration -->
</SfAccumulationChart>

<button @onclick="ExportPNG">Export as PNG</button>

@code {
    private SfAccumulationChart ChartRef;

    private async Task ExportPNG()
    {
        await ChartRef.ExportAsync(Syncfusion.Blazor.Charts.ExportType.PNG, "SalesChart");
    }
}
```

### Export Types

```razor
@code {
    private async Task ExportChart(Syncfusion.Blazor.Charts.ExportType type)
    {
        string filename = $"Chart_{DateTime.Now:yyyyMMdd}";
        await ChartRef.ExportAsync(type, filename);
    }

    // Export types:
    // Syncfusion.Blazor.Charts.ExportType.PNG
    // Syncfusion.Blazor.Charts.ExportType.JPEG
    // Syncfusion.Blazor.Charts.ExportType.SVG
    // Syncfusion.Blazor.Charts.ExportType.PDF
}
```

### Export with Options

```razor
@code {
    private async Task ExportWithOptions()
    {
        var exportSettings = new ExportSettings
        {
            Type = Syncfusion.Blazor.Charts.ExportType.PNG,
            FileName = "HighResSalesChart",
            Orientation = PdfPageOrientation.Landscape,
            Width = 1920,
            Height = 1080
        };
        
        await ChartRef.ExportAsync(exportSettings);
    }
}
```

### Export Event

```razor
<AccumulationChartEvents OnExportComplete="ExportCompleted">
</AccumulationChartEvents>

@code {
    private void ExportCompleted(ExportEventArgs args)
    {
        Console.WriteLine($"Exported as {args.Type}");
        // Show success message, log event
    }
}
```

## Localization

Translate chart text for international audiences.

### Basic Localization

```razor
<SfAccumulationChart Locale="de-DE">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@Data" XName="Kategorie" YName="Wert">
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
</SfAccumulationChart>
```

### Custom Localization

```razor
@code {
    protected override void OnInitialized()
    {
        var culture = new CultureInfo("es-ES");
        CultureInfo.DefaultThreadCurrentCulture = culture;
        CultureInfo.DefaultThreadCurrentUICulture = culture;
    }
}
```

## Accessibility Testing

### Automated Testing Tools

**Axe DevTools:**
- Install browser extension
- Scan page with chart
- Review accessibility violations
- Fix issues and retest

**Lighthouse (Chrome DevTools):**
- Open DevTools
- Run Lighthouse audit
- Review Accessibility score
- Address findings

### Manual Testing Checklist

- [ ] Navigate entire chart with keyboard only
- [ ] Verify screen reader announcements
- [ ] Test with high contrast mode enabled
- [ ] Check color contrast ratios (4.5:1 minimum)
- [ ] Ensure touch targets 44x44px (mobile)
- [ ] Verify RTL layout (if applicable)
- [ ] Test print functionality
- [ ] Validate ARIA attributes
- [ ] Review focus indicators
- [ ] Check tooltip keyboard accessibility

## Best Practices

### Content
- Provide descriptive titles
- Include data summaries for screen readers
- Use clear, concise labels
- Avoid jargon in accessibility text

### Visual Design
- Maintain WCAG AA contrast ratios (4.5:1)
- Don't rely solely on color
- Use patterns or textures as backup
- Provide legends for color-coded data

### Interaction
- Support full keyboard navigation
- Provide clear focus indicators
- Allow dismissing tooltips with ESC
- Enable accessible selection modes

### Documentation
- Document keyboard shortcuts
- Provide data table alternatives
- Include accessibility statement
- Test with assistive technologies

## See Also

- [WCAG 2.2 Guidelines](https://www.w3.org/TR/WCAG22/)
- [Syncfusion Accessibility Documentation](https://blazor.syncfusion.com/documentation/common/accessibility)
- [Keyboard Navigation](animation-events.md) - Event handling
- [Tooltips](tooltip.md) - Accessible data display
- [Data Labels](data-label.md) - Alternative to tooltips
