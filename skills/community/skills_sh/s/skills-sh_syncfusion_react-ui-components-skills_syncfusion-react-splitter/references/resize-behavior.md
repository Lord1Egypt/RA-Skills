# Resize Behavior

## Table of Contents
- [Resize Events](#resize-events)
- [Preventing Resize](#preventing-resize)
- [Dynamic Resize Configuration](#dynamic-resize-configuration)
- [Resize Constraints](#resize-constraints)
- [Event Data and Handling](#event-data-and-handling)

## Resize Events

The Splitter component fires events before and after pane resizing, allowing you to react to or validate resize operations.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';

function ResizeEventsExample() {
  const [resizeInfo, setResizeInfo] = React.useState<string>('');

  const handleBeforeResize = (args: any) => {
    console.log('Before Resize:', {
      pane: args.paneIndex,
      oldSize: args.oldSize,
      newSize: args.newSize
    });
    setResizeInfo(`Before Resize: Pane ${args.paneIndex} - ${args.oldSize} → ${args.newSize}`);
  };

  const handleResized = (args: any) => {
    console.log('After Resize:', {
      pane: args.paneIndex,
      size: args.size
    });
    setResizeInfo(`Resized: Pane ${args.paneIndex} - Final size: ${args.size}`);
  };

  return (
    <div>
      <div style={{ marginBottom: '10px', padding: '10px', backgroundColor: '#f5f5f5' }}>
        <p><strong>Resize Info:</strong> {resizeInfo || 'Drag separator to resize...'}</p>
      </div>

      <SplitterComponent 
        orientation='Horizontal'
        style={{ height: '300px' }}
        beforeResize={handleBeforeResize}
        resized={handleResized}
      >
        <PanesDirective>
          <PaneDirective size='200px'>
            <div style={{ padding: '20px', backgroundColor: '#e3f2fd' }}>
              <h3>Left Pane</h3>
              <p>Resizable</p>
            </div>
          </PaneDirective>
          <PaneDirective size='300px'>
            <div style={{ padding: '20px', backgroundColor: '#f3e5f5' }}>
              <h3>Right Pane</h3>
              <p>Drag separator to see events</p>
            </div>
          </PaneDirective>
        </PanesDirective>
      </SplitterComponent>
    </div>
  );
}

export default ResizeEventsExample;
```

### Event Types

| Event | Trigger | Cancelable | Use Case |
|-------|---------|-----------|----------|
| `beforeResize` | Before resize starts | Yes | Validate new size, prevent resize |
| `resized` | After resize completes | No | Update related components, save size |

### Event Arguments for beforeResize

```tsx
{
  paneIndex: number;        // Index of pane being resized
  oldSize: string;          // Previous size (e.g., "200px")
  newSize: string;          // Proposed new size (e.g., "250px")
  cancel?: boolean;         // Set to true to prevent resize
  event: Event;             // Browser mouse/touch event
}
```

## Preventing Resize

Block resize operations conditionally using the `beforeResize` event.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';

function PreventingResize() {
  const handleBeforeResize = (args: any) => {
    // Prevent first pane from shrinking below 150px
    if (args.paneIndex === 0) {
      const newSizePixels = parseInt(args.newSize);
      if (newSizePixels < 150) {
        args.cancel = true;
        alert('Left pane minimum size is 150px');
        return;
      }
    }

    // Prevent second pane from expanding beyond 400px
    if (args.paneIndex === 1) {
      const newSizePixels = parseInt(args.newSize);
      if (newSizePixels > 400) {
        args.cancel = true;
        alert('Right pane maximum size is 400px');
        return;
      }
    }
  };

  return (
    <SplitterComponent 
      orientation='Horizontal'
      style={{ height: '300px' }}
      beforeResize={handleBeforeResize}
    >
      <PanesDirective>
        <PaneDirective size='200px' min='150px'>
          <div style={{ padding: '20px' }}>
            <h3>Left (Min 150px)</h3>
          </div>
        </PaneDirective>
        <PaneDirective size='300px' max='400px'>
          <div style={{ padding: '20px' }}>
            <h3>Right (Max 400px)</h3>
          </div>
        </PaneDirective>
      </PanesDirective>
    </SplitterComponent>
  );
}

export default PreventingResize;
```

### Using Resizable Property

Completely disable resizing for specific panes:

```tsx
<PaneDirective size='200px' resizable={false}>
  <div>Non-resizable Pane</div>
</PaneDirective>
```

**When to Use `resizable={false}`:**
- Fixed sidebars that shouldn't change size
- Content that requires specific dimensions
- Read-only or display-only panes

## Dynamic Resize Configuration

Configure resizable behavior at runtime.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';

function DynamicResizeConfiguration() {
  const splitterRef = React.useRef<SplitterComponent>(null);
  const [resizeMode, setResizeMode] = React.useState('normal');

  const changeResizeMode = (mode: string) => {
    setResizeMode(mode);

    if (splitterRef.current?.panes) {
      switch(mode) {
        case 'locked':
          // Lock all panes
          splitterRef.current.panes.forEach((pane: any) => {
            pane.resizable = false;
          });
          break;

        case 'flexible':
          // Enable all panes
          splitterRef.current.panes.forEach((pane: any) => {
            pane.resizable = true;
          });
          break;

        case 'left-only':
          // Only first pane resizable
          splitterRef.current.panes[0].resizable = true;
          if (splitterRef.current.panes[1]) {
            splitterRef.current.panes[1].resizable = false;
          }
          break;
      }

      splitterRef.current.refresh();
    }
  };

  return (
    <div>
      <div style={{ marginBottom: '10px' }}>
        <button 
          onClick={() => changeResizeMode('normal')}
          style={{ 
            padding: '8px 12px', 
            marginRight: '5px',
            backgroundColor: resizeMode === 'normal' ? '#007bff' : '#ccc',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Normal
        </button>
        <button 
          onClick={() => changeResizeMode('locked')}
          style={{ 
            padding: '8px 12px', 
            marginRight: '5px',
            backgroundColor: resizeMode === 'locked' ? '#007bff' : '#ccc',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Locked
        </button>
        <button 
          onClick={() => changeResizeMode('flexible')}
          style={{ 
            padding: '8px 12px', 
            marginRight: '5px',
            backgroundColor: resizeMode === 'flexible' ? '#007bff' : '#ccc',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Flexible
        </button>
        <button 
          onClick={() => changeResizeMode('left-only')}
          style={{ 
            padding: '8px 12px',
            backgroundColor: resizeMode === 'left-only' ? '#007bff' : '#ccc',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Left Only
        </button>
      </div>

      <p><em>Current Mode: {resizeMode}</em></p>

      <SplitterComponent 
        ref={splitterRef}
        orientation='Horizontal'
        style={{ height: '300px' }}
      >
        <PanesDirective>
          <PaneDirective size='250px' resizable={true}>
            <div style={{ padding: '20px', backgroundColor: '#e3f2fd' }}>
              <h3>Pane 1</h3>
            </div>
          </PaneDirective>
          <PaneDirective size='250px' resizable={true}>
            <div style={{ padding: '20px', backgroundColor: '#f3e5f5' }}>
              <h3>Pane 2</h3>
            </div>
          </PaneDirective>
        </PanesDirective>
      </SplitterComponent>
    </div>
  );
}

export default DynamicResizeConfiguration;
```

## Resize Constraints

Set minimum and maximum sizes to automatically constrain resizing without event handling.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';

function ResizeConstraints() {
  return (
    <SplitterComponent orientation='Horizontal' style={{ height: '300px' }}>
      <PanesDirective>
        <PaneDirective 
          size='200px'
          min='100px'
          max='400px'
        >
          <div style={{ padding: '20px', backgroundColor: '#c8e6c9' }}>
            <h3>Constrained Pane</h3>
            <p>Min: 100px | Max: 400px</p>
            <p>Try dragging separator - resize is limited</p>
          </div>
        </PaneDirective>

        <PaneDirective size='250px'>
          <div style={{ padding: '20px', backgroundColor: '#fff9c4' }}>
            <h3>Normal Pane</h3>
            <p>No size constraints</p>
          </div>
        </PaneDirective>
      </PanesDirective>
    </SplitterComponent>
  );
}

export default ResizeConstraints;
```

### Properties

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| `size` | string | Current pane size | `size='200px'` |
| `min` | string | Minimum size constraint | `min='100px'` |
| `max` | string | Maximum size constraint | `max='500px'` |
| `resizable` | boolean | Allow user resize | `resizable={false}` |

## Event Data and Handling

Advanced event handling with detailed data.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';

function EventDataHandling() {
  const [events, setEvents] = React.useState<any[]>([]);

  const handleBeforeResize = (args: any) => {
    const oldSizeNum = parseInt(args.oldSize);
    const newSizeNum = parseInt(args.newSize);
    const change = newSizeNum - oldSizeNum;
    const percentChange = ((change / oldSizeNum) * 100).toFixed(2);

    const eventData = {
      type: 'beforeResize',
      pane: args.paneIndex,
      oldSize: args.oldSize,
      newSize: args.newSize,
      change: `${change}px (${percentChange}%)`,
      timestamp: new Date().toLocaleTimeString()
    };

    setEvents(prev => [eventData, ...prev.slice(0, 9)]);
  };

  const handleResized = (args: any) => {
    const eventData = {
      type: 'resized',
      pane: args.paneIndex,
      finalSize: args.size,
      timestamp: new Date().toLocaleTimeString()
    };

    setEvents(prev => [eventData, ...prev.slice(0, 9)]);
  };

  return (
    <div>
      <SplitterComponent 
        orientation='Horizontal'
        style={{ height: '250px', marginBottom: '20px' }}
        beforeResize={handleBeforeResize}
        resized={handleResized}
      >
        <PanesDirective>
          <PaneDirective size='200px'>
            <div style={{ padding: '20px' }}>
              <h3>Left</h3>
              <p>Drag to resize</p>
            </div>
          </PaneDirective>
          <PaneDirective size='300px'>
            <div style={{ padding: '20px' }}>
              <h3>Right</h3>
              <p>Watch events below</p>
            </div>
          </PaneDirective>
        </PanesDirective>
      </SplitterComponent>

      <div style={{ 
        padding: '10px', 
        backgroundColor: '#f5f5f5',
        border: '1px solid #ddd',
        maxHeight: '200px',
        overflowY: 'auto'
      }}>
        <h4>Event Log</h4>
        {events.length === 0 ? (
          <p style={{ color: '#999' }}>Resize to see events...</p>
        ) : (
          events.map((event, idx) => (
            <div key={idx} style={{ 
              padding: '8px', 
              borderBottom: '1px solid #eee',
              fontSize: '12px'
            }}>
              <strong>{event.type}</strong> - Pane {event.pane} @ {event.timestamp}
              {event.change && <div>Change: {event.change}</div>}
              {event.newSize && <div>New: {event.newSize}</div>}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default EventDataHandling;
```

## Best Practices

1. **Always set min/max** - Prevent layout breakage
2. **Validate in beforeResize** - Cancel invalid resizes
3. **Save state in resized** - Persist user preferences
4. **Consider content type** - Match size constraints to content
5. **Test edge cases** - Verify extreme sizes don't break UI
