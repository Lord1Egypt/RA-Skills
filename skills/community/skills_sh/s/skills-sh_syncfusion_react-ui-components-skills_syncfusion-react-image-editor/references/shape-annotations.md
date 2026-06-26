# Shape Annotations

## Table of Contents
- [Drawing Shapes](#drawing-shapes)
- [Shape Properties](#shape-properties)
- [Managing Shapes](#managing-shapes)
- [Customization Events](#customization-events)

## Drawing Shapes

### Draw Rectangle

Add rectangular annotation:

```tsx
function drawRectangle(): void {
  const dimension = imgObj.getImageDimension();
  imgObj.drawRectangle(
    dimension.x + 10,      // x
    dimension.y + 60,      // y
    150,                   // width
    70                     // height
  );
}
```

### Draw Ellipse

Add elliptical annotation:

```tsx
function drawEllipse(): void {
  const dimension = imgObj.getImageDimension();
  imgObj.drawEllipse(
    dimension.x + 100,     // center x
    dimension.y + 100,     // center y
    80,                    // radiusX
    50                     // radiusY
  );
}
```

### Draw Line

Add line annotation:

```tsx
function drawLine(): void {
  const dimension = imgObj.getImageDimension();
  imgObj.drawLine(
    dimension.x + 50,      // startX
    dimension.y + 50,      // startY
    dimension.x + 300,     // endX
    dimension.y + 150      // endY
  );
}
```

### Draw Arrow

Add arrow annotation with direction:

```tsx
function drawArrow(): void {
  const dimension = imgObj.getImageDimension();
  imgObj.drawArrow(
    dimension.x + 100,     // startX
    dimension.y + 100,     // startY
    dimension.x + 300,     // endX
    dimension.y + 200,     // endY
    2,                     // strokeWidth
    'black',               // strokeColor
    ArrowheadType.None,    // arrowStart
    ArrowheadType.SolidArrow // arrowEnd
  );
}
```

### Draw Path

Add complex path annotation:

```tsx
function drawPath(): void {
  const dimension = imgObj.getImageDimension();
  const points = [
    { x: dimension.x, y: dimension.y },
    { x: dimension.x + 50, y: dimension.y + 50 },
    { x: dimension.x + 100, y: dimension.y + 20 },
    { x: dimension.x + 150, y: dimension.y + 80 }
  ];
  
  imgObj.drawPath(points, 5, 'blue');
}
```

## Shape Properties

### Rectangle with Stroke and Fill

Customize rectangle appearance:

```tsx
function customRectangle(): void {
  const dimension = imgObj.getImageDimension();
  imgObj.drawRectangle(
    dimension.x + 10,
    dimension.y + 60,
    150,
    70,
    2,                     // strokeWidth
    'red',                 // strokeColor
    'yellow',              // fillColor
    0,                     // degree
    false,                 // isSelected
    8                      // borderRadius
  );
}
```

### Ellipse with Custom Stroke

Customize ellipse styling:

```tsx
function styledEllipse(): void {
  const dimension = imgObj.getImageDimension();
  imgObj.drawEllipse(
    dimension.x + 100,
    dimension.y + 100,
    80,
    50,
    3,                     // strokeWidth
    'green',               // strokeColor
    'lightgreen',          // fillColor
    0,                     // degree
    false                  // isSelected
  );
}
```

### Rotated Shape

Rotate shape by degree:

```tsx
function rotatedRectangle(): void {
  const dimension = imgObj.getImageDimension();
  imgObj.drawRectangle(
    dimension.x + 100,
    dimension.y + 100,
    100,
    50,
    2,
    'black',
    'transparent',
    45                     // Rotate 45 degrees
  );
}
```

### Arrow Head Types

Different arrow variations:

```tsx
import { ArrowheadType } from '@syncfusion/ej2-react-image-editor';

function differentArrows(): void {
  const dimension = imgObj.getImageDimension();
  
  // Arrow with solid head at end only
  imgObj.drawArrow(50, 50, 150, 50, 2, 'black', ArrowheadType.None, ArrowheadType.SolidArrow);
  
  // Arrow with no heads
  imgObj.drawArrow(50, 100, 150, 100, 2, 'blue', ArrowheadType.None, ArrowheadType.None);
  
  // Double arrow (heads at both ends)
  imgObj.drawArrow(50, 150, 150, 150, 2, 'red', ArrowheadType.SolidArrow, ArrowheadType.SolidArrow);
}
```

## Managing Shapes

### Get All Shapes

Retrieve all shape annotations:

```tsx
function getAllShapes(): void {
  const shapes = imgObj.getShapeSettings();
  const shapeTypes = shapes.map(s => s.type);
  console.log('Shape types:', shapeTypes);
}
```

### Delete Shape

Remove shape by ID:

```tsx
function deleteShape(): void {
  imgObj.deleteShape('shape_1');
}
```

### Delete Multiple Shapes

Remove all shapes of specific type:

```tsx
function deleteAllShapesOfType(shapeType: string): void {
  const shapes = imgObj.getShapeSettings();
  shapes
    .filter(s => s.type === shapeType)
    .forEach(s => imgObj.deleteShape(s.id));
}

// Usage: Delete all rectangles
deleteAllShapesOfType('Rectangle');
```

### Update Shape

Modify existing shape properties:

```tsx
function updateShapeColor(): void {
  const shapes = imgObj.getShapeSettings();
  if (shapes && shapes.length > 0) {
    const shape = shapes[0];
    shape.strokeColor = 'purple';
    imgObj.updateShape(shape);
  }
}
```

### Select Shape

Highlight shape for editing:

```tsx
function selectShapeById(shapeId: string): void {
  imgObj.selectShape(shapeId);
}

// Usage
const shapes = imgObj.getShapeSettings();
if (shapes && shapes.length > 0) {
  selectShapeById(shapes[0].id);
}
```

## Customization Events

### Customize Default Stroke Colors

Apply custom defaults via event:

```tsx
let changeColor = true;

function shapeChanging(args: any): void {
  if (changeColor && args.action === 'insert' && args.currentShapeSettings.type === 'Rectangle') {
    args.currentShapeSettings.strokeColor = 'red';
    args.currentShapeSettings.fillColor = 'lightyellow';
    changeColor = false;
  }
}

<ImageEditorComponent shapeChanging={shapeChanging} />
```

### Prevent Specific Shapes

Block certain shape types:

```tsx
function shapeChanging(args: any): void {
  if (args.currentShapeSettings.type === 'Arrow' && args.action === 'insert') {
    args.cancel = true;
    console.log('Arrows not allowed');
  }
}
```

## Advanced Patterns

### Annotate Regions

Highlight important areas with rectangles:

```tsx
function highlightRegions(): void {
  // Region 1
  imgObj.drawRectangle(50, 50, 150, 100, 2, 'red', 'transparent');
  
  // Region 2
  imgObj.drawRectangle(200, 150, 150, 100, 2, 'green', 'transparent');
  
  // Region 3
  imgObj.drawRectangle(350, 50, 150, 100, 2, 'blue', 'transparent');
}
```

### Create Measurement Lines

Draw lines for distance indication:

```tsx
function drawMeasurementLines(): void {
  const dim = imgObj.getImageDimension();
  
  // Horizontal measurement
  imgObj.drawLine(dim.x, dim.y + 100, dim.x + 200, dim.y + 100, 2, 'black');
  imgObj.drawLine(dim.x, dim.y + 95, dim.x, dim.y + 105, 2, 'black');
  imgObj.drawLine(dim.x + 200, dim.y + 95, dim.x + 200, dim.y + 105, 2, 'black');
}
```

### Draw Grid Pattern

Create overlay grid:

```tsx
function drawGrid(): void {
  const dim = imgObj.getImageDimension();
  const gridSize = 50;
  
  for (let x = 0; x < dim.width; x += gridSize) {
    imgObj.drawLine(dim.x + x, dim.y, dim.x + x, dim.y + dim.height, 1, '#CCC');
  }
  
  for (let y = 0; y < dim.height; y += gridSize) {
    imgObj.drawLine(dim.x, dim.y + y, dim.x + dim.width, dim.y + y, 1, '#CCC');
  }
}
```

### Flowchart Elements

Build diagram shapes:

```tsx
function createFlowchart(): void {
  const dim = imgObj.getImageDimension();
  
  // Start
  imgObj.drawEllipse(dim.x + 200, dim.y + 50, 40, 30, 2, 'black', 'green');
  
  // Process
  imgObj.drawRectangle(dim.x + 150, dim.y + 150, 100, 60, 2, 'black', 'lightblue');
  
  // Decision
  imgObj.drawPath([
    { x: dim.x + 200, y: dim.y + 300 },
    { x: dim.x + 250, y: dim.y + 350 },
    { x: dim.x + 200, y: dim.y + 400 },
    { x: dim.x + 150, y: dim.y + 350 }
  ], 2, 'black');
}
```

### Shape History Tracking

Monitor shape creation:

```tsx
let shapeHistory: any[] = [];

function shapeChanging(args: any): void {
  if (args.action === 'insert') {
    shapeHistory.push({
      type: args.currentShapeSettings.type,
      timestamp: new Date(),
      id: args.currentShapeSettings.id
    });
  }
}

function undoLastShape(): void {
  imgObj.undo();
  shapeHistory.pop();
}
```

### Batch Drawing

Draw multiple related shapes:

```tsx
function batchDraw(shapes: any[]): void {
  shapes.forEach(shape => {
    if (shape.type === 'rectangle') {
      imgObj.drawRectangle(shape.x, shape.y, shape.w, shape.h, shape.stroke);
    } else if (shape.type === 'ellipse') {
      imgObj.drawEllipse(shape.x, shape.y, shape.rx, shape.ry, shape.stroke);
    }
  });
}

const diagramShapes = [
  { type: 'rectangle', x: 50, y: 50, w: 100, h: 80, stroke: 2 },
  { type: 'ellipse', x: 200, y: 100, rx: 40, ry: 30, stroke: 2 }
];

batchDraw(diagramShapes);
```
