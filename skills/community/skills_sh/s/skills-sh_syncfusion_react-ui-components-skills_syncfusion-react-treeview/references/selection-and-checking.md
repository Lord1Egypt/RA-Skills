# Selection and Checking in Syncfusion React TreeView

## Table of Contents
1. [Overview](#overview)
2. [Single vs Multi-Selection Modes](#single-vs-multi-selection-modes)
3. [Checkbox Functionality](#checkbox-functionality)
4. [Three-State Checkbox System](#three-state-checkbox-system)
5. [Parent-Child Checkbox Auto-Sync](#parent-child-checkbox-auto-sync)
6. [Keyboard Selection](#keyboard-selection)
7. [Selection Methods](#selection-methods)
8. [Getting Selected and Checked Nodes](#getting-selected-and-checked-nodes)
9. [Preventing Selection](#preventing-selection)
10. [Preventing Checks](#preventing-checks)
11. [Full Row Selection](#full-row-selection)
12. [Real-World Examples](#real-world-examples)
13. [Troubleshooting](#troubleshooting)

---

## Overview

Selection and checking are fundamental interactions in TreeView components. Syncfusion React TreeView provides flexible mechanisms for:
- Single and multi-node selection
- Three-state checkbox system (checked, unchecked, indeterminate)
- Automatic parent-child synchronization
- Keyboard shortcuts for power users
- Programmatic control via methods
- Event-based prevention logic

These features enable rich user experiences for scenarios like permission management, multi-select workflows, and organizational hierarchies.

---

## Single vs Multi-Selection Modes

### Basic Single Selection

By default, TreeView allows single selection. Only one node can be selected at a time.

```tsx
import React from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Desktop' },
  { id: '02', name: 'Documents', parentID: '01' },
  { id: '03', name: 'Downloads', parentID: '01' }
];

export default function SingleSelectionExample() {
  const handleNodeSelected = (args) => {
    console.log('Selected node:', args.node.textContent);
  };

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
      nodeSelected={handleNodeSelected}
    />
  );
}
```

### Multi-Selection Mode

Enable multi-selection with the `allowMultiSelection` property. Users can select multiple nodes using Ctrl+Click or Shift+Click.

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Desktop' },
  { id: '02', name: 'Documents', parentID: '01' },
  { id: '03', name: 'Downloads', parentID: '01' },
  { id: '04', name: 'Music', parentID: '01' },
  { id: '05', name: 'Projects', parentID: '02' },
  { id: '06', name: 'Resume.docx', parentID: '02' }
];

export default function MultiSelectionExample() {
  const treeRef = useRef(null);

  const handleNodeSelected = (args) => {
    const selectedNodes = treeRef.current?.getSelectedNodes();
    console.log('Selected nodes:', selectedNodes);
  };

  return (
    <div>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
        allowMultiSelection={true}
        nodeSelected={handleNodeSelected}
      />
    </div>
  );
}
```

### Comparison Table

| Feature | Single Selection | Multi-Selection |
|---------|------------------|-----------------|
| Max nodes selected | 1 | Unlimited |
| Ctrl+Click behavior | Deselects current | Toggles selection |
| Shift+Click behavior | Not applicable | Range selection |
| Default behavior | Yes | No (opt-in) |
| Use cases | Simple navigation | Batch operations |

---

## Checkbox Functionality

### Enabling Checkboxes

Add checkboxes to tree nodes with the `showCheckBox` property.

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Desktop' },
  { id: '02', name: 'Documents', parentID: '01' },
  { id: '03', name: 'Downloads', parentID: '01' },
  { id: '04', name: 'Resume.docx', parentID: '02' },
  { id: '05', name: 'CoverLetter.docx', parentID: '02' }
];

export default function CheckboxExample() {
  const treeRef = useRef(null);

  const handleCheckedChanged = (args) => {
    console.log('Checked nodes:', args.checkedNodes);
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
      showCheckBox={true}
      nodeChecked={handleCheckedChanged}
    />
  );
}
```

### Disabling Checkboxes for Specific Nodes

Control checkbox visibility per node using the `isChecked` field or dynamic disable logic.

```tsx
import React from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Desktop' },
  { id: '02', name: 'Documents', parentID: '01', isCheckboxDisabled: false },
  { id: '03', name: 'Downloads', parentID: '01', isCheckboxDisabled: true },
  { id: '04', name: 'Resume.docx', parentID: '02', isCheckboxDisabled: false },
  { id: '05', name: 'CoverLetter.docx', parentID: '02', isCheckboxDisabled: false }
];

export default function SelectiveCheckboxExample() {
  const handleCheckboxRendering = (args) => {
    // Prevent checkbox for read-only nodes
    if (args.node.classList.contains('read-only')) {
      args.node.querySelector('.e-checkbox-wrapper')?.style.setProperty('display', 'none');
    }
  };

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
      showCheckBox={true}
      nodeRendered={handleCheckboxRendering}
    />
  );
}
```

### Checkbox Styling and Customization

```tsx
import React from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';
import './checkbox-style.css';

const data = [
  { id: '01', name: 'Desktop' },
  { id: '02', name: 'Documents', parentID: '01' },
  { id: '03', name: 'Downloads', parentID: '01' }
];

export default function StyledCheckboxExample() {
  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
      showCheckBox={true}
      cssClass="custom-checkbox-treeview"
    />
  );
}
```

```css
/* checkbox-style.css */
.custom-checkbox-treeview .e-checkbox {
  accent-color: #FF6B6B;
  width: 18px;
  height: 18px;
}

.custom-checkbox-treeview .e-checkbox:hover {
  opacity: 0.8;
}

.custom-checkbox-treeview .e-treeview .e-list-item.e-selected > .e-full-row {
  background-color: #E8F5E9;
}
```

---

## Three-State Checkbox System

### Understanding Checkbox States

Syncfusion TreeView supports three checkbox states:
- **Checked**: Node and all children are checked
- **Unchecked**: Node and all children are unchecked
- **Indeterminate**: Some (but not all) children are checked

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const hierarchicalData = [
  { id: '01', name: 'Organization', expanded: true },
  { id: '02', name: 'Executive', parentID: '01', expanded: true },
  { id: '03', name: 'CEO', parentID: '02' },
  { id: '04', name: 'CTO', parentID: '02' },
  { id: '05', name: 'Engineering', parentID: '01', expanded: true },
  { id: '06', name: 'Frontend Lead', parentID: '05' },
  { id: '07', name: 'Backend Lead', parentID: '05' },
  { id: '08', name: 'QA Lead', parentID: '05' }
];

export default function ThreeStateCheckboxExample() {
  const treeRef = useRef(null);

  const getCheckboxStates = () => {
    const checkedNodes = treeRef.current?.getCheckedNodes();
    const uncheckedNodes = treeRef.current?.getAllNodes().filter(
      node => !checkedNodes.includes(node)
    );
    
    const indeterminateNodes = treeRef.current?.getAllNodes().filter(node => {
      const children = treeRef.current?.getChildren(node);
      const checkedChildren = children.filter(child => 
        checkedNodes.includes(child)
      );
      return checkedChildren.length > 0 && checkedChildren.length < children.length;
    });

    return { checkedNodes, uncheckedNodes, indeterminateNodes };
  };

  return (
    <div>
      <button onClick={() => console.log(getCheckboxStates())}>
        Get Checkbox States
      </button>
      <TreeViewComponent
        ref={treeRef}
        fields={{ 
          dataSource: hierarchicalData, 
          id: 'id', 
          text: 'name', 
          parentID: 'parentID',
          expanded: 'expanded'
        }}
        showCheckBox={true}
      />
    </div>
  );
}
```

### Visual Representation

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function CheckboxStateVisualization() {
  const treeRef = useRef(null);

  const renderCheckboxStatus = () => {
    const nodes = treeRef.current?.getAllNodes() || [];
    
    return nodes.map(node => {
      const checkboxElement = node.querySelector('.e-checkbox');
      const isChecked = checkboxElement?.classList.contains('e-check');
      const isIndeterminate = checkboxElement?.classList.contains('e-stop');
      
      return (
        <div key={node.id}>
          <span>{node.textContent}</span>
          <span className="state">
            {isChecked ? '✓ Checked' : isIndeterminate ? '◐ Indeterminate' : '○ Unchecked'}
          </span>
        </div>
      );
    });
  };

  return (
    <div>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
        showCheckBox={true}
      />
      <div className="checkbox-status">
        {renderCheckboxStatus()}
      </div>
    </div>
  );
}
```

---

## Parent-Child Checkbox Auto-Sync

### autoCheck Property

The `autoCheck` property automatically synchronizes checkbox states between parent and child nodes.

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Desktop', expanded: true },
  { id: '02', name: 'Documents', parentID: '01', expanded: true },
  { id: '03', name: 'Resume.docx', parentID: '02' },
  { id: '04', name: 'CoverLetter.docx', parentID: '02' },
  { id: '05', name: 'Downloads', parentID: '01', expanded: true },
  { id: '06', name: 'Software.exe', parentID: '05' },
  { id: '07', name: 'Document.pdf', parentID: '05' }
];

export default function AutoCheckExample() {
  const treeRef = useRef(null);

  const handleSync = () => {
    console.log('Auto-sync enabled: Checking a parent automatically checks children');
  };

  return (
    <div>
      <button onClick={handleSync}>Demonstrate Auto-Sync</button>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
        showCheckBox={true}
        autoCheck={true}
      />
      <p>Tip: Check "Documents" to automatically check all child files</p>
    </div>
  );
}
```

### Manual Parent-Child Sync

When `autoCheck` is false, implement manual synchronization:

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Desktop', expanded: true },
  { id: '02', name: 'Documents', parentID: '01', expanded: true },
  { id: '03', name: 'Resume.docx', parentID: '02' },
  { id: '04', name: 'CoverLetter.docx', parentID: '02' },
  { id: '05', name: 'Downloads', parentID: '01', expanded: true },
  { id: '06', name: 'Software.exe', parentID: '05' },
  { id: '07', name: 'Document.pdf', parentID: '05' }
];

export default function ManualSyncExample() {
  const treeRef = useRef(null);

  const handleNodeChecked = (args) => {
    const checkedNode = args.node;
    const nodeId = checkedNode.getAttribute('data-uid');
    const isChecked = args.node.querySelector('.e-checkbox').classList.contains('e-check');

    // Check/uncheck all children
    const childNodes = treeRef.current?.getChildren(nodeId);
    if (childNodes && childNodes.length > 0) {
      childNodes.forEach(child => {
        if (isChecked) {
          treeRef.current?.checkAll([child]);
        } else {
          treeRef.current?.uncheckAll([child]);
        }
      });
    }

    // Update parent state
    const parentNode = treeRef.current?.getParent(nodeId);
    if (parentNode) {
      updateParentCheckState(parentNode);
    }
  };

  const updateParentCheckState = (parentId) => {
    const parentNode = treeRef.current?.getNode(parentId);
    const children = treeRef.current?.getChildren(parentId);
    const checkedChildren = children.filter(child => 
      treeRef.current?.isNodeChecked(child)
    );

    if (checkedChildren.length === 0) {
      treeRef.current?.uncheckAll([parentId]);
    } else if (checkedChildren.length === children.length) {
      treeRef.current?.checkAll([parentId]);
    } else {
      // Set to indeterminate state (partial check)
      // Note: This is handled automatically by the control
    }
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
      showCheckBox={true}
      autoCheck={false}
      nodeChecked={handleNodeChecked}
    />
  );
}
```

### Advanced Sync with Validation

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function AdvancedSyncExample() {
  const treeRef = useRef(null);
  const maxSelectionsRef = useRef(5);

  const handleNodeChecking = (args) => {
    // Prevent checking if limit reached
    const checkedNodes = treeRef.current?.getCheckedNodes() || [];
    if (checkedNodes.length >= maxSelectionsRef.current && !args.isChecked) {
      args.cancel = true;
      alert(`Maximum ${maxSelectionsRef.current} selections allowed`);
    }
  };

  const handleNodeChecked = (args) => {
    const nodeId = args.node.getAttribute('data-uid');
    const isChecked = args.isChecked;

    // Cascade check/uncheck to children
    const children = treeRef.current?.getChildren(nodeId);
    if (children && children.length > 0) {
      children.forEach(childId => {
        const childCheckbox = treeRef.current?.getNode(childId)
          .querySelector('.e-checkbox');
        
        if (isChecked) {
          childCheckbox?.classList.add('e-check');
        } else {
          childCheckbox?.classList.remove('e-check');
        }
      });
    }
  };

  return (
    <div>
      <label>
        Max Selections:
        <input
          type="number"
          min="1"
          max="20"
          defaultValue={maxSelectionsRef.current}
          onChange={(e) => maxSelectionsRef.current = parseInt(e.target.value)}
        />
      </label>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
        showCheckBox={true}
        autoCheck={true}
        nodeChecking={handleNodeChecking}
        nodeChecked={handleNodeChecked}
      />
    </div>
  );
}
```

---

## Keyboard Selection

### Standard Keyboard Shortcuts

Syncfusion TreeView supports standard keyboard interactions:

| Key | Action |
|-----|--------|
| Arrow Up | Select previous node |
| Arrow Down | Select next node |
| Arrow Left | Collapse node |
| Arrow Right | Expand node |
| Ctrl+A | Select all nodes (when allowMultiSelection is true) |
| Ctrl+Click | Toggle individual node selection |
| Shift+Click | Select range of nodes |
| Space | Toggle checkbox state |
| F2 | Edit node (if allowEditing is true) |

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Desktop', expanded: true },
  { id: '02', name: 'Documents', parentID: '01', expanded: true },
  { id: '03', name: 'Resume.docx', parentID: '02' },
  { id: '04', name: 'CoverLetter.docx', parentID: '02' },
  { id: '05', name: 'Downloads', parentID: '01' }
];

export default function KeyboardNavigationExample() {
  const treeRef = useRef(null);

  const handleKeyDown = (args) => {
    const tree = treeRef.current;
    const selectedNode = tree?.getSelectedNode();

    // Custom keyboard handling
    if (args.key === 'Enter') {
      console.log('Opening:', selectedNode?.textContent);
    } else if (args.key === 'Delete') {
      const selectedNodes = tree?.getSelectedNodes();
      console.log('Deleting:', selectedNodes);
    } else if (args.ctrlKey && args.key === 'c') {
      console.log('Copying:', selectedNode?.textContent);
    }
  };

  return (
    <div onKeyDown={handleKeyDown} tabIndex={0}>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
        allowMultiSelection={true}
      />
      <p>Try: Arrow keys, Ctrl+Click for multi-select, Shift+Click for range</p>
    </div>
  );
}
```

### Custom Keyboard Handler

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function CustomKeyboardHandlerExample() {
  const treeRef = useRef(null);

  const handleCustomKeyboard = (e) => {
    if (!treeRef.current) return;

    const tree = treeRef.current;
    const selectedNode = tree.getSelectedNode();

    switch (e.key) {
      case '1':
        // Quick filter for level 1
        console.log('Filtering level 1 items');
        break;
      case '2':
        // Quick filter for level 2
        console.log('Filtering level 2 items');
        break;
      case 'b':
        if (e.ctrlKey) {
          e.preventDefault();
          // Bulk select children
          const children = tree.getChildren(selectedNode?.getAttribute('data-uid'));
          tree.selectAll();
        }
        break;
      case 'l':
        if (e.ctrlKey) {
          e.preventDefault();
          // Clear selection
          tree.clearSelection();
        }
        break;
      default:
        break;
    }
  };

  React.useEffect(() => {
    window.addEventListener('keydown', handleCustomKeyboard);
    return () => window.removeEventListener('keydown', handleCustomKeyboard);
  }, []);

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
      allowMultiSelection={true}
    />
  );
}
```

---

## Selection Methods

### selectNodes() - Select Specific Nodes

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Desktop' },
  { id: '02', name: 'Documents', parentID: '01' },
  { id: '03', name: 'Downloads', parentID: '01' },
  { id: '04', name: 'Music', parentID: '01' },
  { id: '05', name: 'Resume.docx', parentID: '02' }
];

export default function SelectNodesExample() {
  const treeRef = useRef(null);

  const selectSpecificNodes = () => {
    // Select nodes by array of node elements or IDs
    const nodesToSelect = ['02', '04'];
    treeRef.current?.selectNodes(nodesToSelect);
  };

  const selectByName = (name) => {
    const nodeElements = Array.from(
      treeRef.current?.querySelectorAll('.e-list-item') || []
    ).filter(node => node.textContent.includes(name));

    treeRef.current?.selectNodes(nodeElements);
  };

  return (
    <div>
      <button onClick={selectSpecificNodes}>Select Documents & Music</button>
      <button onClick={() => selectByName('Resume')}>Select Resume Items</button>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
        allowMultiSelection={true}
      />
    </div>
  );
}
```

### clearSelection() - Deselect All Nodes

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function ClearSelectionExample() {
  const treeRef = useRef(null);

  const handleClearSelection = () => {
    treeRef.current?.clearSelection();
    console.log('All selections cleared');
  };

  const handleSelectThenClear = async () => {
    // Select some nodes
    treeRef.current?.selectNodes(['01', '02', '03']);
    
    // Wait 2 seconds, then clear
    setTimeout(() => {
      treeRef.current?.clearSelection();
    }, 2000);
  };

  return (
    <div>
      <button onClick={handleClearSelection}>Clear Selection</button>
      <button onClick={handleSelectThenClear}>Select Then Clear</button>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
        allowMultiSelection={true}
      />
    </div>
  );
}
```

### checkAll() and uncheckAll() - Bulk Checkbox Operations

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Desktop' },
  { id: '02', name: 'Documents', parentID: '01' },
  { id: '03', name: 'Downloads', parentID: '01' },
  { id: '04', name: 'Music', parentID: '01' },
  { id: '05', name: 'Resume.docx', parentID: '02' },
  { id: '06', name: 'CoverLetter.docx', parentID: '02' }
];

export default function CheckAllExample() {
  const treeRef = useRef(null);

  const handleCheckAll = () => {
    treeRef.current?.checkAll();
    console.log('All nodes checked');
  };

  const handleUncheckAll = () => {
    treeRef.current?.uncheckAll();
    console.log('All nodes unchecked');
  };

  const handleCheckSpecific = () => {
    // Check only specific nodes
    const nodesToCheck = ['02', '04'];
    treeRef.current?.checkAll(nodesToCheck);
  };

  const handleToggleChecks = () => {
    const checkedNodes = treeRef.current?.getCheckedNodes() || [];
    const uncheckedNodes = treeRef.current?.getAllNodes().filter(
      node => !checkedNodes.includes(node)
    );

    treeRef.current?.uncheckAll(checkedNodes);
    treeRef.current?.checkAll(uncheckedNodes);
  };

  return (
    <div>
      <button onClick={handleCheckAll}>Check All</button>
      <button onClick={handleUncheckAll}>Uncheck All</button>
      <button onClick={handleCheckSpecific}>Check Specific</button>
      <button onClick={handleToggleChecks}>Toggle All</button>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
        showCheckBox={true}
      />
    </div>
  );
}
```

---

## Getting Selected and Checked Nodes

### getSelectedNodes() - Retrieve Selected Node IDs

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Desktop' },
  { id: '02', name: 'Documents', parentID: '01' },
  { id: '03', name: 'Downloads', parentID: '01' },
  { id: '04', name: 'Music', parentID: '01' }
];

export default function GetSelectedNodesExample() {
  const treeRef = useRef(null);
  const [selectedNodeInfo, setSelectedNodeInfo] = useState([]);

  const displaySelectedNodes = () => {
    const selectedNodes = treeRef.current?.getSelectedNodes() || [];
    const nodeInfo = selectedNodes.map(nodeId => {
      const node = treeRef.current?.getNode(nodeId);
      return {
        id: nodeId,
        text: node?.textContent || 'Unknown',
        level: node?.parentElement?.className?.includes('level-') ? 
          node.parentElement.className.match(/level-(\d+)/)?.[1] : 0
      };
    });
    setSelectedNodeInfo(nodeInfo);
  };

  return (
    <div>
      <button onClick={displaySelectedNodes}>Get Selected Nodes</button>
      <div className="selected-nodes">
        <h3>Selected Nodes:</h3>
        {selectedNodeInfo.map(node => (
          <div key={node.id}>
            <strong>{node.text}</strong> (ID: {node.id}, Level: {node.level})
          </div>
        ))}
      </div>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
        allowMultiSelection={true}
        nodeSelected={() => displaySelectedNodes()}
      />
    </div>
  );
}
```

### getCheckedNodes() - Retrieve Checked Node IDs

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Desktop' },
  { id: '02', name: 'Documents', parentID: '01' },
  { id: '03', name: 'Downloads', parentID: '01' },
  { id: '04', name: 'Music', parentID: '01' },
  { id: '05', name: 'Resume.docx', parentID: '02' }
];

export default function GetCheckedNodesExample() {
  const treeRef = useRef(null);

  const exportCheckedNodes = () => {
    const checkedNodes = treeRef.current?.getCheckedNodes() || [];
    const checkedData = checkedNodes.map(nodeId => {
      const node = treeRef.current?.getNode(nodeId);
      return {
        id: nodeId,
        text: node?.textContent || 'Unknown'
      };
    });

    console.log('Checked nodes:', checkedData);
    console.log('JSON:', JSON.stringify(checkedData, null, 2));

    // Download as JSON
    const dataStr = JSON.stringify(checkedData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'checked-nodes.json';
    link.click();
  };

  const getCheckStats = () => {
    const allNodes = treeRef.current?.getAllNodes() || [];
    const checkedNodes = treeRef.current?.getCheckedNodes() || [];
    
    return {
      total: allNodes.length,
      checked: checkedNodes.length,
      unchecked: allNodes.length - checkedNodes.length,
      percentage: ((checkedNodes.length / allNodes.length) * 100).toFixed(2)
    };
  };

  return (
    <div>
      <button onClick={exportCheckedNodes}>Export Checked Nodes</button>
      <button onClick={() => console.log(getCheckStats())}>Show Stats</button>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
        showCheckBox={true}
      />
    </div>
  );
}
```

### getAllNodes() - Get All Node References

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function GetAllNodesExample() {
  const treeRef = useRef(null);

  const analyzeAllNodes = () => {
    const allNodes = treeRef.current?.getAllNodes() || [];
    
    const analysis = {
      totalNodes: allNodes.length,
      selectedNodes: treeRef.current?.getSelectedNodes().length,
      checkedNodes: treeRef.current?.getCheckedNodes().length,
      expandedNodes: allNodes.filter(id => {
        const node = treeRef.current?.getNode(id);
        return node?.querySelector('.e-icons.e-icon-collapsible')?.classList.contains('e-icon-expandable');
      }).length
    };

    console.log('Node Analysis:', analysis);
    return analysis;
  };

  const treeTraversal = () => {
    const allNodes = treeRef.current?.getAllNodes() || [];
    const hierarchy = {};

    allNodes.forEach(nodeId => {
      const node = treeRef.current?.getNode(nodeId);
      const parent = treeRef.current?.getParent(nodeId);
      hierarchy[nodeId] = {
        text: node?.textContent,
        parent: parent || 'root'
      };
    });

    console.log('Node Hierarchy:', hierarchy);
  };

  return (
    <div>
      <button onClick={analyzeAllNodes}>Analyze All Nodes</button>
      <button onClick={treeTraversal}>Tree Traversal</button>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
        allowMultiSelection={true}
        showCheckBox={true}
      />
    </div>
  );
}
```

---

## Preventing Selection

### nodeSelecting Event - Cancel Selection

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Desktop' },
  { id: '02', name: 'Documents (Read-Only)', parentID: '01', readOnly: true },
  { id: '03', name: 'Downloads', parentID: '01' },
  { id: '04', name: 'Music (Locked)', parentID: '01', locked: true }
];

export default function PreventSelectionExample() {
  const treeRef = useRef(null);

  const handleNodeSelecting = (args) => {
    const nodeElement = args.node;
    const nodeId = nodeElement?.getAttribute('data-uid');
    const nodeData = data.find(d => d.id === nodeId);

    // Prevent selection of read-only nodes
    if (nodeData?.readOnly) {
      args.cancel = true;
      console.log('Cannot select read-only node');
      return;
    }

    // Prevent selection of locked nodes
    if (nodeData?.locked) {
      args.cancel = true;
      console.log('Cannot select locked node');
      return;
    }

    console.log('Selection allowed for:', nodeData?.name);
  };

  const handleNodeSelected = (args) => {
    const selectedNode = args.node;
    console.log('Node selected:', selectedNode?.textContent);
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
      allowMultiSelection={true}
      nodeSelecting={handleNodeSelecting}
      nodeSelected={handleNodeSelected}
    />
  );
}
```

### Prevent Deselection

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function PreventDeselectionExample() {
  const treeRef = useRef(null);
  const mandatorySelectedRef = useRef(['01']); // Must always be selected

  const handleNodeSelecting = (args) => {
    const nodeElement = args.node;
    const nodeId = nodeElement?.getAttribute('data-uid');

    // Prevent deselection of mandatory nodes
    if (mandatorySelectedRef.current.includes(nodeId) && !args.isSelected) {
      args.cancel = true;
      alert('This node must remain selected');
      return;
    }

    // Prevent multiple deselections
    const currentSelected = treeRef.current?.getSelectedNodes() || [];
    if (currentSelected.length === 1 && currentSelected[0] === nodeId && !args.isSelected) {
      args.cancel = true;
      console.log('At least one node must remain selected');
    }
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
      allowMultiSelection={true}
      nodeSelecting={handleNodeSelecting}
    />
  );
}
```

### Selection with Permission-Based Logic

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Public', permission: 'view' },
  { id: '02', name: 'Private', parentID: '01', permission: 'view-edit' },
  { id: '03', name: 'Admin', parentID: '01', permission: 'admin' },
  { id: '04', name: 'Restricted', parentID: '01', permission: 'none' }
];

export default function PermissionBasedSelectionExample() {
  const treeRef = useRef(null);
  const userRoleRef = useRef('user'); // user, editor, admin

  const canSelectNode = (nodeId) => {
    const nodeData = data.find(d => d.id === nodeId);
    if (!nodeData) return true;

    const permissionLevels = {
      none: ['admin'],
      'view-edit': ['editor', 'admin'],
      view: ['user', 'editor', 'admin'],
      admin: ['admin']
    };

    return permissionLevels[nodeData.permission]?.includes(userRoleRef.current) ?? false;
  };

  const handleNodeSelecting = (args) => {
    const nodeElement = args.node;
    const nodeId = nodeElement?.getAttribute('data-uid');

    if (!canSelectNode(nodeId)) {
      args.cancel = true;
      console.log(`User role "${userRoleRef.current}" cannot select this node`);
    }
  };

  return (
    <div>
      <select onChange={(e) => userRoleRef.current = e.target.value}>
        <option value="user">User</option>
        <option value="editor">Editor</option>
        <option value="admin">Admin</option>
      </select>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
        allowMultiSelection={true}
        nodeSelecting={handleNodeSelecting}
      />
    </div>
  );
}
```

---

## Preventing Checks

### nodeChecking Event - Cancel Check Operation

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Desktop' },
  { id: '02', name: 'System Files', parentID: '01', noCheck: true },
  { id: '03', name: 'Documents', parentID: '01' },
  { id: '04', name: 'Read-Only', parentID: '03', noCheck: true }
];

export default function PreventCheckExample() {
  const treeRef = useRef(null);

  const handleNodeChecking = (args) => {
    const nodeElement = args.node;
    const nodeId = nodeElement?.getAttribute('data-uid');
    const nodeData = data.find(d => d.id === nodeId);

    // Prevent checking of protected nodes
    if (nodeData?.noCheck && args.isChecked) {
      args.cancel = true;
      console.log('Cannot check protected node:', nodeData.name);
    }
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
      showCheckBox={true}
      nodeChecking={handleNodeChecking}
    />
  );
}
```

### Limit Number of Checked Nodes

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function CheckLimitExample() {
  const treeRef = useRef(null);
  const maxCheckedRef = useRef(3);

  const handleNodeChecking = (args) => {
    if (!args.isChecked) return; // Allow unchecking

    const checkedNodes = treeRef.current?.getCheckedNodes() || [];
    
    if (checkedNodes.length >= maxCheckedRef.current) {
      args.cancel = true;
      alert(`Maximum ${maxCheckedRef.current} items can be selected`);
    }
  };

  return (
    <div>
      <label>
        Max Checked:
        <input
          type="number"
          min="1"
          defaultValue={maxCheckedRef.current}
          onChange={(e) => maxCheckedRef.current = parseInt(e.target.value)}
        />
      </label>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
        showCheckBox={true}
        nodeChecking={handleNodeChecking}
      />
    </div>
  );
}
```

### Check with Validation Rules

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Role A' },
  { id: '02', name: 'Role B', parentID: '01', conflictsWith: 'Role C' },
  { id: '03', name: 'Role C', parentID: '01', conflictsWith: 'Role B' },
  { id: '04', name: 'Role D', parentID: '01' }
];

export default function CheckValidationRulesExample() {
  const treeRef = useRef(null);

  const hasConflict = (nodeId) => {
    const checkedNodes = treeRef.current?.getCheckedNodes() || [];
    const nodeData = data.find(d => d.id === nodeId);

    if (!nodeData?.conflictsWith) return false;

    return checkedNodes.some(checkedId => {
      const checkedData = data.find(d => d.id === checkedId);
      return checkedData?.name === nodeData.conflictsWith;
    });
  };

  const handleNodeChecking = (args) => {
    const nodeElement = args.node;
    const nodeId = nodeElement?.getAttribute('data-uid');

    if (args.isChecked && hasConflict(nodeId)) {
      args.cancel = true;
      const nodeData = data.find(d => d.id === nodeId);
      alert(`Cannot select ${nodeData?.name} - conflicts with already selected role`);
    }
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
      showCheckBox={true}
      nodeChecking={handleNodeChecking}
    />
  );
}
```

---

## Full Row Selection

### Enable Full Row Selection

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';
import './fullrow.css';

const data = [
  { id: '01', name: 'Desktop' },
  { id: '02', name: 'Documents', parentID: '01' },
  { id: '03', name: 'Downloads', parentID: '01' },
  { id: '04', name: 'Music', parentID: '01' }
];

export default function FullRowSelectionExample() {
  const treeRef = useRef(null);

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
      fullRowSelect={true}
      allowMultiSelection={true}
    />
  );
}
```

```css
/* fullrow.css */
.e-treeview .e-full-row {
  cursor: pointer;
  padding: 8px;
  transition: background-color 0.2s;
}

.e-treeview .e-list-item.e-selected > .e-full-row {
  background-color: #E3F2FD;
  border-left: 3px solid #2196F3;
}

.e-treeview .e-full-row:hover {
  background-color: #F5F5F5;
}

.e-treeview .e-list-item.e-selected > .e-full-row:hover {
  background-color: #BBDEFB;
}
```

### Highlight on Hover with Full Row

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';
import './fullrow-hover.css';

export default function FullRowHoverExample() {
  return (
    <TreeViewComponent
      fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
      fullRowSelect={true}
      cssClass="fullrow-hover-effect"
    />
  );
}
```

```css
/* fullrow-hover.css */
.fullrow-hover-effect .e-full-row {
  position: relative;
  overflow: hidden;
}

.fullrow-hover-effect .e-full-row::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3));
  opacity: 0;
  transition: opacity 0.3s;
}

.fullrow-hover-effect .e-full-row:hover::before {
  opacity: 1;
}
```

---

## Real-World Examples

### Example 1: Organization Chart with Role Selection

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const orgData = [
  { id: '01', name: 'Organization', icon: 'e-icons e-building' },
  { id: '02', name: 'Executive', parentID: '01', icon: 'e-icons e-user' },
  { id: '03', name: 'CEO', parentID: '02', role: 'ceo', salary: 250000 },
  { id: '04', name: 'CTO', parentID: '02', role: 'cto', salary: 200000 },
  { id: '05', name: 'Engineering', parentID: '01', icon: 'e-icons e-folder' },
  { id: '06', name: 'Frontend Lead', parentID: '05', role: 'lead', salary: 150000 },
  { id: '07', name: 'Backend Lead', parentID: '05', role: 'lead', salary: 150000 },
  { id: '08', name: 'QA Lead', parentID: '05', role: 'lead', salary: 140000 }
];

export default function OrgChartSelectionExample() {
  const treeRef = useRef(null);
  const [selectedEmployees, setSelectedEmployees] = useState([]);

  const handleNodeSelected = () => {
    const selectedIds = treeRef.current?.getSelectedNodes() || [];
    const employees = selectedIds.map(id => {
      const emp = orgData.find(e => e.id === id);
      return emp;
    }).filter(e => e?.role);

    setSelectedEmployees(employees);
  };

  const getTotalSalary = () => {
    return selectedEmployees.reduce((sum, emp) => sum + (emp?.salary || 0), 0);
  };

  const exportSelected = () => {
    const data = {
      employees: selectedEmployees,
      totalSalary: getTotalSalary(),
      count: selectedEmployees.length
    };
    console.log(JSON.stringify(data, null, 2));
  };

  return (
    <div>
      <div className="salary-info">
        <h3>Selected Employees</h3>
        <p>Count: {selectedEmployees.length}</p>
        <p>Total Salary: ${getTotalSalary().toLocaleString()}</p>
        <button onClick={exportSelected}>Export</button>
      </div>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: orgData, id: 'id', text: 'name', parentID: 'parentID', iconCss: 'icon' }}
        allowMultiSelection={true}
        fullRowSelect={true}
        nodeSelected={handleNodeSelected}
      />
    </div>
  );
}
```

### Example 2: File Manager with Selective Backup

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const fileData = [
  { id: '01', name: 'Desktop', size: 0, type: 'folder' },
  { id: '02', name: 'Documents', parentID: '01', size: 0, type: 'folder' },
  { id: '03', name: 'Resume.docx', parentID: '02', size: 45, type: 'file' },
  { id: '04', name: 'CoverLetter.docx', parentID: '02', size: 32, type: 'file' },
  { id: '05', name: 'Downloads', parentID: '01', size: 0, type: 'folder' },
  { id: '06', name: 'Software.exe', parentID: '05', size: 512, type: 'file' }
];

export default function FileBackupSelectionExample() {
  const treeRef = useRef(null);
  const [backupStats, setBackupStats] = useState({ files: 0, size: 0 });

  const calculateBackupSize = () => {
    const checkedNodes = treeRef.current?.getCheckedNodes() || [];
    let totalSize = 0;
    let fileCount = 0;

    checkedNodes.forEach(nodeId => {
      const file = fileData.find(f => f.id === nodeId);
      if (file?.type === 'file') {
        totalSize += file.size || 0;
        fileCount++;
      }
    });

    setBackupStats({ files: fileCount, size: totalSize });
  };

  const startBackup = () => {
    const checkedNodes = treeRef.current?.getCheckedNodes() || [];
    const backupItems = checkedNodes.map(id => fileData.find(f => f.id === id));
    console.log('Backing up:', backupItems);
    alert(`Backup started: ${backupStats.files} files, ${backupStats.size} MB`);
  };

  return (
    <div>
      <div className="backup-panel">
        <h3>Backup Manager</h3>
        <p>Files: {backupStats.files}</p>
        <p>Size: {backupStats.size} MB</p>
        <button onClick={calculateBackupSize}>Calculate</button>
        <button onClick={startBackup} disabled={backupStats.files === 0}>
          Start Backup
        </button>
      </div>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: fileData, id: 'id', text: 'name', parentID: 'parentID' }}
        showCheckBox={true}
        autoCheck={true}
      />
    </div>
  );
}
```

### Example 3: Permission Matrix with Multi-Select

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const permissionData = [
  { id: 'users', name: 'User Management' },
  { id: 'users-view', name: 'View Users', parentID: 'users' },
  { id: 'users-create', name: 'Create Users', parentID: 'users' },
  { id: 'users-edit', name: 'Edit Users', parentID: 'users' },
  { id: 'users-delete', name: 'Delete Users', parentID: 'users' },
  { id: 'reports', name: 'Reports' },
  { id: 'reports-view', name: 'View Reports', parentID: 'reports' },
  { id: 'reports-export', name: 'Export Reports', parentID: 'reports' },
  { id: 'admin', name: 'Admin Functions' },
  { id: 'admin-settings', name: 'System Settings', parentID: 'admin' },
  { id: 'admin-backup', name: 'Backup & Restore', parentID: 'admin' }
];

export default function PermissionMatrixExample() {
  const treeRef = useRef(null);
  const [selectedPermissions, setSelectedPermissions] = useState([]);
  const [roleName, setRoleName] = useState('');

  const handlePermissionChange = () => {
    const checked = treeRef.current?.getCheckedNodes() || [];
    setSelectedPermissions(checked);
  };

  const saveRole = () => {
    const roleData = {
      name: roleName,
      permissions: selectedPermissions,
      createdAt: new Date().toISOString()
    };
    console.log('Saving role:', roleData);
    alert(`Role "${roleName}" saved with ${selectedPermissions.length} permissions`);
  };

  return (
    <div>
      <div className="role-editor">
        <label>
          Role Name:
          <input
            value={roleName}
            onChange={(e) => setRoleName(e.target.value)}
            placeholder="Enter role name"
          />
        </label>
        <p>Selected Permissions: {selectedPermissions.length}</p>
        <button onClick={saveRole} disabled={!roleName || selectedPermissions.length === 0}>
          Save Role
        </button>
      </div>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: permissionData, id: 'id', text: 'name', parentID: 'parentID' }}
        showCheckBox={true}
        autoCheck={true}
        nodeChecked={handlePermissionChange}
        nodeUnchecked={handlePermissionChange}
      />
    </div>
  );
}
```

---

## Troubleshooting

### Issue: Parent nodes not automatically checking children

**Solution:** Ensure `autoCheck` property is enabled:

```tsx
<TreeViewComponent
  fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
  showCheckBox={true}
  autoCheck={true}  // Enable auto-sync
/>
```

### Issue: Multi-selection not working with Ctrl+Click

**Solution:** Enable `allowMultiSelection`:

```tsx
<TreeViewComponent
  fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
  allowMultiSelection={true}  // Required for multi-select
/>
```

### Issue: getSelectedNodes() returning empty array

**Solution:** Ensure nodes are selected and the component is properly initialized:

```tsx
const treeRef = useRef(null);

// Wait for component to be ready
const getSelected = () => {
  if (treeRef.current) {
    const selected = treeRef.current.getSelectedNodes();
    console.log('Selected:', selected);
  }
};
```

### Issue: Checkbox state not persisting across expand/collapse

**Solution:** Use `enablePersistence` property:

```tsx
<TreeViewComponent
  fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
  showCheckBox={true}
  enablePersistence={true}  // Persist state
/>
```

### Issue: Selection events not firing

**Solution:** Ensure event handlers are bound correctly:

```tsx
<TreeViewComponent
  ref={treeRef}
  fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
  allowMultiSelection={true}
  nodeSelected={(args) => {
    console.log('Node selected:', args);
  }}
  nodeSelecting={(args) => {
    console.log('Node selecting:', args);
  }}
/>
```

### Performance: Selecting many nodes at once

**Solution:** Use batch operations:

```tsx
const selectManyNodes = async () => {
  const nodeIds = ['01', '02', '03', '04', '05'];
  
  // Instead of calling selectNodes multiple times
  // Call once with array
  treeRef.current?.selectNodes(nodeIds);
};
```

### Issue: Inconsistent checkbox state with manual sync

**Solution:** Implement proper recursive synchronization:

```tsx
const syncCheckState = (nodeId, isChecked) => {
  const tree = treeRef.current;
  
  if (isChecked) {
    tree?.checkAll([nodeId]);
    // Recursively check all children
    const children = tree?.getChildren(nodeId);
    children?.forEach(child => syncCheckState(child, true));
  } else {
    tree?.uncheckAll([nodeId]);
    const children = tree?.getChildren(nodeId);
    children?.forEach(child => syncCheckState(child, false));
  }
};
```

---

## Best Practices

1. **Use autoCheck for parent-child sync** - Reduces manual event handling
2. **Validate before preventing selection** - Always provide user feedback
3. **Batch operations for better performance** - Select multiple nodes at once
4. **Use fullRowSelect for better UX** - Makes selection area larger
5. **Implement keyboard shortcuts** - Improve accessibility and power-user experience
6. **Persist selection state** - Use localStorage or database for critical selections
7. **Provide visual feedback** - Use custom CSS for selected/checked states
8. **Test edge cases** - Empty selections, max limits, conflicts

