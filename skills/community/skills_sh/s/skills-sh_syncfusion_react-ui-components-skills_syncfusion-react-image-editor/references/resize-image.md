# Resize Image

## Table of Contents

- [Basic Resize](#basic-resize)
- [Resize with Aspect Ratio](#resize-with-aspect-ratio)
- [Resize Dialog](#resize-dialog)
- [Programmatic Resize](#programmatic-resize)
- [Resize Events](#resize-events)
- [Advanced Patterns](#advanced-patterns)

## Basic Resize

### Resize Without Aspect Ratio

Change image dimensions independently:

```tsx
const dim = imgObj.getImageDimension();
console.log('Current dimensions:', dim.width, 'x', dim.height);

// Resize to specific dimensions
imgObj.resize(800, 600);
```

### Resize Parameters

```tsx
interface ResizeOptions {
  width: number;
  height: number;
  maintainAspectRatio?: boolean;
}
```

## Resize with Aspect Ratio

### Maintain Aspect Ratio

Preserve image proportions:

```tsx
// This example shows conceptual approach
// Resize maintains aspect ratio when specified
function resizeWithAspectRatio(targetWidth: number): void {
  const dim = imgObj.getImageDimension();
  const aspectRatio = dim.width / dim.height;
  const newHeight = Math.round(targetWidth / aspectRatio);
  
  imgObj.resize(targetWidth, newHeight);
}

// Usage: Resize to 800px wide, height auto-adjusts
resizeWithAspectRatio(800);
```

### Lock Aspect Ratio

```tsx
function resizeWithConstraints(width: number, height: number): void {
  const dim = imgObj.getImageDimension();
  const aspectRatio = dim.width / dim.height;
  
  // Adjust height based on width
  const adjustedHeight = Math.round(width / aspectRatio);
  
  imgObj.resize(width, adjustedHeight);
}

// Resize to 1024x auto-calculated height
resizeWithConstraints(1024, 0);
```

## Resize Dialog

### Open Resize Dialog

Show resize UI:

```tsx
function openResizeDialog(): void {
  const resizeButton = document.querySelector('[title*="Resize"]');
  if (resizeButton) {
    (resizeButton as HTMLElement).click();
  }
}
```

### Resize Dialog Integration

```tsx
const handleToolbarClick = (args: ToolbarClickEventArgs): void => {
  if (args.id === 'Resize') {
    // Resize dialog opens automatically
  }
};

const imageEditor = (
  <ImageEditorComponent toolbarItemClick={handleToolbarClick} />
);
```

## Programmatic Resize

### Resize to Specific Dimensions

```tsx
interface ResizeTarget {
  width: number;
  height: number;
}

function resizeTo(target: ResizeTarget): void {
  imgObj.resize(target.width, target.height);
}

// Usage
resizeTo({ width: 1920, height: 1080 });
```

### Resize by Percentage

```tsx
function resizeByPercentage(percentage: number): void {
  const dim = imgObj.getImageDimension();
  const factor = percentage / 100;
  
  const newWidth = Math.round(dim.width * factor);
  const newHeight = Math.round(dim.height * factor);
  
  imgObj.resize(newWidth, newHeight);
}

// Resize to 50% of original size
resizeByPercentage(50);

// Resize to 150% of original size
resizeByPercentage(150);
```

### Resize to Fit Container

```tsx
function resizeToFitContainer(containerWidth: number, containerHeight: number): void {
  const dim = imgObj.getImageDimension();
  const imageAspect = dim.width / dim.height;
  const containerAspect = containerWidth / containerHeight;
  
  let newWidth: number;
  let newHeight: number;
  
  if (imageAspect > containerAspect) {
    // Image is wider
    newWidth = containerWidth;
    newHeight = Math.round(containerWidth / imageAspect);
  } else {
    // Image is taller
    newHeight = containerHeight;
    newWidth = Math.round(containerHeight * imageAspect);
  }
  
  imgObj.resize(newWidth, newHeight);
}

// Usage
const container = document.querySelector('.editor-container');
if (container) {
  const rect = container.getBoundingClientRect();
  resizeToFitContainer(rect.width, rect.height);
}
```

## Resize Events

### Capturing Resize Event

```tsx
const handleResizing = (args: ResizingEventArgs): void => {
  console.log('Image resizing:', {
    width: args.width,
    height: args.height
  });
};

const imageEditor = (
  <ImageEditorComponent resizing={handleResizing} />
);
```

### Before/After Resize

```tsx
let resizeHistory: { before: any; after: any }[] = [];

const handleBeforeResize = (): void => {
  const dim = imgObj.getImageDimension();
  resizeHistory.push({
    before: { width: dim.width, height: dim.height },
    after: null
  });
};

const handleAfterResize = (): void => {
  if (resizeHistory.length > 0) {
    const dim = imgObj.getImageDimension();
    resizeHistory[resizeHistory.length - 1].after = {
      width: dim.width,
      height: dim.height
    };
  }
};
```

### Validate Resize

```tsx
const handleResizing = (args: ResizingEventArgs): void => {
  // Minimum dimensions
  if (args.width < 100 || args.height < 100) {
    args.cancel = true;
    console.warn('Image too small');
    return;
  }
  
  // Maximum dimensions
  if (args.width > 4000 || args.height > 4000) {
    args.cancel = true;
    console.warn('Image too large');
    return;
  }
};

const imageEditor = (
  <ImageEditorComponent resizing={handleResizing} />
);
```

## Advanced Patterns

### Common Resize Targets

```tsx
interface ResizePreset {
  name: string;
  width: number;
  height: number;
}

const resizePresets: ResizePreset[] = [
  { name: 'Thumbnail', width: 200, height: 200 },
  { name: 'Web Small', width: 640, height: 480 },
  { name: '720p', width: 1280, height: 720 },
  { name: '1080p', width: 1920, height: 1080 },
  { name: '4K', width: 3840, height: 2160 },
  { name: 'Instagram Square', width: 1080, height: 1080 },
  { name: 'Instagram Portrait', width: 1080, height: 1350 },
  { name: 'Twitter', width: 1200, height: 675 }
];

function applyPreset(presetName: string): void {
  const preset = resizePresets.find(p => p.name === presetName);
  if (preset) {
    imgObj.resize(preset.width, preset.height);
  }
}

// Usage
applyPreset('1080p');
```

### Batch Resize

```tsx
async function batchResize(imageUrls: string[], targetWidth: number): Promise<void> {
  for (const url of imageUrls) {
    imgObj.open(url);
    await new Promise(resolve => setTimeout(resolve, 500));
    
    const dim = imgObj.getImageDimension();
    const aspectRatio = dim.width / dim.height;
    const newHeight = Math.round(targetWidth / aspectRatio);
    
    imgObj.resize(targetWidth, newHeight);
    
    // Export the resized image
    imgObj.export('image/png', `resized-${url.split('/').pop()}`);
  }
}

// Usage
batchResize(['image1.jpg', 'image2.jpg', 'image3.jpg'], 800);
```

### Responsive Resize

```tsx
function makeResponsive(): void {
  const updateSize = (): void => {
    const container = document.querySelector('.editor-container');
    if (container) {
      const rect = container.getBoundingClientRect();
      resizeToFitContainer(rect.width, rect.height);
    }
  };
  
  // Initial resize
  updateSize();
  
  // Resize on window change
  window.addEventListener('resize', updateSize);
}

// Usage
makeResponsive();
```

### Resize with Constraints

```tsx
interface ResizeConstraints {
  minWidth: number;
  minHeight: number;
  maxWidth: number;
  maxHeight: number;
  aspectRatio?: number;
}

function resizeWithConstraints(
  width: number,
  height: number,
  constraints: ResizeConstraints
): void {
  let finalWidth = width;
  let finalHeight = height;
  
  // Apply constraints
  if (finalWidth < constraints.minWidth) finalWidth = constraints.minWidth;
  if (finalHeight < constraints.minHeight) finalHeight = constraints.minHeight;
  if (finalWidth > constraints.maxWidth) finalWidth = constraints.maxWidth;
  if (finalHeight > constraints.maxHeight) finalHeight = constraints.maxHeight;
  
  // Maintain aspect ratio
  if (constraints.aspectRatio) {
    finalHeight = Math.round(finalWidth / constraints.aspectRatio);
  }
  
  imgObj.resize(finalWidth, finalHeight);
}

// Usage
const constraints: ResizeConstraints = {
  minWidth: 200,
  minHeight: 200,
  maxWidth: 2000,
  maxHeight: 2000,
  aspectRatio: 16 / 9
};

resizeWithConstraints(1920, 1080, constraints);
```

### Dimension Presets with Custom Sizes

```tsx
class ResizeManager {
  private presets: Map<string, [number, number]> = new Map([
    ['small', [400, 300]],
    ['medium', [800, 600]],
    ['large', [1600, 1200]]
  ]);
  
  addPreset(name: string, width: number, height: number): void {
    this.presets.set(name, [width, height]);
  }
  
  applyPreset(name: string): void {
    const preset = this.presets.get(name);
    if (preset) {
      imgObj.resize(preset[0], preset[1]);
    }
  }
  
  getAllPresets(): string[] {
    return Array.from(this.presets.keys());
  }
}

const manager = new ResizeManager();
manager.applyPreset('large');
```

### Compression via Resize

```tsx
function compressImage(targetSize: number): void {
  // Reduce file size by resizing
  const dim = imgObj.getImageDimension();
  const scale = Math.sqrt(targetSize / (dim.width * dim.height));
  
  const newWidth = Math.round(dim.width * scale);
  const newHeight = Math.round(dim.height * scale);
  
  imgObj.resize(newWidth, newHeight);
}

// Compress to ~50% area
compressImage(0.5);
```
