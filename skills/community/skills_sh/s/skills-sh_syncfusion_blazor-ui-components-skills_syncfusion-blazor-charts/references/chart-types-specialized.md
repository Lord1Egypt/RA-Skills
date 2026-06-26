# Specialized Blazor Chart Types Reference

A comprehensive guide to implementing specialized Syncfusion Blazor chart types including financial, statistical, stacked, range, polar, radar, scatter, and bubble charts. This document is self-contained with complete examples and best practices.

## Table of Contents

- [Financial Charts](#financial-charts)
   - [Candle Charts](#candle-charts)
   - [HILO Charts](#hilo-charts)
   - [HILOOC Charts](#hilooc-charts)
- [Statistical Charts](#statistical-charts)
   - [Box and Whisker](#box-and-whisker)
   - [Histogram](#histogram)
   - [Waterfall](#waterfall)
- [Stacked Charts](#stacked-charts)
   - [Stacked Area](#stacked-area)
   - [Stacked Column/Bar](#stacked-columnbar)
   - [Stacked Line](#stacked-line)
- [Range Charts](#range-charts)
   - [Range Area](#range-area)
   - [Range Column](#range-column)
   - [Range Step Area](#range-step-area)
   - [Spline Range Area](#spline-range-area)
- [Polar and Radar Charts](#polar-and-radar-charts)
- [Scatter and Bubble Charts](#scatter-and-bubble-charts)
   - [Scatter Chart](#scatter-chart)
   - [Bubble Chart](#bubble-chart)
- [Vertical Chart Orientation](#vertical-chart-orientation)
- [Best Practices](#best-practices)
   - [Empty Point Handling](#empty-point-handling)
   - [Series Customization Event](#series-customization-event)
   - [Point Customization Event](#point-customization-event)
   - [Gradient Fill](#gradient-fill)
- [Common Properties](#common-properties)
   - [All Chart Types Support:](#all-chart-types-support)
   - [Data Binding:](#data-binding)
- [Quick Reference](#quick-reference)


## Financial Charts

### Candle Charts

**Overview**: Candle charts display Low, High, Open, and Closing prices for financial data. Ideal for stock market analysis.

**Data Requirements**: Requires 5 fields - X (category/date), Open, High, Low, Close

**Basic Implementation**:
```cshtml
@using Syncfusion.Blazor.Charts

<SfChart>
    <ChartPrimaryXAxis ValueType="Syncfusion.Blazor.Charts.ValueType.Category" />
    
    <ChartSeriesCollection>
        <ChartSeries DataSource="@StockDetails" 
                     XName="X" 
                     High="High" 
                     Low="Low" 
                     Open="Open" 
                     Close="Close" 
                     Type="Syncfusion.Blazor.Charts.ChartSeriesType.Candle">
        </ChartSeries>
    </ChartSeriesCollection>
</SfChart>

@code {
    public class StockData
    {
        public string X { get; set; }
        public double Open { get; set; }
        public double High { get; set; }
        public double Low { get; set; }
        public double Close { get; set; }
    }

    public List<StockData> StockDetails = new List<StockData>
    {
        new StockData { X = "Jan", Open = 120, High = 160, Low = 100, Close = 140 },
        new StockData { X = "Feb", Open = 150, High = 190, Low = 130, Close = 170 },
        new StockData { X = "Mar", Open = 130, High = 170, Low = 110, Close = 150 },
        new StockData { X = "Apr", Open = 160, High = 180, Low = 120, Close = 140 },
        new StockData { X = "May", Open = 150, High = 170, Low = 110, Close = 130 }
    };
}
```

**Customization Options**:
- **BullFillColor**: Color when closing > opening (default: green)
- **BearFillColor**: Color when closing < opening (default: red)
- **EnableSolidCandles**: Fill candles based on open/close comparison

```cshtml
<ChartSeries BearFillColor="#e56590" 
             BullFillColor="#f8b883" 
             EnableSolidCandles="true"
             Type="Syncfusion.Blazor.Charts.ChartSeriesType.Candle">
</ChartSeries>
```

**Use Cases**:
- Stock price analysis
- Trading pattern visualization
- Market trend identification
- Financial forecasting

---

### HILO Charts

**Overview**: High-Low charts show the price range between high and low values.

**Data Requirements**: X, High, Low fields

```cshtml
<ChartSeries DataSource="@PriceData" 
             XName="Period" 
             High="HighPrice" 
             Low="LowPrice" 
             Type="Syncfusion.Blazor.Charts.ChartSeriesType.Hilo">
</ChartSeries>
```

---

### HILOOC Charts

**Overview**: High-Low-Open-Close charts display four price points with opening and closing ticks.

**Data Requirements**: X, High, Low, Open, Close fields

```cshtml
<ChartSeries DataSource="@StockPrices" 
             XName="Date" 
             High="High" 
             Low="Low" 
             Open="Open" 
             Close="Close" 
             Type="Syncfusion.Blazor.Charts.ChartSeriesType.HiloOpenClose">
</ChartSeries>
```

---

## Statistical Charts

### Box and Whisker

**Overview**: Visualizes statistical distribution showing minimum, maximum, median, quartiles, and outliers.

**Data Requirements**: YName requires array of values (minimum 5 values per point)

**Complete Implementation**:
```cshtml
<SfChart>
    <ChartPrimaryXAxis ValueType="Syncfusion.Blazor.Charts.ValueType.Category" />
    
    <ChartSeriesCollection>
        <ChartSeries DataSource="@StatisticalData" 
                     XName="Category" 
                     YName="Values" 
                     Type="Syncfusion.Blazor.Charts.ChartSeriesType.BoxAndWhisker"
                     BoxPlotMode="BoxPlotMode.Normal"
                     ShowMean="true">
        </ChartSeries>
    </ChartSeriesCollection>
</SfChart>

@code {
    public class BoxWhiskerData
    {
        public string Category { get; set; }
        public double[] Values { get; set; }
    }

    public List<BoxWhiskerData> StatisticalData = new List<BoxWhiskerData>
    {
        new BoxWhiskerData { 
            Category = "Development", 
            Values = new double[] { 22, 23, 25, 26, 27, 28, 29, 30, 32, 34 } 
        },
        new BoxWhiskerData { 
            Category = "Testing", 
            Values = new double[] { 22, 23, 25, 26, 28, 29, 30, 33, 34 } 
        }
    };
}
```

**BoxPlotMode Options**:
- **Normal**: Standard quartile calculation
- **Exclusive**: Excludes median from quartile calculation
- **Inclusive**: Includes median in quartile calculation

**Use Cases**:
- Statistical analysis
- Quality control metrics
- Performance comparison
- Outlier detection

---

### Histogram

**Overview**: Displays frequency distribution of continuous data in bins.

**Data Requirements**: YName only (automatically calculates bins)

```cshtml
<ChartSeries DataSource="@ExamScores" 
             YName="Score" 
             Type="Syncfusion.Blazor.Charts.ChartSeriesType.Histogram" 
             BinInterval="20"
             ShowNormalDistribution="true"
             ColumnWidth="0.99">
    <ChartMarker Visible="true" Height="10" Width="10">
        <ChartDataLabel Visible="true" Position="LabelPosition.Top" />
    </ChartMarker>
</ChartSeries>

@code {
    public class ScoreData
    {
        public double Score { get; set; }
    }

    public List<ScoreData> ExamScores = new List<ScoreData>
    {
        new ScoreData { Score = 5.25 },
        new ScoreData { Score = 36.25 },
        new ScoreData { Score = 46.25 },
        new ScoreData { Score = 66.50 },
        new ScoreData { Score = 80.00 }
    };
}
```

---

### Waterfall

**Overview**: Shows cumulative effect of sequential positive/negative values.

**Data Requirements**: XName, YName with IntermediateSumIndexes and SumIndexes

**Complete Example**:
```cshtml
<SfChart>
    <ChartPrimaryXAxis ValueType="Syncfusion.Blazor.Charts.ValueType.Category" />
    
    <ChartSeriesCollection>
        <ChartSeries DataSource="@FinancialData" 
                     XName="Category" 
                     YName="Value" 
                     Type="Syncfusion.Blazor.Charts.ChartSeriesType.Waterfall"
                     IntermediateSumIndexes="@intermediateIndexes"
                     SumIndexes="@sumIndexes"
                     NegativeFillColor="#f8b883"
                     SummaryFillColor="#e56590">
            <ChartCornerRadius TopLeft="5" TopRight="5" />
        </ChartSeries>
    </ChartSeriesCollection>
</SfChart>

@code {
    double[] intermediateIndexes = new double[] { 4 };
    double[] sumIndexes = new double[] { 7 };

    public class WaterfallData
    {
        public string Category { get; set; }
        public double Value { get; set; }
    }

    public List<WaterfallData> FinancialData = new List<WaterfallData>
    {
        new WaterfallData { Category = "Income", Value = 4711 },
        new WaterfallData { Category = "Sales", Value = -1015 },
        new WaterfallData { Category = "Development", Value = -688 },
        new WaterfallData { Category = "Revenue", Value = 1030 },
        new WaterfallData { Category = "Balance", Value = 0 },
        new WaterfallData { Category = "Expense", Value = -361 },
        new WaterfallData { Category = "Tax", Value = -695 },
        new WaterfallData { Category = "Net Profit", Value = 0 }
    };
}
```

**Use Cases**:
- Financial analysis
- Profit/loss breakdown
- Budget variance tracking
- Cash flow visualization

---

## Stacked Charts

### Stacked Area

**Overview**: Shows contribution of multiple series to total over time.

**Multi-Series Implementation**:
```cshtml
<SfChart>
    <ChartPrimaryXAxis ValueType="Syncfusion.Blazor.Charts.ValueType.Category" />
    
    <ChartSeriesCollection>
        <ChartSeries DataSource="@RevenueData" 
                     XName="Year" 
                     YName="ProductA" 
                     Name="Product A"
                     Fill="red" 
                     Opacity="0.7"
                     Type="Syncfusion.Blazor.Charts.ChartSeriesType.StackingArea">
            <ChartSeriesBorder Width="2" Color="black" />
        </ChartSeries>
        
        <ChartSeries DataSource="@RevenueData" 
                     XName="Year" 
                     YName="ProductB" 
                     Name="Product B"
                     Fill="blue" 
                     Opacity="0.7"
                     Type="Syncfusion.Blazor.Charts.ChartSeriesType.StackingArea">
            <ChartSeriesBorder Width="2" Color="black" />
        </ChartSeries>
        
        <ChartSeries DataSource="@RevenueData" 
                     XName="Year" 
                     YName="ProductC" 
                     Name="Product C"
                     Fill="green" 
                     Opacity="0.7"
                     Type="Syncfusion.Blazor.Charts.ChartSeriesType.StackingArea">
            <ChartSeriesBorder Width="2" Color="black" />
        </ChartSeries>
    </ChartSeriesCollection>
    
    <ChartStackLabelSettings Visible="true" Format="{value}" Fill="#ADD8E6">
        <ChartStackLabelFont FontWeight="600" Color="blue" />
    </ChartStackLabelSettings>
</SfChart>

@code {
    public class StackedData
    {
        public double Year { get; set; }
        public double ProductA { get; set; }
        public double ProductB { get; set; }
        public double ProductC { get; set; }
    }

    public List<StackedData> RevenueData = new List<StackedData>
    {
        new StackedData { Year = 2020, ProductA = 0.61, ProductB = 0.03, ProductC = 0.48 },
        new StackedData { Year = 2021, ProductA = 0.81, ProductB = 0.05, ProductC = 0.53 },
        new StackedData { Year = 2022, ProductA = 0.91, ProductB = 0.06, ProductC = 0.57 }
    };
}
```

**Stack Labels**: Display cumulative totals with `ChartStackLabelSettings`

---

### Stacked Column/Bar

**Similar to Stacked Area but with columns/bars**:
```cshtml
<ChartSeries Type="Syncfusion.Blazor.Charts.ChartSeriesType.StackingColumn" />
<ChartSeries Type="Syncfusion.Blazor.Charts.ChartSeriesType.StackingBar" />
```

---

### Stacked Line

```cshtml
<ChartSeries Type="Syncfusion.Blazor.Charts.ChartSeriesType.StackingLine" Width="2" />
```

---

## Range Charts

### Range Area

**Overview**: Shows variation between high and low values over time.

**Data Requirements**: XName, High, Low

```cshtml
<SfChart>
    <ChartPrimaryXAxis ValueType="Syncfusion.Blazor.Charts.ValueType.Category" />
    
    <ChartSeriesCollection>
        <ChartSeries DataSource="@TemperatureData" 
                     XName="Day" 
                     High="MaxTemp" 
                     Low="MinTemp" 
                     Type="Syncfusion.Blazor.Charts.ChartSeriesType.RangeArea"
                     Fill="blue"
                     Opacity="0.5">
            <ChartSeriesBorder Width="2" Color="red" />
        </ChartSeries>
    </ChartSeriesCollection>
</SfChart>

@code {
    public class RangeData
    {
        public string Day { get; set; }
        public double MinTemp { get; set; }
        public double MaxTemp { get; set; }
    }

    public List<RangeData> TemperatureData = new List<RangeData>
    {
        new RangeData { Day = "Mon", MinTemp = 2.5, MaxTemp = 9.8 },
        new RangeData { Day = "Tue", MinTemp = 4.7, MaxTemp = 11.4 },
        new RangeData { Day = "Wed", MinTemp = 6.4, MaxTemp = 14.4 }
    };
}
```

**Use Cases**:
- Temperature ranges
- Price fluctuations
- Performance bounds
- Forecast intervals

---

### Range Column

```cshtml
<ChartSeries Type="Syncfusion.Blazor.Charts.ChartSeriesType.RangeColumn" 
             XName="Category" 
             High="Upper" 
             Low="Lower" />
```

---

### Range Step Area

```cshtml
<ChartSeries Type="Syncfusion.Blazor.Charts.ChartSeriesType.RangeStepArea" 
             XName="X" 
             High="High" 
             Low="Low" />
```

---

### Spline Range Area

**Smooth curves for range visualization**:
```cshtml
<ChartSeries Type="Syncfusion.Blazor.Charts.ChartSeriesType.SplineRangeArea" 
             XName="Month" 
             High="HighValue" 
             Low="LowValue" />
```

---

## Polar and Radar Charts

**Overview**: Display data on circular axes. Polar uses numeric/category axis, Radar uses radial axis.

**Polar with Multiple Draw Types**:
```cshtml
<SfChart>
    <ChartSeriesCollection>
        <!-- Polar Line -->
        <ChartSeries DataSource="@CircularData" 
                     XName="X" 
                     YName="Y" 
                     Type="Syncfusion.Blazor.Charts.ChartSeriesType.Polar"
                     DrawType="ChartDrawType.Line"
                     IsClosed="true"
                     Width="2">
            <ChartMarker Visible="true" Height="10" Width="10" />
        </ChartSeries>
    </ChartSeriesCollection>
</SfChart>

@code {
    public class PolarData
    {
        public double X { get; set; }
        public double Y { get; set; }
    }

    public List<PolarData> CircularData = new List<PolarData>
    {
        new PolarData { X = 2005, Y = 28 },
        new PolarData { X = 2006, Y = 25 },
        new PolarData { X = 2007, Y = 26 }
    };
}
```

**Draw Type Options**:
- Line
- Spline
- Area
- Column
- StackingArea
- StackingColumn
- RangeColumn
- Scatter

**Radar Chart**:
```cshtml
<ChartSeries Type="Syncfusion.Blazor.Charts.ChartSeriesType.Radar" 
             DrawType="ChartDrawType.Area" />
```

**Customization**:
- **StartAngle**: Rotation angle (default: 0)
- **Coefficient**: Radius size (default: 100)

```cshtml
<ChartPrimaryXAxis StartAngle="270" Coefficient="80" />
```

---

## Scatter and Bubble Charts

### Scatter Chart

**Overview**: Plots individual data points to show correlation between two variables.

```cshtml
<SfChart>
    <ChartPrimaryXAxis ValueType="Syncfusion.Blazor.Charts.ValueType.Category" />
    
    <ChartSeriesCollection>
        <ChartSeries DataSource="@ScatterData" 
                     XName="Country" 
                     YName="GoldMedals" 
                     Type="Syncfusion.Blazor.Charts.ChartSeriesType.Scatter"
                     Fill="green"
                     Opacity="0.5">
            <ChartMarker Height="10" Width="10" Shape="ChartShape.Triangle" />
        </ChartSeries>
        
        <ChartSeries DataSource="@ScatterData" 
                     XName="Country" 
                     YName="SilverMedals" 
                     Type="Syncfusion.Blazor.Charts.ChartSeriesType.Scatter"
                     Fill="blue"
                     Opacity="0.5">
            <ChartMarker Height="10" Width="10" Shape="ChartShape.Rectangle" />
        </ChartSeries>
    </ChartSeriesCollection>
</SfChart>
```

---

### Bubble Chart

**Overview**: Three-dimensional scatter chart where bubble size represents third parameter.

**Data Requirements**: XName, YName, Size

```cshtml
<SfChart>
    <ChartSeriesCollection>
        <ChartSeries DataSource="@PopulationData" 
                     XName="LiteracyRate" 
                     YName="GrowthRate" 
                     Size="Population"
                     Type="Syncfusion.Blazor.Charts.ChartSeriesType.Bubble"
                     Fill="blue"
                     Opacity="0.5">
        </ChartSeries>
    </ChartSeriesCollection>
</SfChart>

@code {
    public class BubbleData
    {
        public double LiteracyRate { get; set; }
        public double GrowthRate { get; set; }
        public double Population { get; set; }
        public string Country { get; set; }
    }

    public List<BubbleData> PopulationData = new List<BubbleData>
    {
        new BubbleData { LiteracyRate = 92.2, GrowthRate = 7.8, Population = 1.347, Country = "China" },
        new BubbleData { LiteracyRate = 74, GrowthRate = 6.5, Population = 1.241, Country = "India" }
    };
}
```

---

## Vertical Chart Orientation

**Apply to any chart type**:
```cshtml
<SfChart IsTransposed="true">
    <ChartSeriesCollection>
        <ChartSeries DataSource="@Data" 
                     XName="X" 
                     YName="Y" 
                     Type="Syncfusion.Blazor.Charts.ChartSeriesType.Spline" />
    </ChartSeriesCollection>
</SfChart>
```

---

## Best Practices

### Empty Point Handling
```cshtml
<ChartEmptyPointSettings Mode="EmptyPointMode.Average" Fill="#FFDE59">
    <ChartEmptyPointBorder Color="red" Width="2" />
</ChartEmptyPointSettings>
```

### Series Customization Event
```cshtml
<ChartEvents OnSeriesRender="SeriesRender" />

@code {
    void SeriesRender(SeriesRenderEventArgs args)
    {
        args.Fill = "#FF4081";
    }
}
```

### Point Customization Event
```cshtml
<ChartEvents OnPointRender="PointRender" />

@code {
    void PointRender(PointRenderEventArgs args)
    {
        args.Fill = (args.Point.Index % 2 != 0) ? "#ff6347" : "#009cb8";
    }
}
```

### Gradient Fill
```cshtml
<ChartSeries Fill="url(#grad1)" />

<svg style="height: 0">
    <defs>
        <linearGradient id="grad1" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="20%" style="stop-color:orange;stop-opacity:1" />
            <stop offset="100%" style="stop-color:black;stop-opacity:1" />
        </linearGradient>
    </defs>
</svg>
```

---

## Common Properties

### All Chart Types Support:
- **Fill**: Series color
- **Opacity**: Transparency (0-1)
- **DashArray**: Border pattern
- **ChartSeriesBorder**: Border width and color
- **ChartMarker**: Data point markers
- **ChartDataLabel**: Label customization
- **ChartEmptyPointSettings**: Handling null values

### Data Binding:
- Use `DataSource` property
- Map fields with `XName`, `YName`, `High`, `Low`, etc.
- Supports `SfDataManager` for remote data

---

## Quick Reference

| Chart Type | Data Fields | Use Case |
|------------|-------------|----------|
| Candle | X, Open, High, Low, Close | Stock analysis |
| Box-Whisker | X, Y (array) | Statistical distribution |
| Histogram | Y only | Frequency distribution |
| Waterfall | X, Y, indexes | Financial breakdown |
| Stacked Area | X, Y (multiple) | Contribution analysis |
| Range Area | X, High, Low | Value ranges |
| Polar | X, Y + DrawType | Circular data |
| Scatter | X, Y | Correlation |
| Bubble | X, Y, Size | 3D relationships |

---

**Document Version**: 1.0  
**Last Updated**: March 2026  
**Total Lines**: ~390
