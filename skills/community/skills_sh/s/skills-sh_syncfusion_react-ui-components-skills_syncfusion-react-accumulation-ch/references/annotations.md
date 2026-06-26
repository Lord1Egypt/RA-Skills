# Annotations

## Overview

Annotations add custom HTML content, text, or images at specific positions on the chart, providing additional context, labels, or visual elements beyond standard chart features.

## Basic Annotation

Add annotations using the `annotations` property with `AccumulationAnnotationsDirective`:

```tsx
import { 
  AccumulationChartComponent,
  AccumulationSeriesCollectionDirective,
  AccumulationSeriesDirective,
  AccumulationAnnotationsDirective,
  AccumulationAnnotationDirective,
  Inject,
  PieSeries,
  AccumulationAnnotation
} from '@syncfusion/ej2-react-charts';

function BasicAnnotation() {
  const data = [
    { x: 'Jan', y: 35 },
    { x: 'Feb', y: 28 },
    { x: 'Mar', y: 34 }
  ];

  return (
    <AccumulationChartComponent id='annotation-chart'>
      <Inject services={[PieSeries, AccumulationAnnotation]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
        />
      </AccumulationSeriesCollectionDirective>
      <AccumulationAnnotationsDirective>
        <AccumulationAnnotationDirective
          content='<div style="font-size:18px;font-weight:bold;">Q1 Sales</div>'
          region='Series'  // 'Chart' or 'Series'
          x='50%'
          y='50%'
        />
      </AccumulationAnnotationsDirective>
    </AccumulationChartComponent>
  );
}
```

**Key properties:**
- `content`: HTML string or template
- `region`: 'Chart' (relative to chart area) or 'Series' (relative to series)
- `x`, `y`: Position (pixels, percentages, or coordinates)
- `coordinateUnits`: 'Pixel' or 'Point' positioning

## Positioning Annotations

Position annotations using different coordinate systems:

**Pixel-based positioning:**

```tsx
<AccumulationAnnotationDirective
  content='<div>Top Left</div>'
  region='Chart'
  coordinateUnits='Pixel'
  x='20'
  y='20'
/>
```

**Percentage-based positioning:**

```tsx
<AccumulationAnnotationDirective
  content='<div>Center</div>'
  region='Series'
  x='50%'
  y='50%'
/>
```

**Complete positioning example:**

```tsx
function PositionedAnnotations() {
  const data = [
    { x: 'Chrome', y: 61.3 },
    { x: 'Safari', y: 24.6 },
    { x: 'Firefox', y: 14.1 }
  ];

  return (
    <AccumulationChartComponent 
      id='positioned-annotations'
      title='Browser Market Share'
    >
      <Inject services={[PieSeries, AccumulationAnnotation]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          innerRadius='40%'
        />
      </AccumulationSeriesCollectionDirective>
      <AccumulationAnnotationsDirective>
        {/* Center annotation */}
        <AccumulationAnnotationDirective
          content='<div style="font-size:24px;font-weight:bold;color:#333;">100M</div>'
          region='Series'
          x='50%'
          y='50%'
        />
        {/* Bottom note */}
        <AccumulationAnnotationDirective
          content='<div style="font-size:12px;color:#666;">*Data as of 2024</div>'
          region='Chart'
          coordinateUnits='Pixel'
          x='10'
          y='380'
        />
      </AccumulationAnnotationsDirective>
    </AccumulationChartComponent>
  );
}
```

## Annotation Templates

Create complex annotations using React components:

```tsx
function TemplateAnnotations() {
  const data = [
    { x: 'Product A', y: 45, status: 'success' },
    { x: 'Product B', y: 30, status: 'warning' },
    { x: 'Product C', y: 25, status: 'info' }
  ];

  const centerTemplate = () => {
    return (
      <div style={{
        textAlign: 'center',
        padding: '10px',
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        borderRadius: '8px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
      }}>
        <div style={{ fontSize: '28px', fontWeight: 'bold', color: '#0078d4' }}>
          100
        </div>
        <div style={{ fontSize: '12px', color: '#666', marginTop: '4px' }}>
          Total Items
        </div>
      </div>
    );
  };

  return (
    <AccumulationChartComponent id='template-annotations'>
      <Inject services={[PieSeries, AccumulationAnnotation]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          innerRadius='50%'
        />
      </AccumulationSeriesCollectionDirective>
      <AccumulationAnnotationsDirective>
        <AccumulationAnnotationDirective
          content={centerTemplate}
          region='Series'
          x='50%'
          y='50%'
        />
      </AccumulationAnnotationsDirective>
    </AccumulationChartComponent>
  );
}
```

## Multiple Annotations

Add multiple annotations for complex layouts:

```tsx
function MultipleAnnotations() {
  const data = [
    { x: 'Q1', y: 35 },
    { x: 'Q2', y: 28 },
    { x: 'Q3', y: 42 },
    { x: 'Q4', y: 31 }
  ];

  return (
    <AccumulationChartComponent 
      id='multiple-annotations'
      title='Quarterly Performance'
    >
      <Inject services={[PieSeries, AccumulationAnnotation]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          innerRadius='40%'
        />
      </AccumulationSeriesCollectionDirective>
      <AccumulationAnnotationsDirective>
        {/* Center total */}
        <AccumulationAnnotationDirective
          content='<div style="text-align:center;"><div style="font-size:32px;font-weight:bold;color:#333;">136</div><div style="font-size:14px;color:#666;">Total Sales</div></div>'
          region='Series'
          x='50%'
          y='45%'
        />
        {/* Growth indicator */}
        <AccumulationAnnotationDirective
          content='<div style="color:#28a745;font-size:16px;font-weight:bold;">↑ 12%</div>'
          region='Series'
          x='50%'
          y='60%'
        />
        {/* Footer note */}
        <AccumulationAnnotationDirective
          content='<div style="font-size:11px;color:#999;font-style:italic;">Year over Year Growth</div>'
          region='Chart'
          coordinateUnits='Pixel'
          x='150'
          y='390'
        />
      </AccumulationAnnotationsDirective>
    </AccumulationChartComponent>
  );
}
```

## Dynamic Annotations

Update annotations dynamically based on data or state:

```tsx
function DynamicAnnotations() {
  const [selectedQuarter, setSelectedQuarter] = React.useState('Q3');
  
  const data = [
    { x: 'Q1', y: 35 },
    { x: 'Q2', y: 28 },
    { x: 'Q3', y: 42 },
    { x: 'Q4', y: 31 }
  ];

  const total = data.reduce((sum, item) => sum + item.y, 0);
  const selected = data.find(d => d.x === selectedQuarter);

  const onPointClick = (args: any) => {
    setSelectedQuarter(args.point.x);
  };

  return (
    <AccumulationChartComponent 
      id='dynamic-annotations'
      pointClick={onPointClick}
    >
      <Inject services={[PieSeries, AccumulationAnnotation]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          innerRadius='50%'
        />
      </AccumulationSeriesCollectionDirective>
      <AccumulationAnnotationsDirective>
        <AccumulationAnnotationDirective
          content={`<div style="text-align:center;">
            <div style="font-size:24px;font-weight:bold;color:#0078d4;">${total}</div>
            <div style="font-size:12px;color:#666;margin-top:4px;">Total</div>
            <div style="font-size:16px;font-weight:600;color:#333;margin-top:8px;">${selectedQuarter}</div>
            <div style="font-size:14px;color:#28a745;">${selected?.y}</div>
          </div>`}
          region='Series'
          x='50%'
          y='50%'
        />
      </AccumulationAnnotationsDirective>
    </AccumulationChartComponent>
  );
}
```

## Image Annotations

Add image annotations for logos or icons:

```tsx
function ImageAnnotation() {
  const data = [
    { x: 'Mobile', y: 55 },
    { x: 'Desktop', y: 30 },
    { x: 'Tablet', y: 15 }
  ];

  return (
    <AccumulationChartComponent id='image-annotation'>
      <Inject services={[PieSeries, AccumulationAnnotation]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          innerRadius='40%'
        />
      </AccumulationSeriesCollectionDirective>
      <AccumulationAnnotationsDirective>
        {/* Image in center */}
        <AccumulationAnnotationDirective
          content='<img src="logo.png" style="width:60px;height:60px;" />'
          region='Series'
          x='50%'
          y='50%'
        />
        {/* Watermark */}
        <AccumulationAnnotationDirective
          content='<img src="watermark.png" style="opacity:0.1;width:200px;" />'
          region='Chart'
          coordinateUnits='Pixel'
          x='100'
          y='150'
        />
      </AccumulationAnnotationsDirective>
    </AccumulationChartComponent>
  );
}
```

## Styled Annotations

Apply advanced styling to annotations:

```tsx
function StyledAnnotations() {
  const data = [
    { x: 'Approved', y: 65 },
    { x: 'Pending', y: 25 },
    { x: 'Rejected', y: 10 }
  ];

  const styledContent = `
    <div style="
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 15px 20px;
      border-radius: 12px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      text-align: center;
      color: white;
    ">
      <div style="font-size: 28px; font-weight: bold;">65%</div>
      <div style="font-size: 12px; margin-top: 4px; opacity: 0.9;">Approval Rate</div>
    </div>
  `;

  return (
    <AccumulationChartComponent id='styled-annotations'>
      <Inject services={[PieSeries, AccumulationAnnotation]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          innerRadius='50%'
        />
      </AccumulationSeriesCollectionDirective>
      <AccumulationAnnotationsDirective>
        <AccumulationAnnotationDirective
          content={styledContent}
          region='Series'
          x='50%'
          y='50%'
        />
      </AccumulationAnnotationsDirective>
    </AccumulationChartComponent>
  );
}
```

## Common Issues and Solutions

**Issue: Annotation not visible**
- Solution: Ensure `AccumulationAnnotation` module is injected
- Solution: Check x, y coordinates are within chart bounds
- Solution: Verify content HTML is valid
- Solution: Check z-index if overlapping with other elements

**Issue: Annotation positioned incorrectly**
- Solution: Use percentage values ('50%') for center positioning
- Solution: Check `region` property ('Chart' vs 'Series')
- Solution: Verify `coordinateUnits` matches coordinate type
- Solution: Test with pixel coordinates for absolute positioning

**Issue: Template not rendering**
- Solution: Ensure content is function returning JSX or HTML string
- Solution: Check for React errors in browser console
- Solution: Verify template syntax is correct

**Issue: Annotation overlaps chart elements**
- Solution: Adjust x, y coordinates
- Solution: Use CSS positioning within content
- Solution: Consider using data labels instead for point-specific info
- Solution: Reduce annotation size or reposition

**Issue: Dynamic updates not reflecting**
- Solution: Ensure annotation dependencies trigger re-render
- Solution: Use state/props to update content dynamically
- Solution: Check that content string changes on update
