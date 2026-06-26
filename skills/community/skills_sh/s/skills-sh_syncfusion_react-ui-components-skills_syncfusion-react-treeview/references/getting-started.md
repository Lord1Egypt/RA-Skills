# Getting Started with React TreeView

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Basic Component Setup](#basic-component-setup)
4. [Understanding Data Structure](#understanding-data-structure)
5. [CSS Import and Theming](#css-import-and-theming)
6. [First Interactive TreeView](#first-interactive-treeview)
7. [Enable Ripple Effects](#enable-ripple-effects)
8. [Troubleshooting](#troubleshooting)
9. [Next Steps](#next-steps)

## Overview

The TreeView component displays hierarchical data in a tree structure. Use it to show nested categories, file systems, organization charts, navigation menus, or any multi-level data.

This guide covers:
- Installation of Syncfusion packages
- Component initialization
- Setting up your first TreeView
- Basic configuration options
- Theme selection

## Installation

### Step 1: Install Required Packages

```bash
npm install @syncfusion/ej2-react-navigations --save
```

This package includes TreeViewComponent and related dependencies:
- `@syncfusion/ej2-base` - Core utilities
- `@syncfusion/ej2-data` - Data management
- `@syncfusion/ej2-react-base` - React wrapper
- `@syncfusion/ej2-lists` - List utilities

### Step 2: Install Additional Syncfusion Packages (Optional)

For advanced features:

```bash
# For context menu integration
npm install @syncfusion/ej2-react-popups --save

# For data binding with DataManager
npm install @syncfusion/ej2-data --save

# For styling and theming
npm install @syncfusion/ej2-react-base --save
```

## Basic Component Setup

### Minimal TreeView

```tsx
import * as React from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';
import '@syncfusion/ej2-react-navigations/styles/tree-view.css';

function App() {
  const data = [
    { id: 1, name: 'Item 1' },
    { id: 2, name: 'Item 2' },
    { id: 3, name: 'Item 3' }
  ];

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', text: 'name' }}
    />
  );
}

export default App;
```

This renders three items with no nesting. 

### Required Props

| Prop | Type | Description |
|------|------|-------------|
| `fields` | FieldsSettings | Maps data to TreeView structure |
| `fields.dataSource` | any[] | Array of data items |
| `fields.id` | string | Property name for unique ID |
| `fields.text` | string | Property name for display text |

## Understanding Data Structure

### Hierarchical Data (Nested Arrays)

Most common approach - data naturally nested:

```tsx
const hierarchicalData = [
  {
    id: 1,
    name: 'Syncfusion',
    expanded: true,
    child: [
      { id: 2, name: 'React Components' },
      { id: 3, name: 'Angular Components' },
      { id: 4, name: 'Vue Components' }
    ]
  },
  {
    id: 5,
    name: 'Essential Studio',
    child: [
      { id: 6, name: 'Web (EJ2)' },
      { id: 7, name: 'Desktop' }
    ]
  }
];

// TreeView configuration
<TreeViewComponent
  fields={{
    dataSource: hierarchicalData,
    id: 'id',
    text: 'name',
    child: 'child',       // Property containing children
    expanded: 'expanded'  // Property for initial expansion state
  }}
/>
```

### Self-Referential Data (Flat Arrays with parentID)

Flat array with parent-child relationship via IDs:

```tsx
const selfRefData = [
  { id: 1, pid: null, name: 'Syncfusion', hasChild: true },
  { id: 2, pid: 1, name: 'React Components' },
  { id: 3, pid: 1, name: 'Angular Components' },
  { id: 4, pid: 1, name: 'Vue Components' },
  { id: 5, pid: null, name: 'Essential Studio', hasChild: true },
  { id: 6, pid: 5, name: 'Web' },
  { id: 7, pid: 5, name: 'Desktop' }
];

// TreeView configuration
<TreeViewComponent
  fields={{
    dataSource: selfRefData,
    id: 'id',
    parentID: 'pid',        // Parent ID reference
    text: 'name',
    hasChildren: 'hasChild' // Flag for leaf detection
  }}
/>
```

Use self-referential when:
- Data comes from a database query
- You're using load-on-demand (fetch children on expand)
- You need flat data structure

## CSS Import and Theming

### Import Base CSS

```tsx
import '@syncfusion/ej2-react-navigations/styles/tree-view.css';
```

### Choose a Theme

Syncfusion provides multiple themes:

```tsx
// Material Design (Default, recommended)
import '@syncfusion/ej2-react-navigations/styles/material.css';

// Bootstrap
import '@syncfusion/ej2-react-navigations/styles/bootstrap.css';

// Bootstrap 4
import '@syncfusion/ej2-react-navigations/styles/bootstrap4.css';

// Fabric
import '@syncfusion/ej2-react-navigations/styles/fabric.css';

// High Contrast
import '@syncfusion/ej2-react-navigations/styles/highcontrast.css';
```

### Complete Import Example

```tsx
import * as React from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

// Base CSS
import '@syncfusion/ej2-react-navigations/styles/tree-view.css';
// Theme
import '@syncfusion/ej2-react-navigations/styles/material.css';

function App() {
  // Component code here
}

export default App;
```

## First Interactive TreeView

### Basic Hierarchical Example with Events

```tsx
import * as React from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';
import '@syncfusion/ej2-react-navigations/styles/tree-view.css';
import '@syncfusion/ej2-react-navigations/styles/material.css';

function App() {
  const [selectedNode, setSelectedNode] = React.useState(null);

  const employeeData = [
    {
      id: 1,
      name: 'CEO',
      expanded: true,
      child: [
        {
          id: 2,
          name: 'Manager - HR',
          child: [
            { id: 3, name: 'HR Executive' },
            { id: 4, name: 'Recruiter' }
          ]
        },
        {
          id: 5,
          name: 'Manager - IT',
          child: [
            { id: 6, name: 'Lead Developer' },
            { id: 7, name: 'QA Engineer' }
          ]
        }
      ]
    }
  ];

  const handleNodeSelected = (args) => {
    console.log('Selected Node:', args.nodeData);
    setSelectedNode(args.nodeData.name);
  };

  const handleNodeExpanded = (args) => {
    console.log('Expanded Node:', args.nodeData.name);
  };

  return (
    <div>
      <h2>Organization Chart</h2>
      <TreeViewComponent
        fields={{
          dataSource: employeeData,
          id: 'id',
          text: 'name',
          child: 'child',
          expanded: 'expanded'
        }}
        onNodeSelected={handleNodeSelected}
        onNodeExpanded={handleNodeExpanded}
      />
      <p>Selected: {selectedNode}</p>
    </div>
  );
}

export default App;
```

### With Checkboxes

```tsx
<TreeViewComponent
  fields={{
    dataSource: employeeData,
    id: 'id',
    text: 'name',
    child: 'child'
  }}
  showCheckBox={true}
  autoCheck={true}
  onNodeChecked={(args) => {
    console.log('Checked:', args.nodeData.name);
  }}
/>
```

### With Drag-Drop

```tsx
<TreeViewComponent
  fields={{
    dataSource: employeeData,
    id: 'id',
    text: 'name',
    child: 'child'
  }}
  allowDragAndDrop={true}
  onNodeDropped={(args) => {
    console.log('Dropped:', args.draggedNode, 'onto', args.droppedNode);
  }}
/>
```

### With Editing

```tsx
<TreeViewComponent
  fields={{
    dataSource: employeeData,
    id: 'id',
    text: 'name',
    child: 'child'
  }}
  allowEditing={true}
  onNodeEdited={(args) => {
    console.log('Edited text:', args.newText);
  }}
/>
```

## Enable Ripple Effects

Ripple effects provide visual feedback on interactions (Material Design):

```tsx
import { enableRipple } from '@syncfusion/ej2-base';

enableRipple(true);

export default function App() {
  // Your component
}
```

Or enable per-instance:

```tsx
<TreeViewComponent
  fields={{ dataSource, id: 'id', text: 'name' }}
  ripple={true}  // Material theme ripple
/>
```

## Troubleshooting

### Issue: Component Not Rendering

**Solution:** Verify CSS import

```tsx
// ✅ Correct - Both imports needed
import '@syncfusion/ej2-react-navigations/styles/tree-view.css';
import '@syncfusion/ej2-react-navigations/styles/material.css';

// ❌ Wrong - Missing theme CSS
import '@syncfusion/ej2-react-navigations/styles/tree-view.css';
```

### Issue: Data Not Displaying

**Solution:** Check fields mapping

```tsx
// ✅ Correct - fields matches data properties
const data = [{ id: 1, name: 'Item', child: [{ id: 2, name: 'Child' }] }];
<TreeViewComponent
  fields={{
    dataSource: data,
    id: 'id',        // Matches data property 'id'
    text: 'name',    // Matches data property 'name'
    child: 'child'   // Matches data property 'child'
  }}
/>

// ❌ Wrong - Field names don't match
<TreeViewComponent
  fields={{
    dataSource: data,
    id: 'ID',        // Data has 'id' not 'ID'
    text: 'label',   // Data has 'name' not 'label'
    child: 'children' // Data has 'child' not 'children'
  }}
/>
```

### Issue: Styles Not Applied

**Solution:** Import CSS in correct order

```tsx
// ✅ Correct order
import '@syncfusion/ej2-react-navigations/styles/tree-view.css';
import '@syncfusion/ej2-react-navigations/styles/material.css';
// Your custom CSS
import './App.css';

// ❌ Wrong - Custom CSS before theme
import './App.css';
import '@syncfusion/ej2-react-navigations/styles/material.css';
```

### Issue: Events Not Firing

**Solution:** Use correct event prop names

```tsx
// ✅ Correct - React event naming convention (on + event name)
<TreeViewComponent
  onNodeSelected={handleSelect}    // ✅ onNodeSelected
  onNodeExpanded={handleExpand}    // ✅ onNodeExpanded
  onNodeDropped={handleDrop}       // ✅ onNodeDropped
/>

// ❌ Wrong - Trying to use EJ2 event names
<TreeViewComponent
  nodeSelected={handleSelect}      // ❌ Wrong - should be onNodeSelected
  nodeExpanded={handleExpand}      // ❌ Wrong
/>
```

## Next Steps

1. **Learn Data Binding** → [Data Binding Guide](data-binding.md) - Explore all 5 binding patterns
2. **Add Selection** → [Selection and Checking](selection-and-checking.md) - Single/multi-select, checkboxes
3. **Enable Editing** → [Inline Editing](inline-editing.md) - Let users edit node text
4. **Add Templates** → [Templates and Rendering](templates-and-rendering.md) - Custom node appearance with statelessTemplates
5. **Master Drag-Drop** → [Drag-Drop and Reordering](drag-drop-and-reordering.md) - Node reordering

---

**Key Takeaways:**
- ✅ Install `@syncfusion/ej2-react-navigations`
- ✅ Import both tree-view.css and theme CSS
- ✅ Set up `fields` prop to map data correctly
- ✅ Use hierarchical or self-referential data as appropriate
- ✅ React event names: `on` + event name (e.g., `onNodeSelected`)

