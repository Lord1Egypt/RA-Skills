# Templates and Custom Rendering

## Table of Contents

1. [Overview](#overview)
2. [Template Basics](#template-basics)
3. [String Templates](#string-templates)
4. [HTML Templates](#html-templates)
5. [JSX Function Templates](#jsx-function-templates)
6. [Stateless Templates - Performance Optimization](#stateless-templates---performance-optimization)
7. [drawNode Callback - Alternative Rendering](#drawnode-callback---alternative-rendering)
8. [Dynamic and Conditional Templates](#dynamic-and-conditional-templates)
9. [Template Best Practices](#template-best-practices)
10. [Troubleshooting](#troubleshooting)

## Overview

TreeView provides three main templating approaches:

1. **Template String** - Simple interpolation with `${...}` syntax
2. **HTML Element ID** - Reference external HTML templates
3. **JSX Function** - React components for templates
4. **Stateless Templates** - Performance optimization (prevents re-render)
5. **drawNode Callback** - Custom DOM rendering for complex scenarios

This guide covers all approaches with real-world examples.

## Template Basics

### Template Property

```tsx
<TreeViewComponent
  fields={{ dataSource, id: 'id', text: 'name', child: 'child' }}
  nodeTemplate={/* template here */}
/>
```

The `nodeTemplate` receives node data and must return content (string or JSX.Element).

### What You Get in Template Function

```tsx
const template = (data) => {
  // data properties available:
  console.log(data.id);           // Node ID
  console.log(data.text);         // Node text
  console.log(data.name);         // Any custom property from data
  console.log(data.level);        // Node depth in tree
  console.log(data.hasChildren);  // Is parent node
  // All custom properties from your data are available
};
```

## String Templates

Template strings use `${propertyName}` interpolation syntax:

```tsx
import * as React from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';
import '@syncfusion/ej2-react-navigations/styles/tree-view.css';

function App() {
  const employeeData = [
    { id: 1, name: 'Steven Buchanan', designation: 'CEO', picture: '10' },
    { id: 2, name: 'Laura Callahan', designation: 'Product Manager', picture: '2' },
    { id: 3, name: 'Andrew Fuller', designation: 'Team Lead', picture: '7' }
  ];

  // String template with interpolation
  const template = '<div><img src="url" alt="avatar" class="empimage" />' +
                   '<div class="ename">${name}</div>' +
                   '<div class="designation">${designation}</div></div>';

  return (
    <TreeViewComponent
      fields={{
        dataSource: employeeData,
        id: 'id',
        text: 'name'
      }}
      nodeTemplate={template}
    />
  );
}

export default App;
```

**Pros:** Simple, lightweight
**Cons:** No React component integration, harder to maintain complex templates

## HTML Templates

Reference external HTML templates by element ID:

```tsx
import * as React from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const fileData = [
    { id: 1, name: 'Images', type: 'folder' },
    { id: 2, name: 'photo.jpg', type: 'image' },
    { id: 3, name: 'document.pdf', type: 'document' }
  ];

  return (
    <>
      {/* HTML template - NOT rendered by React */}
      <script id="fileTemplate" type="text/x-jsrender">
        <div class="file-template">
          <span class="icon" data-type="${{type}}"></span>
          <span class="filename">${{name}}</span>
        </div>
      </script>

      <TreeViewComponent
        fields={{
          dataSource: fileData,
          id: 'id',
          text: 'name'
        }}
        nodeTemplate="fileTemplate"  {/* Pass element ID as string */}
      />
    </>
  );
}

export default App;
```

**Pros:** Separates template from component logic
**Cons:** HTML as string is not as clean, still not React components

## JSX Function Templates

Most React-friendly approach - use function that returns JSX:

```tsx
import * as React from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const data = [
    {
      id: 1,
      name: 'Projects',
      icon: 'e-icons e-folder',
      count: 3
    },
    {
      id: 2,
      name: 'Documents',
      icon: 'e-icons e-file',
      count: 5
    }
  ];

  // JSX template function
  const nodeTemplate = (props) => (
    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
      {/* Icon */}
      <span className={props.icon} style={{ fontSize: '16px' }}></span>
      
      {/* Name */}
      <span style={{ fontWeight: 500 }}>{props.name}</span>
      
      {/* Count badge */}
      {props.count && (
        <span
          style={{
            backgroundColor: '#4CAF50',
            color: 'white',
            borderRadius: '12px',
            padding: '2px 8px',
            fontSize: '12px',
            marginLeft: 'auto'
          }}
        >
          {props.count}
        </span>
      )}
    </div>
  );

  return (
    <TreeViewComponent
      fields={{
        dataSource: data,
        id: 'id',
        text: 'name'
      }}
      nodeTemplate={nodeTemplate}
    />
  );
}

export default App;
```

**Pros:** Full React component integration, easy to maintain, props-based
**Cons:** Re-renders on state changes (see statelessTemplates to optimize)

## Stateless Templates - Performance Optimization

**Problem:** Templates re-render when TreeView state updates, even if node didn't change.

**Solution:** Use `statelessTemplates` property to exclude templates from state re-renders.

### Why Stateless Templates?

```tsx
// Without statelessTemplates:
// Every node template re-renders when ANY state changes
// ❌ Performance issue with 1000+ nodes

// With statelessTemplates:
// Specified templates are rendered once, not re-rendered
// ✅ Major performance improvement
```

### Implementation

```tsx
import * as React from 'react';
import { useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const [selectedItem, setSelectedItem] = React.useState(null);
  const [counter, setCounter] = React.useState(0);

  const folderData = [
    { id: 1, name: 'Favorites', hasChild: true },
    { id: 2, pid: 1, name: 'Sales Reports', count: '4' },
    { id: 3, pid: 1, name: 'Marketing Reports', count: '6' },
    { id: 4, name: 'My Folder', hasChild: true, expanded: true },
    { id: 5, pid: 4, name: 'Inbox', selected: true, count: '20' },
    { id: 6, pid: 4, name: 'Drafts', count: '5' }
  ];

  const fields = {
    dataSource: folderData,
    id: 'id',
    parentID: 'pid',
    text: 'name',
    hasChildren: 'hasChild'
  };

  // Template that won't re-render
  const nodeTemplate = (data) => (
    <div style={{ display: 'flex', alignItems: 'center' }}>
      <span style={{ flex: 1 }}>{data.name}</span>
      {data.count && (
        <span
          style={{
            backgroundColor: '#FF9800',
            color: 'white',
            borderRadius: '12px',
            padding: '2px 8px',
            fontSize: '12px'
          }}
        >
          {data.count}
        </span>
      )}
    </div>
  );

  return (
    <div>
      <p>Counter: {counter}</p>
      <button onClick={() => setCounter(counter + 1)}>
        Increment Counter
      </button>

      <p>Selected: {selectedItem?.text}</p>

      <TreeViewComponent
        cssClass="custom"
        fields={fields}
        nodeTemplate={nodeTemplate}
        // ✅ KEY: Tell TreeView to not re-render nodeTemplate on state changes
        statelessTemplates={['nodeTemplate']}
        onNodeSelected={(args) => setSelectedItem(args.nodeData)}
      />
    </div>
  );
}

export default App;
```

### Performance Impact

Without `statelessTemplates`:
- Counter increment → TreeView state updates → ALL 1000 nodes re-render → 500ms lag

With `statelessTemplates=['nodeTemplate']`:
- Counter increment → Tree state updates → Templates NOT re-rendered → Instant response

### When to Use

- ✅ 100+ nodes in TreeView
- ✅ Template changes rarely (static content)
- ✅ Performance is critical
- ❌ DON'T use if template content depends on external state changes

## drawNode Callback - Alternative Rendering

`drawNode` callback provides maximum control via DOM manipulation. Use for:
- Custom node styling based on complex conditions
- Disabling checkboxes for specific nodes
- Adding custom attributes or classes
- Advanced DOM manipulation

### Basic drawNode Example

```tsx
import * as React from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const data = [
    { id: 1, name: 'Enabled Node', status: 'enabled' },
    { id: 2, name: 'Disabled Node', status: 'disabled' },
    { id: 3, name: 'Read-Only Node', status: 'readonly' }
  ];

  // drawNode callback - called for each node during render
  const handleDrawNode = (args) => {
    // args.node - DOM element of the tree node
    // args.nodeData - Data object of the node
    // args.level - Depth level of node

    if (args.nodeData.status === 'disabled') {
      // Disable checkbox for this node
      const checkbox = args.node.querySelector('.e-checkbox');
      if (checkbox) {
        checkbox.classList.add('e-checkbox-disabled');
        checkbox.setAttribute('disabled', 'true');
      }
      // Add disabled class to node
      args.node.classList.add('e-disabled-node');
    }

    if (args.nodeData.status === 'readonly') {
      // Add read-only styling
      args.node.classList.add('e-readonly-node');
      args.node.style.opacity = '0.6';
    }
  };

  return (
    <TreeViewComponent
      fields={{
        dataSource: data,
        id: 'id',
        text: 'name'
      }}
      showCheckBox={true}
      onDrawNode={handleDrawNode}
    />
  );
}

export default App;
```

### Disable Checkboxes for Specific Nodes

```tsx
const handleDrawNode = (args) => {
  // Disable checkbox for node with id=2
  if (args.nodeData.id === 2) {
    const checkbox = args.node.querySelector('.e-checkbox-wrapper');
    if (checkbox) {
      checkbox.classList.add('e-checkbox-disabled');
      checkbox.style.pointerEvents = 'none';
      checkbox.style.opacity = '0.5';
    }
  }
};
```

### Add Custom Icons Based on Node Type

```tsx
const handleDrawNode = (args) => {
  const iconElement = args.node.querySelector('.e-icons');
  
  if (args.nodeData.type === 'folder') {
    iconElement.className = 'e-icons e-folder';
  } else if (args.nodeData.type === 'file') {
    iconElement.className = 'e-icons e-file';
  } else if (args.nodeData.type === 'image') {
    iconElement.className = 'e-icons e-image';
  }
};
```

### Level-Wise Styling with drawNode

```tsx
const handleDrawNode = (args) => {
  const textContent = args.node.querySelector('.e-text-content');
  
  if (args.level === 0) {
    textContent.style.fontWeight = 'bold';
    textContent.style.fontSize = '16px';
  } else if (args.level === 1) {
    textContent.style.fontWeight = '600';
    textContent.style.fontSize = '14px';
  } else {
    textContent.style.fontSize = '12px';
  }
};
```

### drawNode vs nodeTemplate

| Aspect | nodeTemplate | drawNode |
|--------|-------------|----------|
| **DOM Access** | No | Yes - Full DOM control |
| **Performance** | Better | Requires statelessTemplates |
| **Use Case** | Content display | DOM manipulation, styling |
| **Complexity** | Simple | Complex |
| **Conditional Styling** | CSS classes | Direct element manipulation |

## Dynamic and Conditional Templates

### Show Different Content Based on Node Type

```tsx
const nodeTemplate = (data) => {
  // Different template based on node property
  if (data.type === 'folder') {
    return (
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <span className="e-icons e-folder"></span>
        <span style={{ fontWeight: 'bold' }}>{data.name}</span>
        <span style={{ marginLeft: 'auto', fontSize: '12px', color: '#999' }}>
          {data.fileCount} items
        </span>
      </div>
    );
  } else if (data.type === 'file') {
    return (
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <span className="e-icons e-file"></span>
        <span>{data.name}</span>
        <span style={{ marginLeft: 'auto', fontSize: '12px', color: '#999' }}>
          {data.size} KB
        </span>
      </div>
    );
  }
};
```

### Template with Click Handlers

```tsx
const nodeTemplate = (data) => (
  <div
    style={{
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center'
    }}
  >
    <span>{data.name}</span>
    <button
      onClick={(e) => {
        e.stopPropagation(); // Prevent node selection
        console.log('Edit clicked for', data.name);
      }}
      style={{ padding: '4px 8px', fontSize: '12px' }}
    >
      Edit
    </button>
  </div>
);
```

### Template with Nested Components

```tsx
const StatusBadge = ({ status }) => {
  const colors = {
    active: '#4CAF50',
    inactive: '#999',
    pending: '#FF9800'
  };
  return (
    <span
      style={{
        backgroundColor: colors[status],
        color: 'white',
        borderRadius: '4px',
        padding: '2px 6px',
        fontSize: '11px'
      }}
    >
      {status.toUpperCase()}
    </span>
  );
};

const nodeTemplate = (data) => (
  <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
    <span>{data.name}</span>
    <StatusBadge status={data.status} />
  </div>
);
```

## Template Best Practices

### 1. Keep Templates Lightweight

```tsx
// ❌ Bad - Complex computations in template
const expensiveTemplate = (data) => {
  const result = data.list.reduce((sum, item) => {
    return sum + (item.value * item.tax);
  }, 0);
  return <div>{result}</div>;
};

// ✅ Good - Pre-compute in data
const data = [
  { id: 1, name: 'Item', computedValue: 1000 }
];
const simpleTemplate = (data) => <div>{data.computedValue}</div>;
```

### 2. Use Inline Styles Sparingly

```tsx
// ❌ Bad - Inline styles for every node
const template = (data) => (
  <div style={{ color: 'blue', fontSize: '14px', fontWeight: 'bold' }}>
    {data.name}
  </div>
);

// ✅ Good - Use CSS classes
const template = (data) => (
  <div className="node-content">{data.name}</div>
);

// In CSS
.node-content { color: blue; font-size: 14px; font-weight: bold; }
```

### 3. Apply Stateless Templates to Reduce Re-renders

```tsx
// ✅ Prevent template re-renders
<TreeViewComponent
  // ... other props
  statelessTemplates={['nodeTemplate']}
/>
```

### 4. Combine Templates with Styling

```tsx
const nodeTemplate = (data) => (
  <div className={`node-level-${data.level}`}>
    {data.name}
  </div>
);

// CSS
.node-level-0 { font-weight: bold; }
.node-level-1 { font-weight: 600; }
.node-level-2 { font-weight: 400; }
```

### 5. Use drawNode for Complex DOM Manipulation

```tsx
// ✅ Use drawNode, not template, for DOM customization
const handleDrawNode = (args) => {
  // Manipulate DOM here
  args.node.classList.add('custom-styling');
};
```

## Troubleshooting

### Template Not Rendering

```tsx
// ❌ Wrong - JSX function not assigned correctly
<TreeViewComponent
  nodeTemplate={
    (data) => <div>{data.name}</div>
  }
/>

// ✅ Correct
<TreeViewComponent
  nodeTemplate={(data) => <div>{data.name}</div>}
/>
```

### Stateless Template Not Working

```tsx
// ❌ Wrong - Property name misspelled
<TreeViewComponent
  nodeTemplate={template}
  statelessTemplates={['nodeTemplates']} {/* Wrong: extra 's' */}
/>

// ✅ Correct - Exact template property name
<TreeViewComponent
  nodeTemplate={template}
  statelessTemplates={['nodeTemplate']}
/>
```

### drawNode Not Called

```tsx
// ✅ Use correct event name
<TreeViewComponent
  onDrawNode={handleDrawNode}
/>

// ❌ Wrong - Event not exposed in React
onDrawnode={...}
```

### Template Content Not Updating

```tsx
// ✅ If using external state, don't apply statelessTemplates
<TreeViewComponent
  nodeTemplate={template}
  // Don't use statelessTemplates if template depends on external state
/>

// ✅ Or update template data in TreeView
<TreeViewComponent
  nodeTemplate={template}
  statelessTemplates={['nodeTemplate']}
  fields={{ dataSource: updatedData }}  // Update dataSource instead
/>
```

---

**Key Takeaways:**
- ✅ Use `nodeTemplate` for content display
- ✅ Apply `statelessTemplates` for 100+ nodes (performance critical)
- ✅ Use `drawNode` for DOM manipulation and styling
- ✅ JSX templates are most React-friendly
- ✅ Keep templates lightweight and efficient

