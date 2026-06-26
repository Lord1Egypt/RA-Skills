# Appearance and Styling

## Table of Contents
- [Color and Fill](#color-and-fill)
- [Legend Configuration](#legend-configuration)
- [Data Labels](#data-labels)
- [Chart Annotations](#chart-annotations)
- [Gradients](#gradients)
- [Title and Subtitle](#title-and-subtitle)
- [Border and Styling](#border-and-styling)
- [Theme Customization](#theme-customization)

---

## Color and Fill

### Series Color

Set series fill color:

```jsx
<SeriesDirective
  fill='#3B82F6'
  type='Column'
  ...
/>
```

**Supported formats:**
- Hex: `'#3B82F6'`
- RGB: `'rgb(59, 130, 246)'`
- Named colors: `'blue'`, `'red'`, `'green'`

### Palette Colors

Use predefined color palettes:

```jsx
<ChartComponent
  palettes={['#FF5733', '#33FF57', '#3357FF']}
>
  {/* series will cycle through these colors */}
</ChartComponent>
```

**Built-in palettes:**
- Material (default)
- Fabric
- Bootstrap
- HighContrast
- Palette1, Palette2, etc.

### Point-Level Colors (Conditional)

```jsx
const data = [
  { month: 'Jan', value: 35, color: '#4CAF50' },
  { month: 'Feb', value: 28, color: '#F44336' }
];

<SeriesDirective
  dataSource={data}
  pointColorMapping='color' // use data's color property
  ...
/>
```

---

## Legend Configuration

Legends identify series and allow user interaction.

### Basic Legend

```jsx
<ChartComponent
  legendSettings={{
    visible: true,
    position: 'Right' // Top, Bottom, Left, Right, Custom
  }}
>
  {/* chart */}
</ChartComponent>
```

### Legend Customization

```jsx
<ChartComponent
  legendSettings={{
    visible: true,
    position: 'Top',
    alignment: 'Center', // Far, Center, Near
    background: 'white',
    border: {
      color: '#cccccc',
      width: 1
    },
    padding: 10,
    margin: {
      left: 10,
      right: 10,
      top: 10,
      bottom: 10
    },
    labelPosition: 'After', // Before, After
    enablePages: true, // pagination for many series
    maximumLabelWidth: 100
  }}
>
  {/* chart */}
</ChartComponent>
```

### Interactive Legend

```jsx
<ChartComponent
  legendSettings={{
    visible: true,
    toggleVisibility: true // click to hide/show series
  }}
>
  {/* chart */}
</ChartComponent>
```

### Series Name in Legend

```jsx
<SeriesDirective
  name='Monthly Revenue'
  // This name appears in legend
  type='Column'
  ...
/>
```

---

## Data Labels

Display values directly on chart points/bars/columns. Data labels are configured inside the `marker` property of `SeriesDirective` using the `dataLabel` key. Inject the `DataLabel` service to enable this feature.

### Basic Data Labels

```jsx
import { DataLabel } from '@syncfusion/ej2-react-charts';

<ChartComponent id='charts' primaryXAxis={{ valueType: 'Category' }}>
  <Inject services={[ColumnSeries, Category, DataLabel]} />
  <SeriesCollectionDirective>
    <SeriesDirective
      dataSource={data}
      xName='month'
      yName='sales'
      type='Column'
      marker={{
        dataLabel: {
          visible: true,
          position: 'Top' // Top, Bottom, Middle, Outer
        }
      }}
    />
  </SeriesCollectionDirective>
</ChartComponent>
```

**Position options:**
- `Top`, `Bottom`, `Left`, `Right`: Around the point
- `Middle`: Inside the point (column/bar)
- `Outer`: Outside the point (line/area/scatter)

### Data Label Template

Use an HTML template string for fully custom label content:

```jsx
<SeriesDirective
  dataSource={data}
  xName='month'
  yName='sales'
  type='Column'
  marker={{
    dataLabel: {
      visible: true,
      template: `<div style="background:#fff;border:1px solid #333;padding:2px 6px;">${point.x}: ${point.y}</div>`
    }
  }}
/>
```

**Available template variables:**
- `${point.x}`: X value
- `${point.y}`: Y value
- `${point.text}`: Formatted point text
- `${series.name}`: Series name
- `${point.percentage}`: Percentage (for pie/doughnut charts)

### Formatted Data Labels

Use the `format` property for simple value formatting:

```jsx
<SeriesDirective
  dataSource={data}
  xName='month'
  yName='sales'
  type='Column'
  marker={{
    dataLabel: {
      visible: true,
      format: '${value}K'  // appends 'K' after the value
    }
  }}
/>
```

### Data Label Styling

Customize font and spacing inside `marker.dataLabel`:

```jsx
<SeriesDirective
  dataSource={data}
  xName='month'
  yName='sales'
  type='Line'
  marker={{
    visible: true,
    width: 8,
    height: 8,
    dataLabel: {
      visible: true,
      position: 'Top',
      font: {
        fontFamily: 'Arial',
        fontStyle: 'Normal',
        fontWeight: 'Bold',
        size: '12px',
        color: '#000000'
      },
      margin: {
        left: 2,
        right: 2,
        top: 2,
        bottom: 2
      }
    }
  }}
/>
```

### Data Label with Marker (Line/Scatter)

For line and scatter series, combine `marker.visible` with `marker.dataLabel` to show both point markers and labels simultaneously:

```jsx
<SeriesDirective
  dataSource={data}
  xName='month'
  yName='sales'
  type='Line'
  width={2}
  marker={{
    visible: true,         // show dot markers
    shape: 'Circle',
    width: 8,
    height: 8,
    dataLabel: {           // also show data labels
      visible: true,
      position: 'Top'
    }
  }}
/>
```

### Series Labels

Series labels display the series name directly on the chart near the last visible data point, reducing the need to refer to the legend. They can be enabled using the `labelSettings` property in the `SeriesDirective`. This property works independently and does not depend on data label imports.

```jsx
import { SeriesLabel } from '@syncfusion/ej2-react-charts';

<SeriesDirective
  dataSource={data}
  xName='month'
  yName='sales'
  type='Line'
  name='Revenue'
  labelSettings= {{ visible: true, background: 'green', showOverlapText: true, font: {size: '16px' }}}
/>
```

**Note** Module should be injected like data label.

**Available Customization Option for Series Labels**
- `text` - Specifies custom label text.
- `font` -  Controls the label’s text styling.
- `background` - Sets a background color for the label container.
- `border` - Defines the border around the label container.
- `opacity` - Adjusts label transparency.
- `showOverlapText` - if set `true`, show label even collide with chart elements.

### Last Value Labels

Highlight the final data point of each series with a special label and optional indicator line. Useful for emphasizing the latest value/trend in line, area, or similar series.

```jsx
import { LastValueLabel } from '@syncfusion/ej2-react-charts';

<SeriesDirective
  dataSource={data}
  xName='month'
  yName='sales'
  type='Line'
  lastValueLabel={{
    enable: true,
    background: '#3B82F6',
    border: { color: '#ffffff', width: 1 },
    font: { color: '#ffffff', size: '12px' }
    // Additional options: lineColor, lineWidth, dashArray, rx, ry for rounded corners
  }}
/>
```

**Note** Module should be injected like data label.

**When to use**: Time-series or trend charts where the most recent value needs clear visibility (e.g., stock prices, sales performance).

**Customization options:**

- `enable`: Set to true to show the last value label.
- Background, border, font styling.
- Indicator line properties (lineColor, lineWidth, dashArray).

---

## Chart Annotations

Add text, lines, and shapes to highlight specific areas.

### Text Annotation

```jsx
import { ChartAnnotation } from '@syncfusion/ej2-react-charts';

<ChartComponent>
  <Inject services={[ChartAnnotation]} />
  <AnnotationsDirective>
    <AnnotationDirective
      x='50%'
      y='50%'
      content='<div style="color: red;">Peak Sales</div>'
    />
  </AnnotationsDirective>
</ChartComponent>
```

### Line Annotation

```jsx
<AnnotationDirective
  type='Line'
  x1='Jan'
  y1={30}
  x2='Dec'
  y2={30}
  lineStyle={{
    color: 'red',
    dashArray: '5,5',
    width: 2
  }}
/>
```

### Image Annotation

```jsx
<AnnotationDirective
  x='Mar'
  y={35}
  content='<img src="/star.png" width="30" height="30" />'
/>
```

---

## Gradients

Apply gradient fills for visual interest.

### Linear Gradient

```jsx
<SeriesDirective
  fill='url(#linearGradient)'
  type='Column'
/>

{/* Define gradient elsewhere */}
<svg>
  <defs>
    <linearGradient id='linearGradient' x1='0%' y1='0%' x2='0%' y2='100%'>
      <stop offset='0%' stopColor='#FF6B6B' />
      <stop offset='100%' stopColor='#FFE66D' />
    </linearGradient>
  </defs>
</svg>
```

### Gradient via Style

```jsx
<ChartComponent
  chartArea={{
    backgroundColor: 'linear-gradient(180deg, #FF6B6B 0%, #FFE66D 100%)'
  }}
>
  {/* chart */}
</ChartComponent>
```

---

## Title and Subtitle

### Basic Title

```jsx
<ChartComponent
  title='Sales Dashboard 2024'
  subTitle='Monthly Performance Overview'
>
  {/* chart */}
</ChartComponent>
```

### Title Styling

```jsx
<ChartComponent
  title='Sales Dashboard'
  titleStyle={{
    fontFamily: 'Segoe UI',
    fontStyle: 'Normal',
    fontWeight: 'Bold',
    size: '18px',
    color: '#333333',
    textAlignment: 'Center'
  }}
  subTitleStyle={{
    fontFamily: 'Segoe UI',
    fontStyle: 'Italic',
    size: '14px',
    color: '#666666'
  }}
>
  {/* chart */}
</ChartComponent>
```

---

## Border and Styling

### Chart Border

```jsx
<ChartComponent
  border={{
    color: '#cccccc',
    width: 2
  }}
>
  {/* chart */}
</ChartComponent>
```

### Chart Area Background

```jsx
<ChartComponent
  chartArea={{
    border: {
      color: '#e0e0e0',
      width: 1
    },
    backgroundColor: '#fafafa'
  }}
>
  {/* chart */}
</ChartComponent>
```

### Series Border

```jsx
<SeriesDirective
  border={{
    color: '#333333',
    width: 2
  }}
  type='Column'
/>
```

### Margin and Padding

```jsx
<ChartComponent
  margin={{
    left: 40,
    right: 40,
    top: 40,
    bottom: 40
  }}
>
  {/* chart */}
</ChartComponent>
```

---

## Theme Customization

**Available themes (18+ including dark & high contrast):**
- Material, MaterialDark, Material3, Material3Dark
- Fabric, FabricDark
- Bootstrap, BootstrapDark, Bootstrap4, Bootstrap5, Bootstrap5Dark, Bootstrap5.3, Bootstrap5.3Dark
- Tailwind, TailwindDark
- Fluent, FluentDark, Fluent2, Fluent2Dark, Fluent2HighContrast
- HighContrast, HighContrastLight

Switch via the `theme` prop:

```jsx
<ChartComponent theme='Material3Dark'>
  {/* chart content */}
</ChartComponent>
```

### Dark Theme

```jsx
<ChartComponent className='dark-theme'>
  {/* chart */}
</ChartComponent>
```

**dark-theme.css:**
```css
.dark-theme .e-chart {
  background-color: #1f2937;
  color: #ffffff;
}

.dark-theme .e-chart-title {
  color: #ffffff;
}

.dark-theme .e-chart-legend {
  background-color: #111827;
}
```

---

## Complete Styled Chart Example

```jsx
<ChartComponent
  id='styled-chart'
  title='Q1 Sales Performance'
  subTitle='Regional Comparison'
  width='100%'
  height='500px'
  margin={{ left: 40, right: 40, top: 40, bottom: 40 }}
  chartArea={{
    border: { width: 0 },
    backgroundColor: '#fafafa'
  }}
  titleStyle={{
    fontWeight: 'Bold',
    size: '18px',
    color: '#1f2937'
  }}
  subTitleStyle={{
    size: '14px',
    color: '#6b7280'
  }}
  legendSettings={{
    visible: true,
    position: 'Top',
    alignment: 'Center',
    background: 'white'
  }}
  tooltip={{
    enable: true,
    shared: true,
    template: `<div>${point.x}: ${point.y}</div>`
  }}
  primaryXAxis={{
    valueType: 'Category',
    majorGridLines: { width: 0 }
  }}
  primaryYAxis={{
    labelFormat: '${value}K',
    majorGridLines: { color: '#e5e7eb' }
  }}
>
  <Inject services={[ColumnSeries, LineSeries, Category, Legend, Tooltip]} />
  <SeriesCollectionDirective>
    <SeriesDirective
      dataSource={salesData}
      xName='region'
      yName='sales'
      name='Sales'
      type='Column'
      fill='#3B82F6'
      cornerRadius={{ topLeft: 4, topRight: 4 }}
      marker={{
        dataLabel: {
          visible: true,
          position: 'Top',
          font: { fontWeight: 'Bold', size: '12px' }
        }
      }}
    />
    <SeriesDirective
      dataSource={salesData}
      xName='region'
      yName='target'
      name='Target'
      type='Line'
      width={2}
      marker={{
        visible: true,
        width: 8,
        height: 8,
        dataLabel: { visible: false }
      }}
    />
  </SeriesCollectionDirective>
</ChartComponent>
```

---

## Common Styling Patterns

### Pattern 1: Professional Dashboard Style

- Clean white background
- Subtle borders and grid
- Bold title, subtle labels
- Responsive sizing

### Pattern 2: High-Contrast Accessibility

- High contrast colors (#000 on #FFF or vice versa)
- Large font sizes (14px+)
- Thicker borders and lines
- Avoid color-only differentiation

### Pattern 3: Print-Friendly Chart

```jsx
<ChartComponent
  print={{
    type: 'PDF', // or 'PNG', 'SVG'
    orientation: 'Landscape'
  }}
>
  {/* Simplify colors, ensure good contrast */}
</ChartComponent>
```
