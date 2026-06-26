# Recharts API Reference

Complete reference for all Recharts components, props, and configuration options.

## Table of Contents

1. [Chart Components](#chart-components)
2. [Cartesian Components](#cartesian-components)
3. [Polar Components](#polar-components)
4. [General Components](#general-components)
5. [Hooks](#hooks)
6. [Shapes](#shapes)

## Chart Components

### LineChart

Line and area visualizations with support for multiple series, tooltips, and animations.

```jsx
<LineChart
  data={array}              // Required: data array
  width={number}            // Width in px or percentage string
  height={number}           // Height in px or percentage string
  layout="horizontal"       // "horizontal" | "vertical"
  margin={{ top, right, bottom, left }}
  responsive={boolean}      // Auto-resize with container (v3.3+, recommended)
  style={object}            // CSS styles (useful with responsive for maxWidth, aspectRatio, etc.)
  accessibilityLayer={true} // Keyboard navigation and screen reader support (default: true)
  syncId="string"          // Synchronize with other charts
  onClick={func}
  onMouseMove={func}
  onMouseEnter={func}
  onMouseLeave={func}
>
```

**Child components**: XAxis, YAxis, CartesianGrid, Tooltip, Legend, Line, ReferenceLine, ReferenceArea, ReferenceDot, Brush

**Note**: The `responsive`, `style`, and `accessibilityLayer` props are available on all chart types (BarChart, AreaChart, PieChart, ScatterChart, ComposedChart, RadarChart, etc.).

### BarChart

Bar and column charts with stacking, grouping, and custom shapes.

```jsx
<BarChart
  data={array}
  layout="horizontal"
  barCategoryGap="10%"      // Gap between categories
  barGap={4}               // Gap between bars in same category
  barSize={number}         // Fixed bar width
  maxBarSize={number}      // Maximum bar width
  stackOffset="none"       // "none" | "expand" | "positive" | "sign" | "silhouette" | "wiggle"
>
```

**Key props**:
- `barCategoryGap`: Percentage or number for category spacing
- `barGap`: Pixels between bars in same group
- `barSize`: Fixed width/height (auto-calculated if not set)
- `stackOffset`: Strategy for stacked bars

### AreaChart

Filled area charts with gradients and stacking.

```jsx
<AreaChart
  data={array}
  baseValue="dataMin"      // Base for area fill: "dataMin" | "dataMax" | number
  stackOffset="none"
>
```

### PieChart

Pie and donut charts for proportional data.

```jsx
<PieChart
  width={number}
  height={number}
>
  <Pie
    data={array}
    dataKey="value"         // Required: numeric property
    nameKey="name"          // Property for labels
    cx="50%"               // Center X
    cy="50%"               // Center Y
    innerRadius={0}        // For donut chart
    outerRadius={number}    // Pie radius
    startAngle={0}         // Starting angle (degrees)
    endAngle={360}         // Ending angle
    minAngle={0}           // Minimum slice angle
    paddingAngle={0}       // Gap between slices
    label={false}          // Show labels
    labelLine={true}       // Line connecting labels
    isAnimationActive={true}
  />
</PieChart>
```

### ScatterChart

Scatter plots and bubble charts for correlated data.

```jsx
<ScatterChart
  width={number}
  height={number}
  margin={{ top, right, bottom, left }}
>
  <XAxis type="number" dataKey="x" />
  <YAxis type="number" dataKey="y" />
  <Scatter
    data={array}
    dataKey="y"
    fill="#8884d8"
    shape="circle"         // "circle" | "cross" | "diamond" | "square" | "star" | "triangle" | "wye" | function
    legendType="circle"
  />
</ScatterChart>
```

### ComposedChart

Mix multiple chart types (lines, bars, areas) in one chart.

```jsx
<ComposedChart data={array}>
  {/* Can include: Area, Bar, Line, Scatter, XAxis, YAxis, etc. */}
</ComposedChart>
```

### RadarChart

Radar/spider charts for multi-dimensional data.

```jsx
<RadarChart
  cx="50%"
  cy="50%"
  outerRadius={number}
  width={number}
  height={number}
  data={array}
>
  <PolarGrid />
  <PolarAngleAxis dataKey="subject" />
  <PolarRadiusAxis />
  <Radar
    name="Series"
    dataKey="A"
    stroke="#8884d8"
    fill="#8884d8"
    fillOpacity={0.6}
  />
</RadarChart>
```

### RadialBarChart

Circular bar charts.

```jsx
<RadialBarChart
  width={number}
  height={number}
  cx="50%"
  cy="50%"
  innerRadius={number}
  outerRadius={number}
  data={array}
  startAngle={90}
  endAngle={-270}
>
  <RadialBar dataKey="value" background clockWise />
  <Legend />
  <Tooltip />
</RadialBarChart>
```

### Treemap

Hierarchical data visualization.

```jsx
<Treemap
  width={number}
  height={number}
  data={array}
  dataKey="size"
  stroke="#fff"
  fill="#8884d8"
  aspectRatio={number}
  content={func}           // Custom render function
/>
```

### Sankey

Flow diagram for visualizing flow between nodes.

```jsx
<Sankey
  width={number}
  height={number}
  data={sankeyData}        // { nodes: [], links: [] }
  nodePadding={number}
  nodeWidth={number}
  linkCurvature={number}
  iterations={number}
>
```

### SunburstChart

Radial hierarchy visualization.

```jsx
<SunburstChart
  data={hierarchicalData}
  dataKey="value"
/>
```

## Cartesian Components

### XAxis / YAxis

Configure axes for Cartesian charts.

```jsx
<XAxis
  dataKey="name"          // Property for tick labels
  type="category"         // "category" | "number"
  domain={['auto', 'auto']}  // [min, max]
  range={array}          // Custom range
  scale="auto"           // "auto" | "linear" | "pow" | "sqrt" | "log" | "identity" | "time" | "band" | "point" | "ordinal" | function
  tick={object|element}   // Tick style or custom element
  tickLine={true}        // Show tick lines
  axisLine={true}        // Show axis line
  tickFormatter={func}    // Format tick labels
  ticks={array}          // Custom tick values
  interval="preserveEnd"  // "preserveStart" | "preserveEnd" | "preserveStartEnd" | number
  angle={0}              // Rotate labels
  height={30}            // Reserved height
  width={60}             // Reserved width
  label={{ value: 'text', position: 'insideBottom', offset: -10 }}
  orientation="bottom"    // "top" | "bottom" (XAxis) | "left" | "right" (YAxis)
  allowDataOverflow={false}
  allowDecimals={true}
  allowDuplicatedCategory={true}
  hide={false}
  mirror={false}
  reversed={false}
/>
```

### Line

Line series for LineChart and ComposedChart.

```jsx
<Pie
  data={array}
  dataKey="value"         // Required: numeric property
  nameKey="name"          // Property for labels
  cx="50%"               // Center X
  cy="50%"               // Center Y
  innerRadius={0}        // For donut chart
  outerRadius={number}    // Pie radius
  startAngle={0}         // Starting angle (degrees)
  endAngle={360}         // Ending angle
  minAngle={0}           // Minimum slice angle
  paddingAngle={0}       // Gap between slices
  label={false}          // Show labels
  labelLine={true}       // Line connecting labels
  shape={element|func}   // Custom slice render; receives isActive prop for active/inactive styling (replaces deprecated Cell, activeShape, inactiveShape)
  isAnimationActive={true}
/>
```

### Bar

Bar series for BarChart and ComposedChart.

```jsx
<Bar
  dataKey="value"
  name="Series Name"
  xAxisId={0}
  yAxisId={0}
  legendType="rect"
  stackId="a"           // Group into stacks
  barSize={20}          // Fixed bar size
  unit="k"              // Unit suffix
  fill="#8884d8"
  stroke="#8884d8"
  strokeWidth={1}
  radius={[4, 4, 0, 0]}  // Corner radii [tl, tr, br, bl]
  label={false}
  isAnimationActive={true}
  animationBegin={0}
  animationDuration={1500}
  animationEasing="ease"
  hide={false}
  background={false}    // Show background bars
  shape={element|func}  // Custom bar shape
  onClick={func}
  onMouseEnter={func}
  onMouseLeave={func}
/>
```

### Area

Area series for AreaChart and ComposedChart.

```jsx
<Area
  type="monotone"
  dataKey="value"
  name="Series Name"
  xAxisId={0}
  yAxisId={0}
  stackId="a"           // Stack areas
  unit="k"
  stroke="#8884d8"
  strokeWidth={1}
  fill="#8884d8"        // Solid fill
  fillOpacity={0.6}     // Opacity
  fill="url(#gradient)" // Gradient fill
  dot={false}
  activeDot={{ r: 8 }}
  label={false}
  isAnimationActive={true}
  animationDuration={1500}
  animationEasing="ease"
  legendType="line"
  connectNulls={false}
  hide={false}
  baseLine={number}     // Base value for fill
  onClick={func}
  onMouseEnter={func}
/>
```

### Scatter

Scatter plot points.

```jsx
<Scatter
  data={array}
  dataKey="y"
  name="Series Name"
  xAxisId={0}
  yAxisId={0}
  zAxisId={0}
  legendType="circle"
  line={false}          // Connect points with line
  lineType="joint"      // "joint" | "fitting"
  shape="circle"        // Shape or custom function
  fill="#8884d8"
  stroke="#8884d8"
  isAnimationActive={true}
  onClick={func}
>
  <ErrorBar dataKey="error" direction="x" />
  <ErrorBar dataKey="error" direction="y" />
</Scatter>
```

### CartesianGrid

Grid lines for Cartesian charts.

```jsx
<CartesianGrid
  strokeDasharray="3 3"  // Line pattern
  stroke="#ccc"         // Line color
  fill="none"           // Grid fill
  horizontal={true}     // Horizontal lines
  vertical={true}       // Vertical lines
  horizontalCoordinatesGenerator={func}
  verticalCoordinatesGenerator={func}
  x={number}
  y={number}
  width={number}
  height={number}
/>
```

### ReferenceLine

Horizontal or vertical reference line.

```jsx
<ReferenceLine
  x="value"             // X position for vertical line
  y={5000}              // Y position for horizontal line
  xAxisId={0}
  yAxisId={0}
  alwaysShow={false}
  isFront={false}       // Render on top
  stroke="red"
  strokeWidth={1}
  strokeDasharray="3 3"
  label={{ value: "Label", position: "center", fill: "red" }}
/>
```

### ReferenceArea

Highlighted rectangular region.

```jsx
<ReferenceArea
  x1="Jan"              // Start X
  x2="Mar"              // End X
  y1={0}                // Start Y
  y2={100}              // End Y
  xAxisId={0}
  yAxisId={0}
  alwaysShow={false}
  isFront={false}
  stroke="#8884d8"
  strokeWidth={1}
  fill="#8884d8"
  fillOpacity={0.3}
  label={{ value: "Area" }}
/>
```

### ReferenceDot

Highlighted point marker.

```jsx
<ReferenceDot
  x="value"
  y={number}
  xAxisId={0}
  yAxisId={0}
  isFront={false}
  alwaysShow={false}
  r={10}                // Radius
  stroke="#8884d8"
  strokeWidth={2}
  fill="#fff"
  label={{ value: "Point" }}
/>
```

### Brush

Zoom/scroll control for charts.

```jsx
<Brush
  dataKey="name"        // X-axis data key
  width={number}        // Brush width
  height={30}           // Brush height
  x={number}            // X position
  y={number}            // Y position
  startIndex={0}        // Initial start
  endIndex={data.length - 1}
  travellerWidth={5}    // Handle width
  stroke="#8884d8"
  fill="#fff"
  gap={1}               // Gap between items
  onChange={func}       // Selection change callback
  onDragEnd={func}
/>
```

### ErrorBar

Error indicators for scatter and bar charts.

```jsx
<ErrorBar
  dataKey="error"
  direction="x"         // "x" | "y"
  width={5}             // Error bar width
  strokeWidth={2}
/>
```

### ZAxis

Third dimension for bubble charts.

```jsx
<ZAxis
  type="number"
  dataKey="z"
  range={[60, 400]}     // Bubble size range
  unit="units"
/>
```

### Funnel

Funnel chart component (usually in FunnelChart).

```jsx
<Funnel
  dataKey="value"
  data={array}
  nameKey="name"
  isAnimationActive={true}
  animationDuration={1500}
  legendType={string}
/>
```

## Polar Components

### Pie

Pie chart slices.

```jsx
<Pie
  data={array}
  dataKey="value"
  nameKey="name"
  cx="50%"
  cy="50%"
  innerRadius={0}
  outerRadius={number}
  paddingAngle={0}
  startAngle={0}
  endAngle={360}
  minAngle={0}
  cornerRadius={0}      // Rounded corners
  cornerIsExternal={false}
  label={false}         // boolean | object | element | function
  labelLine={true}
  activeIndex={array}   // Currently active slice(s) — DEPRECATED in v3, use Tooltip defaultIndex instead
  activeShape={element|func}  // Active slice style — DEPRECATED, use shape prop with isActive
  shape={element|func}  // Custom slice render; receives isActive for active/inactive styling (replaces deprecated Cell, activeShape, inactiveShape)
  isAnimationActive={true}
  animationBegin={0}
  animationDuration={1500}
  animationEasing="ease"
  onClick={func}
  onMouseEnter={func}
/>

// Per-slice colors using shape prop (replaces deprecated Cell):
<Pie
  data={data}
  dataKey="value"
  shape={(props) => <Sector {...props} fill={COLORS[props.index % COLORS.length]} />}
/>
```

### Radar

Radar chart polygon.

```jsx
<Radar
  name="Series"
  dataKey="value"
  stroke="#8884d8"
  strokeWidth={1}
  fill="#8884d8"
  fillOpacity={0.6}
  isAnimationActive={true}
  legendType="line"
  dot={false}
/>
```

### RadialBar

Radial bar segments.

```jsx
<RadialBar
  dataKey="value"
  background={false}
  clockWise={true}
  minAngle={0}
  cornerRadius={0}
  isAnimationActive={true}
  legendType="circle"
/>
```

### PolarGrid

Grid for radar charts.

```jsx
<PolarGrid
  cx={number}
  cy={number}
  outerRadius={number}
  gridType="polygon"    // "polygon" | "circle"
/>
```

### PolarAngleAxis

Angular axis for radar charts.

```jsx
<PolarAngleAxis
  dataKey="subject"
  type="category"
  tick={object|element}
  tickFormatter={func}
/>
```

### PolarRadiusAxis

Radial axis for radar charts.

```jsx
<PolarRadiusAxis
  type="number"
  domain={[0, 'auto']}
  tick={object}
  tickFormatter={func}
  label={{ value: 'Label', angle: 90 }}
/>
```

## General Components

### ResponsiveContainer

Makes charts responsive to container size. **For Recharts < 3.3.** In Recharts 3.3+, prefer the `responsive` prop on chart components instead.

```jsx
<ResponsiveContainer
  width="100%"           // "100%" | number
  height={300}          // Required: number (NOT percentage)
  aspect={number}        // Aspect ratio (alternative to height)
  minWidth={number}
  minHeight={number}
  maxHeight={number}
  debounce={number}      // Resize debounce (ms)
  className={string}
  style={object}
>
  {/* Chart component */}
</ResponsiveContainer>
```

**Critical**: Height must be a number, not percentage. Parent element must have defined dimensions.

### Tooltip

Hover/click information display. Also controls active element highlighting (replaces removed `activeIndex` prop from v2).

```jsx
<Tooltip
  trigger="hover"         // "hover" (default) | "click"
  defaultIndex={number}   // Initial highlighted item index on render
  active={boolean}        // Force tooltip to stay active
  cursor={{ stroke: '#ccc', strokeWidth: 1 }}  // Cursor style, false to hide
  content={element|func}  // Custom content, () => null to hide text
  contentStyle={object}   // Container styles
  wrapperStyle={object}
  labelStyle={object}
  itemStyle={object}
  separator={" : "}
  formatter={(value, name, props) => [formattedValue, formattedName]}
  labelFormatter={(label) => formattedLabel}
  isAnimationActive={true}
  animationDuration={500}
  animationEasing="ease"
  itemSorter={func}       // Sort tooltip items
  filterNull={true}       // Hide null values
/>
```

**Custom Tooltip**:
```jsx
const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="custom-tooltip">
        <p className="label">{label}</p>
        {payload.map((entry, index) => (
          <p key={index} style={{ color: entry.color }}>
            {entry.name}: {entry.value}
          </p>
        ))}
      </div>
    );
  }
  return null;
};
```

### Legend

Series identification.

```jsx
<Legend
  layout="horizontal"     // "horizontal" | "vertical"
  align="center"         // "left" | "center" | "right"
  verticalAlign="bottom"  // "top" | "middle" | "bottom"
  iconType="line"         // "line" | "square" | "rect" | "circle" | "cross" | "diamond" | "star" | "triangle" | "wye"
  iconSize={14}
  content={element|func}  // Custom content
  payload={array}         // Custom data
  wrapperStyle={object}
  chartWidth={number}
  chartHeight={number}
  onClick={func}
  onMouseEnter={func}
  onMouseLeave={func}
/>
```

**Custom Legend**:
```jsx
const CustomLegend = ({ payload }) => (
  <ul>
    {payload.map((entry, index) => (
      <li key={`item-${index}`} style={{ color: entry.color }}>
        {entry.value}
      </li>
    ))}
  </ul>
);
```

### Label

Individual data point label.

```jsx
<Label
  value="Text"           // Label text
  position="top"         // "top" | "left" | "right" | "bottom" | "inside" | "outside" | "center"
  offset={5}             // Distance from element
  fill="#666"
  fontSize={12}
  formatter={func}
/>
```

### LabelList

List of labels for data series.

```jsx
<LabelList
  dataKey="value"        // Property for label text
  position="top"         // Label position
  offset={10}
  fill="#666"
  fontSize={12}
  formatter={func}       // Format function
  content={element|func}   // Custom label
/>

// Usage within series
<Bar dataKey="sales">
  <LabelList dataKey="sales" position="top" />
</Bar>
```

### Cell (DEPRECATED - removed in Recharts 4.0)

**Do not use in new code.** Use the `shape` prop on `Bar`, `Pie`, `Scatter`, etc. instead.

```jsx
// OLD (deprecated):
{data.map((entry, index) => (
  <Cell key={`cell-${index}`} fill={colors[index]} />
))}

// NEW (use shape prop):
<Bar dataKey="sales" shape={(props) => <Rectangle {...props} fill={colors[props.index]} />} />
<Pie dataKey="value" shape={(props) => <Sector {...props} fill={colors[props.index]} />} />
```

### Text

SVG text element.

```jsx
<Text
  x={number}
  y={number}
  textAnchor="start"      // "start" | "middle" | "end"
  width={number}          // Max width for wrapping
  scaleToFit={false}      // Scale text to fit width
  angle={0}               // Rotation
  lineHeight={string}     // Line height for multi-line
  capHeight={string}      // Capital letter height
  fill="#666"
  fontSize={14}
>
  Text content
</Text>
```

### Customized

Custom SVG elements with chart context.

```jsx
<Customized component={<CustomComponent />} />
```

### Layer

SVG group element.

```jsx
<Layer x={0} y={0} className={string}>
  {/* SVG elements */}
</Layer>
```

## Hooks

### useIsTooltipActive

```jsx
const isActive = useIsTooltipActive();
```

Returns boolean indicating if tooltip is currently active.

### useActiveTooltipCoordinate

```jsx
const coordinate = useActiveTooltipCoordinate();
// { x: number, y: number }
```

Returns coordinate of active tooltip.

### useActiveTooltipDataPoints

```jsx
const dataPoints = useActiveTooltipDataPoints();
```

Returns data points at active tooltip position.

### useActiveTooltipLabel

```jsx
const label = useActiveTooltipLabel();
```

Returns label of active tooltip.

### useCartesianScale

```jsx
const scale = useCartesianScale();
```

Returns Cartesian coordinate scale information.

### useXAxisScale / useYAxisScale

```jsx
const xScale = useXAxisScale(xAxisId);
const yScale = useYAxisScale(yAxisId);
```

Returns specific axis scale (data values to pixel coordinates).

### useXAxisInverseScale / useYAxisInverseScale

```jsx
const xInverse = useXAxisInverseScale(xAxisId);
const yInverse = useYAxisInverseScale(yAxisId);
```

Returns inverse scale (pixel coordinates to data values).

### useXAxisInverseDataSnapScale / useYAxisInverseDataSnapScale

```jsx
const xSnap = useXAxisInverseDataSnapScale(xAxisId);
const ySnap = useYAxisInverseDataSnapScale(yAxisId);
```

Returns inverse scale that snaps to nearest data point.

### useXAxisInverseTickSnapScale / useYAxisInverseTickSnapScale

```jsx
const xTickSnap = useXAxisInverseTickSnapScale(xAxisId);
const yTickSnap = useYAxisInverseTickSnapScale(yAxisId);
```

Returns inverse scale that snaps to nearest tick value.

### useXAxisDomain / useYAxisDomain

```jsx
const xDomain = useXAxisDomain(xAxisId);
const yDomain = useYAxisDomain(yAxisId);
```

Returns axis domain.

### useXAxisTicks / useYAxisTicks

```jsx
const xTicks = useXAxisTicks(xAxisId);
const yTicks = useYAxisTicks(yAxisId);
```

Returns axis tick information.

### useMargin

```jsx
const margin = useMargin();
// { top, right, bottom, left }
```

Returns chart margin.

### useOffset

```jsx
const offset = useOffset();
// { top, left }
```

Returns chart offset.

### usePlotArea

```jsx
const plotArea = usePlotArea();
// { x, y, width, height }
```

Returns plot area dimensions.

### useChartWidth / useChartHeight

```jsx
const width = useChartWidth();
const height = useChartHeight();
```

Returns chart dimensions.

## Shapes

### Rectangle

```jsx
<Rectangle
  x={number}
  y={number}
  width={number}
  height={number}
  radius={[tl, tr, br, bl]}
  fill="none"
  stroke="#000"
  strokeWidth={1}
/>
```

### Circle / Dot

```jsx
<Dot
  cx={number}
  cy={number}
  r={number}
  fill="#8884d8"
  stroke="#8884d8"
  strokeWidth={1}
/>
```

### Sector

```jsx
<Sector
  cx={number}
  cy={number}
  innerRadius={number}
  outerRadius={number}
  startAngle={number}
  endAngle={number}
  fill="#8884d8"
/>
```

### Symbols

```jsx
<Symbols
  cx={number}
  cy={number}
  size={number}
  type="circle"         // "circle" | "cross" | "diamond" | "square" | "star" | "triangle" | "wye"
  fill="#8884d8"
/>
```

### Polygon

```jsx
<Polygon
  points={[{x, y}, ...]}
  fill="none"
  stroke="#000"
/>
```

### Curve

```jsx
<Curve
  type="monotone"
  points={[{x, y}, ...]}
  stroke="#8884d8"
  fill="none"
/>
```

### Cross

```jsx
<Cross
  x={number}
  y={number}
  width={number}
  height={number}
  stroke="#000"
/>
```

### Trapezoid

```jsx
<Trapezoid
  x={number}
  y={number}
  upperWidth={number}
  lowerWidth={number}
  height={number}
  fill="#8884d8"
/>
```

## Utility Functions

### getNiceTickValues

Generate nice axis tick values.

```jsx
import { getNiceTickValues } from 'recharts';

const ticks = getNiceTickValues([0, 100], 5);
// [0, 20, 40, 60, 80, 100]
```

### getRelativeCoordinate

Convert screen coordinates to chart coordinates.

```jsx
import { getRelativeCoordinate } from 'recharts';

const chartPoint = getRelativeCoordinate(event, chartContainer);
// { x, y }
```

## Global Configuration

### RechartsGlobal

Configure global defaults.

```jsx
import { Global } from 'recharts';

<Global 
  isSsrMode={false}      // Server-side rendering mode
/>
```

## Z-Index and Layering

### ZIndexLayer

```jsx
<ZIndexLayer zIndex={number}>
  {/* Components at this z-index */}
</ZIndexLayer>
```

### Default Z-Index Values

Default layer ordering:
- Grid: 0
- Axes: 1
- Chart elements: 2
- Tooltip/Legend: 5

Use `isFront` prop on reference elements to render above chart.
