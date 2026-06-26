# Animation Effects

## Table of Contents
- [Animation Settings](#animation-settings)
- [Available Effects](#available-effects)
- [Effect Examples](#effect-examples)
- [Duration and Delay](#duration-and-delay)
- [Enable/Disable Animation](#enabledisable-animation)
- [Performance Considerations](#performance-considerations)

## Animation Settings

Control dialog open/close animations with the `animationSettings` property:

```jsx
import React, { useRef } from 'react';
import { DialogComponent } from '@syncfusion/ej2-react-popups';
import './App.css';

export default function App() {
  const dialogRef = useRef(null);

  const animationSettings = {
    effect: 'Zoom',      // Animation type
    duration: 400,       // Milliseconds
    delay: 0             // Initial delay in milliseconds
  };

  return (
    <div id="dialog-target" style={{ position: 'relative' }}>
      <button onClick={() => dialogRef.current?.show()}>Open</button>

      <DialogComponent
        ref={dialogRef}
        header="Animated Dialog"
        animationSettings={animationSettings}
        target="#dialog-target"
      >
        Smooth animation on open/close
      </DialogComponent>
    </div>
  );
}
```

## Available Effects

The Dialog supports 15+ animation effects:

| Effect | Open | Close | Description |
|--------|------|-------|-------------|
| `'Fade'` | FadeIn | FadeOut | Opacity transition |
| `'FadeZoom'` | FadeIn + ZoomIn | FadeOut + ZoomOut | Fade + scale combined |
| `'FlipLeftDown'` | Flip left-down | Reverse | 3D flip effect |
| `'FlipLeftUp'` | Flip left-up | Reverse | 3D flip effect |
| `'FlipRightDown'` | Flip right-down | Reverse | 3D flip effect |
| `'FlipRightUp'` | Flip right-up | Reverse | 3D flip effect |
| `'FlipXDown'` | Flip X-down | Reverse | Horizontal flip |
| `'FlipXUp'` | Flip X-up | Reverse | Horizontal flip |
| `'FlipYLeft'` | Flip Y-left | Reverse | Vertical flip |
| `'FlipYRight'` | Flip Y-right | Reverse | Vertical flip |
| `'SlideBottom'` | Slide from bottom | Slide to bottom | Top-to-bottom |
| `'SlideLeft'` | Slide from left | Slide to left | Left-to-right |
| `'SlideRight'` | Slide from right | Slide to right | Right-to-left |
| `'SlideTop'` | Slide from top | Slide to top | Bottom-to-top |
| `'Zoom'` | ZoomIn | ZoomOut | Scale animation |
| `'None'` | No animation | No animation | Instant appearance |

## Effect Examples

### Example 1: Fade Effect (Gentle)

```jsx
<DialogComponent
  animationSettings={{
    effect: 'Fade',
    duration: 300,
    delay: 0
  }}
>
  Fades in smoothly
</DialogComponent>
```

### Example 2: Zoom Effect (Attention-grabbing)

```jsx
<DialogComponent
  animationSettings={{
    effect: 'Zoom',
    duration: 500,
    delay: 0
  }}
>
  Zooms in from center
</DialogComponent>
```

### Example 3: Slide Top (Professional)

```jsx
<DialogComponent
  animationSettings={{
    effect: 'SlideTop',
    duration: 400,
    delay: 0
  }}
>
  Slides down from top
</DialogComponent>
```

### Example 4: Flip (Dramatic)

```jsx
<DialogComponent
  animationSettings={{
    effect: 'FlipXUp',
    duration: 600,
    delay: 0
  }}
>
  Flips up dramatically
</DialogComponent>
```

### Example 5: Slide Bottom (Emphasis)

```jsx
<DialogComponent
  animationSettings={{
    effect: 'SlideBottom',
    duration: 350,
    delay: 0
  }}
>
  Slides up from bottom
</DialogComponent>
```

## Comparing Effects

```jsx
export function AnimationGallery() {
  const dialogRef = useRef(null);
  const [effect, setEffect] = React.useState('Fade');

  const effects = [
    'Fade', 'FadeZoom', 'Zoom',
    'SlideTop', 'SlideBottom', 'SlideLeft', 'SlideRight',
    'FlipXUp', 'FlipYLeft', 'None'
  ];

  const showWithEffect = (selectedEffect) => {
    setEffect(selectedEffect);
    // Close and reopen to trigger animation
    dialogRef.current?.hide();
    setTimeout(() => dialogRef.current?.show(), 100);
  };

  return (
    <div id="dialog-target" style={{ position: 'relative', height: '500px' }}>
      <div style={{ padding: '20px' }}>
        <h3>Choose Animation Effect:</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px' }}>
          {effects.map((eff) => (
            <button
              key={eff}
              onClick={() => showWithEffect(eff)}
              style={{
                padding: '10px',
                background: eff === effect ? '#667eea' : '#e5e7eb',
                color: eff === effect ? 'white' : 'black',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
              }}
            >
              {eff}
            </button>
          ))}
        </div>
      </div>

      <DialogComponent
        ref={dialogRef}
        header="Animation Demo"
        animationSettings={{
          effect: effect,
          duration: 400,
          delay: 0
        }}
        target="#dialog-target"
        showCloseIcon={true}
      >
        Preview: <strong>{effect}</strong> animation
      </DialogComponent>
    </div>
  );
}
```

## Duration and Delay

### Duration (Animation Speed)

Controls how long the animation takes in milliseconds:

```jsx
// Fast (200ms)
animationSettings={{ effect: 'Fade', duration: 200 }}

// Normal (400ms)
animationSettings={{ effect: 'Fade', duration: 400 }}

// Slow (800ms)
animationSettings={{ effect: 'Fade', duration: 800 }}

// Very Slow (1200ms)
animationSettings={{ effect: 'Fade', duration: 1200 }}
```

### Delay (Wait Before Animation)

Initial delay before animation starts:

```jsx
// No delay
animationSettings={{ effect: 'Zoom', duration: 400, delay: 0 }}

// 100ms delay
animationSettings={{ effect: 'Zoom', duration: 400, delay: 100 }}

// 500ms delay
animationSettings={{ effect: 'Zoom', duration: 400, delay: 500 }}
```

### Common Combinations

```jsx
// Snappy (quick with no delay)
{ effect: 'Fade', duration: 200, delay: 0 }

// Smooth (moderate speed, no delay)
{ effect: 'SlideTop', duration: 400, delay: 0 }

// Delayed announcement (with delay before animation)
{ effect: 'Zoom', duration: 500, delay: 200 }

// Slow emphasis (longer animation)
{ effect: 'FadeZoom', duration: 800, delay: 0 }
```

### Example: Adjustable Speed

```jsx
export function AdjustableAnimation() {
  const dialogRef = useRef(null);
  const [duration, setDuration] = React.useState(400);

  return (
    <div id="dialog-target" style={{ position: 'relative' }}>
      <div style={{ padding: '20px' }}>
        <label>
          Animation Duration (ms):
          <input
            type="range"
            min="100"
            max="1000"
            step="100"
            value={duration}
            onChange={(e) => setDuration(Number(e.target.value))}
          />
          {duration}ms
        </label>
      </div>

      <button onClick={() => dialogRef.current?.show()}>Open</button>

      <DialogComponent
        ref={dialogRef}
        header="Adjustable Speed"
        animationSettings={{
          effect: 'Zoom',
          duration: duration,
          delay: 0
        }}
        target="#dialog-target"
      >
        Adjust the slider to change animation speed
      </DialogComponent>
    </div>
  );
}
```

## Enable/Disable Animation

### Disable Animation

```jsx
// Option 1: Use 'None' effect
<DialogComponent
  animationSettings={{ effect: 'None' }}
>
  No animation
</DialogComponent>

// Option 2: Set duration to 0
<DialogComponent
  animationSettings={{ effect: 'Fade', duration: 0, delay: 0 }}
>
  Instant appearance
</DialogComponent>

// Option 3: Omit animationSettings
<DialogComponent>
  Default behavior (usually no animation)
</DialogComponent>
```

### Toggle Animation

```jsx
export function ToggleAnimation() {
  const dialogRef = useRef(null);
  const [animated, setAnimated] = React.useState(true);

  const animationSettings = animated
    ? { effect: 'Zoom', duration: 400, delay: 0 }
    : { effect: 'None' };

  return (
    <div id="dialog-target" style={{ position: 'relative' }}>
      <label>
        <input
          type="checkbox"
          checked={animated}
          onChange={(e) => setAnimated(e.target.checked)}
        />
        Enable Animation
      </label>

      <button onClick={() => dialogRef.current?.show()}>Open</button>

      <DialogComponent
        ref={dialogRef}
        header="Toggle Animation"
        animationSettings={animationSettings}
        target="#dialog-target"
      >
        Animation is {animated ? 'ON' : 'OFF'}
      </DialogComponent>
    </div>
  );
}
```

## Performance Considerations

### Animation Impact on Performance

- **Simple effects** (Fade, Zoom): Minimal performance cost
- **Complex effects** (Flip, FadeZoom): Higher GPU usage
- **Long duration**: Longer animation = more frame rendering
- **Multiple dialogs**: Each animated dialog consumes resources

### Best Practices

```jsx
// ✅ GOOD: Fast, simple animations for better performance
animationSettings={{
  effect: 'Fade',
  duration: 300,
  delay: 0
}}

// ❌ AVOID: Complex, long animations on constrained devices
animationSettings={{
  effect: 'FlipRightDown',
  duration: 2000,
  delay: 500
}}
```

### Disable Animation on Low-End Devices

```jsx
// Detect device capability
const isLowEndDevice = navigator.deviceMemory < 4;

const animationSettings = isLowEndDevice
  ? { effect: 'None' }
  : { effect: 'Zoom', duration: 400, delay: 0 };

<DialogComponent animationSettings={animationSettings}>
  Content
</DialogComponent>
```

### Responsive Animation

```jsx
const isMobile = window.innerWidth < 768;

const animationSettings = isMobile
  ? { effect: 'Fade', duration: 200, delay: 0 }    // Faster on mobile
  : { effect: 'Zoom', duration: 400, delay: 0 };   // Slower on desktop

<DialogComponent animationSettings={animationSettings}>
  Content
</DialogComponent>
```

### Animation During Heavy Processing

```jsx
export function AnimationWithProcessing() {
  const dialogRef = useRef(null);
  const [isProcessing, setIsProcessing] = React.useState(false);

  const handleOpen = () => {
    // Disable animation while processing
    const hasAnimation = !isProcessing;
    dialogRef.current?.show();
  };

  const animationSettings = isProcessing
    ? { effect: 'None' }
    : { effect: 'Zoom', duration: 400, delay: 0 };

  return (
    <div id="dialog-target" style={{ position: 'relative' }}>
      <button onClick={handleOpen}>Open</button>

      <DialogComponent
        ref={dialogRef}
        header="Processing"
        animationSettings={animationSettings}
        target="#dialog-target"
      >
        {isProcessing ? '⏳ Processing...' : '✅ Done'}
      </DialogComponent>
    </div>
  );
}
```

### Animation Queuing

For multiple dialogs, stagger animations:

```jsx
<DialogComponent
  ref={dialog1Ref}
  animationSettings={{ effect: 'Zoom', duration: 400, delay: 0 }}
>
  First dialog - immediate
</DialogComponent>

<DialogComponent
  ref={dialog2Ref}
  animationSettings={{ effect: 'Zoom', duration: 400, delay: 200 }}
>
  Second dialog - 200ms delay
</DialogComponent>

<DialogComponent
  ref={dialog3Ref}
  animationSettings={{ effect: 'Zoom', duration: 400, delay: 400 }}
>
  Third dialog - 400ms delay
</DialogComponent>
```

## Use Case Recommendations

| Use Case | Effect | Duration | Reason |
|----------|--------|----------|--------|
| Alert/Warning | Zoom | 300-400ms | Attention-grabbing |
| Confirmation | Fade | 250-300ms | Quick and professional |
| Information | SlideTop | 350-450ms | Gentle, informative |
| Complex Form | FadeZoom | 400-500ms | Signals importance |
| Notification | SlideTop | 200-300ms | Quick appearance |
| Help/Tutorial | Fade | 300-400ms | Non-intrusive |
| Loading Dialog | None | — | No animation needed |
| Unexpected Error | Zoom | 400-500ms | Emphasizes issue |

**Next:** Choose another reference topic based on your needs.
