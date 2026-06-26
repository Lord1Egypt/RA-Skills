# Dashboard Layout Events Reference

## Table of Contents
- [Overview](#overview)
- [Lifecycle Events](#lifecycle-events)
- [Interaction Events](#interaction-events)
- [Event Arguments](#event-arguments)
- [Common Event Patterns](#common-event-patterns)

## Overview

Dashboard Layout provides comprehensive events for monitoring component lifecycle, user interactions, and panel changes. Events are triggered at specific moments during drag, resize, add/remove operations, and layout changes.

## Lifecycle Events

### created

Triggers when the Dashboard Layout component is fully created and initialized.

**Event Type:** `EmitType<Object>`

**Example:**
```tsx
import { DashboardLayoutComponent } from '@syncfusion/ej2-react-layouts';

<DashboardLayoutComponent
  panels={panels}
  created={(args) => {
    console.log('Dashboard Layout created successfully');
  }}
>
</DashboardLayoutComponent>
```

**Use Case:** Initialize dependent components or load user preferences after dashboard is ready.

### destroyed

Triggers when the Dashboard Layout component is destroyed.

**Event Type:** `EmitType<Object>`

**Example:**
```tsx
<DashboardLayoutComponent
  panels={panels}
  destroyed={(args) => {
    console.log('Dashboard Layout destroyed');
    // Cleanup resources
  }}
>
</DashboardLayoutComponent>
```

**Use Case:** Clean up event listeners, timers, or external resources.

## Interaction Events

### dragStart

Triggers when a panel is about to start being dragged. Use this event to prevent dragging certain panels or implement custom behavior.

**Event Type:** `EmitType<DragStartArgs>`

**Event Arguments:**
- `element` (`HTMLElement`): The panel element being dragged
- `event` (`MouseEvent | TouchEvent`): Original mouse or touch event

**Example:**
```tsx
const handleDragStart = (args: DragStartArgs) => {
  console.log('Drag started on element:', args.element.id);
  
  // Prevent dragging of specific panel
  if (args.element.id === 'locked-panel') {
    args.cancel = true; // Cancel the drag operation
  }
};

<DashboardLayoutComponent
  panels={panels}
  allowDragging={true}
  dragStart={handleDragStart}
>
</DashboardLayoutComponent>
```

### drag

Triggers continuously while a panel is being dragged. Called on every mouse/touch movement during drag.

**Event Type:** `EmitType<DraggedEventArgs>`

**Event Arguments:**
- `element` (`HTMLElement`): The panel element being dragged
- `target` (`HTMLElement`): The element below the dragged panel
- `event` (`MouseEvent | TouchEvent`): Original mouse or touch event

**Example:**
```tsx
const handleDrag = (args: DraggedEventArgs) => {
  // Track drag progress
  console.log('Dragging panel over:', args.target.id);
  
  // Implement custom visual feedback
  if (args.target) {
    args.target.style.backgroundColor = 'lightblue';
  }
};

<DashboardLayoutComponent
  panels={panels}
  allowDragging={true}
  drag={handleDrag}
>
</DashboardLayoutComponent>
```

### dragStop

Triggers when a dragged panel is dropped at its final position.

**Event Type:** `EmitType<DragStopArgs>`

**Event Arguments:**
- `element` (`HTMLElement`): The dropped panel element
- `target` (`HTMLElement`): The element below where panel was dropped
- `event` (`MouseEvent | TouchEvent`): Original mouse or touch event

**Example:**
```tsx
const handleDragStop = (args: DragStopArgs) => {
  console.log('Panel dropped successfully');
  
  // Log final position
  const panelId = args.element.id;
  console.log(`Panel ${panelId} dropped on:`, args.target?.id);
  
  // Save layout after drag
  saveLayoutToStorage();
};

<DashboardLayoutComponent
  panels={panels}
  allowDragging={true}
  dragStop={handleDragStop}
>
</DashboardLayoutComponent>
```

### resizeStart

Triggers when a panel is about to start being resized.

**Event Type:** `EmitType<ResizeArgs>`

**Event Arguments:**
- `element` (`HTMLElement`): The panel element being resized
- `panels` (`PanelModel[]`): Model values of panels before resize
- `event` (`MouseEvent | TouchEvent`): Original mouse or touch event
- `isInteracted` (`boolean`): Whether resized by user interaction

**Example:**
```tsx
const handleResizeStart = (args: ResizeArgs) => {
  console.log('Resize started on:', args.element.id);
  console.log('Current panel state:', args.panels);
  
  // Prevent resizing specific panels
  if (args.element.classList.contains('fixed-size')) {
    args.cancel = true;
  }
};

<DashboardLayoutComponent
  panels={panels}
  allowResizing={true}
  resizeStart={handleResizeStart}
>
</DashboardLayoutComponent>
```

### resize

Triggers continuously while a panel is being resized.

**Event Type:** `EmitType<ResizeArgs>`

**Event Arguments:**
- `element` (`HTMLElement`): The panel being resized
- `panels` (`PanelModel[]`): Current panel configurations being modified
- `event` (`MouseEvent | TouchEvent`): Original mouse or touch event
- `isInteracted` (`boolean`): Whether resized by user interaction

**Example:**
```tsx
const handleResize = (args: ResizeArgs) => {
  // Get current panel dimensions
  const width = args.element.offsetWidth;
  const height = args.element.offsetHeight;
  
  console.log(`Resizing to: ${width}px x ${height}px`);
  
  // Track panels affected by resize
  args.panels.forEach(panel => {
    console.log(`Panel ${panel.id}: ${panel.sizeX} x ${panel.sizeY}`);
  });
};

<DashboardLayoutComponent
  panels={panels}
  allowResizing={true}
  resize={handleResize}
>
</DashboardLayoutComponent>
```

### resizeStop

Triggers when a panel resize is completed.

**Event Type:** `EmitType<ResizeArgs>`

**Event Arguments:**
- `element` (`HTMLElement`): The resized panel element
- `panels` (`PanelModel[]`): Final panel configurations after resize
- `event` (`MouseEvent | TouchEvent`): Original mouse or touch event
- `isInteracted` (`boolean`): Whether resized by user interaction

**Example:**
```tsx
const handleResizeStop = (args: ResizeArgs) => {
  console.log('Resize completed');
  
  // Save final layout
  const finalLayout = args.panels;
  localStorage.setItem('layoutAfterResize', JSON.stringify(finalLayout));
  
  // Notify user
  console.log('Layout saved after resize');
};

<DashboardLayoutComponent
  panels={panels}
  allowResizing={true}
  resizeStop={handleResizeStop}
>
</DashboardLayoutComponent>
```

### change

Triggers whenever panels' positions are changed (add, remove, move, drag, resize).

**Event Type:** `EmitType<ChangeEventArgs>`

**Event Arguments - ChangeEventArgs:**
- `addedPanels` (`PanelModel[]`): Panels newly added
- `removedPanels` (`PanelModel[]`): Panels removed
- `changedPanels` (`PanelModel[]`): Panels whose position changed
- `isInteracted` (`boolean`): True if changed by user, false if programmatic

**Example:**
```tsx
const handleChange = (args: ChangeEventArgs) => {
  console.log('Dashboard layout changed');
  
  // Track additions
  if (args.addedPanels.length > 0) {
    console.log('Added panels:', args.addedPanels.map(p => p.id));
  }
  
  // Track removals
  if (args.removedPanels.length > 0) {
    console.log('Removed panels:', args.removedPanels.map(p => p.id));
  }
  
  // Track position changes
  if (args.changedPanels.length > 0) {
    console.log('Panels with position changes:', args.changedPanels);
  }
  
  // Distinguish user action from programmatic changes
  if (args.isInteracted) {
    console.log('Change triggered by user');
  } else {
    console.log('Change triggered programmatically');
  }
};

<DashboardLayoutComponent
  panels={panels}
  change={handleChange}
>
</DashboardLayoutComponent>
```

## Event Arguments

### DragStartArgs
```typescript
interface DragStartArgs {
  element: HTMLElement;      // Panel being dragged
  event: MouseEvent | TouchEvent;  // Original mouse/touch event
  cancel?: boolean;           // Set to true to cancel drag
}
```

### DraggedEventArgs
```typescript
interface DraggedEventArgs {
  element: HTMLElement;       // Panel being dragged
  target: HTMLElement;        // Element below panel
  event: MouseEvent | TouchEvent;  // Original mouse/touch event
}
```

### ResizeArgs
```typescript
interface ResizeArgs {
  element: HTMLElement;       // Panel being resized
  event: MouseEvent | TouchEvent;  // Original mouse/touch event
  panels: PanelModel[];        // Current panel configurations
  isInteracted: boolean;       // User-triggered or programmatic
  cancel?: boolean;            // Set to true to cancel resize
}
```

### ChangeEventArgs
```typescript
interface ChangeEventArgs {
  addedPanels: PanelModel[];   // Newly added panels
  removedPanels: PanelModel[]; // Removed panels
  changedPanels: PanelModel[]; // Panels with position changes
  isInteracted: boolean;       // User-triggered or programmatic
}
```

## Common Event Patterns

### Complete Event Handling Setup

```tsx
import { useRef } from 'react';
import { DashboardLayoutComponent } from '@syncfusion/ej2-react-layouts';
import { 
  DragStartArgs, 
  DragStopArgs, 
  ResizeArgs, 
  ChangeEventArgs 
} from '@syncfusion/ej2-react-layouts';

export const FullEventDashboard = () => {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);

  const handleDragStart = (args: DragStartArgs) => {
    console.log('Drag start:', args.element.id);
  };

  const handleDrag = (args: DraggedEventArgs) => {
    console.log('Dragging over:', args.target?.id);
  };

  const handleDragStop = (args: DragStopArgs) => {
    console.log('Drag stop:', args.element.id);
    saveDashboardState();
  };

  const handleResizeStart = (args: ResizeArgs) => {
    console.log('Resize start:', args.element.id);
  };

  const handleResize = (args: ResizeArgs) => {
    console.log('Resizing, panels changed:', args.panels.length);
  };

  const handleResizeStop = (args: ResizeArgs) => {
    console.log('Resize stop:', args.element.id);
    saveDashboardState();
  };

  const handleChange = (args: ChangeEventArgs) => {
    if (args.addedPanels.length) console.log('Added:', args.addedPanels);
    if (args.removedPanels.length) console.log('Removed:', args.removedPanels);
    if (args.changedPanels.length) console.log('Changed:', args.changedPanels);
  };

  const saveDashboardState = () => {
    const layout = dashboardRef.current?.serialize();
    localStorage.setItem('dashboardState', JSON.stringify(layout));
  };

  return (
    <DashboardLayoutComponent
      ref={dashboardRef}
      columns={5}
      panels={panels}
      allowDragging={true}
      allowResizing={true}
      dragStart={handleDragStart}
      drag={handleDrag}
      dragStop={handleDragStop}
      resizeStart={handleResizeStart}
      resize={handleResize}
      resizeStop={handleResizeStop}
      change={handleChange}
      created={() => console.log('Dashboard created')}
      destroyed={() => console.log('Dashboard destroyed')}
    >
    </DashboardLayoutComponent>
  );
};
```

### Audit Trail and Logging

```tsx
const auditLog: any[] = [];

const handleChange = (args: ChangeEventArgs) => {
  const timestamp = new Date().toISOString();
  
  if (args.addedPanels.length > 0) {
    auditLog.push({
      timestamp,
      action: 'PANEL_ADDED',
      panels: args.addedPanels.map(p => p.id),
      isUserAction: args.isInteracted
    });
  }
  
  if (args.removedPanels.length > 0) {
    auditLog.push({
      timestamp,
      action: 'PANEL_REMOVED',
      panels: args.removedPanels.map(p => p.id),
      isUserAction: args.isInteracted
    });
  }
  
  if (args.changedPanels.length > 0) {
    auditLog.push({
      timestamp,
      action: 'LAYOUT_CHANGED',
      panelCount: args.changedPanels.length,
      isUserAction: args.isInteracted
    });
  }
};
```

### Error Prevention and Validation

```tsx
const handleDragStart = (args: DragStartArgs) => {
  const panelId = args.element.id;
  
  // Prevent dragging locked panels
  if (lockedPanels.includes(panelId)) {
    args.cancel = true;
    showNotification('This panel cannot be moved');
  }
  
  // Prevent dragging during data load
  if (isLoading) {
    args.cancel = true;
    showNotification('Wait for data to load first');
  }
};

const handleResizeStart = (args: ResizeArgs) => {
  const panelId = args.element.id;
  
  // Prevent resizing panels below minimum content size
  if (requiredMinSize[panelId] && args.panels) {
    const panel = args.panels.find(p => p.id === panelId);
    if (panel && panel.sizeX < requiredMinSize[panelId]) {
      args.cancel = true;
      showNotification('Panel size is too small for its content');
    }
  }
};
```
