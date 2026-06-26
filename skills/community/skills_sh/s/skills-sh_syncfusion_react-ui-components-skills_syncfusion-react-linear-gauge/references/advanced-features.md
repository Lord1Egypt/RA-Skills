# Advanced Features in React Linear Gauge

See API Reference: [API Reference](api-reference.md)

## Table of Contents

- [Animations](#animations)
  - [Animate Pointer Value](#animate-pointer-value)
  - [Animate Gauge Load](#animate-gauge-load)
- [Event Handling](#event-handling)
  - [Value Change Event](#value-change-event)
  - [Drag Events](#drag-events)
  - [Gauge Mouse Events](#gauge-mouse-events)
  - [Load / Resize / Animation Complete](#load--resize--animation-complete)
  - [Rendering Hooks](#rendering-hooks)
  - [Print Event](#print-event)
- [Tooltips](#tooltips)
  - [Basic Tooltip](#basic-tooltip)
  - [Tooltip Customization](#tooltip-customization-style--formatting)
  - [Custom Tooltip Template](#custom-tooltip-template)
- [Print and Export](#print-and-export)
  - [Print](#print)
  - [Export](#export)
- [Real-Time Data Binding](#real-time-data-binding)
  - [Polling Example](#polling-example)
- [Performance Optimization](#performance-optimization)
  - [Memoize Display Components](#memoize-display-components)
  - [useCallback for Event Handlers](#usecallback-for-event-handlers)
  - [Debounce Rapid Updates](#debounce-rapid-updates)
- [Combining Multiple Features](#combining-multiple-features)
  - [Comprehensive Example](#comprehensive-example)


## Animations

Use `animationDuration` on pointers (and the initial load animation) to smooth value transitions.

### Animate Pointer Value

```tsx
import React, { useState } from 'react';
import {
  LinearGaugeComponent,
  AxesDirective,
  AxisDirective,
  PointersDirective,
  PointerDirective
} from '@syncfusion/ej2-react-lineargauge';

export function App() {
  const [value, setValue] = useState(40);

  return (
    <LinearGaugeComponent>
      <AxesDirective>
        <AxisDirective minimum={0} maximum={100}>
          <PointersDirective>
            <PointerDirective
              value={value}
              animationDuration={1000}
            />
          </PointersDirective>
        </AxisDirective>
      </AxesDirective>
    </LinearGaugeComponent>
  );
}
```

### Animate Gauge Load

```tsx
<LinearGaugeComponent animationDuration={1500}>
  {/* AxesDirective + pointers/ranges */}
</LinearGaugeComponent>
```

## Event Handling

React Linear Gauge supports lifecycle and interaction events from `LinearGaugeComponent`.

### Value Change Event

Triggers while changing the value of the pointer by UI interaction.

```tsx
import React, { useState } from 'react';
import {
  LinearGaugeComponent,
  AxesDirective,
  AxisDirective,
  PointersDirective,
  PointerDirective
} from '@syncfusion/ej2-react-lineargauge';

export function App() {
  const [value, setValue] = useState(50);

  const handleValueChange = (e) => {
    console.log('Pointer value changed:', e.value);
    setValue(e.value);
  };

  return (
    <LinearGaugeComponent valueChange={handleValueChange}>
      <AxesDirective>
        <AxisDirective minimum={0} maximum={100}>
          <PointersDirective>
            <PointerDirective value={value} enableDrag={true} />
          </PointersDirective>
        </AxisDirective>
      </AxesDirective>
    </LinearGaugeComponent>
  );
}
```

### Drag Events

```tsx
<LinearGaugeComponent
  dragStart={() => console.log('dragStart')}
  dragMove={() => console.log('dragMove')}
  dragEnd={() => console.log('dragEnd')}
>
  {/* AxesDirective */}
</LinearGaugeComponent>
```

### Gauge Mouse Events

```tsx
<LinearGaugeComponent
  gaugeMouseDown={() => console.log('gaugeMouseDown')}
  gaugeMouseMove={() => console.log('gaugeMouseMove')}
  gaugeMouseUp={() => console.log('gaugeMouseUp')}
  gaugeMouseLeave={() => console.log('gaugeMouseLeave')}
>
  {/* AxesDirective */}
</LinearGaugeComponent>
```

### Load / Resize / Animation Complete

```tsx
<LinearGaugeComponent
  load={() => console.log('load')}
  loaded={() => console.log('loaded')}
  resized={() => console.log('resized')}
  animationComplete={() => console.log('animationComplete')}
>
  {/* AxesDirective */}
</LinearGaugeComponent>
```

### Rendering Hooks

Use these to customize or cancel rendering for annotations, axis labels, and tooltip content.

```tsx
<LinearGaugeComponent
  annotationRender={(args) => {
    // inspect args, then set/modify args.content if needed
  }}
  axisLabelRender={(args) => {
    // example: hide some labels
    if (args.value % 20 === 0) args.cancel = true;
  }}
  tooltipRender={(args) => {
    // inspect args before tooltip renders
  }}
>
  {/* AxesDirective */}
</LinearGaugeComponent>
```

### Print Event

```tsx
<LinearGaugeComponent beforePrint={() => console.log('beforePrint')}>
  {/* AxesDirective */}
</LinearGaugeComponent>
```

## Tooltips

Configure tooltip via the `tooltip` prop on `LinearGaugeComponent`.

### Basic Tooltip

```tsx
<LinearGaugeComponent
  tooltip={{
    enable: true,
    format: '{value}°C'
  }}
>
<Inject services={[GaugeTooltip]} />
</LinearGaugeComponent>
```

### Tooltip Customization (style + formatting)

```tsx
<LinearGaugeComponent
  tooltip={{
    enable: true,
    fill: '#FFFFFF',
    format: '{value}',
    border: { width: 1, color: '#CCCCCC' },
    textStyle: {
      fontFamily: 'Arial',
      size: '12px',
      color: '#333333'
    }
  }}
>
  <Inject services={[GaugeTooltip]} />
  {/* AxesDirective */}
</LinearGaugeComponent>
```

### Custom Tooltip Template

```tsx
const tooltipTemplate = (args) => {
  return `<div>
    <strong>${args.value}</strong><br/>
    <small>Custom tooltip</small>
  </div>`;
};

<LinearGaugeComponent
  tooltip={{
    enable: true,
    template: tooltipTemplate
  }}
>
  <Inject services={[GaugeTooltip]} />
  {/* AxesDirective */}
</LinearGaugeComponent>
```

## Print and Export

Use component `ref` to call `print()` and `export()`.

### Print

```tsx
import React, { useRef } from 'react';
import { LinearGaugeComponent } from '@syncfusion/ej2-react-lineargauge';

export function App() {
  const gaugeRef = useRef(null);

  return (
    <div>
      <button onClick={() => gaugeRef.current?.print()}>Print</button>
      <LinearGaugeComponent ref={gaugeRef}>
        {/* AxesDirective */}
      </LinearGaugeComponent>
    </div>
  );
}
```

### Export

```tsx
gaugeRef.current?.export('PDF', 'gauge.pdf', false, true);
gaugeRef.current?.export('PNG', 'gauge.png', false, true);
gaugeRef.current?.export('SVG', 'gauge.svg', false, true);
```

## Real-Time Data Binding

Update pointer values from live data by updating React state.

### Polling Example

```tsx
import React, { useEffect, useState } from 'react';
import {
  LinearGaugeComponent,
  AxesDirective,
  AxisDirective,
  PointersDirective,
  PointerDirective
} from '@syncfusion/ej2-react-lineargauge';

export function App() {
  const [value, setValue] = useState(50);

  useEffect(() => {
    const interval = setInterval(async () => {
      // Replace with your API call
      const response = await fetch('/api/sensor-data');
      const data = await response.json();
      setValue(data.value);
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <LinearGaugeComponent>
      <AxesDirective>
        <AxisDirective minimum={0} maximum={100}>
          <PointersDirective>
            <PointerDirective value={value} />
          </PointersDirective>
        </AxisDirective>
      </AxesDirective>
    </LinearGaugeComponent>
  );
}
```

## Performance Optimization

### Memoize Display Components

```tsx
import React, { memo } from 'react';

const GaugeDisplay = memo(({ value, title }) => (
  <LinearGaugeComponent title={title}>
    {/* AxesDirective */}
  </LinearGaugeComponent>
));

export default GaugeDisplay;
```

### useCallback for Event Handlers

```tsx
const handleValueChange = React.useCallback((e) => {
  console.log(e.value);
}, []);

<LinearGaugeComponent valueChange={handleValueChange}>
  {/* AxesDirective */}
</LinearGaugeComponent>
```

### Debounce Rapid Updates

```tsx
// Debounce on your state updates so the pointer doesn't re-render too frequently
```

## Combining Multiple Features

### Comprehensive Example

```tsx
import React, { useState, useRef, useEffect, useCallback } from 'react';
import {
  LinearGaugeComponent,
  AxesDirective,
  AxisDirective,
  RangesDirective,
  RangeDirective,
  PointersDirective,
  PointerDirective,
  AnnotationsDirective,
  AnnotationDirective
} from '@syncfusion/ej2-react-lineargauge';

export function App() {
  const gaugeRef = useRef(null);
  const [value, setValue] = useState(50);

  useEffect(() => {
    const interval = setInterval(() => {
      setValue((prev) => {
        const newVal = prev + (Math.random() - 0.5) * 30;
        return Math.max(0, Math.min(100, newVal));
      });
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  const handleValueChange = useCallback((e) => {
    console.log('Manual pointer adjustment:', e.value);
    setValue(e.value);
  }, []);

  return (
    <div style={{ padding: '20px' }}>
      <div style={{ marginBottom: '10px' }}>
        <button onClick={() => gaugeRef.current?.export('PDF', 'gauge.pdf', false, true)}>
          Export as PDF
        </button>
      </div>

      <LinearGaugeComponent
        ref={gaugeRef}
        title="Temperature Monitor"
        valueChange={handleValueChange}
        tooltip={{ enable: true, format: '{value}°C' }}
        height="400px"
      >
        <AxesDirective>
          <AxisDirective minimum={0} maximum={100} labelStyle={{ format: '{value}°C' }}>
            <RangesDirective>
              <RangeDirective start={0} end={33} color="#4CAF50" />
              <RangeDirective start={33} end={66} color="#FFC107" />
              <RangeDirective start={66} end={100} color="#F44336" />
            </RangesDirective>

            <PointersDirective>
              <PointerDirective value={value} enableDrag={true} animationDuration={800} />
            </PointersDirective>
          </AxisDirective>
        </AxesDirective>

        <AnnotationsDirective>
          <AnnotationDirective
            content={`<div style='font-weight: bold; font-size: 18px;'>${Math.round(value)}°C</div>`}
            x={50}
            y={50}
          />
        </AnnotationsDirective>
      </LinearGaugeComponent>
    </div>
  );
}

export default App;
```
