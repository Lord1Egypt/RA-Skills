# Types and Shapes for Progress Bar

## Table of Contents

- [Linear Progress Bar](#linear-progress-bar)
  - [Basic Linear Example](#basic-linear-example)
  - [When to Use Linear](#when-to-use-linear)
  - [Styling Linear Bars](#styling-linear-bars)
- [Circular Progress Bar](#circular-progress-bar)
  - [Basic Circular Example](#basic-circular-example)
  - [When to Use Circular](#when-to-use-circular)
  - [Sizing Circular Bars](#sizing-circular-bars)
- [Semi-Circular Progress Bar](#semi-circular-progress-bar)
  - [Basic Semi-Circular Example](#basic-semi-circular-example)
  - [When to Use Semi-Circular](#when-to-use-semi-circular)
  - [Sizing Semi-Circular Bars](#sizing-semi-circular-bars)
- [Type Comparison](#type-comparison)
- [Choosing the Right Type](#choosing-the-right-type)
  - [Decision Tree](#decision-tree)
  - [Use Case Examples](#use-case-examples)
- [Real-World Examples](#real-world-examples)
  - [Example 1: File Upload with Progress](#example-1-file-upload-with-progress)
  - [Example 2: Dashboard with Multiple Types](#example-2-dashboard-with-multiple-types)
  - [Example 3: Mobile-Responsive Layout](#example-3-mobile-responsive-layout)
- [Performance Notes](#performance-notes)
- [Next Steps](#next-steps)

The Progress Bar component supports three distinct shapes for displaying progress, each with different use cases and visual presentations.

## Linear Progress Bar

The **Linear** type is the default and most common choice for progress visualization. It displays progress as a horizontal bar that fills from left to right (or right to left in RTL).

### Basic Linear Example

```tsx
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

function App() {
  return (
    <ProgressBarComponent
      id="linear"
      type="Linear"
      value={75}
      height="60"
      animation={{
        enable: true,
        duration: 2000,
        delay: 0
      }}
    />
  );
}

export default App;
```

### When to Use Linear

- **File downloads/uploads:** Shows bytes downloaded
- **Task completion:** Display step progress (e.g., 5 of 10 steps)
- **Page loading:** Webpage loading progress
- **Batch operations:** Processing multiple items
- **Installations:** Software installation progress

### Styling Linear Bars

```tsx
// Thin progress bar (default)
<ProgressBarComponent
  type="Linear"
  value={50}
  height="4"
/>

// Thick progress bar (status bar)
<ProgressBarComponent
  type="Linear"
  value={50}
  height="30"
/>

// Full width with height
<ProgressBarComponent
  type="Linear"
  value={50}
  height="60"
  width="100%"
/>
```

**Height guidelines:**
- **4-8px:** Default thin bars (subtle background indicator)
- **20-40px:** Prominent status bars (clear visual focus)
- **60px+:** Large display bars (dashboard/kiosk displays)

## Circular Progress Bar

The **Circular** type displays progress as a circular arc or donut chart. Progress fills from the top and continues clockwise.

### Basic Circular Example

```tsx
<ProgressBarComponent
  id="circular"
  type="Circular"
  value={65}
  height="160px"
  animation={{
    enable: true,
    duration: 2000,
    delay: 0
  }}
/>
```

### When to Use Circular

- **Compact spaces:** Sidebars, widgets, cards
- **File uploads in dialogs:** Limited width constraints
- **Dashboard widgets:** Circular gauges and metrics
- **Process status:** Visual indicators in status pages
- **Time-based progress:** Countdown timers, session timers

### Sizing Circular Bars

```tsx
// Small indicator (compact)
<ProgressBarComponent
  type="Circular"
  value={50}
  height="80px"
/>

// Medium indicator (common)
<ProgressBarComponent
  type="Circular"
  value={50}
  height="160px"
/>

// Large indicator (prominent)
<ProgressBarComponent
  type="Circular"
  value={50}
  height="280px"
/>
```

**Size guidelines:**
- **60-80px:** Compact indicators (inline, sidebars)
- **120-160px:** Standard indicators (cards, widgets)
- **200-280px:** Large prominent indicators (dashboards)
- **300px+:** Very large display (public displays, kiosks)

## Semi-Circular Progress Bar

The **Semicircle** type displays progress as a half-circle arc, useful for specialized layouts and limited vertical space.

### Basic Semi-Circular Example

```tsx
<ProgressBarComponent
  id="semicircle"
  type="Semicircle"
  value={75}
  height="160px"
  animation={{
    enable: true,
    duration: 2000
  }}
/>
```

### When to Use Semi-Circular

- **Dashboard panels:** Stacked in limited height areas
- **Mobile layouts:** Width-constrained vertical stacks
- **Industrial displays:** Gauge-style indicators
- **Stats cards:** KPI displays
- **Process indicators:** Multi-step workflows

### Sizing Semi-Circular Bars

```tsx
// Compact semi-circle
<ProgressBarComponent
  type="Semicircle"
  value={50}
  height="100px"
/>

// Standard semi-circle
<ProgressBarComponent
  type="Semicircle"
  value={50}
  height="160px"
/>

// Large semi-circle
<ProgressBarComponent
  type="Semicircle"
  value={50}
  height="240px"
/>
```

## Type Comparison

| Aspect | Linear | Circular | Semicircle |
|--------|--------|----------|-----------|
| **Space** | Full width horizontal | Compact square | Compact half-height |
| **Best for** | Bars, downloads, steps | Widgets, dashboards | Cards, panels |
| **Height control** | Via `height` prop | Via `height` (diameter) | Via `height` (radius) |
| **RTL support** | Full (auto-reversed) | Full (from top) | Full (from top) |
| **Readability** | Excellent in headers | Good in sidebars | Best in cards |
| **Mobile** | Better | Better | Best |

## Choosing the Right Type

### Decision Tree

```
Do you have full width (>300px)?
├─ YES
│  └─ Use LINEAR
│     (Best for full-width bars, headers, sections)
│
└─ NO (limited space)
   ├─ Height available >120px?
   │  ├─ YES → Use CIRCULAR
   │  │       (Dashboard widgets, cards)
   │  │
   │  └─ NO (<120px) → Use SEMICIRCLE
   │               (Compact cards, mobile)
```

### Use Case Examples

**File Upload Dialog:**
```tsx
// Limited dialog width → Use Circular
<ProgressBarComponent
  type="Circular"
  value={uploadProgress}
  height="120px"
/>
```

**Page Loading Bar:**
```tsx
// Full page width → Use Linear
<ProgressBarComponent
  type="Linear"
  value={pageLoadProgress}
  height="4"
/>
```

**Dashboard Metric:**
```tsx
// Card widget (300x200px) → Use Circular or Semicircle
<div style={{ width: '300px', height: '200px' }}>
  <ProgressBarComponent
    type="Circular"
    value={cpuUsage}
    height="150px"
  />
</div>
```

## Real-World Examples

### Example 1: File Upload with Progress

```tsx
import { useState } from 'react';
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

function FileUploader() {
  const [uploadProgress, setUploadProgress] = useState(0);
  const [fileName, setFileName] = useState('');
  const [status, setStatus] = useState('idle');

  const handleUpload = (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setFileName(file.name);
    setUploadProgress(0);
    setStatus('uploading');

    // Simulate upload with realistic progression
    let progress = 0;
    const interval = setInterval(() => {
      progress += Math.random() * 20;
      if (progress >= 100) {
        setUploadProgress(100);
        setStatus('complete');
        clearInterval(interval);
        setTimeout(() => {
          setUploadProgress(0);
          setStatus('idle');
        }, 2000);
      } else {
        setUploadProgress(Math.min(progress, 99));
      }
    }, 500);
  };

  return (
    <div style={{ width: '100%', maxWidth: '500px' }}>
      <h3>Upload File</h3>
      {fileName && <p>File: {fileName}</p>}
      <ProgressBarComponent
        type="Linear"
        value={uploadProgress}
        height="30"
        showProgressValue={true}
        progressValueFormat="N0 '%'"
        animation={{ enable: true, duration: 500 }}
      />
      <input 
        type="file" 
        onChange={handleUpload}
        disabled={status === 'uploading'}
      />
      <p>Status: {status.toUpperCase()}</p>
    </div>
  );
}

export default FileUploader;
```

### Example 2: Dashboard with Multiple Types

```tsx
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

function Dashboard() {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px' }}>
      {/* Full-width metric */}
      <div style={{ gridColumn: '1 / -1' }}>
        <h4>Overall Progress</h4>
        <ProgressBarComponent
          type="Linear"
          value={65}
          height="20"
        />
      </div>

      {/* Compact circular metrics */}
      <div>
        <h4>CPU Usage</h4>
        <ProgressBarComponent
          type="Circular"
          value={45}
          height="120px"
        />
      </div>

      <div>
        <h4>Memory Usage</h4>
        <ProgressBarComponent
          type="Circular"
          value={72}
          height="120px"
        />
      </div>

      <div>
        <h4>Disk Usage</h4>
        <ProgressBarComponent
          type="Circular"
          value={38}
          height="120px"
        />
      </div>
    </div>
  );
}

export default Dashboard;
```

### Example 3: Mobile-Responsive Layout

```tsx
import { useState, useEffect } from 'react';
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

function ResponsiveProgress() {
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);
  const [value, setValue] = useState(50);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div style={{
      padding: '20px',
      textAlign: 'center'
    }}>
      <h3>Responsive Progress Bar</h3>
      <p>Screen Size: {isMobile ? 'Mobile' : 'Desktop'}</p>

      <ProgressBarComponent
        type={isMobile ? "Semicircle" : "Linear"}
        value={value}
        height={isMobile ? "100px" : "40"}
        showProgressValue={true}
        animation={{ enable: true, duration: 500 }}
      />

      <input
        type="range"
        min="0"
        max="100"
        value={value}
        onChange={(e) => setValue(parseInt(e.target.value))}
        style={{ width: '100%', marginTop: '20px' }}
      />
    </div>
  );
}

export default ResponsiveProgress;
```

## Performance Notes

- **Linear:** Fastest rendering, best for animations, ideal for high-frequency updates
- **Circular:** Slightly slower (SVG rendering), acceptable performance for real-time updates
- **Semicircle:** Similar performance to Circular, excellent for dashboard scenarios

**Performance Tips:**
- For real-time updates (>100 times/sec), prefer Linear type
- Disable animations for better performance on low-end devices
- Use `animation={{ enable: false }}` for non-animated scenarios
- Circular types use SVG, so rendering is efficient but slightly more CPU-intensive

### Browser Compatibility

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| Linear | ✓ | ✓ | ✓ | ✓ |
| Circular | ✓ | ✓ | ✓ | ✓ |
| Semicircle | ✓ | ✓ | ✓ | ✓ |
| Animation | ✓ | ✓ | ✓ | ✓ |
| SVG Rendering | ✓ | ✓ | ✓ | ✓ |

Tested on: IE11+, Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

## Next Steps

- **States & Modes:** Learn Determinate vs. Indeterminate - [states-and-modes.md](states-and-modes.md)
- **Customization:** Style and customize your progress bars - [customization-and-styling.md](customization-and-styling.md)
- **Advanced:** Animations and events - [animations-events-accessibility.md](animations-events-accessibility.md)
