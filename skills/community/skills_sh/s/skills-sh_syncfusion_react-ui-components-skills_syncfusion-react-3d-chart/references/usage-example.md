# Chart3D Usage Example

## Table of contents
- [Minimal Example](usage-example.md#minimal-example)
  - [Imports](usage-example.md#imports)
  - [Data](usage-example.md#data)
  - [Component](usage-example.md#component)
- [See also](usage-example.md#see-also)

Minimal runnable example demonstrating common props, methods, and events for `Chart3DComponent`.

## Imports

```tsx
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import React, { useRef } from 'react';
import {
  Chart3DComponent,
  Chart3DSeriesCollectionDirective,
  Chart3DSeriesDirective,
  Inject,
  ColumnSeries3D,
  Category3D,
  Legend3D,
  Tooltip3D
} from '@syncfusion/ej2-react-charts';
```

## Data

```tsx
const data = [
  { x: 'Jan', y: 40 },
  { x: 'Feb', y: 55 },
  { x: 'Mar', y: 48 }
];
```

## Component

```tsx
export default function Chart3DUsage() {
  const chartRef = useRef(null);

  const handleLoaded = () => console.log('3D chart loaded');

  return (
    <div>
      <Chart3DComponent
        id="chart3d"
        primaryXAxis={{ valueType: 'Category' }}
        dataSource={data}
        enableRotation={true}
        depth={90}
        rotation={15}
        tilt={8}
        tooltip={{ enable: true }}
        loaded={handleLoaded}
      >
        <Inject services={[ColumnSeries3D, Category3D, Legend3D, Tooltip3D]} />
        <Chart3DSeriesCollectionDirective>
          <Chart3DSeriesDirective dataSource={data} xName="x" yName="y" type="Column" name="Sales" />
        </Chart3DSeriesCollectionDirective>
      </Chart3DComponent>
    </div>
  );
}
```

## See also

See also: [api-reference.md](api-reference.md)

ReactDOM.render(<Chart3DUsage />, document.getElementById('charts'));
```

See also: [api-reference.md](api-reference.md)
