# Drag and Drop Reordering

## Table of Contents
- [Basic Drag and Drop](#basic-drag-and-drop)
- [Drag Events](#drag-events)
- [Event Handling](#event-handling)
- [Preventing Drag/Drop](#preventing-dragdrop)
- [Drag Constraints](#drag-constraints)
- [Tab-to-Tab Drag Drop](#tab-to-tab-drag-drop)
- [External Source Integration](#external-source-integration)

## Basic Drag and Drop

Enable drag-and-drop reordering to allow users to rearrange tab items manually.

### Configuration

```jsx
<TabComponent allowDragAndDrop={true}>
  <TabItemsDirective>
    <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
    <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
    <TabItemDirective header={{ text: 'Tab 3' }} content="Content 3" />
  </TabItemsDirective>
</TabComponent>
```

### How It Works

1. User clicks and holds on a tab header
2. Cursor changes to indicate dragging
3. User drags tab to new position
4. Tab reorders when dropped
5. Content automatically updates to match new order

### Visual Feedback

- Dragged tab appears semi-transparent/raised
- Drop target position indicated with visual marker
- Tab snaps to final position on release

### Example: Simple Draggable Tabs

```jsx
import React, { useState } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function DraggableTab() {
  const [tabs, setTabs] = useState([
    { text: 'Projects', content: 'Active projects list' },
    { text: 'Team', content: 'Team members and roles' },
    { text: 'Settings', content: 'Project settings' },
    { text: 'Archive', content: 'Archived items' }
  ]);

  return (
    <div style={{ padding: '20px' }}>
      <h2>Draggable Tabs</h2>
      <p>Drag tab headers to reorder them</p>
      
      <TabComponent allowDragAndDrop={true}>
        <TabItemsDirective>
          {tabs.map((tab, index) => (
            <TabItemDirective 
              key={index}
              header={{ text: tab.text }}
              content={tab.content}
            />
          ))}
        </TabItemsDirective>
      </TabComponent>

      <div style={{ marginTop: '20px', padding: '10px', backgroundColor: '#f0f0f0' }}>
        <h3>Current Tab Order:</h3>
        <ol>
          {tabs.map((tab, i) => <li key={i}>{tab.text}</li>)}
        </ol>
      </div>
    </div>
  );
}
```

## Drag Events

The Tab component provides events to control and respond to drag operations.

### Event Types

| Event | Trigger | Purpose |
|-------|---------|---------|
| `onDragStart` | Before drag begins | Prevent dragging specific items |
| `dragging` | During drag operation | Monitor drag progress |
| `dragged` | After drop completes | Execute post-drop actions |

## Event Handling

### onDragStart Event

Triggered before a tab starts being dragged. Use to prevent dragging specific tabs.

```jsx
const handleDragStart = (args) => {
  // args.draggableData contains info about dragged item
  console.log('Dragging tab:', args.draggableData.text);
  
  // Prevent dragging by setting cancel = true
  if (args.draggableData.text === 'Locked Tab') {
    args.cancel = true;  // Prevent drag
  }
};

<TabComponent 
  allowDragAndDrop={true}
  onDragStart={handleDragStart}
>
  {/* Tabs */}
</TabComponent>
```

### dragging Event

Triggered continuously while dragging. Use to monitor drag progress.

```jsx
const handleDragging = (args) => {
  console.log('Dragging in progress...');
  // Can be used for animations or visual feedback
};

<TabComponent 
  allowDragAndDrop={true}
  dragging={handleDragging}
>
  {/* Tabs */}
</TabComponent>
```

### dragged Event

Triggered after tab is successfully dropped. Use for post-drop actions.

```jsx
const handleDragged = (args) => {
  console.log('Tab dropped at new position');
  console.log('Source index:', args.source);
  console.log('Target index:', args.target);
  
  // Execute custom logic after reordering
};

<TabComponent 
  allowDragAndDrop={true}
  dragged={handleDragged}
>
  {/* Tabs */}
</TabComponent>
```

### Complete Event Handling Example

```jsx
import React, { useState } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function DragEventExample() {
  const [eventLog, setEventLog] = useState([]);

  const handleDragStart = (args) => {
    setEventLog(prev => [...prev, `Start: Dragging "${args.draggableData.text}"`]);
  };

  const handleDragging = (args) => {
    // Only log occasionally to avoid spam
    console.log('Dragging...');
  };

  const handleDragged = (args) => {
    setEventLog(prev => [...prev, 
      `Dropped: Moved from position ${args.source} to ${args.target}`
    ]);
  };

  return (
    <div style={{ padding: '20px', display: 'flex', gap: '20px' }}>
      <div style={{ flex: 1 }}>
        <h2>Draggable Tabs with Events</h2>
        <TabComponent 
          allowDragAndDrop={true}
          onDragStart={handleDragStart}
          dragging={handleDragging}
          dragged={handleDragged}
        >
          <TabItemsDirective>
            <TabItemDirective header={{ text: 'Inbox' }} content="Inbox items" />
            <TabItemDirective header={{ text: 'Drafts' }} content="Draft emails" />
            <TabItemDirective header={{ text: 'Sent' }} content="Sent emails" />
            <TabItemDirective header={{ text: 'Spam' }} content="Spam folder" />
          </TabItemsDirective>
        </TabComponent>
      </div>

      <div style={{ flex: 1, backgroundColor: '#f0f0f0', padding: '10px' }}>
        <h3>Event Log</h3>
        <ul style={{ height: '300px', overflow: 'auto' }}>
          {eventLog.map((log, i) => (
            <li key={i}>{log}</li>
          ))}
        </ul>
        <button onClick={() => setEventLog([])}>Clear</button>
      </div>
    </div>
  );
}
```

## Preventing Drag/Drop

### Prevent Dragging Specific Items

```jsx
const handleDragStart = (args) => {
  // Prevent dragging tabs with "locked" property
  if (args.draggableData.locked) {
    args.cancel = true;
  }
};

<TabComponent 
  allowDragAndDrop={true}
  onDragStart={handleDragStart}
>
  {/* Tabs */}
</TabComponent>
```

### Prevent Dropping on Specific Positions

```jsx
const handleDragged = (args) => {
  // Revert to original position if dropped on locked tab
  if (args.draggableData.locked) {
    args.cancel = true;  // Reverts the drop
  }
};

<TabComponent 
  allowDragAndDrop={true}
  dragged={handleDragged}
>
  {/* Tabs */}
</TabComponent>
```

## Drag Constraints

### dragArea Property

Define the region where dragged tabs can be moved using `dragArea` property.

```jsx
<TabComponent 
  allowDragAndDrop={true}
  dragArea=".tab-drag-area"
>
  {/* Tabs */}
</TabComponent>
```

### Example: Constrained Drag Area

```jsx
import React from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function ConstrainedDragTab() {
  return (
    <div style={{ padding: '20px' }}>
      <h2>Drag Constrained to Tab Area</h2>
      
      <div 
        className="tab-drag-area"
        style={{
          border: '2px dashed #ccc',
          padding: '20px',
          backgroundColor: '#f9f9f9'
        }}
      >
        <p>Tabs can only be dragged within this bordered area</p>
        
        <TabComponent 
          allowDragAndDrop={true}
          dragArea=".tab-drag-area"
        >
          <TabItemsDirective>
            <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
            <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
            <TabItemDirective header={{ text: 'Tab 3' }} content="Content 3" />
          </TabItemsDirective>
        </TabComponent>
      </div>

      <p style={{ marginTop: '20px' }}>
        Tabs cannot be dragged above or below the dashed border.
      </p>
    </div>
  );
}
```

## Tab-to-Tab Drag Drop

Transfer tabs between two Tab components by dragging.

### How It Works

1. Enable `allowDragAndDrop` on both Tab components
2. Implement `onDragStart` to store dragged tab info
3. Implement `dragged` event to transfer tab to target Tab
4. Use `addTab()` and `removeTab()` methods

### Example: Tab Transfer Between Two Containers

```jsx
import React, { useState, useRef } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function TabToTabDragDrop() {
  const [tab1Items, setTab1Items] = useState([
    { text: 'Tab A', content: 'Content A' },
    { text: 'Tab B', content: 'Content B' }
  ]);

  const [tab2Items, setTab2Items] = useState([
    { text: 'Tab 1', content: 'Content 1' },
    { text: 'Tab 2', content: 'Content 2' }
  ]);

  const tab1Ref = useRef(null);
  const tab2Ref = useRef(null);
  const draggedTabRef = useRef(null);

  const handleDragStart1 = (args) => {
    draggedTabRef.current = {
      item: args.draggableData,
      source: 'tab1',
      index: args.index
    };
  };

  const handleDragStart2 = (args) => {
    draggedTabRef.current = {
      item: args.draggableData,
      source: 'tab2',
      index: args.index
    };
  };

  const handleDragged1 = (args) => {
    const draggedInfo = draggedTabRef.current;
    
    if (draggedInfo && draggedInfo.source === 'tab2') {
      // Add to tab1
      const newItem = tab2Items[draggedInfo.index];
      setTab1Items(prev => [...prev, newItem]);
      
      // Remove from tab2
      setTab2Items(prev => prev.filter((_, i) => i !== draggedInfo.index));
    }
  };

  const handleDragged2 = (args) => {
    const draggedInfo = draggedTabRef.current;
    
    if (draggedInfo && draggedInfo.source === 'tab1') {
      // Add to tab2
      const newItem = tab1Items[draggedInfo.index];
      setTab2Items(prev => [...prev, newItem]);
      
      // Remove from tab1
      setTab1Items(prev => prev.filter((_, i) => i !== draggedInfo.index));
    }
  };

  return (
    <div style={{ padding: '20px', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
      <div>
        <h3>Tab Container 1</h3>
        <p>Drag tabs to Container 2</p>
        <TabComponent 
          ref={tab1Ref}
          allowDragAndDrop={true}
          onDragStart={handleDragStart1}
          dragged={handleDragged1}
        >
          <TabItemsDirective>
            {tab1Items.map((item, index) => (
              <TabItemDirective 
                key={index}
                header={{ text: item.text }}
                content={item.content}
              />
            ))}
          </TabItemsDirective>
        </TabComponent>
      </div>

      <div>
        <h3>Tab Container 2</h3>
        <p>Drag tabs to Container 1</p>
        <TabComponent 
          ref={tab2Ref}
          allowDragAndDrop={true}
          onDragStart={handleDragStart2}
          dragged={handleDragged2}
        >
          <TabItemsDirective>
            {tab2Items.map((item, index) => (
              <TabItemDirective 
                key={index}
                header={{ text: item.text }}
                content={item.content}
              />
            ))}
          </TabItemsDirective>
        </TabComponent>
      </div>
    </div>
  );
}
```

## External Source Integration

### Drag Tabs to TreeView

Transfer tabs to a TreeView component:

```jsx
import React, { useState, useRef } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function TabToTreeViewDragDrop() {
  const [tabItems, setTabItems] = useState([
    { text: 'Folder 1', content: 'Content 1' },
    { text: 'Folder 2', content: 'Content 2' },
    { text: 'Folder 3', content: 'Content 3' }
  ]);

  const [treeItems, setTreeItems] = useState([
    { id: '1', text: 'Archives', expanded: true, children: [] }
  ]);

  const draggedTabRef = useRef(null);

  const handleDragStart = (args) => {
    draggedTabRef.current = {
      item: args.draggableData,
      index: args.index
    };
  };

  const handleDragged = (args) => {
    const draggedInfo = draggedTabRef.current;
    if (draggedInfo) {
      // Add to TreeView
      const newNode = {
        id: Date.now().toString(),
        text: draggedInfo.item.text
      };
      setTreeItems(prev => {
        const updated = JSON.parse(JSON.stringify(prev));
        if (updated[0].children) {
          updated[0].children.push(newNode);
        }
        return updated;
      });

      // Remove from Tab
      setTabItems(prev => prev.filter((_, i) => i !== draggedInfo.index));
    }
  };

  return (
    <div style={{ padding: '20px', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
      <div>
        <h3>Tab Component</h3>
        <p>Drag tabs to TreeView below</p>
        <TabComponent 
          allowDragAndDrop={true}
          onDragStart={handleDragStart}
          dragged={handleDragged}
        >
          <TabItemsDirective>
            {tabItems.map((item, index) => (
              <TabItemDirective 
                key={index}
                header={{ text: item.text }}
                content={item.content}
              />
            ))}
          </TabItemsDirective>
        </TabComponent>
      </div>

      <div>
        <h3>TreeView (Drop Target)</h3>
        <TreeViewComponent fields={{ dataSource: treeItems }} />
      </div>
    </div>
  );
}
```

## Best Practices

1. **Provide Visual Feedback**: Use event handlers to show drag status
2. **Set Constraints**: Use `dragArea` to prevent unintended drops
3. **Handle Edge Cases**: 
   - Prevent dragging disabled tabs
   - Validate drop targets
   - Handle empty tab containers
4. **User Guidance**: Add instructions or help text about drag functionality
5. **Mobile Considerations**: Ensure drag works on touch devices; test thoroughly
6. **Accessibility**: Provide keyboard alternatives to drag-and-drop
