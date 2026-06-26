# Fine-Tuning

## Fine-Tune Options

Adjust image properties with precise control:

| Option | Range | Effect |
|--------|-------|--------|
| Brightness | -100 to +100 | Light/dark intensity |
| Contrast | -100 to +100 | Tone separation |
| Saturation | -100 to +100 | Color intensity |
| Hue | -180 to +180 | Color shift |
| Exposure | -100 to +100 | Overall brightness |
| Blur | 0 to +100 | Blur intensity |
| Opacity | 0 to +100 | Transparency |

## Adjusting Brightness

```tsx
import { ImageFinetuneOption } from '@syncfusion/ej2-react-image-editor';

function increaseBrightness(): void {
  imgObj.finetuneImage(ImageFinetuneOption.Brightness, 30);
}

function decreaseBrightness(): void {
  imgObj.finetuneImage(ImageFinetuneOption.Brightness, -30);
}
```

## Adjusting Contrast

```tsx
function increaseContrast(): void {
  imgObj.finetuneImage(ImageFinetuneOption.Contrast, 40);
}

function decreaseContrast(): void {
  imgObj.finetuneImage(ImageFinetuneOption.Contrast, -20);
}
```

## Adjusting Saturation

```tsx
function increaseSaturation(): void {
  imgObj.finetuneImage(ImageFinetuneOption.Saturation, 50);
}

function decreaseSaturation(): void {
  imgObj.finetuneImage(ImageFinetuneOption.Saturation, -50);
}

// Full desaturation (grayscale)
function removeColor(): void {
  imgObj.finetuneImage(ImageFinetuneOption.Saturation, -100);
}
```

## Adjusting Hue

Shift colors across the spectrum:

```tsx
function shiftHueRed(): void {
  imgObj.finetuneImage(ImageFinetuneOption.Hue, 30);
}

function shiftHueGreen(): void {
  imgObj.finetuneImage(ImageFinetuneOption.Hue, 120);
}

function shiftHueBlue(): void {
  imgObj.finetuneImage(ImageFinetuneOption.Hue, -60);
}
```

## Adjusting Exposure

Control overall brightness:

```tsx
function increaseExposure(): void {
  imgObj.finetuneImage(ImageFinetuneOption.Exposure, 40);
}

function decreaseExposure(): void {
  imgObj.finetuneImage(ImageFinetuneOption.Exposure, -40);
}
```

## Adjusting Blur

Add blur effects:

```tsx
function lightBlur(): void {
  imgObj.finetuneImage(ImageFinetuneOption.Blur, 10);
}

function mediumBlur(): void {
  imgObj.finetuneImage(ImageFinetuneOption.Blur, 30);
}

function heavyBlur(): void {
  imgObj.finetuneImage(ImageFinetuneOption.Blur, 60);
}
```

## Adjusting Opacity

```tsx
function makeTransparent(): void {
  imgObj.finetuneImage(ImageFinetuneOption.Opacity, 50);
}

function makeOpaque(): void {
  imgObj.finetuneImage(ImageFinetuneOption.Opacity, 100);
}
```

## Fine-Tune Events

### Detect Fine-Tune Changes

```tsx
function finetuneValueChanging(args: any): void {
  console.log('Fine-tune type:', args.finetune);
  console.log('Value:', args.value);
  // args.cancel = true; // Prevent adjustment
}

<ImageEditorComponent finetuneValueChanging={finetuneValueChanging} />
```

## Advanced Patterns

### Slider-Based Fine-Tuning

Connect slider to fine-tune value:

```tsx
function createBrightnessSlider(): void {
  const slider = document.getElementById('brightness-slider') as HTMLInputElement;
  
  slider.addEventListener('input', (e) => {
    const value = parseInt(e.target.value);
    imgObj.finetuneImage(ImageFinetuneOption.Brightness, value);
  });
}
```

### Multiple Adjustments

Apply several adjustments:

```tsx
function enhanceImage(): void {
  imgObj.finetuneImage(ImageFinetuneOption.Contrast, 20);
  imgObj.finetuneImage(ImageFinetuneOption.Saturation, 30);
  imgObj.finetuneImage(ImageFinetuneOption.Brightness, 15);
}
```

### Reset Specific Adjustment

Undo specific fine-tune:

```tsx
function resetBrightness(): void {
  imgObj.undo(); // Undo last adjustment
}

function resetAll(): void {
  imgObj.reset(); // Reset all changes
}
```

### Preset Adjustments

Create adjustment presets:

```tsx
const presets = {
  vivid: [
    { option: ImageFinetuneOption.Saturation, value: 40 },
    { option: ImageFinetuneOption.Contrast, value: 20 }
  ],
  muted: [
    { option: ImageFinetuneOption.Saturation, value: -30 },
    { option: ImageFinetuneOption.Brightness, value: 10 }
  ],
  vintage: [
    { option: ImageFinetuneOption.Hue, value: -20 },
    { option: ImageFinetuneOption.Saturation, value: -20 },
    { option: ImageFinetuneOption.Brightness, value: 5 }
  ]
};

function applyPreset(presetName: string): void {
  presets[presetName].forEach(adj => {
    imgObj.finetuneImage(adj.option, adj.value);
  });
}

// Usage
applyPreset('vivid');
```

### Real-Time Preview

Live adjustment preview:

```tsx
let adjustmentValue = 0;

function liveAdjust(option: ImageFinetuneOption, value: number): void {
  // Cancel previous and apply new
  imgObj.undo();
  imgObj.finetuneImage(option, value);
  adjustmentValue = value;
}

// On slider input
slider.addEventListener('input', (e) => {
  liveAdjust(ImageFinetuneOption.Contrast, parseInt(e.target.value));
});
```

### Conditional Fine-Tuning

Apply adjustments based on conditions:

```tsx
function smartEnhance(): void {
  const dim = imgObj.getImageDimension();
  
  // If image is large, reduce blur
  if (dim.width > 800) {
    imgObj.finetuneImage(ImageFinetuneOption.Blur, 5);
  } else {
    imgObj.finetuneImage(ImageFinetuneOption.Blur, 10);
  }
  
  // Always increase contrast
  imgObj.finetuneImage(ImageFinetuneOption.Contrast, 15);
}
```

### Undo/Redo with Fine-Tuning

```tsx
let adjustmentHistory: any[] = [];

function recordAdjustment(option: ImageFinetuneOption, value: number): void {
  adjustmentHistory.push({ option, value });
  imgObj.finetuneImage(option, value);
}

function undoAdjustment(): void {
  imgObj.undo();
  adjustmentHistory.pop();
}

function redoAdjustment(): void {
  imgObj.redo();
  adjustmentHistory.push(adjustmentHistory[adjustmentHistory.length - 1]);
}
```

### Combined Filter + Fine-Tune

Perfect professional editing workflow:

```tsx
function professionalEnhancement(): void {
  // Apply sepia filter
  imgObj.applyImageFilter(ImageFilterOption.Sepia);
  
  // Fine-tune for better result
  imgObj.finetuneImage(ImageFinetuneOption.Contrast, 10);
  imgObj.finetuneImage(ImageFinetuneOption.Saturation, 5);
  imgObj.finetuneImage(ImageFinetuneOption.Brightness, -5);
}
```

### Batch Fine-Tuning

Apply list of adjustments:

```tsx
function batchFinetuneImage(adjustments: Array<{option: ImageFinetuneOption, value: number}>): void {
  adjustments.forEach(adj => {
    imgObj.finetuneImage(adj.option, adj.value);
  });
}

// Usage
batchFinetuneImage([
  { option: ImageFinetuneOption.Brightness, value: 20 },
  { option: ImageFinetuneOption.Contrast, value: 15 },
  { option: ImageFinetuneOption.Saturation, value: 25 }
]);
```
