# Resizing and Floating Panels

## Table of Contents
- [Overview](#overview)
- [Resizing Panels](#resizing-panels)
- [Resize Handles](#resize-handles)
- [Resize Constraints](#resize-constraints)
- [Resize Events](#resize-events)
- [Floating Panels](#floating-panels)
- [Floating Behavior](#floating-behavior)
- [Programmatic Resizing](#programmatic-resizing)
- [Advanced Patterns](#advanced-patterns)
- [Best Practices](#best-practices)

## Overview

Dashboard Layout provides flexible resizing and floating capabilities. Panels can be resized in multiple directions, with automatic collision handling. Floating automatically arranges panels to fill empty spaces, optimizing dashboard real estate.

### Key Features

**Resizing:**
- Multi-directional handles (SE, E, W, N, S, NW, SW)
- Size constraints (minSizeX, minSizeY, maxSizeX, maxSizeY)
- Automatic collision handling during resize
- Visual feedback during operation

**Floating:**
- Automatic upward movement to fill gaps
- Configurable via `allowFloating` property
- Works seamlessly with dragging/resizing
- Maintains responsive layout

## Resizing Panels

### Enable Resizing

```tsx
import { DashboardLayoutComponent } from '@syncfusion/ej2-react-layouts';

function ResizableDashboard() {
  const panels = [
    {
      id: 'panel-1',
      header: 'Sales',
      content: '<div>Sales data</div>',
      row: 0,
      col: 0,
      sizeX: 2,
      sizeY: 2,
      minSizeX: 1,
      minSizeY: 1,
      maxSizeX: 5,
      maxSizeY: 4
    },
    {
      id: 'panel-2',
      header: 'Users',
      content: '<div>User data</div>',
      row: 0,
      col: 2,
      sizeX: 3,
      sizeY: 2
    }
  ];

  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={5}
      allowResizing={true}  // Enable resizing
      cellSpacing={[10, 10]}
    />
  );
}
```

### Default Behavior

By default:
- **Handles**: SE (south-east) handle only
- **Direction**: Only resize bottom-right
- **Constraints**: None (unlimited resize)
- **Collision**: Pushes overlapping panels

## Resize Handles

### Resize Handle Directions

```tsx
const resizeDirections = [
  'e-south-east',      // Bottom-right corner (↘)
  'e-east',            // Right edge (→)
  'e-west',            // Left edge (←)
  'e-north',           // Top edge (↑)
  'e-south',           // Bottom edge (↓)
  'e-north-east',      // Top-right corner (↗)
  'e-north-west',      // Top-left corner (↖)
  'e-south-west'       // Bottom-left corner (↙)
];

function MultiDirectionalResize() {
  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={5}
      allowResizing={true}
      resizableHandles={[
        'e-south-east',
        'e-east',
        'e-west',
        'e-north',
        'e-south'
      ]}
    />
  );
}
```

### Complete Resize Configuration

```tsx
function FullyResizableDashboard() {
  const allHandles = [
    'e-south-east',
    'e-east',
    'e-west',
    'e-north',
    'e-south',
    'e-north-east',
    'e-north-west',
    'e-south-west'
  ];

  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={5}
      allowResizing={true}
      resizableHandles={allHandles}
    />
  );
}
```

### Per-Panel Resize Configuration

```tsx
function SelectiveResizablePanels() {
  const panels = [
    {
      id: 'resizable-panel',
      header: 'Full Resize',
      content: '<div>Resizable in all directions</div>',
      row: 0,
      col: 0,
      sizeX: 2,
      sizeY: 2
      // Inherits global resizeHandles
    },
    {
      id: 'fixed-size-panel',
      header: 'Fixed Size',
      content: '<div>Cannot be resized</div>',
      row: 0,
      col: 2,
      sizeX: 3,
      sizeY: 2,
      minSizeX: 3,
      minSizeY: 2,
      maxSizeX: 3,
      maxSizeY: 2
      // Force size - effectively locks resizing
    }
  ];

  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={5}
      allowResizing={true}
      resizableHandles={['e-south-east', 'e-east']}
    />
  );
}
```

## Resize Constraints

Size constraints prevent panels from becoming too small or too large:

### Properties

```typescript
interface PanelModel {
  minSizeX?: number;  // Minimum width in cells
  minSizeY?: number;  // Minimum height in cells
  maxSizeX?: number;  // Maximum width in cells
  maxSizeY?: number;  // Maximum height in cells
}
```

### Example: Setting Constraints

```tsx
function ConstrainedResizeDashboard() {
  const panels = [
    {
      id: 'chart-panel',
      header: 'Chart',
      content: '<canvas id="chart"></canvas>',
      row: 0,
      col: 0,
      sizeX: 3,
      sizeY: 3,
      minSizeX: 2,  // At least 2 cells wide
      minSizeY: 2,  // At least 2 cells tall
      maxSizeX: 4,  // At most 4 cells wide
      maxSizeY: 5   // At most 5 cells tall
    },
    {
      id: 'stat-panel',
      header: 'Stats',
      content: '<div>Stats</div>',
      row: 0,
      col: 3,
      sizeX: 2,
      sizeY: 1,
      minSizeX: 1,  // Can go very small
      minSizeY: 1,
      maxSizeX: 2,  // But capped at 2 cells
      maxSizeY: 3
    }
  ];

  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={5}
      allowResizing={true}
      resizableHandles={['e-south-east', 'e-east', 'e-south']}
    />
  );
}
```

### Dynamic Constraint Updates

```tsx
function DynamicConstraintsDashboard() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);

  const updateConstraints = (panelId: string, constraints: any) => {
    const currentPanels = dashboardRef.current?.serialize() || [];
    const updated = currentPanels.map(panel => {
      if (panel.id === panelId) {
        return { ...panel, ...constraints };
      }
      return panel;
    });
    dashboardRef.current!.panels = updated;
  };

  const lockPanelSize = (panelId: string) => {
    const panels = dashboardRef.current?.serialize() || [];
    const panel = panels.find(p => p.id === panelId);
    if (panel) {
      updateConstraints(panelId, {
        minSizeX: panel.sizeX,
        maxSizeX: panel.sizeX,
        minSizeY: panel.sizeY,
        maxSizeY: panel.sizeY
      });
    }
  };

  return (
    <div>
      <button onClick={() => lockPanelSize('panel-1')}>Lock Panel 1</button>
      <DashboardLayoutComponent
        ref={dashboardRef}
        id='dashboard'
        panels={panels}
        columns={5}
        allowResizing={true}
      />
    </div>
  );
}
```

## Resize Events

### Event Lifecycle

```
User presses resize handle
         ↓
    resizeStart event fires
         ↓
User drags handle
         ↓
    resize event fires (continuously)
         ↓
User releases mouse
         ↓
    resizeStop event fires
```

### resizeStart Event

```tsx
function ResizeStartExample() {
  const handleResizeStart = (args: ResizeStartEventArgs) => {
    console.log('Resize started:', {
      panelId: args.element?.id,
      currentSize: {
        width: args.element?.offsetWidth,
        height: args.element?.offsetHeight
      }
    });
  };

  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={5}
      allowResizing={true}
      resizeStart={handleResizeStart}
    />
  );
}
```

### resize Event

Fires continuously during resizing:

```tsx
function ResizeExample() {
  const [resizeInfo, setResizeInfo] = useState('');

  const handleResize = (args: ResizeEventArgs) => {
    const info = `Resizing: ${args.element?.id} - Size: ${args.element?.offsetWidth}px × ${args.element?.offsetHeight}px`;
    setResizeInfo(info);
  };

  return (
    <div>
      <div>{resizeInfo}</div>
      <DashboardLayoutComponent
        id='dashboard'
        panels={panels}
        columns={5}
        allowResizing={true}
        resize={handleResize}
      />
    </div>
  );
}
```

### resizeStop Event

```tsx
function ResizeStopExample() {
  const handleResizeStop = (args: ResizeStopEventArgs) => {
    const info = {
      panelId: args.element?.id,
      newSize: {
        width: args.element?.offsetWidth,
        height: args.element?.offsetHeight
      }
    };

    console.log('Resize stopped:', info);
    
    // Save layout after resize
    const layout = dashboardRef.current?.serialize();
    localStorage.setItem('dashboard-layout', JSON.stringify(layout));
  };

  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={5}
      allowResizing={true}
      resizeStop={handleResizeStopExample}
    />
  );
}
```

## Floating Panels

### What is Floating?

Floating automatically moves panels upward to fill empty spaces in previous rows. This optimizes dashboard space utilization and creates a compact layout.

### Enable/Disable Floating

```tsx
function FloatingControlDashboard() {
  const [floatingEnabled, setFloatingEnabled] = useState(true);

  return (
    <div>
      <label>
        <input
          type='checkbox'
          checked={floatingEnabled}
          onChange={(e) => setFloatingEnabled(e.target.checked)}
        />
        Allow Floating
      </label>
      
      <DashboardLayoutComponent
        id='dashboard'
        panels={panels}
        columns={5}
        allowFloating={floatingEnabled}
      />
    </div>
  );
}
```

## Floating Behavior

### Before Floating (allowFloating = false)

```
Layout with gaps:
┌─────┐                  Row 0
├─────┤
│     │ Panel at row 1, col 0
│     │ (gap in row 0)
├─────┴────────────────┐ Row 1
│                      │
│   Large panel        │
│                      │ (gap above it - not filled)
└──────────────────────┘
```

### After Floating (allowFloating = true)

```
Panels move up to fill gaps:
┌─────┐ ┌────────────────┐
│ P1  │ │      P3        │ Row 0 (filled)
├─────┴─┤                │
│   P2  │                │ Row 0
│       └────────────────┘
│       (P3 moved up, no gap)
└───────┘
```

### Floating Example

```tsx
function FloatingBehaviorDemo() {
  const panelsWithGaps = [
    {
      id: 'panel-1',
      header: 'Panel 1',
      content: '<div>Content</div>',
      row: 1,  // Starts at row 1
      col: 0,
      sizeX: 2,
      sizeY: 2
    },
    {
      id: 'panel-2',
      header: 'Panel 2',
      content: '<div>Content</div>',
      row: 2,  // Starts at row 2
      col: 2,
      sizeX: 2,
      sizeY: 2
    },
    {
      id: 'panel-3',
      header: 'Panel 3',
      content: '<div>Content</div>',
      row: 3,  // Starts at row 3
      col: 4,
      sizeX: 1,
      sizeY: 3
    }
  ];

  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panelsWithGaps}
      columns={5}
      allowFloating={true}  // Panels automatically move up
      // Result: All panels move to row 0, filling all available space
    />
  );
}
```

## Programmatic Resizing

### resizePanel Method

```typescript
// Method signature
resizePanel(id: string, sizeX: number, sizeY: number): void
```

### Example: Programmatic Resize

```tsx
function ProgrammaticResizeDashboard() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);

  const resizePanel = (panelId: string, newSizeX: number, newSizeY: number) => {
    dashboardRef.current?.resizePanel(panelId, newSizeX, newSizeY);
  };

  const resetAllPanels = () => {
    dashboardRef.current?.resizePanel('panel-1', 2, 2);
    dashboardRef.current?.resizePanel('panel-2', 2, 1);
    dashboardRef.current?.resizePanel('panel-3', 3, 2);
  };

  const maximizePanel = (panelId: string) => {
    resizePanel(panelId, 5, 4);  // Make it very large
  };

  const minimizePanel = (panelId: string) => {
    resizePanel(panelId, 1, 1);  // Make it very small
  };

  return (
    <div>
      <button onClick={() => maximizePanel('panel-1')}>Maximize Panel 1</button>
      <button onClick={() => minimizePanel('panel-1')}>Minimize Panel 1</button>
      <button onClick={resetAllPanels}>Reset All</button>

      <DashboardLayoutComponent
        ref={dashboardRef}
        id='dashboard'
        panels={panels}
        columns={5}
        allowResizing={true}
      />
    </div>
  );
}
```

## Advanced Patterns

### Pattern 1: Responsive Resizing

```tsx
function ResponsiveResizeDashboard() {
  const [screenWidth, setScreenWidth] = useState(window.innerWidth);
  const dashboardRef = useRef<DashboardLayoutComponent>(null);

  useEffect(() => {
    const handleResize = () => {
      const newWidth = window.innerWidth;
      setScreenWidth(newWidth);

      if (newWidth < 768) {
        // Mobile: Make all panels smaller
        dashboardRef.current?.resizePanel('panel-1', 1, 2);
        dashboardRef.current?.resizePanel('panel-2', 1, 1);
      } else {
        // Desktop: Make panels larger
        dashboardRef.current?.resizePanel('panel-1', 3, 2);
        dashboardRef.current?.resizePanel('panel-2', 2, 2);
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <DashboardLayoutComponent
      ref={dashboardRef}
      id='dashboard'
      panels={panels}
      columns={screenWidth < 768 ? 2 : 5}
    />
  );
}
```

### Pattern 2: Aspect Ratio Maintenance

```tsx
function AspectRatioResizeDashboard() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);

  const handleResizeStop = (args: ResizeStopEventArgs) => {
    const panelId = args.element?.id;
    const panels = dashboardRef.current?.serialize() || [];
    const resizedPanel = panels.find(p => p.id === panelId);

    if (resizedPanel && resizedPanel.id === 'aspect-locked-panel') {
      // Maintain 2:1 aspect ratio (2x for width per 1x for height)
      const targetSizeY = Math.round(resizedPanel.sizeX / 2);
      if (resizedPanel.sizeY !== targetSizeY) {
        dashboardRef.current?.resizePanel(panelId, resizedPanel.sizeX, targetSizeY);
      }
    }
  };

  return (
    <DashboardLayoutComponent
      ref={dashboardRef}
      id='dashboard'
      panels={panels}
      columns={5}
      allowResizing={true}
      resizeStop={handleResizeStop}
    />
  );
}
```

### Pattern 3: Grouped Resizing

```tsx
function GroupedResizeDashboard() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);

  const handleResizeStop = (args: ResizeStopEventArgs) => {
    const resizedPanel = args.element?.id;

    // If "master" panel is resized, resize "slave" panels too
    if (resizedPanel === 'master-panel') {
      const panels = dashboardRef.current?.serialize() || [];
      const masterSize = panels.find(p => p.id === 'master-panel');

      if (masterSize) {
        dashboardRef.current?.resizePanel('slave-1', masterSize.sizeX, masterSize.sizeY);
        dashboardRef.current?.resizePanel('slave-2', masterSize.sizeX, masterSize.sizeY);
      }
    }
  };

  return (
    <DashboardLayoutComponent
      ref={dashboardRef}
      id='dashboard'
      panels={panels}
      columns={5}
      allowResizing={true}
      resizeStop={handleResizeStop}
    />
  );
}
```

## Best Practices

### 1. Always Set Meaningful Constraints

```tsx
// ✅ RECOMMENDED
const panels = [
  {
    id: 'chart',
    header: 'Chart',
    content: '<canvas></canvas>',
    row: 0,
    col: 0,
    sizeX: 3,
    sizeY: 3,
    minSizeX: 2,  // Reasonable minimum
    minSizeY: 2,
    maxSizeX: 5,  // Reasonable maximum
    maxSizeY: 5
  }
];

// ❌ AVOID: No constraints (uncontrolled)
const badPanels = [
  {
    id: 'chart',
    row: 0,
    col: 0,
    sizeX: 3,
    sizeY: 3
    // Can be resized to any size
  }
];
```

### 2. Handle Floating Thoughtfully

```tsx
// ✅ RECOMMENDED: Enable floating for optimal space usage
<DashboardLayoutComponent
  id='dashboard'
  panels={panels}
  columns={5}
  allowFloating={true}  // Fills gaps automatically
/>

// ⚠️ CONSIDER: Disable if you need fixed row positions
<DashboardLayoutComponent
  id='dashboard'
  panels={panels}
  columns={5}
  allowFloating={false}  // Preserves exact positions
/>
```

### 3. Debounce Resize Operations

```tsx
// ✅ RECOMMENDED: Debounce expensive operations
function DebouncedResizeSaveDashboard() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);
  const timeoutRef = useRef<NodeJS.Timer>();

  const handleResizeStop = () => {
    clearTimeout(timeoutRef.current);
    timeoutRef.current = setTimeout(() => {
      const layout = dashboardRef.current?.serialize();
      saveLayoutToDatabase(layout);
    }, 500);  // Wait 500ms before saving
  };

  return (
    <DashboardLayoutComponent
      ref={dashboardRef}
      id='dashboard'
      panels={panels}
      columns={5}
      allowResizing={true}
      resizeStop={handleResizeStop}
    />
  );
}
```

### 4. Provide Visual Feedback

```tsx
// ✅ RECOMMENDED: Show what's happening
function FeedbackResizeDashboard() {
  const [resizingPanel, setResizingPanel] = useState<string | null>(null);

  const handleResizeStart = (args: ResizeStartEventArgs) => {
    setResizingPanel(args.element?.id || null);
  };

  const handleResizeStop = () => {
    setResizingPanel(null);
  };

  return (
    <div>
      {resizingPanel && (
        <div className="resize-indicator">Resizing: {resizingPanel}</div>
      )}
      <DashboardLayoutComponent
        id='dashboard'
        panels={panels}
        columns={5}
        allowResizing={true}
        resizeStart={handleResizeStart}
        resizeStop={handleResizeStop}
      />
    </div>
  );
}
```

### 5. Test on All Devices

```tsx
// ✅ RECOMMENDED: Ensure resize works on touch devices
function TouchFriendlyResizeDashboard() {
  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={5}
      allowResizing={true}
      resizableHandles={['e-south-east']}  // Larger handles on mobile
      // CSS: Make handles bigger on touch devices
    />
  );
}

// CSS for larger touch targets
@media (max-width: 768px) {
  .e-panel .e-resize-handle {
    width: 50px !important;
    height: 50px !important;
    bottom: -15px;
    right: -15px;
  }
}
```
