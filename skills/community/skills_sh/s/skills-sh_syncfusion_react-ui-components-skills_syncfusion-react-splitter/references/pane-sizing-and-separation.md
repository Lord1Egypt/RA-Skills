# Pane Sizing and Separation

## Table of Contents
- [Fixed Pane Sizing](#fixed-pane-sizing)
- [Percentage-Based Sizing](#percentage-based-sizing)
- [Min and Max Constraints](#min-and-max-constraints)
- [Separator Styling](#separator-styling)
- [Dynamic Size Adjustment](#dynamic-size-adjustment)

## Fixed Pane Sizing

Fixed sizing sets panes to specific pixel dimensions. Useful for sidebars and fixed-width panels.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';

function FixedSizing() {
  return (
    <SplitterComponent orientation='Horizontal' style={{ height: '400px' }}>
      <PanesDirective>
        <PaneDirective size='250px'>
          <div style={{ padding: '20px', backgroundColor: '#f0f0f0' }}>
            <h3>Sidebar (Fixed 250px)</h3>
            <p>Navigation items here</p>
          </div>
        </PaneDirective>
        
        <PaneDirective size='300px'>
          <div style={{ padding: '20px' }}>
            <h3>Content Area (Fixed 300px)</h3>
            <p>Main content resizable from right</p>
          </div>
        </PaneDirective>
      </PanesDirective>
    </SplitterComponent>
  );
}

export default FixedSizing;
```

**When to Use:**
- Navigation sidebars (always visible)
- Fixed-width panels with specific content
- Tool panels in IDEs

**Best Practices:**
- Use fixed sizing for panels that shouldn't shrink (sidebar)
- Set last pane without size to use remaining space
- Ensure total fixed sizes don't exceed container width

## Percentage-Based Sizing

Percentage sizing distributes space proportionally. Useful for responsive layouts.

```tsx
function PercentageSizing() {
  return (
    <SplitterComponent orientation='Horizontal' style={{ height: '400px' }}>
      <PanesDirective>
        <PaneDirective size='25%'>
          <div style={{ padding: '20px', backgroundColor: '#e8f4f8' }}>
            <h3>Sidebar (25%)</h3>
          </div>
        </PaneDirective>
        
        <PaneDirective size='50%'>
          <div style={{ padding: '20px' }}>
            <h3>Main (50%)</h3>
          </div>
        </PaneDirective>
        
        <PaneDirective size='25%'>
          <div style={{ padding: '20px', backgroundColor: '#f8e8e8' }}>
            <h3>Details (25%)</h3>
          </div>
        </PaneDirective>
      </PanesDirective>
    </SplitterComponent>
  );
}
```

**Advantages:**
- Responsive across screen sizes
- Total should equal 100%
- Resizing updates all percentage-based panes

**Example: Unequal Distribution**

```tsx
<PanesDirective>
  <PaneDirective size='20%'><div>Sidebar</div></PaneDirective>
  <PaneDirective size='60%'><div>Main Content</div></PaneDirective>
  <PaneDirective size='20%'><div>Details</div></PaneDirective>
</PanesDirective>
```

## Min and Max Constraints

Prevent panes from becoming too small or too large during resizing.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';

function SizeConstraints() {
  return (
    <SplitterComponent orientation='Horizontal' style={{ height: '400px' }}>
      <PanesDirective>
        <PaneDirective 
          size='200px'
          min='100px'
          max='400px'
        >
          <div style={{ padding: '20px', backgroundColor: '#f0f0f0' }}>
            <h3>Constrained Pane</h3>
            <p>Min: 100px | Max: 400px</p>
          </div>
        </PaneDirective>
        
        <PaneDirective size='300px'>
          <div style={{ padding: '20px' }}>
            <h3>Resizable (No Constraints)</h3>
          </div>
        </PaneDirective>
      </PanesDirective>
    </SplitterComponent>
  );
}

export default SizeConstraints;
```

### Min Size Purpose
- Prevent content overflow when pane shrinks
- Maintain readability of sidebar navigation
- Ensure minimum button/control visibility

### Max Size Purpose
- Prevent excessive expansion
- Maintain balanced layout
- Ensure main content remains visible

### Example: Content-Based Constraints

```tsx
<PaneDirective 
  size='250px'
  min='200px'  // Never shrink below 200px (width needed for nav)
  max='500px'  // Never expand beyond 500px (too wide for sidebar)
>
  <div>Navigation Sidebar</div>
</PaneDirective>
```

## Separator Styling

Customize the appearance of pane separators (dividers).

```tsx
import './custom-separator.css';

function CustomSeparatorStyling() {
  return (
    <SplitterComponent 
      orientation='Horizontal'
      style={{ height: '400px' }}
      className='custom-splitter'
    >
      <PanesDirective>
        <PaneDirective size='250px'>
          <div style={{ padding: '20px' }}>Pane 1</div>
        </PaneDirective>
        <PaneDirective size='250px'>
          <div style={{ padding: '20px' }}>Pane 2</div>
        </PaneDirective>
      </PanesDirective>
    </SplitterComponent>
  );
}
```

### Custom CSS for Separator

```css
/* Hide default separator and add custom styling */
.custom-splitter .e-splitter-bar {
  background-color: #007bff;
  width: 4px;
  cursor: col-resize;
}

/* Hover effect */
.custom-splitter .e-splitter-bar:hover {
  background-color: #0056b3;
}

/* Gripper icon customization */
.custom-splitter .e-splitter-bar::before {
  content: '|||';
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 12px;
}

/* Vertical splitter bar */
.custom-splitter.e-vertical .e-splitter-bar {
  height: 4px;
  cursor: row-resize;
}
```

### Material Design Separator

```css
.material-splitter .e-splitter-bar {
  background-color: #e0e0e0;
  width: 2px;
  transition: all 0.3s ease;
}

.material-splitter .e-splitter-bar:hover {
  background-color: #2196f3;
  width: 3px;
}
```

## Dynamic Size Adjustment

Programmatically adjust pane sizes after initialization.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';

function DynamicSizeAdjustment() {
  const splitterRef = React.useRef<SplitterComponent>(null);

  const adjustSizes = (ratio: string) => {
    if (splitterRef.current && splitterRef.current.panes) {
      switch(ratio) {
        case 'half':
          // Set equal sizes (50-50)
          splitterRef.current.panes[0].size = '50%';
          splitterRef.current.panes[1].size = '50%';
          break;
        case 'narrow':
          // First pane narrow (30-70)
          splitterRef.current.panes[0].size = '30%';
          splitterRef.current.panes[1].size = '70%';
          break;
        case 'wide':
          // First pane wide (70-30)
          splitterRef.current.panes[0].size = '70%';
          splitterRef.current.panes[1].size = '30%';
          break;
      }
      // Refresh to apply changes
      splitterRef.current.refresh();
    }
  };

  return (
    <div>
      <div style={{ marginBottom: '15px' }}>
        <button onClick={() => adjustSizes('half')}>50-50 Split</button>
        <button onClick={() => adjustSizes('narrow')}>30-70 Split</button>
        <button onClick={() => adjustSizes('wide')}>70-30 Split</button>
      </div>

      <SplitterComponent 
        ref={splitterRef}
        orientation='Horizontal'
        style={{ height: '300px' }}
      >
        <PanesDirective>
          <PaneDirective size='50%'>
            <div style={{ padding: '20px', backgroundColor: '#e3f2fd' }}>
              <h3>Pane 1</h3>
            </div>
          </PaneDirective>
          <PaneDirective size='50%'>
            <div style={{ padding: '20px', backgroundColor: '#f3e5f5' }}>
              <h3>Pane 2</h3>
            </div>
          </PaneDirective>
        </PanesDirective>
      </SplitterComponent>
    </div>
  );
}

export default DynamicSizeAdjustment;
```

### Refresh Method

The `refresh()` method redraws the splitter after programmatic changes:

```tsx
splitterRef.current.refresh();
```

### Example: Responsive Size Adjustment

```tsx
const handleResize = () => {
  const width = window.innerWidth;
  
  if (width < 768) {
    // Mobile: 40-60 split
    splitterRef.current.panes[0].size = '40%';
    splitterRef.current.panes[1].size = '60%';
  } else if (width < 1024) {
    // Tablet: 35-65 split
    splitterRef.current.panes[0].size = '35%';
    splitterRef.current.panes[1].size = '65%';
  } else {
    // Desktop: 30-70 split
    splitterRef.current.panes[0].size = '30%';
    splitterRef.current.panes[1].size = '70%';
  }
  
  splitterRef.current.refresh();
};

React.useEffect(() => {
  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
}, []);
```

## Best Practices

1. **Mix fixed and percentage:** Fixed sidebar + percentage content areas
2. **Always set constraints:** Apply min/max to resizable panes
3. **Test edge cases:** Verify layout at minimum container size
4. **Consider content:** Match pane sizes to typical content dimensions
5. **Maintain readability:** Ensure minimum size prevents text overflow
