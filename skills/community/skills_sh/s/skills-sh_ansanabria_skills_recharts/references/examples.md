# Recharts Examples

Common chart patterns and implementation examples.

> **Note**: Examples below use `ResponsiveContainer` for broad compatibility. In Recharts 3.3+, you can use the `responsive` prop instead:
> ```jsx
> <LineChart data={data} responsive style={{ width: '100%', height: 300 }}>
> ```

## Table of Contents

1. [Line Chart Patterns](#line-chart-patterns)
2. [Bar Chart Patterns](#bar-chart-patterns)
3. [Area Chart Patterns](#area-chart-patterns)
4. [Pie Chart Patterns](#pie-chart-patterns)
5. [Scatter Chart Patterns](#scatter-chart-patterns)
6. [Composed Chart Patterns](#composed-chart-patterns)
7. [Advanced Patterns](#advanced-patterns)

## Line Chart Patterns

### Basic Line Chart

```jsx
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const data = [
  { month: 'Jan', sales: 4000, profit: 2400 },
  { month: 'Feb', sales: 3000, profit: 1398 },
  { month: 'Mar', sales: 2000, profit: 9800 },
  { month: 'Apr', sales: 2780, profit: 3908 },
  { month: 'May', sales: 1890, profit: 4800 },
  { month: 'Jun', sales: 2390, profit: 3800 },
];

function SimpleLineChart() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="sales" stroke="#8884d8" />
        <Line type="monotone" dataKey="profit" stroke="#82ca9d" />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

### Dashed Line Chart

```jsx
<LineChart data={data}>
  <XAxis dataKey="month" />
  <YAxis />
  <CartesianGrid strokeDasharray="3 3" />
  <Tooltip />
  <Line 
    type="monotone" 
    dataKey="sales" 
    stroke="#8884d8" 
    strokeDasharray="5 5"  // Dashed pattern
  />
</LineChart>
```

### Vertical Line Chart

```jsx
<LineChart layout="vertical" data={data}>
  <XAxis type="number" />
  <YAxis type="category" dataKey="month" />
  <CartesianGrid strokeDasharray="3 3" />
  <Tooltip />
  <Legend />
  <Line type="monotone" dataKey="sales" stroke="#8884d8" />
</LineChart>
```

### Line Chart with Custom Dots

```jsx
const CustomDot = (props) => {
  const { cx, cy, stroke, payload, value } = props;
  
  return (
    <svg x={cx - 10} y={cy - 10} width={20} height={20} fill={stroke} viewBox="0 0 1024 1024">
      <path d="M512 0C229.25 0 0 229.25 0 512s229.25 512 512 512 512-229.25 512-512S794.75 0 512 0z" />
    </svg>
  );
};

<LineChart data={data}>
  <XAxis dataKey="month" />
  <YAxis />
  <CartesianGrid strokeDasharray="3 3" />
  <Tooltip />
  <Line 
    type="monotone" 
    dataKey="sales" 
    stroke="#8884d8"
    dot={<CustomDot />}
    activeDot={{ r: 8 }}
  />
</LineChart>
```

### Synchronized Multi-Chart

```jsx
<>
  <ResponsiveContainer width="100%" height={200}>
    <LineChart data={data} syncId="salesSync">
      <XAxis dataKey="month" />
      <YAxis />
      <CartesianGrid strokeDasharray="3 3" />
      <Tooltip />
      <Line type="monotone" dataKey="sales" stroke="#8884d8" />
    </LineChart>
  </ResponsiveContainer>
  
  <ResponsiveContainer width="100%" height={200}>
    <LineChart data={data} syncId="salesSync">
      <XAxis dataKey="month" />
      <YAxis />
      <CartesianGrid strokeDasharray="3 3" />
      <Tooltip />
      <Line type="monotone" dataKey="profit" stroke="#82ca9d" />
    </LineChart>
  </ResponsiveContainer>
  
  <p>Charts share synchronized tooltips</p>
</>
```

### Highlight and Zoom

```jsx
import { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Brush } from 'recharts';

function HighlightZoomChart({ data }) {
  const [refAreaLeft, setRefAreaLeft] = useState('');
  const [refAreaRight, setRefAreaRight] = useState('');
  const [zoomData, setZoomData] = useState(data);

  const zoom = () => {
    if (refAreaLeft === refAreaRight || refAreaRight === '') {
      setRefAreaLeft('');
      setRefAreaRight('');
      return;
    }

    // Filter data between selected range
    const left = Math.min(refAreaLeft, refAreaRight);
    const right = Math.max(refAreaLeft, refAreaRight);
    
    const newData = data.filter(
      (d) => d.index >= left && d.index <= right
    );
    
    setZoomData(newData);
    setRefAreaLeft('');
    setRefAreaRight('');
  };

  return (
    <LineChart
      data={zoomData}
      onMouseDown={(e) => e && setRefAreaLeft(e.activeLabel)}
      onMouseMove={(e) => e && refAreaLeft && setRefAreaRight(e.activeLabel)}
      onMouseUp={zoom}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="name" allowDataOverflow />
      <YAxis allowDataOverflow />
      <Tooltip />
      <Line type="monotone" dataKey="value" stroke="#8884d8" />
      
      {refAreaLeft && refAreaRight && (
        <ReferenceArea
          x1={refAreaLeft}
          x2={refAreaRight}
          strokeOpacity={0.3}
        />
      )}
    </LineChart>
  );
}
```

## Bar Chart Patterns

### Basic Bar Chart

```jsx
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function SimpleBarChart() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="sales" fill="#8884d8" />
        <Bar dataKey="profit" fill="#82ca9d" />
      </BarChart>
    </ResponsiveContainer>
  );
}
```

### Stacked Bar Chart

```jsx
<BarChart data={data}>
  <XAxis dataKey="month" />
  <YAxis />
  <CartesianGrid strokeDasharray="3 3" />
  <Tooltip />
  <Legend />
  <Bar dataKey="sales" stackId="a" fill="#8884d8" />
  <Bar dataKey="profit" stackId="a" fill="#82ca9d" />
  <Bar dataKey="expenses" stackId="a" fill="#ffc658" />
</BarChart>
```

### Horizontal Bar Chart

```jsx
<BarChart layout="vertical" data={data}>
  <XAxis type="number" />
  <YAxis type="category" dataKey="month" />
  <CartesianGrid strokeDasharray="3 3" />
  <Tooltip />
  <Legend />
  <Bar dataKey="sales" fill="#8884d8" />
</BarChart>
```

### Grouped Bar Chart

```jsx
<BarChart data={data}>
  <XAxis dataKey="month" />
  <YAxis />
  <CartesianGrid strokeDasharray="3 3" />
  <Tooltip />
  <Legend />
  {/* No stackId = side by side */}
  <Bar dataKey="sales" fill="#8884d8" />
  <Bar dataKey="profit" fill="#82ca9d" />
</BarChart>
```

### Bar Chart with Custom Shape

```jsx
const CustomBarShape = (props) => {
  const { fill, x, y, width, height } = props;
  
  return (
    <g>
      <rect x={x} y={y} width={width} height={height} rx={5} ry={5} fill={fill} />
      <text x={x + width / 2} y={y - 5} textAnchor="middle" fill="#666">
        {props.value}
      </text>
    </g>
  );
};

<BarChart data={data}>
  <XAxis dataKey="month" />
  <YAxis />
  <CartesianGrid strokeDasharray="3 3" />
  <Tooltip />
  <Bar dataKey="sales" fill="#8884d8" shape={<CustomBarShape />} />
</BarChart>
```

### Rounded Corners

```jsx
<BarChart data={data}>
  <XAxis dataKey="month" />
  <YAxis />
  <CartesianGrid strokeDasharray="3 3" />
  <Tooltip />
  <Bar 
    dataKey="sales" 
    fill="#8884d8"
    radius={[4, 4, 0, 0]}  // [topLeft, topRight, bottomRight, bottomLeft]
  />
</BarChart>
```

### Brush-enabled Bar Chart

```jsx
<BarChart data={data}>
  <CartesianGrid strokeDasharray="3 3" />
  <XAxis dataKey="name" />
  <YAxis />
  <Tooltip />
  <Legend />
  <Bar dataKey="pv" fill="#8884d8" />
  <Bar dataKey="uv" fill="#82ca9d" />
  <Brush dataKey="name" height={30} stroke="#8884d8" />
</BarChart>
```

## Area Chart Patterns

### Basic Area Chart

```jsx
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function SimpleAreaChart() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <AreaChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Area type="monotone" dataKey="sales" stroke="#8884d8" fill="#8884d8" />
      </AreaChart>
    </ResponsiveContainer>
  );
}
```

### Area Chart with Gradient

```jsx
<AreaChart data={data}>
  <defs>
    <linearGradient id="colorSales" x1="0" y1="0" x2="0" y2="1">
      <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8}/>
      <stop offset="95%" stopColor="#8884d8" stopOpacity={0}/>
    </linearGradient>
  </defs>
  <XAxis dataKey="month" />
  <YAxis />
  <CartesianGrid strokeDasharray="3 3" />
  <Tooltip />
  <Area 
    type="monotone" 
    dataKey="sales" 
    stroke="#8884d8" 
    fillOpacity={1} 
    fill="url(#colorSales)" 
  />
</AreaChart>
```

### Stacked Area Chart

```jsx
<AreaChart data={data}>
  <CartesianGrid strokeDasharray="3 3" />
  <XAxis dataKey="month" />
  <YAxis />
  <Tooltip />
  <Legend />
  <Area 
    type="monotone" 
    dataKey="sales" 
    stackId="1" 
    stroke="#8884d8" 
    fill="#8884d8" 
  />
  <Area 
    type="monotone" 
    dataKey="profit" 
    stackId="1" 
    stroke="#82ca9d" 
    fill="#82ca9d" 
  />
</AreaChart>
```

### Percent Area Chart

```jsx
<AreaChart data={data} stackOffset="expand">
  <CartesianGrid strokeDasharray="3 3" />
  <XAxis dataKey="month" />
  <YAxis tickFormatter={(value) => `${(value * 100).toFixed(0)}%`} />
  <Tooltip formatter={(value) => `${(value * 100).toFixed(0)}%`} />
  <Legend />
  <Area type="monotone" dataKey="sales" stackId="1" stroke="#8884d8" fill="#8884d8" />
  <Area type="monotone" dataKey="profit" stackId="1" stroke="#82ca9d" fill="#82ca9d" />
</AreaChart>
```

## Pie Chart Patterns

### Basic Pie Chart

```jsx
import { PieChart, Pie, Sector, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const data = [
  { name: 'Group A', value: 400 },
  { name: 'Group B', value: 300 },
  { name: 'Group C', value: 300 },
  { name: 'Group D', value: 200 },
];

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

function SimplePieChart() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
          outerRadius={80}
          dataKey="value"
          shape={(props) => <Sector {...props} fill={COLORS[props.index % COLORS.length]} />}
        />
        <Tooltip />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
}
```

### Donut Chart

```jsx
<PieChart>
  <Pie
    data={data}
    cx="50%"
    cy="50%"
    innerRadius={60}
    outerRadius={80}
    paddingAngle={5}
    dataKey="value"
    shape={(props) => <Sector {...props} fill={COLORS[props.index % COLORS.length]} />}
  />
  <Tooltip />
</PieChart>
```

### Two-Level Pie Chart

```jsx
<PieChart>
  <Pie
    data={data01}
    dataKey="value"
    nameKey="name"
    cx="50%"
    cy="50%"
    outerRadius={50}
    fill="#8884d8"
  />
  <Pie
    data={data02}
    dataKey="value"
    nameKey="name"
    cx="50%"
    cy="50%"
    innerRadius={60}
    outerRadius={80}
    fill="#82ca9d"
    label
  />
</PieChart>
```

### Pie Chart with Active Slice

```jsx
import { PieChart, Pie, Sector, Tooltip } from 'recharts';

// Use the `shape` prop with `isActive` to render active/inactive slices differently.
// `activeShape` and `activeIndex` props are deprecated — use `shape` instead.

const renderShape = (props) => {
  const { cx, cy, midAngle, innerRadius, outerRadius, startAngle, endAngle, fill, payload, percent, value, isActive } = props;
  
  if (!isActive) {
    return <Sector {...props} />;
  }
  
  // Expanded active slice with label
  return (
    <g>
      <text x={cx} y={cy} dy={8} textAnchor="middle" fill={fill}>
        {payload.name}
      </text>
      <Sector
        cx={cx}
        cy={cy}
        innerRadius={innerRadius}
        outerRadius={outerRadius}
        startAngle={startAngle}
        endAngle={endAngle}
        fill={fill}
      />
      <Sector
        cx={cx}
        cy={cy}
        startAngle={startAngle}
        endAngle={endAngle}
        innerRadius={outerRadius + 6}
        outerRadius={outerRadius + 10}
        fill={fill}
      />
    </g>
  );
};

function ActivePieChart() {
  return (
    <PieChart width={400} height={400}>
      <Pie
        data={data}
        cx="50%"
        cy="50%"
        innerRadius={60}
        outerRadius={80}
        dataKey="value"
        shape={renderShape}
      />
      <Tooltip defaultIndex={0} />
    </PieChart>
  );
}
```

## Scatter Chart Patterns

### Basic Scatter Chart

```jsx
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
  { x: 100, y: 200, z: 200 },
  { x: 120, y: 100, z: 260 },
  { x: 170, y: 300, z: 400 },
  { x: 140, y: 250, z: 280 },
  { x: 150, y: 400, z: 500 },
];

function SimpleScatterChart() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <ScatterChart>
        <CartesianGrid />
        <XAxis type="number" dataKey="x" name="X" unit="px" />
        <YAxis type="number" dataKey="y" name="Y" unit="px" />
        <Tooltip cursor={{ strokeDasharray: '3 3' }} />
        <Scatter name="Series A" data={data} fill="#8884d8" />
      </ScatterChart>
    </ResponsiveContainer>
  );
}
```

### Bubble Chart

```jsx
<ScatterChart>
  <CartesianGrid />
  <XAxis type="number" dataKey="x" name="X" />
  <YAxis type="number" dataKey="y" name="Y" />
  <ZAxis type="number" dataKey="z" range={[100, 500]} name="Size" />
  <Tooltip cursor={{ strokeDasharray: '3 3' }} />
  <Legend />
  <Scatter name="Group A" data={data01} fill="#8884d8" />
  <Scatter name="Group B" data={data02} fill="#82ca9d" />
</ScatterChart>
```

### Scatter with Trend Line

```jsx
import { LineChart, Line, XAxis, YAxis, Tooltip, ReferenceLine } from 'recharts';

function ScatterWithTrend() {
  // Calculate trend line
  const n = data.length;
  const sumX = data.reduce((sum, d) => sum + d.x, 0);
  const sumY = data.reduce((sum, d) => sum + d.y, 0);
  const sumXY = data.reduce((sum, d) => sum + d.x * d.y, 0);
  const sumX2 = data.reduce((sum, d) => sum + d.x * d.x, 0);
  
  const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
  const intercept = (sumY - slope * sumX) / n;
  
  const minX = Math.min(...data.map(d => d.x));
  const maxX = Math.max(...data.map(d => d.x));
  
  return (
    <ScatterChart>
      <CartesianGrid />
      <XAxis type="number" dataKey="x" domain={[minX, maxX]} />
      <YAxis type="number" dataKey="y" />
      <Tooltip cursor={{ strokeDasharray: '3 3' }} />
      <Scatter data={data} fill="#8884d8" />
      <ReferenceLine 
        segment={[
          { x: minX, y: slope * minX + intercept },
          { x: maxX, y: slope * maxX + intercept }
        ]} 
        stroke="red" 
        strokeDasharray="3 3" 
      />
    </ScatterChart>
  );
}
```

## Composed Chart Patterns

### Line + Bar + Area

```jsx
import { ComposedChart, Line, Bar, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

function MixedChart() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <ComposedChart data={data}>
        <CartesianGrid stroke="#f5f5f5" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Area type="monotone" dataKey="total" fill="#8884d8" stroke="#8884d8" />
        <Bar dataKey="sales" barSize={20} fill="#413ea0" />
        <Line type="monotone" dataKey="profit" stroke="#ff7300" />
      </ComposedChart>
    </ResponsiveContainer>
  );
}
```

### Dual Y-Axis Chart

```jsx
<ComposedChart data={data}>
  <CartesianGrid stroke="#f5f5f5" />
  <XAxis dataKey="name" />
  <YAxis yAxisId="left" />
  <YAxis yAxisId="right" orientation="right" />
  <Tooltip />
  <Legend />
  <Bar yAxisId="left" dataKey="sales" fill="#8884d8" />
  <Line yAxisId="right" type="monotone" dataKey="rate" stroke="#ff7300" />
</ComposedChart>
```

## Advanced Patterns

### Real-time Chart

```jsx
import { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';

function RealtimeChart() {
  const [data, setData] = useState([]);
  
  useEffect(() => {
    let counter = 0;
    const interval = setInterval(() => {
      setData(prev => {
        const newData = [...prev, {
          time: new Date().toLocaleTimeString(),
          value: Math.floor(Math.random() * 100),
          index: counter++
        }].slice(-20); // Keep last 20 points
        return newData;
      });
    }, 1000);
    
    return () => clearInterval(interval);
  }, []);
  
  return (
    <LineChart data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="time" interval="preserveStartEnd" />
      <YAxis domain={[0, 100]} />
      <Tooltip />
      <Line 
        type="monotone" 
        dataKey="value" 
        stroke="#8884d8" 
        isAnimationActive={false}  // Disable for performance
        dot={false}
      />
    </LineChart>
  );
}
```

### Chart with Custom Tooltip

```jsx
const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div style={{ 
        backgroundColor: '#fff', 
        padding: '10px', 
        border: '1px solid #ccc',
        borderRadius: '4px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
      }}>
        <p style={{ margin: 0, fontWeight: 'bold' }}>{label}</p>
        {payload.map((entry, index) => (
          <p key={index} style={{ 
            margin: '5px 0 0 0', 
            color: entry.color,
            fontSize: '14px'
          }}>
            {entry.name}: {entry.value.toLocaleString()}
          </p>
        ))}
      </div>
    );
  }
  return null;
};

<LineChart data={data}>
  <XAxis dataKey="month" />
  <YAxis />
  <Tooltip content={<CustomTooltip />} />
  <Line type="monotone" dataKey="sales" stroke="#8884d8" />
</LineChart>
```

### Chart with Reference Elements

```jsx
<LineChart data={data}>
  <CartesianGrid strokeDasharray="3 3" />
  <XAxis dataKey="month" />
  <YAxis />
  <Tooltip />
  <Legend />
  
  {/* Target line */}
  <ReferenceLine 
    y={5000} 
    label="Target" 
    stroke="red" 
    strokeDasharray="3 3" 
  />
  
  {/* Highlighted period */}
  <ReferenceArea 
    x1="Feb" 
    x2="Apr" 
    label="Campaign" 
    fill="#8884d8" 
    fillOpacity={0.1} 
  />
  
  {/* Important point */}
  <ReferenceDot 
    x="Jun" 
    y={9800} 
    r={8} 
    fill="gold" 
    stroke="orange" 
    label="Peak" 
  />
  
  <Line type="monotone" dataKey="sales" stroke="#8884d8" />
</LineChart>
```

### Treemap

```jsx
import { Treemap, Tooltip } from 'recharts';

const treemapData = [
  { name: 'A', size: 100, children: [
    { name: 'A1', size: 30 },
    { name: 'A2', size: 40 },
    { name: 'A3', size: 30 },
  ]},
  { name: 'B', size: 80, children: [
    { name: 'B1', size: 25 },
    { name: 'B2', size: 55 },
  ]},
];

<Treemap
  width={400}
  height={200}
  data={treemapData}
  dataKey="size"
  stroke="#fff"
  fill="#8884d8"
  content={({ x, y, width, height, index, name, value }) => (
    <g>
      <rect x={x} y={y} width={width} height={height} fill={COLORS[index % COLORS.length]} stroke="#fff" />
      {width > 50 && height > 30 && (
        <text x={x + 10} y={y + 20} fill="#fff" fontSize={12}>
          {name} ({value})
        </text>
      )}
    </g>
  )}
/>
```

### Sankey Diagram

```jsx
import { Sankey } from 'recharts';

const sankeyData = {
  nodes: [
    { name: 'Source A' },
    { name: 'Source B' },
    { name: 'Target X' },
    { name: 'Target Y' },
  ],
  links: [
    { source: 0, target: 2, value: 10 },
    { source: 0, target: 3, value: 5 },
    { source: 1, target: 2, value: 8 },
    { source: 1, target: 3, value: 12 },
  ],
};

<Sankey
  width={400}
  height={300}
  data={sankeyData}
  nodePadding={20}
  nodeWidth={20}
  linkCurvature={0.5}
>
  <Tooltip />
</Sankey>
```

### Radar Chart

```jsx
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, Legend } from 'recharts';

const radarData = [
  { subject: 'Math', A: 120, B: 110, fullMark: 150 },
  { subject: 'English', A: 98, B: 130, fullMark: 150 },
  { subject: 'Physics', A: 86, B: 130, fullMark: 150 },
  { subject: 'Chemistry', A: 99, B: 100, fullMark: 150 },
  { subject: 'Biology', A: 85, B: 90, fullMark: 150 },
  { subject: 'History', A: 65, B: 85, fullMark: 150 },
];

<RadarChart cx="50%" cy="50%" outerRadius="80%" data={radarData}>
  <PolarGrid />
  <PolarAngleAxis dataKey="subject" />
  <PolarRadiusAxis angle={30} domain={[0, 150]} />
  <Radar name="Student A" dataKey="A" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
  <Radar name="Student B" dataKey="B" stroke="#82ca9d" fill="#82ca9d" fillOpacity={0.6} />
  <Legend />
  <Tooltip />
</RadarChart>
```

### Custom Axis Tick

```jsx
const CustomTick = ({ x, y, stroke, payload }) => (
  <g transform={`translate(${x},${y})`}>
    <text x={0} y={0} dy={16} textAnchor="end" fill="#666" transform="rotate(-35)">
      {payload.value}
    </text>
  </g>
);

<XAxis dataKey="month" tick={<CustomTick />} height={60} />
```

### Performance-Optimized Large Dataset

```jsx
import { useMemo, useCallback } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip } from 'recharts';

function OptimizedChart({ rawData }) {
  // Memoize data processing
  const data = useMemo(() => {
    // Aggregate or sample data if too large
    if (rawData.length > 1000) {
      return rawData.filter((_, i) => i % Math.ceil(rawData.length / 500) === 0);
    }
    return rawData;
  }, [rawData]);
  
  // Stable callback for dataKey if using function
  const dataKey = useCallback((entry) => entry.value, []);
  
  // Memoized tooltip
  const tooltipContent = useMemo(() => <CustomTooltip />, []);
  
  return (
    <LineChart data={data}>
      <XAxis dataKey="time" interval="preserveStartEnd" />
      <YAxis domain={['auto', 'auto']} />
      <Tooltip content={tooltipContent} />
      <Line 
        type="monotone" 
        dataKey={dataKey}
        stroke="#8884d8"
        dot={false}  // Disable dots for performance
        isAnimationActive={false}  // Disable animation
      />
    </LineChart>
  );
}
```
