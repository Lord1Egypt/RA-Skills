# Selection and Cropping

## Table of Contents
- [Selection Methods](#selection-methods)
- [Cropping](#cropping)
- [Selection Events](#selection-events)
- [Advanced Patterns](#advanced-patterns)

## Selection Methods

### Custom Selection

Create a custom rectangular selection with specified dimensions:

```tsx
function selectCustom(): void {
  imgObj.select('Custom', 50, 50, 300, 200);
  // startX=50, startY=50, width=300, height=200
}
```

### Square Selection

Insert a square selection:

```tsx
function selectSquare(): void {
  imgObj.select('Square', 100, 100, 200, 200);
}
```

### Circle Selection

Insert a circular selection:

```tsx
function selectCircle(): void {
  imgObj.select('Circle', 150, 150, 100, 100);
}
```

### Aspect Ratio Selections

Select with predefined aspect ratios:

```tsx
// 16:9 aspect ratio
function select16_9(): void {
  imgObj.select('16:9', 50, 50);
}

// 9:16 aspect ratio
function select9_16(): void {
  imgObj.select('9:16', 50, 50);
}

// 4:3 aspect ratio
function select4_3(): void {
  imgObj.select('4:3', 50, 50);
}

// 3:4 aspect ratio
function select3_4(): void {
  imgObj.select('3:4', 50, 50);
}

// Supported ratios: 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 5:7, 7:5, 9:16, 16:9
```

## Cropping

### Basic Crop

Crop the image based on current selection:

```tsx
function cropImage(): void {
  imgObj.select('Square');
  imgObj.crop();
}
```

### Crop with Circle Selection

Combine circle selection with cropping:

```tsx
function circleCrop(): void {
  imgObj.select('Circle');
  imgObj.crop();
}
```

### Crop with Ratio

Crop using a specific aspect ratio:

```tsx
function cropWith16_9(): void {
  imgObj.select('16:9', 50, 50);
  imgObj.crop();
}
```

## Selection Events

### Cropping Event

Triggered during the crop operation:

```tsx
function cropping(args: any): void {
  console.log('Start point:', args.startPoint);
  console.log('End point:', args.endPoint);
  // args.cancel = true; // Cancel crop if needed
}

<ImageEditorComponent cropping={cropping} />
```

### Maintain Original Image Size During Cropping

Prevent automatic scaling after cropping:

```tsx
function cropping(args: any): void {
  args.preventScaling = true;
}

<ImageEditorComponent cropping={cropping} />
```

**Result:** Image retains its original size without enlargement.

### Selection Changing Event

Triggered when selection is resized or modified:

```tsx
function selectionChanging(args: any): void {
  console.log('Action:', args.action); // 'insert' or 'resize'
  console.log('Current selection:', args.currentSelectionSettings);
  console.log('Previous selection:', args.previousSelectionSettings);
}

<ImageEditorComponent selectionChanging={selectionChanging} />
```

### Lock Selection Area During Resizing

Prevent users from resizing the selection:

```tsx
function selectionChanging(args: any): void {
  if (args.action === 'resize') {
    args.currentSelectionSettings = args.previousSelectionSettings;
  }
}

<ImageEditorComponent selectionChanging={selectionChanging} />
```

**Result:** Selection handles appear but resize operations are ignored.

## Advanced Patterns

### Custom Ratio Selection

Enforce custom ratio during selection resizing:

```tsx
function selectionChanging(args: any): void {
  if (args.action === 'insert' && args.currentSelectionSettings.type === 'Custom') {
    // Validate and adjust selection before applying
    if (args.currentSelectionSettings.height > 500) {
      args.currentSelectionSettings.height = 500;
    }
    if (args.currentSelectionSettings.width > 500) {
      args.currentSelectionSettings.width = 500;
    }
  }
}

<ImageEditorComponent selectionChanging={selectionChanging} />
```

### Sequential Selections and Crops

Perform multiple selections and crops:

```tsx
function multiCrop(): void {
  // First crop
  imgObj.select('16:9', 0, 0);
  imgObj.crop();
  
  // Clear and second crop
  imgObj.select('Square', 50, 50);
  imgObj.crop();
}
```

### Selection with Panning

Pan to adjust crop area:

```tsx
function selectAndPan(): void {
  // Create selection
  imgObj.select('Custom', 100, 100, 300, 300);
  
  // Pan is available when selection exceeds canvas size
  // User can drag to reposition the crop area
}
```

### Dynamic Selection Based on Image Dimensions

Automatically select based on image size:

```tsx
function intelligentSelect(): void {
  const dimension = imgObj.getImageDimension();
  const width = dimension.width;
  const height = dimension.height;
  
  // Select 80% of image
  const selWidth = width * 0.8;
  const selHeight = height * 0.8;
  const startX = (width - selWidth) / 2;
  const startY = (height - selHeight) / 2;
  
  imgObj.select('Custom', startX, startY, selWidth, selHeight);
}
```

### Crop to Specific Dimensions

Always crop to exact dimensions:

```tsx
function cropToSize(): void {
  const targetWidth = 500;
  const targetHeight = 300;
  
  imgObj.select('Custom', 50, 50, targetWidth, targetHeight);
  imgObj.crop();
  
  // After crop, image will be exactly 500x300 (or close, depending on aspect ratio)
}
```

### Undo Crop Selection

Use undo to revert crop operation:

```tsx
function undoCrop(): void {
  imgObj.undo(); // Reverts the last crop
}
```
