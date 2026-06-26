# Freehand Drawing

## Table of Contents
- [Enable Freehand Drawing](#enable-freehand-drawing)
- [Stroke Customization](#stroke-customization)
- [Managing Drawings](#managing-drawings)
- [Drawing Events](#drawing-events)

## Enable Freehand Drawing

### Start Drawing

Enable freehand drawing mode:

```tsx
function startDrawing(): void {
  imgObj.freeHandDraw(true);
}
```

### Stop Drawing

Disable freehand drawing mode:

```tsx
function stopDrawing(): void {
  imgObj.freeHandDraw(false);
}
```

### Toggle Drawing Mode

Switch drawing on/off:

```tsx
let drawingEnabled = false;

function toggleDrawing(): void {
  drawingEnabled = !drawingEnabled;
  imgObj.freeHandDraw(drawingEnabled);
}
```

## Stroke Customization

### Customize Stroke via Event

Modify stroke properties when drawing:

```tsx
function shapeChanging(args: any): void {
  if (args.currentShapeSettings.type === 'FreehandDraw') {
    args.currentShapeSettings.strokeColor = 'red';
    args.currentShapeSettings.strokeWidth = 5;
  }
}

<ImageEditorComponent shapeChanging={shapeChanging} />
```

### Change Stroke Color

Set custom stroke color for drawings:

```tsx
function drawWithRedStroke(): void {
  const customStroke = { strokeColor: 'red' };
  
  function shapeChanging(args: any): void {
    if (args.currentShapeSettings.type === 'FreehandDraw') {
      args.currentShapeSettings.strokeColor = customStroke.strokeColor;
    }
  }
  
  imgObj.freeHandDraw(true);
}
```

### Change Stroke Width

Adjust line thickness:

```tsx
let strokeWidth = 2;

function increaseStroke(): void {
  strokeWidth += 1;
}

function decreaseStroke(): void {
  if (strokeWidth > 1) {
    strokeWidth -= 1;
  }
}

function applyStroke(): void {
  function shapeChanging(args: any): void {
    if (args.currentShapeSettings.type === 'FreehandDraw') {
      args.currentShapeSettings.strokeWidth = strokeWidth;
    }
  }
}
```

### Multiple Stroke Presets

Offer predefined stroke styles:

```tsx
const strokePresets = {
  thin: { color: 'black', width: 1 },
  normal: { color: 'black', width: 3 },
  bold: { color: 'black', width: 5 },
  highlight: { color: 'yellow', width: 8 }
};

function applyStrokePreset(preset: string): void {
  const style = strokePresets[preset];
  
  function shapeChanging(args: any): void {
    if (args.currentShapeSettings.type === 'FreehandDraw') {
      args.currentShapeSettings.strokeColor = style.color;
      args.currentShapeSettings.strokeWidth = style.width;
    }
  }
  
  imgObj.freeHandDraw(true);
}
```

## Managing Drawings

### Get All Drawings

Retrieve all freehand drawing annotations:

```tsx
function getAllDrawings(): void {
  const shapes = imgObj.getShapeSettings();
  const drawings = shapes.filter(s => s.type === 'FreehandDraw');
  console.log('Freehand drawings:', drawings);
}
```

### Delete Drawing

Remove freehand annotation by shape ID:

```tsx
function deleteDrawing(): void {
  imgObj.deleteShape('pen_1');
}
```

### Delete Last Drawing

Remove the most recently added drawing:

```tsx
function deleteLastDrawing(): void {
  const shapes = imgObj.getShapeSettings();
  if (shapes.length > 0) {
    const lastDrawing = shapes[shapes.length - 1];
    if (lastDrawing.type === 'FreehandDraw') {
      imgObj.deleteShape(lastDrawing.id);
    }
  }
}
```

### Clear All Drawings

Delete all freehand annotations:

```tsx
function clearAllDrawings(): void {
  const shapes = imgObj.getShapeSettings();
  shapes
    .filter(s => s.type === 'FreehandDraw')
    .forEach(s => imgObj.deleteShape(s.id));
}
```

### Select Specific Drawing

Highlight a drawing for editing:

```tsx
function selectDrawing(drawingId: string): void {
  const shapes = imgObj.getShapeSettings();
  const drawing = shapes.find(s => s.id === drawingId);
  if (drawing) {
    drawing.isSelected = true;
    imgObj.updateShape(drawing);
  }
}
```

## Drawing Events

### Shape Changing Event

React to drawing modifications:

```tsx
function shapeChanging(args: any): void {
  if (args.currentShapeSettings.type === 'FreehandDraw') {
    console.log('Drawing stroke color:', args.currentShapeSettings.strokeColor);
    console.log('Drawing stroke width:', args.currentShapeSettings.strokeWidth);
  }
}

<ImageEditorComponent shapeChanging={shapeChanging} />
```

### Track Drawing Count

Monitor number of active drawings:

```tsx
let drawingCount = 0;

function shapeChanging(args: any): void {
  if (args.currentShapeSettings.type === 'FreehandDraw' && args.action === 'insert') {
    drawingCount++;
    console.log(`Drawing #${drawingCount} created`);
  }
}
```

## Advanced Patterns

### Artistic Styles

Apply different artistic styles to drawings:

```tsx
const artisticStyles = {
  sketch: { color: '#444', width: 2, opacity: 0.7 },
  marker: { color: '#FF6B6B', width: 6, opacity: 0.8 },
  pen: { color: '#000', width: 1, opacity: 1 }
};

function applyArtisticStyle(style: string): void {
  const styleConfig = artisticStyles[style];
  
  function shapeChanging(args: any): void {
    if (args.currentShapeSettings.type === 'FreehandDraw') {
      args.currentShapeSettings.strokeColor = styleConfig.color;
      args.currentShapeSettings.strokeWidth = styleConfig.width;
    }
  }
  
  imgObj.freeHandDraw(true);
}
```

### Annotate and Markup Workflow

Combined drawing and text annotation:

```tsx
function markupImage(): void {
  // Add text label
  const dimension = imgObj.getImageDimension();
  imgObj.drawText(dimension.x + 20, dimension.y + 20, 'Review:');
  
  // Enable drawing for marks
  imgObj.freeHandDraw(true);
}

function completeMarkup(): void {
  imgObj.freeHandDraw(false);
  
  // Get all annotations
  const shapes = imgObj.getShapeSettings();
  console.log('Marked up image with', shapes.length, 'annotations');
}
```

### Drawing History

Track drawings in undo/redo stack:

```tsx
function undoLastDrawing(): void {
  imgObj.undo(); // Undo last drawing
}

function redoLastDrawing(): void {
  imgObj.redo(); // Redo last drawing
}
```

### Conditional Drawing

Allow drawing only under certain conditions:

```tsx
let allowDrawing = false;

function enableDrawingMode(): void {
  allowDrawing = true;
  imgObj.freeHandDraw(true);
}

function disableDrawingMode(): void {
  allowDrawing = false;
  imgObj.freeHandDraw(false);
}

function shapeChanging(args: any): void {
  if (!allowDrawing && args.currentShapeSettings.type === 'FreehandDraw') {
    args.cancel = true;
  }
}
```

### Export Drawings as Data

Save drawing data for later use:

```tsx
function exportDrawings(): void {
  const shapes = imgObj.getShapeSettings();
  const drawings = shapes
    .filter(s => s.type === 'FreehandDraw')
    .map(d => ({
      id: d.id,
      stroke: d.strokeColor,
      width: d.strokeWidth
    }));
  
  const json = JSON.stringify(drawings);
  localStorage.setItem('drawings', json);
}

function importDrawings(): void {
  const json = localStorage.getItem('drawings');
  if (json) {
    const drawings = JSON.parse(json);
    console.log('Available drawings:', drawings);
  }
}
```

### Drawing Constraints

Limit drawing to specific areas:

```tsx
let drawingArea = { x: 50, y: 50, width: 400, height: 300 };

function shapeChanging(args: any): void {
  if (args.currentShapeSettings.type === 'FreehandDraw') {
    // Check if drawing is within bounds
    const shape = args.currentShapeSettings;
    if (shape.x! < drawingArea.x || shape.x! > drawingArea.x + drawingArea.width) {
      args.cancel = true;
    }
  }
}
```
