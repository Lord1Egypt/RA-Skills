# Transform: Rotate, Flip, and Straighten

## Table of Contents
- [Rotation](#rotation)
- [Flipping](#flipping)
- [Straightening](#straightening)
- [Transform Events](#transform-events)
- [Combining Transformations](#combining-transformations)

## Rotation

### Rotate Clockwise

Rotate image by positive degrees (clockwise):

```tsx
function rotateClockwise(): void {
  imgObj.rotate(90); // 90 degrees clockwise
}

function rotate180(): void {
  imgObj.rotate(180); // 180 degrees
}

function rotate270(): void {
  imgObj.rotate(270); // 270 degrees clockwise
}
```

### Rotate Counter-Clockwise

Rotate image by negative degrees (counter-clockwise):

```tsx
function rotateCounterClockwise(): void {
  imgObj.rotate(-90); // 90 degrees counter-clockwise
}
```

### Best Practices for Rotation

Use multiples of 90° for proper alignment:

```tsx
// Good - clean rotations
imgObj.rotate(90);   // ✓
imgObj.rotate(180);  // ✓
imgObj.rotate(270);  // ✓

// Not recommended - partial rotations
imgObj.rotate(45);   // ⚠️ May cause image quality loss
imgObj.rotate(30);   // ⚠️ May cause artifacts
```

### Rotate with Annotations

All annotations rotate along with the image:

```tsx
function rotateWithAnnotations(): void {
  // Add annotations first
  imgObj.drawText(100, 100, 'Sample Text');
  imgObj.drawRectangle(50, 50, 150, 100);
  
  // Rotate - annotations rotate too
  imgObj.rotate(90);
}
```

## Flipping

### Flip Horizontally

Create mirror effect along vertical axis:

```tsx
function flipHorizontal(): void {
  imgObj.flip('Horizontal');
}
```

### Flip Vertically

Create mirror effect along horizontal axis:

```tsx
function flipVertical(): void {
  imgObj.flip('Vertical');
}
```

### Flip Combinations

Combine multiple flips:

```tsx
function flipBoth(): void {
  imgObj.flip('Horizontal');
  imgObj.flip('Vertical');
  // Result: 180° rotation via flips
}
```

### Flip with Annotations

Annotations are transformed along with flip:

```tsx
function flipWithAnnotations(): void {
  imgObj.drawText(100, 100, 'Text');
  imgObj.drawArrow(50, 50, 150, 150);
  
  imgObj.flip('Horizontal');
  // Annotations flip along with image
}
```

## Straightening

### Straighten Image

Fine-tune rotation for slight angle corrections (-45° to +45°):

```tsx
function straightenClockwise(): void {
  imgObj.straightenImage(45); // Rotate up to 45° clockwise
}

function straightenCounterClockwise(): void {
  imgObj.straightenImage(-20); // Rotate 20° counter-clockwise
}

function subtleAdjustment(): void {
  imgObj.straightenImage(5); // Minor 5° adjustment
}
```

### Straighten Range

The straightening function accepts degrees between -45 and +45:

```tsx
// Valid range
imgObj.straightenImage(-45);  // Max counter-clockwise
imgObj.straightenImage(0);    // No change
imgObj.straightenImage(45);   // Max clockwise
```

### Use Case: Fix Tilted Photos

Correct slightly tilted images:

```tsx
function fixTiltedPhoto(): void {
  // User determines angle needed, e.g., -8 degrees
  imgObj.straightenImage(-8);
}
```

## Transform Events

### Rotating Event

Triggered during rotation:

```tsx
function rotating(args: any): void {
  console.log('Previous degree:', args.previousDegree);
  console.log('Current degree:', args.currentDegree);
  // args.cancel = true; // Cancel rotation
}

<ImageEditorComponent rotating={rotating} />
```

### Flipping Event

Triggered during flip operation:

```tsx
function flipping(args: any): void {
  console.log('Flip direction:', args.direction); // 'Horizontal' or 'Vertical'
  // args.cancel = true; // Cancel flip
}

<ImageEditorComponent flipping={flipping} />
```

### Validate Rotation Angle

Prevent excessive rotations:

```tsx
function rotating(args: any): void {
  const newDegree = args.currentDegree;
  
  // Only allow 0, 90, 180, 270
  const validDegrees = [0, 90, 180, 270];
  if (!validDegrees.includes(newDegree % 360)) {
    args.cancel = true;
  }
}
```

## Combining Transformations

### Sequential Transformations

Apply multiple transforms in sequence:

```tsx
function complexTransform(): void {
  imgObj.rotate(90);          // Rotate
  imgObj.flip('Horizontal');  // Flip
  imgObj.straightenImage(5);  // Straighten
}
```

### Transform with Zoom and Pan

Combine transforms with zoom/pan:

```tsx
function transformAndZoom(): void {
  imgObj.rotate(90);
  imgObj.zoom(1.5);  // Zoom to 1.5x
  imgObj.pan(true);  // Enable panning
}
```

### Reset Transformations

Use undo or reset to revert transformations:

```tsx
function undoTransform(): void {
  imgObj.undo(); // Undo last transformation
}

function resetAll(): void {
  imgObj.reset(); // Reset all changes to original
}
```

### Transform Pipeline

Apply transforms in a controlled pipeline:

```tsx
function transformPipeline(): void {
  const transforms = [
    () => imgObj.rotate(90),
    () => imgObj.flip('Horizontal'),
    () => imgObj.straightenImage(10)
  ];
  
  transforms.forEach(transform => transform());
}
```

### Get Current Rotation State

Track current transformation state:

```tsx
let rotationState = 0;

function trackRotation(): void {
  function rotating(args: any): void {
    rotationState = args.currentDegree;
    console.log('Current rotation:', rotationState);
  }
  
  return <ImageEditorComponent rotating={rotating} />;
}
```

### Transform with Annotations

Apply transforms that affect all elements:

```tsx
function transformAll(): void {
  // Add various annotations
  imgObj.drawText(50, 50, 'Label');
  imgObj.drawRectangle(100, 100, 150, 100);
  imgObj.drawCircle(250, 250);
  
  // Rotate everything together
  imgObj.rotate(90);
  
  // All annotations rotate with the image
}
```

### Prevent Transform

Cancel specific transformations based on conditions:

```tsx
function rotating(args: any): void {
  // Don't allow rotation if image dimensions exceed limits
  if (args.currentDegree !== 0 && args.currentDegree % 90 !== 0) {
    args.cancel = true;
    console.log('Only 90° rotations allowed');
  }
}
```
