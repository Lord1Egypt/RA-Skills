# Animation and Events

## Table of Contents

- [Animation](#animation)
   - [Enable/Disable Animation](#enabledisable-animation)
   - [Animation Behavior](#animation-behavior)
   - [Disable Animation on Programmatic Refresh](#disable-animation-on-programmatic-refresh)
   - [Custom Animation Timing](#custom-animation-timing)
- [Chart Lifecycle Events](#chart-lifecycle-events)
   - [OnLoad](#onload)
   - [Loaded](#loaded)
   - [BeforeResize / Resized](#beforeresize-resized)
   - [SizeChanged](#sizechanged)
- [Point and Series Events](#point-and-series-events)
   - [OnPointClick](#onpointclick)
   - [OnPointMove](#onpointmove)
   - [SeriesRender](#seriesrender)
- [Rendering Events](#rendering-events)
   - [OnPointRender](#onpointrender)
   - [OnDataLabelRender](#ondatalabelrender)
   - [OnLegendItemRender](#onlegenditemrender)
   - [TextRender](#textrender)
- [Selection Events](#selection-events)
   - [OnSelectionComplete](#onselectioncomplete)
   - [Selection Pattern](#selection-pattern)
- [Interaction Events](#interaction-events)
   - [OnLegendClick](#onlegendclick)
   - [TooltipRender](#tooltiprender)
   - [OnExportComplete](#onexportcomplete)
   - [OnPrintComplete](#onprintcomplete)
- [Event Patterns](#event-patterns)
   - [Cancellable Events](#cancellable-events)
   - [Event Chaining](#event-chaining)
- [Common Use Cases](#common-use-cases)
   - [Interactive Filtering](#interactive-filtering)
   - [Drill-Down](#drill-down)
   - [Real-Time Updates with Controlled Animation](#real-time-updates-with-controlled-animation)
   - [Conditional Styling](#conditional-styling)
- [Best Practices](#best-practices)
   - [Performance](#performance)
   - [User Experience](#user-experience)
   - [Maintainability](#maintainability)


## Animation

Control chart load and refresh animations for visual appeal and user engagement.

### Enable/Disable Animation

```razor
<AccumulationChartSeries DataSource="@Data" XName="Category" YName="Value">
    <AccumulationChartAnimation Enable="true" 
                                Duration="1500" 
                                Delay="0">
    </AccumulationChartAnimation>
</AccumulationChartSeries>
```

**Properties:**
- **Enable**: `true` (animated), `false` (instant render)
- **Duration**: Animation length in milliseconds (default: 1000ms)
- **Delay**: Wait time before starting (milliseconds)

### Animation Behavior

**On Load:**
- Slices/segments draw from center outward
- Smooth fade-in effect
- Sequential rendering feel

**On Refresh:**
- Smooth transition between old and new values
- Morphing animation for data changes

### Disable Animation on Programmatic Refresh

```razor
<SfAccumulationChart @ref="ChartRef">
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@Data" XName="X" YName="Y">
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
</SfAccumulationChart>

<button @onclick="RefreshChart">Refresh Chart</button>

@code {
    private SfAccumulationChart ChartRef;

    private async Task RefreshChart()
    {
        // Refresh without animation
        await ChartRef.Refresh(false);
    }
}
```

**When to disable animations:**
- Rapid data updates (real-time dashboards)
- Performance-critical scenarios
- Accessibility requirements (motion sensitivity)
- Testing and automation

### Custom Animation Timing

```razor
<!-- Slow, dramatic entrance -->
<AccumulationChartAnimation Enable="true" Duration="2000" Delay="500">
</AccumulationChartAnimation>

<!-- Quick, snappy animation -->
<AccumulationChartAnimation Enable="true" Duration="600" Delay="0">
</AccumulationChartAnimation>
```

## Chart Lifecycle Events

Events fired during chart initialization, rendering, and resize.

### OnLoad

Fires before chart rendering begins:

```razor
<AccumulationChartEvents OnLoad="ChartLoad">
</AccumulationChartEvents>

@code {
    private void ChartLoad(IAccumulationLoadedEventArgs args)
    {
        // Modify chart properties before rendering
        // Access args.AccumulationChart for chart instance
    }
}
```

**Use cases:**
- Dynamic theme application
- Loading external data
- Pre-render configuration

### Loaded

Fires after chart fully renders:

```razor
<AccumulationChartEvents Loaded="ChartLoaded">
</AccumulationChartEvents>

@code {
    private void ChartLoaded(IAccumulationLoadedEventArgs args)
    {
        Console.WriteLine("Chart rendering complete");
        // Perform post-render operations
    }
}
```

### BeforeResize / Resized

Track chart dimension changes:

```razor
<AccumulationChartEvents BeforeResize="OnBeforeResize" 
                         Resized="OnResized">
</AccumulationChartEvents>

@code {
    private void OnBeforeResize(IAccumulationResizeEventArgs args)
    {
        // Before resize starts
        // args.PreviousSize, args.CurrentSize
    }

    private void OnResized(IAccumulationResizeEventArgs args)
    {
        // After resize completes
        // Recalculate layout, adjust responsive behavior
    }
}
```

### SizeChanged

Alternative resize event:

```razor
<AccumulationChartEvents SizeChanged="OnSizeChanged">
</AccumulationChartEvents>

@code {
    private void OnSizeChanged(AccumulationResizeEventArgs args)
    {
        // args.CurrentSize.Height, args.CurrentSize.Width
    }
}
```

## Point and Series Events

Interact with individual data points and series.

### OnPointClick

User clicks a slice/segment:

```razor
<AccumulationChartEvents OnPointClick="PointClicked">
</AccumulationChartEvents>

@code {
    private void PointClicked(AccumulationPointEventArgs args)
    {
        string category = args.Point.X.ToString();
        double value = args.Point.Y;
        
        Console.WriteLine($"Clicked: {category} = {value}");
        
        // Navigate, show details, filter data, etc.
    }
}
```

**Event data:**
- `Point.X` - Category value
- `Point.Y` - Numeric value
- `Point.Index` - Point index in series
- `Point.Color` - Slice fill color

### OnPointMove

Mouse hovers over a point:

```razor
<AccumulationChartEvents OnPointMove="PointHovered">
</AccumulationChartEvents>

@code {
    private void PointHovered(AccumulationPointEventArgs args)
    {
        // Update external UI, preview data, etc.
        CurrentHoveredCategory = args.Point.X.ToString();
    }

    private string CurrentHoveredCategory = "";
}
```

### SeriesRender

Customize series before rendering:

```razor
<AccumulationChartEvents SeriesRender="OnSeriesRender">
</AccumulationChartEvents>

@code {
    private void OnSeriesRender(AccumulationSeriesRenderEventArgs args)
    {
        // Modify series properties
        // args.Series.InnerRadius, args.Series.Radius, etc.
    }
}
```

## Rendering Events

Customize visual elements during rendering.

### OnPointRender

Modify individual point appearance:

```razor
<AccumulationChartEvents OnPointRender="CustomizePoint">
</AccumulationChartEvents>

@code {
    private void CustomizePoint(AccumulationPointRenderEventArgs args)
    {
        // Conditional coloring
        if (args.Point.Y < 10)
        {
            args.Fill = "#ff0000";  // Red for low values
        }
        else if (args.Point.Y > 30)
        {
            args.Fill = "#00ff00";  // Green for high values
        }
        
        // Apply gradient
        args.Fill = new AccumulationChartLinearGradient { /* gradient config */ };
        
        // Set border
        args.Border = new { Width = 2, Color = "#000" };
    }
}
```

**Use cases:**
- Conditional formatting
- Per-point gradients
- Dynamic borders
- Highlighting specific data

### OnDataLabelRender

Customize data label appearance:

```razor
<AccumulationChartEvents OnDataLabelRender="CustomizeLabel">
</AccumulationChartEvents>

@code {
    private void CustomizeLabel(AccumulationTextRenderEventArgs args)
    {
        // Modify label text
        args.Text = $"{args.Point.X}: {args.Point.Y}%";
        
        // Conditional styling
        if (args.Point.Y > 30)
        {
            args.Color = "red";
            args.Font = new AccumulationChartFont { Size = "16px", FontWeight = "bold" };
        }
    }
}
```

### OnLegendItemRender

Customize legend items:

```razor
<AccumulationChartEvents OnLegendItemRender="CustomizeLegend">
</AccumulationChartEvents>

@code {
    private void CustomizeLegend(AccumulationLegendRenderEventArgs args)
    {
        // Modify legend text
        args.Text = $"{args.Text} ({args.Shape})";
        
        // Change legend shape
        args.Shape = LegendShape.Circle;
        
        // Conditional styling
        args.Fill = GetCategoryColor(args.Text);
    }
}
```

### TextRender

General text rendering event:

```razor
<AccumulationChartEvents TextRender="OnTextRender">
</AccumulationChartEvents>

@code {
    private void OnTextRender(AccumulationTextRenderEventArgs args)
    {
        // Apply to all chart text (title, labels, etc.)
    }
}
```

## Selection Events

Handle point/series selection.

### OnSelectionComplete

Fires after selection completes:

```razor
<SfAccumulationChart SelectionMode="Syncfusion.Blazor.Charts.AccumulationSelectionMode.Point">
    <AccumulationChartEvents OnSelectionComplete="SelectionMade">
    </AccumulationChartEvents>
    <AccumulationChartSeriesCollection>
        <AccumulationChartSeries DataSource="@Data" XName="X" YName="Y">
        </AccumulationChartSeries>
    </AccumulationChartSeriesCollection>
</SfAccumulationChart>

@code {
    private void SelectionMade(AccumulationSelectionCompleteEventArgs args)
    {
        // args.SelectedDataValues - array of selected points
        var selectedCategories = args.SelectedDataValues.Select(p => p.X).ToList();
        
        // Filter data, show details, update other components
    }
}
```

**Selection modes:**
- `Syncfusion.Blazor.Charts.AccumulationSelectionMode.Point` - Select individual slices
- `Syncfusion.Blazor.Charts.AccumulationSelectionMode.Series` - Select entire series

### Selection Pattern

```razor
<SfAccumulationChart SelectionMode="Syncfusion.Blazor.Charts.AccumulationSelectionMode.Point"
                     SelectionPattern="Syncfusion.Blazor.Charts.SelectionPattern.DiagonalForward"
                     HighlightMode="Syncfusion.Blazor.Charts.HighlightMode.Point"
                     HighlightPattern="Syncfusion.Blazor.Charts.SelectionPattern.Dots">
```

## Interaction Events

Track user interactions with the chart.

### OnLegendClick

User clicks legend item:

```razor
<AccumulationChartEvents OnLegendClick="LegendClicked">
</AccumulationChartEvents>

@code {
    private void LegendClicked(AccumulationLegendClickEventArgs args)
    {
        string legendText = args.LegendText;
        bool isVisible = args.LegendVisible;
        
        // Toggle visibility, filter data, navigate
        
        // Cancel default behavior
        args.Cancel = true;  // Prevent toggling visibility
    }
}
```

### TooltipRender

Customize tooltip before display:

```razor
<AccumulationChartEvents TooltipRender="CustomizeTooltip">
</AccumulationChartEvents>

@code {
    private void CustomizeTooltip(AccumulationTooltipRenderEventArgs args)
    {
        // Modify tooltip content
        args.Text = $"<b>{args.Point.X}</b><br/>Value: {args.Point.Y}<br/>Share: {args.Point.Percentage}%";
        
        // Change tooltip header
        args.HeaderText = "Sales Data";
        
        // Custom styling
        args.TextStyle = new AccumulationChartFont
        {
            Color = "#fff",
            Size = "14px",
            FontFamily = "Segoe UI"
        };
    }
}
```

### OnExportComplete

Fires after chart export finishes:

```razor
<AccumulationChartEvents OnExportComplete="ExportDone">
</AccumulationChartEvents>

@code {
    private void ExportDone(ExportEventArgs args)
    {
        Console.WriteLine($"Export completed: {args.Type}");
    }
}
```

### OnPrintComplete

Fires after print operation:

```razor
<AccumulationChartEvents OnPrintComplete="PrintDone">
</AccumulationChartEvents>

@code {
    private void PrintDone()
    {
        Console.WriteLine("Print completed");
    }
}
```

## Event Patterns

### Cancellable Events

Some events allow preventing default behavior:

```razor
@code {
    private void OnPointRender(AccumulationPointRenderEventArgs args)
    {
        if (args.Point.X == "Exclude")
        {
            args.Cancel = true;  // Don't render this point
        }
    }
}
```

### Event Chaining

Combine events for complex workflows:

```razor
<AccumulationChartEvents OnPointClick="PointClicked"
                         OnSelectionComplete="SelectionMade"
                         OnDataLabelRender="CustomizeLabel">
</AccumulationChartEvents>

@code {
    private void PointClicked(AccumulationPointEventArgs args)
    {
        SelectedPoint = args.Point;
    }

    private void SelectionMade(AccumulationSelectionCompleteEventArgs args)
    {
        UpdateDashboard(args.SelectedDataValues);
    }

    private void CustomizeLabel(AccumulationTextRenderEventArgs args)
    {
        if (SelectedPoint != null && args.Point.Index == SelectedPoint.Index)
        {
            args.Color = "red";  // Highlight selected point's label
        }
    }
}
```

## Common Use Cases

### Interactive Filtering

```razor
@code {
    private List<ChartData> FullData = /* all data */;
    private List<ChartData> FilteredData;

    private void PointClicked(AccumulationPointEventArgs args)
    {
        string category = args.Point.X.ToString();
        FilteredData = FullData.Where(d => d.Category == category).ToList();
        StateHasChanged();
    }
}
```

### Drill-Down

```razor
@code {
    private void PointClicked(AccumulationPointEventArgs args)
    {
        NavigationManager.NavigateTo($"/details/{args.Point.X}");
    }
}
```

### Real-Time Updates with Controlled Animation

```razor
@code {
    private async Task UpdateData()
    {
        Data = await FetchNewData();
        await ChartRef.Refresh(false);  // No animation for frequent updates
    }
}
```

### Conditional Styling

```razor
@code {
    private void CustomizePoint(AccumulationPointRenderEventArgs args)
    {
        if (args.Point.Y > Threshold)
        {
            args.Fill = "#00ff00";
            args.Border = new { Width = 3, Color = "#006600" };
        }
    }
}
```

## Best Practices

### Performance
- Avoid heavy computations in render events
- Use `Cancel = true` to skip unnecessary renders
- Throttle frequent updates
- Disable animation for rapid data changes

### User Experience
- Use animations for initial load (engaging)
- Disable for subsequent updates (clarity)
- Provide feedback on interactions
- Keep event handlers responsive

### Maintainability
- Separate event logic from UI code
- Use typed event args for IntelliSense
- Document complex event chains
- Test event scenarios thoroughly
