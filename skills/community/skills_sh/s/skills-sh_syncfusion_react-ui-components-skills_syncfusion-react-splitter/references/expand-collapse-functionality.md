# Expand and Collapse Functionality

## Table of Contents
- [Collapsed State Initialization](#collapsed-state-initialization)
- [Collapse and Expand Methods](#collapse-and-expand-methods)
- [Expand and Collapse Events](#expand-and-collapse-events)
- [Button Integration](#button-integration)
- [Collapsible Configuration](#collapsible-configuration)

## Collapsed State Initialization

Set panes to collapsed (hidden) state on component load using the `collapsed` property.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';

function CollapsedStateInitialization() {
  return (
    <SplitterComponent orientation='Horizontal' style={{ height: '400px' }}>
      <PanesDirective>
        {/* This pane is visible initially */}
        <PaneDirective size='250px' collapsed={false}>
          <div style={{ padding: '20px', backgroundColor: '#e3f2fd' }}>
            <h3>Visible Pane</h3>
            <p>This pane is expanded by default</p>
          </div>
        </PaneDirective>

        {/* This pane is hidden initially */}
        <PaneDirective size='250px' collapsed={true}>
          <div style={{ padding: '20px', backgroundColor: '#f3e5f5' }}>
            <h3>Hidden Pane</h3>
            <p>This pane starts collapsed</p>
          </div>
        </PaneDirective>
      </PanesDirective>
    </SplitterComponent>
  );
}

export default CollapsedStateInitialization;
```

**Use Cases:**
- Hide secondary panels on page load
- Show/hide sidebar by default based on user preference
- Collapsible detail panes in dashboards
- Save user preferences and restore on reload

## Collapse and Expand Methods

Programmatically collapse or expand panes using public methods.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';

function CollapseExpandMethods() {
  const splitterRef = React.useRef<SplitterComponent>(null);

  const collapsePane = (index: number) => {
    if (splitterRef.current) {
      splitterRef.current.collapse(index);
    }
  };

  const expandPane = (index: number) => {
    if (splitterRef.current) {
      splitterRef.current.expand(index);
    }
  };

  return (
    <div>
      <div style={{ marginBottom: '15px' }}>
        <button onClick={() => collapsePane(0)}>Collapse Left Pane</button>
        <button onClick={() => expandPane(0)}>Expand Left Pane</button>
        <button onClick={() => collapsePane(1)}>Collapse Right Pane</button>
        <button onClick={() => expandPane(1)}>Expand Right Pane</button>
      </div>

      <SplitterComponent 
        ref={splitterRef}
        orientation='Horizontal'
        style={{ height: '400px' }}
      >
        <PanesDirective>
          <PaneDirective size='250px' collapsible={true}>
            <div style={{ padding: '20px', backgroundColor: '#e8f5e9' }}>
              <h3>Collapsible Pane 1</h3>
              <p>Click buttons to collapse/expand</p>
            </div>
          </PaneDirective>

          <PaneDirective size='300px' collapsible={true}>
            <div style={{ padding: '20px', backgroundColor: '#fff3e0' }}>
              <h3>Collapsible Pane 2</h3>
              <p>Can be toggled independently</p>
            </div>
          </PaneDirective>
        </PanesDirective>
      </SplitterComponent>
    </div>
  );
}

export default CollapseExpandMethods;
```

### Method Signatures

```tsx
collapse(index: number): void
expand(index: number): void
```

**Parameters:**
- `index` - Zero-based pane index to collapse/expand

**Example: Toggle Pane State**

```tsx
const togglePane = (index: number) => {
  const pane = splitterRef.current?.panes?.[index];
  
  if (pane?.collapsed) {
    splitterRef.current?.expand(index);
  } else {
    splitterRef.current?.collapse(index);
  }
};
```

## Expand and Collapse Events

React to collapse and expand actions using events.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';

function ExpandCollapseEvents() {
  const [eventLog, setEventLog] = React.useState<string[]>([]);

  const handleBeforeExpand = (args: any) => {
    console.log('Before Expand - Pane Index:', args.index);
    setEventLog(prev => [...prev, `Before Expand: Pane ${args.index}`]);
  };

  const handleExpanded = (args: any) => {
    console.log('Expanded - Pane Index:', args.index);
    setEventLog(prev => [...prev, `Expanded: Pane ${args.index}`]);
  };

  const handleBeforeCollapse = (args: any) => {
    console.log('Before Collapse - Pane Index:', args.index);
    setEventLog(prev => [...prev, `Before Collapse: Pane ${args.index}`]);
  };

  const handleCollapsed = (args: any) => {
    console.log('Collapsed - Pane Index:', args.index);
    setEventLog(prev => [...prev, `Collapsed: Pane ${args.index}`]);
  };

  const clearLog = () => setEventLog([]);

  return (
    <div>
      <div style={{ marginBottom: '10px' }}>
        <button onClick={clearLog}>Clear Log</button>
      </div>

      <SplitterComponent 
        orientation='Horizontal'
        style={{ height: '300px' }}
        beforeExpand={handleBeforeExpand}
        expanded={handleExpanded}
        beforeCollapse={handleBeforeCollapse}
        collapsed={handleCollapsed}
      >
        <PanesDirective>
          <PaneDirective size='200px' collapsible={true}>
            <div style={{ padding: '20px' }}>
              <h3>Pane 1</h3>
              <p>Collapse/Expand this pane</p>
            </div>
          </PaneDirective>

          <PaneDirective size='200px' collapsible={true}>
            <div style={{ padding: '20px' }}>
              <h3>Pane 2</h3>
              <p>Watch events in log</p>
            </div>
          </PaneDirective>
        </PanesDirective>
      </SplitterComponent>

      <div style={{ marginTop: '15px', padding: '10px', backgroundColor: '#f5f5f5', maxHeight: '150px', overflow: 'auto' }}>
        <h4>Event Log:</h4>
        {eventLog.map((log, idx) => (
          <div key={idx}>{log}</div>
        ))}
      </div>
    </div>
  );
}

export default ExpandCollapseEvents;
```

### Event Types

| Event | Trigger | Cancelable | Use Case |
|-------|---------|-----------|----------|
| `beforeExpand` | Before pane expands | Yes | Validate before expand, prevent expansion |
| `expanded` | After pane expanded | No | Update UI, refresh content |
| `beforeCollapse` | Before pane collapses | Yes | Save state, confirm action |
| `collapsed` | After pane collapsed | No | Update related components |

### Example: Prevent Collapse with Unsaved Changes

```tsx
const handleBeforeCollapse = (args: any) => {
  if (hasUnsavedChanges) {
    args.cancel = true; // Prevent collapse
    alert('Please save changes before collapsing');
  }
};

<SplitterComponent beforeCollapse={handleBeforeCollapse}>
  {/* panes */}
</SplitterComponent>
```

## Button Integration

Add buttons to trigger collapse/expand programmatically.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';

function ButtonIntegration() {
  const splitterRef = React.useRef<SplitterComponent>(null);
  const [isSidebarCollapsed, setIsSidebarCollapsed] = React.useState(false);

  const toggleSidebar = () => {
    const sidebarPane = 0; // First pane is sidebar
    
    if (isSidebarCollapsed) {
      splitterRef.current?.expand(sidebarPane);
      setIsSidebarCollapsed(false);
    } else {
      splitterRef.current?.collapse(sidebarPane);
      setIsSidebarCollapsed(true);
    }
  };

  return (
    <div>
      <div style={{ marginBottom: '10px', padding: '10px', backgroundColor: '#f0f0f0' }}>
        <button 
          onClick={toggleSidebar}
          style={{
            padding: '8px 16px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          {isSidebarCollapsed ? '☰ Show' : '✕ Hide'} Sidebar
        </button>
      </div>

      <SplitterComponent 
        ref={splitterRef}
        orientation='Horizontal'
        style={{ height: '400px' }}
      >
        <PanesDirective>
          <PaneDirective size='250px' collapsible={true}>
            <div style={{ 
              padding: '20px', 
              backgroundColor: '#e3f2fd',
              height: '100%',
              overflowY: 'auto'
            }}>
              <h3>Navigation</h3>
              <ul style={{ listStyle: 'none', padding: 0 }}>
                <li style={{ padding: '8px' }}>🏠 Home</li>
                <li style={{ padding: '8px' }}>📁 Files</li>
                <li style={{ padding: '8px' }}>⚙️ Settings</li>
                <li style={{ padding: '8px' }}>ℹ️ About</li>
              </ul>
            </div>
          </PaneDirective>

          <PaneDirective size='auto'>
            <div style={{ padding: '20px' }}>
              <h3>Main Content</h3>
              <p>Content area grows when sidebar collapses</p>
            </div>
          </PaneDirective>
        </PanesDirective>
      </SplitterComponent>
    </div>
  );
}

export default ButtonIntegration;
```

**Use Cases:**
- Menu toggle button (hamburger menu pattern)
- Collapse all / Expand all buttons
- Panel visibility controls
- Responsive layout switches

## Collapsible Configuration

Configure which panes can be collapsed by users.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';

function CollapsibleConfiguration() {
  return (
    <SplitterComponent orientation='Horizontal' style={{ height: '400px' }}>
      <PanesDirective>
        {/* Collapsible pane - user can collapse */}
        <PaneDirective size='200px' collapsible={true}>
          <div style={{ padding: '20px', backgroundColor: '#c8e6c9' }}>
            <h3>Collapsible Pane</h3>
            <p>User can click gripper to collapse</p>
          </div>
        </PaneDirective>

        {/* Non-collapsible pane - user cannot collapse */}
        <PaneDirective size='200px' collapsible={false}>
          <div style={{ padding: '20px', backgroundColor: '#ffccbc' }}>
            <h3>Non-Collapsible Pane</h3>
            <p>This pane cannot be collapsed by user</p>
          </div>
        </PaneDirective>

        {/* Collapsible pane */}
        <PaneDirective size='200px' collapsible={true}>
          <div style={{ padding: '20px', backgroundColor: '#b3e5fc' }}>
            <h3>Also Collapsible</h3>
            <p>User can toggle this pane</p>
          </div>
        </PaneDirective>
      </PanesDirective>
    </SplitterComponent>
  );
}

export default CollapsibleConfiguration;
```

### Gripper UI

When `collapsible={true}`, a gripper icon appears at the pane edge. Users click it to toggle collapse state.

**Default Gripper Appearance:**
- Vertical bars `|||` or chevron `<`/`>`
- Positioned at separator
- Clickable area for collapse/expand

### Best Practices

1. **Set collapsible strategically** - Only for secondary panes
2. **Provide feedback** - Update button states when pane collapses
3. **Save preferences** - Store collapse state in localStorage
4. **Consider content** - Ensure collapsed pane content is not essential
5. **Test responsiveness** - Collapse behavior on mobile devices
