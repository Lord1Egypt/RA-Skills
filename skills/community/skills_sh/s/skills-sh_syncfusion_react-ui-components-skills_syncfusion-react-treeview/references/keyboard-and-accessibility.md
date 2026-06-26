# TreeView Keyboard Navigation and Accessibility Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Keyboard Navigation Basics](#keyboard-navigation-basics)
3. [Arrow Keys Navigation](#arrow-keys-navigation)
4. [Function Keys](#function-keys)
5. [Shortcut Keys](#shortcut-keys)
6. [Complete Keyboard Shortcuts Reference](#complete-keyboard-shortcuts-reference)
7. [Inline Editing with F2](#inline-editing-with-f2)
8. [Selection with Enter and Escape](#selection-with-enter-and-escape)
9. [Multi-Selection with Modifiers](#multi-selection-with-modifiers)
10. [ARIA Attributes and Roles](#aria-attributes-and-roles)
11. [Screen Reader Support](#screen-reader-support)
12. [WCAG 2.1 AA Compliance](#wcag-21-aa-compliance)
13. [Focus Management](#focus-management)
14. [Semantic HTML Structure](#semantic-html-structure)
15. [Keyboard Event Handling](#keyboard-event-handling)
16. [Real-World Accessibility Examples](#real-world-accessibility-examples)
17. [Testing for Accessibility](#testing-for-accessibility)
18. [Troubleshooting](#troubleshooting)

---

## Introduction

The Syncfusion React TreeView component is designed with full keyboard navigation support and accessibility compliance. This guide covers all keyboard shortcuts, ARIA attributes, screen reader support, and best practices for creating accessible tree implementations.

### Key Accessibility Features
- Full keyboard navigation support
- ARIA roles and attributes
- Screen reader compatibility
- WCAG 2.1 AA compliance
- Focus management
- Semantic HTML structure
- Color-independent information display

---

## Keyboard Navigation Basics

### Enabling Keyboard Navigation

Keyboard navigation is enabled by default in the TreeView component. No special configuration is needed:

```tsx
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

function AccessibleTreeView() {
  const data = [
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' },
    { id: 3, name: 'Item 2', hasChild: true },
    { id: 4, pid: 3, name: 'Item 2.1' }
  ];

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      role="tree"
      ariaLabel="Navigation Tree"
    />
  );
}

export default AccessibleTreeView;
```

### Focus and Activation

Users can navigate using the keyboard with focus management:

```tsx
function KeyboardFocusTreeView() {
  const treeRef = useRef(null);
  const [currentNode, setCurrentNode] = useState(null);

  const handleKeyDown = (e) => {
    const treeInstance = treeRef.current.ej2_instances[0];
    console.log('Focused element:', document.activeElement);
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      keyDown={handleKeyDown}
    />
  );
}

export default KeyboardFocusTreeView;
```

---

## Arrow Keys Navigation

### Up Arrow Key (↑)

Moves focus to the previous sibling or parent node:

```tsx
function ArrowNavigation() {
  const data = [
    { id: 1, name: 'Section A', hasChild: true },
    { id: 2, pid: 1, name: 'Item A1' },
    { id: 3, pid: 1, name: 'Item A2' }, // Focus here
    { id: 4, name: 'Section B', hasChild: true }
  ];

  // Up arrow moves from Item A2 to Item A1
  // Up arrow from Item A1 moves to Section A

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      cssClass="arrow-navigation-demo"
    />
  );
}

export default ArrowNavigation;
```

### Down Arrow Key (↓)

Moves focus to the next sibling or first child of expanded node:

```tsx
function DownArrowNavigation() {
  const data = [
    { id: 1, name: 'Parent', hasChild: true }, // Focus here
    { id: 2, pid: 1, name: 'Child 1' },
    { id: 3, pid: 1, name: 'Child 2' },
    { id: 4, name: 'Next Parent' }
  ];

  // Down arrow expands parent and moves to Child 1
  // If parent collapsed, down arrow moves to Next Parent

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
    />
  );
}

export default DownArrowNavigation;
```

### Left Arrow Key (←)

Collapses parent nodes or moves to parent:

```tsx
function LeftArrowNavigation() {
  const data = [
    { id: 1, name: 'Parent', hasChild: true },
    { id: 2, pid: 1, name: 'Child 1' }, // Focus here, parent is expanded
    { id: 3, pid: 1, name: 'Child 2' }
  ];

  // Left arrow collapses parent
  // Left arrow again moves focus to parent node

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
    />
  );
}

export default LeftArrowNavigation;
```

### Right Arrow Key (→)

Expands parent nodes or moves to first child:

```tsx
function RightArrowNavigation() {
  const data = [
    { id: 1, name: 'Parent', hasChild: true }, // Focus here, collapsed
    { id: 2, pid: 1, name: 'Child 1' },
    { id: 3, pid: 1, name: 'Child 2' }
  ];

  // Right arrow expands parent
  // Right arrow again moves focus to first child

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
    />
  );
}

export default RightArrowNavigation;
```

---

## Function Keys

### Home Key

Moves focus to the first node in the tree:

```tsx
function HomeKeyNavigation() {
  const data = [
    { id: 1, name: 'First Item' },
    { id: 2, name: 'Middle Item' }, // User is here
    { id: 3, name: 'Last Item' }
  ];

  // Pressing Home moves focus to First Item

  const handleKeyDown = (e) => {
    if (e.keyCode === 36) { // Home key
      console.log('Home key pressed - moving to first node');
    }
  };

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', text: 'name' }}
      keyDown={handleKeyDown}
    />
  );
}

export default HomeKeyNavigation;
```

### End Key

Moves focus to the last node in the tree:

```tsx
function EndKeyNavigation() {
  const data = [
    { id: 1, name: 'First Item' },
    { id: 2, name: 'Middle Item' }, // User is here
    { id: 3, name: 'Last Item' }
  ];

  // Pressing End moves focus to Last Item

  const handleKeyDown = (e) => {
    if (e.keyCode === 35) { // End key
      console.log('End key pressed - moving to last node');
    }
  };

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', text: 'name' }}
      keyDown={handleKeyDown}
    />
  );
}

export default EndKeyNavigation;
```

---

## Shortcut Keys

### F2 Key: Inline Editing

Enables inline editing of the focused node:

```tsx
function F2EditingTreeView() {
  const data = [
    { id: 1, name: 'Editable Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Editable Item 1.1' }
  ];

  const handleNodeEdited = (args) => {
    console.log('Node edited:', args.newText);
  };

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      allowEditing={true}
      nodeEdited={handleNodeEdited}
      ariaLabel="Editable TreeView - Press F2 to edit"
    />
  );
}

export default F2EditingTreeView;
```

### Enter Key: Selection and Confirmation

Selects the focused node or confirms an action:

```tsx
function EnterKeySelectionTreeView() {
  const data = [
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' }
  ];

  const handleNodeSelected = (args) => {
    console.log('Node selected:', args.nodeData.name);
  };

  const handleNodeClicked = (args) => {
    // Enter key triggers click event
    if (args && args.event && args.event.key === 'Enter') {
      console.log('Enter key confirmed selection');
    }
  };

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      nodeSelected={handleNodeSelected}
      nodeClicked={handleNodeClicked}
    />
  );
}

export default EnterKeySelectionTreeView;
```

### Escape Key: Cancel Operations

Cancels inline editing or closes dialogs:

```tsx
function EscapeKeyCancelTreeView() {
  const data = [
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' }
  ];

  const handleNodeEdit = (args) => {
    console.log('Node editing started');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      console.log('Escape pressed - cancel operation');
      // Escape cancels inline editing
    }
  };

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      allowEditing={true}
      nodeEdit={handleNodeEdit}
      keyDown={handleKeyDown}
    />
  );
}

export default EscapeKeyCancelTreeView;
```

### Tab Key: Focus Navigation

Moves focus to the next interactive element:

```tsx
function TabNavigationTreeView() {
  const data = [
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' },
    { id: 3, name: 'Item 2' }
  ];

  return (
    <>
      <button>Button before TreeView</button>
      <TreeViewComponent
        fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
        tabIndex={0}
        ariaLabel="TreeView - use Tab to navigate"
      />
      <button>Button after TreeView</button>
      {/* Tab navigates: Button before → TreeView → Button after */}
    </>
  );
}

export default TabNavigationTreeView;
```

---

## Complete Keyboard Shortcuts Reference

### Keyboard Shortcuts Table

| Key | Function | Context |
|-----|----------|---------|
| ↑ (Up Arrow) | Move to previous node | Navigation |
| ↓ (Down Arrow) | Move to next node | Navigation |
| → (Right Arrow) | Expand parent or move to first child | Navigation/Expansion |
| ← (Left Arrow) | Collapse parent or move to parent | Navigation/Collapsing |
| Home | Move to first node | Navigation |
| End | Move to last node | Navigation |
| F2 | Start inline editing | Editing (if enabled) |
| Enter | Select node or confirm action | Selection |
| Escape | Cancel inline editing | Editing |
| Tab | Move to next interactive element | Focus |
| Shift+Tab | Move to previous interactive element | Focus |
| Ctrl+Click | Multi-select node | Selection |
| Shift+Click | Range select nodes | Selection |
| Space | Toggle checkbox | Selection (if checkboxes enabled) |

### Implementation Example

```tsx
function AllShortcutsTreeView() {
  const data = [
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' },
    { id: 3, name: 'Item 2', hasChild: true },
    { id: 4, pid: 3, name: 'Item 2.1' }
  ];

  const handleKeyDown = (e) => {
    const keyMap = {
      38: 'Up Arrow - Previous node',
      40: 'Down Arrow - Next node',
      39: 'Right Arrow - Expand/Move right',
      37: 'Left Arrow - Collapse/Move left',
      36: 'Home - First node',
      35: 'End - Last node',
      113: 'F2 - Edit node',
      13: 'Enter - Select node',
      27: 'Escape - Cancel',
      9: 'Tab - Next focus',
      32: 'Space - Toggle checkbox'
    };

    const action = keyMap[e.keyCode];
    if (action) {
      console.log('Keyboard action:', action);
    }
  };

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      allowEditing={true}
      allowMultiSelection={true}
      showCheckBox={true}
      keyDown={handleKeyDown}
    />
  );
}

export default AllShortcutsTreeView;
```

---

## Inline Editing with F2

### Complete F2 Editing Example

```tsx
function InlineEditingTreeView() {
  const treeRef = useRef(null);
  const [editedNodes, setEditedNodes] = useState({});

  const data = [
    { id: 1, name: 'Editable Parent', hasChild: true },
    { id: 2, pid: 1, name: 'Editable Child 1' },
    { id: 3, pid: 1, name: 'Editable Child 2' }
  ];

  const handleNodeEdit = (args) => {
    console.log('Edit started for:', args.nodeData.name);
  };

  const handleNodeEdited = (args) => {
    console.log('Node edited from', args.oldText, 'to', args.newText);
    setEditedNodes(prev => ({
      ...prev,
      [args.nodeData.id]: args.newText
    }));
  };

  const handleNodeEditKeyDown = (e) => {
    if (e.key === 'F2') {
      console.log('F2 pressed - starting edit');
    }
    if (e.key === 'Enter') {
      console.log('Enter pressed - save edit');
    }
    if (e.key === 'Escape') {
      console.log('Escape pressed - cancel edit');
    }
  };

  return (
    <>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
        allowEditing={true}
        nodeEdit={handleNodeEdit}
        nodeEdited={handleNodeEdited}
        keyDown={handleNodeEditKeyDown}
        ariaLabel="Editable TreeView - Select node and press F2 to edit"
      />
      <div className="edited-nodes">
        <h3>Recently Edited Nodes:</h3>
        <ul>
          {Object.entries(editedNodes).map(([id, name]) => (
            <li key={id}>{name}</li>
          ))}
        </ul>
      </div>
    </>
  );
}

export default InlineEditingTreeView;
```

### Validating Edit Input

```tsx
function ValidatedEditingTreeView() {
  const handleBeforeEdit = (args) => {
    // Prevent editing for certain nodes
    if (args.nodeData.id === 1) {
      args.cancel = true;
      console.log('This node cannot be edited');
    }
  };

  const handleNodeEdited = (args) => {
    // Validate edited text
    if (args.newText.trim().length === 0) {
      console.log('Text cannot be empty');
      args.cancel = true;
      return;
    }

    if (args.newText.length > 50) {
      console.log('Text too long (max 50 characters)');
      args.cancel = true;
      return;
    }

    console.log('Edit valid:', args.newText);
  };

  const data = [
    { id: 1, name: 'Protected Node', hasChild: true },
    { id: 2, pid: 1, name: 'Editable Node' }
  ];

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      allowEditing={true}
      nodeEdit={handleBeforeEdit}
      nodeEdited={handleNodeEdited}
    />
  );
}

export default ValidatedEditingTreeView;
```

---

## Selection with Enter and Escape

### Enter Key Selection Handler

```tsx
function EnterKeySelectionHandler() {
  const treeRef = useRef(null);
  const [selectedNodes, setSelectedNodes] = useState([]);

  const data = [
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' },
    { id: 3, name: 'Item 2' }
  ];

  const handleNodeClicked = (args) => {
    // Check if triggered by Enter key
    if (args && args.event && args.event.keyCode === 13) {
      setSelectedNodes([args.nodeData.id]);
      console.log('Node selected with Enter:', args.nodeData.name);
    }
  };

  const handleNodeSelected = (args) => {
    console.log('Node selected:', args.nodeData.name);
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      nodeClicked={handleNodeClicked}
      nodeSelected={handleNodeSelected}
      ariaLabel="TreeView - Press Enter to select nodes"
    />
  );
}

export default EnterKeySelectionHandler;
```

### Escape to Cancel Selection

```tsx
function EscapeKeyCancelSelection() {
  const treeRef = useRef(null);
  const [selectedNode, setSelectedNode] = useState(null);

  const data = [
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' }
  ];

  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      // Clear selection
      setSelectedNode(null);
      // Clear focus
      const treeInstance = treeRef.current?.ej2_instances?.[0];
      if (treeInstance) {
        treeInstance.element.querySelector('[tabindex="0"]')?.focus?.();
      }
      console.log('Selection cleared with Escape');
    }
  };

  const handleNodeSelected = (args) => {
    setSelectedNode(args.nodeData.id);
    console.log('Node selected:', args.nodeData.name);
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      nodeSelected={handleNodeSelected}
      keyDown={handleKeyDown}
      selectedNode={selectedNode}
      ariaLabel="TreeView - Press Escape to clear selection"
    />
  );
}

export default EscapeKeyCancelSelection;
```

---

## Multi-Selection with Modifiers

### Ctrl+Click Multi-Selection

```tsx
function CtrlClickMultiSelection() {
  const [selectedNodes, setSelectedNodes] = useState([]);

  const data = [
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' },
    { id: 3, name: 'Item 2', hasChild: true },
    { id: 4, pid: 3, name: 'Item 2.1' }
  ];

  const handleNodeClicked = (args) => {
    if (args.event.ctrlKey) {
      // Ctrl+Click: Toggle node in selection
      setSelectedNodes(prev => {
        if (prev.includes(args.nodeData.id)) {
          return prev.filter(id => id !== args.nodeData.id);
        } else {
          return [...prev, args.nodeData.id];
        }
      });
      console.log('Ctrl+Click - Toggle selection:', args.nodeData.name);
    }
  };

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      nodeClicked={handleNodeClicked}
      allowMultiSelection={true}
      ariaLabel="TreeView - Use Ctrl+Click to select multiple nodes"
    />
  );
}

export default CtrlClickMultiSelection;
```

### Shift+Click Range Selection

```tsx
function ShiftClickRangeSelection() {
  const [selectedNodes, setSelectedNodes] = useState([]);
  const [lastSelectedId, setLastSelectedId] = useState(null);

  const data = [
    { id: 1, name: 'Item 1' },
    { id: 2, name: 'Item 2' },
    { id: 3, name: 'Item 3' },
    { id: 4, name: 'Item 4' },
    { id: 5, name: 'Item 5' }
  ];

  const getAllNodesBetween = (startId, endId) => {
    // Get all node IDs between start and end
    const startIndex = data.findIndex(item => item.id === startId);
    const endIndex = data.findIndex(item => item.id === endId);
    const start = Math.min(startIndex, endIndex);
    const end = Math.max(startIndex, endIndex);
    return data.slice(start, end + 1).map(item => item.id);
  };

  const handleNodeClicked = (args) => {
    if (args.event.shiftKey && lastSelectedId) {
      // Shift+Click: Select range
      const range = getAllNodesBetween(lastSelectedId, args.nodeData.id);
      setSelectedNodes(range);
      console.log('Shift+Click - Range selection:', range);
    } else {
      // Regular click
      setSelectedNodes([args.nodeData.id]);
      setLastSelectedId(args.nodeData.id);
    }
  };

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', text: 'name' }}
      nodeClicked={handleNodeClicked}
      allowMultiSelection={true}
      ariaLabel="TreeView - Use Shift+Click for range selection"
    />
  );
}

export default ShiftClickRangeSelection;
```

### Space Bar for Checkbox Toggle

```tsx
function SpaceBarCheckboxToggle() {
  const [checkedNodes, setCheckedNodes] = useState([]);

  const data = [
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' },
    { id: 3, name: 'Item 2' }
  ];

  const handleNodeChecked = (args) => {
    console.log('Node checked:', args.nodeData.name, 'State:', args.isChecked);
    if (args.isChecked) {
      setCheckedNodes(prev => [...prev, args.nodeData.id]);
    } else {
      setCheckedNodes(prev => prev.filter(id => id !== args.nodeData.id));
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === ' ') {
      console.log('Space bar pressed - toggle checkbox');
    }
  };

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      showCheckBox={true}
      nodeChecked={handleNodeChecked}
      keyDown={handleKeyDown}
      ariaLabel="TreeView with checkboxes - Use Space to toggle"
    />
  );
}

export default SpaceBarCheckboxToggle;
```

---

## ARIA Attributes and Roles

### Essential ARIA Attributes

The TreeView component automatically includes ARIA attributes, but you can enhance them:

```tsx
function AriaEnhancedTreeView() {
  const data = [
    { id: 1, name: 'Parent 1', hasChild: true, description: 'Main category' },
    { id: 2, pid: 1, name: 'Child 1.1', description: 'Subcategory' },
    { id: 3, name: 'Parent 2', hasChild: true, description: 'Another category' }
  ];

  const nodeTemplate = (props) => (
    <div
      role="treeitem"
      aria-label={`${props.name}, ${props.description}`}
      aria-expanded={props.isExpanded}
      aria-level={props.level}
    >
      {props.name}
    </div>
  );

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      nodeTemplate={nodeTemplate}
      role="tree"
      ariaLabel="Navigation tree with categories"
      ariaDescribedBy="tree-description"
    />
  );
}

export default AriaEnhancedTreeView;
```

### ARIA Roles and Attributes Reference

| ARIA Attribute | Purpose | Example |
|---|---|---|
| `role="tree"` | Identifies as tree structure | Root container |
| `role="treeitem"` | Identifies as tree item | Individual nodes |
| `aria-expanded` | Shows if node is expanded/collapsed | `aria-expanded="true"` |
| `aria-selected` | Shows if node is selected | `aria-selected="true"` |
| `aria-checked` | Shows checkbox state | `aria-checked="true"` |
| `aria-level` | Nesting level | `aria-level="2"` |
| `aria-label` | Accessible name | `aria-label="Item name"` |
| `aria-describedby` | Description reference | `aria-describedby="desc-id"` |
| `aria-disabled` | Disables node | `aria-disabled="true"` |

### Implementing ARIA Attributes

```tsx
function FullAriaImplementation() {
  const data = [
    { id: 1, name: 'Reports', hasChild: true, disabled: false },
    { id: 2, pid: 1, name: 'Sales Report', disabled: false },
    { id: 3, pid: 1, name: 'Archived Report', disabled: true }
  ];

  const nodeTemplate = (props) => (
    <div
      role="treeitem"
      aria-label={props.name}
      aria-level={props.level}
      aria-expanded={props.isExpanded}
      aria-selected={props.isSelected}
      aria-disabled={props.disabled}
      aria-describedby={`desc-${props.id}`}
    >
      <span id={`desc-${props.id}`} style={{ display: 'none' }}>
        {props.disabled ? 'This item is disabled' : `Item at level ${props.level}`}
      </span>
      {props.name}
    </div>
  );

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      nodeTemplate={nodeTemplate}
      role="tree"
      ariaLabel="Reports and documents tree"
      ariaLiveRegion="assertive"
    />
  );
}

export default FullAriaImplementation;
```

---

## Screen Reader Support

### Announcing Node Selection

```tsx
function ScreenReaderAnnouncements() {
  const [announcement, setAnnouncement] = useState('');
  const [selectedNode, setSelectedNode] = useState(null);

  const data = [
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' },
    { id: 3, name: 'Item 2' }
  ];

  const handleNodeSelected = (args) => {
    const message = `${args.nodeData.name} selected, level ${args.nodeData.level}, ${args.nodeData.hasChild ? 'has children' : 'no children'}`;
    setAnnouncement(message);
    setSelectedNode(args.nodeData.id);
  };

  const handleNodeExpanded = (args) => {
    const message = `${args.nodeData.name} expanded, showing ${args.childNodes?.length || 0} children`;
    setAnnouncement(message);
  };

  return (
    <>
      <div
        role="status"
        aria-live="polite"
        aria-atomic="true"
        className="sr-only"
      >
        {announcement}
      </div>
      <TreeViewComponent
        fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
        nodeSelected={handleNodeSelected}
        nodeExpanded={handleNodeExpanded}
        role="tree"
        ariaLabel="Screen-reader supported tree"
      />
    </>
  );
}

export default ScreenReaderAnnouncements;
```

### Live Region for Updates

```tsx
function LiveRegionUpdates() {
  const [liveAnnouncement, setLiveAnnouncement] = useState('');

  const data = [
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' },
    { id: 3, name: 'Item 2' }
  ];

  const handleNodeChecked = (args) => {
    const status = args.isChecked ? 'checked' : 'unchecked';
    setLiveAnnouncement(`${args.nodeData.name} ${status}`);
  };

  return (
    <>
      <div
        role="log"
        aria-live="polite"
        aria-atomic="true"
        className="announcement-area"
      >
        {liveAnnouncement}
      </div>
      <TreeViewComponent
        fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
        showCheckBox={true}
        nodeChecked={handleNodeChecked}
      />
    </>
  );
}

export default LiveRegionUpdates;
```

---

## WCAG 2.1 AA Compliance

### Color Contrast Requirements

```tsx
function ContrastCompliantTreeView() {
  const data = [
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' }
  ];

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      cssClass="wcag-compliant"
    />
  );
}

export default ContrastCompliantTreeView;
```

```css
/* WCAG AA Compliance: 4.5:1 contrast ratio for text */
.wcag-compliant .e-treeview {
  background-color: #ffffff; /* White */
  color: #212121; /* Very dark gray - 19.56:1 contrast */
}

.wcag-compliant .e-list-item:hover {
  background-color: #f5f5f5;
  color: #000000; /* Black - 21:1 contrast */
}

.wcag-compliant .e-list-item.e-active {
  background-color: #1976d2; /* Blue */
  color: #ffffff; /* White - 8.59:1 contrast */
}

/* Icon contrast */
.wcag-compliant .e-icons {
  color: #1976d2; /* Sufficient contrast on white background */
}

/* Focus indicator - must be visible */
.wcag-compliant .e-node-focus {
  outline: 3px solid #1976d2;
  outline-offset: 2px;
}

/* No color-only information */
.wcag-compliant .e-list-item.error-state {
  border-left: 4px solid #d32f2f; /* Icon AND color */
}

.wcag-compliant .e-list-item.success-state {
  border-left: 4px solid #388e3c; /* Icon AND color */
}
```

### Testing WCAG Compliance

```tsx
function WCAGTestTreeView() {
  // Test data includes various states
  const data = [
    { id: 1, name: 'Standard Item', hasChild: true },
    { id: 2, pid: 1, name: 'Selected Item', isSelected: true },
    { id: 3, name: 'Disabled Item', disabled: true },
    { id: 4, name: 'Item with Long Text: This is a very long item name that should wrap properly without overflow' }
  ];

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      cssClass="wcag-test"
      role="tree"
      ariaLabel="WCAG compliance test tree"
    />
  );
}

export default WCAGTestTreeView;
```

---

## Focus Management

### Focus Indicators

```tsx
function FocusIndicatorsTreeView() {
  const treeRef = useRef(null);
  const [focusedNode, setFocusedNode] = useState(null);

  const data = [
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' },
    { id: 3, name: 'Item 2' }
  ];

  const handleFocus = (e) => {
    const nodeId = e.target.closest('[data-node-id]')?.dataset.nodeId;
    if (nodeId) {
      setFocusedNode(nodeId);
      console.log('Focus on node:', nodeId);
    }
  };

  const handleBlur = () => {
    setFocusedNode(null);
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      onFocus={handleFocus}
      onBlur={handleBlur}
      cssClass={focusedNode ? 'focus-visible' : ''}
    />
  );
}

export default FocusIndicatorsTreeView;
```

```css
/* Visible focus indicator */
.e-treeview .e-node-focus {
  outline: 3px solid #4527a0;
  outline-offset: -3px;
  border-radius: 2px;
}

/* Alternative focus style for high contrast mode */
@media (prefers-contrast: more) {
  .e-treeview .e-node-focus {
    outline: 4px solid #000000;
    outline-offset: -4px;
  }
}

/* Focus-visible only when keyboard navigating */
.e-treeview .e-list-item:focus-visible {
  outline: 3px solid #1976d2;
}

/* Remove outline on mouse focus */
.e-treeview .e-list-item:focus:not(:focus-visible) {
  outline: none;
}
```

### Focus Restoration

```tsx
function FocusRestorationTreeView() {
  const treeRef = useRef(null);
  const lastFocusedNodeRef = useRef(null);

  const data = [
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' },
    { id: 3, name: 'Item 2' }
  ];

  const saveFocus = () => {
    lastFocusedNodeRef.current = document.activeElement;
  };

  const restoreFocus = () => {
    if (lastFocusedNodeRef.current?.offsetParent !== null) {
      lastFocusedNodeRef.current?.focus();
    } else {
      treeRef.current?.focus();
    }
  };

  return (
    <>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
        onFocus={saveFocus}
      />
      <button onClick={restoreFocus}>Restore Focus</button>
    </>
  );
}

export default FocusRestorationTreeView;
```

---

## Semantic HTML Structure

### Semantic Markup

```tsx
function SemanticTreeView() {
  const data = [
    { id: 1, name: 'Documentation', hasChild: true, type: 'folder' },
    { id: 2, pid: 1, name: 'Getting Started', type: 'document' },
    { id: 3, name: 'Examples', hasChild: true, type: 'folder' }
  ];

  return (
    <nav aria-label="Main navigation">
      <TreeViewComponent
        fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
        role="tree"
        ariaLabel="Main navigation tree"
      />
    </nav>
  );
}

export default SemanticTreeView;
```

### Proper Nesting Structure

```tsx
function ProperNestingTreeView() {
  const data = [
    { id: 1, name: 'Level 1', hasChild: true },
    { id: 2, pid: 1, name: 'Level 2', hasChild: true },
    { id: 3, pid: 2, name: 'Level 3' }
  ];

  // TreeView automatically creates proper nesting:
  // <div role="tree">
  //   <div role="treeitem">Level 1
  //     <div role="group">
  //       <div role="treeitem">Level 2
  //         <div role="group">
  //           <div role="treeitem">Level 3</div>
  //         </div>
  //       </div>
  //     </div>
  //   </div>
  // </div>

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
    />
  );
}

export default ProperNestingTreeView;
```

---

## Keyboard Event Handling

### Complete KeyDown Handler

```tsx
function KeyDownHandlerTreeView() {
  const treeRef = useRef(null);

  const data = [
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' },
    { id: 3, name: 'Item 2' }
  ];

  const handleKeyDown = (e) => {
    const keyCode = e.keyCode;
    const keyName = e.key;

    const keyActions = {
      38: () => console.log('↑ Up - Move to previous node'),
      40: () => console.log('↓ Down - Move to next node'),
      37: () => console.log('← Left - Collapse or move to parent'),
      39: () => console.log('→ Right - Expand or move to child'),
      36: () => console.log('Home - Move to first node'),
      35: () => console.log('End - Move to last node'),
      113: () => console.log('F2 - Edit node'),
      13: () => console.log('Enter - Select/Confirm'),
      27: () => console.log('Escape - Cancel'),
      9: () => console.log('Tab - Move to next interactive element'),
      32: () => console.log('Space - Toggle checkbox')
    };

    if (keyActions[keyCode]) {
      keyActions[keyCode]();
    }

    // Prevent default for arrow keys to ensure TreeView navigation
    if ([37, 38, 39, 40].includes(keyCode)) {
      e.preventDefault();
    }
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      keyDown={handleKeyDown}
      ariaLabel="KeyDown handler test tree"
    />
  );
}

export default KeyDownHandlerTreeView;
```

---

## Real-World Accessibility Examples

### Accessible File Manager

```tsx
function AccessibleFileManagerTree() {
  const data = [
    { id: 1, name: 'Downloads', hasChild: true, type: 'folder', icon: 'folder' },
    { id: 2, pid: 1, name: 'Document.pdf', type: 'file', icon: 'pdf' },
    { id: 3, name: 'Documents', hasChild: true, type: 'folder', icon: 'folder' },
    { id: 4, pid: 3, name: 'Report.docx', type: 'file', icon: 'doc' }
  ];

  const [selectedFile, setSelectedFile] = useState(null);

  const nodeTemplate = (props) => (
    <div
      role="treeitem"
      aria-label={`${props.name}, ${props.type}`}
      data-node-id={props.id}
    >
      <i className={`icon-${props.icon}`}></i>
      <span>{props.name}</span>
    </div>
  );

  const handleNodeSelected = (args) => {
    setSelectedFile(args.nodeData.id);
  };

  return (
    <aside aria-label="File manager">
      <TreeViewComponent
        fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
        nodeTemplate={nodeTemplate}
        nodeSelected={handleNodeSelected}
        role="tree"
        ariaLabel="Accessible file manager tree"
      />
    </aside>
  );
}

export default AccessibleFileManagerTree;
```

---

## Testing for Accessibility

### Automated Testing with AXIO

```tsx
import axe from 'axe-core';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

function AccessibilityTestTreeView() {
  const treeRef = useRef(null);

  const data = [
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' }
  ];

  const runAccessibilityTest = async () => {
    if (treeRef.current) {
      const results = await axe.run(treeRef.current);
      console.log('Accessibility test results:', results);
      if (results.violations.length > 0) {
        console.error('Accessibility violations found:', results.violations);
      } else {
        console.log('No accessibility violations found');
      }
    }
  };

  return (
    <>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      />
      <button onClick={runAccessibilityTest}>Run A11y Test</button>
    </>
  );
}

export default AccessibilityTestTreeView;
```

### Manual Testing Checklist

```
Keyboard Navigation:
☐ Arrow keys navigate correctly
☐ Home/End keys jump to first/last
☐ F2 activates edit mode
☐ Enter confirms selection
☐ Escape cancels operations
☐ Tab moves focus through elements

ARIA:
☐ role="tree" on root
☐ role="treeitem" on items
☐ aria-expanded shows state
☐ aria-selected on active nodes
☐ aria-label on items

Screen Reader:
☐ TreeView structure announced correctly
☐ Node names announced
☐ Selected/expanded states announced
☐ Live regions working

Visual:
☐ Focus indicator visible (3px)
☐ Color contrast 4.5:1 minimum
☐ No color-only information
☐ Text resizable to 200%
```

---

## Troubleshooting

### Keyboard Not Working

```tsx
// Problem: Keyboard navigation not working
function TroubleshootKeyboard() {
  const treeRef = useRef(null);

  // Solution: Ensure TreeView is focused
  const focusTreeView = () => {
    treeRef.current?.focus();
  };

  return (
    <>
      <button onClick={focusTreeView}>Focus TreeView</button>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
        tabIndex={0}
      />
    </>
  );
}

export default TroubleshootKeyboard;
```

### ARIA Not Applied

```tsx
// Problem: ARIA attributes not showing
// Solution: Verify component renders correctly

const CheckAriaAttributes = () => {
  const treeRef = useRef(null);

  useEffect(() => {
    const tree = treeRef.current;
    const items = tree?.querySelectorAll('[role="treeitem"]');
    console.log('ARIA attributes on items:', items?.length);
    items?.forEach(item => {
      console.log('aria-expanded:', item.getAttribute('aria-expanded'));
      console.log('aria-level:', item.getAttribute('aria-level'));
    });
  }, []);

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
    />
  );
};
```

### Screen Reader Not Announcing

```tsx
// Problem: Screen reader not announcing changes
// Solution: Use aria-live regions

function AnnounceChanges() {
  const [announcement, setAnnouncement] = useState('');

  const handleNodeSelected = (args) => {
    setAnnouncement(`Selected: ${args.nodeData.name}`);
  };

  return (
    <>
      <div role="status" aria-live="polite" aria-atomic="true">
        {announcement}
      </div>
      <TreeViewComponent
        fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
        nodeSelected={handleNodeSelected}
      />
    </>
  );
}

export default AnnounceChanges;
```
