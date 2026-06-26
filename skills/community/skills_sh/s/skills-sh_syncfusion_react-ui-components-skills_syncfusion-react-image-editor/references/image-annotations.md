# Image Annotations

## Adding Image Annotations

### Basic Image Annotation

Insert an image as annotation:

```tsx
function addImage(): void {
  const dimension = imgObj.getImageDimension();
  imgObj.drawImage(
    'https://ej2.syncfusion.com/react/documentation/image-editor/images/flower.jpeg',
    dimension.x,
    dimension.y,
    100,      // width
    80        // height
  );
}
```

### Image with Aspect Ratio

Maintain aspect ratio when adding image:

```tsx
function addImageWithAspectRatio(): void {
  const dimension = imgObj.getImageDimension();
  imgObj.drawImage(
    'https://example.com/logo.png',
    dimension.x + 50,
    dimension.y + 50,
    100,
    80,
    true      // isAspectRatio - maintains aspect ratio
  );
}
```

### Rotated Image Annotation

Add image rotated by degrees:

```tsx
function addRotatedImage(): void {
  const dimension = imgObj.getImageDimension();
  imgObj.drawImage(
    'https://example.com/icon.png',
    dimension.x + 100,
    dimension.y + 100,
    80,
    80,
    true,     // aspect ratio
    45        // degree rotation
  );
}
```

### Image with Opacity

Add semi-transparent image:

```tsx
function addTransparentImage(): void {
  const dimension = imgObj.getImageDimension();
  imgObj.drawImage(
    'https://example.com/watermark.png',
    dimension.x,
    dimension.y,
    150,
    100,
    true,
    0,
    0.5       // opacity (0-1, where 0.5 is 50% transparent)
  );
}
```

### Image as Selected Annotation

Add image in selected state:

```tsx
function addSelectedImage(): void {
  const dimension = imgObj.getImageDimension();
  imgObj.drawImage(
    'https://example.com/image.jpg',
    dimension.x,
    dimension.y,
    100,
    100,
    true,
    0,
    1,
    true      // isSelected - shows selection handles
  );
}
```

## Image Watermarks

### Add Watermark Logo

Place watermark at specific location:

```tsx
function addWatermark(): void {
  const dimension = imgObj.getImageDimension();
  imgObj.drawImage(
    'https://example.com/company-logo.png',
    dimension.x + dimension.width - 120,
    dimension.y + dimension.height - 80,
    100,
    60,
    true,
    0,
    0.6  // Semi-transparent watermark
  );
}
```

### Center Watermark

Center watermark on image:

```tsx
function addCenterWatermark(): void {
  const dimension = imgObj.getImageDimension();
  const centerX = dimension.x + dimension.width / 2 - 50;
  const centerY = dimension.y + dimension.height / 2 - 40;
  
  imgObj.drawImage(
    'https://example.com/watermark.png',
    centerX,
    centerY,
    100,
    80,
    true,
    0,
    0.4
  );
}
```

### Copyright Badge

Add copyright image in corner:

```tsx
function addCopyrightBadge(): void {
  const dimension = imgObj.getImageDimension();
  imgObj.drawImage(
    'https://example.com/copyright-badge.png',
    dimension.x + 10,
    dimension.y + dimension.height - 50,
    40,
    40,
    true,
    0,
    0.8
  );
}
```

## Managing Image Annotations

### Get All Image Annotations

Retrieve all image annotations:

```tsx
function getAllImages(): void {
  const shapes = imgObj.getShapeSettings();
  const images = shapes.filter(s => s.type === 'Image');
  console.log('Image annotations:', images);
}
```

### Delete Image Annotation

Remove image by shape ID:

```tsx
function deleteImage(shapeId: string): void {
  imgObj.deleteShape(shapeId);
}

// Usage
const shapes = imgObj.getShapeSettings();
if (shapes.length > 0) {
  deleteImage(shapes[0].id);
}
```

### Delete All Images

Remove all image annotations:

```tsx
function deleteAllImages(): void {
  const shapes = imgObj.getShapeSettings();
  shapes
    .filter(s => s.type === 'Image')
    .forEach(s => imgObj.deleteShape(s.id));
}
```

### Update Image Properties

Modify existing image annotation:

```tsx
function updateImageOpacity(shapeId: string, opacity: number): void {
  const shapes = imgObj.getShapeSettings();
  const imageShape = shapes.find(s => s.id === shapeId && s.type === 'Image');
  
  if (imageShape) {
    imageShape.opacity = opacity;
    imgObj.updateShape(imageShape);
  }
}

// Usage
updateImageOpacity('shape_1', 0.3);
```

## Advanced Patterns

### Multiple Watermarks

Layer multiple watermarks:

```tsx
function addMultipleWatermarks(): void {
  const dimension = imgObj.getImageDimension();
  
  // Top-left logo
  imgObj.drawImage(
    'https://example.com/logo1.png',
    dimension.x + 10,
    dimension.y + 10,
    80,
    60,
    true,
    0,
    0.5
  );
  
  // Bottom-right watermark
  imgObj.drawImage(
    'https://example.com/watermark.png',
    dimension.x + dimension.width - 110,
    dimension.y + dimension.height - 70,
    100,
    60,
    true,
    0,
    0.4
  );
  
  // Center watermark
  imgObj.drawImage(
    'https://example.com/center-mark.png',
    dimension.x + dimension.width / 2 - 50,
    dimension.y + dimension.height / 2 - 40,
    100,
    80,
    true,
    0,
    0.2
  );
}
```

### Branded Overlay

Add branded image overlay:

```tsx
function addBrandedOverlay(): void {
  const dimension = imgObj.getImageDimension();
  
  // Brand bar
  imgObj.drawRectangle(
    dimension.x,
    dimension.y,
    dimension.width,
    60,
    0,
    'transparent',
    '#F0F0F0'
  );
  
  // Brand logo
  imgObj.drawImage(
    'https://example.com/brand-logo.png',
    dimension.x + 10,
    dimension.y + 10,
    40,
    40,
    true
  );
}
```

### Rotated Logo Annotation

Combine rotation with positioning:

```tsx
function addRotatedLogo(): void {
  const dimension = imgObj.getImageDimension();
  
  imgObj.drawImage(
    'https://example.com/logo.png',
    dimension.x + dimension.width / 2,
    dimension.y + dimension.height / 2,
    120,
    120,
    true,
    45,  // 45-degree rotation
    0.6
  );
}
```

### Icon Annotation

Small icon with label:

```tsx
function addIconWithLabel(): void {
  const dimension = imgObj.getImageDimension();
  
  // Icon
  imgObj.drawImage(
    'https://example.com/icon.png',
    dimension.x + 200,
    dimension.y + 100,
    40,
    40,
    true
  );
  
  // Text label
  imgObj.drawText(
    dimension.x + 250,
    dimension.y + 110,
    'Featured',
    'Arial',
    12
  );
}
```

### Thumbnail Annotation

Add thumbnail image for reference:

```tsx
function addThumbnail(): void {
  const dimension = imgObj.getImageDimension();
  
  imgObj.drawRectangle(
    dimension.x + dimension.width - 110,
    dimension.y + 10,
    100,
    75,
    2,
    'black',
    'white'
  );
  
  imgObj.drawImage(
    'https://example.com/thumbnail.jpg',
    dimension.x + dimension.width - 105,
    dimension.y + 15,
    90,
    65,
    true
  );
}
```

### Duplicate Image Annotation

Clone existing image:

```tsx
function duplicateImage(shapeId: string): void {
  const shapes = imgObj.getShapeSettings();
  const original = shapes.find(s => s.id === shapeId && s.type === 'Image');
  
  if (original) {
    // Create a copy offset from the original
    imgObj.drawImage(
      original.src || '',
      (original.x || 0) + 20,
      (original.y || 0) + 20,
      original.width || 100,
      original.height || 100,
      true,
      original.degree || 0,
      original.opacity || 1
    );
  }
}
```

### Scale Image Annotation

Resize existing image:

```tsx
function scaleImage(shapeId: string, factor: number): void {
  // Use updateShape to modify image dimensions
  // Get current shape first
  const shape = imgObj.getShapeSetting(shapeId);
  
  if (shape && shape.type === 'Image') {
    // Calculate new dimensions
    const currentWidth = shape.width || 100;
    const currentHeight = shape.height || 100;
    const newWidth = currentWidth * factor;
    const newHeight = currentHeight * factor;
    
    // Update via API
    imgObj.updateShape(shapeId, { 
      width: newWidth, 
      height: newHeight 
    });
  }
}

// Usage
scaleImage('shape_1', 1.5); // Scale to 150%
```
