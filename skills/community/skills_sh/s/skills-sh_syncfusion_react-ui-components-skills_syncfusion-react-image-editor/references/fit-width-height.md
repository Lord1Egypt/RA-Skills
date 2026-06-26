# Fit to Width and Height

## Table of Contents

- [Fit to Width](#fit-to-width)
- [Fit to Height](#fit-to-height)
- [Fit to Viewport](#fit-to-viewport)
- [Smart Zoom Patterns](#smart-zoom-patterns)

## Fit to Width

### Zoom to Fit Width

Scale image to fit container width:

```tsx
function fitToWidth(): void {
  const dim = imgObj.getImageDimension();
  const container = document.querySelector('.editor-container');
  
  if (!container) return;
  
  const containerWidth = container.clientWidth;
  const scale = containerWidth / dim.width;
  
  imgObj.zoom(scale);
}
```

### Calculate Width Zoom

```tsx
function calculateZoomForWidth(containerWidth: number, imageWidth: number): number {
  const padding = 20; // Account for padding/margins
  const availableWidth = containerWidth - padding;
  return availableWidth / imageWidth;
}

// Usage
const zoom = calculateZoomForWidth(800, 1200);
imgObj.zoom(zoom);
```

### Fit with Padding

```tsx
function fitToWidthWithPadding(paddingPercent: number = 10): void {
  const dim = imgObj.getImageDimension();
  const container = document.querySelector('.editor-container');
  
  if (!container) return;
  
  const containerWidth = container.clientWidth;
  const availableWidth = containerWidth * (1 - paddingPercent / 100);
  const scale = availableWidth / dim.width;
  
  imgObj.zoom(scale);
}

// Fit with 10% padding
fitToWidthWithPadding(10);
```

## Fit to Height

### Zoom to Fit Height

Scale image to fit container height:

```tsx
function fitToHeight(): void {
  const dim = imgObj.getImageDimension();
  const container = document.querySelector('.editor-container');
  
  if (!container) return;
  
  const containerHeight = container.clientHeight;
  const scale = containerHeight / dim.height;
  
  imgObj.zoom(scale);
}
```

### Calculate Height Zoom

```tsx
function calculateZoomForHeight(containerHeight: number, imageHeight: number): number {
  const padding = 20;
  const availableHeight = containerHeight - padding;
  return availableHeight / imageHeight;
}

// Usage
const zoom = calculateZoomForHeight(600, 1600);
imgObj.zoom(zoom);
```

### Fit with Padding

```tsx
function fitToHeightWithPadding(paddingPercent: number = 10): void {
  const dim = imgObj.getImageDimension();
  const container = document.querySelector('.editor-container');
  
  if (!container) return;
  
  const containerHeight = container.clientHeight;
  const availableHeight = containerHeight * (1 - paddingPercent / 100);
  const scale = availableHeight / dim.height;
  
  imgObj.zoom(scale);
}

// Fit with 10% padding
fitToHeightWithPadding(10);
```

## Fit to Viewport

### Fit Best (Contain)

Scale to fit entire image in view:

```tsx
function fitBest(): void {
  const dim = imgObj.getImageDimension();
  const container = document.querySelector('.editor-container');
  
  if (!container) return;
  
  const containerWidth = container.clientWidth;
  const containerHeight = container.clientHeight;
  
  const widthScale = containerWidth / dim.width;
  const heightScale = containerHeight / dim.height;
  
  const scale = Math.min(widthScale, heightScale);
  imgObj.zoom(scale);
}
```

### Fit to Cover

Scale to cover entire viewport:

```tsx
function fitCover(): void {
  const dim = imgObj.getImageDimension();
  const container = document.querySelector('.editor-container');
  
  if (!container) return;
  
  const containerWidth = container.clientWidth;
  const containerHeight = container.clientHeight;
  
  const widthScale = containerWidth / dim.width;
  const heightScale = containerHeight / dim.height;
  
  const scale = Math.max(widthScale, heightScale);
  imgObj.zoom(scale);
}
```

### Fit Exact

Fill viewport exactly (may distort):

```tsx
function fitExact(): void {
  const dim = imgObj.getImageDimension();
  const container = document.querySelector('.editor-container');
  
  if (!container) return;
  
  const containerWidth = container.clientWidth;
  const containerHeight = container.clientHeight;
  
  imgObj.zoom(containerWidth / dim.width);
  imgObj.zoom(containerHeight / dim.height);
}
```

## Smart Zoom Patterns

### Auto Zoom on Load

```tsx
const handleImageOpened = (): void => {
  // Auto-fit on load
  fitBest();
};

const imageEditor = (
  <ImageEditorComponent fileOpened={handleImageOpened} />
);
```

### Responsive Fit

```tsx
function setupResponsiveFit(): void {
  const resizeObserver = new ResizeObserver(() => {
    fitBest();
  });
  
  const container = document.querySelector('.editor-container');
  if (container) {
    resizeObserver.observe(container);
  }
}

// Usage on component mount
useEffect(() => {
  setupResponsiveFit();
}, []);
```

### Orientation-Based Fit

```tsx
function fitByOrientation(): void {
  const dim = imgObj.getImageDimension();
  const isPortrait = dim.height > dim.width;
  
  if (isPortrait) {
    fitToHeight();
  } else {
    fitToWidth();
  }
}
```

### Zoom with Constraints

```tsx
interface ZoomConstraints {
  minZoom: number;
  maxZoom: number;
}

function fitWithConstraints(scale: number, constraints: ZoomConstraints): void {
  const constrainedScale = Math.max(
    constraints.minZoom,
    Math.min(scale, constraints.maxZoom)
  );
  
  imgObj.zoom(constrainedScale);
}

// Usage
const constraints: ZoomConstraints = { minZoom: 0.1, maxZoom: 3 };
fitWithConstraints(1.5, constraints);
```

### Fit to Specific Aspect Ratio

```tsx
function fitToAspectRatio(targetAspect: number): void {
  const dim = imgObj.getImageDimension();
  const container = document.querySelector('.editor-container');
  
  if (!container) return;
  
  const containerWidth = container.clientWidth;
  const containerHeight = container.clientHeight;
  const containerAspect = containerWidth / containerHeight;
  
  let scale: number;
  
  if (containerAspect > targetAspect) {
    // Container wider
    scale = containerHeight / dim.height;
  } else {
    // Container taller
    scale = containerWidth / dim.width;
  }
  
  imgObj.zoom(scale);
}

// Fit to 16:9
fitToAspectRatio(16 / 9);
```

### Fit with Animation

```tsx
function fitWithAnimation(targetScale: number, duration: number = 500): void {
  const startScale = imgObj.zoom();
  const startTime = Date.now();
  
  function animate(): void {
    const elapsed = Date.now() - startTime;
    const progress = Math.min(elapsed / duration, 1);
    
    // Easing function
    const eased = progress < 0.5
      ? 2 * progress * progress
      : -1 + (4 - 2 * progress) * progress;
    
    const currentScale = startScale + (targetScale - startScale) * eased;
    imgObj.zoom(currentScale);
    
    if (progress < 1) {
      requestAnimationFrame(animate);
    }
  }
  
  animate();
}

// Usage
fitWithAnimation(1.5, 500);
```

### Fit with Transition

```tsx
function fitWithTransition(action: () => void, duration: number = 300): void {
  const editor = document.querySelector('.editor-container');
  if (editor) {
    (editor as HTMLElement).style.transition = `transform ${duration}ms ease-in-out`;
  }
  
  action();
  
  setTimeout(() => {
    if (editor) {
      (editor as HTMLElement).style.transition = '';
    }
  }, duration);
}

// Usage
fitWithTransition(() => fitBest(), 300);
```

### Smart Fit Strategy

```tsx
enum FitStrategy {
  Auto = 'auto',
  Width = 'width',
  Height = 'height',
  Contain = 'contain'
}

function smartFit(strategy: FitStrategy = FitStrategy.Auto): void {
  const dim = imgObj.getImageDimension();
  const container = document.querySelector('.editor-container');
  
  if (!container) return;
  
  const containerWidth = container.clientWidth;
  const containerHeight = container.clientHeight;
  
  switch (strategy) {
    case FitStrategy.Width:
      fitToWidth();
      break;
    case FitStrategy.Height:
      fitToHeight();
      break;
    case FitStrategy.Contain:
      fitBest();
      break;
    case FitStrategy.Auto:
      // Auto-select best strategy
      const isPortrait = dim.height > dim.width;
      const isLandscape = dim.width > dim.height;
      
      if (isPortrait) {
        fitToHeight();
      } else if (isLandscape) {
        fitToWidth();
      } else {
        fitBest();
      }
      break;
  }
}

// Usage
smartFit(FitStrategy.Auto);
```

### Keyboard Shortcuts for Fit

```tsx
const fitKeyboardShortcuts: Record<string, () => void> = {
  'f': fitBest,
  'w': fitToWidth,
  'h': fitToHeight,
  'c': fitCover
};

document.addEventListener('keydown', (e: KeyboardEvent) => {
  if (e.altKey && fitKeyboardShortcuts[e.key]) {
    e.preventDefault();
    fitKeyboardShortcuts[e.key]();
  }
});
```

### Fit with Toolbar Integration

```tsx
const customToolbar = [
  'Open',
  'Save',
  {
    id: 'fit-width',
    text: 'Fit Width',
    tooltipText: 'Fit to Width'
  },
  {
    id: 'fit-height',
    text: 'Fit Height',
    tooltipText: 'Fit to Height'
  },
  {
    id: 'fit-best',
    text: 'Fit Best',
    tooltipText: 'Fit Best'
  }
];

const handleToolbarClick = (args: any): void => {
  switch (args.id) {
    case 'fit-width':
      fitToWidth();
      break;
    case 'fit-height':
      fitToHeight();
      break;
    case 'fit-best':
      fitBest();
      break;
  }
};

const imageEditor = (
  <ImageEditorComponent
    toolbar={customToolbar}
    toolbarItemClick={handleToolbarClick}
  />
);
```
