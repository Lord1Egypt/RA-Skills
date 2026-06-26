# Appearance and Theming

## Table of Contents
- [Overview](#overview)
- [Built-in Themes](#built-in-themes)
- [Custom Themes](#custom-themes)
- [Gradient Effects](#gradient-effects)
- [Chart Export and Printing](#chart-export-and-printing)
- [Responsive Design](#responsive-design)
- [Dynamic Updates](#dynamic-updates)
- [Animation Settings](#animation-settings)

## Overview

Appearance and theming customize the visual presentation of accumulation charts, from built-in themes to gradients, printing, and dynamic updates.

## Built-in Themes

Apply Syncfusion's built-in themes by importing the corresponding CSS:

```tsx
import { 
  AccumulationChartComponent,
  AccumulationSeriesCollectionDirective,
  AccumulationSeriesDirective,
  Inject,
  PieSeries
} from '@syncfusion/ej2-react-charts';

function ThemedChart() {
  const data = [
    { x: 'Chrome', y: 61.3 },
    { x: 'Safari', y: 24.6 },
    { x: 'Firefox', y: 14.1 }
  ];

  return (
    <AccumulationChartComponent theme='Material' id='themed-chart'>
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

**Available themes:**
- Material
- Material 3
- Bootstrap 5
- Bootstrap 4
- Tailwind CSS
- Fluent
- Fabric (Microsoft)
- High Contrast

## Custom Themes

Create custom themes by defining color palettes and styles:

```tsx
function CustomThemedChart() {
  const data = [
    { x: 'Product A', y: 45 },
    { x: 'Product B', y: 30 },
    { x: 'Product C', y: 25 }
  ];

  // Custom color palette
  const customPalette = [
    '#667eea',
    '#764ba2',
    '#f093fb',
    '#4facfe'
  ];

  return (
    <AccumulationChartComponent 
      id='custom-theme'
      background='#f8f9fa'
      palettes={customPalette}
      titleStyle={{
        fontFamily: 'Segoe UI, sans-serif',
        size: '18px',
        fontWeight: '600',
        color: '#333333'
      }}
      margin={{ left: 20, right: 20, top: 30, bottom: 20 }}
      border={{ width: 0 }}
    >
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          border={{ width: 2, color: '#ffffff' }}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

**Complete theme object:**

```tsx
function FullCustomTheme() {
  const data = [
    { x: 'Q1', y: 35 },
    { x: 'Q2', y: 28 },
    { x: 'Q3', y: 42 },
    { x: 'Q4', y: 31 }
  ];

  const darkTheme = {
    background: '#1e1e1e',
    palette: ['#00d4ff', '#00ff88', '#ffaa00', '#ff0066'],
    title: {
      fontFamily: 'Consolas, monospace',
      size: '20px',
      fontWeight: 'bold',
      color: '#ffffff'
    },
    border: {
      width: 1,
      color: '#444444'
    }
  };

  return (
    <AccumulationChartComponent 
      id='full-custom-theme'
      title='Quarterly Sales - Dark Theme'
      background={darkTheme.background}
      palettes={darkTheme.palette}
      titleStyle={darkTheme.title}
      border={darkTheme.border}
    >
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          border={{ width: 2, color: '#000000' }}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Gradient Effects

Apply gradient fills to slices using pointRender event:

```tsx
import { IAccPointRenderEventArgs } from '@syncfusion/ej2-react-charts';

function GradientChart() {
  const data = [
    { x: 'Chrome', y: 61.3 },
    { x: 'Safari', y: 24.6 },
    { x: 'Firefox', y: 14.1 }
  ];

  const gradients = [
    'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
  ];

  const onPointRender = (args: IAccPointRenderEventArgs): void => {
    args.fill = gradients[args.point.index % gradients.length];
  };

  return (
    <AccumulationChartComponent 
      id='gradient-chart'
      pointRender={onPointRender}
    >
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

**SVG gradient fills:**

```tsx
function SVGGradientChart() {
  const data = [
    { x: 'Product A', y: 45 },
    { x: 'Product B', y: 30 },
    { x: 'Product C', y: 25 }
  ];

  const onPointRender = (args: IAccPointRenderEventArgs): void => {
    args.fill = `url(#gradient${args.point.index})`;
  };

  return (
    <div>
      <svg width="0" height="0">
        <defs>
          <linearGradient id="gradient0" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style={{ stopColor: '#667eea', stopOpacity: 1 }} />
            <stop offset="100%" style={{ stopColor: '#764ba2', stopOpacity: 1 }} />
          </linearGradient>
          <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style={{ stopColor: '#f093fb', stopOpacity: 1 }} />
            <stop offset="100%" style={{ stopColor: '#f5576c', stopOpacity: 1 }} />
          </linearGradient>
          <linearGradient id="gradient2" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style={{ stopColor: '#4facfe', stopOpacity: 1 }} />
            <stop offset="100%" style={{ stopColor: '#00f2fe', stopOpacity: 1 }} />
          </linearGradient>
        </defs>
      </svg>

      <AccumulationChartComponent 
        id='svg-gradient'
        pointRender={onPointRender}
      >
        <Inject services={[PieSeries]} />
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective
            dataSource={data}
            xName='x'
            yName='y'
          />
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>
    </div>
  );
}
```

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
<AccumulationChartComponent theme='Material3Dark'>
  {/* chart content */}
</AccumulationChartComponent>

## Chart Export and Printing

Export charts as images or PDF, or print directly:

```tsx
import { 
  AccumulationChartComponent,
  Inject,
  PieSeries,
  AccumulationDataLabel
} from '@syncfusion/ej2-react-charts';

function ExportPrintChart() {
  const chartRef = React.useRef<AccumulationChartComponent>(null);
  
  const data = [
    { x: 'Chrome', y: 61.3 },
    { x: 'Safari', y: 24.6 },
    { x: 'Firefox', y: 14.1 }
  ];

  const exportChart = (type: 'PNG' | 'JPEG' | 'SVG' | 'PDF') => {
    if (chartRef.current) {
      chartRef.current.export(type, 'chart-export');
    }
  };

  const printChart = () => {
    if (chartRef.current) {
      chartRef.current.print();
    }
  };

  return (
    <div>
      <div style={{ marginBottom: '10px' }}>
        <button onClick={() => exportChart('PNG')}>Export as PNG</button>
        <button onClick={() => exportChart('JPEG')}>Export as JPEG</button>
        <button onClick={() => exportChart('SVG')}>Export as SVG</button>
        <button onClick={() => exportChart('PDF')}>Export as PDF</button>
        <button onClick={printChart}>Print Chart</button>
      </div>

      <AccumulationChartComponent 
        id='export-print-chart'
        ref={chartRef}
        title='Browser Market Share'
      >
        <Inject services={[PieSeries, AccumulationDataLabel]} />
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective
            dataSource={data}
            xName='x'
            yName='y'
            dataLabel={{ visible: true }}
          />
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>
    </div>
  );
}
```

## Responsive Design

Make charts responsive to container size changes:

```tsx
function ResponsiveChart() {
  const data = [
    { x: 'Mobile', y: 55 },
    { x: 'Desktop', y: 30 },
    { x: 'Tablet', y: 15 }
  ];

  return (
    <div style={{ width: '100%', height: '400px' }}>
      <AccumulationChartComponent 
        id='responsive-chart'
        width='100%'
        height='100%'
      >
        <Inject services={[PieSeries]} />
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective
            dataSource={data}
            xName='x'
            yName='y'
            radius='80%'
          />
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>
    </div>
  );
}
```

**Responsive with breakpoints:**

```tsx
function ResponsiveBreakpoints() {
  const [isMobile, setIsMobile] = React.useState(window.innerWidth < 768);

  React.useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const data = [
    { x: 'Category A', y: 35 },
    { x: 'Category B', y: 28 },
    { x: 'Category C', y: 22 },
    { x: 'Category D', y: 15 }
  ];

  return (
    <AccumulationChartComponent 
      id='responsive-breakpoints'
      width='100%'
      height={isMobile ? '300px' : '450px'}
    >
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          radius={isMobile ? '70%' : '85%'}
          innerRadius={isMobile ? '0%' : '40%'}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Dynamic Updates

Update chart data and appearance dynamically:

```tsx
function DynamicUpdates() {
  const [data, setData] = React.useState([
    { x: 'Product A', y: 45 },
    { x: 'Product B', y: 30 },
    { x: 'Product C', y: 25 }
  ]);

  const [theme, setTheme] = React.useState('light');

  const refreshData = () => {
    setData([
      { x: 'Product A', y: Math.floor(Math.random() * 50) + 20 },
      { x: 'Product B', y: Math.floor(Math.random() * 50) + 20 },
      { x: 'Product C', y: Math.floor(Math.random() * 50) + 20 }
    ]);
  };

  const toggleTheme = () => {
    setTheme(theme === 'light' ? 'dark' : 'light');
  };

  const lightPalette = ['#667eea', '#764ba2', '#f093fb'];
  const darkPalette = ['#00d4ff', '#00ff88', '#ffaa00'];

  return (
    <div>
      <div style={{ marginBottom: '10px' }}>
        <button onClick={refreshData}>Refresh Data</button>
        <button onClick={toggleTheme}>Toggle Theme</button>
      </div>

      <AccumulationChartComponent 
        id='dynamic-updates'
        background={theme === 'light' ? '#ffffff' : '#1e1e1e'}
        palettes={theme === 'light' ? lightPalette : darkPalette}
        titleStyle={{
          color: theme === 'light' ? '#333' : '#fff'
        }}
      >
        <Inject services={[PieSeries]} />
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective
            dataSource={data}
            xName='x'
            yName='y'
            animation={{ enable: true, duration: 800 }}
          />
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>
    </div>
  );
}
```

## Animation Settings

Control chart animations:

```tsx
function AnimationSettings() {
  const data = [
    { x: 'Jan', y: 35 },
    { x: 'Feb', y: 28 },
    { x: 'Mar', y: 34 }
  ];

  return (
    <AccumulationChartComponent 
      id='animation-settings'
      enableAnimation={true}
    >
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          animation={{
            enable: true,
            duration: 1200,      // Animation duration in ms
            delay: 0             // Delay before animation starts
          }}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

**Disable animations:**

```tsx
function NoAnimation() {
  const data = [
    { x: 'A', y: 25 },
    { x: 'B', y: 35 },
    { x: 'C', y: 40 }
  ];

  return (
    <AccumulationChartComponent 
      id='no-animation'
      enableAnimation={false}
    >
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          animation={{ enable: false }}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

**Advanced Animation:**

Data label templates and dynamic updates (`addPoint`, `removePoint`, `setData`) also respect animation settings. Labels are hidden during animation and revealed after `animationComplete` event.

```tsx
<AccumulationChartComponent 
  enableAnimation={true}
  animationComplete={(args) => {
    console.log('Animation completed for', args.series.name);
  }}>
  {/* series with animation enabled */}
</AccumulationChartComponent>
```

## Common Issues and Solutions

**Issue: Theme CSS not applied**
- Solution: Ensure theme CSS is imported in main App.tsx or index.tsx
- Solution: Import both base and charts theme files
- Solution: Check CSS import order (base before component)

**Issue: Custom colors not showing**
- Solution: Verify palettes array has enough colors
- Solution: Check pointColorMapping if using data-based colors
- Solution: Ensure colors use valid CSS color values

**Issue: Gradients not rendering**
- Solution: Use SVG gradients defined in defs
- Solution: Apply gradients via pointRender event
- Solution: Check browser compatibility for gradient syntax

**Issue: Export not working**
- Solution: Ensure chart reference is properly set
- Solution: Call export method after chart is fully rendered
- Solution: Check browser console for errors

**Issue: Chart not responsive**
- Solution: Set width='100%' and height='100%'
- Solution: Ensure parent container has defined dimensions
- Solution: Use percentage-based radius values

**Issue: Animation lagging**
- Solution: Reduce animation duration
- Solution: Disable animation for large datasets
- Solution: Optimize data point count
