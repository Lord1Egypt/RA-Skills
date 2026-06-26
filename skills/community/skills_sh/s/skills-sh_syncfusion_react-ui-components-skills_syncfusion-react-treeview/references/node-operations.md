# Node Operations and Manipulation

## Table of Contents

1. [Overview](#overview)
2. [Adding Nodes](#adding-nodes)
3. [Removing Nodes](#removing-nodes)
4. [Updating Node Data](#updating-node-data)
5. [Moving Nodes](#moving-nodes)
6. [Refreshing Nodes](#refreshing-nodes)
7. [Getting Node Information](#getting-node-information)
8. [Expanding and Collapsing](#expanding-and-collapsing)
9. [Advanced Operations](#advanced-operations)
10. [Troubleshooting](#troubleshooting)

## Overview

Dynamic node operations allow programmatic control over TreeView:
- Create new nodes (addNodes)
- Delete existing nodes (removeNodes)
- Modify node data (updateNode)
- Move nodes between parents (moveNodes)
- Refresh node data from backend (refreshNode)
- Retrieve node information (getNode, getTreeData)

## Adding Nodes

### Add as Child Node

```tsx
import * as React from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const treeRef = React.useRef(null);
  const [data, setData] = React.useState([
    {
      id: 1,
      name: 'Parent 1',
      child: [
        { id: 2, name: 'Child 1.1' }
      ]
    }
  ]);

  const addNode = () => {
    // Method 1: Using reference
    if (treeRef.current) {
      const newNode = { id: 3, name: 'Child 1.2' };
      treeRef.current.addNodes([newNode], '1'); // Add as child of node 1
    }
  };

  return (
    <>
      <button onClick={addNode}>Add Child to Parent 1</button>
      <TreeViewComponent
        ref={treeRef}
        fields={{
          dataSource: data,
          id: 'id',
          text: 'name',
          child: 'child'
        }}
      />
    </>
  );
}

export default App;
```

### Add Multiple Nodes

```tsx
const addMultipleNodes = () => {
  const newNodes = [
    { id: 4, name: 'New Child 1' },
    { id: 5, name: 'New Child 2' },
    { id: 6, name: 'New Child 3' }
  ];
  
  treeRef.current.addNodes(newNodes, '1'); // All as children of node 1
};
```

### Add with Specific Index

```tsx
// Add at specific position in children list
treeRef.current.addNodes([{ id: 7, name: 'Inserted' }], '1', 0); // Insert at index 0

// Method: addNodes(nodeArray, targetId, index)
// If index not provided, adds at end
```

### Add as Sibling

```tsx
// Get parent of reference node, then add as child
const addSibling = (targetNodeId) => {
  const targetNode = treeRef.current.getNode(/* get element */);
  const parentNode = targetNode.parentElement; // Navigate DOM
  
  // Better: Use parent ID from data
  const newNode = { id: 8, name: 'Sibling', pid: targetNode.parentID };
  treeRef.current.addNodes([newNode], targetNode.parentID);
};
```

## Removing Nodes

### Remove Single Node

```tsx
const removeNode = (nodeId) => {
  if (treeRef.current) {
    treeRef.current.removeNodes([nodeId]);
  }
};

// Usage
<button onClick={() => removeNode('2')}>Remove Node 2</button>
```

### Remove Multiple Nodes

```tsx
const removeMultipleNodes = () => {
  const nodeIds = ['2', '3', '4'];
  treeRef.current.removeNodes(nodeIds);
};
```

### Remove with Confirmation

```tsx
const removeNodeSafe = (nodeId) => {
  if (window.confirm('Are you sure?')) {
    treeRef.current.removeNodes([nodeId]);
  }
};
```

## Updating Node Data

### Change Node Text

```tsx
const updateNodeText = (nodeId, newText) => {
  if (treeRef.current) {
    treeRef.current.updateNode(nodeId, newText);
  }
};

// Usage
<button onClick={() => updateNodeText('2', 'Updated Name')}>
  Update Node 2
</button>
```

### Update Node with New Data

```tsx
const updateNodeData = (nodeId, newData) => {
  // updateNode only changes text
  // For other properties, update source and refresh
  
  // Find node in data
  const updateInData = (nodes) => {
    return nodes.map(node => {
      if (node.id === nodeId) {
        return { ...node, ...newData };
      }
      if (node.child) {
        node.child = updateInData(node.child);
      }
      return node;
    });
  };

  const updated = updateInData(data);
  setData(updated);
  
  // Update display
  treeRef.current.updateNode(nodeId, newData.name);
};
```

## Moving Nodes

### Move Node to Different Parent

```tsx
const moveNode = (nodeId, newParentId, position = -1) => {
  if (treeRef.current) {
    // moveNodes(nodeIds, targetId, index)
    treeRef.current.moveNodes([nodeId], newParentId, position);
  }
};

// Move node 5 to be child of node 3, at position 0
<button onClick={() => moveNode('5', '3', 0)}>
  Move to Different Parent
</button>
```

### Reorder Siblings

```tsx
// Move node before another node at same level
const moveNodeBefore = (nodeId, beforeNodeId) => {
  // Get parent of beforeNode
  const getParentId = (nodes, targetId) => {
    for (let node of nodes) {
      if (node.child) {
        const index = node.child.findIndex(n => n.id === targetId);
        if (index >= 0) return node.id;
        const found = getParentId(node.child, targetId);
        if (found) return found;
      }
    }
    return null;
  };

  const parentId = getParentId(data, beforeNodeId);
  if (parentId) {
    treeRef.current.moveNodes([nodeId], parentId, 0);
  }
};
```

## Refreshing Nodes

### Refresh Single Node from Backend

```tsx
const refreshNode = async (nodeId) => {
  // Fetch fresh data from server
  const response = await fetch(`/api/nodes/${nodeId}`);
  const freshData = await response.json();

  // Update TreeView
  if (treeRef.current) {
    treeRef.current.refreshNode(nodeId, freshData);
  }
};
```

### Refresh Children on Expand

```tsx
const handleNodeExpanding = async (args) => {
  if (args.nodeData.hasChildren && !args.nodeData.child) {
    // Children not loaded, fetch from backend
    const response = await fetch(`/api/nodes/${args.nodeData.id}/children`);
    const children = await response.json();
    args.nodeData.child = children;
    
    // Refresh display
    treeRef.current.refreshNode(args.nodeData.id, args.nodeData);
  }
};
```

## Getting Node Information

### Get Node by Element

```tsx
const getNodeInfo = (element) => {
  const node = treeRef.current.getNode(element);
  console.log('Node ID:', node.id);
  console.log('Node Text:', node.text);
};
```

### Get All Tree Data

```tsx
const getAllData = () => {
  if (treeRef.current) {
    const allData = treeRef.current.getTreeData();
    console.log('All tree data:', allData);
    return allData;
  }
};
```

### Get Specific Node Data

```tsx
const getNodeData = (nodeId) => {
  const allData = treeRef.current.getTreeData();
  
  const find = (nodes) => {
    for (let node of nodes) {
      if (node.id === nodeId) return node;
      if (node.child) {
        const found = find(node.child);
        if (found) return found;
      }
    }
    return null;
  };

  return find(allData);
};
```

### Get Selected Nodes

```tsx
const getSelectedNodeIds = () => {
  const selectedIds = treeRef.current.selectedNodes;
  console.log('Selected IDs:', selectedIds);
};

// Get selected node data
const getSelectedNodeData = () => {
  const selectedIds = treeRef.current.selectedNodes;
  const allData = treeRef.current.getTreeData();
  
  const selected = [];
  const findNodes = (nodes) => {
    nodes.forEach(node => {
      if (selectedIds.includes(node.id.toString())) {
        selected.push(node);
      }
      if (node.child) findNodes(node.child);
    });
  };
  
  findNodes(allData);
  return selected;
};
```

### Get Checked Nodes

```tsx
const getCheckedNodeIds = () => {
  return treeRef.current.checkedNodes;
};

const getCheckedNodeData = () => {
  const checkedIds = treeRef.current.checkedNodes;
  const allData = treeRef.current.getTreeData();
  
  // Similar to getSelectedNodeData
  // Filter nodes where id is in checkedIds
};
```

## Expanding and Collapsing

### Expand All Nodes

```tsx
const expandAll = () => {
  treeRef.current.expandAll();
};
```

### Collapse All Nodes

```tsx
const collapseAll = () => {
  treeRef.current.collapseAll();
};
```

### Expand Specific Nodes

```tsx
const expandNodes = (nodeIds) => {
  if (treeRef.current) {
    treeRef.current.expandAll(nodeIds);
  }
};

// Expand nodes with IDs 1 and 3
<button onClick={() => expandNodes(['1', '3'])}>
  Expand Selected
</button>
```

### Expand Only Parent Nodes

```tsx
const expandParentNodesOnly = () => {
  const allData = treeRef.current.getTreeData();
  const parentIds = [];
  
  const findParents = (nodes) => {
    nodes.forEach(node => {
      if (node.child && node.child.length > 0) {
        parentIds.push(node.id.toString());
      }
      if (node.child) findParents(node.child);
    });
  };
  
  findParents(allData);
  treeRef.current.expandAll(parentIds);
};
```

## Advanced Operations

### Bulk Operations

```tsx
const bulkAddNodes = async (parentId, count) => {
  const newNodes = [];
  for (let i = 0; i < count; i++) {
    newNodes.push({
      id: Date.now() + i,
      name: `New Node ${i + 1}`
    });
  }
  treeRef.current.addNodes(newNodes, parentId);
};

// Add 100 nodes
<button onClick={() => bulkAddNodes('1', 100)}>
  Add 100 Nodes
</button>
```

### Transaction-like Operations

```tsx
const performOperations = (operations) => {
  // operations = [
  //   { action: 'add', data: [...], parentId: '1' },
  //   { action: 'remove', nodeIds: ['2', '3'] },
  //   { action: 'update', nodeId: '4', data: {...} }
  // ]

  operations.forEach(op => {
    switch (op.action) {
      case 'add':
        treeRef.current.addNodes(op.data, op.parentId);
        break;
      case 'remove':
        treeRef.current.removeNodes(op.nodeIds);
        break;
      case 'update':
        treeRef.current.updateNode(op.nodeId, op.data.name);
        break;
    }
  });
};
```

### Undo/Redo Operations

```tsx
class TreeOperationHistory {
  constructor() {
    this.history = [];
    this.currentIndex = -1;
  }

  addOperation(operation) {
    this.history = this.history.slice(0, this.currentIndex + 1);
    this.history.push(operation);
    this.currentIndex++;
  }

  undo() {
    if (this.currentIndex > 0) {
      this.currentIndex--;
      return this.history[this.currentIndex];
    }
  }

  redo() {
    if (this.currentIndex < this.history.length - 1) {
      this.currentIndex++;
      return this.history[this.currentIndex];
    }
  }
}

// Usage
const history = new TreeOperationHistory();

const addWithHistory = (nodes, parentId) => {
  treeRef.current.addNodes(nodes, parentId);
  history.addOperation({ action: 'add', nodes, parentId });
};
```

## Troubleshooting

### Nodes Not Adding

```tsx
// ❌ Wrong - ref not initialized
treeRef.current.addNodes([newNode], '1'); // Error if not ready

// ✅ Correct - Check ref exists
if (treeRef.current) {
  treeRef.current.addNodes([newNode], '1');
}
```

### Move Not Working

```tsx
// ❌ Wrong - NodeID as number
treeRef.current.moveNodes([5], 3); // IDs should be strings

// ✅ Correct - String IDs
treeRef.current.moveNodes(['5'], '3');
```

### Update Not Persisting

```tsx
// ✅ Update both TreeView and source data
const updateNodeWithPersist = (nodeId, newText) => {
  // Update display
  treeRef.current.updateNode(nodeId, newText);
  
  // Update source data
  const updated = updateInData(data, nodeId, newText);
  setData(updated);
  
  // Optionally save to backend
  saveNodeToServer(nodeId, newText);
};
```

---

**Key Takeaways:**
- ✅ Use `addNodes()` to create nodes dynamically
- ✅ Use `removeNodes()` to delete nodes
- ✅ Use `updateNode()` for text changes
- ✅ Use `moveNodes()` to reorder or move nodes
- ✅ Use `refreshNode()` for backend data updates
- ✅ Check ref exists before operations
- ✅ Keep source data in sync with TreeView

