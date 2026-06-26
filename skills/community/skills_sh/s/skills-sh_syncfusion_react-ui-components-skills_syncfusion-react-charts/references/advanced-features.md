# Advanced Features

## Financial Chart Types

### Candlestick Chart (OHLC)

Use for stock market data displaying Open, High, Low, and Close values.

```jsx
import { CandleSeries } from '@syncfusion/ej2-react-charts';

const stockData = [
  { date: '2024-01-01', open: 100, high: 105, low: 98, close: 103 },
  { date: '2024-01-02', open: 103, high: 108, low: 101, close: 107 }
];

<ChartComponent
  primaryXAxis={{
    valueType: 'DateTime',
    intervalType: 'Days'
  }}
>
  <Inject services={[CandleSeries]} />
  <SeriesCollectionDirective>
    <SeriesDirective
      dataSource={stockData}
      xName='date'
      low='low'
      high='high'
      open='open'
      close='close'
      type='Candle'
    />
  </SeriesCollectionDirective>
</ChartComponent>
```

**When to use:**
- Stock price analysis
- Currency pairs
- Financial instruments

### HLOC Chart (High-Low-Open-Close)

Alternative representation of OHLC data:

```jsx
<SeriesDirective
  dataSource={stockData}
  type='HighLowOpenClose'
  xName='date'
  low='low'
  high='high'
  open='open'
  close='close'
/>
```

### HiLo Chart (High-Low)

Simplified version showing only high and low values:

```jsx
<SeriesDirective
  dataSource={data}
  type='HiLo'
  xName='date'
  low='low'
  high='high'
/>
```

---

## Technical Indicators

Add moving averages, trend lines, and other technical analysis overlays.

### Trendlines

```jsx
import { Trendlines } from '@syncfusion/ej2-react-charts';

<ChartComponent>
  <Inject services={[LineSeries, Trendlines]} />
  <SeriesCollectionDirective>
    <SeriesDirective
      dataSource={data}
      type='Line'
      trendlines={[{
        type: 'MovingAverage',
        period: 20, // 20-day moving average
        name: 'MA20',
        fill: '#FF6B6B',
        width: 2
      }]}
    />
  </SeriesCollectionDirective>
</ChartComponent>
```

**Trendline types:**
- `Linear`: Best-fit line
- `Exponential`: Exponential curve
- `Logarithmic`: Logarithmic fit
- `Polynomial`: Polynomial regression
- `Power`: Power function
- `MovingAverage`: Simple moving average

### Technical Indicators (EMA, SMA, RSI, MACD, etc.)

Use dedicated indicator modules for financial analysis:

```jsx
import {
  ChartComponent,
  SeriesCollectionDirective,
  SeriesDirective,
  IndicatorsDirective,
  IndicatorDirective,
  Inject,
  CandleSeries,
  Category,
  Tooltip,
  Crosshair,
  Zoom,
  EmaIndicator,
  SmaIndicator,
  RsiIndicator,
  MacdIndicator,
  AtrIndicator,
  MomentumIndicator,
  StochasticIndicator,
  BollingerBands,
  TmaIndicator,
  AccumulationDistributionIndicator
} from '@syncfusion/ej2-react-charts';

// Example: RSI Indicator
<ChartComponent
  rows={[
    { height: '70%' },
    { height: '30%' }
  ]}
  axes={[
    { name: 'priceAxis', rowIndex: 0 },
    { name: 'rsiAxis', rowIndex: 1, minimum: 0, maximum: 100 }
  ]}
>
  <Inject services={[
    CandleSeries,
    Category,
    Tooltip,
    Crosshair,
    Zoom,
    RsiIndicator
  ]} />
  
  <SeriesCollectionDirective>
    <SeriesDirective
      dataSource={stockData}
      type='Candle'
      xName='date'
      low='low'
      high='high'
      open='open'
      close='close'
      yAxisName='priceAxis'
    />
  </SeriesCollectionDirective>
  
  <IndicatorsDirective>
    <IndicatorDirective
      type='Rsi'
      field='Close'
      yAxisName='rsiAxis'
      period={14}
      fill='#6063ff'
      upperLine={{ color: '#e74c3c' }}
      lowerLine={{ color: '#2ecc71' }}
    />
  </IndicatorsDirective>
</ChartComponent>
```

### Available Technical Indicators

**Trend Indicators:**
- **EMA (Exponential Moving Average):** `EmaIndicator`
- **SMA (Simple Moving Average):** `SmaIndicator`
- **TMA (Triangular Moving Average):** `TmaIndicator`

**Momentum Indicators:**
- **RSI (Relative Strength Index):** `RsiIndicator`
- **Momentum:** `MomentumIndicator`
- **Stochastic:** `StochasticIndicator`

**Volatility Indicators:**
- **ATR (Average True Range):** `AtrIndicator`
- **Bollinger Bands:** `BollingerBands`

**Volume Indicators:**
- **Accumulation Distribution:** `AccumulationDistributionIndicator`

**Composite Indicators:**
- **MACD (Moving Average Convergence Divergence):** `MacdIndicator`

### MACD Indicator Example

```jsx
<ChartComponent
  rows={[
    { height: '60%' },
    { height: '40%' }
  ]}
>
  <Inject services={[CandleSeries, MacdIndicator, Category]} />
  
  <SeriesCollectionDirective>
    <SeriesDirective
      dataSource={stockData}
      type='Candle'
      xName='date'
      low='low'
      high='high'
      open='open'
      close='close'
    />
  </SeriesCollectionDirective>
  
  <IndicatorsDirective>
    <IndicatorDirective
      type='Macd'
      field='Close'
      fastPeriod={12}
      slowPeriod={26}
      signalPeriod={9}
      macdLine={{ color: '#ff6347', width: 2 }}
      signalLine={{ color: '#00ff7f', width: 2 }}
    />
  </IndicatorsDirective>
</ChartComponent>
```

### Bollinger Bands Example

```jsx
<ChartComponent>
  <Inject services={[LineSeries, BollingerBands, Category]} />
  
  <SeriesCollectionDirective>
    <SeriesDirective
      dataSource={stockData}
      type='Line'
      xName='date'
      yName='close'
    />
  </SeriesCollectionDirective>
  
  <IndicatorsDirective>
    <IndicatorDirective
      type='BollingerBands'
      field='Close'
      period={20}
      standardDeviation={2}
      upperLine={{ color: '#ffb74d', width: 1 }}
      lowerLine={{ color: '#e91e63', width: 1 }}
    />
  </IndicatorsDirective>
</ChartComponent>
```

### Linear Regression

```jsx
<SeriesDirective
  trendlines={[{
    type: 'Linear',
    name: 'Trend',
    width: 2,
    fill: '#3B82F6'
  }]}
/>
```

### Polynomial Regression

```jsx
<SeriesDirective
  trendlines={[{
    type: 'Polynomial',
    polynomialOrder: 3, // cubic fit
    name: 'Polynomial Fit',
    fill: '#FF6B6B'
  }]}
/>
```

---

## Multiple Panes

Split chart into multiple sections for comparing different scales or time periods.

### Two-Pane Financial Chart

```jsx
<ChartComponent
  rows={[
    { height: '70%' }, // price pane
    { height: '30%' }  // volume pane
  ]}
  axes={[
    {
      name: 'priceYAxis',
      rowIndex: 0,
      valueType: 'Double',
      title: 'Price ($)',
      labelFormat: '${value}'
    },
    {
      name: 'volumeYAxis',
      rowIndex: 1,
      valueType: 'Double',
      title: 'Volume (M)',
      labelFormat: '{value}M'
    }
  ]}
>
  <SeriesCollectionDirective>
    {/* Price series in top pane */}
    <SeriesDirective
      dataSource={stockData}
      type='Candle'
      yAxisName='priceYAxis'
      xName='date'
      low='low'
      high='high'
      open='open'
      close='close'
    />
    
    {/* Volume series in bottom pane */}
    <SeriesDirective
      dataSource={stockData}
      type='Column'
      yAxisName='volumeYAxis'
      xName='date'
      yName='volume'
      fill='#90CAF9'
    />
  </SeriesCollectionDirective>
</ChartComponent>
```

### Column-Based Layout

```jsx
<ChartComponent
  columns={[
    { width: '60%' },
    { width: '40%' }
  ]}
  axes={[
    { name: 'leftAxis', columnIndex: 0, ... },
    { name: 'rightAxis', columnIndex: 1, ... }
  ]}
>
  {/* series for left and right panes */}
</ChartComponent>
```

---

## Accessibility

Ensure charts are usable by everyone, including people with disabilities.

### WCAG Compliance

```jsx
<ChartComponent
  accessibility={{
    tabIndex: 0,
    accessibilityRole: 'region',
    accessibilityDescription: 'Shows monthly sales data from January to December 2024'
  }}
  title='Sales Performance'
  width='100%'
  height='400px'
>
  {/* chart */}
</ChartComponent>
```

### Keyboard Navigation

Enable keyboard access:

We do not expose a dedicated API like `allowKeyboardInteraction` for keyboard navigation. The desired navigation behavior is achieved through standard Tab and arrow key actions.

```jsx
<ChartComponent
  selectionMode='Point'
>
  {/* Use arrow keys to select points, Enter to interact */}
</ChartComponent>
```

### Color Contrast

Use high-contrast color palettes:

```jsx
<ChartComponent
  palettes={[
    '#000000', // black
    '#FFFFFF', // white
    '#FFFF00'  // yellow
  ]}
>
  {/* Avoid red/green only differentiation */}
</ChartComponent>
```

### Alt Text and Descriptions

```jsx
<ChartComponent
  title='Q1 Revenue'
  subTitle='$500K total revenue across all regions'
  accessibility={{
    accessibility: 'Shows monthly sales data from January to December 2024'
  }}
>
  {/* Provide context in title/subtitle */}
</ChartComponent>
```

### Print Functionality

```jsx
const chartRef = useRef(null);

const handlePrint = () => {
  chartRef.current?.print();
};

<ChartComponent
  ref={chartRef}
  title='Chart for Printing'
>
  {/* Chart */}
</ChartComponent>
```

---

## Internationalization (i18n)

Support multiple languages and locales.

### Locale Configuration

```jsx
import { L10n } from '@syncfusion/ej2-base';

// Define locale strings
L10n.load({
  'de': {
    'charts': {
      'Click': 'Klicken Sie',
      'ZoomIn': 'Vergrößern',
      'ZoomOut': 'Verkleinern',
      'Reset': 'Zurücksetzen'
    }
  }
});

<ChartComponent locale='de'>
  {/* Chart in German */}
</ChartComponent>
```

### Date Formatting by Locale

```jsx
<ChartComponent
  primaryXAxis={{
    valueType: 'DateTime',
    intervalType: 'Months',
    labelFormat: 'MMMM', // localizes month names automatically
  }}
>
  {/* Chart */}
</ChartComponent>
```

### Number Formatting by Locale

```jsx
<SeriesDirective
  dataLabel={{
    visible: true,
    format: 'n2' // formats based on locale (1,234.56 vs 1.234,56)
  }}
/>
```

---

## Export and Print

Save charts as images or PDF.

### Export to Image

> ⚠️ **Important:** The `Export` service must be imported and injected into the chart for exporting to work. Without this, the export functionality will be unavailable.

```jsx
import { Export } from '@syncfusion/ej2-react-charts';

const chartRef = useRef(null);

const handleExport = () => {
  chartRef.current?.export('PNG', 'chart');
};

<ChartComponent ref={chartRef} export={{
  enabled: true,
  type: 'PNG'
}}>
  <Inject services={[Export]} />
  {/* Chart */}
</ChartComponent>
```

**Export formats:**
- `PNG`, `JPEG`, `SVG`: Raster/vector images
- `PDF`: PDF document
- `XLSX`, `CSV`: Data export

### Export to PDF

```jsx
const handlePDFExport = () => {
  chartRef.current?.export('PDF', 'chart', 'Landscape');
};
```

### Print Chart

```jsx
const handlePrint = () => {
  chartRef.current?.print();
};

<button onClick={handlePrint}>Print Chart</button>
```

---

## Real-Time Data Updates

Efficiently update chart data for live feeds.

### Streaming Data Pattern

```jsx
const [data, setData] = useState(initialData);
const dataRef = useRef(data);

useEffect(() => {
  const subscription = liveDataStream.subscribe((newPoint) => {
    dataRef.current = [...dataRef.current, newPoint];
    
    // Keep last 100 points
    if (dataRef.current.length > 100) {
      dataRef.current.shift();
    }
    
    setData([...dataRef.current]);
  });

  return () => subscription.unsubscribe();
}, []);

<SeriesDirective dataSource={data} />
```

### Rendering Options

**Canvas Rendering**

Enables canvas-based rendering for improved performance with large datasets.

```jsx
<ChartComponent enableCanvas={true}>
  {/* chart - better performance for large datasets */}
</ChartComponent>
```

**RTL Support**

Enables right-to-left layout rendering for RTL languages.

```jsx
<ChartComponent enableRtl={true}>
  {/* Right-to-left rendering */}
</ChartComponent>
```

**Transposed Chart**

Swaps the X and Y axes to change the chart orientation.

```jsx
<ChartComponent isTransposed={true}>
  {/* Swap X and Y axes orientation */}
</ChartComponent>
```

**Side-by-Side Placement**
```jsx
<ChartComponent enableSideBySidePlacement={true}>
  {/* Column/Bar series side-by-side */}
</ChartComponent>
```

**HTML Sanitization**
```jsx
<ChartComponent enableHtmlSanitizer={true}>
  {/* Sanitize HTML in templates/annotations */}
</ChartComponent>
```

---

## Custom Rendering

Override default rendering for complete control.

### Custom Series Rendering

```jsx
<SeriesDirective
  pointRender={(args) => {
    // Customize each point
    if (args.point.y > 100) {
      args.fill = '#4CAF50';
      args.pointSize = 10;
    } else if (args.point.y < 50) {
      args.fill = '#F44336';
    }
  }}
/>
```

### Template-Based Rendering

```jsx
<SeriesDirective
  type='Column'
   marker={{
    dataLabel: {
      visible: true,
      template: `<div style="background:#fff;border:1px solid #333;padding:2px 6px;">${point.x}: ${point.y}</div>`
    }
  }}
/>
```

---

## Performance Optimization

### Large Dataset Handling

```jsx
// Use category axis for performance
<ChartComponent
  primaryXAxis={{
    valueType: 'Category' // faster than DateTime for large datasets
  }}
>
  {/* Chart */}
</ChartComponent>

// Aggregate data before visualization
const aggregatedData = data.reduce((acc, item) => {
  const date = item.date.toDateString();
  const existing = acc.find(d => d.date === date);
  
  if (existing) {
    existing.value += item.value;
  } else {
    acc.push({ date, value: item.value });
  }
  
  return acc;
}, []);
```

### Debounce Updates

```jsx
const [data, setData] = useState([]);

useEffect(() => {
  const timeoutId = setTimeout(() => {
    setData(newData);
  }, 300); // Debounce rapid updates

  return () => clearTimeout(timeoutId);
}, [newData]);
```

---

## Responsive Design

Make charts adapt to screen size.

### Fluid Layout

```jsx
<ChartComponent
  width='100%'
  height='400px'
>
  {/* Chart fills container width */}
</ChartComponent>
```

### Media Query Adjustments

```jsx
useEffect(() => {
  const handleResize = () => {
    if (window.innerWidth < 768) {
      setChartConfig({
        height: '300px',
        legendSettings: { position: 'Bottom' }
      });
    } else {
      setChartConfig({
        height: '500px',
        legendSettings: { position: 'Right' }
      });
    }
  };

  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
}, []);
```

---

## Common Advanced Patterns

### Pattern 1: Dashboard with Multiple Charts

```jsx
export default function Dashboard() {
  return (
    <div className='grid grid-cols-2 gap-4'>
      <ChartComponent>
        {/* Revenue chart */}
      </ChartComponent>
      <ChartComponent>
        {/* Profit chart */}
      </ChartComponent>
      <ChartComponent>
        {/* Growth chart */}
      </ChartComponent>
      <ChartComponent>
        {/* Comparison chart */}
      </ChartComponent>
    </div>
  );
}
```

### Pattern 2: Drill-Down with Multiple Levels

```jsx
const [level, setLevel] = useState('year'); // year → month → day

const data = useMemo(() => {
  switch (level) {
    case 'year': return yearlyData;
    case 'month': return monthlyData;
    case 'day': return dailyData;
  }
}, [level]);

const handlePointClick = (args) => {
  setLevel(level === 'year' ? 'month' : 'day');
};

<ChartComponent chartMouseClick={handlePointClick}>
  <SeriesDirective dataSource={data} />
</ChartComponent>
```

### Pattern 3: Combined Technical Analysis

```jsx
<ChartComponent>
  <SeriesCollectionDirective>
    {/* Candlestick for price */}
    <SeriesDirective
      type='Candle'
      trendlines={[
        { type: 'MovingAverage', period: 20 },
        { type: 'MovingAverage', period: 50 }
      ]}
    />
    
    {/* RSI indicator on separate pane */}
  </SeriesCollectionDirective>
</ChartComponent>
```

---

## Troubleshooting Advanced Features

| Issue | Cause | Solution |
|-------|-------|----------|
| Trendlines not showing | Trendlines service not injected | Add Trendlines to Inject services array |
| Indicators not rendering | Indicator module not injected | Import and inject specific indicator (e.g., RsiIndicator) |
| Moving average incorrect | Wrong period value | Verify period matches data density |
| Performance slow with 10k+ points | Rendering all points | Use virtual scrolling or aggregate data |
| Export not working | Export module not injected | Inject Export service and set enableExport |
| i18n strings not translating | Locale not registered | Call `L10n.load()` before rendering |

---

## Strip Lines

Add reference lines or bands to highlight specific ranges:

```jsx
import { StripLine } from '@syncfusion/ej2-react-charts';

<ChartComponent
  primaryYAxis={{
    stripLines: [
      {
        start: 30,
        end: 40,
        color: 'rgba(255, 0, 0, 0.1)',
        text: 'Target Range',
        textStyle: {
          size: '12px',
          color: '#ff0000'
        }
      },
      {
        start: 50,
        size: 0,
        color: '#ff0000',
        dashArray: '5,5',
        text: 'Threshold'
      }
    ]
  }}
>
  <Inject services={[LineSeries, Category, StripLine]} />
  {/* chart content */}
</ChartComponent>
```

---

## Multi-Level Labels

Create hierarchical axis labels:

```jsx
import { MultiLevelLabel } from '@syncfusion/ej2-react-charts';

<ChartComponent
  primaryXAxis={{
    valueType: 'Category',
    multiLevelLabels: [
      {
        categories: [
          { start: 'Jan', end: 'Mar', text: 'Q1' },
          { start: 'Apr', end: 'Jun', text: 'Q2' },
          { start: 'Jul', end: 'Sep', text: 'Q3' },
          { start: 'Oct', end: 'Dec', text: 'Q4' }
        ]
      }
    ]
  }}
>
  <Inject services={[ColumnSeries, Category, MultiLevelLabel]} />
  {/* chart content */}
</ChartComponent>
```

---

## API Reference

For complete details on advanced features:
- **Advanced Features API:** https://ej2.syncfusion.com/react/documentation/api/chart/overview
- **Technical Indicators:** https://ej2.syncfusion.com/react/documentation/api/chart/technicalindicatormodel
- **Trendlines:** https://ej2.syncfusion.com/react/documentation/api/chart/trendline
- **Annotations:** https://ej2.syncfusion.com/react/documentation/api/chart/chartannotationsettingsmodel
