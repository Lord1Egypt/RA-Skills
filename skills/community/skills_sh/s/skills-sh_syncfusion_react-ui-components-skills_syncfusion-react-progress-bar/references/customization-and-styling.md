# Customization and Styling for Progress Bar

## Table of contents

- [Sizing](#sizing)
  - [Height Control](#height-control)
  - [Width Control](#width-control)
  - [Circular Type Sizing](#circular-type-sizing)
- [Colors and Fill](#colors-and-fill)
  - [Track Thickness](#track-thickness)
  - [Progress Thickness](#progress-thickness)
  - [Using CSS Classes](#using-css-classes)
- [Labels and Text](#labels-and-text)
  - [Show Progress Value](#show-progress-value)
  - [Custom Text Format](#custom-text-format)
  - [Labels with State](#labels-with-state)
- [Theme Application](#theme-application)
  - [Theme Characteristics](#theme-characteristics)
  - [Switching Themes Dynamically](#switching-themes-dynamically)
- [CSS Customization](#css-customization)
  - [Complete Custom Styling Example](#complete-custom-styling-example)
  - [Circular Progress Customization](#circular-progress-customization)
- [Range Colors](#range-colors)
- [Striped and Gradient Effects](#striped-and-gradient-effects)
- [Advanced Examples](#advanced-examples)
  - [Example 1: Gradient Progress Bar with Custom Styling](#example-1-gradient-progress-bar-with-custom-styling)
  - [Example 2: Status Color Based on Progress](#example-2-status-color-based-on-progress)
  - [Example 3: Responsive Dashboard](#example-3-responsive-dashboard)
- [Next Steps](#next-steps)

## Sizing

Control the dimensions of your progress bar for different use cases.

### Height Control

```tsx
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

// Thin progress bar (3px)
<ProgressBarComponent
  type="Linear"
  value={50}
  height="3"
/>

// Default (20px)
<ProgressBarComponent
  type="Linear"
  value={50}
  height="20"
/>

// Thick status bar (40px)
<ProgressBarComponent
  type="Linear"
  value={50}
  height="40"
/>

// Very thick (80px)
<ProgressBarComponent
  type="Linear"
  value={50}
  height="80"
/>
```

### Width Control

```tsx
// Full width (default)
<ProgressBarComponent
  type="Linear"
  value={50}
  width="100%"
  height="20"
/>

// Fixed width
<ProgressBarComponent
  type="Linear"
  value={50}
  width="400px"
  height="20"
/>

// Responsive with container
<div style={{ maxWidth: '600px', margin: '0 auto' }}>
  <ProgressBarComponent
    type="Linear"
    value={50}
    width="100%"
    height="20"
  />
</div>
```

### Circular Type Sizing

For circular and semicircle types, `height` represents the diameter (or radius for semicircle):

```tsx
// Compact circular (60px diameter)
<ProgressBarComponent
  type="Circular"
  value={50}
  height="60px"
/>

// Standard circular (120px diameter)
<ProgressBarComponent
  type="Circular"
  value={50}
  height="120px"
/>

// Large circular (200px diameter)
<ProgressBarComponent
  type="Circular"
  value={50}
  height="200px"
/>

// Semicircle (100px radius)
<ProgressBarComponent
  type="Semicircle"
  value={50}
  height="100px"
/>
```

---

## Colors and Fill

Customize colors for different themes and states.

### Track Thickness

```tsx
// Thin track (2px)
<ProgressBarComponent
  type="Linear"
  value={50}
  trackThickness={2}
  height="20"
/>

// Thicker track (4px)
<ProgressBarComponent
  type="Linear"
  value={50}
  trackThickness={4}
  height="20"
/>

// Very thick track (6px)
<ProgressBarComponent
  type="Linear"
  value={50}
  trackThickness={6}
  height="20"
/>
```

### Progress Thickness

```tsx
// Thin progress bar
<ProgressBarComponent
  type="Linear"
  value={50}
  progressThickness={2}
  height="20"
/>

// Standard progress bar
<ProgressBarComponent
  type="Linear"
  value={50}
  progressThickness={4}
  height="20"
/>

// Thick progress bar
<ProgressBarComponent
  type="Linear"
  value={50}
  progressThickness={6}
  height="20"
/>
```

### Using CSS Classes

Customize colors via CSS:

```tsx
import './progress.css';

<ProgressBarComponent
  id="custom"
  type="Linear"
  value={50}
  cssClass="custom-progress"
  height="20"
/>
```

**progress.css:**
```css
/* Primary progress bar */
.custom-progress .e-progress {
  background-color: #4CAF50;
}

/* Track background */
.custom-progress .e-progress-bar {
  background-color: #e0e0e0;
}

/* Secondary progress (buffer) */
.custom-progress .e-progress-secondary {
  background-color: #90CAF9;
}
```

---

## Labels and Text

Display progress values and custom labels.

### Show Progress Value

```tsx
// Display percentage
<ProgressBarComponent
  type="Linear"
  value={75}
  showProgressValue={true}
  progressValueFormat="N0 '%'"
  height="30"
/>
```

**Output:** Shows "75 %" inside or near the progress bar

### Custom Text Format

```tsx
// Different number formats
<ProgressBarComponent
  type="Linear"
  value={50}
  showProgressValue={true}
  progressValueFormat="N1 '%'"  // One decimal: "50.0 %"
  height="30"
/>

<ProgressBarComponent
  type="Linear"
  value={50}
  showProgressValue={true}
  progressValueFormat="0.00 '%'"  // Two decimals: "50.00 %"
  height="30"
/>
```

### Labels with State

```tsx
import { useState } from 'react';
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

function ProgressWithLabel() {
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState('Starting...');

  const handleStart = () => {
    let current = 0;
    const interval = setInterval(() => {
      current += Math.random() * 30;
      if (current >= 100) {
        setProgress(100);
        setStatus('Complete!');
        clearInterval(interval);
      } else {
        setProgress(current);
        setStatus(`Processing: ${Math.round(current)}%`);
      }
    }, 800);
  };

  return (
    <div>
      <h3>{status}</h3>
      <ProgressBarComponent
        type="Linear"
        value={progress}
        showProgressValue={true}
        height="30"
      />
    </div>
  );
}

export default ProgressWithLabel;
```

---

## Theme Application

Syncfusion includes multiple built-in themes for different design systems.



**Theme Characteristics:**

| Theme | Best For | Color Palette | Use Case |
|-------|----------|---------------|----------|
| **Material** | Modern apps | Vibrant, flat colors | Default choice, Material Design |
| **Bootstrap5** | Bootstrap projects | Bootstrap colors | Bootstrap-based applications |
| **Tailwind** | Tailwind projects | Neutral tones | Tailwind CSS environments |
| **Fluent** | Microsoft apps | Modern blue/gray | Office 365 style apps |
| **Fabric** | Office integration | Office colors | Microsoft product integration |
| **HighContrast** | Accessibility | High contrast | Users with visual impairments |

### Switching Themes Dynamically

```tsx
import { useState } from 'react';
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

function App() {
  const [theme, setTheme] = useState('Material');
  const [value, setValue] = useState(65);

  const themes = [
    { id: 'Material', label: 'Material' },
    { id: 'Bootstrap5', label: 'Bootstrap 5' },
    { id: 'Tailwind', label: 'Tailwind' },
    { id: 'Fluent', label: 'Fluent UI' },
    { id: 'Fabric', label: 'Office Fabric' }
  ];

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h3>Theme Selector</h3>

      {/* Theme Dropdown */}
      <select
        value={theme}
        onChange={(e) => setTheme(e.target.value)}
        style={{ padding: '5px', marginBottom: '15px' }}
      >
        {themes.map(t => (
          <option key={t.id} value={t.id}>{t.label}</option>
        ))}
      </select>

      <div style={{ marginTop: '20px' }}>
        <p>
          Current Theme: <strong>{theme}</strong>
        </p>

        <ProgressBarComponent
          type="Linear"
          value={value}
          height="30"
          showProgressValue={true}
          theme={theme}
        />

        <input
          type="range"
          min="0"
          max="100"
          value={value}
          onChange={(e) => setValue(parseInt(e.target.value))}
          style={{ marginTop: '20px', width: '100%' }}
        />
      </div>
    </div>
  );
}

export default App;
```

**Note:** To switch themes dynamically in production, you would need to:
1. Dynamically import CSS files based on theme selection
2. Or use CSS variables that can be changed at runtime
3. Reference the Syncfusion documentation for dynamic theming

---

## CSS Customization

Fine-tune styling with custom CSS.

### Complete Custom Styling Example

```tsx
import './custom-progress.css';
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

function App() {
  return (
    <ProgressBarComponent
      id="custom"
      type="Linear"
      value={60}
      cssClass="custom-progress-theme"
      height="40"
      showProgressValue={true}
    />
  );
}

export default App;
```

**custom-progress.css:**
```css
/* Container styling */
.custom-progress-theme {
  margin: 20px 0;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Track background */
.custom-progress-theme .e-progress-bar {
  background: linear-gradient(to right, #f0f0f0, #e8e8e8);
  border-radius: 4px;
}

/* Progress fill */
.custom-progress-theme .e-progress {
  background: linear-gradient(to right, #667eea, #764ba2);
  border-radius: 4px;
  transition: width 0.3s ease;
}

/* Secondary progress (buffer) */
.custom-progress-theme .e-progress-secondary {
  background: linear-gradient(to right, rgba(102, 126, 234, 0.3), rgba(118, 75, 162, 0.3));
  border-radius: 4px;
}

/* Progress value text */
.custom-progress-theme .e-progress-value {
  color: #333;
  font-weight: 600;
  font-size: 14px;
}
```

### Circular Progress Customization

```css
/* Circular progress styling */
.custom-circular .e-progressbar-svg {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

.custom-circular .e-progress-circle {
  stroke: url(#progressGradient);
  stroke-width: 6;
}

.custom-circular .e-progress-track-circle {
  stroke: #e8e8e8;
  stroke-width: 6;
}
```

---

## Range Colors

Define different colors for different progress ranges:

```tsx
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

function RangeColorProgress() {
  const rangeColors = [
    { color: '#FF3333', start: 0, end: 25 },    // Red: 0-25%
    { color: '#FF9800', start: 25, end: 50 },   // Orange: 25-50%
    { color: '#FFC107', start: 50, end: 75 },   // Yellow: 50-75%
    { color: '#4CAF50', start: 75, end: 100 }   // Green: 75-100%
  ];

  return (
    <div>
      <h3>Range Color Progress</h3>
      <ProgressBarComponent
        type="Linear"
        value={65}
        height="40"
        showProgressValue={true}
        rangeColors={rangeColors}
        animation={{ enable: true, duration: 1000 }}
      />
      <p>0-25%: Red | 25-50%: Orange | 50-75%: Yellow | 75-100%: Green</p>
    </div>
  );
}

export default RangeColorProgress;
```

## Striped and Gradient Effects

Add visual variety to progress bars:

```tsx
// Striped Progress Bar
<ProgressBarComponent
  type="Linear"
  value={50}
  height="30"
  isStriped={true}
/>

// Gradient Progress Bar
<ProgressBarComponent
  type="Linear"
  value={50}
  height="30"
  isGradient={true}
/>

// Combine both
<ProgressBarComponent
  type="Linear"
  value={50}
  height="30"
  isStriped={true}
  isGradient={true}
/>
```

## Advanced Examples

### Example 1: Gradient Progress Bar with Custom Styling

```tsx
import './gradient-progress.css';

function GradientProgress() {
  return (
    <ProgressBarComponent
      id="gradient"
      type="Linear"
      value={65}
      cssClass="gradient-progress"
      height="40"
      showProgressValue={true}
    />
  );
}

export default GradientProgress;
```

**gradient-progress.css:**
```css
.gradient-progress .e-progress {
  background: linear-gradient(
    to right,
    #FF6B6B 0%,
    #FFA06B 25%,
    #FFD06B 50%,
    #6BCB77 75%,
    #4D96FF 100%
  );
}
```

### Example 2: Status Color Based on Progress

```tsx
import { useState } from 'react';
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

function StatusProgress() {
  const [progress, setProgress] = useState(30);

  const getStatusClass = () => {
    if (progress < 33) return 'status-low';
    if (progress < 67) return 'status-medium';
    return 'status-high';
  };

  const getStatusText = () => {
    if (progress < 33) return '⚠️ Low';
    if (progress < 67) return '🔄 Medium';
    return '✓ High';
  };

  return (
    <div>
      <h3>{getStatusText()}</h3>
      <ProgressBarComponent
        type="Linear"
        value={progress}
        cssClass={`status-progress ${getStatusClass()}`}
        height="30"
        showProgressValue={true}
      />
      <input
        type="range"
        min="0"
        max="100"
        value={progress}
        onChange={(e) => setProgress(parseInt(e.target.value))}
      />
    </div>
  );
}

export default StatusProgress;
```

**CSS:**
```css
.status-progress.status-low .e-progress {
  background-color: #FFA06B;
}

.status-progress.status-medium .e-progress {
  background-color: #FFD06B;
}

.status-progress.status-high .e-progress {
  background-color: #6BCB77;
}
```

### Example 3: Responsive Dashboard

```tsx
import { useState } from 'react';
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

function ResponsiveDashboard() {
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);

  return (
    <div className={`dashboard ${isMobile ? 'mobile' : 'desktop'}`}>
      {/* Full width on mobile, grid on desktop */}
      <div className="metric">
        <h4>CPU Usage</h4>
        <ProgressBarComponent
          type={isMobile ? "Semicircle" : "Circular"}
          value={45}
          height={isMobile ? "80px" : "120px"}
        />
      </div>

      <div className="metric">
        <h4>Memory Usage</h4>
        <ProgressBarComponent
          type={isMobile ? "Semicircle" : "Circular"}
          value={72}
          height={isMobile ? "80px" : "120px"}
        />
      </div>

      <div className="metric full-width">
        <h4>Overall Progress</h4>
        <ProgressBarComponent
          type="Linear"
          value={65}
          height={isMobile ? "30" : "40"}
          showProgressValue={true}
        />
      </div>
    </div>
  );
}

export default ResponsiveDashboard;
```

---

## Next Steps

- **Animations & Events:** Advanced features - [animations-events-accessibility.md](animations-events-accessibility.md)
- **Types:** Different shapes - [types-and-shapes.md](types-and-shapes.md)
- **States:** Determinate vs Indeterminate - [states-and-modes.md](states-and-modes.md)
