# Common Patterns & Use Cases

Refer to the API quick guide: [api-reference.md](api-reference.md) for exact prop, method and directive names used in these patterns.

## Table of Contents
- [Speedometer Pattern](#speedometer-pattern)
- [Progress/Percentage Gauge](#progresspercentage-gauge)
- [Temperature Gauge](#temperature-gauge)
- [Multi-Pointer Comparison](#multi-pointer-comparison)
- [Real-Time Monitoring Dashboard](#real-time-monitoring-dashboard)
- [Performance Troubleshooting](#performance-troubleshooting)
  - [Gauge Renders Slowly](#issue-gauge-renders-slowly-with-real-time-updates)
  - [Multiple Gauges Cause Performance Issues](#issue-multiple-gauges-cause-performance-issues)
  - [Large Ranges or Pointers Overlap](#issue-large-ranges-or-pointers-overlap)
  - [Export/Print Produces Blurry Output](#issue-exportprint-produces-blurry-output)
- [Accessibility Best Practices](#accessibility-best-practices)
- [Performance Tips](#performance-tips)

---

## Speedometer Pattern

Classic speedometer showing speed with colored zones:

```tsx
import * as React from "react";
import { createRoot } from 'react-dom/client';
import React from 'react';
import { CircularGaugeComponent, AxesDirective, AxisDirective,
         PointersDirective, PointerDirective, RangesDirective, RangeDirective,
         AnnotationsDirective, AnnotationDirective }
  from '@syncfusion/ej2-react-circulargauge';

export function App() {
  const [speed, setSpeed] = React.useState(60);

  return (
    <div style={{ height: '600px' }}>
      <CircularGaugeComponent
        title="Speedometer"
        titleStyle={{ size: '22px', color: '#424242' }}
      >
        <AxesDirective>
          <AxisDirective
            startAngle={270}
            endAngle={90}
            minimum={0}
            maximum={240}
            lineStyle={{ width: 2, color: '#e0e0e0' }}
            majorTicks={{
              interval: 20,
              width: 2,
              color: '#616161',
              offset: 5
            }}
            minorTicks={{
              interval: 4,
              width: 1,
              color: '#9e9e9e',
              offset: 5
            }}
            labelStyle={{
              color: '#616161',
              offset: 15,
              format: '{value}'
            }}
          >
            <RangesDirective>
              <RangeDirective
                start={0}
                end={80}
                color='#4caf50'
                startWidth={12}
                endWidth={12}
                label='Safe'
              />
              <RangeDirective
                start={80}
                end={160}
                color='#fbc02d'
                startWidth={12}
                endWidth={12}
                label='Caution'
              />
              <RangeDirective
                start={160}
                end={240}
                color='#f44336'
                startWidth={12}
                endWidth={12}
                label='Danger'
              />
            </RangesDirective>

            <PointersDirective>
              <PointerDirective
                value={speed}
                type='Needle'
                radius='80%'
                pointerWidth={5}
                color='#424242'
                animation={{
                  enable: true,
                  duration: 300
                }}
                cap={{
                  radius: 10,
                  color: '#424242',
                  border: {
                    color: '#ffffff',
                    width: 2
                  }
                }}
                needleTail={{
                  length: '20%',
                  color: '#424242'
                }}
              />
            </PointersDirective>

            <AnnotationsDirective>
              <AnnotationDirective
                content={`${Math.round(speed)} km/h`}
                radius="0%"
                angle={0}
                textStyle={{
                  size: '24px',
                  fontWeight: 'bold',
                  color: '#1976d2'
                }}
              />
            </AnnotationsDirective>
          </AxisDirective>
        </AxesDirective>
      </CircularGaugeComponent>

      <div style={{ marginTop: '20px' }}>
        <input
          type="range"
          min="0"
          max="240"
          value={speed}
          onChange={(e) => setSpeed(Number(e.target.value))}
          style={{ width: '100%' }}
        />
      </div>
    </div>
  );
}
const root = createRoot(document.getElementById('container'));
root.render(<App />);
```

---

## Progress/Percentage Gauge

Circular progress indicator showing completion percentage:

```tsx
eimport * as React from "react";
import { createRoot } from 'react-dom/client';
import React from 'react';
import { CircularGaugeComponent, AxesDirective, AxisDirective,
         PointersDirective, PointerDirective, RangesDirective, RangeDirective,
         AnnotationsDirective, AnnotationDirective }
  from '@syncfusion/ej2-react-circulargauge';

  export function ProgressGauge() {
    const [progress, setProgress] = React.useState(65);
  
    return (
      <div style={{ height: '400px' }}>
        <CircularGaugeComponent
          title="Project Progress"
          titleStyle={{ size: '18px' }}
          background='#f5f5f5'
        >
          <AxesDirective>
            <AxisDirective
              startAngle={270}
              endAngle={90}
              minimum={0}
              maximum={100}
              lineStyle={{ width: 0 }}  // No axis line
              majorTicks={{ interval: 0 }}  // No ticks
              minorTicks={{ interval: 0 }}
              labelStyle={{ size: '0px' }}  // No labels
            >
              <RangesDirective>
                {/* Background range */}
                <RangeDirective
                  start={0}
                  end={100}
                  color='#e0e0e0'
                  startWidth={20}
                  endWidth={20}
                />
                {/* Progress range */}
                <RangeDirective
                  start={0}
                  end={progress}
                  color='#4caf50'
                  startWidth={20}
                  endWidth={20}
                />
              </RangesDirective>
  
              <PointersDirective>
                <PointerDirective
                  value={0}  // Don't show pointer
                  type='Needle'
                  radius='0%'
                />
              </PointersDirective>
  
              <AnnotationsDirective>
                <AnnotationDirective
                  content={`${progress}%`}
                  radius="0%"
                  textStyle={{
                    size: '36px',
                    fontWeight: 'bold',
                    color: '#1976d2'
                  }}
                />
                <AnnotationDirective
                  content="Complete"
                  radius="0%"
                  angle={90}
                  textStyle={{
                    size: '14px',
                    color: '#757575'
                  }}
                />
              </AnnotationsDirective>
            </AxisDirective>
          </AxesDirective>
        </CircularGaugeComponent>
      </div>
    );
  }
const root = createRoot(document.getElementById('container'));
root.render(<ProgressGauge />);
```

---

## Temperature Gauge

Monitor temperature with intuitive color zones:

```tsx
import * as React from "react";
import { createRoot } from 'react-dom/client';
import React from 'react';
import { CircularGaugeComponent, AxesDirective, AxisDirective,
         PointersDirective, PointerDirective, RangesDirective, RangeDirective,
         AnnotationsDirective, AnnotationDirective }
  from '@syncfusion/ej2-react-circulargauge';

  export function TemperatureGauge() {
    const [temperature, setTemperature] = React.useState(22);
  
    const getStatus = () => {
      if (temperature < 0) return 'Frozen';
      if (temperature < 15) return 'Cold';
      if (temperature < 25) return 'Comfortable';
      if (temperature < 35) return 'Warm';
      return 'Hot';
    };
  
    return (
      <div style={{ height: '500px' }}>
        <CircularGaugeComponent
          title="Temperature Monitor"
        >
          <AxesDirective>
            <AxisDirective
              minimum={-50}
              maximum={50}
              startAngle={270}
              endAngle={90}
              lineStyle={{ width: 2, color: '#90caf9' }}
              labelStyle={{
                format: '{value}°C',
                color: '#1976d2'
              }}
              majorTicks={{
                interval: 10,
                color: '#1976d2'
              }}
            >
              <RangesDirective>
                <RangeDirective
                  start={-50}
                  end={0}
                  color='#2196f3'
                  startWidth={15}
                  endWidth={15}
                  label='Below 0°C'
                />
                <RangeDirective
                  start={0}
                  end={15}
                  color='#4caf50'
                  startWidth={15}
                  endWidth={15}
                  label='Cold'
                />
                <RangeDirective
                  start={15}
                  end={25}
                  color='#8bc34a'
                  startWidth={15}
                  endWidth={15}
                  label='Comfort'
                />
                <RangeDirective
                  start={25}
                  end={35}
                  color='#ff9800'
                  startWidth={15}
                  endWidth={15}
                  label='Warm'
                />
                <RangeDirective
                  start={35}
                  end={50}
                  color='#f44336'
                  startWidth={15}
                  endWidth={15}
                  label='Hot'
                />
              </RangesDirective>
  
              <PointersDirective>
                <PointerDirective
                  value={temperature}
                  type='Needle'
                  radius='80%'
                  color='#616161'
                  animation={{ enable: true, duration: 500 }}
                />
              </PointersDirective>
  
              <AnnotationsDirective>
                <AnnotationDirective
                  content={`${temperature}°C`}
                  radius="0%"
                  textStyle={{ size: '28px', fontWeight: 'bold' }}
                />
                <AnnotationDirective
                  content={getStatus()}
                  radius="0%"
                  angle={90}
                  textStyle={{ size: '16px', color: '#757575' }}
                />
              </AnnotationsDirective>
            </AxisDirective>
          </AxesDirective>
        </CircularGaugeComponent>
  
        <div style={{ marginTop: '20px' }}>
          <input
            type="range"
            min="-50"
            max="50"
            value={temperature}
            onChange={(e) => setTemperature(Number(e.target.value))}
            style={{ width: '100%' }}
          />
        </div>
      </div>
    );
  }
const root = createRoot(document.getElementById('container'));
root.render(<TemperatureGauge />);
```

---

## Multi-Pointer Comparison

Compare multiple values on same gauge:

```tsx
import * as React from 'react';
import { createRoot } from 'react-dom/client';
import React from 'react';
import {
  CircularGaugeComponent,
  AxesDirective,
  AxisDirective,
  PointersDirective,
  PointerDirective,
  RangesDirective,
  RangeDirective,
  AnnotationsDirective,
  AnnotationDirective,
} from '@syncfusion/ej2-react-circulargauge';

export function MultiPointerGauge() {
  return (
    <div style={{ height: '500px' }}>
      <CircularGaugeComponent title="Performance Comparison">
        <AxesDirective>
          <AxisDirective
            minimum={0}
            maximum={100}
            startAngle={270}
            endAngle={90}
          >
            <RangesDirective>
              <RangeDirective
                start={0}
                end={30}
                color="#4caf50"
                startWidth={10}
                endWidth={10}
              />
              <RangeDirective
                start={30}
                end={60}
                color="#fbc02d"
                startWidth={10}
                endWidth={10}
              />
              <RangeDirective
                start={60}
                end={100}
                color="#f44336"
                startWidth={10}
                endWidth={10}
              />
            </RangesDirective>

            <PointersDirective>
              {/* Target/Goal */}
              <PointerDirective
                value={80}
                type="Marker"
                markerShape="Circle"
                markerWidth={16}
                markerHeight={16}
                color="#1976d2"
                radius="85%"
              />
              {/* Actual */}
              <PointerDirective
                value={65}
                type="Needle"
                radius="80%"
                color="#f44336"
              />
              {/* Forecast */}
              <PointerDirective
                value={72}
                type="Marker"
                markerShape="Triangle"
                markerWidth={14}
                markerHeight={14}
                color="#ff9800"
                radius="75%"
              />
            </PointersDirective>

            <AnnotationsDirective>
              <AnnotationDirective
                content="Legend:"
                radius="120%"
                angle={270}
                textStyle={{ size: '12px' }}
              />
              <AnnotationDirective
                content="● Actual: 65%"
                radius="120%"
                angle={260}
                textStyle={{ size: '11px', color: '#f44336' }}
              />
              <AnnotationDirective
                content="● Target: 80%"
                radius="120%"
                angle={250}
                textStyle={{ size: '11px', color: '#1976d2' }}
              />
              <AnnotationDirective
                content="▲ Forecast: 72%"
                radius="120%"
                angle={240}
                textStyle={{ size: '11px', color: '#ff9800' }}
              />
            </AnnotationsDirective>
          </AxisDirective>
        </AxesDirective>
      </CircularGaugeComponent>
    </div>
  );
}
const root = createRoot(document.getElementById('container'));
root.render(<MultiPointerGauge />);

```

---

## Real-Time Monitoring Dashboard

Complete dashboard with multiple real-time gauges:

```tsx
import * as React from 'react';
import { createRoot } from 'react-dom/client';
import React from 'react';
import {
  CircularGaugeComponent,
  AxesDirective,
  AxisDirective,
  PointersDirective,
  PointerDirective,
  RangesDirective,
  RangeDirective,
  AnnotationsDirective,
  AnnotationDirective,
} from '@syncfusion/ej2-react-circulargauge';
import React, { useState, useEffect } from 'react';

export function RealtimeDashboard() {
  const [metrics, setMetrics] = useState({
    cpu: 45,
    memory: 60,
    disk: 75,
    network: 30,
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics({
        cpu: Math.max(0, Math.min(100, 40 + Math.random() * 60)),
        memory: Math.max(0, Math.min(100, 45 + Math.random() * 50)),
        disk: Math.max(0, Math.min(100, 70 + Math.random() * 20)),
        network: Math.max(0, Math.min(100, 20 + Math.random() * 60)),
      });
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  const MetricGauge = ({ title, value, unit }) => (
    <div style={{ height: '350px', padding: '10px' }}>
      <CircularGaugeComponent title={title}>
        <AxesDirective>
          <AxisDirective minimum={0} maximum={100}>
            <RangesDirective>
              <RangeDirective
                start={0}
                end={30}
                color="#4caf50"
                startWidth={10}
                endWidth={10}
              />
              <RangeDirective
                start={30}
                end={60}
                color="#fbc02d"
                startWidth={10}
                endWidth={10}
              />
              <RangeDirective
                start={60}
                end={100}
                color="#f44336"
                startWidth={10}
                endWidth={10}
              />
            </RangesDirective>
            <PointersDirective>
              <PointerDirective
                value={value}
                animation={{ enable: true, duration: 500 }}
              />
            </PointersDirective>
            <AnnotationsDirective>
              <AnnotationDirective
                content={`${value.toFixed(1)}${unit}`}
                radius="0%"
                textStyle={{ size: '22px', fontWeight: 'bold' }}
              />
            </AnnotationsDirective>
          </AxisDirective>
        </AxesDirective>
      </CircularGaugeComponent>
    </div>
  );

  return (
    <div
      style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
        gap: '10px',
        padding: '20px',
        backgroundColor: '#fafafa',
      }}
    >
      <MetricGauge title="CPU Usage" value={metrics.cpu} unit="%" />
      <MetricGauge title="Memory Usage" value={metrics.memory} unit="%" />
      <MetricGauge title="Disk Usage" value={metrics.disk} unit="%" />
      <MetricGauge title="Network" value={metrics.network} unit="%" />
    </div>
  );
}
const root = createRoot(document.getElementById('container'));
root.render(<RealtimeDashboard />);

```

---

## Performance Troubleshooting

### Common Issues and Solutions

#### Issue: Gauge Renders Slowly with Real-Time Updates

**Cause:** Frequent re-renders with unnecessary animations

**Solution:** Throttle updates and use `shouldComponentUpdate`:

```tsx
import React, { useState, useEffect, useCallback } from 'react';

export function OptimizedGauge() {
  const [value, setValue] = useState(50);
  const [lastUpdate, setLastUpdate] = useState(Date.now());

  useEffect(() => {
    const interval = setInterval(() => {
      const now = Date.now();
      // Only update if 500ms has passed
      if (now - lastUpdate > 500) {
        setValue(Math.random() * 100);
        setLastUpdate(now);
      }
    }, 500);

    return () => clearInterval(interval);
  }, [lastUpdate]);

  return (
    <CircularGaugeComponent>
      {/* gauge with optimized updates */}
    </CircularGaugeComponent>
  );
}
```

#### Issue: Multiple Gauges Cause Performance Issues

**Solution:** Lazy load or virtualize gauges:

```tsx
import React, { useState, lazy, Suspense } from 'react';

const GaugeComponent = lazy(() =>
  Promise.resolve({ default: () => <CircularGaugeComponent>{/* */}</CircularGaugeComponent> })
);

export function EfficientDashboard() {
  const [visibleGauges, setVisibleGauges] = useState([0, 1]);

  return (
    <div>
      {visibleGauges.map((index) => (
        <Suspense key={index} fallback={<div>Loading...</div>}>
          <GaugeComponent />
        </Suspense>
      ))}
    </div>
  );
}
```

#### Issue: Large Ranges or Pointers Overlap

**Solution:** Adjust radius and pointer width:

```tsx
// Spread out multiple pointers
<PointersDirective>
  <PointerDirective value={30} radius="60%" pointerWidth={3} />
  <PointerDirective value={50} radius="70%" pointerWidth={3} />
  <PointerDirective value={70} radius="80%" pointerWidth={3} />
</PointersDirective>
```

#### Issue: Export/Print Produces Blurry Output

**Solution:** Ensure sufficient container size before export:

```tsx
// Make container larger for export
<div style={{ height: '800px', width: '800px' }}>
  <CircularGaugeComponent ref={gaugeRef}>
    {/* gauge */}
  </CircularGaugeComponent>
</div>

// Then export
gaugeRef.current?.export('PNG', 'gauge.png');
```

---

## Accessibility Best Practices

- Add `ariaLabel` for all gauges
- Use sufficient color contrast (minimum 4.5:1)
- Test keyboard navigation
- Provide text alternatives for complex visualizations
- Use `aria-live` for real-time updates

---

## Performance Tips

- Throttle real-time updates to ~500-1000ms
- Disable animations for frequent updates
- Limit to 4-6 gauges per page
- Use SVG export for printing (better quality)
- Lazy load gauges outside viewport
- Avoid complex HTML in annotations
