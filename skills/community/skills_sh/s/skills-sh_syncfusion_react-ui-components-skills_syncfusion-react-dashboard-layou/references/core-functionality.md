# Dashboard Layout Core Functionality

## Table of Contents
- [Panel Management](#panel-management)
- [Dragging & Positioning](#dragging--positioning)
- [Resizing](#resizing)
- [Floating & Auto-Arrangement](#floating--auto-arrangement)
- [Grid Configuration](#grid-configuration)
- [Responsive Behavior](#responsive-behavior)
- [State Persistence](#state-persistence)

## Panel Management

### Creating Panels

Define panels with the PanelModel interface:

```typescript
interface PanelModel {
  id: string;              // Unique identifier (required)
  row: number;             // Row position (required)
  col: number;             // Column position (required)
  sizeX: number;           // Width in cells (default: 1)
  sizeY: number;           // Height in cells (default: 1)
  header?: string | HTMLElement | Function;  // Panel header
  content?: string | HTMLElement | Function; // Panel content
  cssClass?: string;       // Custom CSS classes
  enabled?: boolean;       // Enable/disable panel (default: true)
  minSizeX?: number;       // Minimum width (default: 1)
  minSizeY?: number;       // Minimum height (default: 1)
  maxSizeX?: number;       // Maximum width (default: null)
  maxSizeY?: number;       // Maximum height (default: null)
  zIndex?: number;         // Z-index stacking (default: 1000)
}
```

### Panel Configuration Example

```tsx
const panels: PanelModel[] = [
  {
    id: 'analytics-panel',
    row: 0,
    col: 0,
    sizeX: 3,
    sizeY: 2,
    header: 'Analytics Dashboard',
    content: '<div>Chart content here</div>',
    minSizeX: 2,
    minSizeY: 1,
    maxSizeX: 4,
    maxSizeY: 3,
    cssClass: 'custom-analytics'
  },
  {
    id: 'reports-panel',
    row: 0,
    col: 3,
    sizeX: 2,
    sizeY: 2,
    header: 'Reports',
    content: '<div>Report content here</div>',
    enabled: true
  }
];
```

### Disable Specific Panels

```tsx
// Make panel non-interactive
const disabledPanel: PanelModel = {
  id: 'read-only-panel',
  row: 0,
  col: 0,
  sizeX: 2,
  sizeY: 1,
  header: 'Read Only',
  content: 'This panel is locked',
  enabled: false  // Panel won't respond to drag/resize
};
```

### Panel Size Constraints

```tsx
// Enforce minimum and maximum sizes
const constrainedPanel: PanelModel = {
  id: 'constrained-panel',
  row: 0,
  col: 0,
  sizeX: 2,
  sizeY: 1,
  minSizeX: 1,  // Cannot be smaller than 1 cell width
  minSizeY: 1,  // Cannot be smaller than 1 cell height
  maxSizeX: 4,  // Cannot exceed 4 cells width
  maxSizeY: 3   // Cannot exceed 3 cells height
};
```

## Dragging & Positioning

### Enable Dragging

Dragging is enabled by default. Control it with `allowDragging` property:

```tsx
<DashboardLayoutComponent
  allowDragging={true}  // Enable dragging
  panels={panels}
>
</DashboardLayoutComponent>
```

### Draggable Handle

Restrict dragging to specific elements using `draggableHandle`:

```tsx
<DashboardLayoutComponent
  allowDragging={true}
  draggableHandle='.e-panel-header'  // Only header can be dragged
  panels={panels}
>
</DashboardLayoutComponent>
```

```tsx
// HTML Implementation
<div id='panel1' className='e-panel' data-row='0' data-col='0' data-sizex='2' data-sizey='1'>
  <div className='e-panel-header'>Panel 1</div>  {/* Only this is draggable */}
  <div className='e-panel-content'>Content</div>
</div>
```

### Programmatic Panel Movement

Move panels using the `movePanel()` method:

```tsx
const dashboardRef = useRef<DashboardLayoutComponent>(null);

// Move panel to specific position
const handleMovePanel = () => {
  dashboardRef.current?.movePanel('panel1', 1, 2);  // row: 1, col: 2
};

<DashboardLayoutComponent ref={dashboardRef} panels={panels}>
</DashboardLayoutComponent>
```

### Reorder Panels Logic

```tsx
const reorderPanels = (dashboardRef: any) => {
  // Move all panels one position to the right
  dashboardRef.current?.movePanel('panel1', 0, 1);
  dashboardRef.current?.movePanel('panel2', 0, 3);
  dashboardRef.current?.movePanel('panel3', 0, 5);
};
```

## Resizing

### Enable Resizing

Enable resizing with the `allowResizing` property:

```tsx
<DashboardLayoutComponent
  allowResizing={true}  // Enable resize handles
  resizableHandles={['e-south-east', 'e-south', 'e-east']}
  panels={panels}
>
</DashboardLayoutComponent>
```

### Resize Handles

Configure which edges/corners can be dragged to resize:

```tsx
<DashboardLayoutComponent
  allowResizing={true}
  resizableHandles={[
    'e-south-east',   // Bottom-right corner
    'e-south',        // Bottom edge
    'e-east',         // Right edge
    'e-north-east',   // Top-right corner
    'e-west'          // Left edge
  ]}
  panels={panels}
>
</DashboardLayoutComponent>
```

### Programmatic Resizing

Resize panels using the `resizePanel()` method:

```tsx
const handleResizePanel = () => {
  // Resize panel to 3 columns wide x 2 rows high
  dashboardRef.current?.resizePanel('panel1', 3, 2);
};
```

### Size Constraints Example

```tsx
const constrainedPanels: PanelModel[] = [
  {
    id: 'fixed-panel',
    row: 0,
    col: 0,
    sizeX: 2,
    sizeY: 1,
    minSizeX: 2,      // Cannot shrink below 2 cells
    minSizeY: 1,
    maxSizeX: 2,      // Cannot expand beyond 2 cells
    maxSizeY: 1,
    header: 'Fixed Size Panel'
  },
  {
    id: 'flexible-panel',
    row: 0,
    col: 2,
    sizeX: 1,
    sizeY: 1,
    minSizeX: 1,
    minSizeY: 1,
    maxSizeX: 5,      // Can expand up to 5 cells
    maxSizeY: 4,
    header: 'Flexible Panel'
  }
];
```

## Floating & Auto-Arrangement

### Enable Floating

When enabled, panels automatically move upward to fill empty spaces:

```tsx
<DashboardLayoutComponent
  allowFloating={true}  // Enable auto-arrangement
  panels={panels}
>
</DashboardLayoutComponent>
```

**Behavior:**
- When a panel is dragged or resized, others automatically move to fill empty cells
- Creates compact layout without gaps
- Improves space utilization

### Floating Example

```tsx
// Initial layout:
// [Panel1] [Panel3]
// [Panel2] [Empty]

// After dragging Panel1 down with floating enabled:
// [Panel3] [Empty]
// [Panel1] [Panel2]  ← Panel2 auto-moves up

<DashboardLayoutComponent
  allowFloating={true}
  panels={panels}
  dragStop={() => console.log('Panels auto-arranged')}
>
</DashboardLayoutComponent>
```

## Grid Configuration

### Column Layout

Configure the number of columns in the dashboard:

```tsx
<DashboardLayoutComponent
  columns={5}  // 5-column grid
  panels={panels}
>
</DashboardLayoutComponent>
```

### Cell Spacing

Control horizontal and vertical spacing between panels:

```tsx
<DashboardLayoutComponent
  columns={5}
  cellSpacing={[10, 10]}  // [horizontal, vertical] spacing in pixels
  panels={panels}
>
</DashboardLayoutComponent>
```

**Common Spacing Values:**
```tsx
// Compact layout
cellSpacing={[5, 5]}

// Moderate spacing
cellSpacing={[10, 10]}

// Spacious layout
cellSpacing={[20, 20]}

// Asymmetric spacing
cellSpacing={[15, 5]}   // More horizontal than vertical
```

### Cell Aspect Ratio

Control the height-to-width ratio of grid cells:

```tsx
<DashboardLayoutComponent
  columns={5}
  cellAspectRatio={1}      // Square cells (default)
  panels={panels}
>
</DashboardLayoutComponent>
```

**Common Ratios:**
```tsx
cellAspectRatio={1}      // Square (1:1)
cellAspectRatio={0.5}    // Wider (2:1)
cellAspectRatio={2}      // Taller (1:2)
cellAspectRatio={1.5}    // Slightly taller
```

### Grid Visualization

Show grid lines for debugging layout:

```tsx
<DashboardLayoutComponent
  columns={5}
  showGridLines={true}   // Display grid lines
  panels={panels}
>
</DashboardLayoutComponent>
```

## Responsive Behavior

### Media Query Configuration

Automatically adjust layout on different screen sizes:

```tsx
<DashboardLayoutComponent
  columns={5}
  mediaQuery='max-width:768px'  // Stack to single column on tablets
  panels={panels}
>
</DashboardLayoutComponent>
```

**Common Breakpoints:**
```tsx
// Desktop
mediaQuery='max-width:1200px'

// Tablet
mediaQuery='max-width:768px'

// Mobile
mediaQuery='max-width:600px'
```

### Responsive Example

```tsx
<DashboardLayoutComponent
  columns={5}
  mediaQuery='max-width:600px'
  cellSpacing={[10, 10]}
  allowDragging={true}
  allowResizing={true}
  panels={panels}
>
</DashboardLayoutComponent>
```

**Behavior:**
- On desktop (>600px width): 5-column layout with all panels draggable/resizable
- On mobile (<600px width): Single column (1-column) layout, panels stack

## State Persistence

### Enable Persistence

Save and restore dashboard layout across sessions:

```tsx
<DashboardLayoutComponent
  id='my-dashboard'        // Unique identifier required
  enablePersistence={true} // Enable automatic persistence
  panels={panels}
>
</DashboardLayoutComponent>
```

### Persistence Storage

Dashboard state is automatically saved to browser localStorage when:
- Panel positions change (drag/drop)
- Panels are resized
- Panels are added/removed
- Component is destroyed

Data is restored when component is recreated.

### Manual Save & Restore

Programmatically save and restore layout:

```tsx
// Save layout
const saveLayout = () => {
  const layout = dashboardRef.current?.serialize();
  localStorage.setItem('customLayout', JSON.stringify(layout));
};

// Restore layout
const restoreLayout = () => {
  const savedLayout = localStorage.getItem('customLayout');
  if (savedLayout) {
    const layout = JSON.parse(savedLayout);
    // Update component with saved layout
    dashboardRef.current?.removeAll();
    layout.forEach(panel => {
      dashboardRef.current?.addPanel(panel);
    });
  }
};
```

### Full Persistence Example

```tsx
const PersistentDashboard = () => {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);
  const [panels, setPanels] = useState<PanelModel[]>(defaultPanels);

  // Auto-save on layout changes
  const handleChange = () => {
    const layout = dashboardRef.current?.serialize();
    sessionStorage.setItem('dashboardLayout', JSON.stringify(layout));
  };

  // Manual reset to default
  const resetLayout = () => {
    dashboardRef.current?.removeAll();
    defaultPanels.forEach(panel => {
      dashboardRef.current?.addPanel(panel);
    });
  };

  return (
    <>
      <button onClick={resetLayout}>Reset to Default</button>
      
      <DashboardLayoutComponent
        ref={dashboardRef}
        id='persistent-dashboard'
        enablePersistence={true}
        panels={panels}
        change={handleChange}
      >
      </DashboardLayoutComponent>
    </>
  );
};
```
