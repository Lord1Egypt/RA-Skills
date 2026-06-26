# Annotations and Polygons in React Maps

## Overview

Annotations add custom HTML content at specific positions on maps. Polygons render custom shapes beyond GeoJSON data.

## Annotations

### Basic Annotations

```tsx
import {
  MapsComponent,
  LayersDirective,
  LayerDirective,
  AnnotationsDirective,
  AnnotationDirective,
  Inject,
  Annotations
} from '@syncfusion/ej2-react-maps';

function AnnotatedMap() {
  const annotationTemplate = () => {
    return (
      <div style={{
        background: '#FF6347',
        color: 'white',
        padding: '10px 20px',
        borderRadius: '5px',
        fontSize: '14px',
        fontWeight: 'bold'
      }}>
        Pacific Ocean
      </div>
    );
  };

  return (
    <MapsComponent>
      <Inject services={[Annotations]} />
      <AnnotationsDirective>
        <AnnotationDirective
          content={annotationTemplate}
          x='50%'
          y='50%'
        />
      </AnnotationsDirective>
      <LayersDirective>
        <LayerDirective shapeData={world_map} />
      </LayersDirective>
    </MapsComponent>
  );
}
```

### Position Annotations

```tsx
// Percentage positioning
<AnnotationDirective
  content={template}
  x='25%'   // 25% from left
  y='75%'   // 75% from top
/>

// Pixel positioning
<AnnotationDirective
  content={template}
  x='100'   // 100px from left
  y='200'   // 200px from top
/>
```

### Multiple Annotations

```tsx
function MultiAnnotationMap() {
  const oceanLabel = () => (
    <div style={{background: '#4682B4', color: 'white', padding: '5px 10px', borderRadius: '3px'}}>
      Atlantic Ocean
    </div>
  );

  const titleAnnotation = () => (
    <h2 style={{color: '#333', textAlign: 'center'}}>
      World Oceans Map
    </h2>
  );

  return (
    <MapsComponent>
      <Inject services={[Annotations]} />
      <AnnotationsDirective>
        <AnnotationDirective content={titleAnnotation} x='50%' y='5%' />
        <AnnotationDirective content={oceanLabel} x='30%' y='40%' />
      </AnnotationsDirective>
      <LayersDirective>
        <LayerDirective shapeData={world_map} />
      </LayersDirective>
    </MapsComponent>
  );
}
```

## Polygons

### Basic Polygon

```tsx
import {
  MapsComponent,
  LayersDirective,
  LayerDirective,
  Inject,
  Polygon
} from '@syncfusion/ej2-react-maps';

function PolygonMap() {
  const polygonData = [
    {
      points: [
        { latitude: 37.0902, longitude: -95.7129 },
        { latitude: 38.7, longitude: -96.0 },
        { latitude: 37.0, longitude: -96.0 }
      ],
      fill: 'rgba(255, 0, 0, 0.4)',
      borderColor: '#FF0000',
      borderWidth: 2
    }
  ];

  return (
    <MapsComponent>
      <Inject services={[Polygon]} />
      <LayersDirective>
        <LayerDirective
          shapeData={usa_map}
          polygonSettings={{
            polygons: polygonData
          }}
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

### Custom Shape Overlay

```tsx
const customRegions = [
  {
    points: [
      { latitude: 40, longitude: -100 },
      { latitude: 42, longitude: -98 },
      { latitude: 41, longitude: -96 },
      { latitude: 39, longitude: -97 }
    ],
    fill: 'rgba(76, 175, 80, 0.3)',
    borderColor: '#4CAF50',
    borderWidth: 3,
    opacity: 0.7
  },
  {
    points: [
      { latitude: 35, longitude: -105 },
      { latitude: 37, longitude: -103 },
      { latitude: 36, longitude: -101 },
      { latitude: 34, longitude: -102 }
    ],
    fill: 'rgba(255, 152, 0, 0.3)',
    borderColor: '#FF9800',
    borderWidth: 3
  }
];

<LayerDirective
  shapeData={usa_map}
  polygonSettings={{ polygons: customRegions }}
/>
```

## Use Cases

### Highlighting Search Areas

```tsx
function SearchAreaMap() {
  const searchArea = [
    {
      points: [
        { latitude: 51.6, longitude: -0.3 },
        { latitude: 51.6, longitude: 0.1 },
        { latitude: 51.4, longitude: 0.1 },
        { latitude: 51.4, longitude: -0.3 }
      ],
      fill: 'rgba(33, 150, 243, 0.2)',
      borderColor: '#2196F3',
      borderWidth: 2
    }
  ];

  return (
    <MapsComponent>
      <Inject services={[Polygon]} />
      <LayersDirective>
        <LayerDirective
          shapeData={london_map}
          polygonSettings={{ polygons: searchArea }}
        />
      </LayersDirective>
    </MapsComponent>
  );
}
```

### Territory Zones

```tsx
const territories = [
  {
    points: [
      /* North territory coordinates */
    ],
    fill: 'rgba(255, 99, 71, 0.3)',
    borderColor: '#FF6347',
    borderWidth: 2
  },
  {
    points: [
      /* South territory coordinates */
    ],
    fill: 'rgba(135, 206, 235, 0.3)',
    borderColor: '#87CEEB',
    borderWidth: 2
  }
];

<LayerDirective
  shapeData={region_map}
  polygonSettings={{ polygons: territories }}
/>
```

## Troubleshooting

### Issue: Annotations not appearing

**Solution:** Inject `Annotations` service
```tsx
<MapsComponent>
  <Inject services={[Annotations]} />
</MapsComponent>
```

### Issue: Polygon not visible

**Solutions:**
1. Inject `Polygon` service
2. Verify coordinate points are within map bounds
3. Check fill opacity isn't 0
