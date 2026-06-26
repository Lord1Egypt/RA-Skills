# Funnel and Pyramid Charts

## Table of Contents
- [Overview](#overview)
- [Funnel Chart Basics](#funnel-chart-basics)
- [Funnel Size Customization](#funnel-size-customization)
- [Neck Size Configuration](#neck-size-configuration)
- [Gap Between Segments](#gap-between-segments)
- [Funnel Rendering Modes](#funnel-rendering-modes)
- [Pyramid Chart Basics](#pyramid-chart-basics)
- [Pyramid Rendering Modes](#pyramid-rendering-modes)
- [Pyramid Size Customization](#pyramid-size-customization)
- [Explode Effects](#explode-effects)
- [Smart Data Labels for Funnels](#smart-data-labels-for-funnels)

## Overview

**Funnel Charts** represent data in a progressively decreasing manner, ideal for:
- Sales funnels showing conversion rates
- Process stages with drop-offs
- Filtering or reduction workflows
- Lead generation pipelines

**Pyramid Charts** display hierarchical data in a triangular format, useful for:
- Population demographics
- Organizational structures
- Priority hierarchies
- Resource allocation

## Funnel Chart Basics

To create a funnel chart, inject `FunnelSeries` module and set series type to 'Funnel':

```tsx
import { 
  AccumulationChartComponent,
  AccumulationSeriesCollectionDirective,
  AccumulationSeriesDirective,
  Inject,
  FunnelSeries,
  AccumulationDataLabel
} from '@syncfusion/ej2-react-charts';

function FunnelChart() {
  const salesFunnelData = [
    { stage: 'Website Visits', count: 10000 },
    { stage: 'Sign Ups', count: 5000 },
    { stage: 'Active Users', count: 3000 },
    { stage: 'Premium Users', count: 1500 },
    { stage: 'Retained', count: 1200 }
  ];

  return (
    <AccumulationChartComponent 
      id='funnel-chart'
      title='Sales Conversion Funnel'
    >
      <Inject services={[FunnelSeries, AccumulationDataLabel]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective 
          dataSource={salesFunnelData}
          xName='stage'
          yName='count'
          type='Funnel'
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Funnel Size Customization

Customize funnel dimensions using `width` and `height` properties:

```tsx
<AccumulationSeriesDirective 
  dataSource={data}
  xName='stage'
  yName='value'
  type='Funnel'
  width='60%'   // Funnel width relative to container
  height='80%'  // Funnel height relative to container
/>
```

**Size guidelines:**
- **width**: '40%'-'80%' (default: '80%')
- **height**: '60%'-'90%' (default: '80%')
- Smaller values create more white space around funnel
- Larger values maximize funnel size

**Responsive sizing example:**

```tsx
function ResponsiveFunnel() {
  const data = [
    { x: 'Stage 1', y: 100 },
    { x: 'Stage 2', y: 80 },
    { x: 'Stage 3', y: 60 },
    { x: 'Stage 4', y: 40 }
  ];

  return (
    <AccumulationChartComponent 
      id='responsive-funnel'
      height='400px'
      width='100%'
    >
      <Inject services={[FunnelSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective 
          dataSource={data}
          xName='x'
          yName='y'
          type='Funnel'
          width='70%'
          height='85%'
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Neck Size Configuration

The funnel "neck" is the narrow section at the bottom. Customize it using `neckWidth` and `neckHeight`:

```tsx
<AccumulationSeriesDirective 
  dataSource={data}
  xName='stage'
  yName='count'
  type='Funnel'
  neckWidth='25%'   // Width of neck (0%-100%)
  neckHeight='5%'   // Height of neck (0%-100%)
/>
```

**Neck sizing effects:**

**Wide neck (neckWidth='50%'):**
- Less dramatic taper
- Better for data with less variation

**Narrow neck (neckWidth='15%'):**
- More dramatic funnel shape
- Emphasizes reduction/conversion

**Tall neck (neckHeight='20%'):**
- Longer neck section
- Good for showing final stable stage

**Short neck (neckHeight='5%'):**
- Minimal neck
- More traditional funnel shape

**Complete example:**

```tsx
function CustomNeckFunnel() {
  const data = [
    { x: 'Leads', y: 1000 },
    { x: 'Qualified', y: 600 },
    { x: 'Proposals', y: 400 },
    { x: 'Negotiations', y: 250 },
    { x: 'Closed', y: 150 }
  ];

  return (
    <AccumulationChartComponent 
      id='custom-neck'
      title='Sales Pipeline'
    >
      <Inject services={[FunnelSeries, AccumulationDataLabel]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective 
          dataSource={data}
          xName='x'
          yName='y'
          type='Funnel'
          neckWidth='20%'
          neckHeight='10%'
          dataLabel={{ visible: true, position: 'Outside' }}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Gap Between Segments

Add spacing between funnel segments using `gapRatio` (value from 0 to 1):

```tsx
<AccumulationSeriesDirective 
  dataSource={data}
  xName='x'
  yName='y'
  type='Funnel'
  gapRatio={0.08}  // 8% gap between segments
/>
```

**Gap ratio values:**
- `0`: No gap (segments touch)
- `0.05`: Subtle separation
- `0.08`-`0.10`: Standard gap
- `0.15`+: Wide separation

**Use gaps when:**
- You want clear visual separation
- Highlighting individual stages
- Improving readability with many segments

```tsx
function GappedFunnel() {
  const processData = [
    { step: 'Raw Materials', qty: 10000 },
    { step: 'Processing', qty: 8000 },
    { step: 'Quality Check', qty: 7500 },
    { step: 'Packaging', qty: 7000 },
    { step: 'Distribution', qty: 6800 }
  ];

  return (
    <AccumulationChartComponent id='gapped-funnel'>
      <Inject services={[FunnelSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective 
          dataSource={processData}
          xName='step'
          yName='qty'
          type='Funnel'
          gapRatio={0.1}
          width='65%'
          height='80%'
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Funnel Rendering Modes

Funnels support two rendering modes via the `funnelMode` property:

### Standard Mode (Default)

Traditional funnel shape with continuous width narrowing:

```tsx
<AccumulationSeriesDirective 
  dataSource={data}
  xName='x'
  yName='y'
  type='Funnel'
  funnelMode='Standard'  // Default
/>
```

**Characteristics:**
- Width continuously narrows to a point
- Classic funnel appearance
- Good for showing progressive reduction

### Trapezoidal Mode

Modified funnel with flattened sections, creating trapezoidal shapes:

```tsx
<AccumulationSeriesDirective 
  dataSource={data}
  xName='x'
  yName='y'
  type='Funnel'
  funnelMode='Trapezoidal'
/>
```

**Characteristics:**
- Each segment has parallel top and bottom
- Easier to compare segment sizes
- Better for data analysis

**Mode comparison example:**

```tsx
function FunnelModeComparison() {
  const data = [
    { x: 'Awareness', y: 100 },
    { x: 'Interest', y: 75 },
    { x: 'Consideration', y: 50 },
    { x: 'Intent', y: 30 },
    { x: 'Purchase', y: 15 }
  ];

  return (
    <div style={{ display: 'flex', gap: '20px' }}>
      <AccumulationChartComponent 
        id='standard-funnel'
        title='Standard Mode'
      >
        <Inject services={[FunnelSeries]} />
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective 
            dataSource={data}
            xName='x'
            yName='y'
            type='Funnel'
            funnelMode='Standard'
          />
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>

      <AccumulationChartComponent 
        id='trapezoidal-funnel'
        title='Trapezoidal Mode'
      >
        <Inject services={[FunnelSeries]} />
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective 
            dataSource={data}
            xName='x'
            yName='y'
            type='Funnel'
            funnelMode='Trapezoidal'
          />
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>
    </div>
  );
}
```

## Pyramid Chart Basics

Create a pyramid chart by injecting `PyramidSeries` and setting type to 'Pyramid':

```tsx
import { 
  AccumulationChartComponent,
  AccumulationSeriesCollectionDirective,
  AccumulationSeriesDirective,
  Inject,
  PyramidSeries
} from '@syncfusion/ej2-react-charts';

function PyramidChart() {
  const populationData = [
    { age: '0-14', population: 1.5 },
    { age: '15-24', population: 1.3 },
    { age: '25-54', population: 3.0 },
    { age: '55-64', population: 1.2 },
    { age: '65+', population: 1.0 }
  ];

  return (
    <AccumulationChartComponent 
      id='pyramid-chart'
      title='Age Distribution'
    >
      <Inject services={[PyramidSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective 
          dataSource={populationData}
          xName='age'
          yName='population'
          type='Pyramid'
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Pyramid Rendering Modes

Pyramids support two modes via `pyramidMode`:

### Linear Mode (Default)

Values determine segment heights linearly:

```tsx
<AccumulationSeriesDirective 
  dataSource={data}
  xName='x'
  yName='y'
  type='Pyramid'
  pyramidMode='Linear'  // Default
/>
```

### Surface Mode

Values determine surface areas rather than heights:

```tsx
<AccumulationSeriesDirective 
  dataSource={data}
  xName='x'
  yName='y'
  type='Pyramid'
  pyramidMode='Surface'
/>
```

**When to use Surface mode:**
- More accurate area-based representation
- Scientific or demographic data
- When proportions must be precise

**Mode comparison:**

```tsx
function PyramidModeComparison() {
  const data = [
    { x: 'Executive', y: 5 },
    { x: 'Management', y: 20 },
    { x: 'Supervisors', y: 50 },
    { x: 'Staff', y: 200 }
  ];

  return (
    <div style={{ display: 'flex', gap: '20px' }}>
      <AccumulationChartComponent 
        id='linear-pyramid'
        title='Linear Mode'
      >
        <Inject services={[PyramidSeries]} />
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective 
            dataSource={data}
            xName='x'
            yName='y'
            type='Pyramid'
            pyramidMode='Linear'
          />
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>

      <AccumulationChartComponent 
        id='surface-pyramid'
        title='Surface Mode'
      >
        <Inject services={[PyramidSeries]} />
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective 
            dataSource={data}
            xName='x'
            yName='y'
            type='Pyramid'
            pyramidMode='Surface'
          />
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>
    </div>
  );
}
```

## Pyramid Size Customization

Like funnels, customize pyramid size using `width` and `height`:

```tsx
<AccumulationSeriesDirective 
  dataSource={data}
  xName='x'
  yName='y'
  type='Pyramid'
  width='60%'
  height='80%'
/>
```

Add gaps between pyramid segments:

```tsx
<AccumulationSeriesDirective 
  dataSource={data}
  xName='x'
  yName='y'
  type='Pyramid'
  gapRatio={0.2}  // 20% gap between segments
/>
```

## Explode Effects

Add explode effects to emphasize specific segments in both funnels and pyramids:

```tsx
<AccumulationSeriesDirective 
  dataSource={data}
  xName='x'
  yName='y'
  type='Funnel'  // or 'Pyramid'
  explode={true}          // Enable click-to-explode
  explodeOffset='10%'     // Distance when exploded
  explodeIndex={3}        // Explode 4th segment by default
  explodeAll={false}      // Don't explode all segments
/>
```

**Explode properties:**
- `explode`: Enable/disable explode on click
- `explodeOffset`: Distance ('10px' or '10%')
- `explodeIndex`: Index of segment to explode on load
- `explodeAll`: Explode all segments at once

**Complete explode example:**

```tsx
function ExplodedFunnel() {
  const data = [
    { stage: 'Awareness', count: 10000 },
    { stage: 'Downloaded', count: 5000 },
    { stage: 'Active', count: 3000 },
    { stage: 'Subscribed', count: 1500 }
  ];

  return (
    <AccumulationChartComponent 
      id='exploded-funnel'
      title='App Conversion Funnel'
      legendSettings={{ visible: true }}
    >
      <Inject services={[FunnelSeries, AccumulationLegend]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective 
          dataSource={data}
          xName='stage'
          yName='count'
          type='Funnel'
          explode={true}
          explodeOffset='15%'
          explodeIndex={1}  // Highlight "Downloaded" stage
          gapRatio={0.08}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Smart Data Labels for Funnels

Funnel and pyramid charts automatically arrange data labels to prevent overlapping. Overlapping labels are positioned to the left side:

```tsx
function SmartLabelFunnel() {
  const data = [
    { x: 'Raw Materials', y: 9000 },
    { x: 'Initial Processing', y: 8500 },
    { x: 'Secondary Processing', y: 8200 },
    { x: 'Quality Control', y: 8000 },
    { x: 'Packaging Stage', y: 7800 },
    { x: 'Final Inspection', y: 7600 },
    { x: 'Distribution Ready', y: 7500 }
  ];

  return (
    <AccumulationChartComponent 
      id='smart-label-funnel'
      title='Manufacturing Process'
      legendSettings={{ visible: false }}
    >
      <Inject services={[FunnelSeries, AccumulationDataLabel]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective 
          dataSource={data}
          xName='x'
          yName='y'
          type='Funnel'
          dataLabel={{
            visible: true,
            position: 'Outside',
            connectorStyle: { length: '6%' },
            name: 'x'
          }}
          neckWidth='25%'
          neckHeight='10%'
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

**Smart label behavior:**
- Labels automatically positioned to avoid overlap
- Overlapping labels moved to left side
- Connector lines adjust automatically
- No configuration needed - works out of the box

## Point Customization for Funnels/Pyramids

Customize individual segments using the `pointRender` event:

```tsx
import { IAccPointRenderEventArgs } from '@syncfusion/ej2-react-charts';

function CustomFunnel() {
  const data = [
    { x: 'Awareness', y: 100 },
    { x: 'Interest', y: 75 },
    { x: 'Consideration', y: 50 },
    { x: 'Purchase', y: 25 }
  ];

  const onPointRender = (args: IAccPointRenderEventArgs): void => {
    // Highlight the "Purchase" stage
    if (args.point.x === 'Purchase') {
      args.fill = '#4BC0C0';  // Teal color
    } else {
      args.fill = '#FF6384';  // Pink color
    }
  };

  return (
    <AccumulationChartComponent 
      id='custom-funnel'
      pointRender={onPointRender}
    >
      <Inject services={[FunnelSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective 
          dataSource={data}
          xName='x'
          yName='y'
          type='Funnel'
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Common Use Cases

**Funnel Charts:**
- Sales conversion tracking
- User onboarding flows
- Marketing campaign effectiveness
- Application process stages
- Website analytics funnels

**Pyramid Charts:**
- Organizational hierarchies
- Age demographics
- Priority systems
- Food chains
- Social class structures

## Troubleshooting

**Issue: Funnel neck too wide/narrow**
- Solution: Adjust `neckWidth` (15%-50% typically works well)

**Issue: Segments too close together**
- Solution: Increase `gapRatio` to 0.08-0.15

**Issue: Funnel too small in container**
- Solution: Increase `width` and `height` to 70%-90%

**Issue: Labels overlapping despite smart labels**
- Solution: Use `position: 'Outside'` for data labels and adjust connector length

**Issue: Wrong pyramid proportions**
- Solution: Try `pyramidMode='Surface'` for area-based representation
