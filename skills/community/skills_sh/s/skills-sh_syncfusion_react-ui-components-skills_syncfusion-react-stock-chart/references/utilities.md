# Utilities: Export, Print, and Accessibility

Comprehensive guide for exporting stock charts to various formats, printing functionality, and implementing accessibility features for WCAG compliance.

> Reference API: [references/api.md](./api.md)

**Note:** Export/Print require injecting `Export` modules; the method signatures and available export types are listed in the API reference.

## Table of Contents
- [Export](#export-functionality)
  - [Export Formats](#export-formats)
  - [Export Methods](#export-methods)
  - [Export Configuration](#export-configuration)
  - [Disabling Export](#disabling-export)
- [Print](#print-functionality)
  - [Print Methods](#print-methods)
  - [Print Configuration](#print-configuration)
  - [Disabling Print](#disabling-print)
- [Accessibility](#accessibility)
  - [WCAG Compliance](#wcag-compliance)
  - [Keyboard Navigation](#keyboard-navigation)
  - [Screen Reader Support](#screen-reader-support)
  - [Color Contrast](#color-contrast)
  - [Implementation Guide](#accessibility-implementation-guide)

## Export Functionality

Stock Chart provides built-in export functionality to save charts as image files (JPEG, PNG, SVG) or PDF documents.

### Export Formats

The chart can be exported in four formats:

1. **JPEG** - Compressed raster image format
2. **PNG** - Lossless raster image format (recommended for quality)
3. **SVG** - Scalable vector graphics (best for scaling)
4. **PDF** - Portable document format (for documents/reports)

### Export Methods

#### Using Export Dropdown (Default)

The chart includes a built-in export dropdown in the period selector toolbar:

```typescript
import { 
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  Inject,
  DateTime,
  CandleSeries,
  Export
} from '@syncfusion/ej2-react-charts';

function ExportableChart() {
  const stockData = [ /* data */ ];

  return (
    <StockChartComponent
      id='stockchart'
      title='Stock Price'
      primaryXAxis={{ valueType: 'DateTime' }}
      exportType={['PNG', 'JPEG', 'SVG', 'PDF']}  // Available export types
    >
      <Inject services={[DateTime, CandleSeries, Export]} />
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

**Important:** Inject `Export` module to enable export functionality.

### Disabling Export

To disable the export button, set `exportType` to an empty array:

```typescript
<StockChartComponent
  exportType={[]}  // Disables export dropdown
>
  {/* ... */}
</StockChartComponent>
```

Or remove specific export types:

```typescript
<StockChartComponent
  exportType={['PNG', 'PDF']}  // Only PNG and PDF available
>
  {/* ... */}
</StockChartComponent>
```

## Print Functionality

The StockChart component provides built-in print functionality through the toolbar.
- No modules are required for stock chart printing.

Print Usage

### Print Methods

#### Using Print Button (Default)

The chart includes a built-in print button in the period selector toolbar:

```typescript
import { 
  StockChartComponent,
  Inject,
  DateTime,
  CandleSeries
} from '@syncfusion/ej2-react-charts';

function PrintableChart() {
  const stockData = [ /* data */ ];

  return (
    <StockChartComponent
      id='stockchart'
      title='Stock Price'
      primaryXAxis={{ valueType: 'DateTime' }}
    >
      <Inject services={[DateTime, CandleSeries]} />
      {/* Print button automatically available */}
    </StockChartComponent>
  );
}
```

**Important:** No modules are required for stock chart printing. Printing works directly on the stock chart when using the print method. There is no print module for the stock chart. Printing is handled internally via the toolbar.

#### Keyboard Shortcut

Users can also print using `Ctrl + P` keyboard shortcut when the chart has focus.

### Print Configuration

The print functionality uses the browser's native print dialog, which allows users to:
- Select printer
- Choose page orientation (portrait/landscape)
- Set page margins
- Preview before printing
- Save as PDF (browser-dependent)

### Disabling Print

To disable the print functionality, clear the toolbar or remove the Print option:

```typescript
// Disable all toolbar options
<StockChartComponent toolbar={[]} />

// Or disable just print while keeping other toolbar items
<StockChartComponent toolbar={['Export']} />  // Only export, no print
```

## Accessibility

Stock Chart follows accessibility guidelines and standards including ADA, Section 508, and WCAG 2.2 for users with disabilities.

### WCAG Compliance

The Stock Chart component meets the following accessibility standards:

| Standard | Compliance |
|----------|-----------|
| WCAG 2.2 | ✅ Full Support |
| Section 508 | ✅ Full Support |
| Screen Reader | ✅ Full Support |
| Right-to-Left (RTL) | ✅ Full Support |
| Color Contrast | ✅ Full Support |
| Mobile Device | ✅ Full Support |
| Keyboard Navigation | ✅ Full Support |
| Accessibility Checker | ✅ Validated |
| Axe-core Validation | ✅ Validated |

### WAI-ARIA Attributes

The Stock Chart implements WAI-ARIA attributes for assistive technologies:

**ARIA Roles:**
- `img` - Chart area identified as image
- `button` - Interactive buttons (export, print, period selectors)
- `region` - Chart regions for navigation

**ARIA Attributes:**
- `aria-label` - Descriptive labels for chart elements
- `aria-hidden` - Hides decorative elements from screen readers
- `aria-pressed` - Button state for toggles

### Keyboard Navigation

Complete keyboard support for accessibility:

| Key Combination | Action |
|----------------|--------|
| `Alt + J` | Move focus to Stock Chart element |
| `Tab` | Move to next element in chart |
| `Shift + Tab` | Move to previous element in chart |
| `Down Arrow` | Move focus to data point on left |
| `Up Arrow` | Move focus to data point on right |
| `ESC` | Cancel tooltip for data point |
| `Ctrl + P` | Print the Stock Chart |
| `Enter` | Activate focused element (button/control) |
| `Space` | Toggle focused element |

### Screen Reader Support

Stock Chart provides comprehensive screen reader support:

**Accessible features:**
- Chart title announced
- Axis labels and values read
- Series names and data points described
- Interactive elements clearly labeled
- State changes announced
- Error messages communicated

**Implementation:**
```typescript
<StockChartComponent
  title='AAPL Stock Price Analysis'  // Announced by screen readers
  primaryXAxis={{
    title: 'Trading Date',  // Axis title announced
    valueType: 'DateTime'
  }}
  primaryYAxis={{
    title: 'Price in US Dollars'  // Descriptive title
  }}
>
  <StockChartSeriesDirective
    name='Apple Inc Stock Price'  // Series name for screen readers
    dataSource={stockData}
  />
</StockChartComponent>
```

### Color Contrast

Stock Chart themes meet WCAG color contrast requirements:

**Contrast ratios:**
- Normal text: Minimum 4.5:1
- Large text: Minimum 3:1
- Interactive elements: Minimum 3:1

**High contrast theme:**
```typescript
<StockChartComponent
  theme='HighContrast'  // Maximum contrast for visibility
>
  {/* ... */}
</StockChartComponent>
```

**Custom accessible colors:**
```typescript
<StockChartSeriesDirective
  bearFillColor='#c62828'  // Dark red (good contrast)
  bullFillColor='#2e7d32'  // Dark green (good contrast)
/>
```

### Accessibility Implementation Guide

#### 1. Provide Descriptive Titles

```typescript
<StockChartComponent
  title='Apple Inc (AAPL) Stock Price Performance - Last 12 Months'
  primaryXAxis={{ title: 'Trading Date (Month/Year)' }}
  primaryYAxis={{ title: 'Stock Price (US Dollars)' }}
>
  {/* ... */}
</StockChartComponent>
```

#### 2. Use Semantic Series Names

```typescript
<StockChartSeriesDirective
  name='AAPL Daily Stock Price'  // Clear, descriptive name
  dataSource={stockData}
/>
```

#### 3. Enable Keyboard Navigation

Keyboard navigation is enabled by default. Ensure focus management:

```typescript
import { useEffect, useRef } from 'react';

function AccessibleChart() {
  const chartRef = useRef(null);

  useEffect(() => {
    // Set focus to chart when component mounts
    if (chartRef.current) {
      const chartElement = document.getElementById('stockchart');
      if (chartElement) {
        chartElement.setAttribute('tabindex', '0');
      }
    }
  }, []);

  return (
    <StockChartComponent
      ref={chartRef}
      id='stockchart'
      title='Accessible Stock Chart'
    >
      {/* ... */}
    </StockChartComponent>
  );
}
```

#### 4. Use High Contrast Themes

```typescript
<StockChartComponent
  theme='HighContrast'
  tooltip={{
    enable: true,
    fill: '#000000',
    textStyle: { color: '#ffffff' }
  }}
>
  {/* ... */}
</StockChartComponent>
```

#### 5. Provide Text Alternatives

```typescript
function AccessibleStockChart() {
  const stockData = [ /* data */ ];
  
  return (
    <div>
      <StockChartComponent
        id='stockchart'
        title='Stock Price Chart'
      >
        {/* ... */}
      </StockChartComponent>
      
      {/* Text alternative for screen readers */}
      <div className="sr-only" aria-live="polite">
        Stock price chart showing AAPL trading data from January to December 2023.
        Opening price: $125.50, Closing price: $152.25, representing a 21% increase.
      </div>
    </div>
  );
}

export default AccessibleStockChart;
```

#### 6. Complete Accessible Example

```typescript
import { 
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  Inject,
  DateTime,
  CandleSeries,
  Tooltip,
  Crosshair,
  Export
} from '@syncfusion/ej2-react-charts';

function FullyAccessibleChart() {
  const stockData = [ /* data */ ];

  return (
    <div role="region" aria-label="Stock Price Analysis Dashboard">
      <h2 id="chart-heading">Apple Inc (AAPL) Stock Performance</h2>
      
      <StockChartComponent
        id='accessibleChart'
        title='AAPL Stock Price - Last Year'
        titleStyle={{
          fontSize: '16px',
          fontWeight: 'bold'
        }}
        theme='HighContrast'
        primaryXAxis={{
          valueType: 'DateTime',
          title: 'Trading Date',
          labelFormat: 'MMM dd, yyyy'
        }}
        primaryYAxis={{
          title: 'Stock Price (USD)',
          labelFormat: '${value}'
        }}
        tooltip={{
          enable: true,
          format: 'Date: ${point.x}<br/>Open: ${point.open}<br/>High: ${point.high}<br/>Low: ${point.low}<br/>Close: ${point.close}'
        }}
        crosshair={{
          enable: true,
          lineType: 'Both'
        }}
        aria-labelledby="chart-heading"
      >
        <Inject services={[DateTime, CandleSeries, Tooltip, Crosshair, Export]} />
        <StockChartSeriesCollectionDirective>
          <StockChartSeriesDirective
            dataSource={stockData}
            type='Candle'
            name='AAPL Stock Price'
            xName='x'
            high='high'
            low='low'
            open='open'
            close='close'
            bearFillColor='#c62828'
            bullFillColor='#2e7d32'
          />
        </StockChartSeriesCollectionDirective>
      </StockChartComponent>

      {/* Screen reader announcement */}
      <div 
        className="sr-only" 
        role="status" 
        aria-live="polite"
        aria-atomic="true"
      >
        Stock chart loaded. Use Alt+J to focus on chart, then use arrow keys to navigate data points.
        Press Ctrl+P to print, or use export dropdown for saving.
      </div>
    </div>
  );
}

export default FullyAccessibleChart;
```

### Accessibility Testing

**Recommended tools:**
1. **Accessibility Checker** - `npm install accessibility-checker`
2. **Axe DevTools** - Browser extension
3. **NVDA/JAWS** - Screen reader testing
4. **Wave** - Web accessibility evaluation tool
5. **Lighthouse** - Chrome DevTools audit

**Testing checklist:**
- ✅ Test keyboard navigation (Tab, Arrow keys)
- ✅ Verify screen reader announcements
- ✅ Check color contrast ratios
- ✅ Test with high contrast themes
- ✅ Verify ARIA attributes
- ✅ Test focus indicators
- ✅ Validate with automated tools
- ✅ Test with real assistive technologies

## Best Practices

**Export:**
- Provide multiple format options (PNG, PDF, SVG)
- Use descriptive file names with dates
- Include export instructions for users
- Test exported files for quality

**Print:**
- Ensure chart renders well in print preview
- Consider page orientation (landscape for wide charts)
- Test print output on different browsers
- Provide print-friendly styling

**Accessibility:**
- Always use high contrast themes option
- Provide descriptive titles and labels
- Test with keyboard navigation
- Verify screen reader compatibility
- Include text alternatives
- Use semantic HTML structure
- Test with real assistive technologies
- Follow WCAG 2.2 Level AA guidelines

**Performance:**
- Export/print operations are client-side
- No performance impact on chart rendering
- Large charts may take longer to export/print
- Consider reducing data density for exports
