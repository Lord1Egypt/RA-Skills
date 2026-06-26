# Zooming and Panning

## Table of Contents
- [Zoom Methods](#zoom-methods)
- [Zoom Settings](#zoom-settings)
- [Panning](#panning)
- [Zoom and Pan Events](#zoom-and-pan-events)

## Zoom Methods

### Zoom In

Increase magnification level:

```tsx
function zoomIn(): void {
  imgObj.zoom(1.5); // 150% zoom
}

function zoomIn2x(): void {
  imgObj.zoom(2); // 200% zoom
}
```

### Zoom Out

Decrease magnification level:

```tsx
function zoomOut(): void {
  imgObj.zoom(0.8); // 80% zoom
}

function zoomOutToFit(): void {
  imgObj.zoom(0.5); // 50% zoom
}
```

### Reset Zoom

Return to 100% (original size):

```tsx
function resetZoom(): void {
  imgObj.zoom(1); // 100% - original size
}
```

### Zoom at Specific Point

Zoom centered on specific coordinates:

```tsx
function zoomAtPoint(): void {
  const zoomFactor = 2;
  const centerX = 150;
  const centerY = 100;
  
  imgObj.zoom(zoomFactor, { x: centerX, y: centerY });
}
```

## Zoom Settings

### Configure Min and Max Zoom

Set zoom boundaries in `zoomSettings`:

```tsx
import { ZoomSettingsModel } from '@syncfusion/ej2-react-image-editor';

function App() {
  const zoomSettings: ZoomSettingsModel = {
    minZoomFactor: 0.1,  // Can zoom out to 10% of original
    maxZoomFactor: 30    // Can zoom in to 30x original
  };
  
  return <ImageEditorComponent zoomSettings={zoomSettings} />;
}
```

### Default Zoom Limits

By default:
- **Minimum:** 0.1 (10% of original)
- **Maximum:** 10 (10x original size)

### Implement Zoom Controls

Create zoom in/out buttons with limits:

```tsx
let currentZoom = 1;

function zoomInClick(): void {
  if (currentZoom < 1) {
    currentZoom += 0.1;
  } else {
    currentZoom += 1;
  }
  
  if (currentZoom > zoomSettings.maxZoomFactor!) {
    currentZoom = zoomSettings.maxZoomFactor!;
  }
  
  imgObj.zoom(currentZoom);
}

function zoomOutClick(): void {
  if (currentZoom <= 1) {
    currentZoom -= 0.1;
  } else {
    currentZoom -= 1;
  }
  
  if (currentZoom < zoomSettings.minZoomFactor!) {
    currentZoom = zoomSettings.minZoomFactor!;
  }
  
  imgObj.zoom(currentZoom);
}

return (
  <div>
    <button onClick={zoomInClick}>Zoom In</button>
    <button onClick={zoomOutClick}>Zoom Out</button>
    <span>{Math.round(currentZoom * 100)}%</span>
  </div>
);
```

## Panning

### Enable Panning Mode

Allow users to drag and pan the image:

```tsx
function enablePan(): void {
  imgObj.pan(true);
}

function disablePan(): void {
  imgObj.pan(false);
}
```

### Pan When Zoomed

Panning is typically enabled when image exceeds canvas size:

```tsx
function zoomAndPan(): void {
  imgObj.zoom(3); // Zoom to 300%
  imgObj.pan(true); // Enable dragging to move image
}
```

### Pan During Cropping

Users can pan within crop selection:

```tsx
function selectAndPan(): void {
  imgObj.select('Square', 50, 50, 300, 300);
  // Panning automatically becomes available for repositioning crop area
}
```

## Zoom and Pan Events

### Zooming Event

Triggered during zoom operation:

```tsx
function zooming(args: any): void {
  console.log('Zoom point:', args.zoomPoint);
  console.log('Previous zoom:', args.previousZoomFactor);
  console.log('Current zoom:', args.currentZoomFactor);
  console.log('Trigger:', args.zoomTrigger); // toolbar, mouse, keyboard, etc.
  
  // args.cancel = true; // Cancel zoom if needed
}

<ImageEditorComponent zooming={zooming} />
```

### Validate Zoom Level

Restrict zoom to specific increments:

```tsx
function zooming(args: any): void {
  // Only allow zoom at 0.5x increments
  const validZooms = [0.5, 1, 1.5, 2, 2.5, 3];
  
  if (!validZooms.includes(args.currentZoomFactor)) {
    args.cancel = true;
  }
}
```

### Panning Event

Triggered when user drags the image:

```tsx
function panning(args: any): void {
  console.log('Start point:', args.startPoint);
  console.log('End point:', args.endpoint);
  
  // args.cancel = true; // Cancel panning if needed
}

<ImageEditorComponent panning={panning} />
```

### Handle Pan Events

React to panning operations:

```tsx
function panning(args: any): void {
  console.log('Panning started');
  console.log('Start point:', args.startPoint);
  console.log('End point:', args.endpoint);
  
  // You can cancel panning if needed
  // args.cancel = true;
}

<ImageEditorComponent panning={panning} />
```

## Combined Patterns

### Zoom Level Display

Show current zoom percentage:

```tsx
let currentZoomLevel = 100;

function zooming(args: any): void {
  currentZoomLevel = Math.round(args.currentZoomFactor * 100);
  updateZoomDisplay(currentZoomLevel);
}

function updateZoomDisplay(level: number): void {
  document.getElementById('zoom-display').textContent = `${level}%`;
}
```

### Zoom to Fit Width

Scale image to fit container width:

```tsx
function zoomToWidth(): void {
  const dimension = imgObj.getImageDimension();
  const container = document.querySelector('.editor-container') as HTMLElement;
  if (container) {
    const containerWidth = container.offsetWidth;
    const zoomFactor = containerWidth / dimension.width;
    imgObj.zoom(zoomFactor);
  }
}
```

### Zoom to Fit Height

Scale image to fit container height:

```tsx
function zoomToHeight(): void {
  const dimension = imgObj.getImageDimension();
  const container = document.querySelector('.editor-container') as HTMLElement;
  if (container) {
    const containerHeight = container.offsetHeight;
    const zoomFactor = containerHeight / dimension.height;
    imgObj.zoom(zoomFactor);
  }
}
```

### Continuous Zoom

Smooth zoom animation:

```tsx
function continuousZoom(targetZoom: number, steps: number = 10): void {
  let currentZoom = 1;
  const step = (targetZoom - 1) / steps;
  
  const interval = setInterval(() => {
    currentZoom += step;
    imgObj.zoom(currentZoom);
    
    if (currentZoom >= targetZoom) {
      clearInterval(interval);
    }
  }, 50);
}

// Usage
continuousZoom(2); // Smooth zoom to 200%
```

### Keyboard Zoom

Support zoom with keyboard shortcuts:

```tsx
document.addEventListener('keydown', (e) => {
  if (e.ctrlKey) {
    if (e.key === '+' || e.key === '=') {
      e.preventDefault();
      imgObj.zoom(currentZoom + 0.1);
    } else if (e.key === '-') {
      e.preventDefault();
      imgObj.zoom(currentZoom - 0.1);
    }
  }
});
```
