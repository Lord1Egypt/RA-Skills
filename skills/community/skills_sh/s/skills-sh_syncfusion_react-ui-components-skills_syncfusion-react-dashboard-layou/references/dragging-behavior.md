# Dragging and Moving Panels

## Table of Contents
- [Overview](#overview)
- [Enabling Drag Functionality](#enabling-drag-functionality)
- [Drag Events](#drag-events)
- [Collision and Pushing](#collision-and-pushing)
- [Custom Drag Handles](#custom-drag-handles)
- [Disabling Drag Operations](#disabling-drag-operations)
- [Visual Feedback](#visual-feedback)
- [Advanced Dragging](#advanced-dragging)
- [Best Practices](#best-practices)

## Overview

Dashboard Layout provides comprehensive dragging functionality for repositioning panels. When dragging a panel, the component automatically manages collisions, provides visual feedback, and triggers events at each stage of the operation.

### Dragging Capabilities

- **Drag-and-Drop**: Move panels to new positions
- **Collision Detection**: Automatic pushing of overlapping panels
- **Visual Preview**: Shows where panel will be placed
- **Event System**: Hooks into drag lifecycle
- **Custom Handles**: Restrict dragging to specific elements
- **Undo/Redo Support**: Track layout changes

## Enabling Drag Functionality

### Basic Setup

```tsx
import { DashboardLayoutComponent } from '@syncfusion/ej2-react-layouts';

function DraggableDashboard() {
  const panels = [
    {
      id: 'panel-1',
      header: 'Sales',
      content: '<div>Sales data</div>',
      row: 0,
      col: 0,
      sizeX: 2,
      sizeY: 2
    },
    {
      id: 'panel-2',
      header: 'Users',
      content: '<div>User data</div>',
      row: 0,
      col: 2,
      sizeX: 2,
      sizeY: 2
    }
  ];

  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={5}
      allowDragging={true}  // Enable dragging
      cellSpacing={[10, 10]}
    />
  );
}
```

### Default Dragging Behavior

By default:
- **Handle**: Entire panel is draggable (including header and content)
- **Visual**: Placeholder shows target position
- **Movement**: Free movement within grid bounds
- **Snap**: Aligns to grid cells automatically

## Drag Events

Dashboard Layout triggers three main events during dragging:

### Event Sequence

```
User presses mouse down on panel
         ↓
    dragStart event fires
         ↓
User moves mouse (dragging)
         ↓
    drag event fires (continuously)
         ↓
User releases mouse
         ↓
    dragStop event fires
```

### dragStart Event

Fires when user begins dragging a panel:

```tsx
function DashboardWithDragStart() {
  const handleDragStart = (args: DragStartEventArgs) => {
    console.log('Drag started:', {
      panelId: args.element?.id,
      position: {
        x: args.element?.offsetLeft,
        y: args.element?.offsetTop
      }
    });

    // Example: Prevent dragging specific panels
    if (args.element?.id === 'locked-panel') {
      args.cancel = true;
    }
  };

  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={5}
      allowDragging={true}
      dragStart={handleDragStart}
    />
  );
}
```

**Available Properties:**
- `element`: DOM element being dragged
- `event`: Mouse event object
- `cancel`: Set to true to prevent drag

### drag Event

Fires continuously while dragging:

```tsx
function DashboardWithDrag() {
  const [dragInfo, setDragInfo] = useState<string>('');

  const handleDrag = (args: DragEventArgs) => {
    const info = `Dragging: ${args.element?.id} - Position: (${args.event?.clientX}, ${args.event?.clientY})`;
    setDragInfo(info);
  };

  return (
    <div>
      <div>{dragInfo}</div>
      <DashboardLayoutComponent
        id='dashboard'
        panels={panels}
        columns={5}
        allowDragging={true}
        drag={handleDrag}
      />
    </div>
  );
}
```

**Use Cases:**
- Show real-time coordinates
- Update external UI based on cursor position
- Validate target positions
- Trigger animations

### dragStop Event

Fires when dragging completes:

```tsx
function DashboardWithDragStop() {
  const [lastDragInfo, setLastDragInfo] = useState<string>('');

  const handleDragStop = (args: DragStopEventArgs) => {
    const info = {
      panelId: args.element?.id,
      newPosition: {
        row: args.newIndex?.row,
        col: args.newIndex?.col
      },
      previousPosition: {
        row: args.oldIndex?.row,
        col: args.oldIndex?.col
      },
      moved: args.element?.id
    };

    setLastDragInfo(JSON.stringify(info, null, 2));
    
    // Save layout after drag
    saveLayout();
  };

  return (
    <div>
      <pre>{lastDragInfo}</pre>
      <DashboardLayoutComponent
        id='dashboard'
        panels={panels}
        columns={5}
        allowDragging={true}
        dragStop={handleDragStop}
      />
    </div>
  );
}
```

**Available Properties:**
- `element`: Panel that was dragged
- `newIndex`: New row/col position
- `oldIndex`: Previous row/col position
- `event`: Mouse event object

## Collision and Pushing

### How Collision Works

When a panel collides with another during dragging:
1. Collision detected automatically
2. Overlapping panel(s) pushed in available directions
3. Push direction: left, right, top, or bottom (whichever is available)
4. Real-time feedback shows target positions

### Example: Collision Behavior

```tsx
function DashboardWithCollision() {
  const panels = [
    {
      id: 'panel-1',
      header: 'Panel 1',
      content: '<div class="content">1</div>',
      row: 0,
      col: 0,
      sizeX: 1,
      sizeY: 1
    },
    {
      id: 'panel-2',
      header: 'Panel 2',
      content: '<div class="content">2</div>',
      row: 0,
      col: 1,
      sizeX: 3,
      sizeY: 2
    },
    {
      id: 'panel-3',
      header: 'Panel 3',
      content: '<div class="content">3</div>',
      row: 0,
      col: 4,
      sizeX: 1,
      sizeY: 3
    }
  ];

  const handleDragStop = (args: DragStopEventArgs) => {
    console.log(`Panel ${args.element?.id} moved to row ${args.newIndex?.row}, col ${args.newIndex?.col}`);
    // Panel 1 was dragged onto Panel 2
    // Panel 2 automatically pushed to adjacent position
  };

  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={5}
      cellSpacing={[10, 10]}
      allowDragging={true}
      dragStop={handleDragStop}
    />
  );
}
```

### Preventing Collision (Static Layout)

To prevent panels from being pushed, set `allowFloating` to false:

```tsx
<DashboardLayoutComponent
  id='dashboard'
  panels={panels}
  columns={5}
  allowDragging={true}
  allowFloating={false}  // Prevents automatic pushing
/>
```

## Custom Drag Handles

Restrict dragging to specific elements using `draggableHandle` property:

### Pattern 1: Header-Only Dragging

```tsx
function HeaderDragDashboard() {
  const panels = [
    {
      id: 'chart-panel',
      header: '<div class="panel-header">📊 Sales Chart</div>',
      content: '<canvas id="chart"></canvas>',
      row: 0,
      col: 0,
      sizeX: 2,
      sizeY: 2
    }
  ];

  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={5}
      allowDragging={true}
      draggableHandle='.panel-header'  // Only drag from header
    />
  );
}

// CSS
// .panel-header { cursor: move; user-select: none; }
```

### Pattern 2: Icon-Only Dragging

```tsx
function IconDragDashboard() {
  const panels = [
    {
      id: 'widget',
      header: '<div><span class="drag-icon">≡</span> Widget Title</div>',
      content: '<div>Widget content</div>',
      row: 0,
      col: 0,
      sizeX: 2,
      sizeY: 1
    }
  ];

  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={5}
      allowDragging={true}
      draggableHandle='.drag-icon'  // Only drag from icon
    />
  );
}

// CSS
// .drag-icon { cursor: grab; font-weight: bold; padding: 8px; }
// .drag-icon:active { cursor: grabbing; }
```

### Pattern 3: Multiple Handles

```tsx
function MultiHandleDashboard() {
  const panels = [
    {
      id: 'complex-panel',
      header: `
        <div class="header-controls">
          <span class="header-title">Panel Title</span>
          <div class="drag-handle">↕</div>
        </div>
      `,
      content: '<div>Content here</div>',
      row: 0,
      col: 0,
      sizeX: 2,
      sizeY: 2
    }
  ];

  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={5}
      allowDragging={true}
      draggableHandle='.header-title, .drag-handle'  // Multiple selectors
    />
  );
}
```

## Disabling Drag Operations

### Pattern 1: Disable for Specific Panels

```tsx
function MixedDragDashboard() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);

  const handleDragStart = (args: DragStartEventArgs) => {
    const panelId = args.element?.id;
    
    // List of panels that cannot be dragged
    const lockedPanels = ['locked-1', 'locked-2', 'header-panel'];
    
    if (lockedPanels.includes(panelId)) {
      args.cancel = true;  // Prevent drag
    }
  };

  return (
    <DashboardLayoutComponent
      ref={dashboardRef}
      id='dashboard'
      panels={panels}
      columns={5}
      allowDragging={true}
      dragStart={handleDragStart}
    />
  );
}
```

### Pattern 2: Disable All Dragging

```tsx
function StaticDashboard() {
  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={5}
      allowDragging={false}  // Disable all dragging
    />
  );
}
```

### Pattern 3: Conditional Disabling Based on User Role

```tsx
function RoleBasedDragDashboard() {
  const [userRole, setUserRole] = useState('viewer');
  const canEditLayout = userRole === 'admin' || userRole === 'editor';

  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={5}
      allowDragging={canEditLayout}
      disabled={!canEditLayout}
    />
  );
}
```

## Visual Feedback

### Placeholder During Drag

The placeholder shows where the panel will be positioned:

```css
/* Customize placeholder styling */
.e-placeholder {
  border: 2px dashed #2196F3;
  background: rgba(33, 150, 243, 0.1);
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.2);
}
```

### Dragging Panel Visual State

```css
/* Panel being dragged */
.e-panel.e-dragging {
  opacity: 0.8;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
  z-index: 1000;
}

/* Dragging animation */
.e-panel.e-dragging {
  transition: none;  /* Disable transitions during drag */
}
```

### Custom Drag Feedback

```tsx
function CustomDragFeedbackDashboard() {
  const [draggingPanel, setDraggingPanel] = useState<string | null>(null);

  const handleDragStart = (args: DragStartEventArgs) => {
    setDraggingPanel(args.element?.id || null);
  };

  const handleDragStop = () => {
    setDraggingPanel(null);
  };

  return (
    <div>
      {draggingPanel && (
        <div className="drag-indicator">
          Moving: {draggingPanel}
        </div>
      )}
      <DashboardLayoutComponent
        id='dashboard'
        panels={panels}
        columns={5}
        allowDragging={true}
        dragStart={handleDragStart}
        dragStop={handleDragStop}
      />
    </div>
  );
}
```

## Advanced Dragging

### Programmatic Panel Movement

Move panels via `movePanel` method:

```tsx
function ProgrammaticMoveDashboard() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);

  const movePanel = (panelId: string, newRow: number, newCol: number) => {
    dashboardRef.current?.movePanel(panelId, newRow, newCol);
  };

  const arrangeInGrid = () => {
    movePanel('panel-1', 0, 0);
    movePanel('panel-2', 0, 2);
    movePanel('panel-3', 0, 4);
  };

  return (
    <div>
      <button onClick={arrangeInGrid}>Arrange in Grid</button>
      <DashboardLayoutComponent
        ref={dashboardRef}
        id='dashboard'
        panels={panels}
        columns={5}
        allowDragging={true}
      />
    </div>
  );
}
```

### Undo/Redo Dragging

```tsx
function UndoRedoDashboard() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [historyIndex, setHistoryIndex] = useState(-1);

  const recordState = () => {
    const currentState = dashboardRef.current?.serialize();
    const newHistory = history.slice(0, historyIndex + 1);
    newHistory.push(currentState);
    setHistory(newHistory);
    setHistoryIndex(newHistory.length - 1);
  };

  const undo = () => {
    if (historyIndex > 0) {
      const newIndex = historyIndex - 1;
      dashboardRef.current!.panels = history[newIndex];
      setHistoryIndex(newIndex);
    }
  };

  const redo = () => {
    if (historyIndex < history.length - 1) {
      const newIndex = historyIndex + 1;
      dashboardRef.current!.panels = history[newIndex];
      setHistoryIndex(newIndex);
    }
  };

  return (
    <div>
      <button onClick={undo} disabled={historyIndex <= 0}>Undo</button>
      <button onClick={redo} disabled={historyIndex >= history.length - 1}>Redo</button>
      <DashboardLayoutComponent
        ref={dashboardRef}
        id='dashboard'
        panels={panels}
        columns={5}
        allowDragging={true}
        dragStop={recordState}
      />
    </div>
  );
}
```

### Drag Constraints

Limit which areas panels can be dragged to:

```tsx
function ConstrainedDragDashboard() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);

  const handleDragStart = (args: DragStartEventArgs) => {
    const panelId = args.element?.id;
    
    // Prevent specific panels from moving to certain areas
    if (panelId === 'priority-panel') {
      // Can only be in top row
      // Additional validation needed
    }
  };

  const handleDragStop = (args: DragStopEventArgs) => {
    const newRow = args.newIndex?.row || 0;

    // Revert if moved to restricted area
    if (args.element?.id === 'top-only-panel' && newRow > 0) {
      // Restore to previous position
      dashboardRef.current?.movePanel(
        args.element.id,
        args.oldIndex?.row || 0,
        args.oldIndex?.col || 0
      );
    }
  };

  return (
    <DashboardLayoutComponent
      ref={dashboardRef}
      id='dashboard'
      panels={panels}
      columns={5}
      allowDragging={true}
      dragStop={handleDragStop}
    />
  );
}
```

## Best Practices

### 1. Always Enable Drag Event Handlers

```tsx
// ✅ RECOMMENDED: Track all drag lifecycle events
function BestPracticeDashboard() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);
  const [dragState, setDragState] = useState('idle');

  return (
    <div>
      <div>State: {dragState}</div>
      <DashboardLayoutComponent
        ref={dashboardRef}
        id='dashboard'
        panels={panels}
        columns={5}
        allowDragging={true}
        dragStart={() => setDragState('dragging')}
        dragStop={() => {
          setDragState('dropped');
          setTimeout(() => setDragState('idle'), 500);
        }}
      />
    </div>
  );
}
```

### 2. Provide Visual Feedback

```tsx
// ✅ RECOMMENDED: Clear visual indicators
.e-panel {
  transition: all 0.2s ease;
}

.e-panel.e-dragging {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  opacity: 0.9;
}

.e-placeholder {
  border: 2px dashed #2196F3;
  background: rgba(33, 150, 243, 0.08);
  animation: pulse 1s infinite;
}
```

### 3. Save After Drag Stops

```tsx
// ✅ RECOMMENDED: Persist layout after drag
function PersistentDragDashboard() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);

  const handleDragStop = () => {
    const layout = dashboardRef.current?.serialize();
    localStorage.setItem('dashboard-layout', JSON.stringify(layout));
  };

  return (
    <DashboardLayoutComponent
      ref={dashboardRef}
      id='dashboard'
      panels={panels}
      columns={5}
      allowDragging={true}
      dragStop={handleDragStop}
    />
  );
}
```

### 4. Use Proper Drag Handles for Content-Heavy Panels

```tsx
// ✅ RECOMMENDED: For complex panels, limit drag area
function HandleDashboard() {
  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={5}
      allowDragging={true}
      draggableHandle='.e-panel-header'  // Only header is draggable
    />
  );
}
```

### 5. Test Keyboard Accessibility

```tsx
// ✅ RECOMMENDED: Ensure keyboard support
function AccessibleDragDashboard() {
  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === 'Escape') {
      // Cancel ongoing drag
    }
  };

  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={5}
      allowDragging={true}
      onKeyDown={handleKeyDown}
    />
  );
}
```
