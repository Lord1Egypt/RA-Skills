# Positioning and Dragging

## Table of Contents
- [Built-in Positions](#built-in-positions)
- [Custom Position Coordinates](#custom-position-coordinates)
- [Position Property Examples](#position-property-examples)
- [Draggable Dialogs](#draggable-dialogs)
- [Container Constraints](#container-constraints)
- [Resize Configuration](#resize-configuration)
- [Common Use Cases](#common-use-cases)

## Built-in Positions

The Dialog supports preset positions using the `position` object. Use X and Y properties with string values:

```jsx
<DialogComponent position={{ X: 'center', Y: 'center' }}>
  Positioned at center
</DialogComponent>
```

### Position Options

X-axis values: `'left'`, `'center'`, `'right'`, or pixel value (number)  
Y-axis values: `'top'`, `'center'`, `'bottom'`, or pixel value (number)

| X Value | Y Value | Result | Example |
|---------|---------|--------|---------|
| `'left'` | `'top'` | Top-left corner | `{ X: 'left', Y: 'top' }` |
| `'center'` | `'top'` | Top-center | `{ X: 'center', Y: 'top' }` |
| `'right'` | `'top'` | Top-right corner | `{ X: 'right', Y: 'top' }` |
| `'left'` | `'center'` | Middle-left | `{ X: 'left', Y: 'center' }` |
| `'center'` | `'center'` | Center | `{ X: 'center', Y: 'center' }` |
| `'right'` | `'center'` | Middle-right | `{ X: 'right', Y: 'center' }` |
| `'left'` | `'bottom'` | Bottom-left | `{ X: 'left', Y: 'bottom' }` |
| `'center'` | `'bottom'` | Bottom-center | `{ X: 'center', Y: 'bottom' }` |
| `'right'` | `'bottom'` | Bottom-right | `{ X: 'right', Y: 'bottom' }` |

### Visual Layout

```
{ X: 'left',    { X: 'center',    { X: 'right',
  Y: 'top' }      Y: 'top' }        Y: 'top' }
   │               │                 │
   ├───────────┬──┼──┬──────────────┤
   │           │  │  │              │
   │ { X: 'left',  { X: 'center',   { X: 'right',
   │   Y: 'center' Y: 'center' }    Y: 'center' }
   │           │  │  │              │
   ├───────────┼──┼──┼──────────────┤
   │           │  │  │              │
{ X: 'left',    { X: 'center',    { X: 'right',
  Y: 'bottom' }  Y: 'bottom' }    Y: 'bottom' }
```

### Using Preset Positions

```jsx
import React, { useRef, useState } from 'react';
import { DialogComponent } from '@syncfusion/ej2-react-popups';
import '@syncfusion/ej2-base/styles/material.css';
import '@syncfusion/ej2-popups/styles/material.css';

export default function App() {
  const dialogRef = useRef(null);
  const [position, setPosition] = useState({ X: 'center', Y: 'center' });

  const positions = [
    { label: 'Top Left', value: { X: 'left', Y: 'top' } },
    { label: 'Top Center', value: { X: 'center', Y: 'top' } },
    { label: 'Top Right', value: { X: 'right', Y: 'top' } },
    { label: 'Middle Left', value: { X: 'left', Y: 'center' } },
    { label: 'Center', value: { X: 'center', Y: 'center' } },
    { label: 'Middle Right', value: { X: 'right', Y: 'center' } },
    { label: 'Bottom Left', value: { X: 'left', Y: 'bottom' } },
    { label: 'Bottom Center', value: { X: 'center', Y: 'bottom' } },
    { label: 'Bottom Right', value: { X: 'right', Y: 'bottom' } },
  ];

  return (
    <div id="dialog-target" style={{ position: 'relative', height: '600px', border: '1px solid #ccc' }}>
      <div style={{ padding: '20px' }}>
        <h3>Select Position:</h3>
        {positions.map((pos) => (
          <button
            key={pos.label}
            onClick={() => {
              setPosition(pos.value);
              dialogRef.current?.show();
            }}
            style={{ margin: '5px' }}
          >
            {pos.label}
          </button>
        ))}
      </div>

      <DialogComponent
        ref={dialogRef}
        header="Dialog"
        position={position}
        target="#dialog-target"
        showCloseIcon={true}
      >
        This dialog is positioned at: <strong>{position}</strong>
      </DialogComponent>
    </div>
  );
}
```

## Custom Position Coordinates

For precise positioning, use X and Y coordinates:

```jsx
<DialogComponent
  position={{ X: 100, Y: 50 }}
  header="Custom Position"
>
  100px from left, 50px from top
</DialogComponent>
```

### Position Object

```jsx
{
  X: number | string,  // Pixels or percentage from left
  Y: number | string   // Pixels or percentage from top
}
```

### Units

```jsx
// Pixels
<DialogComponent position={{ X: 200, Y: 100 }} />

// Percentage (relative to container width/height)
<DialogComponent position={{ X: '50%', Y: '25%' }} />

// String with units
<DialogComponent position={{ X: '10px', Y: '20px' }} />
```

### Centering Dialog Programmatically

```jsx
const centerDialog = (containerWidth, containerHeight) => {
  const dialogWidth = 400;
  const dialogHeight = 300;
  
  return {
    X: (containerWidth - dialogWidth) / 2,
    Y: (containerHeight - dialogHeight) / 2
  };
};

<DialogComponent
  position={centerDialog(800, 600)}
  width="400px"
  height="300px"
>
  Perfectly centered
</DialogComponent>
```

### Dynamic Positioning

```jsx
const [position, setPosition] = React.useState({ X: 100, Y: 100 });

const moveDialog = (direction) => {
  setPosition((prev) => {
    switch(direction) {
      case 'up': return { ...prev, Y: prev.Y - 20 };
      case 'down': return { ...prev, Y: prev.Y + 20 };
      case 'left': return { ...prev, X: prev.X - 20 };
      case 'right': return { ...prev, X: prev.X + 20 };
      default: return prev;
    }
  });
};

<DialogComponent
  position={position}
  header="Movable by Code"
>
  <div style={{ padding: '20px' }}>
    <button onClick={() => moveDialog('up')}>Up</button>
    <button onClick={() => moveDialog('down')}>Down</button>
    <button onClick={() => moveDialog('left')}>Left</button>
    <button onClick={() => moveDialog('right')}>Right</button>
  </div>
</DialogComponent>
```

## Position Property Examples

### Example 1: Sticky Top-Right (Notifications)

```jsx
<DialogComponent
  position={{ X: 'calc(100% - 350px)', Y: 10 }}
  width="320px"
  isModal={false}
  showCloseIcon={true}
>
  🔔 Notification message
</DialogComponent>
```

### Example 2: Offset from Click

```jsx
export function ContextMenuDialog() {
  const dialogRef = useRef(null);
  const [position, setPosition] = React.useState({ X: 0, Y: 0 });

  const handleContextMenu = (e) => {
    e.preventDefault();
    setPosition({ X: e.clientX, Y: e.clientY });
    dialogRef.current?.show();
  };

  return (
    <div
      onContextMenu={handleContextMenu}
      style={{ width: '100%', height: '400px', border: '1px solid #ccc', position: 'relative' }}
    >
      Right-click anywhere
      <DialogComponent
        ref={dialogRef}
        position={position}
        header="Context Menu"
        showCloseIcon={true}
        isModal={false}
      >
        <ul style={{ listStyle: 'none', padding: '10px', margin: 0 }}>
          <li><a href="#">Edit</a></li>
          <li><a href="#">Copy</a></li>
          <li><a href="#">Paste</a></li>
        </ul>
      </DialogComponent>
    </div>
  );
}
```

### Example 3: Relative to Window

```jsx
// Position relative to viewport instead of container
<DialogComponent
  position={{ X: 'center', Y: 'center' }}
  width="400px"
>
  Centered on screen
</DialogComponent>
```

## Draggable Dialogs

Enable users to drag the dialog around:

```jsx
<DialogComponent
  allowDragging={true}
  position={{ X: 100, Y: 100 }}
  header="Drag me around!"
>
  Click and drag the header to move this dialog
</DialogComponent>
```

### Draggable with Constraints

```jsx
<DialogComponent
  allowDragging={true}
  position={{ X: 50, Y: 50 }}
  dragArea="#dialog-target"  // Constrain to container
  header="Constrained Dragging"
>
  I cannot be dragged outside the container
</DialogComponent>
```

### Example: Floating Tool Panel

```jsx
export function FloatingToolPanel() {
  const dialogRef = useRef(null);

  return (
    <div id="dialog-target" style={{ position: 'relative', height: '600px', border: '1px solid #ccc' }}>
      <button onClick={() => dialogRef.current?.show()} className="e-btn">
        Open Tool
      </button>

      <DialogComponent
        ref={dialogRef}
        header="Tools"
        allowDragging={true}
        position={{ X: 200, Y: 100 }}
        width="250px"
        isModal={false}
        target="#dialog-target"
        showCloseIcon={true}
      >
        <div style={{ padding: '15px' }}>
          <button className="e-btn" style={{ width: '100%', marginBottom: '10px' }}>
            Tool 1
          </button>
          <button className="e-btn" style={{ width: '100%', marginBottom: '10px' }}>
            Tool 2
          </button>
          <button className="e-btn" style={{ width: '100%' }}>
            Tool 3
          </button>
        </div>
      </DialogComponent>
    </div>
  );
}
```

### Control Drag Behavior with Events

```jsx
export function ControlledDragging() {
  const dialogRef = useRef(null);
  const [isDragging, setIsDragging] = React.useState(false);

  const handleDragStart = (args) => {
    // You can prevent dragging based on conditions
    setIsDragging(true);
  };

  const handleDragStop = (args) => {
    setIsDragging(false);
  };

  return (
    <DialogComponent
      ref={dialogRef}
      allowDragging={true}
      header="Draggable Dialog"
      dragStart={handleDragStart}
      dragStop={handleDragStop}
    >
      <p>This dialog can be dragged by the header</p>
      <p>{isDragging ? 'Currently dragging...' : 'Not dragging'}</p>
    </DialogComponent>
  );
}
```

## Container Constraints

The `target` property constrains the dialog to a container:

```jsx
<div id="dialog-target" style={{ position: 'relative', width: '500px', height: '400px' }}>
  <DialogComponent
    target="#dialog-target"
    allowDragging={true}
    position={{ X: 50, Y: 50 }}
  >
    Dialog is constrained to this container
  </DialogComponent>
</div>
```

### Behavior:
- Dialog position is relative to container
- Modal overlay covers only the container
- Dragging limited to container boundaries

## Resize Configuration

### Enable Resizing

```jsx
<DialogComponent
  enableResize={true}
  resizeHandles={['All']}
  position={{ X: 100, Y: 100 }}
  width="400px"
  height="300px"
  header="Resizable Dialog"
>
  Drag the corner to resize
</DialogComponent>
```

### Min Height Size

```jsx
<DialogComponent
  enableResize={true}
  minHeight="200px"
  position={{ X: 100, Y: 100 }}
>
  Resizable with limits
</DialogComponent>
```

**Note:** Syncfusion Dialog supports `minHeight`

### Resize Handles

The resize handle appears in the bottom-right corner by default. This is auto-generated when `enableResize={true}`.

### Example: Draggable + Resizable Window

```jsx
export function WindowLike() {
  const dialogRef = useRef(null);

  return (
    <div id="dialog-target" style={{ position: 'relative', height: '600px' }}>
      <button onClick={() => dialogRef.current?.show()}>Open Window</button>

      <DialogComponent
        ref={dialogRef}
        header="My Window"
        allowDragging={true}
        enableResize={true}
        resizeHandles={['All']}
        minHeight="150px"
        position={{ X: 100, Y: 100 }}
        width="400px"
        height="300px"
        target="#dialog-target"
        showCloseIcon={true}
      >
        <p>Drag the header to move</p>
        <p>Drag the corner to resize</p>
      </DialogComponent>
    </div>
  );
}
```

## Common Use Cases

### Use Case 1: Help Tooltip (Top-Right)

```jsx
<DialogComponent
  position={{ X: 'calc(100% - 300px)', Y: 10 }}
  width="280px"
  isModal={false}
  header="Help"
  showCloseIcon={true}
>
  Click buttons to learn more
</DialogComponent>
```

### Use Case 2: Modal Center (Critical Alert)

```jsx
<DialogComponent
  position="Center"
  isModal={true}
  header="⚠️ Important Alert"
>
  Your action requires confirmation
</DialogComponent>
```

### Use Case 3: Floating Palette (Bottom-Left)

```jsx
<DialogComponent
  position={{ X: 10, Y: 'calc(100% - 310px)' }}
  allowDragging={true}
  isModal={false}
  width="300px"
  header="Color Palette"
>
  Select a color
</DialogComponent>
```

### Use Case 4: Context-Aware (Follow Cursor)

```jsx
export function ContextDialog() {
  const dialogRef = useRef(null);
  const [pos, setPos] = React.useState({ X: 0, Y: 0 });

  const handleHover = (e) => {
    setPos({ X: e.clientX + 10, Y: e.clientY + 10 });
  };

  return (
    <div onMouseMove={handleHover} style={{ height: '400px' }}>
      Hover here
      <DialogComponent
        position={pos}
        isModal={false}
        header="Info"
        width="200px"
      >
        Following your cursor
      </DialogComponent>
    </div>
  );
}
```

## Edge Cases

### Repositioning After Window Resize

```jsx
React.useEffect(() => {
  const handleWindowResize = () => {
    // Recalculate position if needed
    setPosition({
      X: window.innerWidth / 2 - 200,
      Y: window.innerHeight / 2 - 150
    });
  };

  window.addEventListener('resize', handleWindowResize);
  return () => window.removeEventListener('resize', handleWindowResize);
}, []);
```

### Preventing Drag Outside Container

The `target` property automatically prevents dragging outside its bounds. No additional code needed.

### Position State Persistence

```jsx
// Save position to localStorage
const savePosition = (newPos) => {
  localStorage.setItem('dialogPosition', JSON.stringify(newPos));
  setPosition(newPos);
};

// Restore on mount
React.useEffect(() => {
  const saved = localStorage.getItem('dialogPosition');
  if (saved) setPosition(JSON.parse(saved));
}, []);
```

**Next:** Choose another reference topic based on your needs.
