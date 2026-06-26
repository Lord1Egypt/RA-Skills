# Text Annotations

## Table of Contents
- [Adding Text](#adding-text)
- [Text Styling](#text-styling)
- [Font Customization](#font-customization)
- [Multiline Text](#multiline-text)
- [Managing Text Annotations](#managing-text-annotations)

## Adding Text

### Basic Text

Add simple text annotation at specific coordinates:

```tsx
function addText(): void {
  const dimension = imgObj.getImageDimension();
  imgObj.drawText(dimension.x, dimension.y, 'Sample Text');
}
```

### Text with Font Properties

Add text with customized font settings:

```tsx
function addStyledText(): void {
  const dimension = imgObj.getImageDimension();
  imgObj.drawText(
    dimension.x + 50,           // x coordinate
    dimension.y + 50,           // y coordinate
    'Syncfusion',               // text content
    'Arial',                    // font family
    30,                         // font size
    false,                      // bold (boolean)
    false,                      // italic (boolean)
    'blue'                      // color
  );
}
```

### Text with Background and Outline

Add text with background color and stroke:

```tsx
function addTextWithOutline(): void {
  const dimension = imgObj.getImageDimension();
  imgObj.drawText(
    dimension.x + 100,
    dimension.y + 100,
    'Watermark',
    'Arial',
    40,
    false,
    false,
    'white',      // font color
    false,        // isSelected
    0,            // degree
    'red',        // fillColor (background)
    'black',      // strokeColor (outline)
    2             // strokeWidth
  );
}
```

### Text with Rotation

Add text rotated by specific degree:

```tsx
function addRotatedText(): void {
  const dimension = imgObj.getImageDimension();
  imgObj.drawText(
    dimension.x + 50,
    dimension.y + 50,
    'Rotated Text',
    'Arial',
    25,
    false,
    false,
    'black',
    false,
    45  // 45 degree rotation
  );
}
```

## Text Styling

### Bold Text

Add bold text annotations:

```tsx
function addBoldText(): void {
  const dimension = imgObj.getImageDimension();
  imgObj.drawText(
    dimension.x,
    dimension.y,
    'Bold Text',
    'Arial',
    25,
    true,  // bold = true
    false
  );
}
```

### Italic Text

Add italic styled text:

```tsx
function addItalicText(): void {
  const dimension = imgObj.getImageDimension();
  imgObj.drawText(
    dimension.x,
    dimension.y,
    'Italic Text',
    'Arial',
    25,
    false,
    true   // italic = true
  );
}
```

### Bold Italic Text

Combine bold and italic:

```tsx
function addBoldItalicText(): void {
  const dimension = imgObj.getImageDimension();
  imgObj.drawText(
    dimension.x,
    dimension.y,
    'Bold Italic',
    'Arial',
    25,
    true,  // bold
    true   // italic
  );
}
```

### Underline and Strikethrough

Add text with underline or strikethrough using the drawText method:

```tsx
function addUnderlineText(): void {
  const dimension = imgObj.getImageDimension();
  imgObj.drawText(
    dimension.x,
    dimension.y,
    'Underlined Text',
    'Arial',
    20,
    false,
    false,
    '#000000',
    false,
    0,
    '',
    '',
    0,
    true,  // underline
    false  // strikethrough
  );
}

function addStrikethroughText(): void {
  const dimension = imgObj.getImageDimension();
  imgObj.drawText(
    dimension.x,
    dimension.y,
    'Strikethrough Text',
    'Arial',
    20,
    false,
    false,
    '#000000',
    false,
    0,
    '',
    '',
    0,
    false, // underline
    true   // strikethrough
  );
}
```

## Font Customization

### Add Custom Font Families

Extend available fonts:

```tsx
const fontFamily = {
  default: 'Arial',
  items: [
    { id: 'arial', text: 'Arial' },
    { id: 'brush script mt', text: 'Brush Script MT' },
    { id: 'papyrus', text: 'Papyrus' },
    { id: 'times new roman', text: 'Times New Roman' },
    { id: 'courier new', text: 'Courier New' }
  ]
};

<ImageEditorComponent fontFamily={fontFamily} />
```

### Use Custom Fonts

Apply custom font when adding text:

```tsx
function addWithCustomFont(): void {
  const dimension = imgObj.getImageDimension();
  imgObj.drawText(
    dimension.x,
    dimension.y,
    'Fancy Text',
    'Papyrus',  // Custom font
    28
  );
}
```

### Change Font via Event

Customize font family dynamically:

```tsx
function shapeChanging(args: any): void {
  if (args.currentShapeSettings.type === 'Text') {
    args.currentShapeSettings.color = 'red';
    args.currentShapeSettings.fontFamily = 'Times New Roman';
  }
}

<ImageEditorComponent shapeChanging={shapeChanging} />
```

## Multiline Text

### Add Multiline Text

Use newline character `\n` for multiple lines:

```tsx
function addMultilineText(): void {
  const dimension = imgObj.getImageDimension();
  imgObj.drawText(
    dimension.x,
    dimension.y,
    'Line 1\nLine 2\nLine 3',
    'Arial',
    20
  );
}
```

### Multiline with Styling

Style multiline text:

```tsx
function addStyledMultiline(): void {
  const dimension = imgObj.getImageDimension();
  imgObj.drawText(
    dimension.x + 50,
    dimension.y + 50,
    'Header\nSubtitle\nDescription',
    'Arial',
    25,
    true,      // bold header effect
    false,
    'darkblue'
  );
}
```

## Managing Text Annotations

### Get All Text Annotations

Retrieve all shapes (including text):

```tsx
function getAllText(): void {
  const shapes = imgObj.getShapeSettings();
  const textShapes = shapes.filter(s => s.type === 'Text');
  console.log('Text annotations:', textShapes);
}
```

### Delete Text Annotation

Remove text by shape ID:

```tsx
function deleteText(): void {
  imgObj.deleteShape('shape_1');
}

// Or delete last added text
function deleteLastText(): void {
  const shapes = imgObj.getShapeSettings();
  if (shapes.length > 0) {
    imgObj.deleteShape(shapes[shapes.length - 1].id);
  }
}
```

### Update Text Properties

Modify existing text annotation:

```tsx
function updateTextColor(): void {
  const shapes = imgObj.getShapeSettings();
  if (shapes && shapes[0].type === 'Text') {
    shapes[0].color = 'green';
    imgObj.updateShape(shapes[0]);
  }
}
```

### Find Text Containing Keyword

Search for specific text:

```tsx
function findText(keyword: string): any {
  const shapes = imgObj.getShapeSettings();
  return shapes.find(s => 
    s.type === 'Text' && s.text.includes(keyword)
  );
}

const found = findText('Sync');
if (found) {
  console.log('Found:', found);
}
```

## Advanced Patterns

### Text Positioning

Align text at specific positions:

```tsx
function addTopLeftText(): void {
  const dimension = imgObj.getImageDimension();
  imgObj.drawText(dimension.x + 10, dimension.y + 10, 'Top Left');
}

function addCenterText(): void {
  const dimension = imgObj.getImageDimension();
  const centerX = dimension.x + dimension.width / 2;
  const centerY = dimension.y + dimension.height / 2;
  imgObj.drawText(centerX, centerY, 'Center');
}

function addBottomRightText(): void {
  const dimension = imgObj.getImageDimension();
  const x = dimension.x + dimension.width - 100;
  const y = dimension.y + dimension.height - 30;
  imgObj.drawText(x, y, 'Bottom Right');
}
```

### Watermark Pattern

Add semi-transparent watermark:

```tsx
function addWatermark(): void {
  const dimension = imgObj.getImageDimension();
  imgObj.drawText(
    dimension.x + 50,
    dimension.y + 50,
    'WATERMARK',
    'Arial',
    50,
    false,
    false,
    '#80808080'  // Semi-transparent gray
  );
}
```

### Date Timestamp

Add current date as text:

```tsx
function addTimestamp(): void {
  const dimension = imgObj.getImageDimension();
  const now = new Date().toLocaleString();
  imgObj.drawText(
    dimension.x + 10,
    dimension.y + dimension.height - 30,
    `Created: ${now}`,
    'Arial',
    12
  );
}
```

### Duplicate Text

Clone existing text annotation:

```tsx
function duplicateText(): void {
  const shapes = imgObj.getShapeSettings();
  if (shapes && shapes.length > 0 && shapes[0].type === 'Text') {
    const original = shapes[0];
    // Create offset copy of the text
    imgObj.drawText(
      (original.x || 0) + 20,
      (original.y || 0) + 20,
      original.text || 'Text',
      original.fontFamily || 'Arial',
      original.fontSize || 12,
      false,
      false,
      original.color || '#000000'
    );
  }
}
```
