# States and Modes for Progress Bar

## Table of contents

- [Determinate State](#determinate-state)
  - [Basic Determinate Example](#basic-determinate-example)
  - [When to Use Determinate](#when-to-use-determinate)
  - [Updating Determinate Progress](#updating-determinate-progress)
- [Indeterminate State](#indeterminate-state)
  - [Basic Indeterminate Example](#basic-indeterminate-example)
  - [When to Use Indeterminate](#when-to-use-indeterminate)
  - [Indeterminate with Circular Type](#indeterminate-with-circular-type)
  - [Transitioning from Indeterminate to Determinate](#transitioning-from-indeterminate-to-determinate)
- [Buffer/Secondary Progress](#buffersecondary-progress)
  - [Basic Buffer Example](#basic-buffer-example)
  - [When to Use Buffer](#when-to-use-buffer)
  - [Streaming Scenario Example](#streaming-scenario-example)
- [State Comparison](#state-comparison)
- [Real-World Scenarios](#real-world-scenarios)
  - [Scenario 1: File Upload (Determinate)](#scenario-1-file-upload-determinate)
  - [Scenario 2: API Loading (Indeterminate to Determinate)](#scenario-2-api-loading-indeterminate-to-determinate)
  - [Scenario 3: Multi-Step Process (Determinate with Steps)](#scenario-3-multi-step-process-determinate-with-steps)
- [Combining States](#combining-states)
  - [State Transition Best Practices](#state-transition-best-practices)
- [Next Steps](#next-steps)

## Determinate State

The **Determinate** state is used when you know the exact progress of a task. This is the default state when `isIndeterminate` is not set or is `false`.

### Basic Determinate Example

```tsx
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

function App() {
  return (
    <ProgressBarComponent
      id="determinate"
      type="Linear"
      value={65}
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

**What happens:**
- Progress bar shows 65% filled
- Stays at 65% until value prop changes
- Animation optional but recommended

### When to Use Determinate

- **Known progress:** Download at 45%, file processing at 78%
- **Step-based tasks:** 5 of 10 steps completed
- **Percentage calculations:** 23 MB of 100 MB uploaded
- **Timed operations:** Script running for 30 of 120 seconds
- **Batch operations:** 8 of 15 items processed

### Updating Determinate Progress

```tsx
import { useState, useEffect } from 'react';
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

function DownloadProgress() {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    // Simulate download progress
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          return 100;
        }
        return prev + Math.random() * 25;
      });
    }, 800);

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h3>Downloading File...</h3>
      <ProgressBarComponent
        id="download"
        type="Linear"
        value={progress}
        height="40"
        showProgressValue={true}
        progressValueFormat="N0 '%'"
        animation={{
          enable: true,
          duration: 500,
          delay: 0
        }}
      />
      <p>Downloaded: {Math.round(progress)}%</p>
    </div>
  );
}

export default DownloadProgress;
```

---

## Indeterminate State

The **Indeterminate** state is used when progress cannot be estimated. It shows continuous animation without a specific value, commonly seen as loading spinners.

### Basic Indeterminate Example

```tsx
<ProgressBarComponent
  id="indeterminate"
  type="Linear"
  isIndeterminate={true}
  height="60"
  animation={{
    enable: true,
    duration: 2000,
    delay: 0
  }}
/>
```

**What happens:**
- Animated bar continuously moves (doesn't fill to a value)
- No completion point visible
- Continues animating until disabled or hidden

### When to Use Indeterminate

- **Unknown duration:** Processing API calls, database queries
- **Loading states:** Page loading, content fetching
- **Background tasks:** Sync operations, auto-save
- **Waiting states:** Server response pending
- **Initial load:** Before progress can be tracked

### Indeterminate with Circular Type

```tsx
// Loading spinner (best practice)
<ProgressBarComponent
  id="spinner"
  type="Circular"
  isIndeterminate={true}
  height="100px"
  animation={{
    enable: true,
    duration: 2000,
    delay: 0
  }}
/>
```

### Transitioning from Indeterminate to Determinate

Switch to determinate once actual progress becomes known:

```tsx
import { useState } from 'react';
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

function SmartProgress() {
  const [isLoading, setIsLoading] = useState(true);
  const [progress, setProgress] = useState(0);

  const handleUpload = async () => {
    setIsLoading(true);
    setProgress(0);

    // Start with indeterminate (we don't know total size)
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Switch to determinate once we know size
    setIsLoading(false);
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
      <ProgressBarComponent
        id="smart"
        type="Linear"
        value={progress}
        isIndeterminate={isLoading}
        height="40"
        showProgressValue={!isLoading}
      />
      <button onClick={handleUpload}>Start Upload</button>
    </div>
  );
}

export default SmartProgress;
```

---

## Buffer/Secondary Progress

The **Buffer** (secondary progress) state shows dual progress: actual progress and estimated/buffered progress. Useful when actual progress lags behind total available data.

### Basic Buffer Example

```tsx
<ProgressBarComponent
  id="buffer"
  type="Linear"
  value={40}
  secondaryProgress={75}
  height="60"
  animation={{
    enable: true,
    duration: 2000
  }}
/>
```

**What happens:**
- Primary progress (red): 40% filled
- Secondary progress (light blue): 75% filled
- Visual shows buffer ahead of actual progress

### When to Use Buffer

- **Streaming media:** Actual playback vs. buffered video
- **Large file downloads:** Downloaded vs. pre-fetched chunks
- **Database pagination:** Current page vs. prefetched pages
- **Real-time data:** Processed vs. received data points
- **Queue processing:** Processed vs. queued items

### Streaming Scenario Example

```tsx
import { useState, useEffect } from 'react';
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

function VideoStreamProgress() {
  const [playbackTime, setPlaybackTime] = useState(0);
  const [bufferedTime, setBufferedTime] = useState(0);
  const totalDuration = 100; // seconds

  useEffect(() => {
    const interval = setInterval(() => {
      setPlaybackTime(prev => {
        const next = prev + 0.5;
        return next > totalDuration ? totalDuration : next;
      });

      // Buffer ahead of playback
      setBufferedTime(prev => {
        if (prev < playbackTime + 15) {
          return Math.min(prev + 1, totalDuration);
        }
        return prev;
      });
    }, 100);

    return () => clearInterval(interval);
  }, []);

  const playbackPercent = (playbackTime / totalDuration) * 100;
  const bufferedPercent = (bufferedTime / totalDuration) * 100;

  return (
    <div>
      <h3>Video Player</h3>
      <ProgressBarComponent
        id="video"
        type="Linear"
        value={playbackPercent}
        secondaryProgress={bufferedPercent}
        height="40"
        animation={{
          enable: true,
          duration: 100
        }}
      />
      <p>Playing: {playbackTime.toFixed(1)}s / Buffered: {bufferedTime.toFixed(1)}s</p>
    </div>
  );
}

export default VideoStreamProgress;
```

---

## State Comparison

| Feature | Determinate | Indeterminate | Buffer |
|---------|-------------|---------------|--------|
| **Progress Known** | ✓ Yes | ✗ No | ✓ Yes (dual) |
| **Value Updates** | ✓ Required | ✗ None | ✓ Both values |
| **Animation** | Optional | Continuous | Optional |
| **Use Case** | Known progress | Unknown duration | Dual progress |
| **Example** | Download 45% | Loading... | 40% actual, 75% buffered |

---

## Real-World Scenarios

### Scenario 1: File Upload (Determinate)

```tsx
  const [uploadProgress, setUploadProgress] = useState(0);

  const handleFileUpload = (file) => {
    const formData = new FormData();
    formData.append("file", file);

    const xhr = new XMLHttpRequest();

    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable) {
        const percent = Math.round((event.loaded / event.total) * 100);
        setUploadProgress(percent);
      }
    };

    xhr.onload = () => {
      setUploadProgress(100);
    };

    xhr.open("POST", "/upload");
    xhr.send(formData);
  };

  return (
    <div style={{ width: "400px" }}>
      <input
        type="file"
        onChange={(e) => handleFileUpload(e.target.files[0])}
      />

      <ProgressBarComponent
        type="Linear"
        value={uploadProgress}
        showProgressValue={true}
        height="30"
     
      />
    </div>
  );
```

### Scenario 2: API Loading (Indeterminate → Determinate)

```tsx
const [data, setData] = useState(null);
const [isLoading, setIsLoading] = useState(false);
const [progress, setProgress] = useState(0);

const fetchData = async () => {
  setIsLoading(true);
  setProgress(0);

  try {
    // Indeterminate while fetching
    const response = await fetch('/api/data');
    
    // Switch to determinate while processing
    setIsLoading(false);
    const items = await response.json();
    
    for (let i = 0; i < items.length; i++) {
      // Process items with progress
      setProgress((i / items.length) * 100);
      // ... process item
    }
    
    setData(items);
    setProgress(100);
  } catch (error) {
    console.error('Error:', error);
  }
};

return (
  <>
    <ProgressBarComponent
      type="Circular"
      isIndeterminate={isLoading}
      value={progress}
      height="100px"
    />
    <button onClick={fetchData}>Fetch Data</button>
  </>
);
```

### Scenario 3: Multi-Step Process (Determinate with Steps)

```tsx
import { useState } from 'react';
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

function MultiStepProcess() {
  const steps = [
    { name: 'Validation', duration: 2000 },
    { name: 'Processing', duration: 3000 },
    { name: 'Upload', duration: 2000 },
    { name: 'Confirmation', duration: 1000 }
  ];

  const [currentStep, setCurrentStep] = useState(0);
  const [isProcessing, setIsProcessing] = useState(false);

  const startProcess = async () => {
    setIsProcessing(true);
    setCurrentStep(0);

    for (let i = 0; i < steps.length; i++) {
      setCurrentStep(i);
      await new Promise(resolve => 
        setTimeout(resolve, steps[i].duration)
      );
    }

    setIsProcessing(false);
  };

  const progress = ((currentStep + 1) / steps.length) * 100;

  return (
    <div>
      <div>
        <h3>Processing Steps</h3>
        {steps.map((step, i) => (
          <div key={i}>
            <span>{step.name}</span>
            <span>{i === currentStep ? '🔄' : i < currentStep ? '✓' : '⏳'}</span>
          </div>
        ))}
      </div>

      <ProgressBarComponent
        type="Linear"
        value={progress}
        height="30"
        showProgressValue={true}
      />

      <button onClick={startProcess} disabled={isProcessing}>
        {isProcessing ? 'Processing...' : 'Start Process'}
      </button>
    </div>
  );
}

export default MultiStepProcess;
```

---

## Combining States

You can transition between states based on your application flow:

```tsx
import { useState } from 'react';
import { ProgressBarComponent } from '@syncfusion/ej2-react-progressbar';

function ProgressStateTransition() {
  const [progress, setProgress] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [phase, setPhase] = useState('idle');

  const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

  const handleUpload = async () => {
    try {
      // Phase 1: Connecting (indeterminate)
      setIsLoading(true);
      setPhase('connecting');
      setProgress(0);
      await delay(2000);

      // Phase 2: Uploading (determinate)
      setPhase('uploading');
      setIsLoading(false);
      for (let i = 0; i <= 100; i += 10) {
        setProgress(i);
        await delay(500);
      }

      // Phase 3: Complete
      setProgress(100);
      setPhase('complete');
      
      setTimeout(() => {
        setProgress(0);
        setPhase('idle');
      }, 2000);
    } catch (error) {
      setPhase('error');
      setIsLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '600px' }}>
      <h3>Multi-Phase Progress</h3>
      
      <ProgressBarComponent
        type="Linear"
        value={progress}
        isIndeterminate={isLoading}
        height="40"
        showProgressValue={!isLoading}
        progressValueFormat="N0 '%'"
        animation={{ enable: true, duration: 300 }}
      />

      <p>Phase: <strong>{phase.toUpperCase()}</strong></p>
      {phase === 'error' && <p style={{ color: 'red' }}>Upload failed. Please try again.</p>}

      <button 
        onClick={handleUpload}
        disabled={isLoading || phase === 'complete'}
      >
        {isLoading ? 'Uploading...' : phase === 'complete' ? 'Upload Complete' : 'Start Upload'}
      </button>
    </div>
  );
}

export default ProgressStateTransition;
```

### State Transition Best Practices

1. **Error Handling:** Always include error states to handle failed operations
2. **User Feedback:** Display current phase to keep users informed
3. **Disable Interactions:** Prevent duplicate submissions during loading
4. **Reset State:** Clear progress after operations complete
5. **Timeout Protection:** Add timeouts to prevent indefinite loading states

---

## Next Steps

- **Customization:** Style and colors - [customization-and-styling.md](customization-and-styling.md)
- **Animations & Events:** Advanced features - [animations-events-accessibility.md](animations-events-accessibility.md)
- **Types:** Different shapes - [types-and-shapes.md](types-and-shapes.md)
