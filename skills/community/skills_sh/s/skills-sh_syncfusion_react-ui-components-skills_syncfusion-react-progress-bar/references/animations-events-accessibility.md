# Animations, Events, and Accessibility

## Table of contents

- [Animations](#animations)
  - [Animation Configuration](#animation-configuration)
  - [Common Animation Patterns](#common-animation-patterns)
  - [Indeterminate Animation](#indeterminate-animation)
  - [Real-World Animation Example](#real-world-animation-example)
- [Event Handling](#event-handling)
  - [Available Events](#available-events)
  - [Event Usage Examples](#event-usage-examples)
  - [Multi-Step Process with Events](#multi-step-process-with-events)
- [Accessibility](#accessibility)
  - [WCAG 2.1 Compliance](#wcag-21-compliance)
  - [Adding ARIA Labels](#adding-aria-labels)
  - [Accessible Progress Pattern](#accessible-progress-pattern)
  - [Screen Reader Announcements](#screen-reader-announcements)
  - [CSS for Screen Readers](#css-for-screen-readers)
- [Tooltips and Annotations](#tooltips-and-annotations)
  - [Tooltip Support (Built-in Syncfusion Tooltips)](#tooltip-support-built-in-syncfusion-tooltips)
  - [Tooltip with Custom Styling](#tooltip-with-custom-styling)
  - [Annotations with Tooltips](#annotations-with-tooltips)
  - [Custom Tooltip Implementation (External Library)](#custom-tooltip-implementation-external-library)
- [Advanced Scenarios](#advanced-scenarios)
  - [Scenario 1: File Upload with Progress Tracking](#scenario-1-file-upload-with-progress-tracking)
  - [Scenario 2: Real-time Data Processing](#scenario-2-real-time-data-processing)
  - [Scenario 3: Multi-Type Progress Dashboard](#scenario-3-multi-type-progress-dashboard)
- [Next Steps](#next-steps)

## Animations

Control smooth transitions and visual effects for your progress bar.

### Animation Configuration

```tsx
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

<ProgressBarComponent
  type="Linear"
  value={80}
  animation={{
    enable: true,
    duration: 2000,    // milliseconds
    delay: 0           // milliseconds before animation starts
  }}
/>
```

### Common Animation Patterns

**Instant (no animation):**
```tsx
<ProgressBarComponent
  type="Linear"
  value={50}
  animation={{
    enable: false
  }}
/>
```

**Quick animation (500ms):**
```tsx
<ProgressBarComponent
  type="Linear"
  value={50}
  animation={{
    enable: true,
    duration: 500,
    delay: 0
  }}
/>
```

**Smooth animation (2000ms):**
```tsx
<ProgressBarComponent
  type="Linear"
  value={50}
  animation={{
    enable: true,
    duration: 2000,
    delay: 0
  }}
/>
```

**Delayed animation:**
```tsx
<ProgressBarComponent
  type="Linear"
  value={50}
  animation={{
    enable: true,
    duration: 1500,
    delay: 500       // Wait 500ms before animating
  }}
/>
```

### Indeterminate Animation

Indeterminate state has continuous animation:

```tsx
// Adjust animation speed for indeterminate spinners
<ProgressBarComponent
  type="Circular"
  isIndeterminate={true}
  animation={{
    enable: true,
    duration: 2000   // Duration of spin cycle
  }}
/>
```

### Real-World Animation Example

```tsx
import { useState } from 'react';
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

function AnimatedProgress() {
  const [progress, setProgress] = useState(0);
  const [isRunning, setIsRunning] = useState(false);

  const startAnimation = () => {
    if (isRunning) return;
    
    setIsRunning(true);
    setProgress(0);

    let current = 0;
    const interval = setInterval(() => {
      current += Math.random() * 25;
      if (current >= 100) {
        setProgress(100);
        clearInterval(interval);
        setTimeout(() => {
          setProgress(0);
          setIsRunning(false);
        }, 1000);
      } else {
        setProgress(current);
      }
    }, 600);
  };

  return (
    <div>
      <ProgressBarComponent
        type="Linear"
        value={progress}
        height="40"
        showProgressValue={true}
        animation={{
          enable: true,
          duration: 600,
          delay: 0
        }}
      />
      <button onClick={startAnimation} disabled={isRunning}>
        {isRunning ? 'Running...' : 'Start Animation'}
      </button>
    </div>
  );
}

export default AnimatedProgress;
```

---

## Event Handling

Track progress bar events for custom logic.

### Available Events

```tsx
<ProgressBarComponent
  type="Linear"
  value={50}
  progressStart={() => console.log('Animation started')}
  progressComplete={() => console.log('Animation completed')}
/>
```

### Event Usage Examples

**Complete Handler:**
```tsx
function ProgressComplete() {
  const handleComplete = () => {
    alert('Task completed!');
    // Trigger next action
    // Update UI
    // Send notification
  };

  return (
    <ProgressBarComponent
      type="Linear"
      value={100}
      progressComplete={handleComplete}
    />
  );
}

export default ProgressComplete;
```

**Start Handler:**
```tsx
function ProgressStart() {
  const handleStart = () => {
    console.log('Progress animation started');
    // Log event
    // Track analytics
    // Start timer
  };

  return (
    <ProgressBarComponent
      type="Linear"
      value={50}
      progressStart={handleStart}
    />
  );
}

export default ProgressStart;
```

### Multi-Step Process with Events

```tsx
import { useState } from 'react';
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

function MultiStepWithEvents() {
  const [step, setStep] = useState(0);
  const [completed, setCompleted] = useState(false);

  const steps = ['Validation', 'Processing', 'Upload', 'Confirm'];
  const progress = ((step + 1) / steps.length) * 100;

  const handleComplete = () => {
    if (step < steps.length - 1) {
      setStep(step + 1);
    } else {
      setCompleted(true);
    }
  };

  return (
    <div>
      <h3>Current: {steps[step]}</h3>
      <ProgressBarComponent
        type="Linear"
        value={progress}
        progressComplete={handleComplete}
        showProgressValue={true}
      />
      {completed && <p>✓ All steps completed!</p>}
    </div>
  );
}

export default MultiStepWithEvents;
```

---

## Accessibility

Ensure your progress bars are accessible to all users.

### WCAG 2.1 Compliance

The Syncfusion Progress Bar includes built-in accessibility features:
- Semantic HTML structure
- ARIA labels and roles
- Keyboard navigation support
- Screen reader support

### Adding ARIA Labels

```tsx
<ProgressBarComponent
  id="accessible-progress"
  type="Linear"
  value={65}
  role="progressbar"
  aria-valuenow={65}
  aria-valuemin={0}
  aria-valuemax={100}
  aria-label="File upload progress"
  aria-describedby="progress-description"
/>

<p id="progress-description">Uploading: 65% complete (1.3 MB of 2 MB)</p>
```

### Accessible Progress Pattern

```tsx
import { useState } from 'react';
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

function AccessibleFileUpload() {
  const [progress, setProgress] = useState(0);
  const [fileName, setFileName] = useState('');
  const totalSize = 2000000; // 2MB
  const uploadedSize = (progress / 100) * totalSize;

  const handleUpload = (file) => {
    setFileName(file.name);
    // Simulate upload
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          return 100;
        }
        return prev + 10;
      });
    }, 500);
  };

  return (
    <div>
      <label htmlFor="upload-progress">
        Uploading: {fileName}
      </label>

      <ProgressBarComponent
        id="upload-progress"
        type="Linear"
        value={progress}
        height="30"
        showProgressValue={true}
        role="progressbar"
        aria-label={`Uploading ${fileName}: ${progress}% complete`}
        aria-describedby="upload-details"
      />

      <div id="upload-details">
        {Math.round(uploadedSize / 1000)} KB of{' '}
        {Math.round(totalSize / 1000)} KB uploaded
      </div>
    </div>
  );
}

export default AccessibleFileUpload;
```

### Screen Reader Announcements

```tsx
import { useState } from 'react';
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

function ScreenReaderProgress() {
  const [progress, setProgress] = useState(0);
  const [announcement, setAnnouncement] = useState('');

  const updateProgress = (newProgress) => {
    setProgress(newProgress);

    // Announce milestone achievements
    if (newProgress === 25) {
      setAnnouncement('25% complete');
    } else if (newProgress === 50) {
      setAnnouncement('50% complete');
    } else if (newProgress === 75) {
      setAnnouncement('75% complete');
    } else if (newProgress === 100) {
      setAnnouncement('Processing complete');
    }
  };

  return (
    <div>
      {/* Live region for announcements */}
      <div
        role="status"
        aria-live="polite"
        aria-atomic="true"
        className="sr-only"
      >
        {announcement}
      </div>

      <ProgressBarComponent
        type="Linear"
        value={progress}
        aria-label="Processing progress"
      />

      <button onClick={() => updateProgress(progress + 25)}>
        Advance Progress
      </button>
    </div>
  );
}

export default ScreenReaderProgress;
```

### CSS for Screen Readers

```css
/* Hide visually but keep for screen readers */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```

---

## Tooltips and Annotations

Add additional information to your progress bars using built-in Syncfusion tooltip and annotation features.

### Tooltip Support (Built-in Syncfusion Tooltips)

Use the `tooltip` property with `TooltipSettingsModel` to enable built-in tooltips:

```tsx
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

function TooltipProgress() {
  return (
    <ProgressBarComponent
      id="progress-with-tooltip"
      type="Linear"
      value={65}
      height="30"
      showProgressValue={true}
      tooltip={{
        enable: true,
        showTooltipOnHover: true,
        format: 'Progress: ${value}%'
      }}
    />
  );
}

export default TooltipProgress;
```

**Tooltip Properties:**
- `enable: true` - Activates tooltip functionality
- `showTooltipOnHover: true` - Displays tooltip when user hovers over the progress bar
- `format: string` - Formats tooltip content using `${value}` placeholder to display the progress value

### Tooltip with Custom Styling

```tsx
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

function StyledTooltip() {
  return (
    <ProgressBarComponent
      type="Linear"
      value={45}
      height="30"
      tooltip={{
        enable: true,
        showTooltipOnHover: true,
        format: '${value}% Complete',
        fill: '#3366FF',
        textStyle: {
          color: '#FFFFFF',
          size: '12px',
          bold: true
        }
      }}
    />
  );
}

export default StyledTooltip;
```

### Annotations with Tooltips

Add annotations to the center of circular progress bars to mark milestones:

```tsx
import { 
  ProgressBarComponent, 
  ProgressBarAnnotationsDirective, 
  ProgressBarAnnotationDirective,
  Inject,
  ProgressAnnotation 
} from '@syncfusion/ej2-react-progressbar';

function AnnotatedProgress() {
  const content = '<div style="font-size:18px;font-weight:bold;color:#ffffff;"><span>60%</span></div>';

  return (
    <ProgressBarComponent
      id="circular-annotation"
      type="Circular"
      value={60}
      height="160px"
      innerRadius="190%"
      trackThickness={80}
      cornerRadius="Round"
      trackColor="#FFD939"
      showProgressValue={true}
      tooltip={{
        enable: true,
        showTooltipOnHover: true,
        format: 'Current: ${value}%'
      }}
    >
      <Inject services={[ProgressAnnotation]} />
      <ProgressBarAnnotationsDirective>
        <ProgressBarAnnotationDirective content={content} />
      </ProgressBarAnnotationsDirective>
    </ProgressBarComponent>
  );
}

export default AnnotatedProgress;
```

### Custom Tooltip Implementation (External Library)

If you need advanced tooltip features, use external libraries like react-tooltip:

```tsx
import { useState } from 'react';
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

function CustomTooltip() {
  const [showTooltip, setShowTooltip] = useState(false);
  const [tooltipText, setTooltipText] = useState('');
  const [progress, setProgress] = useState(50);

  const handleMouseEnter = () => {
    setShowTooltip(true);
    setTooltipText(`Progress: ${progress}%`);
  };

  const handleMouseLeave = () => {
    setShowTooltip(false);
  };

  return (
    <div
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      style={{ position: 'relative' }}
    >
      <ProgressBarComponent
        type="Linear"
        value={progress}
        height="30"
        showProgressValue={true}
      />

      {showTooltip && (
        <div
          style={{
            position: 'absolute',
            top: '-35px',
            left: '50%',
            transform: 'translateX(-50%)',
            background: '#333',
            color: '#fff',
            padding: '8px 12px',
            borderRadius: '4px',
            fontSize: '12px',
            whiteSpace: 'nowrap',
            zIndex: 1000
          }}
        >
          {tooltipText}
        </div>
      )}
    </div>
  );
}

export default CustomTooltip;
```

---

## Advanced Scenarios

### Scenario 1: File Upload with Progress Tracking

```tsx
import { useState } from 'react';
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

function FileUploadWithTracking() {
  const [uploadState, setUploadState] = useState({
    isLoading: true,
    progress: 0,
    fileName: 'document.pdf',
    uploadedSize: 0,
    totalSize: 2000000
  });

  const handleUpload = async (file) => {
    setUploadState({
      isLoading: true,
      progress: 0,
      fileName: file.name,
      uploadedSize: 0,
      totalSize: file.size
    });

    // Simulate chunked upload
    const chunkSize = 100000;
    let uploaded = 0;

    while (uploaded < file.size) {
      const chunk = Math.min(chunkSize, file.size - uploaded);
      uploaded += chunk;

      const progress = (uploaded / file.size) * 100;
      setUploadState(prev => ({
        ...prev,
        progress,
        uploadedSize: uploaded
      }));

      // Simulate network delay
      await new Promise(resolve => setTimeout(resolve, 200));
    }

    setUploadState(prev => ({
      ...prev,
      isLoading: false,
      progress: 100
    }));
  };

  const { progress, fileName, uploadedSize, totalSize } = uploadState;

  return (
    <div>
      <h3>Upload: {fileName}</h3>

      <ProgressBarComponent
        type="Linear"
        value={progress}
        isIndeterminate={uploadState.isLoading}
        height="30"
        showProgressValue={true}
      />

      <p>
        {Math.round(uploadedSize / 1000)} KB /{' '}
        {Math.round(totalSize / 1000)} KB
      </p>
    </div>
  );
}

export default FileUploadWithTracking;
```

### Scenario 2: Real-time Data Processing

```tsx
import { useState, useEffect } from 'react';
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

function DataProcessing() {
  const [state, setState] = useState({
    processed: 0,
    total: 1000,
    currentItem: null,
    startTime: Date.now()
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setState(prev => {
        if (prev.processed >= prev.total) {
          clearInterval(interval);
          return prev;
        }

        const batchSize = Math.floor(Math.random() * 50) + 25;
        const processed = Math.min(prev.processed + batchSize, prev.total);

        return {
          ...prev,
          processed,
          currentItem: `Processing item ${processed} of ${prev.total}`
        };
      });
    }, 300);

    return () => clearInterval(interval);
  }, []);

  const { processed, total, currentItem, startTime } = state;
  const progress = (processed / total) * 100;
  const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);

  return (
    <div>
      <h3>Data Processing</h3>
      <p>{currentItem}</p>

      <ProgressBarComponent
        type="Linear"
        value={progress}
        height="30"
        showProgressValue={true}
        progressValueFormat="N0 '%'"
      />

      <p>
        Processed: {processed} / {total} (Elapsed: {elapsed}s)
      </p>
    </div>
  );
}

export default DataProcessing;
```

### Scenario 3: Multi-Type Progress Dashboard

```tsx
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

function ProgressDashboard() {
  const metrics = [
    { label: 'CPU', value: 45, type: 'Circular' },
    { label: 'Memory', value: 72, type: 'Circular' },
    { label: 'Disk', value: 38, type: 'Circular' },
    { label: 'Overall', value: 52, type: 'Linear' }
  ];

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
      gap: '20px'
    }}>
      {metrics.map((metric) => (
        <div key={metric.label} style={{ textAlign: 'center' }}>
          <h4>{metric.label}</h4>
          <ProgressBarComponent
            type={metric.type}
            value={metric.value}
            height={metric.type === 'Circular' ? '100px' : '30'}
            showProgressValue={true}
          />
          <p>{metric.value}%</p>
        </div>
      ))}
    </div>
  );
}

export default ProgressDashboard;
```

---

## Next Steps

- **Customization:** Colors and styling - [customization-and-styling.md](customization-and-styling.md)
- **States:** Determinate vs Indeterminate - [states-and-modes.md](states-and-modes.md)
- **Types:** Different shapes - [types-and-shapes.md](types-and-shapes.md)
