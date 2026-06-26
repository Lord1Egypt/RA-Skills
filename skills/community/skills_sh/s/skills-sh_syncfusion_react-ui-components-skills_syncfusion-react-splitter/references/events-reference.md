# Splitter Events Reference

## Table of Contents
- [created](#created)
- [beforeCollapse](#beforecollapse)
- [collapsed](#collapsed)
- [beforeExpand](#beforeexpand)
- [expanded](#expanded)
- [resizeStart](#resizestart)
- [resizing](#resizing)
- [resizeStop](#resizestop)
- [beforeSanitizeHtml](#beforesanitizehtml)
- [Event Handling Patterns](#event-handling-patterns)

---

## created

**Event:** `created`

**Description:** Fires when the Splitter component is created and initialized. Useful for performing initialization tasks after the component is ready.

**Event Arguments:** `CreateEventArgs`

**Properties:**
- `element` (HTMLElement): The Splitter DOM element
- `name` (string): The name of the event

**Example:**

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from "react";

function App() {
  const onCreated = (args: any) => {
    console.log('Splitter created successfully', args.element);
  };

  return (
    <SplitterComponent
      height="250px"
      width="600px"
      created={onCreated}
    >
      <PanesDirective>
        <PaneDirective size='200px'>
          <div>Pane 1</div>
        </PaneDirective>
        <PaneDirective size='200px'>
          <div>Pane 2</div>
        </PaneDirective>
      </PanesDirective>
    </SplitterComponent>
  );
}

export default App;
```

**When to Use:**
- Initialize third-party libraries within panes
- Set up event listeners on pane content
- Perform calculations based on pane dimensions
- Apply initial styling or animations

**Common Patterns:**
```tsx
const handleCreated = (args: any) => {
  // Access pane dimensions
  console.log('Total splitter height:', args.element.offsetHeight);
  
  // Set up content after initialization
  const panes = args.element.querySelectorAll('.e-pane');
  panes.forEach((pane: HTMLElement) => {
    pane.classList.add('initialized');
  });
};
```

---

## beforeCollapse

**Event:** `beforeCollapse`

**Description:** Fires before a pane is collapsed. You can cancel the collapse operation by setting `cancel: true` in the event args.

**Event Arguments:** `BeforeCollapseEventArgs`

**Properties:**
- `index` (number): Index of the pane being collapsed
- `element` (HTMLElement): The Splitter element
- `cancel` (boolean): Set to true to prevent collapse

**Example - Allow/Prevent Collapse:**

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from "react";

function App() {
  const onBeforeCollapse = (args: any) => {
    // Prevent collapsing pane at index 0
    if (args.index === 0) {
      args.cancel = true;
      console.log('Cannot collapse the first pane');
    } else {
      console.log(`Collapsing pane at index: ${args.index}`);
    }
  };

  return (
    <SplitterComponent
      height="300px"
      width="600px"
      beforeCollapse={onBeforeCollapse}
    >
      <PanesDirective>
        <PaneDirective size='200px' collapsible={true}>
          <div>Primary pane (cannot collapse)</div>
        </PaneDirective>
        <PaneDirective size='200px' collapsible={true}>
          <div>Secondary pane (can collapse)</div>
        </PaneDirective>
      </PanesDirective>
    </SplitterComponent>
  );
}

export default App;
```

**When to Use:**
- Validate data before hiding panes
- Prevent collapse of critical sections
- Show confirmation dialogs before collapse
- Log user interactions for analytics

---

## collapsed

**Event:** `collapsed`

**Description:** Fires after a pane is successfully collapsed. Use this event for post-collapse actions.

**Event Arguments:** `CollapsedEventArgs`

**Properties:**
- `index` (number): Index of the collapsed pane
- `element` (HTMLElement): The Splitter element

**Example - Update State After Collapse:**

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from "react";

function App() {
  const [collapsedPanes, setCollapsedPanes] = React.useState<number[]>([]);

  const onCollapsed = (args: any) => {
    setCollapsedPanes((prev) => [...prev, args.index]);
    console.log(`Pane ${args.index} collapsed`);
    console.log('All collapsed panes:', [...collapsedPanes, args.index]);
  };

  return (
    <div>
      <div>Collapsed panes: {collapsedPanes.join(', ')}</div>
      <SplitterComponent
        height="300px"
        width="600px"
        collapsed={onCollapsed}
      >
        <PanesDirective>
          <PaneDirective size='200px' collapsible={true}>
            <div>Pane 1</div>
          </PaneDirective>
          <PaneDirective size='200px' collapsible={true}>
            <div>Pane 2</div>
          </PaneDirective>
        </PanesDirective>
      </SplitterComponent>
    </div>
  );
}

export default App;
```

**When to Use:**
- Update UI state after pane collapse
- Trigger dependent actions
- Log analytics events
- Refresh content in remaining panes

---

## beforeExpand

**Event:** `beforeExpand`

**Description:** Fires before a pane is expanded. You can cancel the expand operation by setting `cancel: true` in the event args.

**Event Arguments:** `BeforeExpandEventArgs`

**Properties:**
- `index` (number): Index of the pane being expanded
- `element` (HTMLElement): The Splitter element
- `cancel` (boolean): Set to true to prevent expand

**Example - Confirm Expansion:**

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from "react";

function App() {
  const onBeforeExpand = (args: any) => {
    // Show confirmation or validate state before expanding
    console.log(`Attempting to expand pane ${args.index}`);
    
    // Example: Only expand if valid state
    const isValidState = true; // Your validation logic
    if (!isValidState) {
      args.cancel = true;
      console.log('Cannot expand: Invalid state');
    }
  };

  return (
    <SplitterComponent
      height="300px"
      width="600px"
      beforeExpand={onBeforeExpand}
    >
      <PanesDirective>
        <PaneDirective size='200px' collapsed={true} collapsible={true}>
          <div>Collapsible pane</div>
        </PaneDirective>
        <PaneDirective size='200px'>
          <div>Content pane</div>
        </PaneDirective>
      </PanesDirective>
    </SplitterComponent>
  );
}

export default App;
```

**When to Use:**
- Load data before expanding
- Validate state before showing content
- Prevent expansion under certain conditions
- Require confirmation from user

---

## expanded

**Event:** `expanded`

**Description:** Fires after a pane is successfully expanded. Use for post-expansion actions and content updates.

**Event Arguments:** `ExpandedEventArgs`

**Properties:**
- `index` (number): Index of the expanded pane
- `element` (HTMLElement): The Splitter element

**Example - Load Content on Expand:**

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from "react";

function App() {
  const [expandedPanes, setExpandedPanes] = React.useState<number[]>([]);

  const onExpanded = (args: any) => {
    // Load content for expanded pane
    const paneElement = args.element.querySelectorAll('.e-pane')[args.index];
    console.log(`Pane ${args.index} expanded`);
    
    setExpandedPanes((prev) => [...prev, args.index]);
    
    // Trigger content loading
    loadPaneContent(args.index);
  };

  const loadPaneContent = (index: number) => {
    console.log(`Loading content for pane ${index}...`);
    // Fetch or render content
  };

  return (
    <SplitterComponent
      height="300px"
      width="600px"
      expanded={onExpanded}
    >
      <PanesDirective>
        <PaneDirective size='200px' collapsed={true} collapsible={true}>
          <div>Lazy-loaded pane</div>
        </PaneDirective>
        <PaneDirective size='200px'>
          <div>Content pane</div>
        </PaneDirective>
      </PanesDirective>
    </SplitterComponent>
  );
}

export default App;
```

**When to Use:**
- Load pane content on-demand
- Update UI state after expansion
- Refresh pane data
- Trigger dependent UI updates

---

## resizeStart

**Event:** `resizeStart`

**Description:** Fires when the user starts dragging the separator to resize panes. Use to prepare for resize operations.

**Event Arguments:** `ResizeEventArgs`

**Properties:**
- `index` (number): Index of the pane being resized
- `element` (HTMLElement): The Splitter element
- `previous` (number): Previous pane size
- `current` (number): Current pane size

**Example - Show Resize Indicator:**

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from "react";

function App() {
  const [isResizing, setIsResizing] = React.useState(false);

  const onResizeStart = (args: any) => {
    setIsResizing(true);
    console.log(`Resize started for pane ${args.index}`);
    console.log(`Previous size: ${args.previous}px`);
  };

  return (
    <div>
      {isResizing && <div className="resize-indicator">Resizing...</div>}
      <SplitterComponent
        height="300px"
        width="600px"
        resizeStart={onResizeStart}
      >
        <PanesDirective>
          <PaneDirective size='200px'>
            <div>Pane 1</div>
          </PaneDirective>
          <PaneDirective size='200px'>
            <div>Pane 2</div>
          </PaneDirective>
        </PanesDirective>
      </SplitterComponent>
    </div>
  );
}

export default App;
```

**When to Use:**
- Show resize handles or indicators
- Disable other interactions during resize
- Log analytics for resize events
- Freeze content updates during drag

---

## resizing

**Event:** `resizing`

**Description:** Fires continuously while the user is dragging the separator. Useful for real-time feedback during resize operations.

**Event Arguments:** `ResizingEventArgs`

**Properties:**
- `index` (number): Index of the pane being resized
- `element` (HTMLElement): The Splitter element
- `previous` (number): Previous pane size
- `current` (number): Current pane size (changes as user drags)
- `cancel` (boolean): Set to true to cancel the resize

**Example - Prevent Resize Below Minimum:**

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from "react";

function App() {
  const [sizes, setSizes] = React.useState({ pane1: 200, pane2: 200 });

  const onResizing = (args: any) => {
    setSizes({ pane1: args.previous, pane2: args.current });
    
    // Custom validation: prevent pane from going below 100px
    if (args.current < 100) {
      args.cancel = true;
      console.log('Resize cancelled: Below minimum size');
    }
  };

  return (
    <div>
      <div>Pane 1: {sizes.pane1}px | Pane 2: {sizes.pane2}px</div>
      <SplitterComponent
        height="300px"
        width="600px"
        resizing={onResizing}
      >
        <PanesDirective>
          <PaneDirective size='200px' min='100px'>
            <div>Pane 1</div>
          </PaneDirective>
          <PaneDirective size='200px' min='100px'>
            <div>Pane 2</div>
          </PaneDirective>
        </PanesDirective>
      </SplitterComponent>
    </div>
  );
}

export default App;
```

**When to Use:**
- Display real-time size feedback
- Validate resize operations
- Update dependent layouts
- Prevent invalid resize operations

---

## resizeStop

**Event:** `resizeStop`

**Description:** Fires when the user finishes dragging the separator and releases the mouse. Use for post-resize actions.

**Event Arguments:** `ResizeEventArgs`

**Properties:**
- `index` (number): Index of the pane that was resized
- `element` (HTMLElement): The Splitter element
- `previous` (number): Previous pane size
- `current` (number): Final pane size after resize

**Example - Save Resize State:**

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from "react";

function App() {
  const [isResizing, setIsResizing] = React.useState(false);

  const onResizeStop = (args: any) => {
    setIsResizing(false);
    console.log(`Resize completed for pane ${args.index}`);
    console.log(`Final size: ${args.current}px (was ${args.previous}px)`);
    
    // Save layout preferences
    savePaneSize(args.index, args.current);
  };

  const savePaneSize = (index: number, size: number) => {
    const sizes = JSON.parse(localStorage.getItem('pane-sizes') || '{}');
    sizes[`pane-${index}`] = size;
    localStorage.setItem('pane-sizes', JSON.stringify(sizes));
    console.log('Layout saved to localStorage');
  };

  return (
    <SplitterComponent
      height="300px"
      width="600px"
      resizeStart={() => setIsResizing(true)}
      resizeStop={onResizeStop}
    >
      <PanesDirective>
        <PaneDirective size='200px'>
          <div>Pane 1</div>
        </PaneDirective>
        <PaneDirective size='200px'>
          <div>Pane 2</div>
        </PaneDirective>
      </PanesDirective>
    </SplitterComponent>
  );
}

export default App;
```

**When to Use:**
- Save user layout preferences
- Remove resize indicators
- Refresh dependent components
- Perform heavy calculations after resize completes
- Persist state to local storage or database

---

## beforeSanitizeHtml

**Event:** `beforeSanitizeHtml`

**Description:** Fires before HTML content is sanitized. This event allows you to customize the sanitization process by modifying attributes or elements that should be removed or preserved. Use this event to whitelist specific HTML elements or attributes that should bypass sanitization.

**Event Arguments:** `BeforeSanitizeHtmlArgs`

**Properties:**
- `value` (string): The HTML content to be sanitized
- `cancel` (boolean): Set to true to prevent default sanitization

**Example - Customize Sanitization Rules:**

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from "react";

function App() {
  const onBeforeSanitizeHtml = (args: any) => {
    // Log content before sanitization
    console.log('Content before sanitization:', args.value);
    
    // Example: Allow specific data attributes
    // The sanitizer will process the content according to your requirements
    // You can analyze the content and modify if needed
  };

  return (
    <SplitterComponent
      height="300px"
      width="600px"
      enableHtmlSanitizer={true}
      beforeSanitizeHtml={onBeforeSanitizeHtml}
    >
      <PanesDirective>
        <PaneDirective content="<div data-id='123'>Content with data attribute</div>">
          <div>Pane 1</div>
        </PaneDirective>
        <PaneDirective>
          <div>Pane 2</div>
        </PaneDirective>
      </PanesDirective>
    </SplitterComponent>
  );
}

export default App;
```

**Example - Monitor Sanitization Events:**

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from "react";

function App() {
  const [sanitizationLog, setSanitizationLog] = React.useState<string[]>([]);

  const onBeforeSanitizeHtml = (args: any) => {
    const logEntry = `Sanitizing: ${args.value.substring(0, 50)}...`;
    setSanitizationLog((prev) => [...prev, logEntry]);
    console.log('Sanitization event fired:', args);
  };

  return (
    <div>
      <div className="log">
        <h4>Sanitization Log:</h4>
        <ul>
          {sanitizationLog.map((entry, index) => (
            <li key={index}>{entry}</li>
          ))}
        </ul>
      </div>
      <SplitterComponent
        height="300px"
        width="600px"
        enableHtmlSanitizer={true}
        beforeSanitizeHtml={onBeforeSanitizeHtml}
      >
        <PanesDirective>
          <PaneDirective content="<div><h3>Safe Content</h3></div>">
            <div>Pane 1</div>
          </PaneDirective>
          <PaneDirective content="<p>Paragraph content</p>">
            <div>Pane 2</div>
          </PaneDirective>
        </PanesDirective>
      </SplitterComponent>
    </div>
  );
}

export default App;
```

**When to Use:**
- Monitor which HTML content is being sanitized
- Log sanitization events for debugging
- Implement custom sanitization logic
- Track user-provided content being processed
- Audit security-sensitive operations

**Security Considerations:**
- Always keep `enableHtmlSanitizer={true}` unless you control all content sources
- Use beforeSanitizeHtml only for monitoring or logging
- Do not disable sanitization in production for untrusted content
- XSS attacks can compromise your application - sanitization protects users

---

## Event Handling Patterns

### Pattern 1: Track All Pane State Changes

```tsx
const [paneState, setPaneState] = React.useState({
  collapsed: [false, false],
  sizes: [200, 200]
});

const handleBeforeCollapse = (args: any) => {
  if (args.index === 0) args.cancel = true;
};

const handleCollapsed = (args: any) => {
  setPaneState({
    ...paneState,
    collapsed: paneState.collapsed.map((c, i) => i === args.index ? true : c)
  });
};

const handleExpanded = (args: any) => {
  setPaneState({
    ...paneState,
    collapsed: paneState.collapsed.map((c, i) => i === args.index ? false : c)
  });
};

const handleResizeStop = (args: any) => {
  setPaneState({
    ...paneState,
    sizes: paneState.sizes.map((s, i) => i === args.index ? args.current : s)
  });
};

return (
  <SplitterComponent
    beforeCollapse={handleBeforeCollapse}
    collapsed={handleCollapsed}
    expanded={handleExpanded}
    resizeStop={handleResizeStop}
  >
    {/* Panes */}
  </SplitterComponent>
);
```

### Pattern 2: Persist and Restore Layout

```tsx
const STORAGE_KEY = 'splitter-layout';

const saveLayout = (state: any) => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
};

const restoreLayout = () => {
  return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
};

const handleCollapsed = (args: any) => {
  const state = restoreLayout();
  state.collapsed = state.collapsed || [];
  state.collapsed[args.index] = true;
  saveLayout(state);
};

const handleResizeStop = (args: any) => {
  const state = restoreLayout();
  state.sizes = state.sizes || [];
  state.sizes[args.index] = args.current;
  saveLayout(state);
};
```

### Pattern 3: Lazy Load Pane Content

```tsx
const [loadedPanes, setLoadedPanes] = React.useState<Set<number>>(new Set());

const loadPaneContent = async (index: number) => {
  if (!loadedPanes.has(index)) {
    const data = await fetch(`/api/pane/${index}`);
    // Update pane content
    setLoadedPanes(new Set([...loadedPanes, index]));
  }
};

const handleExpanded = (args: any) => {
  loadPaneContent(args.index);
};
```

---

## Event Quick Reference

| Event | Fires When | Key Properties | Use Case |
|-------|-----------|-----------------|----------|
| `created` | Component initialized | element, name | Initialize content |
| `beforeCollapse` | Before pane collapse | index, cancel | Validate/prevent collapse |
| `collapsed` | After pane collapse | index | Update UI state |
| `beforeExpand` | Before pane expand | index, cancel | Validate/prevent expand |
| `expanded` | After pane expand | index | Load content |
| `resizeStart` | Drag separator starts | index, previous | Show indicators |
| `resizing` | During drag (continuous) | index, current, cancel | Real-time feedback |
| `resizeStop` | Drag separator ends | index, previous, current | Save layout |
| `beforeSanitizeHtml` | Before HTML sanitization | value | Monitor/customize sanitization |

