# Data Labels

## Table of Contents
- [Overview](#overview)
- [Enabling Data Labels](#enabling-data-labels)
- [Positioning Labels](#positioning-labels)
- [Data Label Rotation](#data-label-rotation)
- [Smart Labels](#smart-labels)
- [Formatting Labels](#formatting-labels)
- [Data Label Templates](#data-label-templates)
- [Connector Lines](#connector-lines)
- [Text Mapping](#text-mapping)
- [Customizing with textRender](#customizing-with-textrender)
- [Text Wrapping](#text-wrapping)
- [Showing Percentages](#showing-percentages)

## Overview

Data labels display values or information for each chart point, improving readability and providing immediate insights without requiring tooltips.

## Enabling Data Labels

Enable data labels by setting `visible: true` and injecting the `AccumulationDataLabel` module:

```tsx
import { 
  AccumulationChartComponent,
  AccumulationSeriesCollectionDirective,
  AccumulationSeriesDirective,
  Inject,
  PieSeries,
  AccumulationDataLabel
} from '@syncfusion/ej2-react-charts';

function App() {
  const data = [
    { x: 'Jan', y: 35 },
    { x: 'Feb', y: 28 },
    { x: 'Mar', y: 34 }
  ];

  return (
    <AccumulationChartComponent 
      id='chart'
      enableSmartLabels={true}
    >
      <Inject services={[PieSeries, AccumulationDataLabel]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          dataLabel={{ visible: true }}  // Enable data labels
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Positioning Labels

Position labels `Inside` or `Outside` the chart using the `position` property:

**Outside Position:**
```tsx
dataLabel={{
  visible: true,
  position: 'Outside'  // Labels outside slices with connector lines
}}
```

**Inside Position:**
```tsx
dataLabel={{
  visible: true,
  position: 'Inside'  // Labels within slices
}}
```

**When to use each:**
- **Outside**: Better for small slices, prevents overlap, clearer reading
- **Inside**: Compact layout, works well with large slices, modern look

**Complete example:**

```tsx
function LabelPositioning() {
  const data = [
    { category: 'Mobile', value: 45 },
    { category: 'Desktop', value: 35 },
    { category: 'Tablet', value: 20 }
  ];

  return (
    <div style={{ display: 'flex', gap: '20px' }}>
      <AccumulationChartComponent 
        id='inside-labels'
        title='Inside Labels'
      >
        <Inject services={[PieSeries, AccumulationDataLabel]} />
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective
            dataSource={data}
            xName='category'
            yName='value'
            dataLabel={{
              visible: true,
              position: 'Inside',
              font: { color: 'white', fontWeight: '600' }
            }}
          />
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>

      <AccumulationChartComponent 
        id='outside-labels'
        title='Outside Labels'
      >
        <Inject services={[PieSeries, AccumulationDataLabel]} />
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective
            dataSource={data}
            xName='category'
            yName='value'
            dataLabel={{
              visible: true,
              position: 'Outside'
            }}
          />
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>
    </div>
  );
}
```

## Data Label Rotation

Rotate data labels using the `angle` property combined with `enableRotation`:

```tsx
dataLabel={{
  visible: true,
  angle: 90,  // Rotate 90 degrees
  enableRotation: true
}}
```

**Rotation behavior:**
- When `enableRotation: true`, labels rotate along the slice angle by default
- Set specific `angle` value to override automatic rotation
- Useful for long labels or custom orientations

**Example:**

```tsx
function RotatedLabels() {
  const data = [
    { x: 'Product A', y: 25 },
    { x: 'Product B', y: 30 },
    { x: 'Product C', y: 45 }
  ];

  return (
    <AccumulationChartComponent 
      id='rotated-labels'
      enableSmartLabels={true}
    >
      <Inject services={[PieSeries, AccumulationDataLabel]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          dataLabel={{
            visible: true,
            angle: 90,
            enableRotation: true,
            position: 'Inside'
          }}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Smart Labels

Smart labels automatically prevent overlapping by repositioning labels intelligently:

```tsx
<AccumulationChartComponent 
  id='chart'
  enableSmartLabels={true}  // Enable on chart component
>
  <Inject services={[PieSeries, AccumulationDataLabel]} />
  <AccumulationSeriesCollectionDirective>
    <AccumulationSeriesDirective
      dataSource={data}
      xName='x'
      yName='y'
      dataLabel={{
        visible: true,
        position: 'Outside',
        name: 'text'
      }}
    />
  </AccumulationSeriesCollectionDirective>
</AccumulationChartComponent>
```

**Smart label features:**
- Automatically detects overlapping labels
- Repositions labels to available space
- Adjusts connector lines accordingly
- Works best with `position: 'Outside'`

**When to enable:**
- Charts with many small slices (8+)
- Similar-sized data values causing label clustering
- Variable data that might cause overlap

## Formatting Labels

Format data label text using the `format` property with standard number formats:

```tsx
dataLabel={{
  visible: true,
  format: 'n2'  // Number format with 2 decimal places
}}
```

**Format options:**

| Format | Example Input | Output | Description |
|--------|---------------|--------|-------------|
| `n0` | 1000 | 1000 | Integer, no decimals |
| `n1` | 1000 | 1000.0 | 1 decimal place |
| `n2` | 1000 | 1000.00 | 2 decimal places |
| `p0` | 0.45 | 45% | Percentage, no decimals |
| `p1` | 0.45 | 45.0% | Percentage, 1 decimal |
| `p2` | 0.45 | 45.00% | Percentage, 2 decimals |
| `c0` | 1000 | $1000 | Currency, no decimals |
| `c2` | 1000 | $1000.00 | Currency, 2 decimals |

**Example with formatting:**

```tsx
function FormattedLabels() {
  const salesData = [
    { product: 'Laptop', revenue: 45000.5 },
    { product: 'Phone', revenue: 38500.25 },
    { product: 'Tablet', revenue: 25000.75 }
  ];

  return (
    <AccumulationChartComponent 
      id='formatted-labels'
      title='Revenue Distribution'
    >
      <Inject services={[PieSeries, AccumulationDataLabel]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={salesData}
          xName='product'
          yName='revenue'
          dataLabel={{
            visible: true,
            position: 'Outside',
            format: 'c0'  // Currency format: $45000, $38500, $25000
          }}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Data Label Templates

Create custom label layouts using HTML templates with the `template` property:

```tsx
function TemplatedLabels() {
  const data = [
    { x: 'Chrome', y: 61.3 },
    { x: 'Safari', y: 24.6 },
    { x: 'Firefox', y: 14.1 }
  ];

  const labelTemplate = (args: any) => {
    return (
      <div style={{
        border: '1px solid #ddd',
        backgroundColor: '#f9f9f9',
        padding: '5px',
        borderRadius: '4px'
      }}>
        <div style={{ fontWeight: 'bold', color: '#333' }}>
          {args.point.x}
        </div>
        <div style={{ fontSize: '12px', color: '#666' }}>
          {args.point.y}%
        </div>
      </div>
    );
  };

  return (
    <AccumulationChartComponent id='template-labels'>
      <Inject services={[PieSeries, AccumulationDataLabel]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          dataLabel={{
            visible: true,
            position: 'Outside',
            template: labelTemplate
          }}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

**Template variables available:**
- `${point.x}`: Category/label value
- `${point.y}`: Numeric value
- `${point.percentage}`: Calculated percentage
- `${point.text}`: Custom text from data
- `${series.name}`: Series name

## Connector Lines

Connector lines link outside labels to their corresponding slices. Customize with `connectorStyle`:

```tsx
dataLabel={{
  visible: true,
  position: 'Outside',
  connectorStyle: {
    length: '50px',     // Line length
    width: 2,           // Line thickness
    dashArray: '5,3',   // Dash pattern
    color: '#f4429e',   // Line color
    type: 'Curve'       // 'Line' or 'Curve'
  }
}}
```

**Connector properties:**
- `length`: Distance from slice ('20px', '50px', '10%')
- `width`: Line thickness in pixels
- `color`: Line color (hex, rgb, color name)
- `dashArray`: Dash pattern ('5,3' = 5px dash, 3px gap)
- `type`: 'Line' (straight) or 'Curve' (curved)

**Complete example:**

```tsx
function StyledConnectors() {
  const data = [
    { x: 'Category A', y: 35, text: 'A: 35%' },
    { x: 'Category B', y: 28, text: 'B: 28%' },
    { x: 'Category C', y: 37, text: 'C: 37%' }
  ];

  return (
    <AccumulationChartComponent 
      id='styled-connectors'
      enableSmartLabels={true}
    >
      <Inject services={[PieSeries, AccumulationDataLabel]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          dataLabel={{
            visible: true,
            position: 'Outside',
            name: 'text',
            connectorStyle: {
              length: '40px',
              width: 2,
              color: '#0078d4',
              type: 'Curve',
              dashArray: '0'
            }
          }}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Text Mapping

Map label text from a data field using the `name` property:

```tsx
function TextMapping() {
  const data = [
    { 
      x: 'Jan', 
      y: 35, 
      text: 'January: 35 units',
      fill: '#FF6384'
    },
    { 
      x: 'Feb', 
      y: 28, 
      text: 'February: 28 units',
      fill: '#36A2EB'
    },
    { 
      x: 'Mar', 
      y: 34, 
      text: 'March: 34 units',
      fill: '#FFCE56'
    }
  ];

  return (
    <AccumulationChartComponent id='text-mapped'>
      <Inject services={[PieSeries, AccumulationDataLabel]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          pointColorMapping='fill'  // Map colors
          dataLabel={{
            visible: true,
            name: 'text',  // Use 'text' field for labels
            position: 'Outside'
          }}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Customizing with textRender

Use the `textRender` event to dynamically customize individual labels:

```tsx
import { IAccTextRenderEventArgs } from '@syncfusion/ej2-react-charts';

function DynamicLabels() {
  const data = [
    { x: 'Q1', y: 7 },
    { x: 'Q2', y: 15 },
    { x: 'Q3', y: 21 },
    { x: 'Q4', y: 18 }
  ];

  const onTextRender = (args: IAccTextRenderEventArgs): void => {
    // Highlight Q3 label
    if (args.text === '21') {
      args.color = 'red';
      args.border.width = 2;
      args.border.color = 'darkred';
      args.text = 'Peak: ' + args.text;
    }
  };

  return (
    <AccumulationChartComponent 
      id='dynamic-labels'
      enableSmartLabels={true}
      textRender={onTextRender}
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
  );
}
```

## Text Wrapping

Wrap long label text using the `textWrap` property with `maxWidth`:

```tsx
dataLabel={{
  visible: true,
  position: 'Inside',
  maxWidth: 100,        // Max width in pixels
  textWrap: 'Wrap',     // 'Normal', 'Wrap', or 'AnyWhere'
  enableRotation: true
}}
```

**textWrap modes:**
- `'Normal'`: No wrapping (default)
- `'Wrap'`: Wrap at word boundaries
- `'AnyWhere'`: Wrap anywhere if needed

**Example:**

```tsx
function WrappedLabels() {
  const data = [
    { 
      x: 'Chrome', 
      y: 100, 
      text: 'Chrome (100M) 40%'
    },
    { 
      x: 'UC Browser', 
      y: 40, 
      text: 'UC Browser (40M) 16%'
    },
    { 
      x: 'Firefox', 
      y: 25, 
      text: 'Firefox (25M) 10%'
    }
  ];

  return (
    <AccumulationChartComponent 
      id='wrapped-labels'
      enableSmartLabels={true}
    >
      <Inject services={[PieSeries, AccumulationDataLabel]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          innerRadius='40%'
          dataLabel={{
            visible: true,
            position: 'Inside',
            maxWidth: 100,
            textWrap: 'Wrap',
            name: 'text',
            enableRotation: true,
            font: { size: '11px' }
          }}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Showing Percentages

Display percentages in labels using either `textRender` event or templates:

**Method 1: Using textRender Event**

```tsx
function PercentageLabelsEvent() {
  const data = [
    { x: 'Product A', y: 45 },
    { x: 'Product B', y: 30 },
    { x: 'Product C', y: 25 }
  ];

  const onTextRender = (args: IAccTextRenderEventArgs): void => {
    args.text = args.point.percentage.toFixed(1) + '%';
  };

  return (
    <AccumulationChartComponent 
      id='percentage-event'
      textRender={onTextRender}
    >
      <Inject services={[PieSeries, AccumulationDataLabel]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          dataLabel={{ visible: true, position: 'Outside' }}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

**Method 2: Using Template**

```tsx
function PercentageLabelsTemplate() {
  const data = [
    { x: 'Product A', y: 45 },
    { x: 'Product B', y: 30 },
    { x: 'Product C', y: 25 }
  ];

  const percentageTemplate = (args: any) => {
    return (
      <div style={{ fontWeight: 'bold', fontSize: '14px' }}>
        {args.point.percentage.toFixed(1)}%
      </div>
    );
  };

  return (
    <AccumulationChartComponent id='percentage-template'>
      <Inject services={[PieSeries, AccumulationDataLabel]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          dataLabel={{
            visible: true,
            position: 'Outside',
            template: percentageTemplate
          }}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Common Issues and Solutions

**Issue: Labels overlapping**
- Solution: Enable `enableSmartLabels={true}` on chart component
- Solution: Use `position: 'Outside'` for more space
- Solution: Reduce font size in label settings

**Issue: Connector lines too short/long**
- Solution: Adjust `connectorStyle.length` ('30px', '50px', etc.)

**Issue: Labels not showing**
- Solution: Ensure `AccumulationDataLabel` module is injected
- Solution: Verify `visible: true` in dataLabel settings
- Solution: Check if data values are valid numbers

**Issue: Template not rendering**
- Solution: Ensure template function returns valid JSX
- Solution: Check that point properties are accessed correctly

**Issue: Percentage calculation incorrect**
- Solution: Use `args.point.percentage` from textRender - automatically calculated
- Solution: Ensure y values are positive numbers
