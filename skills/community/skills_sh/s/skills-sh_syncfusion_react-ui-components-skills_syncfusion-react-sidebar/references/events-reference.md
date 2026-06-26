# Events Reference

## Table of Contents
- [Overview](#overview)
- [change Event](#change-event)
- [open Event](#open-event)
- [close Event](#close-event)
- [created Event](#created-event)
- [destroyed Event](#destroyed-event)
- [Event Patterns](#event-patterns)

---

## Overview

The Sidebar component provides 5 events for lifecycle and state tracking. Events can be preventable (open, close) or notification-only (change, created, destroyed).

---

## change Event

Triggers when the sidebar state changes (expand/collapse). This is the primary event for tracking state transitions. Note: For `Auto` type sidebars, state changes on viewport resize will not include user interaction flag.

**Event Type:** `EmitType<ChangeEventArgs>`

**Callback Signature:**
```typescript
(args: ChangeEventArgs) => void
```

**Example 1: Track sidebar state changes**
```jsx
import React, { useState } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const [sidebarState, setSidebarState] = useState('closed');

  const handleChange = (args) => {
    if (args.element.classList.contains('e-open')) {
      setSidebarState('open');
      console.log('Sidebar opened');
    } else {
      setSidebarState('closed');
      console.log('Sidebar closed');
    }
  };

  return (
    <>
      <div>Sidebar is: {sidebarState}</div>
      <SidebarComponent
        change={handleChange}
        type="Over"
        width="250px"
      >
        Content
      </SidebarComponent>
    </>
  );
}

export default App;
```

**Example 2: Differentiate user interaction from programmatic changes**
```jsx
const handleChange = (args) => {
  if (args.isInteracted) {
    console.log('User manually toggled sidebar');
  } else {
    console.log('Sidebar state changed programmatically');
  }
};

return <SidebarComponent change={handleChange} />;
```

**Example 3: Log event name with change event**
```jsx
const handleChange = (args) => {
  console.log(`Event: ${args.name}`);
  console.log(`Is User Interaction: ${args.isInteracted}`);
  console.log(`Element:`, args.element);
};

return <SidebarComponent change={handleChange} />;
```

---

## open Event

Triggers when the sidebar is about to open. You can prevent the opening by setting `args.cancel = true`.

**Event Type:** `EmitType<EventArgs>`

**Callback Signature:**
```typescript
(args: EventArgs) => void
```

**Example 1: Allow conditional opening**
```jsx
import React, { useState } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const [isAuthorized, setIsAuthorized] = useState(true);

  const handleOpen = (args) => {
    if (!isAuthorized) {
      args.cancel = true;  // Prevent opening
      alert('Not authorized to open sidebar');
    } else {
      console.log('Opening sidebar...');
    }
  };

  return (
    <SidebarComponent
      open={handleOpen}
      type="Over"
    >
      Sidebar Content
    </SidebarComponent>
  );
}

export default App;
```

**Example 2: Access event details**
```jsx
const handleOpen = (args) => {
  console.log('Open triggered by:', args.event);
  console.log('User interaction:', args.isInteracted);
  console.log('Element:', args.element);
};

return <SidebarComponent open={handleOpen} />;
```

**Example 3: Cancel based on external state**
```jsx
const handleOpen = (args) => {
  if (userPreferences.sidebarDisabled) {
    args.cancel = true;
    showNotification('Sidebar is disabled');
  }
};

return <SidebarComponent open={handleOpen} />;
```

---

## close Event

Triggers when the sidebar is about to close. You can prevent the closing by setting `args.cancel = true`.

**Event Type:** `EmitType<EventArgs>`

**Callback Signature:**
```typescript
(args: EventArgs) => void
```

**Example 1: Confirm before closing**
```jsx
import React, { useState } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);

  const handleClose = (args) => {
    if (hasUnsavedChanges) {
      const proceed = window.confirm(
        'You have unsaved changes. Close anyway?'
      );
      if (!proceed) {
        args.cancel = true;  // Prevent closing
      }
    }
  };

  return (
    <SidebarComponent
      close={handleClose}
      type="Over"
    >
      Sidebar Content
    </SidebarComponent>
  );
}

export default App;
```

**Example 2: Track close events**
```jsx
const handleClose = (args) => {
  console.log('Closing sidebar...');
  console.log('User triggered:', args.isInteracted);
  
  if (args.isInteracted) {
    console.log('User clicked to close');
  } else {
    console.log('Close triggered programmatically');
  }
};

return <SidebarComponent close={handleClose} />;
```

**Example 3: Save state before closing**
```jsx
const handleClose = (args) => {
  // Save current sidebar state to localStorage
  localStorage.setItem('sidebarOpen', 'false');
  console.log('Sidebar state saved');
};

return <SidebarComponent close={handleClose} />;
```

---

## created Event

Triggers after the sidebar component is initialized, rendered into the DOM, and ready to use. This is the ideal place to set up additional event listeners, initialize child components, or perform setup tasks.

**Event Type:** `EmitType<Object>`

**Callback Signature:**
```typescript
() => void
```

**Example 1: Initialize on component creation**
```jsx
import React, { useRef } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const sidebarRef = useRef(null);

  const handleCreated = () => {
    console.log('Sidebar created and initialized');
    console.log('Sidebar element:', sidebarRef.current?.element);
  };

  return (
    <SidebarComponent
      ref={sidebarRef}
      created={handleCreated}
      type="Over"
    >
      Sidebar Content
    </SidebarComponent>
  );
}

export default App;
```

**Example 2: Setup custom event listeners**
```jsx
const handleCreated = () => {
  const sidebarElement = sidebarRef.current?.element;
  
  // Add custom keyboard shortcuts
  sidebarElement?.addEventListener('keydown', (e) => {
    if (e.key === 's') {
      // Custom action
    }
  });

  console.log('Custom event listeners attached');
};

return (
  <SidebarComponent
    ref={sidebarRef}
    created={handleCreated}
  />
);
```

**Example 3: Initialize related components**
```jsx
const handleCreated = () => {
  console.log('Sidebar is ready');
  
  // Initialize ListView or other components
  initializeNavigationItems();
  loadUserPreferences();
};

return (
  <SidebarComponent created={handleCreated} />
);
```

---

## destroyed Event

Triggers when the sidebar component is destroyed/removed. Use this to clean up resources, remove event listeners, or perform tear-down tasks.

**Event Type:** `EmitType<Object>`

**Callback Signature:**
```typescript
() => void
```

**Example 1: Cleanup on destroy**
```jsx
import React, { useRef } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const sidebarRef = useRef(null);

  const handleDestroyed = () => {
    console.log('Sidebar destroyed');
    console.log('Cleaning up resources...');
  };

  return (
    <SidebarComponent
      ref={sidebarRef}
      destroyed={handleDestroyed}
      type="Over"
    >
      Sidebar Content
    </SidebarComponent>
  );
}

export default App;
```

**Example 2: Remove custom listeners on destroy**
```jsx
const handleDestroyed = () => {
  // Remove custom event listeners
  const sidebarElement = sidebarRef.current?.element;
  sidebarElement?.removeEventListener('keydown', customKeyHandler);
  
  // Clear cached data
  sessionStorage.removeItem('sidebarState');
  
  console.log('Resources cleaned up');
};

return (
  <SidebarComponent destroyed={handleDestroyed} />
);
```

**Example 3: Notify parent component**
```jsx
const handleDestroyed = () => {
  if (onSidebarDestroyed) {
    onSidebarDestroyed();
  }
};

return (
  <SidebarComponent destroyed={handleDestroyed} />
);
```

---

## Event Patterns

### State Tracking Pattern

```jsx
const [isOpen, setIsOpen] = useState(false);

<SidebarComponent
  change={(args) => {
    setIsOpen(args.element.classList.contains('e-open'));
  }}
/>
```

### Prevention Pattern

```jsx
const handleOpen = (args) => {
  if (!canOpen) {
    args.cancel = true;
  }
};

<SidebarComponent open={handleOpen} />
```

### Lifecycle Pattern

```jsx
<SidebarComponent
  created={() => setupListeners()}
  destroyed={() => cleanupListeners()}
/>
```

### Interaction Detection Pattern

```jsx
const handleChange = (args) => {
  if (args.isInteracted) {
    console.log('User action');
  } else {
    console.log('Programmatic change');
  }
};

<SidebarComponent change={handleChange} />
```

---
