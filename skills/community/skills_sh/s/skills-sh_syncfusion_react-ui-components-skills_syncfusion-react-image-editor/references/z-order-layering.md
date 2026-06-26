# Z-Order and Layering

## Table of Contents

- [Z-Order Operations](#z-order-operations)
- [Layer Management](#layer-management)
- [Stacking Patterns](#stacking-patterns)
- [Advanced Patterns](#advanced-patterns)

## Z-Order Operations

### Bring Forward

Move annotation one layer forward:

```tsx
function bringForward(shapeId: string): void {
  imgObj.bringForward(shapeId);
}

// Usage
const shapes = imgObj.getShapeSettings();
if (shapes.length > 0) {
  bringForward(shapes[0].id);
}
```

### Send Backward

Move annotation one layer backward:

```tsx
function sendBackward(shapeId: string): void {
  imgObj.sendBackward(shapeId);
}

// Usage
const shapes = imgObj.getShapeSettings();
if (shapes.length > 0) {
  sendBackward(shapes[0].id);
}
```

### Bring to Front

Move annotation to topmost layer:

```tsx
function bringToFront(shapeId: string): void {
  imgObj.bringToFront(shapeId);
}

// Usage
const shapes = imgObj.getShapeSettings();
if (shapes.length > 0) {
  bringToFront(shapes[0].id);
}
```

### Send to Back

Move annotation to bottom layer:

```tsx
function sendToBack(shapeId: string): void {
  imgObj.sendToBack(shapeId);
}

// Usage
const shapes = imgObj.getShapeSettings();
if (shapes.length > 0) {
  sendToBack(shapes[0].id);
}
```

## Layer Management

### Get All Shapes

Access all annotations:

```tsx
function getAllShapes(): void {
  const shapes = imgObj.getShapeSettings();
  console.log('Total annotations:', shapes.length);
  
  shapes.forEach((shape, index) => {
    console.log(`Shape ${index}:`, {
      type: shape.type,
      id: shape.id
    });
  });
}
```

### Get Specific Shape

Get a particular shape by ID:

```tsx
function getShapeById(shapeId: string): void {
  const shape = imgObj.getShapeSetting(shapeId);
  if (shape) {
    console.log('Shape details:', {
      type: shape.type,
      id: shape.id
    });
  }
}
```

### Layer Order Display

```tsx
function displayLayerStack(): void {
  const objects = imgObj.getShapeSettings();
  
  console.log('=== Layer Stack ===');
  objects.forEach((obj, index) => {
    console.log(`${index}: ${obj.type}`);
  });
}
```

## Stacking Patterns

### Arrange Multiple Items

Organize stack of annotations:

```tsx
function arrangeStack(): void {
  // Select text first
  const textItem = imgObj.getShapeSettings().find(obj => obj.type === 'Text');
  if (textItem) {
    imgObj.bringToFront(textItem.id);
  }
  
  // Shape behind text
  const shapeItem = imgObj.getShapeSettings().find(obj => obj.type === 'Shape');
  if (shapeItem) {
    imgObj.sendToBack(shapeItem.id);
  }
}
```

### Layer Priority

```tsx
interface LayerPriority {
  name: string;
  type: string;
  priority: number;
}

const layerPriorities: LayerPriority[] = [
  { name: 'Background', type: 'Background', priority: 0 },
  { name: 'Base Shapes', type: 'Shape', priority: 1 },
  { name: 'Images', type: 'Image', priority: 2 },
  { name: 'Text', type: 'Text', priority: 3 },
  { name: 'Overlay', type: 'Freehand', priority: 4 }
];

function organizeByPriority(): void {
  const objects = imgObj.getShapeSettings();
  
  // Sort by priority
  const sorted = objects.sort((a, b) => {
    const priorityA = layerPriorities.find(p => p.type === a.type)?.priority ?? 999;
    const priorityB = layerPriorities.find(p => p.type === b.type)?.priority ?? 999;
    return priorityA - priorityB;
  });
}
```

### Move Between Specific Layers

```tsx
function moveToLayer(itemId: string, targetIndex: number): void {
  const objects = imgObj.getShapeSettings();
  const currentIndex = objects.findIndex(obj => obj.id === itemId);
  
  if (currentIndex < targetIndex) {
    // Move forward
    for (let i = currentIndex; i < targetIndex; i++) {
      imgObj.bringForward(itemId);
    }
  } else if (currentIndex > targetIndex) {
    // Move backward
    for (let i = currentIndex; i > targetIndex; i--) {
      imgObj.sendBackward(itemId);
    }
  }
}

// Usage: Move item to position 2
moveToLayer('shape-1', 2);
```

## Advanced Patterns

### Automatic Layering

```tsx
class LayerManager {
  private layerMap: Map<string, number> = new Map();
  
  addLayer(itemId: string, zIndex: number): void {
    this.layerMap.set(itemId, zIndex);
  }
  
  arrangeAll(): void {
    const sorted = Array.from(this.layerMap.entries())
      .sort((a, b) => a[1] - b[1]);
    
    sorted.forEach(([itemId]) => {
      imgObj.sendToBack(itemId);
    });
  }
  
  moveUp(itemId: string): void {
    imgObj.bringForward(itemId);
  }
  
  moveDown(itemId: string): void {
    imgObj.sendBackward(itemId);
  }
}

const layerManager = new LayerManager();
layerManager.addLayer('text-1', 10);
layerManager.addLayer('shape-1', 5);
layerManager.arrangeAll();
```

### Group Operations

```tsx
interface LayerGroup {
  name: string;
  items: string[];
}

const layerGroups: LayerGroup[] = [
  { name: 'Watermarks', items: ['watermark-1', 'watermark-2'] },
  { name: 'Annotations', items: ['note-1', 'note-2', 'note-3'] },
  { name: 'Highlights', items: ['highlight-1'] }
];

function bringGroupForward(groupName: string): void {
  const group = layerGroups.find(g => g.name === groupName);
  if (group) {
    group.items.forEach(itemId => {
      imgObj.bringForward(itemId);
    });
  }
}

function sendGroupToBack(groupName: string): void {
  const group = layerGroups.find(g => g.name === groupName);
  if (group) {
    group.items.forEach(itemId => {
      imgObj.sendToBack(itemId);
    });
  }
}

// Usage
bringGroupForward('Watermarks');
```

### Layer Visibility Toggle

```tsx
interface LayerVisibility {
  itemId: string;
  visible: boolean;
}

class VisibilityManager {
  private visibilityMap: Map<string, boolean> = new Map();
  
  setVisibility(itemId: string, visible: boolean): void {
    this.visibilityMap.set(itemId, visible);
    this.updateVisibility(itemId, visible);
  }
  
  private updateVisibility(itemId: string, visible: boolean): void {
    // Note: Direct visibility toggle not available in official API
    // Use updateRedact() or shape updates through proper API methods
    this.visibilityMap.set(itemId, visible);
  }
  
  toggleVisibility(itemId: string): void {
    const current = this.visibilityMap.get(itemId) ?? true;
    this.setVisibility(itemId, !current);
  }
}

const visibilityManager = new VisibilityManager();
visibilityManager.setVisibility('watermark-1', false);
visibilityManager.toggleVisibility('watermark-1');
```

### Layer Hierarchy Display

```tsx
function renderLayerPanel(): void {
  const objects = imgObj.getShapeSettings();
  
  const layerHTML = objects
    .map((obj, index) => `
      <div class="layer-item" data-id="${obj.id}">
        <span class="layer-index">${index}</span>
        <span class="layer-type">${obj.type}</span>
        <button onclick="bringToFrontLayer('${obj.id}')">↑</button>
        <button onclick="sendToBackLayer('${obj.id}')">↓</button>
      </div>
    `)
    .join('');
  
  const panel = document.querySelector('.layer-panel');
  if (panel) {
    panel.innerHTML = `<div class="layer-stack">${layerHTML}</div>`;
  }
}

function bringToFrontLayer(itemId: string): void {
  imgObj.bringToFront(itemId);
  renderLayerPanel();
}

function sendToBackLayer(itemId: string): void {
  imgObj.sendToBack(itemId);
  renderLayerPanel();
}
```

### Batch Z-Order Management

```tsx
interface ZOrderConfig {
  itemId: string;
  operation: 'front' | 'back' | 'forward' | 'backward';
}

function batchUpdateZOrder(configs: ZOrderConfig[]): void {
  configs.forEach(config => {
    switch (config.operation) {
      case 'front':
        imgObj.bringToFront(config.itemId);
        break;
      case 'back':
        imgObj.sendToBack(config.itemId);
        break;
      case 'forward':
        imgObj.bringForward(config.itemId);
        break;
      case 'backward':
        imgObj.sendBackward(config.itemId);
        break;
    }
  });
}

// Usage
const orders: ZOrderConfig[] = [
  { itemId: 'text-1', operation: 'front' },
  { itemId: 'shape-1', operation: 'backward' },
  { itemId: 'image-1', operation: 'back' }
];

batchUpdateZOrder(orders);
```

### Lock Layer Order

```tsx
class LockedLayerManager {
  private lockedOrder: string[] = [];
  
  lockCurrentOrder(): void {
    const objects = imgObj.getShapeSettings();
    this.lockedOrder = objects.map(obj => obj.id);
  }
  
  restoreLockedOrder(): void {
    this.lockedOrder.forEach((itemId, targetIndex) => {
      const objects = imgObj.getShapeSettings();
      const currentIndex = objects.findIndex(obj => obj.id === itemId);
      
      if (currentIndex !== targetIndex) {
        if (currentIndex < targetIndex) {
          for (let i = 0; i < (targetIndex - currentIndex); i++) {
            imgObj.bringForward(itemId);
          }
        } else {
          for (let i = 0; i < (currentIndex - targetIndex); i++) {
            imgObj.sendBackward(itemId);
          }
        }
      }
    });
  }
}

const lockedManager = new LockedLayerManager();
lockedManager.lockCurrentOrder();
// ... user makes changes ...
lockedManager.restoreLockedOrder();
```

### Smart Layering

```tsx
function smartLayerArrangement(): void {
  const objects = imgObj.getShapeSettings();
  
  // Categorize objects
  const categories = {
    text: objects.filter(obj => obj.type === 'Text'),
    shapes: objects.filter(obj => obj.type === 'Shape'),
    images: objects.filter(obj => obj.type === 'Image'),
    freehand: objects.filter(obj => obj.type === 'Freehand')
  };
  
  // Arrange by category: backgrounds bottom, text top
  const order = [
    ...categories.images,
    ...categories.shapes,
    ...categories.freehand,
    ...categories.text
  ];
  
  order.forEach((obj, index) => {
    if (index === order.length - 1) {
      imgObj.bringToFront(obj.id);
    } else {
      imgObj.sendToBack(obj.id);
    }
  });
}
```
