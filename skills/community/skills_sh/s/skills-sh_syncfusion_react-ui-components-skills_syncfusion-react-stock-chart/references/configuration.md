# Chart Configuration: Axes, Dimensions, Appearance, and Gradients

Comprehensive guide for configuring Stock Chart axes, controlling dimensions, customizing appearance with themes, and applying gradient fills.

> See the concise API summary in [API Reference](./api.md) for prop/method/event names and quick examples.

**Additional StockChart features covered (from API):**
- `enableCustomRange`, `enablePersistence`, `enableRtl`, `zoomSettings`, `selectionMode`, `enablePeriodSelector`, `enableSelector`

**Quick link:** Full API summary: [references/api.md](./api.md)

## Table of Contents
- [Axes Configuration](#axes-configuration)
  - [Axis Types](#axis-types)
  - [DateTime Axis](#datetime-axis-configuration)
  - [Numeric Axis](#numeric-axis-configuration)
  - [Axis Customization](#axis-customization)
  - [Multiple Axes](#multiple-axes)
- [Chart Dimensions](#chart-dimensions)
  - [Container-Based Sizing](#container-based-sizing)
  - [Direct Sizing](#direct-sizing-width-and-height)
  - [Responsive Design](#responsive-design)
- [Appearance](#appearance-and-theming)
  - [Chart Title](#chart-title)
  - [Built-in Themes](#built-in-themes)
  - [Background and Border](#background-and-border)
  - [Chart Area Customization](#chart-area-customization)
- [Gradient Fills](#gradient-fills)
  - [Linear Gradients](#linear-gradients)
  - [Radial Gradients](#radial-gradients)

## Axes Configuration

### Axis Types

Stock Chart supports four axis types:

1. **DateTime** - For date/time data (most common for stock charts)
2. **Numeric** - For numerical data
3. **Logarithmic** - For logarithmic scales
4. **Category** - For categorical data

### DateTime Axis Configuration

DateTime axis is essential for stock charts as it handles date-based data:

```typescript
import { 
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  Inject,
  DateTime,
  CandleSeries
} from '@syncfusion/ej2-react-charts';

function DateTimeAxisChart() {
  const stockData = [
    { x: new Date('2012-04-02'), open: 320.71, high: 324.07, low: 317.74, close: 323.78 },
    { x: new Date('2012-04-03'), open: 323.03, high: 324.30, low: 319.64, close: 321.63 },
    // More data...
  ];

  return (
    <StockChartComponent
      id='stockchart'
      primaryXAxis={{ 
        valueType: 'DateTime',  // Essential for date-based data
        title: 'Date',
        labelFormat: 'MMM yyyy'
      }}
      primaryYAxis={{
        title: 'Price ($)',
        labelFormat: '${value}'
      }}
    >
      <Inject services={[DateTime, CandleSeries]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={stockData}
          type='Candle'
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
```

**DateTime axis properties:**
- `valueType: 'DateTime'` - Sets axis to handle dates
- `labelFormat` - Date format string (e.g., 'MMM dd, yyyy', 'dd/MM/yyyy')
- `intervalType` - 'Auto', 'Years', 'Months', 'Days', 'Hours', 'Minutes'
- `interval` - Interval between labels

### Numeric Axis Configuration

Numeric axis for price values:

```typescript
<StockChartComponent
  primaryYAxis={{
    valueType: 'Double',  // Numeric axis (default)
    title: 'Stock Price',
    minimum: 300,
    maximum: 400,
    interval: 20,
    labelFormat: '${value}',
    rangePadding: 'Additional'
  }}
>
  {/* ... */}
</StockChartComponent>
```

**Numeric axis properties:**
- `minimum` - Minimum axis value
- `maximum` - Maximum axis value
- `interval` - Interval between labels
- `labelFormat` - Format string for labels
- `rangePadding` - 'None', 'Normal', 'Additional', 'Round', 'Auto'

### Axis Customization

#### Label Formatting

```typescript
// Currency format
primaryYAxis={{
  labelFormat: '${value}',
  title: 'Price (USD)'
}}

// Percentage format
primaryYAxis={{
  labelFormat: '{value}%',
  title: 'Change (%)'
}}

// Custom format
primaryYAxis={{
  labelFormat: 'Price: {value}',
  title: 'Stock Price'
}}
```

#### Axis Range

Set explicit ranges:

```typescript
primaryYAxis={{
  minimum: 100,
  maximum: 200,
  interval: 10
}}
```

#### Axis Title

```typescript
primaryXAxis={{
  valueType: 'DateTime',
  title: 'Trading Date',
  titleStyle: {
    fontFamily: 'Arial',
    fontSize: '14px',
    fontWeight: 'bold',
    color: '#333333'
  }
}}
```

#### Grid Lines

Customize grid appearance:

```typescript
primaryYAxis={{
  majorGridLines: {
    width: 1,
    color: '#e0e0e0',
    dashArray: '5,5'
  },
  minorGridLines: {
    width: 0.5,
    color: '#f0f0f0',
    dashArray: '3,3'
  },
  minorTicksPerInterval: 5
}}
```

#### Axis Line

Customize axis line:

```typescript
primaryYAxis={{
  lineStyle: {
    width: 2,
    color: '#000000',
    dashArray: '0'
  }
}}
```

### Multiple Axes

Add multiple Y-axes for different value scales:

```typescript
import { 
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  StockChartAxisDirective,
  StockChartAxesDirective,
  Inject,
  DateTime,
  LineSeries,
  ColumnSeries
} from '@syncfusion/ej2-react-charts';

function MultipleAxesChart() {
  const priceData = [ /* price data */ ];
  const volumeData = [ /* volume data */ ];

  return (
    <StockChartComponent
      id='stockchart'
      primaryXAxis={{ valueType: 'DateTime' }}
      primaryYAxis={{
        title: 'Price ($)',
        labelFormat: '${value}'
      }}
    >
      <Inject services={[DateTime, LineSeries, ColumnSeries]} />
      
      {/* Additional Y-axis for volume */}
      <StockChartAxesDirective>
        <StockChartAxisDirective
          name='volumeAxis'
          opposedPosition={true}
          title='Volume'
          labelFormat='{value}M'
          majorGridLines={{ width: 0 }}
        />
      </StockChartAxesDirective>
      
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={priceData}
          type='Line'
          yAxisName='primaryYAxis'  // Uses primary Y-axis
        />
        <StockChartSeriesDirective
          dataSource={volumeData}
          type='Column'
          yAxisName='volumeAxis'  // Uses volume axis
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
```

### Complete Axis Configuration Example

```typescript
function ComprehensiveAxisChart() {
  const stockData = [ /* data */ ];

  return (
    <StockChartComponent
      id='stockchart'
      title='Stock Price Analysis'
      primaryXAxis={{
        valueType: 'DateTime',
        title: 'Trading Date',
        labelFormat: 'MMM dd',
        intervalType: 'Days',
        interval: 5,
        majorGridLines: {
          width: 1,
          color: '#e0e0e0'
        },
        minorGridLines: {
          width: 0.5,
          color: '#f5f5f5'
        },
        lineStyle: {
          width: 1,
          color: '#333333'
        },
        titleStyle: {
          fontSize: '14px',
          fontWeight: 'bold'
        }
      }}
      primaryYAxis={{
        title: 'Price (USD)',
        labelFormat: '${value}',
        minimum: 300,
        maximum: 400,
        interval: 20,
        rangePadding: 'Additional',
        majorGridLines: {
          width: 1,
          color: '#e0e0e0',
          dashArray: '5,5'
        },
        lineStyle: {
          width: 1,
          color: '#333333'
        },
        titleStyle: {
          fontSize: '14px',
          fontWeight: 'bold'
        }
      }}
    >
      <Inject services={[DateTime, CandleSeries]} />
      {/* ... series ... */}
    </StockChartComponent>
  );
}
```

## Chart Dimensions

### Container-Based Sizing

Chart automatically sizes to its container:

```typescript
// HTML container
<div id="chart-container" style={{ width: '800px', height: '450px' }}>
  <StockChartComponent id='stockchart'>
    {/* Chart inherits container dimensions */}
  </StockChartComponent>
</div>
```

```typescript
// React component with styled container
function ContainerSizedChart() {
  return (
    <div style={{ width: '100%', height: '500px', padding: '20px' }}>
      <StockChartComponent id='stockchart'>
        <Inject services={[DateTime, CandleSeries]} />
        {/* ... */}
      </StockChartComponent>
    </div>
  );
}
```

### Direct Sizing (Width and Height)

Set chart size directly using `width` and `height` properties:

**Pixel sizing:**
```typescript
<StockChartComponent
  id='stockchart'
  width='800px'
  height='450px'
>
  {/* ... */}
</StockChartComponent>
```

**Percentage sizing:**
```typescript
<StockChartComponent
  id='stockchart'
  width='100%'   // 100% of container width
  height='80%'   // 80% of container height
>
  {/* ... */}
</StockChartComponent>
```

**Mixed sizing:**
```typescript
<StockChartComponent
  id='stockchart'
  width='1200px'  // Fixed width
  height='60%'    // Percentage height
>
  {/* ... */}
</StockChartComponent>
```

**Default size:** When not specified, chart uses `450px` height and window width.

### Responsive Design

Create responsive charts:

```typescript
function ResponsiveChart() {
  return (
    <div className="chart-container" style={{
      width: '100%',
      height: '100vh',
      maxWidth: '1400px',
      minHeight: '400px',
      margin: '0 auto',
      padding: '20px'
    }}>
      <StockChartComponent
        id='stockchart'
        width='100%'
        height='90%'
      >
        {/* ... */}
      </StockChartComponent>
    </div>
  );
}
```

**Responsive patterns:**
```typescript
// Full viewport
width='100vw' height='100vh'

// Card/panel sizing
width='100%' height='400px'

// Aspect ratio
width='100%' height='56.25%'  // 16:9 aspect ratio

// Media query with React state
const [chartSize, setChartSize] = useState({ width: '1200px', height: '600px' });
```

## Appearance and Theming

### Chart Title

Add and customize chart title:

```typescript
<StockChartComponent
  title='AAPL Stock Price Analysis'
  titleStyle={{
    fontFamily: 'Arial, sans-serif',
    fontSize: '18px',
    fontWeight: 'bold',
    color: '#333333',
    textAlignment: 'Center',
    textOverflow: 'Wrap'
  }}
>
  {/* ... */}
</StockChartComponent>
```

**Title style properties:**
- `fontFamily` - Font family
- `fontSize` - Font size (e.g., '16px', '1.2em')
- `fontWeight` - 'normal', 'bold', '400', '700'
- `color` - Text color
- `textAlignment` - 'Near', 'Center', 'Far'
- `textOverflow` - 'None', 'Wrap', 'Trim'

### Built-in Themes

Stock Chart ships with 9 built-in themes:

```typescript
<StockChartComponent
  theme='Material'  // Choose from available themes
>
  {/* ... */}
</StockChartComponent>
```

**Available themes:**
1. **Material** - Google Material Design
2. **MaterialDark** - Material dark theme
3. **Fabric** - Microsoft Fabric Design
4. **FabricDark** - Fabric dark theme
5. **Bootstrap** - Bootstrap styling
6. **Bootstrap4** - Bootstrap 4 styling
7. **BootstrapDark** - Bootstrap dark theme
8. **HighContrast** - High contrast for accessibility
9. **HighContrastLight** - Light high contrast

**Theme examples:**
```typescript
// Material theme
<StockChartComponent theme='Material'>

// Dark theme for dashboards
<StockChartComponent theme='MaterialDark'>

// High contrast for accessibility
<StockChartComponent theme='HighContrast'>
```

### Background and Border

Customize chart background and border:

```typescript
<StockChartComponent
  background='#f9f9f9'  // Background color
  border={{
    width: 2,
    color: '#dddddd'
  }}
  margin={{
    left: 40,
    right: 40,
    top: 40,
    bottom: 40
  }}
>
  {/* ... */}
</StockChartComponent>
```

### Chart Area Customization

Customize the chart plotting area:

```typescript
<StockChartComponent
  chartArea={{
    background: '#ffffff',
    border: {
      width: 1,
      color: '#e0e0e0'
    }
  }}
>
  {/* ... */}
</StockChartComponent>
```

### Complete Appearance Example

```typescript
function StyledChart() {
  const stockData = [ /* data */ ];

  return (
    <StockChartComponent
      id='stockchart'
      title='Professional Stock Analysis'
      titleStyle={{
        fontFamily: '"Segoe UI", Arial, sans-serif',
        fontSize: '20px',
        fontWeight: 'bold',
        color: '#1a1a1a'
      }}
      theme='Material'
      background='#fafafa'
      border={{
        width: 1,
        color: '#e0e0e0'
      }}
      margin={{
        left: 50,
        right: 50,
        top: 50,
        bottom: 50
      }}
      chartArea={{
        background: '#ffffff',
        border: {
          width: 1,
          color: '#e8e8e8'
        }
      }}
      primaryXAxis={{
        valueType: 'DateTime',
        majorGridLines: { color: '#f0f0f0' }
      }}
      primaryYAxis={{
        majorGridLines: { color: '#f0f0f0', dashArray: '5,5' }
      }}
    >
      <Inject services={[DateTime, CandleSeries]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={stockData}
          type='Candle'
          bearFillColor='#ef5350'
          bullFillColor='#26a69a'
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
```

## Gradient Fills

Apply gradient fills to series for enhanced visual appeal.

### Linear Gradients

Linear gradients transition colors along a line:

```typescript
import { 
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  Inject,
  DateTime,
  AreaSeries
} from '@syncfusion/ej2-react-charts';

function LinearGradientChart() {
  const stockData = [ /* data */ ];

  const linearGradient = {
    id: 'gradient1',
    x1: '0%',
    y1: '0%',
    x2: '0%',
    y2: '100%',
    stops: [
      { offset: '0%', color: 'rgba(0, 128, 255, 0.9)' },
      { offset: '100%', color: 'rgba(0, 128, 255, 0.1)' }
    ]
  };

  return (
    <StockChartComponent
      id='stockchart'
      primaryXAxis={{ valueType: 'DateTime' }}
    >
      <Inject services={[DateTime, AreaSeries]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={stockData}
          type='Area'
          xName='x'
          yName='close'
          fill='url(#gradient1)'
          border={{ width: 2, color: '#0080ff' }}
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
```

**Linear gradient configuration:**
- `x1, y1` - Start point (0%-100%)
- `x2, y2` - End point (0%-100%)
- `stops` - Color stops array
  - `offset` - Position (0%-100%)
  - `color` - Color at that position

**Gradient directions:**
```typescript
// Vertical (top to bottom)
{ x1: '0%', y1: '0%', x2: '0%', y2: '100%' }

// Horizontal (left to right)
{ x1: '0%', y1: '0%', x2: '100%', y2: '0%' }

// Diagonal
{ x1: '0%', y1: '0%', x2: '100%', y2: '100%' }
```

### Radial Gradients

Radial gradients radiate from a center point:

```typescript
function RadialGradientChart() {
  const stockData = [ /* data */ ];

  const radialGradient = {
    id: 'gradient2',
    cx: '50%',
    cy: '50%',
    r: '50%',
    stops: [
      { offset: '0%', color: 'rgba(255, 128, 0, 0.9)' },
      { offset: '100%', color: 'rgba(255, 128, 0, 0.2)' }
    ]
  };

  return (
    <StockChartComponent
      id='stockchart'
      primaryXAxis={{ valueType: 'DateTime' }}
    >
      <Inject services={[DateTime, AreaSeries]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={stockData}
          type='Area'
          fill='url(#gradient2)'
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
```

**Radial gradient configuration:**
- `cx, cy` - Center point (0%-100%)
- `r` - Radius (0%-100%)
- `stops` - Color stops array

### Multiple Series with Gradients

```typescript
function MultiGradientChart() {
  const series1Data = [ /* data */ ];
  const series2Data = [ /* data */ ];

  return (
    <StockChartComponent
      id='stockchart'
      primaryXAxis={{ valueType: 'DateTime' }}
    >
      <Inject services={[DateTime, AreaSeries]} />
      <StockChartSeriesCollectionDirective>
        {/* Blue gradient series */}
        <StockChartSeriesDirective
          dataSource={series1Data}
          type='Area'
          fill='url(#blueGradient)'
          name='Series 1'
        />
        {/* Orange gradient series */}
        <StockChartSeriesDirective
          dataSource={series2Data}
          type='Area'
          fill='url(#orangeGradient)'
          name='Series 2'
          opacity={0.7}
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
```

### Complete Gradient Example

```typescript
function ComprehensiveGradientChart() {
  const stockData = [
    { x: new Date('2012-01-01'), close: 125.50 },
    { x: new Date('2012-02-01'), close: 132.30 },
    { x: new Date('2012-03-01'), close: 145.00 },
    { x: new Date('2012-04-01'), close: 138.75 },
    { x: new Date('2012-05-01'), close: 152.25 }
  ];

  return (
    <div>
      <svg style={{ height: 0 }}>
        <defs>
          <linearGradient id="priceGradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" style={{ stopColor: 'rgba(0, 128, 255, 0.9)', stopOpacity: 1 }} />
            <stop offset="50%" style={{ stopColor: 'rgba(0, 128, 255, 0.5)', stopOpacity: 1 }} />
            <stop offset="100%" style={{ stopColor: 'rgba(0, 128, 255, 0.1)', stopOpacity: 1 }} />
          </linearGradient>
        </defs>
      </svg>
      
      <StockChartComponent
        id='stockchart'
        title='Stock Price with Gradient Fill'
        primaryXAxis={{ valueType: 'DateTime' }}
        primaryYAxis={{ title: 'Price ($)' }}
      >
        <Inject services={[DateTime, AreaSeries]} />
        <StockChartSeriesCollectionDirective>
          <StockChartSeriesDirective
            dataSource={stockData}
            type='Area'
            xName='x'
            yName='close'
            fill='url(#priceGradient)'
            border={{ width: 3, color: '#0080ff' }}
            opacity={1}
          />
        </StockChartSeriesCollectionDirective>
      </StockChartComponent>
    </div>
  );
}

export default ComprehensiveGradientChart;
```

## Best Practices

**Axes:**
- Always use DateTime axis for stock data
- Set meaningful axis titles
- Format labels for readability ($, %, etc.)
- Use appropriate ranges to avoid distortion
- Enable grid lines for easier value reading

**Dimensions:**
- Use percentage sizing for responsive layouts
- Set minimum dimensions for readability (min 400px height)
- Test on different screen sizes
- Consider 16:9 or 4:3 aspect ratios

**Appearance:**
- Choose themes consistent with your application
- Use high contrast themes for accessibility
- Keep backgrounds subtle to focus on data
- Maintain consistent styling across charts

**Gradients:**
- Use gradients sparingly for visual appeal
- Ensure gradients don't obscure data readability
- Use semi-transparent gradients for area charts
- Test gradient visibility across themes

**Performance:**
- Theming has no performance impact
- Complex gradients may slightly affect rendering
- Minimize re-renders by memoizing configurations
- Use appropriate intervals for large date ranges
