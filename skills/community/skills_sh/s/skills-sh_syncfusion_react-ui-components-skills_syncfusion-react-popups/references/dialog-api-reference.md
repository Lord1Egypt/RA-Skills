# Dialog API Reference

Complete API documentation for Syncfusion React DialogComponent from official EJ2 documentation.

## Table of Contents
- [Component](#component)
- [Properties (DialogModel)](#properties-dialogmodel)
- [Methods](#methods)
- [Events](#events)
- [Button Properties (ButtonPropsModel)](#button-properties-buttonpropsmodel)
- [Animation Settings (AnimationSettingsModel)](#animation-settings-animationsettingsmodel)
- [Types and Enumerations](#types-and-enumerations)
- [Quick Reference](#quick-reference)

---

## Component

### DialogComponent

The main React component for displaying dialogs and modal windows.

**Package:** `@syncfusion/ej2-react-popups`

**Import:**
```jsx
import { DialogComponent } from '@syncfusion/ej2-react-popups';
```

**Basic Usage:**
```jsx
<DialogComponent
  ref={dialogRef}
  header="Title"
  width="400px"
  visible={false}
  isModal={true}
>
  Dialog content goes here
</DialogComponent>
```

---

## Properties (DialogModel)

### Core Properties

#### `header`
- **Type:** `string | HTMLElement | Function`
- **Default:** `null`
- **Description:** Specifies the value that can be displayed in the dialog's title area
- **Example:**
  ```jsx
  <DialogComponent header="Welcome to Dialog" />
  
  // With JSX
  <DialogComponent header={<div>Custom <strong>Header</strong></div>} />
  ```

#### `content`
- **Type:** `string | HTMLElement | Function`
- **Default:** `null`
- **Description:** Specifies the value displayed in dialog's content area
- **Example:**
  ```jsx
  <DialogComponent content="This is content" />
  
  // With JSX
  <DialogComponent content={<div><p>Rich content</p></div>} />
  ```

#### `width`
- **Type:** `string | number`
- **Default:** `'330px'`
- **Description:** Specifies the width of the dialog component
- **Example:**
  ```jsx
  <DialogComponent width="400px" />
  <DialogComponent width={500} />
  <DialogComponent width="80%" />
  ```

#### `height`
- **Type:** `string | number`
- **Default:** `'auto'`
- **Description:** Specifies the height of the dialog component
- **Important:** The dialog's `max-height` is calculated based on the height of its **target element**. If the dialog's height is larger than the target (body) height, the dialog height will not be set correctly. Always ensure the target container has proper dimensions.
- **Example:**
  ```jsx
  <DialogComponent height="300px" />
  <DialogComponent height={400} />
  <DialogComponent height="100%" />
  ```

#### `minHeight`
- **Type:** `string | number`
- **Default:** `null`
- **Description:** Specifies the minimum height of the dialog during resize
- **Example:**
  ```jsx
  <DialogComponent minHeight="200px" enableResize={true} />
  ```

### Visibility and Modal Properties

#### `visible`
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Specifies whether the dialog component is visible
- **Example:**
  ```jsx
  const [isVisible, setIsVisible] = useState(false);
  <DialogComponent visible={isVisible} />
  ```

#### `isModal`
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Specifies if the dialog can be displayed as modal (blocks parent) or modeless
- **Example:**
  ```jsx
  <DialogComponent isModal={true} />      // Blocks interaction
  <DialogComponent isModal={false} />     // Allows interaction
  ```

#### `closeOnEscape`
- **Type:** `boolean`
- **Default:** `true`
- **Description:** Specifies whether dialog can be closed with Escape key
- **Example:**
  ```jsx
  <DialogComponent closeOnEscape={true} />
  <DialogComponent closeOnEscape={false} />
  ```

### Positioning and Layout Properties

#### `position`
- **Type:** `PositionDataModel`
- **Default:** `{ X: 'center', Y: 'center' }`
- **Description:** Specifies where the dialog can be positioned
- **PositionDataModel:**
  ```typescript
  {
    X: 'left' | 'center' | 'right' | number,  // X position
    Y: 'top' | 'center' | 'bottom' | number   // Y position
  }
  ```
- **Example:**
  ```jsx
  // Preset positions
  <DialogComponent position={{ X: 'center', Y: 'center' }} />
  <DialogComponent position={{ X: 'left', Y: 'top' }} />
  <DialogComponent position={{ X: 'right', Y: 'bottom' }} />
  
  // Custom pixels
  <DialogComponent position={{ X: 100, Y: 50 }} />
  
  // Mixed
  <DialogComponent position={{ X: 'center', Y: 100 }} />
  ```

#### `target`
- **Type:** `HTMLElement | string`
- **Default:** `document.body`
- **Description:** Specifies the target element in which the dialog displays (required for modal)
- **Important:** The dialog's `max-height` is calculated based on this target element's height. If `target` is not configured, `document.body` is used. To ensure the dialog displays at its proper height, the target element must have an explicit `min-height` or `height`. When `document.body` is the target, set CSS for both `html` and `body` so the dialog can size correctly:
  ```css
  html, body {
    height: 100%;
    margin: 0;
  }
  ```
- **Example:**
  ```jsx
  <div id="dialog-container" style={{ position: 'relative', minHeight: '500px' }}>
    <DialogComponent 
      target="#dialog-container"
      isModal={true}
    />
  </div>
  ```

#### `zIndex`
- **Type:** `number`
- **Default:** `auto`
- **Description:** Specifies z-order for rendering (determines front/back display)
- **Example:**
  ```jsx
  <DialogComponent zIndex={2000} />
  <DialogComponent zIndex={2001} />  // Appears in front
  ```

### Interaction Properties

#### `allowDragging`
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Specifies whether dialog component can be dragged
- **Example:**
  ```jsx
  <DialogComponent 
    allowDragging={true}
    position={{ X: 100, Y: 100 }}
  />
  ```

#### `enableResize`
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Specifies whether dialog component can be resized
- **Example:**
  ```jsx
  <DialogComponent 
    enableResize={true}
    resizeHandles={['All']}
  />
  ```

#### `resizeHandles`
- **Type:** `ResizeDirections[]`
- **Default:** `['All']`
- **Description:** Specifies which resize handles direction in dialog
- **ResizeDirections:** `'All' | 'North' | 'South' | 'East' | 'West' | 'NorthEast' | 'NorthWest' | 'SouthEast' | 'SouthWest'`
- **Example:**
  ```jsx
  <DialogComponent 
    enableResize={true}
    resizeHandles={['All']}
  />
  
  <DialogComponent 
    enableResize={true}
    resizeHandles={['East', 'West', 'South']}
  />
  ```

### Button and Template Properties

#### `buttons`
- **Type:** `ButtonPropsModel[]`
- **Default:** `null`
- **Description:** Configures action buttons with button properties
- **Example:**
  ```jsx
  const buttons = [
    {
      buttonModel: {
        content: 'OK',
        isPrimary: true,
        cssClass: 'e-flat'
      },
      click: handleOK
    },
    {
      buttonModel: {
        content: 'Cancel',
        cssClass: 'e-flat'
      },
      click: handleCancel
    }
  ];
  
  <DialogComponent buttons={buttons} />
  ```

#### `footerTemplate`
- **Type:** `HTMLElement | string | Function`
- **Default:** `null`
- **Description:** Specifies custom footer template (replaces buttons)
- **Example:**
  ```jsx
  <DialogComponent
    footerTemplate={
      <div style={{ padding: '12px', textAlign: 'right' }}>
        <button>Save</button>
        <button>Cancel</button>
      </div>
    }
  />
  ```

#### `showCloseIcon`
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Specifies whether close icon is shown in header
- **Example:**
  ```jsx
  <DialogComponent showCloseIcon={true} />
  ```

### Animation Properties

#### `animationSettings`
- **Type:** `AnimationSettingsModel`
- **Default:** `null`
- **Description:** Specifies animation settings for dialog open/close
- **Example:**
  ```jsx
  <DialogComponent
    animationSettings={{
      effect: 'Zoom',
      duration: 400,
      delay: 0
    }}
  />
  ```

### Customization Properties

#### `cssClass`
- **Type:** `string`
- **Default:** `null`
- **Description:** Specifies CSS classes to append to root element
- **Example:**
  ```jsx
  <DialogComponent cssClass="custom-dialog dark-theme" />
  ```

#### `enableHtmlSanitizer`
- **Type:** `boolean`
- **Default:** `true`
- **Description:** Defines whether to sanitize HTML content (security)
- **Example:**
  ```jsx
  <DialogComponent enableHtmlSanitizer={true} />
  ```

#### `enableRtl`
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Enable/disable rendering in right-to-left direction
- **Example:**
  ```jsx
  <DialogComponent enableRtl={true} />
  ```

#### `locale`
- **Type:** `string`
- **Default:** `'en-US'`
- **Description:** Overrides global culture and localization for this component
- **Example:**
  ```jsx
  <DialogComponent locale="de" />
  <DialogComponent locale="es" />
  <DialogComponent locale="fr" />
  <DialogComponent locale="ja" />
  <DialogComponent locale="zh" />
  ```

#### `enablePersistence`
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Enables persistence of dialog dimensions and position between page reloads
- **Example:**
  ```jsx
  <DialogComponent enablePersistence={true} />
  ```

---

## Methods

### Public Methods

#### `show()`
- **Description:** Display the dialog
- **Syntax:** `dialogRef.current?.show()`
- **Return Type:** `void`
- **Example:**
  ```jsx
  const dialogRef = useRef(null);
  
  const handleOpen = () => {
    dialogRef.current?.show();
  };
  ```

#### `hide()`
- **Description:** Hide the dialog
- **Syntax:** `dialogRef.current?.hide()`
- **Return Type:** `void`
- **Example:**
  ```jsx
  const handleClose = () => {
    dialogRef.current?.hide();
  };
  ```

#### `refresh()`
- **Description:** Refresh the dialog (recalculate position)
- **Syntax:** `dialogRef.current?.refresh()`
- **Return Type:** `void`
- **Example:**
  ```jsx
  const handleRefresh = () => {
    dialogRef.current?.refresh();
  };
  ```

#### `destroy()`
- **Description:** Destroy the dialog component and clean up resources
- **Syntax:** `dialogRef.current?.destroy()`
- **Return Type:** `void`
- **Example:**
  ```jsx
  useEffect(() => {
    return () => {
      dialogRef.current?.destroy();
    };
  }, []);
  ```

---

## Events

### Dialog Events

All events receive the event arguments as callback parameter.

#### `beforeOpen`
- **Type:** `EmitType<BeforeOpenEventArgs>`
- **Description:** Event triggers when dialog is being opened (can be cancelled)
- **Can Cancel:** Yes
- **Example:**
  ```jsx
  const handleBeforeOpen = (args) => {
    console.log('Dialog opening...');
    // args.cancel = true; // Prevent opening
  };
  
  <DialogComponent beforeOpen={handleBeforeOpen} />
  ```

#### `open`
- **Type:** `EmitType<OpenEventArgs>`
- **Description:** Event triggers after dialog has opened
- **Example:**
  ```jsx
  const handleOpen = (args) => {
    console.log('Dialog opened');
  };
  
  <DialogComponent open={handleOpen} />
  ```

#### `beforeClose`
- **Type:** `EmitType<BeforeCloseEventArgs>`
- **Description:** Event triggers before dialog closes (can be cancelled)
- **Can Cancel:** Yes
- **Example:**
  ```jsx
  const handleBeforeClose = (args) => {
    if (hasUnsavedChanges) {
      args.cancel = true; // Prevent closing
    }
  };
  
  <DialogComponent beforeClose={handleBeforeClose} />
  ```

#### `close`
- **Type:** `EmitType<CloseEventArgs>`
- **Description:** Event triggers after dialog has closed
- **Example:**
  ```jsx
  const handleClose = (args) => {
    console.log('Dialog closed');
  };
  
  <DialogComponent close={handleClose} />
  ```

### Drag Events

#### `dragStart`
- **Type:** `EmitType<DragStartEventArgs>`
- **Description:** Event triggers when user begins dragging dialog
- **Example:**
  ```jsx
  const handleDragStart = (args) => {
    console.log('Drag started at:', args.clientX, args.clientY);
  };
  
  <DialogComponent
    allowDragging={true}
    dragStart={handleDragStart}
  />
  ```

#### `drag`
- **Type:** `EmitType<DragEventArgs>`
- **Description:** Event triggers while user is dragging dialog
- **Example:**
  ```jsx
  const handleDrag = (args) => {
    console.log('Dragging:', args.clientX, args.clientY);
  };
  
  <DialogComponent
    allowDragging={true}
    drag={handleDrag}
  />
  ```

#### `dragStop`
- **Type:** `EmitType<DragStopEventArgs>`
- **Description:** Event triggers when user stops dragging dialog
- **Example:**
  ```jsx
  const handleDragStop = (args) => {
    console.log('Drag stopped');
  };
  
  <DialogComponent
    allowDragging={true}
    dragStop={handleDragStop}
  />
  ```

### Resize Events

#### `resizeStart`
- **Type:** `EmitType<Object>`
- **Description:** Event triggers when user begins resizing dialog
- **Example:**
  ```jsx
  const handleResizeStart = (args) => {
    console.log('Resize started');
  };
  
  <DialogComponent
    enableResize={true}
    resizeStart={handleResizeStart}
  />
  ```

#### `resizing`
- **Type:** `EmitType<Object>`
- **Description:** Event triggers while user is resizing dialog
- **Example:**
  ```jsx
  const handleResizing = (args) => {
    console.log('Resizing...');
  };
  
  <DialogComponent
    enableResize={true}
    resizing={handleResizing}
  />
  ```

#### `resizeStop`
- **Type:** `EmitType<Object>`
- **Description:** Event triggers when user stops resizing dialog
- **Example:**
  ```jsx
  const handleResizeStop = (args) => {
    console.log('Resize stopped');
  };
  
  <DialogComponent
    enableResize={true}
    resizeStop={handleResizeStop}
  />
  ```

### Other Events

#### `overlayClick`
- **Type:** `EmitType<Object>`
- **Description:** Event triggers when overlay (backdrop) is clicked in modal dialogs
- **Example:**
  ```jsx
  const handleOverlayClick = (args) => {
    console.log('Overlay clicked');
  };
  
  <DialogComponent
    isModal={true}
    overlayClick={handleOverlayClick}
  />
  ```

#### `created`
- **Type:** `EmitType<Object>`
- **Description:** Event triggers when dialog is created
- **Example:**
  ```jsx
  const handleCreated = () => {
    console.log('Dialog component created');
  };
  
  <DialogComponent created={handleCreated} />
  ```

#### `destroyed`
- **Type:** `EmitType<Event>`
- **Description:** Event triggers when dialog is destroyed
- **Example:**
  ```jsx
  const handleDestroyed = () => {
    console.log('Dialog destroyed');
  };
  
  <DialogComponent destroyed={handleDestroyed} />
  ```

---

## Button Properties (ButtonPropsModel)

### ButtonPropsModel Structure

Each button in the `buttons` array follows this structure:

```jsx
{
  buttonModel: ButtonModel,      // Button configuration
  click: EmitType<Object>,       // Click event handler
  isFlat?: boolean,              // Flat appearance (default: true)
  type?: ButtonType              // Button type
}
```

### ButtonModel Properties

#### `content`
- **Type:** `string`
- **Description:** Button text/label
- **Example:** `{ content: 'Save' }`

#### `isPrimary`
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Highlight button as primary action
- **Example:** `{ isPrimary: true }`

#### `cssClass`
- **Type:** `string`
- **Description:** CSS classes for styling
- **Common Classes:**
  - `e-flat` - Flat style
  - `e-outline` - Outline style
  - `e-danger` - Red danger color
  - `e-success` - Green success color
  - `e-warning` - Yellow warning color
- **Example:** `{ cssClass: 'e-flat e-danger' }`

#### `id`
- **Type:** `string`
- **Description:** HTML id for button element
- **Example:** `{ id: 'save-btn' }`

#### `iconCss`
- **Type:** `string`
- **Description:** Icon class (Font Awesome, Material Icons)
- **Example:** `{ iconCss: 'e-icons e-save' }`

### ButtonType Enumeration

- `'Button'` - Standard button (default)
- `'Submit'` - Submit form
- `'Reset'` - Reset form

### Complete Button Example

```jsx
const buttons = [
  {
    buttonModel: {
      content: 'Save',
      cssClass: 'e-flat e-primary',
      isPrimary: true,
      iconCss: 'e-icons e-save',
      id: 'save-btn'
    },
    click: handleSave,
    isFlat: true,
    type: 'Submit'
  },
  {
    buttonModel: {
      content: 'Cancel',
      cssClass: 'e-flat',
      id: 'cancel-btn'
    },
    click: handleCancel,
    isFlat: true,
    type: 'Button'
  }
];
```

---

## Animation Settings (AnimationSettingsModel)

### AnimationSettingsModel Properties

#### `effect`
- **Type:** `DialogEffect`
- **Default:** `'Fade'`
- **Description:** Animation effect for open/close
- **Supported Effects:**
  1. `'Fade'` - Opacity transition
  2. `'FadeZoom'` - Fade + zoom combined
  3. `'FlipLeftDown'` - 3D flip left-down
  4. `'FlipLeftUp'` - 3D flip left-up
  5. `'FlipRightDown'` - 3D flip right-down
  6. `'FlipRightUp'` - 3D flip right-up
  7. `'FlipXDown'` - Horizontal flip down
  8. `'FlipXUp'` - Horizontal flip up
  9. `'FlipYLeft'` - Vertical flip left
  10. `'FlipYRight'` - Vertical flip right
  11. `'SlideBottom'` - Slide from bottom
  12. `'SlideLeft'` - Slide from left
  13. `'SlideRight'` - Slide from right
  14. `'SlideTop'` - Slide from top
  15. `'Zoom'` - Scale animation
  16. `'None'` - No animation

#### `duration`
- **Type:** `number`
- **Default:** `400`
- **Description:** Animation duration in milliseconds
- **Example:** `{ duration: 300 }` - 300ms animation

#### `delay`
- **Type:** `number`
- **Default:** `0`
- **Description:** Delay before animation starts in milliseconds
- **Example:** `{ delay: 100 }` - 100ms delay before animation

### AnimationSettingsModel Examples

```jsx
// Fast zoom
<DialogComponent
  animationSettings={{
    effect: 'Zoom',
    duration: 200,
    delay: 0
  }}
/>

// Slow slide with delay
<DialogComponent
  animationSettings={{
    effect: 'SlideBottom',
    duration: 600,
    delay: 100
  }}
/>

// 3D flip
<DialogComponent
  animationSettings={{
    effect: 'FlipLeftDown',
    duration: 500,
    delay: 0
  }}
/>

// No animation
<DialogComponent
  animationSettings={{
    effect: 'None'
  }}
/>
```

---

## Types and Enumerations

### DialogEffect

Animation effects available for dialog:

```typescript
type DialogEffect = 
  'Fade' | 'FadeZoom' | 'FlipLeftDown' | 'FlipLeftUp' |
  'FlipRightDown' | 'FlipRightUp' | 'FlipXDown' | 'FlipXUp' |
  'FlipYLeft' | 'FlipYRight' | 'SlideBottom' | 'SlideLeft' |
  'SlideRight' | 'SlideTop' | 'Zoom' | 'None';
```

### ResizeDirections

Resize handle directions:

```typescript
type ResizeDirections = 
  'All' | 'North' | 'South' | 'East' | 'West' |
  'NorthEast' | 'NorthWest' | 'SouthEast' | 'SouthWest';
```

### ButtonType

Button type enumeration:

```typescript
type ButtonType = 'Button' | 'Submit' | 'Reset';
```

### PositionDataModel

Position configuration:

```typescript
interface PositionDataModel {
  X: 'left' | 'center' | 'right' | number;
  Y: 'top' | 'center' | 'bottom' | number;
}
```

---

## Quick Reference

### Common Property Combinations

**Modal Confirmation Dialog:**
```jsx
<DialogComponent
  header="Confirm"
  isModal={true}
  showCloseIcon={true}
  buttons={[
    { buttonModel: { content: 'OK', isPrimary: true }, click: handleOK },
    { buttonModel: { content: 'Cancel' }, click: handleCancel }
  ]}
  width="400px"
  position={{ X: 'center', Y: 'center' }}
/>
```

**Draggable Tool Panel:**
```jsx
<DialogComponent
  header="Tools"
  isModal={false}
  allowDragging={true}
  enableResize={true}
  position={{ X: 100, Y: 100 }}
  width="300px"
  showCloseIcon={true}
/>
```

**Animated Modal:**
```jsx
<DialogComponent
  header="Welcome"
  isModal={true}
  animationSettings={{ effect: 'Zoom', duration: 400 }}
  position={{ X: 'center', Y: 'center' }}
  width="500px"
/>
```

**Localized Dialog:**
```jsx
<DialogComponent
  header="Dialog"
  locale="es"
  enableRtl={true}
  isModal={true}
/>
```

### Event Examples

```jsx
<DialogComponent
  ref={dialogRef}
  header="Event Example"
  beforeOpen={(args) => console.log('Before open')}
  open={(args) => console.log('Opened')}
  beforeClose={(args) => console.log('Before close')}
  close={(args) => console.log('Closed')}
  dragStart={(args) => console.log('Drag started')}
  drag={(args) => console.log('Dragging')}
  dragStop={(args) => console.log('Drag stopped')}
/>
```

---

**Source:** [Syncfusion EJ2 React Dialog API Documentation](https://ej2.syncfusion.com/react/documentation/api/dialog/overview)

