# Pane Layout Configuration

## Table of Contents
- [Horizontal Layout](#horizontal-layout)
- [Vertical Layout](#vertical-layout)
- [Multiple Panes](#multiple-panes)
- [Nested Splitters](#nested-splitters)
- [Dynamic Pane Addition](#dynamic-pane-addition)
- [Dynamic Pane Removal](#dynamic-pane-removal)
- [Pane Properties](#pane-properties)

## Horizontal Layout

Horizontal layout displays panes side-by-side, separated by vertical dividers.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';

function HorizontalLayout() {
  return (
    <SplitterComponent orientation='Horizontal'>
      <PanesDirective>
        <PaneDirective size='300px'>
          <div>Left Pane</div>
        </PaneDirective>
        <PaneDirective size='300px'>
          <div>Right Pane</div>
        </PaneDirective>
      </PanesDirective>
    </SplitterComponent>
  );
}

export default HorizontalLayout;
```

**Use Case:** File explorer with editor, email client with message list and preview, dashboard with sidebar and content.

### Size Options
- Pixel size: `size='200px'`
- Percentage: `size='50%'` (each pane gets equal space)
- Mixed: First pane 250px, second pane takes remaining space

## Vertical Layout

Vertical layout stacks panes top-to-bottom, separated by horizontal dividers.

```tsx
function VerticalLayout() {
  return (
    <SplitterComponent orientation='Vertical'>
      <PanesDirective>
        <PaneDirective size='200px'>
          <div>Top Pane</div>
        </PaneDirective>
        <PaneDirective size='300px'>
          <div>Bottom Pane</div>
        </PaneDirective>
      </PanesDirective>
    </SplitterComponent>
  );
}
```

**Use Case:** Code editor with code area on top and console/output at bottom, dashboard with header and content area.

## Multiple Panes

Create layouts with 3 or more panes. Total sizes should equal available space.

```tsx
function MultiplePanes() {
  return (
    <SplitterComponent orientation='Horizontal'>
      <PanesDirective>
        <PaneDirective size='20%'>
          <div style={{ padding: '15px' }}>
            <h4>Sidebar</h4>
            <ul>
              <li>Nav 1</li>
              <li>Nav 2</li>
            </ul>
          </div>
        </PaneDirective>
        
        <PaneDirective size='60%'>
          <div style={{ padding: '15px' }}>
            <h4>Main Content</h4>
            <p>Primary content area</p>
          </div>
        </PaneDirective>
        
        <PaneDirective size='20%'>
          <div style={{ padding: '15px' }}>
            <h4>Details</h4>
            <p>Side panel for details</p>
          </div>
        </PaneDirective>
      </PanesDirective>
    </SplitterComponent>
  );
}
```

**Best Practice:** Use percentages for multiple panes to ensure they fit the container.

## Nested Splitters

Combine horizontal and vertical splitters for complex layouts like IDE interfaces.

```tsx
function NestedSplitters() {
  return (
    <SplitterComponent orientation='Horizontal'>
      <PanesDirective>
        <PaneDirective size='250px'>
          <div style={{ padding: '10px' }}>
            <h4>File Explorer</h4>
            <div>file1.ts</div>
            <div>file2.ts</div>
          </div>
        </PaneDirective>
        
        {/* Vertical splitter inside horizontal */}
        <PaneDirective size='auto'>
          <SplitterComponent orientation='Vertical'>
            <PanesDirective>
              <PaneDirective size='70%'>
                <div style={{ padding: '10px' }}>
                  <h4>Code Editor</h4>
                  <p>Write code here...</p>
                </div>
              </PaneDirective>
              <PaneDirective size='30%'>
                <div style={{ padding: '10px' }}>
                  <h4>Console</h4>
                  <p>Output here...</p>
                </div>
              </PaneDirective>
            </PanesDirective>
          </SplitterComponent>
        </PaneDirective>
      </PanesDirective>
    </SplitterComponent>
  );
}
```

**IDE Layout Pattern:**
- Outer: Horizontal (Sidebar | Editor Area)
- Inner (Editor Area): Vertical (Code | Console)

## Dynamic Pane Addition

Add panes at runtime using the `addPane()` public method.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';

function DynamicPaneAddition() {
  const splitterRef = React.useRef<SplitterComponent>(null);
  const [paneCount, setPaneCount] = React.useState(2);

  const addNewPane = () => {
    const newIndex = paneCount;
    
    // Create pane object
    const paneObj = {
      size: '200px',
      content: `<div style="padding: 15px;"><h4>Pane ${newIndex + 1}</h4></div>`,
      resizable: true
    };

    // Add pane using public method
    if (splitterRef.current) {
      splitterRef.current.addPane(paneObj, newIndex);
      setPaneCount(newIndex + 1);
    }
  };

  return (
    <div>
      <button onClick={addNewPane}>Add Pane</button>
      
      <SplitterComponent 
        ref={splitterRef}
        orientation='Horizontal'
      >
        <PanesDirective>
          <PaneDirective size='200px'>
            <div style={{ padding: '15px' }}>Pane 1</div>
          </PaneDirective>
          <PaneDirective size='200px'>
            <div style={{ padding: '15px' }}>Pane 2</div>
          </PaneDirective>
        </PanesDirective>
      </SplitterComponent>
    </div>
  );
}

export default DynamicPaneAddition;
```

### addPane() Method Signature

```tsx
addPane(paneProperties, index): void
```

**Parameters:**
- `paneProperties` - Pane configuration object with properties like `size`, `content`, `resizable`
- `index` - Position to insert the pane (optional, defaults to end)

**Example: Add pane at specific index**

```tsx
const paneObj = {
  size: '150px',
  content: '<div>New Pane</div>'
};

splitterRef.current.addPane(paneObj, 1); // Insert at position 1
```

**Example: Add pane with React component content**

```tsx
const paneObj = {
  size: '250px',
  contentTemplate: () => (
    <div>
      <h3>Dynamic Content</h3>
      <button>Click Me</button>
    </div>
  )
};

splitterRef.current.addPane(paneObj);
```

## Dynamic Pane Removal

Remove panes at runtime using the `removePane()` public method.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';

function DynamicPaneRemoval() {
  const splitterRef = React.useRef<SplitterComponent>(null);

  const removePane = (index: number) => {
    if (splitterRef.current) {
      splitterRef.current.removePane(index);
    }
  };

  return (
    <div>
      <div style={{ marginBottom: '10px' }}>
        <button onClick={() => removePane(0)}>Remove Pane 1</button>
        <button onClick={() => removePane(1)}>Remove Pane 2</button>
      </div>
      
      <SplitterComponent 
        ref={splitterRef}
        orientation='Horizontal'
      >
        <PanesDirective>
          <PaneDirective size='200px'>
            <div style={{ padding: '15px' }}>Pane 1</div>
          </PaneDirective>
          <PaneDirective size='200px'>
            <div style={{ padding: '15px' }}>Pane 2</div>
          </PaneDirective>
          <PaneDirective size='200px'>
            <div style={{ padding: '15px' }}>Pane 3</div>
          </PaneDirective>
        </PanesDirective>
      </SplitterComponent>
    </div>
  );
}

export default DynamicPaneRemoval;
```

### removePane() Method Signature

```tsx
removePane(index): void
```

**Parameters:**
- `index` - The pane index/position to remove (0-based)

**Example: Remove specific pane**

```tsx
splitterRef.current.removePane(0); // Remove first pane
splitterRef.current.removePane(2); // Remove third pane
```

**Example: Conditional removal with validation**

```tsx
const removePaneIfExists = (index: number) => {
  const paneCount = splitterRef.current?.panes?.length || 0;
  
  if (index >= 0 && index < paneCount) {
    splitterRef.current?.removePane(index);
  } else {
    console.warn(`Cannot remove pane at index ${index}`);
  }
};
```

## Pane Properties

Configure individual panes with these properties:

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| `size` | string | Pane width (px or %) | `size='300px'` |
| `min` | string | Minimum size constraint | `min='100px'` |
| `max` | string | Maximum size constraint | `max='500px'` |
| `collapsed` | boolean | Initial collapsed state | `collapsed={true}` |
| `collapsible` | boolean | Allow user collapse/expand | `collapsible={true}` |
| `resizable` | boolean | Allow user to resize | `resizable={false}` |
| `content` | string/JSX | Pane content | `content='<div>Text</div>'` |

### Example: Pane with All Properties

```tsx
<PaneDirective
  size='250px'
  min='100px'
  max='500px'
  collapsed={false}
  collapsible={true}
  resizable={true}
>
  <div style={{ padding: '15px' }}>
    <h4>Configurable Pane</h4>
  </div>
</PaneDirective>
```

### Best Practices for Pane Configuration

1. **Always set size** - Use px or % consistently
2. **Set min/max for resizable panes** - Prevent usability issues
3. **Use collapsible for space-saving** - Hide secondary panels
4. **Test responsiveness** - Ensure layouts work on mobile
5. **Consider content type** - Match pane size to content (scrollable vs fixed)
