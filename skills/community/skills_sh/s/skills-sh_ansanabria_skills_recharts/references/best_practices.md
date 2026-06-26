# Recharts Best Practices

Design, performance, and accessibility guidelines for building production-ready charts with Recharts.

## Table of Contents

1. [Performance Optimization](#performance-optimization)
2. [Responsive Design](#responsive-design)
3. [Accessibility](#accessibility)
4. [Data Patterns](#data-patterns)
5. [Visual Design](#visual-design)
6. [Testing and Debugging](#testing-and-debugging)
7. [Common Pitfalls](#common-pitfalls)

## Performance Optimization

### 1. Memoize Data and Props

Always use `useMemo` for data transformations and `useCallback` for event handlers:

```jsx
// GOOD: Stable data reference
const processedData = useMemo(() => {
  return rawData.map(item => ({
    ...item,
    total: item.revenue + item.expenses
  }));
}, [rawData]);

// GOOD: Stable callback
const handleClick = useCallback((data) => {
  console.log('Clicked:', data);
}, []);

// GOOD: Stable dataKey function
const dataKeyFn = useCallback((entry) => entry.value * 100, []);

<LineChart data={processedData}>
  <Line dataKey={dataKeyFn} onClick={handleClick} />
</LineChart>
```

**Why this matters**: Recharts compares props by reference. New function references on each render trigger unnecessary recalculations.

### 2. Memoize Components

Wrap chart components with `React.memo` when they receive stable props:

```jsx
const MemoizedChart = React.memo(({ data }) => (
  <LineChart data={data}>
    <XAxis dataKey="name" />
    <YAxis />
    <Line type="monotone" dataKey="value" />
  </LineChart>
));

// Parent component
function Dashboard() {
  const [data] = useState(initialData);
  
  return <MemoizedChart data={data} />; // Won't re-render if data is stable
}
```

### 3. Isolate Frequently Updating Components

Separate static and dynamic chart parts:

```jsx
function OptimizedChart() {
  const [hoveredPoint, setHoveredPoint] = useState(null);
  
  // Debounced hover handler
  const handleMouseMove = useDebouncedCallback((e) => {
    if (e && e.activePayload) {
      setHoveredPoint(e.activePayload[0]);
    }
  }, 50);
  
  return (
    <LineChart data={data} onMouseMove={handleMouseMove}>
      {/* Static - rarely changes */}
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="name" />
      <YAxis />
      <Tooltip />
      <Line type="monotone" dataKey="sales" stroke="#8884d8" />
      
      {/* Dynamic - changes often */}
      {hoveredPoint && (
        <ReferenceLine 
          x={hoveredPoint.payload.name} 
          stroke="#ff7300" 
          strokeDasharray="3 3"
        />
      )}
    </LineChart>
  );
}
```

### 4. Reduce Data Points for Large Datasets

For datasets with thousands of points, aggregate or sample:

```jsx
import * as d3 from 'd3';

function OptimizedLargeChart({ rawData }) {
  // Sample data if too large
  const data = useMemo(() => {
    if (rawData.length <= 500) return rawData;
    
    // Use d3.bin for histogram or simple sampling
    const step = Math.ceil(rawData.length / 500);
    return rawData.filter((_, i) => i % step === 0);
  }, [rawData]);
  
  // Or use binning for distributions
  const binnedData = useMemo(() => {
    if (rawData.length <= 500) return rawData;
    
    const bin = d3.bin()
      .value(d => d.x)
      .thresholds(50);
    
    return bin(rawData).map(b => ({
      x0: b.x0,
      x1: b.x1,
      count: b.length,
      y: d3.mean(b, d => d.y)
    }));
  }, [rawData]);
  
  return (
    <ScatterChart>
      <Scatter data={binnedData} />
    </ScatterChart>
  );
}
```

### 5. Disable Animations for Real-time Data

```jsx
function RealtimeChart() {
  const [data, setData] = useState([]);
  
  useEffect(() => {
    const interval = setInterval(() => {
      setData(prev => [...prev.slice(-50), newPoint]);
    }, 100);
    return () => clearInterval(interval);
  }, []);
  
  return (
    <LineChart data={data}>
      <Line 
        type="monotone" 
        dataKey="value" 
        stroke="#8884d8"
        isAnimationActive={false}  // Critical for performance
        dot={false}                // Disable dots
      />
    </LineChart>
  );
}
```

### 6. Optimize Tooltip Performance

```jsx
// BAD: New component reference every render
<Tooltip content={<CustomTooltip />} />

// GOOD: Stable component reference
const CustomTooltip = useMemo(() => {
  return ({ active, payload }) => {
    if (active && payload) {
      return <div>{payload[0].value}</div>;
    }
    return null;
  };
}, []);

<Tooltip content={CustomTooltip} />

// OR use a separate component outside the render function
const StableTooltip = React.memo(({ active, payload }) => {
  if (!active || !payload) return null;
  return <div>{payload[0].value}</div>;
});

<Tooltip content={<StableTooltip />} />
```

### 7. Virtualize Lists with Charts

When rendering many charts in a list:

```jsx
import { useVirtualizer } from '@tanstack/react-virtual';

function ChartList({ datasets }) {
  const parentRef = useRef();
  
  const virtualizer = useVirtualizer({
    count: datasets.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 300,
  });
  
  return (
    <div ref={parentRef} style={{ height: '600px', overflow: 'auto' }}>
      <div style={{ height: `${virtualizer.getTotalSize()}px`, position: 'relative' }}>
        {virtualizer.getVirtualItems().map(virtualItem => (
          <div
            key={virtualItem.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualItem.size}px`,
              transform: `translateY(${virtualItem.start}px)`,
            }}
          >
            <ChartComponent data={datasets[virtualItem.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

## Responsive Design

### 1. Use the `responsive` prop (Recharts 3.3+, recommended)

The `responsive` prop makes charts automatically resize when their container dimensions change. Works with standard CSS sizing, flexbox, and CSS grid:

```jsx
// GOOD: Responsive with CSS sizing
<LineChart data={data} responsive style={{ width: '100%', maxWidth: 800, aspectRatio: '16/9' }}>
  {/* ... */}
</LineChart>

// GOOD: Responsive with explicit dimensions
<LineChart data={data} width="100%" height={300} responsive>
  {/* ... */}
</LineChart>

// BAD: Fixed size - won't adapt to container changes
<LineChart width={600} height={300} data={data}>
  {/* ... */}
</LineChart>
```

### 2. Use ResponsiveContainer (older versions)

For Recharts < 3.3, wrap the chart in `ResponsiveContainer`:

```jsx
<ResponsiveContainer width="100%" height={300}>
  <LineChart data={data}>
    {/* ... */}
  </LineChart>
</ResponsiveContainer>
```

**Important**: `ResponsiveContainer` must have a parent with defined dimensions. Height must be a number, not a percentage.

### 3. Handle Container Sizing

Ensure parent container has defined dimensions (applies to both `responsive` prop and `ResponsiveContainer`):

```jsx
// Parent must have explicit height or flex layout
<div style={{ width: '100%', height: '400px' }}>
  <LineChart data={data} responsive style={{ width: '100%', height: '100%' }}>
    {/* ... */}
  </LineChart>
</div>

// OR using flexbox
<div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
  <div style={{ flex: 1 }}>
    <LineChart data={data} responsive style={{ width: '100%', height: '100%' }}>
      {/* ... */}
    </LineChart>
  </div>
</div>
```

### 3. Adjust for Small Screens

```jsx
import { useMediaQuery } from 'react-responsive';

function AdaptiveChart({ data }) {
  const isMobile = useMediaQuery({ maxWidth: 768 });
  
  return (
    <LineChart data={data} responsive style={{ width: '100%', height: isMobile ? 200 : 400 }}>
      <XAxis 
        dataKey="name" 
        interval={isMobile ? 'preserveEnd' : 0}
        angle={isMobile ? -45 : 0}
        height={isMobile ? 50 : 30}
      />
      <YAxis width={isMobile ? 30 : 60} />
      <Tooltip />
      {/* Reduce chart complexity on mobile */}
      {!isMobile && <Legend />}
      <Line type="monotone" dataKey="value" stroke="#8884d8" />
    </LineChart>
  );
}
```

### 4. Aspect Ratio Preservation

```jsx
<LineChart data={data} responsive style={{ width: '100%', aspectRatio: '16/9' }}>
  {/* ... */}
</LineChart>

{/* Or with ResponsiveContainer (older versions): */}
<ResponsiveContainer width="100%" aspect={16 / 9}>
  <LineChart>{/* ... */}</LineChart>
</ResponsiveContainer>
```

## Accessibility

### 1. Enable Accessibility Layer

Enabled by default, but can be explicitly set:

```jsx
<LineChart accessibilityLayer={true}>
  {/* Components */}
</LineChart>
```

### 2. Add ARIA Labels

```jsx
<LineChart 
  role="img" 
  aria-label="Line chart showing monthly sales from January to June 2024"
>
  {/* Components */}
</LineChart>
```

### 3. Provide Text Alternatives

Always include descriptive text near charts:

```jsx
<figure>
  <LineChart data={data} responsive style={{ width: '100%', height: 300 }}>
    {/* ... */}
  </LineChart>
  <figcaption>
    Sales increased 25% from January to June 2024, 
    with the highest sales in June at $9,800.
  </figcaption>
</figure>
```

### 4. Keyboard Navigation

Charts are keyboard navigable by default when `accessibilityLayer` is enabled (which it is by default). The chart's `tabIndex` prop controls where it appears in the tab order:

```jsx
<LineChart tabIndex={0} accessibilityLayer>
  {/* Components */}
</LineChart>
```

### 5. Color Contrast

Ensure sufficient contrast for all chart elements:

```jsx
<LineChart>
  <Line stroke="#1f77b4" />  // Good contrast on white
  <Line stroke="#ff7f0e" />  // Good contrast on white
  {/* Avoid: stroke="#ddd" on white background */}
</LineChart>
```

### 6. Don't Rely on Color Alone

Use patterns, labels, or different line styles:

```jsx
<LineChart>
  <Line 
    type="monotone" 
    dataKey="sales" 
    stroke="#8884d8" 
    strokeWidth={2}
    name="Sales (solid line)"
  />
  <Line 
    type="monotone" 
    dataKey="profit" 
    stroke="#82ca9d" 
    strokeWidth={2}
    strokeDasharray="5 5"
    name="Profit (dashed line)"
  />
  <Legend />
</LineChart>
```

## Data Patterns

### 1. Data Shape

Recharts expects array of objects:

```javascript
// GOOD
const data = [
  { month: 'Jan', sales: 4000, profit: 2400 },
  { month: 'Feb', sales: 3000, profit: 1398 },
];

// BAD: Array of arrays
const badData = [
  ['Jan', 4000, 2400],
  ['Feb', 3000, 1398],
];

// BAD: Object of arrays
const alsoBad = {
  months: ['Jan', 'Feb'],
  sales: [4000, 3000],
};
```

### 2. Handling Null/Undefined

```jsx
// Data with missing values
const data = [
  { month: 'Jan', sales: 4000 },
  { month: 'Feb', sales: null },  // Missing
  { month: 'Mar', sales: 3000 },
];

// Option 1: Connect through nulls
<Line type="monotone" dataKey="sales" connectNulls={true} />

// Option 2: Gap at null
<Line type="monotone" dataKey="sales" connectNulls={false} />

// Option 3: Pre-process to fill values
const filledData = data.map(item => ({
  ...item,
  sales: item.sales ?? 0  // or interpolate
}));
```

### 3. Data Pre-processing

Transform data before passing to Recharts:

```jsx
const Chart = ({ rawData }) => {
  // Calculate derived values
  const processedData = useMemo(() => {
    return rawData.map(item => ({
      ...item,
      total: item.q1 + item.q2 + item.q3 + item.q4,
      average: (item.q1 + item.q2 + item.q3 + item.q4) / 4,
      growth: ((item.q4 - item.q1) / item.q1) * 100
    }));
  }, [rawData]);
  
  // Filter or sort if needed
  const filteredData = useMemo(() => {
    return processedData
      .filter(item => item.total > 0)
      .sort((a, b) => b.total - a.total);
  }, [processedData]);
  
  return (
    <LineChart data={filteredData}>
      {/* ... */}
    </LineChart>
  );
};
```

### 4. Date/Time Handling

```jsx
import { format, parseISO } from 'date-fns';

const data = [
  { date: '2024-01-01', value: 100 },
  { date: '2024-02-01', value: 150 },
];

// Option 1: Format in data
const formattedData = data.map(d => ({
  ...d,
  formattedDate: format(parseISO(d.date), 'MMM yyyy')
}));

<XAxis dataKey="formattedDate" />

// Option 2: Format with tickFormatter
<XAxis 
  dataKey="date" 
  tickFormatter={(date) => format(parseISO(date), 'MMM')}
/>

// Option 3: Use time scale with custom domain
<XAxis 
  dataKey="date" 
  type="number" 
  scale="time"
  domain={['auto', 'auto']}
  tickFormatter={(timestamp) => format(new Date(timestamp), 'MMM d')}
/>
```

## Visual Design

### 1. Consistent Color Palette

Define a color scheme:

```jsx
const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

// Use consistently
<Line stroke={COLORS[0]} />
<Line stroke={COLORS[1]} />
<Bar fill={COLORS[0]} />
```

### 2. Typography

```jsx
<XAxis 
  tick={{ fontSize: 12, fontFamily: 'Arial, sans-serif', fill: '#666' }}
  label={{ value: 'Month', fontSize: 14, fontWeight: 'bold', fill: '#333' }}
/>

<YAxis 
  tick={{ fontSize: 12, fill: '#666' }}
  tickFormatter={(value) => `$${value.toLocaleString()}`}
/>
```

### 3. Spacing and Margins

```jsx
<LineChart margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
  <XAxis dataKey="name" height={60} />
  <YAxis width={80} />
  {/* ... */}
</LineChart>
```

### 4. Grid Styling

```jsx
<CartesianGrid 
  strokeDasharray="3 3" 
  stroke="#e0e0e0"
  vertical={true}
  horizontal={true}
/>
```

### 5. Legends

```jsx
<Legend 
  verticalAlign="top" 
  height={36}
  iconType="circle"
  wrapperStyle={{ paddingTop: 20 }}
/>
```

### 6. Tooltips

```jsx
<Tooltip 
  contentStyle={{ 
    backgroundColor: '#fff', 
    border: '1px solid #ccc',
    borderRadius: '4px',
    padding: '10px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
  }}
  labelStyle={{ fontWeight: 'bold', marginBottom: '8px' }}
  itemStyle={{ fontSize: '14px' }}
  separator={": "}
/>
```

## Testing and Debugging

### 1. Use Recharts DevTools

Install devtools for debugging:

```bash
npm install @recharts/devtools
```

```jsx
import { RechartsDevtools } from '@recharts/devtools';

<LineChart data={data}>
  {/* ... */}
  <RechartsDevtools />  // Shows hook inspector
</LineChart>
```

### 2. Testing Chart Components

```jsx
import { render, screen } from '@testing-library/react';
import { LineChart, Line, XAxis, YAxis, ResponsiveContainer } from 'recharts';

describe('ChartComponent', () => {
  const mockData = [
    { name: 'A', value: 10 },
    { name: 'B', value: 20 },
  ];
  
  it('renders without crashing', () => {
    render(
      <div style={{ width: '400px', height: '300px' }}>
        <ResponsiveContainer>
          <LineChart data={mockData}>
            <XAxis dataKey="name" />
            <YAxis />
            <Line dataKey="value" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    );
  });
  
  it('displays correct data', () => {
    render(<ChartComponent data={mockData} />);
    // Check for aria-label or figcaption content
    expect(screen.getByLabelText(/sales chart/i)).toBeInTheDocument();
  });
});
```

### 3. Debugging Tips

- Check that parent container has explicit dimensions
- Verify data is array of objects
- Ensure all `dataKey` values exist in data
- Look for console warnings about prop types
- Use React DevTools to inspect re-renders

## Common Pitfalls

### 1. Chart Without Defined Size

```jsx
// WRONG: No dimensions specified
<LineChart data={data}>
  {/* ... */}
</LineChart>

// CORRECT: Use responsive prop with CSS sizing (Recharts 3.3+)
<LineChart data={data} responsive style={{ width: '100%', height: 300 }}>
  {/* ... */}
</LineChart>

// CORRECT: Static pixel dimensions
<LineChart data={data} width={600} height={300}>
  {/* ... */}
</LineChart>

// CORRECT: ResponsiveContainer (older versions) - parent must have defined height
<div style={{ height: '300px' }}>
  <ResponsiveContainer>
    <LineChart data={data}>{/* ... */}</LineChart>
  </ResponsiveContainer>
</div>
```

### 2. Missing dataKey

```jsx
// WRONG
<XAxis />  // No dataKey - won't show labels

// CORRECT
<XAxis dataKey="name" />
```

### 3. Unstable References

```jsx
// WRONG: New array every render
<LineChart data={getData()}>

// CORRECT: Memoized data
const data = useMemo(() => getData(), []);
<LineChart data={data}>
```

### 4. Incorrect Percentage in ResponsiveContainer

```jsx
// WRONG: Height cannot be percentage in ResponsiveContainer
<ResponsiveContainer width="100%" height="100%">

// CORRECT: Height must be number in ResponsiveContainer
<ResponsiveContainer width="100%" height={300}>
// OR use aspect
<ResponsiveContainer width="100%" aspect={2}>

// BETTER (Recharts 3.3+): Use responsive prop — supports CSS percentages
<LineChart data={data} responsive style={{ width: '100%', height: '100%' }}>
```

### 5. Overlapping Labels

```jsx
// Solution: Rotate labels
<XAxis 
  dataKey="name" 
  angle={-45} 
  textAnchor="end" 
  height={80} 
/>

// OR reduce tick count
<XAxis dataKey="name" interval="preserveStartEnd" />
```

### 6. Ignoring Performance Warnings

Always check for:
- Creating new functions in render
- Not memoizing data transformations
- Animating large datasets
- Not using `isAnimationActive={false}` for real-time

## ESLint Configuration

Use eslint-plugin-react-perf to catch performance issues:

```json
{
  "extends": ["plugin:react-perf/recommended"],
  "rules": {
    "react-perf/jsx-no-new-object-as-prop": "warn",
    "react-perf/jsx-no-new-array-as-prop": "warn",
    "react-perf/jsx-no-new-function-as-prop": "warn"
  }
}
```

## Resources

- [Official Performance Guide](https://recharts.github.io/en-US/guide/performance)
- [React.memo Documentation](https://react.dev/reference/react/memo)
- [useMemo Documentation](https://react.dev/reference/react/useMemo)
- [useCallback Documentation](https://react.dev/reference/react/useCallback)
