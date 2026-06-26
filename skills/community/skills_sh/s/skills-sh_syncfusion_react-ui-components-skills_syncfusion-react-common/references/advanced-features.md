# Advanced Features and Utilities

## Table of Contents
- [Animation Effects](#animation-effects)
- [Animation Timing](#animation-timing)
- [Global Animation Control](#global-animation-control)
- [Drag and Drop](#drag-and-drop)
- [Draggable Configuration](#draggable-configuration)
- [Droppable Configuration](#droppable-configuration)
- [Template Customization](#template-customization)
- [State Persistence](#state-persistence)
- [Security Best Practices](#security-best-practices)

## Animation Effects

The Animation utility creates smooth visual transitions for HTML elements. Syncfusion provides built-in animation effects that enhance user experience.

### Available Animation Effects

- **Fade:** `FadeIn`, `FadeOut`, `FadeZoomIn`, `FadeZoomOut`
- **Flip:** `FlipLeftDownIn`, `FlipLeftDownOut`, `FlipLeftUpIn`, `FlipLeftUpOut`, `FlipRightDownIn`, `FlipRightDownOut`, `FlipRightUpIn`, `FlipRightUpOut`, `FlipXDownIn`, `FlipXDownOut`, `FlipXUpIn`, `FlipXUpOut`, `FlipYLeftIn`, `FlipYLeftOut`, `FlipYRightIn`, `FlipYRightOut`
- **Slide:** `SlideBottomIn`, `SlideBottomOut`, `SlideDownIn`, `SlideDownOut`, `SlideLeftIn`, `SlideLeftOut`, `SlideRightIn`, `SlideRightOut`, `SlideTopIn`, `SlideTopOut`, `SlideUpIn`, `SlideUpOut`
- **Zoom:** `ZoomIn`, `ZoomOut`
- **None:** Disables animation

### Basic Animation Example

```typescript
import * as React from 'react';
import { useEffect, useRef } from 'react';
import { Animation } from '@syncfusion/ej2-base';

function App() {
  const element1 = useRef(null);
  const element2 = useRef(null);

  useEffect(() => {
    const animation = new Animation();
    
    // Apply FadeOut to element1
    if (element1.current) {
      animation.animate(element1.current, { name: 'FadeOut' });
    }
    
    // Apply ZoomOut to element2
    if (element2.current) {
      animation.animate(element2.current, { name: 'ZoomOut' });
    }
  }, []);

  return (
    <div id="container">
      <div id="element1" ref={element1} style={{ width: '100px', height: '100px', backgroundColor: '#4CAF50' }} />
      <div id="element2" ref={element2} style={{ width: '100px', height: '100px', backgroundColor: '#2196F3' }} />
    </div>
  );
}

export default App;
```

## Animation Timing

Control animation speed and timing with `duration` and `delay` properties:

- **duration:** Total time in milliseconds for animation to complete (default: 400ms)
- **delay:** Time in milliseconds before animation starts (default: 0ms)

```typescript
import * as React from 'react';
import { useEffect, useRef } from 'react';
import { Animation } from '@syncfusion/ej2-base';

function App() {
  const element1 = useRef(null);
  const element2 = useRef(null);

  useEffect(() => {
    // Create animation with custom timing
    const animation = new Animation({ delay: 2000, duration: 5000 });
    
    if (element1.current) {
      animation.animate(element1.current, { name: 'FadeOut' });
    }
    
    if (element2.current) {
      animation.animate(element2.current, { name: 'ZoomOut' });
    }
  }, []);

  return (
    <div id="container">
      <div id="element1" ref={element1} style={{ width: '100px', height: '100px', backgroundColor: '#FF9800' }} />
      <div id="element2" ref={element2} style={{ width: '100px', height: '100px', backgroundColor: '#E91E63' }} />
    </div>
  );
}

export default App;
```

## Global Animation Control

Control animations for all Syncfusion components globally:

```typescript
import { GlobalAnimationMode, setGlobalAnimation } from "@syncfusion/ej2-base";

// Call in your application entry point before initializing components

// Enable animations globally (overrides component settings)
setGlobalAnimation(GlobalAnimationMode.Enable);

// Disable animations globally (overrides component settings)
setGlobalAnimation(GlobalAnimationMode.Disable);

// Use component's own animation settings (default)
setGlobalAnimation(GlobalAnimationMode.Default);
```

**Note:** The `setGlobalAnimation` method controls JavaScript-based animations through component APIs and the Animation library. It does not affect CSS-based animations or direct style-based animation properties.

## Drag and Drop

Implement custom drag-and-drop interactions using Draggable and Droppable utilities from `@syncfusion/ej2-base`.

### Draggable Utility

Transform any DOM element into a draggable item:

```typescript
import * as React from 'react';
import { useEffect } from 'react';
import { Draggable } from '@syncfusion/ej2-base';

function App() {
  useEffect(() => {
    // Create draggable element
    const draggable = new Draggable(document.getElementById('element'), { clone: false });
  }, []);

  return (
    <div id='container'>
      <div id='element' style={{ width: '100px', height: '100px', backgroundColor: '#4CAF50', cursor: 'move', padding: '10px' }}>
        <p>Draggable Element</p>
      </div>
    </div>
  );
}

export default App;
```

## Draggable Configuration

### Clone Option

Create a visual copy during drag operation:

```typescript
const draggable = new Draggable(document.getElementById('element'), { clone: true });
```

When `clone: true`, the original element stays in place while a copy follows the cursor.

### Drag Area Constraint

Restrict dragging to a specific region:

```typescript
const draggable = new Draggable(document.getElementById('draggable'), { 
  clone: false, 
  dragArea: "#droppable"  // Restrict to #droppable container
});
```

### Complete Draggable Example

```typescript
import * as React from 'react';
import { useEffect } from 'react';
import { Draggable } from '@syncfusion/ej2-base';

function App() {
  useEffect(() => {
    // Draggable with clone and drag area constraints
    const draggable = new Draggable(document.getElementById('draggable'), { 
      clone: false, 
      dragArea: "#droppable" 
    });
  }, []);

  return (
    <div id='container'>
      <div id='droppable' style={{ border: '2px dashed #ccc', padding: '20px', minHeight: '200px' }}>
        <p>Drag Area</p>
      </div>
      <div id='draggable' style={{ width: '100px', height: '100px', backgroundColor: '#4CAF50', cursor: 'move', marginTop: '10px' }}>
        <p id='drag'>Draggable Element</p>
      </div>
    </div>
  );
}

export default App;
```

## Droppable Configuration

A droppable zone accepts and responds to draggable elements:

```typescript
import * as React from 'react';
import { useEffect } from 'react';
import { Draggable, Droppable, DropEventArgs } from '@syncfusion/ej2-base';

function App() {
  useEffect(() => {
    const draggable = new Draggable(document.getElementById('draggable'), { clone: false });
    
    const droppable = new Droppable(document.getElementById('droppable'), {
      drop: (e: DropEventArgs) => {
        // Handle drop event
        e.droppedElement.querySelector('#drag').textContent = 'Dropped Successfully!';
        console.log('Dropped element:', e.droppedElement);
        console.log('Target:', e.target);
      }
    });
  }, []);

  return (
    <div id='container'>
      <div id='droppable' style={{ border: '2px solid #2196F3', padding: '20px', minHeight: '200px', backgroundColor: '#E3F2FD' }}>
        <p>Drop Zone</p>
      </div>
      <div id='draggable' style={{ width: '100px', height: '100px', backgroundColor: '#4CAF50', cursor: 'move', marginTop: '10px' }}>
        <p id='drag'>Draggable</p>
      </div>
    </div>
  );
}

export default App;
```

## Template Customization

Templates allow customizing component layouts with React components:

```typescript
import './App.css';
import * as React from 'react';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { ColumnDirective, ColumnsDirective, GridComponent } from '@syncfusion/ej2-react-grids';

export default function App() {
  const data = [
    { OrderID: 10248, CustomerID: 'VINET', ShipCountry: 'France' },
    { OrderID: 10249, CustomerID: 'TOMSP', ShipCountry: 'Germany' },
    { OrderID: 10250, CustomerID: 'HANAR', ShipCountry: 'Brazil' }
  ];

  // Template function receives row data as props
  function gridTemplate(props) {
    return (
      <div className='custom'>
        <ButtonComponent>{props.ShipCountry}</ButtonComponent>
      </div>
    );
  }

  return (
    <GridComponent dataSource={data}>
      <ColumnsDirective>
        <ColumnDirective field='OrderID' width='100' />
        <ColumnDirective field='CustomerID' width='100' />
        <ColumnDirective field='ShipCountry' width='100' template={gridTemplate} />
      </ColumnsDirective>
    </GridComponent>
  );
}
```

### Stateless Templates for Performance

Exclude templates from state-driven re-renders to improve performance:

```typescript
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

function nodeTemplate(props) {
  return <span>{props.text}</span>;
}

function App() {
  return (
    <TreeViewComponent 
      fields={fields}
      // Exclude nodeTemplate from React state updates
      statelessTemplates={['nodeTemplate']}
      nodeTemplate={nodeTemplate}
    />
  );
}
```

For Grid with nested directives:

```typescript
<GridComponent dataSource={data} statelessTemplates={['directiveTemplates']}>
  <ColumnsDirective>
    <ColumnDirective field="name" headerText="Name" />
    <ColumnDirective field="status" headerText="Status" template={renderStatusCell} />
  </ColumnsDirective>
</GridComponent>
```

## State Persistence

Automatically persist component state to browser localStorage across page refreshes:

```typescript
import { GridComponent } from '@syncfusion/ej2-react-grids';

export let data: Object[] = [
    { OrderID: 10248, CustomerID: 'VINET', EmployeeID: 5, ShipCountry: 'France', Freight: 32.38 }
];

function App() {
  const pageSettings = { pageSize: 6 };

  return (
    <GridComponent 
      dataSource={data}
      enablePersistence={true}  // Enable persistence
      allowPaging={true}
      pageSettings={pageSettings}
    >
      {/* Grid content */}
    </GridComponent>
  );
}

export default App;
```
### Managing Persisted Data

```typescript
// Clear persisted state for a component
localStorage.removeItem('grid-state-key');

// Disable persistence
<GridComponent enablePersistence={false} ... />
```

## Security Best Practices

When working with Syncfusion React components, follow secure coding practices to protect your application and user data.

> **Note:** For comprehensive security guidelines and best practices, please refer to the [Syncfusion Security Documentation](https://ej2.syncfusion.com/react/documentation/common/security).

