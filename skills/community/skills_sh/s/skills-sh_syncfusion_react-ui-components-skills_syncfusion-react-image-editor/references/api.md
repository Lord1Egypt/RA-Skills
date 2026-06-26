# Image Editor API Reference

Complete API documentation for the Syncfusion React ImageEditorComponent. This reference covers all properties, methods, and events available for programmatic interaction.

## Component Declaration

```tsx
<ImageEditorComponent></ImageEditorComponent>
```

---

## Properties

### Core Configuration

#### `width` (string)
- **Description:** Specifies the width of the Image Editor container
- **Default Value:** `'100%'`
- **Example:**
  ```tsx
  <ImageEditorComponent width="550px" />
  ```

#### `height` (string)
- **Description:** Specifies the height of the Image Editor container
- **Default Value:** `'100%'`
- **Example:**
  ```tsx
  <ImageEditorComponent height="350px" />
  ```

#### `disabled` (boolean)
- **Description:** Defines whether the Image Editor component is enabled or disabled
- **Default Value:** `false`
- **Example:**
  ```tsx
  <ImageEditorComponent disabled={true} />
  ```

#### `cssClass` (string)
- **Description:** Defines one or more CSS classes for customizing the appearance of the Image Editor component
- **Default Value:** `''`
- **Example:**
  ```tsx
  <ImageEditorComponent cssClass="custom-editor-class" />
  ```

### Editing and Operations

#### `allowUndoRedo` (boolean)
- **Description:** Specifies whether undo/redo operations are enabled in the image editor
- **Default Value:** `true`
- **Example:**
  ```tsx
  <ImageEditorComponent allowUndoRedo={true} />
  ```

#### `imageSmoothingEnabled` (boolean)
- **Description:** Determines whether high-quality images should be smoothed when rendered
- **Default Value:** `false`
- **Example:**
  ```tsx
  <ImageEditorComponent imageSmoothingEnabled={true} />
  ```

### Toolbar Configuration

#### `toolbar` (string[] | ItemModel[])
- **Description:** Specifies the toolbar items to perform UI interactions. Accepts string array of predefined commands or custom ItemModel array
- **Default Value:** `null` (renders default toolbar with all commands)
- **Available Commands:**
  - `Crop` - Crop image with various selection shapes and aspect ratios
  - `Straightening` - Rotate image by specified angle
  - `Annotate` - Insert shapes, text, images, and freehand drawings
  - `Transform` - Rotate and flip operations
  - `Finetunes` - Color adjustments (brightness, contrast, saturation, etc.)
  - `Filters` - Apply predefined color filters
  - `Frame` - Add decorative borders
  - `Resize` - Modify image dimensions
  - `ZoomIn` - Zoom in on image
  - `ZoomOut` - Zoom out from image
  - `Save` - Export modified image
  - `Open` - Open image for editing
  - `Undo` - Revert last action
  - `Redo` - Redo last action
  - `Reset` - Restore original image
- **Example:**
  ```tsx
  const toolbar = ['Crop', 'ZoomIn', 'ZoomOut', 'Transform', { text: 'Custom' }];
  <ImageEditorComponent toolbar={toolbar} />
  ```

#### `toolbarTemplate` (string | Function)
- **Description:** Specifies a custom template for the toolbar. If defined, the toolbar property has no effect
- **Default Value:** `null`
- **Example:**
  ```tsx
  function customToolbar() {
    return <ButtonComponent content='Custom' />;
  }
  <ImageEditorComponent toolbarTemplate={customToolbar} />
  ```

#### `showQuickAccessToolbar` (boolean)
- **Description:** Specifies whether to show or hide the quick access toolbar
- **Default Value:** `true`
- **Example:**
  ```tsx
  <ImageEditorComponent showQuickAccessToolbar={true} />
  ```

#### `quickAccessToolbarTemplate` (string | Function)
- **Description:** Specifies a template for the quick access toolbar for customization
- **Default Value:** `null`
- **Example:**
  ```tsx
  function customQuickToolbar() {
    return <div>Quick Toolbar Items</div>;
  }
  <ImageEditorComponent quickAccessToolbarTemplate={customQuickToolbar} />
  ```

### Advanced Configuration

#### `theme` (string | Theme)
- **Description:** Specifies the theme of the Image Editor. Determines the appearance of shape selections and UI elements
- **Default Value:** `Theme.Bootstrap5`
- **Supported Themes:** Bootstrap5, and other Syncfusion themes
- **Example:**
  ```tsx
  <ImageEditorComponent theme="Bootstrap5" />
  ```

#### `locale` (string)
- **Description:** Overrides the global culture and localization value for this component
- **Default Value:** `'en-US'`
- **Supported Locales:** 120+ language codes (de-DE, fr-FR, es-ES, etc.)
- **Example:**
  ```tsx
  <ImageEditorComponent locale="de-DE" />
  ```

### Settings Objects

#### `finetuneSettings` (FinetuneSettingsModel)
- **Description:** Specifies finetune settings for color adjustments in the image editor
- **Default Value:** `null`
- **Properties:**
  - `brightness` - Brightness adjustment range (min, max, defaultValue)
  - `contrast` - Contrast adjustment range
  - `saturation` - Saturation adjustment range
  - `hue` - Hue adjustment range
  - `exposure` - Exposure adjustment range
  - `blur` - Blur adjustment range
  - `opacity` - Opacity adjustment range
- **Example:**
  ```tsx
  const finetune = {
    brightness: { min: -100, max: 100, defaultValue: 0 },
    contrast: { min: -100, max: 100, defaultValue: 0 }
  };
  <ImageEditorComponent finetuneSettings={finetune} />
  ```

#### `fontFamily` (FontFamilyModel)
- **Description:** Predefines font families that populate in the font family dropdown list from the toolbar
- **Default Value:** `null`
- **Example:**
  ```tsx
  const fonts = ['Arial', 'Courier New', 'Georgia'];
  <ImageEditorComponent fontFamily={fonts} />
  ```

#### `selectionSettings` (SelectionSettingsModel)
- **Description:** Specifies selection settings to customize selection appearance and behavior
- **Default Value:** `null`
- **Example:**
  ```tsx
  const selectionSettings = {
    // Customization options
  };
  <ImageEditorComponent selectionSettings={selectionSettings} />
  ```

#### `zoomSettings` (ZoomSettingsModel)
- **Description:** Specifies zoom settings for zooming actions
- **Default Value:** `null`
- **Properties:**
  - `minZoomFactor` - Minimum zoom factor
  - `maxZoomFactor` - Maximum zoom factor
  - `zoomFactor` - Current zoom factor
  - `zoomTrigger` - Zoom triggers (MouseWheel, Pinch, Toolbar, Commands)
  - `zoomPoint` - Point to zoom in/out on (Point object with x, y)
- **Example:**
  ```tsx
  const zoomSettings = {
    minZoomFactor: 1,
    maxZoomFactor: 100,
    zoomFactor: 1,
    zoomTrigger: ZoomTrigger.MouseWheel | ZoomTrigger.Pinch
  };
  <ImageEditorComponent zoomSettings={zoomSettings} />
  ```

#### `uploadSettings` (UploadSettingsModel)
- **Description:** Represents settings for configuring image uploads with restrictions
- **Default Value:** `null`
- **Properties:**
  - `allowedExtensions` - Allowed file extensions (e.g., ['jpg', 'png', 'svg'])
  - `minFileSize` - Minimum file size in bytes
  - `maxFileSize` - Maximum file size in bytes
- **Example:**
  ```tsx
  const uploadSettings = {
    allowedExtensions: ['jpg', 'png', 'svg', 'webp', 'bmp'],
    maxFileSize: 5242880 // 5MB in bytes
  };
  <ImageEditorComponent uploadSettings={uploadSettings} />
  ```

---

## Methods

### Image Operations

#### `open(data: string | ImageData): void`
- **Description:** Opens an image as URL, base64 string, blob, or ImageData for editing
- **Parameters:**
  - `data` (string | ImageData) - URL, base64 string, blob, or ImageData object
- **Returns:** void
- **Example:**
  ```tsx
  imageObj.open('https://ej2.syncfusion.com/demos/src/image-editor/images/bridge.png');
  ```

#### `clearImage(): void`
- **Description:** Clears the loaded image in the Image Editor and resets the state
- **Returns:** void
- **Example:**
  ```tsx
  imageObj.clearImage();
  ```

#### `reset(): void`
- **Description:** Resets all modifications done in the image editor and reverts to the original image
- **Returns:** void
- **Example:**
  ```tsx
  imageObj.reset();
  ```

#### `export(type?: string, fileName?: string, imageQuality?: number): void`
- **Description:** Exports the edited image using specified file format, name, and quality
- **Parameters:**
  - `type` (string, optional) - Image format: 'image/png', 'image/jpeg', 'image/svg+xml', 'image/webp'
  - `fileName` (string, optional) - Name for the saved file
  - `imageQuality` (number, optional) - Quality of image (0-1). Default is 1
- **Returns:** void
- **Example:**
  ```tsx
  imageObj.export('image/png', 'edited-image', 0.95);
  ```

#### `getImageData(): ImageData`
- **Description:** Returns image as ImageData to load it into a canvas
- **Returns:** ImageData object
- **Example:**
  ```tsx
  const imageData = imageObj.getImageData();
  ```

#### `getImageDimension(): Dimension`
- **Description:** Gets the dimension of the image including x, y, width, and height. Useful after cropping
- **Returns:** Dimension object with x, y, width, height properties
- **Example:**
  ```tsx
  const dimension = imageObj.getImageDimension();
  console.log(dimension.width, dimension.height);
  ```

#### `resize(width: number, height: number, isAspectRatio?: boolean): boolean`
- **Description:** Resizes the image by changing its width and height
- **Parameters:**
  - `width` (number) - New width in pixels
  - `height` (number) - New height in pixels
  - `isAspectRatio` (boolean, optional) - Whether to maintain aspect ratio
- **Returns:** boolean (true if successful)
- **Example:**
  ```tsx
  imageObj.resize(800, 600, true);
  ```

### Selection and Cropping

#### `select(type: string, startX?: number, startY?: number, width?: number, height?: number): void`
- **Description:** Performs selection in the image editor for cropping purposes
- **Parameters:**
  - `type` (string) - Selection type: 'circle', 'square', 'custom', or aspect ratio like '16:9', '4:3', '3:2', etc.
  - `startX` (number, optional) - Start x-coordinate of selection
  - `startY` (number, optional) - Start y-coordinate of selection
  - `width` (number, optional) - Width of selection area
  - `height` (number, optional) - Height of selection area
- **Returns:** void
- **Example:**
  ```tsx
  imageObj.select('16:9', 10, 10, 400, 225);
  ```

#### `clearSelection(resetCrop?: boolean): void`
- **Description:** Clears the current selection performed in the image editor
- **Parameters:**
  - `resetCrop` (boolean, optional) - Whether to reset last cropped image
- **Returns:** void
- **Example:**
  ```tsx
  imageObj.clearSelection(true);
  ```

#### `crop(): boolean`
- **Description:** Crops an image based on the selection done in the image editor
- **Returns:** boolean (true if crop successful)
- **Example:**
  ```tsx
  imageObj.select('16:9', 10, 10);
  imageObj.crop();
  ```

### Transformation Methods

#### `rotate(degree: number): boolean`
- **Description:** Rotates an image clockwise (positive) or counter-clockwise (negative)
- **Parameters:**
  - `degree` (number) - Rotation angle in degrees. Positive for clockwise, negative for counter-clockwise
- **Returns:** boolean (true if successful)
- **Example:**
  ```tsx
  imageObj.rotate(90); // Rotate 90 degrees clockwise
  imageObj.rotate(-45); // Rotate 45 degrees counter-clockwise
  ```

#### `flip(direction: Direction): void`
- **Description:** Flips the image horizontally or vertically
- **Parameters:**
  - `direction` (Direction) - Flip direction: Direction.Horizontal or Direction.Vertical
- **Returns:** void
- **Example:**
  ```tsx
  imageObj.flip(Direction.Horizontal); // Flip left-right
  imageObj.flip(Direction.Vertical); // Flip top-bottom
  ```

#### `straightenImage(degree: number): boolean`
- **Description:** Straightens an image by rotating it clockwise or counter-clockwise
- **Parameters:**
  - `degree` (number) - Degree value for straightening. Positive for clockwise, negative for counter-clockwise
- **Returns:** boolean (true if successful)
- **Example:**
  ```tsx
  imageObj.straightenImage(5);
  ```

### Zoom and Pan Methods

#### `zoom(zoomFactor: number, zoomPoint?: Point): void`
- **Description:** Zooms in or out on a specific point in the image editor
- **Parameters:**
  - `zoomFactor` (number) - Percentage-based zoom factor (e.g., 20 for 2x zoom)
  - `zoomPoint` (Point, optional) - Point to zoom on with x, y coordinates
- **Returns:** void
- **Example:**
  ```tsx
  imageObj.zoom(40, { x: 400, y: 400 });
  ```

#### `pan(value: boolean, x?: number, y?: number): void`
- **Description:** Enables or disables panning on the image editor
- **Parameters:**
  - `value` (boolean) - Whether to enable or disable panning
  - `x` (number, optional) - Horizontal pan value
  - `y` (number, optional) - Vertical pan value
- **Returns:** void
- **Example:**
  ```tsx
  imageObj.pan(true, 50, 30);
  ```

#### `freehandDraw(value: boolean): void`
- **Description:** Enables or disables freehand drawing in the image editor
- **Parameters:**
  - `value` (boolean) - Whether to enable or disable freehand drawing
- **Returns:** void
- **Example:**
  ```tsx
  imageObj.freehandDraw(true);
  ```

### Annotation: Drawing Shapes

#### `drawRectangle(x?: number, y?: number, width?: number, height?: number, strokeWidth?: number, strokeColor?: string, fillColor?: string, degree?: number, isSelected?: boolean, borderRadius?: number): boolean`
- **Description:** Draws a rectangle on the image
- **Parameters:**
  - `x` (number, optional) - X-coordinate of rectangle
  - `y` (number, optional) - Y-coordinate of rectangle
  - `width` (number, optional) - Width of rectangle
  - `height` (number, optional) - Height of rectangle
  - `strokeWidth` (number, optional) - Stroke width
  - `strokeColor` (string, optional) - Stroke color (hex or rgb)
  - `fillColor` (string, optional) - Fill color
  - `degree` (number, optional) - Rotation degree
  - `isSelected` (boolean, optional) - Show in selected state
  - `borderRadius` (number, optional) - Border radius
- **Returns:** boolean (true if successful)
- **Example:**
  ```tsx
  imageObj.drawRectangle(50, 50, 100, 80, 2, '#FF0000', '#FFFF00', 0, true);
  ```

#### `drawEllipse(x?: number, y?: number, radiusX?: number, radiusY?: number, strokeWidth?: number, strokeColor?: string, fillColor?: string, degree?: number, isSelected?: boolean): boolean`
- **Description:** Draws an ellipse on the image
- **Parameters:**
  - `x` (number, optional) - X-coordinate of ellipse center
  - `y` (number, optional) - Y-coordinate of ellipse center
  - `radiusX` (number, optional) - Horizontal radius
  - `radiusY` (number, optional) - Vertical radius
  - `strokeWidth` (number, optional) - Stroke width
  - `strokeColor` (string, optional) - Stroke color
  - `fillColor` (string, optional) - Fill color
  - `degree` (number, optional) - Rotation degree
  - `isSelected` (boolean, optional) - Show in selected state
- **Returns:** boolean (true if successful)
- **Example:**
  ```tsx
  imageObj.drawEllipse(150, 100, 40, 60, 2, '#0000FF', '', 0, true);
  ```

#### `drawLine(startX?: number, startY?: number, endX?: number, endY?: number, strokeWidth?: number, strokeColor?: string, isSelected?: boolean): boolean`
- **Description:** Draws a line on the image
- **Parameters:**
  - `startX` (number, optional) - Start X-coordinate
  - `startY` (number, optional) - Start Y-coordinate
  - `endX` (number, optional) - End X-coordinate
  - `endY` (number, optional) - End Y-coordinate
  - `strokeWidth` (number, optional) - Stroke width
  - `strokeColor` (string, optional) - Stroke color
  - `isSelected` (boolean, optional) - Show in selected state
- **Returns:** boolean (true if successful)
- **Example:**
  ```tsx
  imageObj.drawLine(10, 10, 100, 100, 2, '#000000', true);
  ```

#### `drawArrow(startX?: number, startY?: number, endX?: number, endY?: number, strokeWidth?: number, strokeColor?: string, arrowStart?: ArrowheadType, arrowEnd?: ArrowheadType, isSelected?: boolean): boolean`
- **Description:** Draws an arrow on the image
- **Parameters:**
  - `startX` (number, optional) - Start X-coordinate
  - `startY` (number, optional) - Start Y-coordinate
  - `endX` (number, optional) - End X-coordinate
  - `endY` (number, optional) - End Y-coordinate
  - `strokeWidth` (number, optional) - Stroke width
  - `strokeColor` (string, optional) - Stroke color
  - `arrowStart` (ArrowheadType, optional) - Start arrowhead type (default: None)
  - `arrowEnd` (ArrowheadType, optional) - End arrowhead type (default: SolidArrow)
  - `isSelected` (boolean, optional) - Show in selected state
- **Returns:** boolean (true if successful)
- **Example:**
  ```tsx
  imageObj.drawArrow(20, 20, 150, 150, 2, '#FF0000', ArrowheadType.None, ArrowheadType.SolidArrow);
  ```

#### `drawPath(pointColl: Point[], strokeWidth?: number, strokeColor?: string, isSelected?: boolean): boolean`
- **Description:** Draws a path (polyline) on the image
- **Parameters:**
  - `pointColl` (Point[]) - Array of points with x, y coordinates
  - `strokeWidth` (number, optional) - Stroke width
  - `strokeColor` (string, optional) - Stroke color
  - `isSelected` (boolean, optional) - Show in selected state
- **Returns:** boolean (true if successful)
- **Example:**
  ```tsx
  const points = [{ x: 10, y: 10 }, { x: 50, y: 50 }, { x: 100, y: 20 }];
  imageObj.drawPath(points, 2, '#000000', true);
  ```

#### `drawText(x?: number, y?: number, text?: string, fontFamily?: string, fontSize?: number, bold?: boolean, italic?: boolean, color?: string, isSelected?: boolean, degree?: number, fillColor?: string, strokeColor?: string, strokeWidth?: number, underline?: boolean, strikethrough?: boolean): boolean`
- **Description:** Draws text annotation on the image
- **Parameters:**
  - `x` (number, optional) - X-coordinate of text
  - `y` (number, optional) - Y-coordinate of text
  - `text` (string, optional) - Text content
  - `fontFamily` (string, optional) - Font family name
  - `fontSize` (number, optional) - Font size in pixels
  - `bold` (boolean, optional) - Whether text is bold
  - `italic` (boolean, optional) - Whether text is italic
  - `color` (string, optional) - Text color
  - `isSelected` (boolean, optional) - Show in selected state
  - `degree` (number, optional) - Rotation degree
  - `fillColor` (string, optional) - Background fill color
  - `strokeColor` (string, optional) - Text outline color
  - `strokeWidth` (number, optional) - Outline stroke width
  - `underline` (boolean, optional) - Whether text is underlined
  - `strikethrough` (boolean, optional) - Whether text has strikethrough
- **Returns:** boolean (true if successful)
- **Example:**
  ```tsx
  imageObj.drawText(100, 100, 'Syncfusion', 'Arial', 20, true, false, '#000000');
  ```

#### `drawImage(data: string | ImageData, x?: number, y?: number, width?: number, height?: number, isAspectRatio?: boolean, degree?: number, opacity?: number, isSelected?: boolean): boolean`
- **Description:** Draws an image as annotation on the image
- **Parameters:**
  - `data` (string | ImageData) - Image URL or ImageData
  - `x` (number, optional) - X-coordinate
  - `y` (number, optional) - Y-coordinate
  - `width` (number, optional) - Width of image
  - `height` (number, optional) - Height of image
  - `isAspectRatio` (boolean, optional) - Maintain aspect ratio
  - `degree` (number, optional) - Rotation degree
  - `opacity` (number, optional) - Opacity value (0-1)
  - `isSelected` (boolean, optional) - Show in selected state
- **Returns:** boolean (true if successful)
- **Example:**
  ```tsx
  imageObj.drawImage('watermark.png', 50, 50, 100, 100, true, 0, 0.5);
  ```

#### `drawFrame(frameType: FrameType, color?: string, gradientColor?: string, size?: number, inset?: number, offset?: number, borderRadius?: number, frameLineStyle?: FrameLineStyle, lineCount?: number): boolean`
- **Description:** Draws a frame decoration on the image
- **Parameters:**
  - `frameType` (FrameType) - Frame type to apply
  - `color` (string, optional) - Frame color (default: '#fff')
  - `gradientColor` (string, optional) - Gradient color for frame
  - `size` (number, optional) - Frame size as percentage (default: 20)
  - `inset` (number, optional) - Inset value for specific frame types
  - `offset` (number, optional) - Offset value for specific frame types
  - `borderRadius` (number, optional) - Border radius for line-type frames
  - `frameLineStyle` (FrameLineStyle, optional) - Line style (default: Solid)
  - `lineCount` (number, optional) - Number of lines for line-type frames
- **Returns:** boolean (true if successful)
- **Example:**
  ```tsx
  imageObj.drawFrame(FrameType.Mat, '#CCCCCC', '', 15);
  ```

### Annotation: Redaction

#### `drawRedact(type?: RedactType, x?: number, y?: number, width?: number, height?: number, value?: number): boolean`
- **Description:** Draws a redaction (blur or pixelate) on the image for sensitive information
- **Parameters:**
  - `type` (RedactType, optional) - Redaction type: Blur or Pixelate (default: Blur)
  - `x` (number, optional) - X-coordinate of redaction
  - `y` (number, optional) - Y-coordinate of redaction
  - `width` (number, optional) - Width of redaction area (default: 100)
  - `height` (number, optional) - Height of redaction area (default: 50)
  - `value` (number, optional) - Blur value or pixel size (default: 20)
- **Returns:** boolean (true if successful)
- **Example:**
  ```tsx
  imageObj.drawRedact(RedactType.Blur, 100, 100, 150, 80, 20);
  ```

#### `deleteRedact(id: string): void`
- **Description:** Deletes a redaction based on the given redaction ID
- **Parameters:**
  - `id` (string) - Redaction ID to delete
- **Returns:** void
- **Example:**
  ```tsx
  imageObj.deleteRedact('redact_1');
  ```

#### `updateRedact(setting: RedactSettings, isSelected?: boolean): boolean`
- **Description:** Updates existing redaction by changing height, width, blur, or pixel size
- **Parameters:**
  - `setting` (RedactSettings) - Redaction settings to update
  - `isSelected` (boolean, optional) - Show in selected state
- **Returns:** boolean (true if successful)
- **Example:**
  ```tsx
  const redactSettings = { id: 'redact_1', width: 200, height: 100 };
  imageObj.updateRedact(redactSettings, true);
  ```

#### `selectRedact(id: string): boolean`
- **Description:** Selects a redaction based on the given redaction ID
- **Parameters:**
  - `id` (string) - Redaction ID to select
- **Returns:** boolean (true if selected)
- **Example:**
  ```tsx
  imageObj.selectRedact('redact_1');
  ```

#### `getRedacts(): RedactSettings[]`
- **Description:** Gets all redaction details that are drawn on the image editor
- **Returns:** Array of RedactSettings objects
- **Example:**
  ```tsx
  const redacts = imageObj.getRedacts();
  console.log(redacts);
  ```

### Annotation: Shape Management

#### `deleteShape(id: string): void`
- **Description:** Deletes a shape annotation based on the given shape ID
- **Parameters:**
  - `id` (string) - Shape ID to delete
- **Returns:** void
- **Example:**
  ```tsx
  imageObj.deleteShape('shape_1');
  ```

#### `updateShape(setting: ShapeSettings, isSelected?: boolean): boolean`
- **Description:** Updates existing shape by changing height, width, color, and font styles
- **Parameters:**
  - `setting` (ShapeSettings) - Shape settings to update
  - `isSelected` (boolean, optional) - Show in selected state
- **Returns:** boolean (true if successful)
- **Example:**
  ```tsx
  const shapeSettings = { id: 'shape_1', strokeColor: '#FF0000', strokeWidth: 3 };
  imageObj.updateShape(shapeSettings, true);
  ```

#### `selectShape(id: string): boolean`
- **Description:** Selects a shape based on the given shape ID
- **Parameters:**
  - `id` (string) - Shape ID to select
- **Returns:** boolean (true if selected)
- **Example:**
  ```tsx
  imageObj.selectShape('shape_1');
  ```

#### `getShapeSetting(id: string): ShapeSettings`
- **Description:** Gets a specific shape's details based on its ID
- **Parameters:**
  - `id` (string) - Shape ID
- **Returns:** ShapeSettings object
- **Example:**
  ```tsx
  const shape = imageObj.getShapeSetting('shape_1');
  console.log(shape.type, shape.strokeColor);
  ```

#### `getShapeSettings(): ShapeSettings[]`
- **Description:** Gets all shape details drawn on the image editor
- **Returns:** Array of ShapeSettings objects
- **Example:**
  ```tsx
  const shapes = imageObj.getShapeSettings();
  ```

#### `cloneShape(shapeId: string): boolean`
- **Description:** Duplicates a shape based on the given shape ID
- **Parameters:**
  - `shapeId` (string) - Shape ID to clone
- **Returns:** boolean (true if cloned successfully)
- **Example:**
  ```tsx
  imageObj.cloneShape('shape_1');
  ```

### Annotation: Z-Order Management

#### `bringForward(shapeId: string): void`
- **Description:** Moves a shape ahead of one shape based on the given shape ID
- **Parameters:**
  - `shapeId` (string) - Shape ID to move forward
- **Returns:** void
- **Example:**
  ```tsx
  imageObj.bringForward('shape_1');
  ```

#### `bringToFront(shapeId: string): void`
- **Description:** Moves a shape to the front of all other shapes
- **Parameters:**
  - `shapeId` (string) - Shape ID to bring to front
- **Returns:** void
- **Example:**
  ```tsx
  imageObj.bringToFront('shape_1');
  ```

#### `sendBackward(shapeId: string): void`
- **Description:** Moves a shape behind one shape based on the given shape ID
- **Parameters:**
  - `shapeId` (string) - Shape ID to move backward
- **Returns:** void
- **Example:**
  ```tsx
  imageObj.sendBackward('shape_1');
  ```

#### `sendToBack(shapeId: string): void`
- **Description:** Moves a shape to behind all other shapes
- **Parameters:**
  - `shapeId` (string) - Shape ID to send to back
- **Returns:** void
- **Example:**
  ```tsx
  imageObj.sendToBack('shape_1');
  ```

### Effects and Filters

#### `applyImageFilter(filterOption: ImageFilterOption): void`
- **Description:** Applies a filter to the image
- **Parameters:**
  - `filterOption` (ImageFilterOption) - Filter options object with filter type and parameters
- **Returns:** void
- **Example:**
  ```tsx
  imageObj.applyImageFilter({ type: 'Chrome' });
  imageObj.applyImageFilter({ type: 'Grayscale' });
  ```

#### `getImageFilter(filterOption: ImageFilterOption): string`
- **Description:** Gets and updates filter to the canvas in the image editor
- **Parameters:**
  - `filterOption` (ImageFilterOption) - Filter options to retrieve
- **Returns:** string (filter result)
- **Example:**
  ```tsx
  const filter = imageObj.getImageFilter({ type: 'Sepia' });
  ```

#### `finetuneImage(finetuneOption: ImageFinetuneOption, value: number): void`
- **Description:** Fine-tunes image with specified adjustment type and value
- **Parameters:**
  - `finetuneOption` (ImageFinetuneOption) - Finetune option: Brightness, Contrast, Saturation, Hue, Exposure, Blur, Opacity
  - `value` (number) - Adjustment value
- **Returns:** void
- **Example:**
  ```tsx
  imageObj.finetuneImage(ImageFinetuneOption.Brightness, 30);
  imageObj.finetuneImage(ImageFinetuneOption.Contrast, -15);
  ```

### Text Editing

#### `enableTextEditing(): void`
- **Description:** Enables text area editing in the image editor
- **Returns:** void
- **Example:**
  ```tsx
  imageObj.enableTextEditing();
  ```

### Shape Drawing Control

#### `enableShapeDrawing(shapeType: ShapeType, isEnabled?: boolean): void`
- **Description:** Enables or disables shape drawing option in the image editor
- **Parameters:**
  - `shapeType` (ShapeType) - Type of shape to enable/disable
  - `isEnabled` (boolean, optional) - Enable or disable (default: true)
- **Returns:** void
- **Example:**
  ```tsx
  imageObj.enableShapeDrawing(ShapeType.Circle, true);
  imageObj.enableShapeDrawing(ShapeType.Rectangle, false);
  ```

### Undo/Redo Operations

#### `undo(): void`
- **Description:** Reverses the last action performed by the user
- **Returns:** void
- **Example:**
  ```tsx
  imageObj.undo();
  ```

#### `redo(): void`
- **Description:** Redoes the last user action that was undone
- **Returns:** void
- **Example:**
  ```tsx
  imageObj.redo();
  ```

#### `canUndo(): boolean`
- **Description:** Specifies if it's possible to undo the last recent action
- **Returns:** boolean (true if undo is available)
- **Example:**
  ```tsx
  if (imageObj.canUndo()) {
    imageObj.undo();
  }
  ```

#### `canRedo(): boolean`
- **Description:** Specifies if it's possible to redo the last recent action
- **Returns:** boolean (true if redo is available)
- **Example:**
  ```tsx
  if (imageObj.canRedo()) {
    imageObj.redo();
  }
  ```

### Canvas Management

#### `apply(): void`
- **Description:** Applies the operations performed in the image editor (annotation drawings)
- **Returns:** void
- **Example:**
  ```tsx
  imageObj.apply();
  ```

#### `discard(): void`
- **Description:** Discards the operations performed in the image editor
- **Returns:** void
- **Example:**
  ```tsx
  imageObj.discard();
  ```

#### `update(): void`
- **Description:** Refreshes the canvas wrapper to reflect changes
- **Returns:** void
- **Example:**
  ```tsx
  imageObj.update();
  ```

---

## Events

### Lifecycle Events

#### `created`
- **Type:** `EmitType<Event>`
- **Description:** Triggered after the Image Editor component is rendered
- **Use Case:** Load initial image, apply default settings
- **Example:**
  ```tsx
  function handleCreated(): void {
    imageObj.open('https://ej2.syncfusion.com/demos/src/image-editor/images/bridge.png');
  }
  <ImageEditorComponent created={handleCreated} />
  ```

#### `destroyed`
- **Type:** `EmitType<Event>`
- **Description:** Triggered once the component is destroyed with its elements and bound events
- **Use Case:** Cleanup, dispose resources
- **Example:**
  ```tsx
  function handleDestroyed(): void {
    console.log('Component destroyed');
  }
  <ImageEditorComponent destroyed={handleDestroyed} />
  ```

### File Operations

#### `fileOpened`
- **Type:** `EmitType<OpenEventArgs>`
- **Description:** Triggered once an image is opened in the image editor
- **Event Args:**
  - `fileName` - Name of opened file
  - `fileSize` - Size of opened file
- **Use Case:** Add watermarks, apply default effects, validate image
- **Example:**
  ```tsx
  function handleFileOpened(args: OpenEventArgs): void {
    console.log('File opened:', args.fileName);
  }
  <ImageEditorComponent fileOpened={handleFileOpened} />
  ```

#### `beforeSave`
- **Type:** `EmitType<BeforeSaveEventArgs>`
- **Description:** Triggered before an image is saved
- **Event Args:** Save event details
- **Use Case:** Validation, add metadata, confirm save
- **Example:**
  ```tsx
  function handleBeforeSave(args: BeforeSaveEventArgs): void {
    console.log('About to save image');
  }
  <ImageEditorComponent beforeSave={handleBeforeSave} />
  ```

#### `saved`
- **Type:** `EmitType<SaveEventArgs>`
- **Description:** Triggered once an image is successfully saved
- **Event Args:** Save event details
- **Use Case:** Show success message, upload to server
- **Example:**
  ```tsx
  function handleSaved(args: SaveEventArgs): void {
    console.log('Image saved successfully');
  }
  <ImageEditorComponent saved={handleSaved} />
  ```

### Interaction Events

#### `click`
- **Type:** `EmitType<ImageEditorClickEventArgs>`
- **Description:** Triggered while clicking on an image in the image editor
- **Event Args:**
  - `pageX` - X-coordinate of click
  - `pageY` - Y-coordinate of click
- **Use Case:** Handle custom click interactions
- **Example:**
  ```tsx
  function handleClick(args: ImageEditorClickEventArgs): void {
    console.log('Clicked at:', args.pageX, args.pageY);
  }
  <ImageEditorComponent click={handleClick} />
  ```

### Transformation Events

#### `cropping`
- **Type:** `EmitType<CropEventArgs>`
- **Description:** Triggered while cropping an image
- **Event Args:** Crop event details with dimensions
- **Use Case:** Prevent invalid crops, lock aspect ratio
- **Example:**
  ```tsx
  function handleCropping(args: CropEventArgs): void {
    console.log('Cropping...');
  }
  <ImageEditorComponent cropping={handleCropping} />
  ```

#### `rotating`
- **Type:** `EmitType<RotateEventArgs>`
- **Description:** Triggered while rotating an image
- **Event Args:** Rotation angle and details
- **Use Case:** Track rotation state
- **Example:**
  ```tsx
  function handleRotating(args: RotateEventArgs): void {
    console.log('Rotating to:', args.degree);
  }
  <ImageEditorComponent rotating={handleRotating} />
  ```

#### `flipping`
- **Type:** `EmitType<FlipEventArgs>`
- **Description:** Triggered while flipping an image
- **Event Args:** Flip direction
- **Use Case:** Track flip state
- **Example:**
  ```tsx
  function handleFlipping(args: FlipEventArgs): void {
    console.log('Flipped:', args.direction);
  }
  <ImageEditorComponent flipping={handleFlipping} />
  ```

#### `resizing`
- **Type:** `EmitType<ResizeEventArgs>`
- **Description:** Triggered while resizing an image
- **Event Args:** New width and height
- **Use Case:** Validate dimensions, show resize preview
- **Example:**
  ```tsx
  function handleResizing(args: ResizeEventArgs): void {
    console.log('Resizing to:', args.width, args.height);
  }
  <ImageEditorComponent resizing={handleResizing} />
  ```

### Zoom and Pan Events

#### `zooming`
- **Type:** `EmitType<ZoomEventArgs>`
- **Description:** Triggered while zooming an image
- **Event Args:** Zoom factor and point
- **Use Case:** Update UI indicators, sync other components
- **Example:**
  ```tsx
  function handleZooming(args: ZoomEventArgs): void {
    console.log('Zoom factor:', args.zoomFactor);
  }
  <ImageEditorComponent zooming={handleZooming} />
  ```

#### `panning`
- **Type:** `EmitType<PanEventArgs>`
- **Description:** Triggered while panning an image
- **Event Args:** Pan offset values
- **Use Case:** Track pan state
- **Example:**
  ```tsx
  function handlePanning(args: PanEventArgs): void {
    console.log('Panning...');
  }
  <ImageEditorComponent panning={handlePanning} />
  ```

### Effect Events

#### `imageFiltering`
- **Type:** `EmitType<ImageFilterEventArgs>`
- **Description:** Triggered when applying a filter to an image
- **Event Args:** Filter type and parameters
- **Use Case:** Preview filter, log applied filters
- **Example:**
  ```tsx
  function handleImageFiltering(args: ImageFilterEventArgs): void {
    console.log('Applied filter:', args.filterType);
  }
  <ImageEditorComponent imageFiltering={handleImageFiltering} />
  ```

#### `finetuneValueChanging`
- **Type:** `EmitType<FinetuneEventArgs>`
- **Description:** Triggered when applying fine-tune adjustments to an image
- **Event Args:** Finetune type and value
- **Use Case:** Show finetune preview, track adjustments
- **Example:**
  ```tsx
  function handleFinetuneValueChanging(args: FinetuneEventArgs): void {
    console.log('Finetune:', args.type, args.value);
  }
  <ImageEditorComponent finetuneValueChanging={handleFinetuneValueChanging} />
  ```

#### `frameChange`
- **Type:** `EmitType<FrameChangeEventArgs>`
- **Description:** Triggered while applying frames on an image
- **Event Args:** Frame type and properties
- **Use Case:** Track frame application
- **Example:**
  ```tsx
  function handleFrameChange(args: FrameChangeEventArgs): void {
    console.log('Frame changed');
  }
  <ImageEditorComponent frameChange={handleFrameChange} />
  ```

### Selection Events

#### `selectionChanging`
- **Type:** `EmitType<SelectionChangeEventArgs>`
- **Description:** Triggered while changing selection in the image editor
- **Event Args:** Selection dimensions
- **Use Case:** Update UI, validate selection
- **Example:**
  ```tsx
  function handleSelectionChanging(args: SelectionChangeEventArgs): void {
    console.log('Selection changed');
  }
  <ImageEditorComponent selectionChanging={handleSelectionChanging} />
  ```

### Shape and Annotation Events

#### `shapeChanging`
- **Type:** `EmitType<ShapeChangeEventArgs>`
- **Description:** Triggered while changing shapes in the image editor
- **Event Args:** Shape properties and changes
- **Use Case:** Customize shape appearance, validate changes
- **Example:**
  ```tsx
  function handleShapeChanging(args: ShapeChangeEventArgs): void {
    // Customize shape on the fly
    if (args.type === 'text') {
      args.fillColor = '#FF0000';
    }
  }
  <ImageEditorComponent shapeChanging={handleShapeChanging} />
  ```

#### `shapeChange`
- **Type:** `EmitType<ShapeChangeEventArgs>`
- **Description:** Triggered after shape changing action is completed
- **Event Args:** Final shape properties
- **Use Case:** Log changes, update data model
- **Example:**
  ```tsx
  function handleShapeChange(args: ShapeChangeEventArgs): void {
    console.log('Shape changed:', args.id);
  }
  <ImageEditorComponent shapeChange={handleShapeChange} />
  ```

#### `editComplete`
- **Type:** `EmitType<EditCompleteEventArgs>`
- **Description:** Triggered after completion of any editing action in the image editor
- **Event Args:** Edit action details
- **Use Case:** Update UI, save state, trigger related actions
- **Example:**
  ```tsx
  function handleEditComplete(args: EditCompleteEventArgs): void {
    console.log('Edit complete:', args.action);
  }
  <ImageEditorComponent editComplete={handleEditComplete} />
  ```

### Toolbar Events

#### `toolbarCreated`
- **Type:** `EmitType<ToolbarEventArgs>`
- **Description:** Triggered once the toolbar is created
- **Event Args:** Toolbar items and configuration
- **Use Case:** Add/remove toolbar items, customize appearance
- **Example:**
  ```tsx
  function handleToolbarCreated(args: ToolbarEventArgs): void {
    console.log('Toolbar created');
  }
  <ImageEditorComponent toolbarCreated={handleToolbarCreated} />
  ```

#### `toolbarUpdating`
- **Type:** `EmitType<ToolbarEventArgs>`
- **Description:** Triggered while updating or refreshing the toolbar
- **Event Args:** Toolbar type and items
- **Use Case:** Dynamically customize contextual toolbars
- **Example:**
  ```tsx
  function handleToolbarUpdating(args: ToolbarEventArgs): void {
    if (args.toolbarType === 'shapes') {
      args.toolbarItems = ['fillColor', 'strokeColor', 'strokeWidth'];
    }
  }
  <ImageEditorComponent toolbarUpdating={handleToolbarUpdating} />
  ```

#### `toolbarItemClicked`
- **Type:** `EmitType<ClickEventArgs>`
- **Description:** Triggered once a toolbar item is clicked
- **Event Args:** Clicked item information
- **Use Case:** Handle custom toolbar item actions
- **Example:**
  ```tsx
  function handleToolbarItemClicked(args: ClickEventArgs): void {
    console.log('Toolbar item clicked');
  }
  <ImageEditorComponent toolbarItemClicked={handleToolbarItemClicked} />
  ```

### Quick Access Toolbar Events

#### `quickAccessToolbarOpen`
- **Type:** `EmitType<QuickAccessToolbarEventArgs>`
- **Description:** Triggered when the quick access toolbar opens
- **Event Args:** Toolbar configuration
- **Use Case:** Customize quick access items
- **Example:**
  ```tsx
  function handleQuickAccessToolbarOpen(args: QuickAccessToolbarEventArgs): void {
    console.log('Quick access toolbar opened');
  }
  <ImageEditorComponent quickAccessToolbarOpen={handleQuickAccessToolbarOpen} />
  ```

#### `quickAccessToolbarItemClick`
- **Type:** `EmitType<ClickEventArgs>`
- **Description:** Triggered when a quick access toolbar item is clicked
- **Event Args:** Clicked item information
- **Use Case:** Handle quick access item actions
- **Example:**
  ```tsx
  function handleQuickAccessToolbarItemClick(args: ClickEventArgs): void {
    console.log('Quick access toolbar item clicked');
  }
  <ImageEditorComponent quickAccessToolbarItemClick={handleQuickAccessToolbarItemClick} />
  ```

---

## Enums and Type Definitions

### Direction
Direction for flip operations:
- `Horizontal` - Flip left-right
- `Vertical` - Flip top-bottom

### ArrowheadType
Arrowhead style for arrow annotations:
- `None` - No arrowhead
- `SolidArrow` - Solid arrowhead
- `BarArrow` - Bar arrowhead

### RedactType
Type of redaction:
- `Blur` - Blur sensitive content
- `Pixelate` - Pixelate sensitive content

### FrameType
Frame decoration styles:
- `Mat` - Matte frame
- `Bevel` - Beveled frame
- `Line` - Line frame
- `Inset` - Inset frame
- `Hook` - Hook frame

### ShapeType
Shape types for enabling/disabling:
- `Rectangle`, `Ellipse`, `Line`, `Arrow`, `Path`, `Text`, `Image`, `Freehand`, `RedactRectangle`, `RedactEllipse`

### ImageFinetuneOption
Fine-tune adjustment types:
- `Brightness` - Adjust brightness
- `Contrast` - Adjust contrast
- `Saturation` - Adjust saturation
- `Hue` - Adjust hue
- `Exposure` - Adjust exposure
- `Blur` - Apply blur effect
- `Opacity` - Adjust opacity

### Theme
Available themes:
- `Bootstrap5`

### ZoomTrigger
Zoom activation methods (can be combined with bitwise OR):
- `MouseWheel` - Scroll to zoom
- `Pinch` - Pinch gesture on touch devices
- `Toolbar` - Zoom buttons
- `Commands` - Programmatic zoom via methods

---

## Complete API Example

```tsx
import { ImageEditorComponent } from '@syncfusion/ej2-react-image-editor';
import React, { useRef } from 'react';

function ImageEditorDemo() {
  const imageEditorRef = useRef<ImageEditorComponent>(null);

  const handleCreated = () => {
    imageEditorRef.current?.open(
      'https://ej2.syncfusion.com/demos/src/image-editor/images/bridge.png'
    );
  };

  const handleRotate = () => {
    imageEditorRef.current?.rotate(90);
  };

  const handleCrop = () => {
    imageEditorRef.current?.select('16:9', 10, 10);
    imageEditorRef.current?.crop();
  };

  const handleExport = () => {
    imageEditorRef.current?.export('image/png', 'edited-image');
  };

  const handleAddText = () => {
    const dimension = imageEditorRef.current?.getImageDimension();
    imageEditorRef.current?.drawText(
      dimension?.x || 100,
      dimension?.y || 100,
      'Sample Text',
      'Arial',
      20,
      false,
      false,
      '#000000'
    );
  };

  return (
    <div>
      <ImageEditorComponent
        ref={imageEditorRef}
        width="550px"
        height="350px"
        created={handleCreated}
        toolbar={['Crop', 'ZoomIn', 'ZoomOut', 'Transform', 'Save', 'Reset']}
      />
      <div>
        <button onClick={handleRotate}>Rotate 90°</button>
        <button onClick={handleCrop}>Crop 16:9</button>
        <button onClick={handleAddText}>Add Text</button>
        <button onClick={handleExport}>Export</button>
      </div>
    </div>
  );
}

export default ImageEditorDemo;
```

---

## Related References

- [Getting Started](getting-started.md) - Installation and basic setup
- [Opening and Saving Images](opening-saving-images.md) - File operations
- [Selection and Cropping](selection-cropping.md) - Crop functionality
- [Transform, Rotate, Flip](transform-rotate-flip.md) - Image transformations
- [Text Annotations](text-annotations.md) - Adding text
- [Shape Annotations](shape-annotations.md) - Drawing shapes
- [Filters](filters.md) - Apply image filters
- [Fine-Tuning](finetune.md) - Color adjustments
- [Accessibility and Localization](accessibility-localization.md) - Accessibility features
