# Event Arguments Reference

## Table of Contents
- [Overview](#overview)
- [ChangeEventArgs](#changeeventargs)
- [EventArgs](#eventargs)
- [SidebarModel](#sidebarmodel)

---

## Overview

This reference documents the argument objects passed to Sidebar event handlers. Understanding these objects is essential for implementing proper event handling.

---

## ChangeEventArgs

Passed to the `change` event handler. Represents state change notification with user interaction tracking.

**Type Definition:**
```typescript
interface ChangeEventArgs {
  element: HTMLElement      // The Sidebar DOM element
  name: string             // Event name string ('change')
  cancel?: boolean         // Set to true to prevent the state change
  isInteracted: boolean    // True if state changed by user interaction
                           // False if changed programmatically
}
```

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `element` | `HTMLElement` | Reference to the Sidebar DOM element |
| `name` | `string` | The name of the event ('change') |
| `cancel` | `boolean` (optional) | Set to `true` to prevent the state change |
| `isInteracted` | `boolean` | Indicates whether the state change was caused by user interaction (click, gesture, key) vs programmatic methods (show/hide/toggle) |

**Usage Examples:**

**Example 1: Check interaction type**
```jsx
import { useState } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const [changeLog, setChangeLog] = useState([]);

  const handleChange = (args) => {
    if (args.isInteracted) {
      console.log('User manually changed sidebar state');
      setChangeLog(prev => [...prev, 'User action']);
    } else {
      console.log('State changed by program (show/hide/toggle methods)');
      setChangeLog(prev => [...prev, 'Programmatic change']);
    }
  };

  return (
    <div>
      <ul>
        {changeLog.map((log, i) => <li key={i}>{log}</li>)}
      </ul>
      <SidebarComponent change={handleChange} />
    </div>
  );
}

export default App;
```

**Example 2: Access element properties**
```jsx
const handleChange = (args) => {
  const isOpen = args.element.classList.contains('e-open');
  const isAnimating = args.element.classList.contains('e-animate');
  console.log('Open:', isOpen, 'Animating:', isAnimating);
};

return <SidebarComponent change={handleChange} />;
```

**Example 3: Cancel state change (edge case)**
```jsx
const handleChange = (args) => {
  // Rarely used, but example for reference
  if (restrictedMode && !args.isInteracted) {
    args.cancel = true;
  }
};

return <SidebarComponent change={handleChange} />;
```

---

## EventArgs

Passed to `open`, `close`, `created`, and `destroyed` event handlers. Provides detailed event information including the triggering event and sidebar model.

**Type Definition:**
```typescript
interface EventArgs {
  cancel?: boolean              // Set to true to prevent the action (open/close)
  element: HTMLElement          // The Sidebar DOM element
  event?: MouseEvent | Event    // Original DOM event that triggered the action
  isInteracted?: boolean        // True if triggered by user interaction
  model: SidebarModel          // Current Sidebar configuration model
}
```

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `cancel` | `boolean` (optional) | For `open`/`close` events, set to `true` to prevent the action |
| `element` | `HTMLElement` | Reference to the Sidebar DOM element |
| `event` | `MouseEvent \| Event` (optional) | The original DOM event that triggered this event (e.g., click, keydown) |
| `isInteracted` | `boolean` (optional) | Indicates whether the event was triggered by user interaction |
| `model` | `SidebarModel` | The complete Sidebar configuration model at time of event |

**Usage Examples:**

**Example 1: Prevent opening based on conditions**
```jsx
import React from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const [userAuthorized, setUserAuthorized] = React.useState(false);

  const handleOpen = (args) => {
    if (!userAuthorized) {
      args.cancel = true;
      console.log('Opening cancelled - authorization required');
    }
  };

  return (
    <SidebarComponent open={handleOpen} type="Over">
      Sidebar Content
    </SidebarComponent>
  );
}

export default App;
```

**Example 2: Access event source**
```jsx
const handleClose = (args) => {
  if (args.event) {
    console.log('Close triggered by:', args.event.type);
    console.log('Target element:', args.event.target);
  }
};

return <SidebarComponent close={handleClose} />;
```

**Example 3: Access sidebar model configuration**
```jsx
const handleOpen = (args) => {
  // Check current configuration
  console.log('Current sidebar type:', args.model.type);
  console.log('Current position:', args.model.position);
  console.log('Current width:', args.model.width);
  console.log('Animations enabled:', args.model.animate);
};

return <SidebarComponent open={handleOpen} />;
```

**Example 4: Distinguish event types**
```jsx
const handleOpen = (args) => {
  if (args.isInteracted) {
    console.log('User triggered opening (click, gesture, key)');
  } else {
    console.log('Program triggered opening (show/toggle methods)');
  }
};

return <SidebarComponent open={handleOpen} />;
```

**Example 5: Conditional actions on close**
```jsx
const handleClose = (args) => {
  // Different logic for user vs programmatic close
  if (args.isInteracted) {
    // User-triggered close - save preference
    localStorage.setItem('userClosedSidebar', 'true');
  } else {
    // Programmatic close
    console.log('Sidebar closed by app logic');
  }
};

return <SidebarComponent close={handleClose} />;
```

---

## SidebarModel

Reference object containing the complete Sidebar configuration at time of event.

**Type Definition:**
```typescript
interface SidebarModel {
  type: 'Over' | 'Push' | 'Slide' | 'Auto'
  position: 'Left' | 'Right'
  width: string | number
  target?: HTMLElement | string
  isOpen: boolean
  animate: boolean
  showBackdrop: boolean
  closeOnDocumentClick: boolean
  enableDock: boolean
  dockSize: string | number
  enableGestures: boolean
  enableRtl: boolean
  enablePersistence: boolean
  mediaQuery?: string | MediaQueryList
  zIndex: string | number
}
```

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `type` | `'Over' \| 'Push' \| 'Slide' \| 'Auto'` | Display mode |
| `position` | `'Left' \| 'Right'` | Sidebar placement |
| `width` | `string \| number` | Current width setting |
| `target` | `HTMLElement \| string` (optional) | Container element |
| `isOpen` | `boolean` | Current open state |
| `animate` | `boolean` | Animation enabled |
| `showBackdrop` | `boolean` | Overlay visible |
| `closeOnDocumentClick` | `boolean` | Auto-close enabled |
| `enableDock` | `boolean` | Dock mode enabled |
| `dockSize` | `string \| number` | Dock width |
| `enableGestures` | `boolean` | Touch gestures enabled |
| `enableRtl` | `boolean` | RTL mode enabled |
| `enablePersistence` | `boolean` | Persistence enabled |
| `mediaQuery` | `string \| MediaQueryList` (optional) | Responsive query |
| `zIndex` | `string \| number` | CSS z-index |

**Usage Examples:**

**Example 1: Log all configuration on open**
```jsx
const handleOpen = (args) => {
  console.log('Sidebar Configuration:', {
    type: args.model.type,
    position: args.model.position,
    width: args.model.width,
    openState: args.model.isOpen,
    animations: args.model.animate,
    backdrop: args.model.showBackdrop,
  });
};

return <SidebarComponent open={handleOpen} />;
```

**Example 2: Verify responsive behavior**
```jsx
const handleOpen = (args) => {
  if (args.model.type === 'Auto') {
    console.log('Sidebar is in responsive Auto mode');
  }
  
  if (args.model.mediaQuery) {
    console.log('Media query set:', args.model.mediaQuery);
  }
};

return <SidebarComponent open={handleOpen} type="Auto" />;
```

**Example 3: Check persistence settings**
```jsx
const handleOpen = (args) => {
  if (args.model.enablePersistence) {
    console.log('Sidebar state will be saved to storage');
  }
};

return (
  <SidebarComponent 
    open={handleOpen}
    enablePersistence={true}
  />
);
```

---
