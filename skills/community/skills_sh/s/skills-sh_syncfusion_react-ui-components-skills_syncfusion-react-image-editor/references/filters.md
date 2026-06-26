# Filters

## Available Filters

The Image Editor supports 6 predefined filters for instant visual effects:

| Filter | Effect | Use Case |
|--------|--------|----------|
| Chrome | Metallic effect | Modern look |
| Cold | Blue tones | Winter/cool mood |
| Warm | Orange/yellow tones | Sunset/warm mood |
| Grayscale | Black & white | Professional/vintage |
| Sepia | Brown tones | Vintage/antique |
| Invert | Negative colors | X-ray effect |

## Applying Filters

### Apply Single Filter

```tsx
import { ImageFilterOption } from '@syncfusion/ej2-react-image-editor';

function applyChrome(): void {
  imgObj.applyImageFilter(ImageFilterOption.Chrome);
}

function applyCold(): void {
  imgObj.applyImageFilter(ImageFilterOption.Cold);
}

function applyWarm(): void {
  imgObj.applyImageFilter(ImageFilterOption.Warm);
}

function applyGrayscale(): void {
  imgObj.applyImageFilter(ImageFilterOption.Grayscale);
}

function applySepia(): void {
  imgObj.applyImageFilter(ImageFilterOption.Sepia);
}

function applyInvert(): void {
  imgObj.applyImageFilter(ImageFilterOption.Invert);
}
```

### Filter Toolbar Integration

Add filter buttons to toolbar:

```tsx
const toolbar = [
  'Open',
  'Filter',
  'ZoomIn',
  'ZoomOut',
  {text: 'Chrome', prefixIcon: 'e-icons e-filter'},
  {text: 'Sepia', prefixIcon: 'e-icons e-filter'},
  'Save'
];

function toolbarItemClicked(args: any): void {
  if (args.item.text === 'Chrome') {
    imgObj.applyImageFilter(ImageFilterOption.Chrome);
  } else if (args.item.text === 'Sepia') {
    imgObj.applyImageFilter(ImageFilterOption.Sepia);
  }
}

<ImageEditorComponent toolbar={toolbar} toolbarItemClicked={toolbarItemClicked} />
```

## Filter Effects Gallery

### Chrome Effect

Modern metallic appearance:

```tsx
function applyChromeEffect(): void {
  imgObj.applyImageFilter(ImageFilterOption.Chrome);
}
```

### Cold Effect

Cool blue tone enhancement:

```tsx
function applyColdEffect(): void {
  imgObj.applyImageFilter(ImageFilterOption.Cold);
}
```

### Warm Effect

Warm orange/yellow tone:

```tsx
function applyWarmEffect(): void {
  imgObj.applyImageFilter(ImageFilterOption.Warm);
}
```

### Sepia Effect

Vintage brown tone:

```tsx
function applySepiaEffect(): void {
  imgObj.applyImageFilter(ImageFilterOption.Sepia);
}
```

### Grayscale Effect

Black and white conversion:

```tsx
function applyGrayscaleEffect(): void {
  imgObj.applyImageFilter(ImageFilterOption.Grayscale);
}
```

### Invert Effect

Negative/inverted colors:

```tsx
function applyInvertEffect(): void {
  imgObj.applyImageFilter(ImageFilterOption.Invert);
}
```

## Filter Events

### Detect Filter Application

React to filter changes:

```tsx
function imageFiltering(args: any): void {
  console.log('Applying filter:', args.filter);
  // args.cancel = true; // Prevent filter if needed
}

<ImageEditorComponent imageFiltering={imageFiltering} />
```

### Log Filter History

Track applied filters:

```tsx
let filterHistory: string[] = [];

function imageFiltering(args: any): void {
  filterHistory.push(args.filter);
  console.log('Filter history:', filterHistory);
}
```

## Advanced Patterns

### Filter Toggle

Apply and remove filters:

```tsx
let currentFilter: string | null = null;

function toggleFilter(filter: ImageFilterOption): void {
  if (currentFilter === filter) {
    imgObj.reset(); // Remove filter
    currentFilter = null;
  } else {
    if (currentFilter) {
      imgObj.undo(); // Remove previous filter
    }
    imgObj.applyImageFilter(filter);
    currentFilter = filter;
  }
}
```

### Filter Preview

Show before/after comparison:

```tsx
function previewFilter(filter: ImageFilterOption): void {
  // Save original state
  const originalImage = imgObj.getImageData();
  
  // Apply filter
  imgObj.applyImageFilter(filter);
  
  // User can accept or undo
}
```

### Sequential Filters

Apply multiple filters in sequence:

```tsx
function applyFilterSequence(): void {
  imgObj.applyImageFilter(ImageFilterOption.Grayscale);
  imgObj.applyImageFilter(ImageFilterOption.Cold);
}

// Result: Grayscale + Cold combined
```

### Undo Filter

Remove last applied filter:

```tsx
function undoFilter(): void {
  imgObj.undo();
}
```

### Reset All Filters

Remove all effects:

```tsx
function resetFilters(): void {
  imgObj.reset();
}
```

### Filter with Fine-tuning

Combine filter with adjustments:

```tsx
function enhancedSepia(): void {
  // Apply sepia
  imgObj.applyImageFilter(ImageFilterOption.Sepia);
  
  // Fine-tune contrast
  imgObj.finetuneImage(ImageFinetuneOption.Contrast, 20);
  
  // Fine-tune saturation
  imgObj.finetuneImage(ImageFinetuneOption.Saturation, 15);
}
```

### Dynamic Filter Selection

Filter selector UI:

```tsx
function selectFilter(filterName: string): void {
  const filterMap = {
    'chrome': ImageFilterOption.Chrome,
    'cold': ImageFilterOption.Cold,
    'warm': ImageFilterOption.Warm,
    'grayscale': ImageFilterOption.Grayscale,
    'sepia': ImageFilterOption.Sepia,
    'invert': ImageFilterOption.Invert
  };
  
  const filter = filterMap[filterName];
  if (filter) {
    imgObj.applyImageFilter(filter);
  }
}

// Usage
selectFilter('sepia');
```

### Filter History Playback

Replay previous filters:

```tsx
let appliedFilters: ImageFilterOption[] = [];

function recordAndApplyFilter(filter: ImageFilterOption): void {
  appliedFilters.push(filter);
  imgObj.applyImageFilter(filter);
}

function replayFilters(): void {
  imgObj.reset();
  appliedFilters.forEach(filter => {
    imgObj.applyImageFilter(filter);
  });
}
```

### Non-Destructive Filtering

Keep original with filter layer:

```tsx
let hasFilter = false;
let filterApplied: ImageFilterOption | null = null;

function applyNonDestructive(filter: ImageFilterOption): void {
  if (hasFilter && filterApplied) {
    imgObj.undo();
  }
  
  imgObj.applyImageFilter(filter);
  hasFilter = true;
  filterApplied = filter;
}

function removeFilter(): void {
  if (hasFilter) {
    imgObj.undo();
    hasFilter = false;
    filterApplied = null;
  }
}
```
