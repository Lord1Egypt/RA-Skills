---
name: syncfusion-react-progress-bar
description: Implement Syncfusion React Progress Bar for visual feedback. Use this skill whenever users need to display progress indicators, loading states, file uploads, data processing, or task completion in React applications. Trigger when user mentions progress bars, loading spinners, progress indicators, determinate/indeterminate states, circular/linear progress, or any progress visualization scenario.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Notifications"
---

# Implementing React Progress Bar Component

A comprehensive skill for implementing the Syncfusion React Progress Bar component for visual progress feedback, loading states, and task completion indicators.

## When to Use This Skill

Use this skill when you need to:
- Display progress of file uploads or downloads
- Show task completion percentage
- Indicate loading states (determinate or indeterminate)
- Visualize data processing or long-running operations
- Create progress spinners or circular indicators
- Handle secondary progress (buffer scenarios)
- Customize progress bar appearance and colors
- Implement animations and transitions
- Handle progress events and callbacks
- Ensure accessibility compliance for progress indicators

## Component Overview

The Syncfusion React Progress Bar is a lightweight component that visualizes task progress in linear, circular, or semi-circular shapes. It supports multiple states (determinate, indeterminate, buffer) and features animations, customization, and full accessibility support.

**Key Features:**
- **Multiple Types:** Linear, Circular, Semi-Circular shapes
- **States:** Determinate (known progress), Indeterminate (unknown), Buffer (secondary progress)
- **Animations:** Smooth transitions with configurable duration and delay
- **Customization:** Colors, heights, labels, themes
- **Events:** Progress tracking, start/complete callbacks
- **Accessibility:** WCAG 2.1 compliant with ARIA support
- **RTL Support:** Right-to-left language support

## Documentation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Basic progress bar implementation
- CSS imports and themes
- First component example
- TypeScript vs JavaScript

### Types and Shapes
📄 **Read:** [references/types-and-shapes.md](references/types-and-shapes.md)
- Linear progress bar
- Circular progress bar
- Semi-circular progress bar
- Shape variations and code examples
- Choosing the right type for your use case

### States and Modes
📄 **Read:** [references/states-and-modes.md](references/states-and-modes.md)
- Determinate state (known progress, default)
- Indeterminate state (unknown progress, spinners)
- Buffer/Secondary progress (dual progress indicators)
- Combining multiple states
- Real-world scenarios for each state

### Customization and Styling
📄 **Read:** [references/customization-and-styling.md](references/customization-and-styling.md)
- Sizing (height, width configurations)
- Colors and fill customization
- Labels and text display
- Theme application
- CSS customization
- Responsive design patterns

### Animations, Events, and Accessibility
📄 **Read:** [references/animations-events-accessibility.md](references/animations-events-accessibility.md)
- Animation configuration and control
- Event handlers for progress tracking
- Using callbacks for task completion
- WCAG compliance
- ARIA attributes and labels
- Tooltip and annotation support
- Troubleshooting common issues

### API Reference
📄 **Read:** [references/api.md](references/api.md)
- Full list of public properties, methods and events for `ProgressBarComponent` (see file).

## Quick Start Example

```tsx
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

function App() {
  return (
    <div>
      {/* Linear Determinate Progress Bar */}
      <ProgressBarComponent
        id="linear"
        type="Linear"
        height="60"
        value={75}
        animation={{
          enable: true,
          duration: 2000,
          delay: 0
        }}
      />

      {/* Circular Progress Bar */}
      <ProgressBarComponent
        id="circular"
        type="Circular"
        height="160px"
        value={60}
      />

      {/* Indeterminate Loading Spinner */}
      <ProgressBarComponent
        id="indeterminate"
        type="Linear"
        height="60"
        isIndeterminate={true}
        animation={{
          enable: true,
          duration: 2000,
          delay: 0
        }}
      />
    </div>
  );
}

export default App;
```

## Common Patterns

### 1. File Upload Progress
```tsx
<ProgressBarComponent
  id="upload"
  type="Linear"
  value={uploadPercentage}
  showProgressValue={true}
  progressValueFormat="N0 '%'"
/>
```

### 2. Loading Spinner
```tsx
<ProgressBarComponent
  id="spinner"
  type="Circular"
  isIndeterminate={true}
  height="100px"
/>
```

### 3. Buffer Progress (Buffered Loading)
```tsx
<ProgressBarComponent
  id="buffer"
  type="Linear"
  value={40}
  secondaryProgress={80}
  height="60"
/>
```

### 4. Determinate Task Progress
```tsx
<ProgressBarComponent
  id="task"
  type="Linear"
  value={taskCompletionPercentage}
  showProgressValue={true}
  animation={{
    enable: true,
    duration: 1500
  }}
/>
```

## Key Props Reference

### Core Properties

| Prop | Type | Default | Purpose |
|------|------|---------|---------|
| `id` | string | - | Unique identifier for component |
| `type` | "Linear" \| "Circular" \| "Semicircle" | "Linear" | Shape of progress bar |
| `value` | number | 0 | Current progress value (0-100) |
| `secondaryProgress` | number | 0 | Secondary/buffer progress value |
| `isIndeterminate` | boolean | false | Indeterminate/loading mode |
| `height` | string | "100%" | Height of progress bar (CSS value) |
| `width` | string | "100%" | Width of progress bar (CSS value) |
| `showProgressValue` | boolean | false | Display percentage text |

### Animation & Styling

| Prop | Type | Default | Purpose |
|------|------|---------|---------|
| `animation` | AnimationModel | - | Animation config: `{ enable, duration, delay }` |
| `progressColor` | string | - | Color for progress fill (CSS color) |
| `trackColor` | string | - | Color for track background |
| `progressThickness` | number | 4 | Progress bar thickness (pixels) |
| `trackThickness` | number | 4 | Track thickness (pixels) |
| `isStriped` | boolean | false | Striped pattern appearance |
| `isGradient` | boolean | false | Gradient fill effect |
| `cssClass` | string | - | Custom CSS class for styling |

### Advanced Features

| Prop | Type | Default | Purpose |
|------|------|---------|---------|
| `cornerRadius` | "Round" \| "Auto" | "Auto" | Corner style for ends |
| `enableRtl` | boolean | false | Right-to-left layout |
| `enablePieProgress` | boolean | false | Pie view for circular type |
| `enableProgressSegments` | boolean | false | Segmented progress rendering |
| `segmentCount` | number | 1 | Number of segments |
| `rangeColors` | RangeColorModel[] | - | Colors for different ranges |
| `minimum` | number | 0 | Minimum progress value |
| `maximum` | number | 100 | Maximum progress value |

### Label & Format

| Prop | Type | Default | Purpose |
|------|------|---------|---------|
| `progressValueFormat` | string | "N0 '%'" | Format for value display (e.g., "N2 '%'") |
| `labelOnTrack` | boolean | true | Show label on the track |
| `labelStyle` | FontModel | - | Font styling for label |

**When to use each:**
- **type**: Choose based on space: Linear (full-width), Circular/Semicircle (compact)
- **value**: Update via state to reflect real progress
- **isIndeterminate**: Use for unknown duration tasks (loading, processing)
- **secondaryProgress**: Show buffer/estimated vs. actual progress
- **animation**: Enhance UX with smooth transitions (disable for real-time high-frequency updates)
- **cornerRadius**: "Round" for modern look, "Auto" for default
- **segmentCount**: Split progress into visual segments (e.g., 10 segments = 10% per segment)

## Common Use Cases with Code Examples

### Use Case 1: File Upload/Download

```tsx
const [uploadProgress, setUploadProgress] = useState(0);

<ProgressBarComponent
  type="Linear"
  value={uploadProgress}
  showProgressValue={true}
  progressValueFormat="N0 '%'"
  height="30"
  animation={{ enable: true, duration: 500 }}
/>
```

**Best Practices:**
- Use Linear type for wide displays
- Update value from upload progress events
- Show estimated time in addition to percentage
- Optional `secondaryProgress` for pre-fetched bytes

### Use Case 2: Loading State (Unknown Duration)

```tsx
<ProgressBarComponent
  type="Circular"
  isIndeterminate={true}
  height="100px"
  animation={{ enable: true, duration: 2000 }}
/>
```

**Best Practices:**
- Use Circular for compact display
- Keep `isIndeterminate={true}` until operation completes
- Spinner continues animating indefinitely
- Replace with determinate once progress can be tracked

### Use Case 3: Data Processing

```tsx
const [processProgress, setProcessProgress] = useState(0);
const totalItems = 100;

useEffect(() => {
  processItems().then(processed => {
    setProcessProgress((processed / totalItems) * 100);
  });
}, []);

<ProgressBarComponent
  type="Linear"
  value={processProgress}
  showProgressValue={true}
  height="30"
/>
```

**Best Practices:**
- Update value as items are processed
- Show item count: "25 of 100 items"
- Show elapsed time and estimated remaining
- Display success/error message on completion

### Use Case 4: Multiple Tasks (Buffering/Streaming)

```tsx
const [processedItems, setProcessedItems] = useState(30);
const [queuedItems, setQueuedItems] = useState(75);
const totalItems = 100;

<ProgressBarComponent
  type="Linear"
  value={(processedItems / totalItems) * 100}
  secondaryProgress={(queuedItems / totalItems) * 100}
  height="30"
/>
```

**Best Practices:**
- Primary progress (value) = actual processed
- Secondary progress = queued/buffered items
- Great for streaming/video buffering scenarios
- Also works for task queue management

### Use Case 5: Multi-Step Workflow

```tsx
const steps = ['Validation', 'Processing', 'Upload', 'Confirmation'];
const [currentStep, setCurrentStep] = useState(0);
const progress = ((currentStep + 1) / steps.length) * 100;

<ProgressBarComponent
  type="Linear"
  value={progress}
  showProgressValue={true}
  height="30"
/>

<div>
  {steps.map((step, i) => (
    <div key={i}>
      {step} {i === currentStep ? '🔄' : i < currentStep ? '✓' : '⏳'}
    </div>
  ))}
</div>
```

**Best Practices:**
- Calculate progress as (currentStep / totalSteps) * 100
- Show step indicators alongside progress bar
- Highlight current step
- Disable user interactions during processing

## Advanced Usage Patterns

### 1. Value Binding with State Management

```tsx
import { useState, useEffect } from 'react';
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

function ProgressManager() {
  const [progress, setProgress] = useState(0);
  const [isProcessing, setIsProcessing] = useState(false);

  useEffect(() => {
    if (!isProcessing) return;

    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          setIsProcessing(false);
          return 100;
        }
        return prev + Math.random() * 15;
      });
    }, 500);

    return () => clearInterval(interval);
  }, [isProcessing]);

  return (
    <div>
      <ProgressBarComponent 
        type="Linear"
        value={progress}
        showProgressValue={true}
      />
      <button 
        onClick={() => { setProgress(0); setIsProcessing(true); }}
        disabled={isProcessing}
      >
        {isProcessing ? 'Processing...' : 'Start'}
      </button>
    </div>
  );
}

export default ProgressManager;
```

### 2. Animation Configuration Patterns

```tsx
// Real-time updates (no animation for smoothness)
animation={{ enable: false }}

// User interactions (quick feedback)
animation={{ enable: true, duration: 300, delay: 0 }}

// Page loads (smooth transition)
animation={{ enable: true, duration: 1500, delay: 0 }}

// Cascading effects (staggered)
animation={{ enable: true, duration: 1000, delay: 200 }}

// Loading spinners (continuous)
animation={{ enable: true, duration: 2000 }}
```

### 3. Conditional Rendering Based on State

```tsx
function ConditionalProgress() {
  const [state, setState] = useState('idle'); // idle | loading | success | error
  const [value, setValue] = useState(0);

  const getProgressType = () => {
    if (state === 'loading') return 'Circular';
    return 'Linear';
  };

  return (
    <>
      {state === 'loading' && (
        <ProgressBarComponent
          type={getProgressType()}
          isIndeterminate={state === 'loading'}
          height="100px"
        />
      )}

      {state === 'success' && (
        <div style={{ color: 'green' }}>✓ Complete</div>
      )}

      {state === 'error' && (
        <div style={{ color: 'red' }}>✗ Error occurred</div>
      )}
    </>
  );
}

export default ConditionalProgress;
```

### 4. Event Handling for Tracking

```tsx
function ProgressWithEvents() {
  const handleStart = () => {
    console.log('Progress started');
    analytics.track('progress_started');
  };

  const handleComplete = () => {
    console.log('Progress completed');
    analytics.track('progress_completed');
    showNotification('Task completed!');
  };

  const handleValueChange = (args) => {
    console.log(`Progress: ${args.value}%`);
    // Milestone tracking
    if (args.value === 50) {
      analytics.track('progress_midpoint');
    }
  };

  return (
    <ProgressBarComponent
      type="Linear"
      value={75}
      progressStart={handleStart}
      progressComplete={handleComplete}
      valueChanged={handleValueChange}
    />
  );
}

export default ProgressWithEvents;
```

### 5. Responsive Design

```tsx
function ResponsiveProgress() {
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);

  useEffect(() => {
    const handleResize = () => setIsMobile(window.innerWidth < 768);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <ProgressBarComponent
      type={isMobile ? 'Semicircle' : 'Linear'}
      value={65}
      height={isMobile ? '100px' : '40'}
      showProgressValue={true}
    />
  );
}

export default ResponsiveProgress;
```

### 6. Error Handling & Retry Logic

```tsx
async function uploadWithRetry(file, maxRetries = 3) {
  const [attempts, setAttempts] = useState(0);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState(null);

  for (let i = 0; i < maxRetries; i++) {
    try {
      setAttempts(i + 1);
      const result = await uploadFile(file, (p) => setProgress(p));
      return result;
    } catch (err) {
      if (i === maxRetries - 1) {
        setError(`Failed after ${maxRetries} attempts`);
        throw err;
      }
      // Retry with exponential backoff
      await new Promise(r => setTimeout(r, Math.pow(2, i) * 1000));
    }
  }
}
```

## Integration with Common Patterns

### With React Query
```tsx
import { useQuery } from '@tanstack/react-query';

function DataProcessing() {
  const { data, isLoading, progress } = useQuery({
    queryKey: ['processData'],
    queryFn: async ({ signal }) => {
      // Process with progress tracking
    }
  });

  return (
    <ProgressBarComponent
      isIndeterminate={isLoading}
      value={progress || 0}
    />
  );
}
```

### With Redux
```tsx
import { useSelector, useDispatch } from 'react-redux';

function ReduxProgress() {
  const { progress, isLoading } = useSelector(state => state.upload);
  const dispatch = useDispatch();

  return (
    <ProgressBarComponent
      value={progress}
      isIndeterminate={isLoading}
      progressComplete={() => dispatch(resetProgress())}
    />
  );
}
```
