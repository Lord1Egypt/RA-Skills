# Methods Reference

## Table of Contents
- [Overview](#overview)
- [show()](#show)
- [hide()](#hide)
- [toggle()](#toggle)
- [destroy()](#destroy)
- [Method Patterns](#method-patterns)

---

## Overview

The Sidebar component provides 4 public methods for programmatic control. All methods return `void`.

---

## show()

Displays the sidebar if currently closed. Triggers the `open` event. Optionally accepts an Event parameter that triggered the show action.

**Signature:**
```typescript
show(e?: Event): void
```

**Parameters:**
| Parameter | Type | Optional | Description |
|-----------|------|----------|-------------|
| `e` | `Event` | Yes | The DOM event that triggered the show action (e.g., click, keydown) |

**Returns:** `void`

**Example 1: Basic show() without event**
```jsx
import React, { useRef } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const sidebarRef = useRef(null);

  const handleShow = () => {
    sidebarRef.current?.show();
  };

  return (
    <>
      <button onClick={handleShow}>Open Sidebar</button>
      <SidebarComponent 
        ref={sidebarRef}
        type="Over"
        width="250px"
      >
        <div>Sidebar Content</div>
      </SidebarComponent>
    </>
  );
}

export default App;
```

**Example 2: show() with event parameter from click handler**
```jsx
const handleShowWithEvent = (e) => {
  sidebarRef.current?.show(e);
};

return (
  <button onClick={handleShowWithEvent}>
    Open Sidebar
  </button>
);
```

**Example 3: show() with keyboard event**
```jsx
const handleKeyPress = (e) => {
  if (e.key === 'Enter') {
    sidebarRef.current?.show(e);
  }
};

return (
  <input 
    type="button" 
    value="Show on Enter"
    onKeyPress={handleKeyPress}
  />
);
```

---

## hide()

Hides the sidebar if currently open. Triggers the `close` event. Optionally accepts an Event parameter that triggered the hide action.

**Signature:**
```typescript
hide(e?: Event): void
```

**Parameters:**
| Parameter | Type | Optional | Description |
|-----------|------|----------|-------------|
| `e` | `Event` | Yes | The DOM event that triggered the hide action |

**Returns:** `void`

**Example 1: Basic hide() without event**
```jsx
function App() {
  const sidebarRef = useRef(null);

  const handleHide = () => {
    sidebarRef.current?.hide();
  };

  return (
    <>
      <button onClick={handleHide}>Close Sidebar</button>
      <SidebarComponent ref={sidebarRef} type="Over" width="250px" />
    </>
  );
}
```

**Example 2: hide() with event from button click**
```jsx
const handleHideWithEvent = (e) => {
  sidebarRef.current?.hide(e);
};

return (
  <button onClick={handleHideWithEvent}>
    Close Sidebar
  </button>
);
```

**Example 3: hide() on escape key press**
```jsx
import { useEffect } from 'react';

useEffect(() => {
  const handleEscapeKey = (e) => {
    if (e.key === 'Escape') {
      sidebarRef.current?.hide(e);
    }
  };

  document.addEventListener('keydown', handleEscapeKey);
  return () => document.removeEventListener('keydown', handleEscapeKey);
}, []);
```

---

## toggle()

Toggles the sidebar between open and closed states. Automatically triggers appropriate `open` or `close` events.

**Signature:**
```typescript
toggle(): void
```

**Returns:** `void`

**Example 1: Basic toggle**
```jsx
import React, { useRef } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const sidebarRef = useRef(null);

  const handleToggle = () => {
    sidebarRef.current?.toggle();
  };

  return (
    <>
      <button className="e-btn e-primary" onClick={handleToggle}>
        ☰ Menu
      </button>
      <SidebarComponent 
        ref={sidebarRef}
        type="Over"
        width="250px"
      >
        <div>Navigation Items</div>
      </SidebarComponent>
    </>
  );
}

export default App;
```

**Example 2: Toggle with state synchronization**
```jsx
import { useState } from 'react';

function App() {
  const sidebarRef = useRef(null);
  const [isOpen, setIsOpen] = useState(false);

  const handleToggle = () => {
    sidebarRef.current?.toggle();
    setIsOpen(!isOpen);
  };

  return (
    <>
      <button onClick={handleToggle}>
        {isOpen ? 'Close' : 'Open'} Sidebar
      </button>
      <SidebarComponent ref={sidebarRef} type="Over" />
    </>
  );
}
```

---

## destroy()

Removes the sidebar component from the DOM and detaches all event handlers, attributes, and classes. After calling `destroy()`, the component must be re-initialized to use again.

**Signature:**
```typescript
destroy(): void
```

**Returns:** `void`

**Example 1: Basic destroy**
```jsx
function App() {
  const sidebarRef = useRef(null);

  const handleDestroy = () => {
    sidebarRef.current?.destroy();
  };

  return (
    <>
      <button onClick={handleDestroy}>
        Destroy Sidebar
      </button>
      <SidebarComponent ref={sidebarRef} />
    </>
  );
}
```

**Example 2: Cleanup on component unmount**
```jsx
import { useEffect } from 'react';

function App() {
  const sidebarRef = useRef(null);

  useEffect(() => {
    return () => {
      // Cleanup: destroy sidebar when component unmounts
      sidebarRef.current?.destroy();
    };
  }, []);

  return (
    <SidebarComponent ref={sidebarRef} type="Over" />
  );
}
```

**Example 3: Destroy and recreate pattern**
```jsx
function App() {
  const containerRef = useRef(null);
  const [destroyed, setDestroyed] = useState(false);

  const handleDestroyAndRecreate = () => {
    if (!destroyed) {
      containerRef.current?.destroy();
      setDestroyed(true);
    } else {
      setDestroyed(false);
    }
  };

  return (
    <>
      <button onClick={handleDestroyAndRecreate}>
        {destroyed ? 'Recreate' : 'Destroy'}
      </button>
      {!destroyed && (
        <SidebarComponent ref={containerRef} type="Over" />
      )}
    </>
  );
}
```

---

## Method Patterns

### Control Pattern: show/hide

```jsx
// Explicit show/hide control
const handleShowSidebar = () => sidebarRef.current?.show();
const handleHideSidebar = () => sidebarRef.current?.hide();

return (
  <>
    <button onClick={handleShowSidebar}>Open</button>
    <button onClick={handleHideSidebar}>Close</button>
    <SidebarComponent ref={sidebarRef} />
  </>
);
```

### Toggle Pattern

```jsx
// Simple toggle for hamburger menus
<button onClick={() => sidebarRef.current?.toggle()}>
  ☰ Menu
</button>
```

### Event Parameter Pattern

```jsx
// Pass event context to methods
const handleMenuClick = (e) => {
  sidebarRef.current?.show(e);
};
```

### Lifecycle Pattern

```jsx
useEffect(() => {
  return () => {
    sidebarRef.current?.destroy();
  };
}, []);
```

---
