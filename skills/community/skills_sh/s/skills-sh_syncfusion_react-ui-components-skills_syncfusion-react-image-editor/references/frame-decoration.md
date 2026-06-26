# Frame Decoration

## Table of Contents

- [Frame Types](#frame-types)
- [Apply Frame](#apply-frame)
- [Frame Customization](#frame-customization)
- [Frame Events](#frame-events)
- [Advanced Patterns](#advanced-patterns)

## Frame Types

The Image Editor supports 5 frame types:

| Frame Type | Description | Use Case |
|-----------|-------------|----------|
| Mat | Solid border with inner bevel | Professional photos |
| Bevel | 3D beveled border | Formal documents |
| Line | Simple line border | Minimalist design |
| Inset | Pressed/embedded appearance | Classic photos |
| Hook | Decorative hook-style frame | Artistic images |

## Apply Frame

### Mat Frame

Classic solid border:

```tsx
import { FrameType } from '@syncfusion/ej2-react-image-editor';

function applyMatFrame(): void {
  imgObj.drawFrame(
    FrameType.Mat,
    '#CCCCCC', // Color
    '',        // gradientColor
    20         // size as percentage
  );
}
```

### Bevel Frame

3D beveled effect:

```tsx
import { FrameType } from '@syncfusion/ej2-react-image-editor';

function applyBevelFrame(): void {
  imgObj.drawFrame(
    FrameType.Bevel,
    '#999999',
    '',
    15
  );
}
```

### Line Frame

Simple border:

```tsx
import { FrameType } from '@syncfusion/ej2-react-image-editor';

function applyLineFrame(): void {
  imgObj.drawFrame(
    FrameType.Line,
    '#000000',
    '',
    10
  );
}
```

### Inset Frame

Embedded appearance:

```tsx
import { FrameType } from '@syncfusion/ej2-react-image-editor';

function applyInsetFrame(): void {
  imgObj.drawFrame(
    FrameType.Inset,
    '#666666',
    '',
    15
  );
}
```

### Hook Frame

Decorative frame:

```tsx
import { FrameType } from '@syncfusion/ej2-react-image-editor';

function applyHookFrame(): void {
  imgObj.drawFrame(
    FrameType.Hook,
    '#8B7355',
    '',
    20
  );
}
```

## Frame Customization

### Custom Frame Width

Control frame thickness:

```tsx
function applyCustomFrame(frameType: FrameType, width: number, color: string): void {
  imgObj.drawFrame(frameType, color, '', width);
}

// Thin frame
applyCustomFrame(FrameType.Mat, 10, '#CCCCCC');

// Thick frame
applyCustomFrame(FrameType.Bevel, 80, '#999999');

// Extra thick frame
applyCustomFrame(FrameType.Hook, 100, '#8B7355');
```

### Custom Frame Color

Select frame color:

```tsx
const frameColors = {
  light: '#EEEEEE',
  medium: '#CCCCCC',
  dark: '#666666',
  gold: '#FFD700',
  silver: '#C0C0C0',
  wood: '#8B4513'
};

function applyColoredFrame(colorName: keyof typeof frameColors): void {
  imgObj.drawFrame(
    FrameType.Mat,
    frameColors[colorName],
    '',
    40
  );
}

// Apply gold frame
applyColoredFrame('gold');
```

### Dynamic Frame Properties

```tsx
interface FrameConfig {
  type: FrameType;
  width: number;
  color: string;
}

function applyDynamicFrame(config: FrameConfig): void {
  imgObj.drawFrame(config.type, config.width, config.color);
}

// Usage
const config: FrameConfig = {
  type: FrameType.Bevel,
  width: 50,
  color: '#C0C0C0'
};

applyDynamicFrame(config);
```

## Frame Events

### Capturing Frame Events

```tsx
const handleFrameDrawing = (args: any): void => {
  console.log('Frame applied:', {
    type: args.frameType,
    width: args.width,
    color: args.color
  });
};

const imageEditor = (
  <ImageEditorComponent
    onFrameChange={handleFrameDrawing}
  />
);
```

### Before Frame Application

```tsx
const handleBeforeFrame = (args: any): void => {
  // Validate or modify frame before applying
  if (args.width > 100) {
    console.warn('Frame width exceeds maximum');
    args.cancel = true;
  }
};
```

## Advanced Patterns

### Frame Presets

```tsx
interface FramePreset {
  name: string;
  type: FrameType;
  width: number;
  color: string;
}

const framePresets: FramePreset[] = [
  {
    name: 'Classic',
    type: FrameType.Mat,
    width: 30,
    color: '#8B8B8B'
  },
  {
    name: 'Elegant',
    type: FrameType.Bevel,
    width: 40,
    color: '#C0C0C0'
  },
  {
    name: 'Modern',
    type: FrameType.Line,
    width: 10,
    color: '#000000'
  },
  {
    name: 'Vintage',
    type: FrameType.Hook,
    width: 50,
    color: '#8B7355'
  },
  {
    name: 'Minimal',
    type: FrameType.Line,
    width: 5,
    color: '#CCCCCC'
  }
];

function applyFramePreset(presetName: string): void {
  const preset = framePresets.find(p => p.name === presetName);
  if (preset) {
    imgObj.drawFrame(preset.type, preset.color, '', preset.width);
  }
}

// Usage
applyFramePreset('Elegant');
```

### Frame by Use Case

```tsx
enum ImageCategory {
  Portrait = 'portrait',
  Landscape = 'landscape',
  Square = 'square',
  Document = 'document'
}

function getAppropriateFrame(category: ImageCategory): FramePreset {
  const frameMap: { [key in ImageCategory]: FramePreset } = {
    [ImageCategory.Portrait]: {
      name: 'Portrait',
      type: FrameType.Bevel,
      width: 35,
      color: '#8B7355'
    },
    [ImageCategory.Landscape]: {
      name: 'Landscape',
      type: FrameType.Mat,
      width: 30,
      color: '#C0C0C0'
    },
    [ImageCategory.Square]: {
      name: 'Square',
      type: FrameType.Hook,
      width: 40,
      color: '#FFD700'
    },
    [ImageCategory.Document]: {
      name: 'Document',
      type: FrameType.Line,
      width: 10,
      color: '#000000'
    }
  };
  
  return frameMap[category];
}

function autoSelectFrame(): void {
  const dim = imgObj.getImageDimension();
  let category: ImageCategory;
  
  if (dim.width > dim.height) {
    category = ImageCategory.Landscape;
  } else if (dim.height > dim.width) {
    category = ImageCategory.Portrait;
  } else {
    category = ImageCategory.Square;
  }
  
  const frame = getAppropriateFrame(category);
  imgObj.drawFrame(frame.type, frame.width, frame.color);
}
```

### Responsive Frame Width

Adjust frame based on image size:

```tsx
function applyResponsiveFrame(baseWidth: number): void {
  const dim = imgObj.getImageDimension();
  
  // Scale frame width proportionally to image size
  const scale = Math.min(dim.width, dim.height) / 1000;
  const scaledWidth = Math.round(baseWidth * scale);
  
  imgObj.drawFrame(FrameType.Mat, '#CCCCCC', '', scaledWidth);
}

// Frame scales with image size
applyResponsiveFrame(50);
```

### Frame with Color Palette

```tsx
interface ColorPalette {
  light: string;
  medium: string;
  dark: string;
  accent: string;
}

const palettes: { [key: string]: ColorPalette } = {
  warm: {
    light: '#FFE4C4',
    medium: '#D2691E',
    dark: '#8B4513',
    accent: '#FF8C00'
  },
  cool: {
    light: '#ADD8E6',
    medium: '#4682B4',
    dark: '#191970',
    accent: '#00CED1'
  },
  neutral: {
    light: '#E8E8E8',
    medium: '#808080',
    dark: '#2F2F2F',
    accent: '#C0C0C0'
  }
};

function applyPaletteFrame(paletteName: string, toneLevel: 'light' | 'medium' | 'dark'): void {
  const palette = palettes[paletteName];
  if (palette) {
    imgObj.drawFrame(FrameType.Mat, palette[toneLevel], '', 35);
  }
}

// Usage
applyPaletteFrame('warm', 'dark');
```

### Frame Combination

```tsx
function applyDoubleFrame(): void {
  // Apply outer frame
  imgObj.drawFrame(FrameType.Bevel, '#8B7355', '', 40);
  
  // Inner frame effect would require additional processing
}

function applyStyledFrame(thickness: number, style: 'solid' | 'decorative' | 'modern'): void {
  const styleConfig = {
    solid: { type: FrameType.Mat, color: '#808080' },
    decorative: { type: FrameType.Hook, color: '#8B7355' },
    modern: { type: FrameType.Line, color: '#000000' }
  };
  
  const config = styleConfig[style];
  imgObj.drawFrame(config.type, thickness, config.color);
}

// Usage
applyStyledFrame(30, 'decorative');
```

### Frame Styles by Context

```tsx
interface FrameContext {
  purpose: 'web' | 'print' | 'social' | 'gallery';
  mood: 'professional' | 'casual' | 'artistic' | 'vintage';
}

function selectFrameByContext(context: FrameContext): void {
  const contextFrames: { [key: string]: FramePreset } = {
    'web-professional': {
      name: 'Web Pro',
      type: FrameType.Line,
      width: 5,
      color: '#000000'
    },
    'print-artistic': {
      name: 'Print Art',
      type: FrameType.Hook,
      width: 60,
      color: '#8B7355'
    },
    'social-casual': {
      name: 'Social',
      type: FrameType.Mat,
      width: 20,
      color: '#FFD700'
    },
    'gallery-vintage': {
      name: 'Gallery',
      type: FrameType.Bevel,
      width: 50,
      color: '#CD853F'
    }
  };
  
  const key = `${context.purpose}-${context.mood}`;
  const frame = contextFrames[key];
  
  if (frame) {
    imgObj.drawFrame(frame.type, frame.width, frame.color);
  }
}

// Usage
selectFrameByContext({
  purpose: 'print',
  mood: 'artistic'
});
```

### Frame Undo/Redo Integration

```tsx
let appliedFrames: FramePreset[] = [];

function applyFrameWithHistory(preset: FramePreset): void {
  appliedFrames.push(preset);
  imgObj.drawFrame(preset.type, preset.width, preset.color);
}

function undoFrame(): void {
  if (appliedFrames.length > 0) {
    appliedFrames.pop();
    imgObj.undo();
  }
}

function redoFrame(): void {
  if (appliedFrames.length > 0) {
    const frame = appliedFrames[appliedFrames.length - 1];
    imgObj.drawFrame(frame.type, frame.width, frame.color);
  }
}
```
