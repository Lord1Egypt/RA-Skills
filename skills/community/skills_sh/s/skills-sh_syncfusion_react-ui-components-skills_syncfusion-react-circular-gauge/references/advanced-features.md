# Advanced Features

## Table of Contents
- [Animation](#animation)
  - [Enable Animation](#enable-animation)
  - [Pointer Animation](#pointer-animation)
  - [Animation Timing](#animation-timing)
  - [Disabling Animation](#disabling-animation)
  - [Animation on Value Change](#animation-on-value-change)
- [User Interaction](#user-interaction)
  - [Tooltip Configuration](#tooltip-configuration)
  - [Tooltip Styling](#tooltip-styling)
  - [Custom Tooltip Template](#custom-tooltip-template)
  - [Mouse Events](#mouse-events)
- [Print and Export](#print-and-export)
  - [Print Gauge](#print-gauge)
  - [Export to Image (PNG)](#export-to-image-png)
  - [Export to PDF](#export-to-pdf)
  - [All Export Options](#all-export-options)
  - [Export with Custom Filename](#export-with-custom-filename)
- [Real-Time Data Binding](#real-time-data-binding)
  - [Update Pointer Value](#update-pointer-value)
  - [Real-Time Updates with Interval](#real-time-updates-with-interval)
  - [API Data Binding](#api-data-binding)
  - [WebSocket Real-Time Updates](#websocket-real-time-updates)
- [Event Handling](#event-handling)
  - [Load Event](#load-event)
  - [Pointer Drag Events](#pointer-drag-events)
  - [Range Interaction Events](#range-interaction-events)
  - [Gauge Mouse Events](#gauge-mouse-events)
  - [Tooltip & Annotation Events](#tooltip--annotation-events)
  - [Axis Label Customization](#axis-label-customization)
- [Multiple Gauge Instances](#multiple-gauge-instances)
  - [Side-by-Side Gauges](#side-by-side-gauges)
  - [Dashboard with Multiple Gauges](#dashboard-with-multiple-gauges)
  - [Responsive Multi-Gauge Layout](#responsive-multi-gauge-layout)
- [Tips and Best Practices](#tips-and-best-practices)

## Animation

### Enable Animation

Animate pointer movements:

```tsx
<CircularGaugeComponent
  animationDuration={1000}  // milliseconds
>
  {/* gauge content */}
</CircularGaugeComponent>
```

### Pointer Animation

Control animation on individual pointers:

```tsx
<PointerDirective
  value={85}
  type='Needle'
  animation={{
    enable: true,
    duration: 1000,  // milliseconds
    delay: 0
  }}
/>
```

### Animation Timing

Control animation behavior:

```tsx
<PointerDirective
  value={75}
  animation={{
    enable: true,
    duration: 500,   // Fast animation
    delay: 100       // Delay before start
  }}
/>

// Slow animation
<PointerDirective
  value={60}
  animation={{
    enable: true,
    duration: 2000,  // 2 seconds
    delay: 0
  }}
/>
```

### Disabling Animation

```tsx
<PointerDirective
  value={50}
  animation={{ enable: false }}
/>
```

### Animation on Value Change

Animate when pointer value changes:

```tsx
import React, { useState } from 'react';
import { CircularGaugeComponent, AxesDirective, AxisDirective,
         PointersDirective, PointerDirective } 
  from '@syncfusion/ej2-react-circulargauge';

export function AnimatedPointer() {
  const [value, setValue] = useState(30);

  const handleUpdate = () => {
    // This triggers animation
    setValue(75);
  };

  return (
    <div>
      <CircularGaugeComponent animationDuration={800}>
        <AxesDirective>
          <AxisDirective minimum={0} maximum={100}>
            <PointersDirective>
              <PointerDirective
                value={value}
                animation={{
                  enable: true,
                  duration: 800
                }}
              />
            </PointersDirective>
          </AxisDirective>
        </AxesDirective>
      </CircularGaugeComponent>
      <button onClick={handleUpdate}>Update Value (Animated)</button>
    </div>
  );
}
```

---

## User Interaction

### Tooltip Configuration

Display values on hover:

```tsx
<CircularGaugeComponent
  tooltip={{
    enable: true,
    type: TooltipType[]  // 'Pointer' | 'Range' | 'Annotation'
  }}
>
  {/* gauge content */}
</CircularGaugeComponent>
```

### Tooltip Styling

```tsx
<CircularGaugeComponent
  tooltip={{
    enable: true,
    type: ['Pointer', 'Range'],
    template: '{value}',  // Custom format
    fill: '#1976d2',
    textStyle: {
      color: '#ffffff',
      size: '14px'
    }
  }}
>
  {/* gauge content */}
</CircularGaugeComponent>
```

### Custom Tooltip Template

```tsx
<CircularGaugeComponent
  tooltip={{
    enable: true,
    template: '<div>Speed: {value} km/h</div>'
  }}
>
  {/* gauge content */}
</CircularGaugeComponent>
```

### Mouse Events

```tsx
import React from 'react';

export function InteractiveGauge() {
  const handleMouseMove = (args: any) => {
    console.log('Mouse position:', args);
  };

  const handleMouseLeave = (args: any) => {
    console.log('Mouse left gauge');
  };

  return (
    <CircularGaugeComponent
      gaugeMouseMove={handleMouseMove}
      mouseLeaveEvent={handleMouseLeave}
    >
      {/* gauge content */}
    </CircularGaugeComponent>
  );
}
```

---

## Print and Export

### Print Gauge

```tsx
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { CircularGaugeComponent, Print, Inject } from '@syncfusion/ej2-react-circulargauge';

export function App() {
  var gaugeInstance;
  function clickHandler() {
    gaugeInstance.print();
  }
  return (<div>
      <ButtonComponent onClick={clickHandler}>
        print
      </ButtonComponent>
      <CircularGaugeComponent
        id="circulargauge"
        allowPrint={true}
        ref={(g) => (gaugeInstance = g)}
      >
        <Inject services={[Print]} />
      </CircularGaugeComponent>
    </div>
  );
}
const root = ReactDOM.createRoot(document.getElementById('container'));
root.render(<App />);
```

### Export to Image (PNG)

```tsx
import * as React from "react";
import * as ReactDOM from "react-dom";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { CircularGaugeComponent, ImageExport, Inject } from '@syncfusion/ej2-react-circulargauge';

export function App() {
  var gaugeInstance;
  function clickHandler(){
     gaugeInstance.export('PNG','Gauge');
  }
    return (<div>
    <ButtonComponent onClick= {clickHandler}>Export</ButtonComponent>
    <CircularGaugeComponent  allowImageExport={true} ref={g => gaugeInstance = g}>
        <Inject services={[ImageExport]} />
    </CircularGaugeComponent>
    </div>);
}
const root = ReactDOM.createRoot(document.getElementById('container'));
root.render(<App />);
```

### Export to PDF

```tsx
  var gaugeInstance;
  function clickHandler(){
    gaugeInstance.export('PDF','Gauge', 0);
  }
```

### All Export Options

```tsx
<div>
  <button onClick={() => gaugeRef.current?.export('PNG', 'gauge.png')}>
    Export PNG
  </button>
  <button onClick={() => gaugeRef.current?.export('PDF', 'gauge.pdf')}>
    Export PDF
  </button>
  <button onClick={() => gaugeRef.current?.export('SVG', 'gauge.svg')}>
    Export SVG
  </button>
  <button onClick={() => gaugeRef.current?.print()}>
    Print
  </button>
</div>
```

### Export with Custom Filename

```tsx
const timestamp = new Date().toISOString().slice(0, 10);
gaugeRef.current?.export('PNG', `gauge-${timestamp}.png`);
```

---

## Real-Time Data Binding

### Update Pointer Value

```tsx
import React, { useState } from 'react';
import { CircularGaugeComponent,AxesDirective , AxisDirective, PointerDirective, PointersDirective} from '@syncfusion/ej2-react-circulargauge';

export function RealTimeGauge() {
  const [value, setValue] = useState(50);

  return (
    <div>
      <CircularGaugeComponent>
        <AxesDirective>
          <AxisDirective minimum={0} maximum={100}>
            <PointersDirective>
              <PointerDirective value={value} />
            </PointersDirective>
          </AxisDirective>
        </AxesDirective>
      </CircularGaugeComponent>
      <button onClick={() => setValue(Math.random() * 100)}>
        Update Value
      </button>
    </div>
  );
}
const root = createRoot(document.getElementById('container'));
root.render(<RealTimeGauge />);
```

### Real-Time Updates with Interval

Monitor changing data:

```tsx
import { createRoot } from 'react-dom/client';
import React, { useState } from 'react';
import { CircularGaugeComponent,AxesDirective , AxisDirective, PointerDirective, PointersDirective} from '@syncfusion/ej2-react-circulargauge';

import React, { useState, useEffect } from 'react';

export function RealtimeMonitor() {
  const [value, setValue] = useState(50);

  useEffect(() => {
    // Simulate real-time data
    const interval = setInterval(() => {
      const newValue = 40 + Math.random() * 60; // Random 40-100
      setValue(newValue);
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <CircularGaugeComponent>
      <AxesDirective>
        <AxisDirective minimum={0} maximum={100}>
          <PointersDirective>
            <PointerDirective
              value={value}
              animation={{ enable: true, duration: 500 }}
            />
          </PointersDirective>
        </AxisDirective>
      </AxesDirective>
    </CircularGaugeComponent>
  );
}
const root = createRoot(document.getElementById('container'));
root.render(<RealtimeMonitor />);
```

### API Data Binding

Fetch and display real data:

```tsx
import React, { useState } from 'react';
import { CircularGaugeComponent,AxesDirective , AxisDirective, PointerDirective, PointersDirective} from '@syncfusion/ej2-react-circulargauge';

import React, { useState, useEffect } from 'react';

export function APIBoundGauge() {
  const [sensorData, setSensorData] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Example API call
        const response = await fetch('/api/sensor/temperature');
        const data = await response.json();
        setSensorData(data.value);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
        setLoading(false);
      }
    };

    // Initial fetch
    fetchData();

    // Poll every 5 seconds
    const interval = setInterval(fetchData, 5000);

    return () => clearInterval(interval);
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <CircularGaugeComponent>
      <AxesDirective>
        <AxisDirective minimum={0} maximum={100}>
          <PointersDirective>
            <PointerDirective value={sensorData} />
          </PointersDirective>
        </AxisDirective>
      </AxesDirective>
    </CircularGaugeComponent>
  );
}
const root = createRoot(document.getElementById('container'));
root.render(<APIBoundGauge />);
```

### WebSocket Real-Time Updates

```tsx
import React, { useState } from 'react';
import { CircularGaugeComponent,AxesDirective , AxisDirective, PointerDirective, PointersDirective} from '@syncfusion/ej2-react-circulargauge';

import React, { useState, useEffect } from 'react';

export function WebSocketGauge() {
  const [value, setValue] = useState(50);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8080/gauge');

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setValue(data.value);
    };

    return () => ws.close();
  }, []);

  return (
    <CircularGaugeComponent>
      <AxesDirective>
        <AxisDirective minimum={0} maximum={100}>
          <PointersDirective>
            <PointerDirective value={value} />
          </PointersDirective>
        </AxisDirective>
      </AxesDirective>
    </CircularGaugeComponent>
  );
}
const root = createRoot(document.getElementById('container'));
root.render(<WebSocketGauge />);
```

---

## Event Handling

See [API Reference](api-reference.md) for full event arg types and method signatures.

### Load Event

Handle gauge initialization:

```tsx
<CircularGaugeComponent
  load={(args: ILoadEventArgs) => {
    console.log('Before gauge load:', args);
  }}
  loaded={(args: ILoadedEventArgs) => {
    console.log('Gauge fully rendered:', args);
  }}
  resized={(args: IResizeEventArgs) => {
    console.log('Gauge resized:', args);
  }}
  animationComplete={(args: IAnimationCompleteEventArgs) => {
    console.log('Animation completed:', args);
  }}
>
  {/* gauge content */}
</CircularGaugeComponent>
```

### Pointer Drag Events

```tsx
<CircularGaugeComponent
  enablePointerDrag={true}
  pointerDragStart={(args: IPointerDragEventArgs) => {
    console.log('Pointer drag started:', args.currentValue);
  }}
  pointerDragMove={(args: IPointerDragEventArgs) => {
    console.log('Pointer dragging:', args.currentValue);
  }}
  pointerDragEnd={(args: IPointerDragEventArgs) => {
    console.log('Pointer drag ended:', args.currentValue);
  }}
>
  {/* gauge content */}
</CircularGaugeComponent>
```

### Range Interaction Events

```tsx
<CircularGaugeComponent
  rangeMouseClick={(args: IMouseEventArgs) => {
    console.log('Range clicked:', args);
  }}
  rangeMouseMove={(args: IMouseEventArgs) => {
    console.log('Range hover:', args);
  }}
  rangeMouseLeave={(args: IMouseEventArgs) => {
    console.log('Range leave:', args);
  }}
>
  {/* gauge content */}
</CircularGaugeComponent>
```

### Gauge Mouse Events

```tsx
<CircularGaugeComponent
  gaugeMouseMove={(args: IMouseEventArgs) => {
    console.log('Mouse move:', args);
  }}
  gaugeMouseLeave={(args: IMouseEventArgs) => {
    console.log('Mouse leave:', args);
  }}
  gaugeMouseDown={(args: IMouseEventArgs) => {
    console.log('Mouse down:', args);
  }}
  gaugeMouseUp={(args: IMouseEventArgs) => {
    console.log('Mouse up:', args);
  }}
>
  {/* gauge content */}
</CircularGaugeComponent>
```
### Tooltip & Annotation Events

```tsx
<CircularGaugeComponent
  tooltipRender={(args: ITooltipRenderEventArgs) => {
    args.content = [`Value: ${args.currentValue}`];
  }}
  annotationRender={(args: IAnnotationRenderEventArgs) => {
    console.log('Annotation rendering:', args);
  }}
>
  {/* gauge content */}
</CircularGaugeComponent>
```

### Axis Label Customization

```tsx
<CircularGaugeComponent
  axisLabelRender={(args: IAxisLabelRenderEventArgs) => {
    args.text = `${args.text}°`;
  }}
>
  {/* gauge content */}
</CircularGaugeComponent>
```

### Complete Event Example

```tsx
import React, { useState } from 'react';
import { CircularGaugeComponent} from '@syncfusion/ej2-react-circulargauge';

import React, { useState, useEffect } from 'react';


export function EventHandlingGauge() {
  const [lastEvent, setLastEvent] = useState('');

  return (
    <div>
      <CircularGaugeComponent
        load={() => setLastEvent('Gauge loaded')}
        pointerDragMove={(args) => setLastEvent(`Pointer value: ${args.value}`)}
        rangeMouseClick={() => setLastEvent('Range clicked')}
      >
        {/* gauge content */}
      </CircularGaugeComponent>
      <p>Last Event: {lastEvent}</p>
    </div>
  );
}
const root = createRoot(document.getElementById('container'));
root.render(<EventHandlingGauge />);
```

---

## Multiple Gauge Instances

### Side-by-Side Gauges

```tsx
import React from 'react';
import { CircularGaugeComponent,AxesDirective , AxisDirective, PointerDirective, PointersDirective} from '@syncfusion/ej2-react-circulargauge';

import React, { useState, useEffect } from 'react';


export function App() {
  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: '1fr 1fr',
      gap: '20px'
    }}>
      <div style={{ height: '400px' }}>
        <CircularGaugeComponent title="Temperature">
          <AxesDirective>
            <AxisDirective minimum={0} maximum={50}>
              <PointersDirective>
                <PointerDirective value={25} />
              </PointersDirective>
            </AxisDirective>
          </AxesDirective>
        </CircularGaugeComponent>
      </div>
    
      <div style={{ height: '400px' }}>
        <CircularGaugeComponent title="Humidity">
          <AxesDirective>
            <AxisDirective minimum={0} maximum={100}>
              <PointersDirective>
                <PointerDirective value={65} />
              </PointersDirective>
            </AxisDirective>
          </AxesDirective>
        </CircularGaugeComponent>
      </div>
    </div>
  );
}
const root = createRoot(document.getElementById('container'));
root.render(<App />);
```

### Dashboard with Multiple Gauges

```tsx

import React, { useState, useEffect } from 'react';
import { CircularGaugeComponent,AxesDirective , AxisDirective, PointerDirective, PointersDirective,RangesDirective,RangeDirective } from '@syncfusion/ej2-react-circulargauge';

export function DashboardGauges() {
  const [metrics, setMetrics] = useState({
    cpu: 45,
    memory: 60,
    disk: 75,
    network: 30
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics({
        cpu: 30 + Math.random() * 50,
        memory: 40 + Math.random() * 40,
        disk: Math.random() * 100,
        network: Math.random() * 100
      });
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
      gap: '20px',
      padding: '20px'
    }}>
      {Object.entries(metrics).map(([label, value]) => (
        <div key={label} style={{ height: '400px' }}>
          <CircularGaugeComponent title={label.toUpperCase()}>
            <AxesDirective>
              <AxisDirective minimum={0} maximum={100}>
                <RangesDirective>
                  <RangeDirective start={0} end={30} color='#4caf50' />
                  <RangeDirective start={30} end={60} color='#fbc02d' />
                  <RangeDirective start={60} end={100} color='#f44336' />
                </RangesDirective>
                <PointersDirective>
                  <PointerDirective
                    value={value}
                    animation={{ enable: true, duration: 500 }}
                  />
                </PointersDirective>
              </AxisDirective>
            </AxesDirective>
          </CircularGaugeComponent>
        </div>
      ))}
    </div>
  );
}
const root = createRoot(document.getElementById('container'));
root.render(<DashboardGauges />);
```

### Responsive Multi-Gauge Layout

```tsx
<div style={{
  display: 'flex',
  flexWrap: 'wrap',
  gap: '20px',
  justifyContent: 'space-around'
}}>
  {/* Gauge 1 */}
  <div style={{
    flex: '1 1 calc(50% - 10px)',
    minWidth: '250px',
    height: '400px'
  }}>
    <CircularGaugeComponent>
      {/* content */}
    </CircularGaugeComponent>
  </div>

  {/* Gauge 2 */}
  <div style={{
    flex: '1 1 calc(50% - 10px)',
    minWidth: '250px',
    height: '400px'
  }}>
    <CircularGaugeComponent>
      {/* content */}
    </CircularGaugeComponent>
  </div>

  {/* Gauge 3 */}
  <div style={{
    flex: '1 1 calc(50% - 10px)',
    minWidth: '250px',
    height: '400px'
  }}>
    <CircularGaugeComponent>
      {/* content */}
    </CircularGaugeComponent>
  </div>
</div>
```

---

## Tips and Best Practices

- **Animation duration:** Keep under 1000ms for responsive feel
- **Export format:** Use PNG for web, SVG for printing with high quality
- **Real-time updates:** Throttle updates to ~1000ms for performance
- **Event handling:** Avoid heavy computations in event handlers
- **Multiple gauges:** Limit to 4-6 on one screen to avoid performance issues
- **Tooltips:** Enable only when necessary to avoid cluttering
