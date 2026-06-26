# Splitter Methods Reference

## Table of Contents
- [addPane()](#addpane)
- [removePane()](#removepane)
- [collapse()](#collapse)
- [expand()](#expand)
- [destroy()](#destroy)
- [Method Patterns](#method-patterns)

## addPane()

**Signature:** `addPane(paneProperties: PanePropertiesModel, index?: number): void`

**Description:** Dynamically adds a new pane to the Splitter at the specified index position.

**Parameters:**
- `paneProperties` (PanePropertiesModel): Configuration object for the new pane
- `index` (number, optional): Position where the pane should be inserted (0-based). If not specified, pane is added at the end

**Returns:** void

**Example - Add Pane with Full Configuration:**

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import { PanePropertiesModel } from '@syncfusion/ej2-react-layouts';
import * as React from "react";

function App() {
  let splitterInstance: any;

  const paneDetails: PanePropertiesModel = {
    content: 'New Pane',
    max: '250px',
    min: '30px',
    size: '150px',
    collapsible: true,
    resizable: true
  };

  const addPane = () => {
    if (splitterInstance) {
      splitterInstance.addPane(paneDetails, 1);
    }
  };

  return (
    <>
      <button onClick={addPane}>Add Pane</button>
      <SplitterComponent
        ref={(splitter) => (splitterInstance = splitter)}
        height="250px"
        width="600px"
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
    </>
  );
}

export default App;
```

**When to Use:**
- Creating dynamic layouts where panes are added at runtime
- Building collapsible panel systems
- Implementing tabbed interfaces with pane switching
- Responsive designs that add/remove panels based on screen size

**Best Practices:**
- Always use `ref` to access the Splitter instance
- Provide complete `PanePropertiesModel` configuration
- Verify pane index is within bounds (0 to total panes)
- Trigger UI updates after adding panes

---

## removePane()

**Signature:** `removePane(index: number): void`

**Description:** Removes a pane from the Splitter at the specified index.

**Parameters:**
- `index` (number): Zero-based index of the pane to remove

**Returns:** void

**Example - Remove Specific Pane:**

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from "react";

function App() {
  let splitterInstance: any;

  const removePane = (paneIndex: number) => {
    if (splitterInstance && paneIndex >= 0 && paneIndex < 3) {
      splitterInstance.removePane(paneIndex);
    }
  };

  return (
    <>
      <button onClick={() => removePane(1)}>Remove Middle Pane</button>
      <SplitterComponent
        ref={(splitter) => (splitterInstance = splitter)}
        height="250px"
        width="600px"
      >
        <PanesDirective>
          <PaneDirective size='150px'>
            <div>Pane 1</div>
          </PaneDirective>
          <PaneDirective size='150px'>
            <div>Pane 2 (removable)</div>
          </PaneDirective>
          <PaneDirective size='150px'>
            <div>Pane 3</div>
          </PaneDirective>
        </PanesDirective>
      </SplitterComponent>
    </>
  );
}

export default App;
```

**When to Use:**
- Removing panes when tabs are closed
- Cleaning up dynamic layouts
- Responding to user preferences
- Resetting layout to default configuration

**Best Practices:**
- Always validate the index before removing
- Ensure at least one pane remains in the Splitter
- Recalculate remaining pane sizes if needed
- Provide visual feedback when pane is removed

---

## collapse()

**Signature:** `collapse(index: number): void`

**Description:** Programmatically collapses a pane at the specified index. The pane becomes hidden and its space is redistributed to adjacent panes.

**Parameters:**
- `index` (number): Zero-based index of the pane to collapse

**Returns:** void

**Prerequisite:** The pane must have `collapsible={true}` set

**Example - Programmatically Collapse Pane:**

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from "react";

function App() {
  let splitterInstance: any;

  const collapseSidebar = () => {
    if (splitterInstance) {
      splitterInstance.collapse(0);
    }
  };

  return (
    <>
      <button onClick={collapseSidebar}>Hide Sidebar</button>
      <SplitterComponent
        ref={(splitter) => (splitterInstance = splitter)}
        height="400px"
        width="100%"
      >
        <PanesDirective>
          <PaneDirective size='250px' collapsible={true}>
            <div>Navigation Sidebar</div>
          </PaneDirective>
          <PaneDirective size='auto'>
            <div>Main Content Area</div>
          </PaneDirective>
        </PanesDirective>
      </SplitterComponent>
    </>
  );
}

export default App;
```

**When to Use:**
- Creating toggle buttons for sidebar visibility
- Implementing responsive layouts
- Saving screen space for focus areas
- Programmatic control of pane visibility

**Best Practices:**
- Only collapse panes with `collapsible={true}`
- Provide UI feedback that pane is collapsed
- Keep at least one pane visible
- Consider using with `expand()` for toggle functionality

---

## expand()

**Signature:** `expand(index: number): void`

**Description:** Programmatically expands a collapsed pane at the specified index, making it visible again.

**Parameters:**
- `index` (number): Zero-based index of the pane to expand

**Returns:** void

**Example - Programmatically Expand Pane:**

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from "react";

function App() {
  let splitterInstance: any;
  const [collapsed, setCollapsed] = React.useState(false);

  const toggleSidebar = () => {
    if (splitterInstance) {
      if (collapsed) {
        splitterInstance.expand(0);
        setCollapsed(false);
      } else {
        splitterInstance.collapse(0);
        setCollapsed(true);
      }
    }
  };

  return (
    <>
      <button onClick={toggleSidebar}>
        {collapsed ? 'Show' : 'Hide'} Sidebar
      </button>
      <SplitterComponent
        ref={(splitter) => (splitterInstance = splitter)}
        height="400px"
        width="100%"
      >
        <PanesDirective>
          <PaneDirective size='250px' collapsible={true}>
            <div>Navigation Sidebar</div>
          </PaneDirective>
          <PaneDirective size='auto'>
            <div>Main Content Area</div>
          </PaneDirective>
        </PanesDirective>
      </SplitterComponent>
    </>
  );
}

export default App;
```

**When to Use:**
- Restoring hidden panes on demand
- Implementing toggle buttons
- Responding to user preferences
- Programmatic control of pane visibility

**Best Practices:**
- Use with `collapse()` for toggle functionality
- Track collapsed state in React state
- Provide clear visual indicators of pane state
- Combine with CSS transitions for smooth animations

---

## destroy()

**Signature:** `destroy(): void`

**Description:** Destroys the Splitter component and releases all its resources. Should be called during component cleanup.

**Parameters:** None

**Returns:** void

**Example - Destroy on Unmount:**

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from "react";

function App() {
  let splitterInstance: any;

  React.useEffect(() => {
    return () => {
      // Cleanup: destroy splitter when component unmounts
      if (splitterInstance) {
        splitterInstance.destroy();
      }
    };
  }, []);

  return (
    <SplitterComponent
      ref={(splitter) => (splitterInstance = splitter)}
      height="250px"
      width="600px"
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
- Component unmounting and cleanup
- Preventing memory leaks
- Closing modal dialogs with Splitters
- Conditional rendering scenarios

**Best Practices:**
- Always call in `useEffect` cleanup function
- Null-check the instance before destroying
- Release any event listeners before destroying
- Consider framework-specific cleanup patterns

---

## Method Patterns

### Pattern 1: Add/Remove Dynamic Panes

```tsx
const [paneCount, setPaneCount] = React.useState(2);

const handleAddPane = () => {
  if (splitterInstance) {
    const newPane: PanePropertiesModel = {
      size: '150px',
      min: '100px',
      max: '300px',
      content: `Pane ${paneCount + 1}`
    };
    splitterInstance.addPane(newPane);
    setPaneCount(paneCount + 1);
  }
};

const handleRemovePane = () => {
  if (splitterInstance && paneCount > 1) {
    splitterInstance.removePane(paneCount - 1);
    setPaneCount(paneCount - 1);
  }
};

return (
  <>
    <button onClick={handleAddPane}>Add Pane</button>
    <button onClick={handleRemovePane}>Remove Pane</button>
  </>
);
```

### Pattern 2: Toggle Collapse/Expand

```tsx
const [expanded, setExpanded] = React.useState({
  0: true,
  1: true,
  2: true
});

const togglePane = (index: number) => {
  if (splitterInstance) {
    if (expanded[index]) {
      splitterInstance.collapse(index);
    } else {
      splitterInstance.expand(index);
    }
    setExpanded({
      ...expanded,
      [index]: !expanded[index]
    });
  }
};

return (
  <>
    <button onClick={() => togglePane(0)}>
      {expanded[0] ? 'Collapse' : 'Expand'} Pane 1
    </button>
  </>
);
```

### Pattern 3: Responsive Pane Management

```tsx
React.useEffect(() => {
  const handleResize = () => {
    if (window.innerWidth < 768) {
      // Collapse sidebar on small screens
      if (splitterInstance && expanded[0]) {
        splitterInstance.collapse(0);
        setExpanded({ ...expanded, 0: false });
      }
    }
  };

  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
}, [expanded]);
```

---

## Method Quick Reference

| Method | Parameters | Use Case |
|--------|-----------|----------|
| `addPane()` | PanePropertiesModel, index? | Add panes dynamically |
| `removePane()` | index | Remove panes dynamically |
| `collapse()` | index | Hide pane programmatically |
| `expand()` | index | Show collapsed pane |
| `destroy()` | none | Cleanup on unmount |

