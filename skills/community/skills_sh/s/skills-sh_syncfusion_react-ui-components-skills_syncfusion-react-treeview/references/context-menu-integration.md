# TreeView Context Menu Integration Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Context Menu Setup](#context-menu-setup)
3. [ContextMenuComponent Overview](#contextmenucomponent-overview)
4. [Right-Click Node Selection](#right-click-node-selection)
5. [Context Menu Items Configuration](#context-menu-items-configuration)
6. [Event Handling](#event-handling)
7. [Menu Item Enabling/Disabling](#menu-item-enablingdisabling)
8. [Node Operations via Context Menu](#node-operations-via-context-menu)
9. [Copy/Cut/Paste Patterns](#copycutpaste-patterns)
10. [Data Coordination](#data-coordination)
11. [Menu Items with Icons](#menu-items-with-icons)
12. [Separators and Submenus](#separators-and-submenus)
13. [Custom Menu Styling](#custom-menu-styling)
14. [Dynamic Menu Items](#dynamic-menu-items)
15. [Real-World Patterns](#real-world-patterns)
16. [Performance Optimization](#performance-optimization)
17. [Troubleshooting](#troubleshooting)
18. [Best Practices](#best-practices)

---

## Introduction

Context menus provide quick access to node operations in TreeView. This guide covers integrating Syncfusion's ContextMenuComponent with TreeView to enable right-click operations like add, edit, delete, copy, cut, and paste.

### Key Integration Points
- ContextMenuComponent from @syncfusion/ej2-react-popups
- Right-click event handling
- Node operation coordination
- Menu item state management
- Copy/paste clipboard operations
- Dynamic menu item generation

---

## Context Menu Setup

### Installation

```bash
npm install @syncfusion/ej2-react-popups
npm install @syncfusion/ej2-react-navigations
```

### Basic Setup

```tsx
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';
import { ContextMenuComponent } from '@syncfusion/ej2-react-popups';
import React, { useRef, useState } from 'react';

function TreeViewWithContextMenu() {
  const treeRef = useRef(null);
  const contextMenuRef = useRef(null);

  const data = [
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' },
    { id: 3, name: 'Item 2', hasChild: true }
  ];

  const menuItems = [
    { text: 'Add', id: 'add', icon: 'e-icons e-plus' },
    { text: 'Edit', id: 'edit', icon: 'e-icons e-edit' },
    { text: 'Delete', id: 'delete', icon: 'e-icons e-trash' }
  ];

  return (
    <>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      />
      <ContextMenuComponent
        ref={contextMenuRef}
        items={menuItems}
        target=".e-treeview .e-list-item"
      />
    </>
  );
}

export default TreeViewWithContextMenu;
```

---

## ContextMenuComponent Overview

### Component Properties

```tsx
function ContextMenuPropertiesDemo() {
  const menuItems = [
    { text: 'Cut', id: 'cut', icon: 'e-icons e-cut' },
    { text: 'Copy', id: 'copy', icon: 'e-icons e-copy' },
    { text: 'Paste', id: 'paste', icon: 'e-icons e-paste' }
  ];

  return (
    <ContextMenuComponent
      items={menuItems}
      target=".e-treeview .e-list-item"
      cssClass="custom-context-menu"
      enableScrolling={true}
      maxHeight="300px"
      closeOnDocumentClick={true}
      enabled={true}
    />
  );
}

export default ContextMenuPropertiesDemo;
```

### Available ContextMenu Properties

| Property | Type | Description |
|----------|------|-------------|
| `items` | MenuItemModel[] | Array of menu items |
| `target` | string | Selector for target elements |
| `cssClass` | string | CSS class for styling |
| `showIcon` | boolean | Show icons in menu items |
| `enableScrolling` | boolean | Enable scrolling for long menus |
| `closeOnDocumentClick` | boolean | Close menu when clicking outside |
| `enabled` | boolean | Enable/disable context menu |
| `animationSettings` | AnimationSettings | Animation configuration |

---

## Right-Click Node Selection

### Handling Right-Click Events

```tsx
function RightClickSelection() {
  const [selectedNode, setSelectedNode] = useState(null);
  const treeRef = useRef(null);
  const contextMenuRef = useRef(null);

  const data = [
    { id: 1, name: 'Folder 1', hasChild: true },
    { id: 2, pid: 1, name: 'File 1.txt' },
    { id: 3, name: 'Folder 2', hasChild: true }
  ];

  const handleNodeRightClick = (args) => {
    // Prevent default context menu
    args.event.preventDefault();

    // Select the right-clicked node
    const nodeElement = args.event.target.closest('.e-list-item');
    if (nodeElement) {
      const nodeId = nodeElement.id || nodeElement.getAttribute('data-node-id');
      setSelectedNode(nodeId);
      console.log('Right-clicked node:', nodeId);
    }
  };

  const handleTreeContextMenu = (e) => {
    if (e.which === 3) { // Right-click
      e.preventDefault();
      const nodeElement = e.target.closest('.e-list-item');
      if (nodeElement) {
        setSelectedNode(nodeElement.id);
      }
    }
  };

  const menuItems = [
    { text: 'Cut', id: 'cut', icon: 'e-icons e-cut' },
    { text: 'Copy', id: 'copy', icon: 'e-icons e-copy' },
    { text: 'Paste', id: 'paste', icon: 'e-icons e-paste' }
  ];

  return (
    <div onContextMenu={handleTreeContextMenu}>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
        cssClass={selectedNode ? 'node-selected' : ''}
      />
      <ContextMenuComponent
        ref={contextMenuRef}
        items={menuItems}
        target=".e-treeview .e-list-item"
      />
    </div>
  );
}

export default RightClickSelection;
```

### CSS for Selected Node

```css
.e-treeview .e-list-item {
  transition: background-color 0.2s ease;
}

.e-treeview .node-selected .e-list-item.e-active {
  background-color: #bbdefb;
  border-left: 4px solid #1976d2;
}

.e-treeview .e-list-item:hover {
  background-color: #f5f5f5;
}
```

---

## Context Menu Items Configuration

### Basic Menu Items

```tsx
function BasicMenuItems() {
  const menuItems = [
    { text: 'New', id: 'new' },
    { text: 'Open', id: 'open' },
    { text: 'Save', id: 'save' }
  ];

  return (
    <ContextMenuComponent
      items={menuItems}
      target=".e-treeview .e-list-item"
    />
  );
}

export default BasicMenuItems;
```

### Menu Items with Properties

```tsx
function AdvancedMenuItems() {
  const menuItems = [
    {
      text: 'Add Item',
      id: 'add-item',
      icon: 'e-icons e-plus',
      title: 'Add a new item'
    },
    {
      text: 'Edit Item',
      id: 'edit-item',
      icon: 'e-icons e-edit',
      title: 'Edit current item',
      enabled: true
    },
    {
      text: 'Delete Item',
      id: 'delete-item',
      icon: 'e-icons e-trash',
      title: 'Delete current item',
      className: 'danger-item'
    },
    {
      text: 'Rename',
      id: 'rename',
      icon: 'e-icons e-rename',
      disabled: false
    }
  ];

  return (
    <ContextMenuComponent
      items={menuItems}
      target=".e-treeview .e-list-item"
      showIcon={true}
    />
  );
}

export default AdvancedMenuItems;
```

### Menu Item Event Arguments

```tsx
function MenuItemEventHandling() {
  const menuItems = [
    { text: 'Action 1', id: 'action1' },
    { text: 'Action 2', id: 'action2' }
  ];

  const handleBeforeOpen = (args) => {
    // args.element - Target element
    // args.items - Menu items
    // args.event - Event object
    console.log('Menu before open:', args);
  };

  const handleSelect = (args) => {
    // args.item - Selected item
    // args.element - Menu item element
    // args.event - Event object
    console.log('Menu item selected:', args.item.id);
  };

  const handleClose = (args) => {
    console.log('Menu closed');
  };

  return (
    <ContextMenuComponent
      items={menuItems}
      target=".e-treeview .e-list-item"
      beforeOpen={handleBeforeOpen}
      select={handleSelect}
      close={handleClose}
    />
  );
}

export default MenuItemEventHandling;
```

---

## Event Handling

### beforeOpen Event

```tsx
function BeforeOpenEventHandler() {
  const treeRef = useRef(null);
  const contextMenuRef = useRef(null);

  const data = [
    { id: 1, name: 'Locked Item', locked: true, hasChild: true },
    { id: 2, pid: 1, name: 'Child Item' },
    { id: 3, name: 'Regular Item', hasChild: true }
  ];

  const menuItems = [
    { text: 'Edit', id: 'edit', icon: 'e-icons e-edit' },
    { text: 'Delete', id: 'delete', icon: 'e-icons e-trash' },
    { text: 'Lock', id: 'lock', icon: 'e-icons e-lock' }
  ];

  const handleBeforeOpen = (args) => {
    const nodeElement = args.element;
    const nodeId = nodeElement.id;
    
    // Get node data
    const treeInstance = treeRef.current.ej2_instances[0];
    const nodeData = treeInstance.getNode(nodeId);

    // Disable menu items based on node state
    if (nodeData && nodeData.locked) {
      // Disable edit for locked items
      args.items.forEach(item => {
        if (item.id === 'edit') {
          item.disabled = true;
        }
      });
    }
  };

  return (
    <>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      />
      <ContextMenuComponent
        ref={contextMenuRef}
        items={menuItems}
        target=".e-treeview .e-list-item"
        beforeOpen={handleBeforeOpen}
      />
    </>
  );
}

export default BeforeOpenEventHandler;
```

### select Event

```tsx
function SelectEventHandler() {
  const treeRef = useRef(null);

  const data = [
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' }
  ];

  const menuItems = [
    { text: 'Add', id: 'add', icon: 'e-icons e-plus' },
    { text: 'Edit', id: 'edit', icon: 'e-icons e-edit' },
    { text: 'Delete', id: 'delete', icon: 'e-icons e-trash' }
  ];

  const handleMenuSelect = (args) => {
    const targetElement = args.element;
    const itemId = args.item.id;
    const nodeId = targetElement.id;

    const treeInstance = treeRef.current.ej2_instances[0];
    const nodeData = treeInstance.getNode(nodeId);

    switch (itemId) {
      case 'add':
        console.log('Add new item under:', nodeData.text);
        // Handle add operation
        break;
      case 'edit':
        console.log('Edit item:', nodeData.text);
        // Handle edit operation
        break;
      case 'delete':
        console.log('Delete item:', nodeData.text);
        // Handle delete operation
        break;
      default:
        break;
    }
  };

  return (
    <>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      />
      <ContextMenuComponent
        items={menuItems}
        target=".e-treeview .e-list-item"
        select={handleMenuSelect}
      />
    </>
  );
}

export default SelectEventHandler;
```

### close Event

```tsx
function CloseEventHandler() {
  const handleMenuClose = (args) => {
    console.log('Context menu closed');
    // Clean up or save state
  };

  const menuItems = [
    { text: 'Action', id: 'action' }
  ];

  return (
    <ContextMenuComponent
      items={menuItems}
      target=".e-treeview .e-list-item"
      close={handleMenuClose}
    />
  );
}

export default CloseEventHandler;
```

---

## Menu Item Enabling/Disabling

### Conditional Enabling Based on Node Type

```tsx
function ConditionalMenuEnabling() {
  const treeRef = useRef(null);

  const data = [
    { id: 1, name: 'Folder', hasChild: true, type: 'folder' },
    { id: 2, pid: 1, name: 'File.txt', type: 'file' },
    { id: 3, name: 'Read-Only', type: 'readonly' }
  ];

  const menuItems = [
    { text: 'Add Item', id: 'add', icon: 'e-icons e-plus' },
    { text: 'Edit', id: 'edit', icon: 'e-icons e-edit' },
    { text: 'Delete', id: 'delete', icon: 'e-icons e-trash' },
    { text: 'Compress', id: 'compress', icon: 'e-icons e-compress' }
  ];

  const handleBeforeOpen = (args) => {
    const targetElement = args.element;
    const treeInstance = treeRef.current.ej2_instances[0];
    const nodeData = treeInstance.getNode(targetElement.id);

    // Reset all items as enabled
    args.items.forEach(item => item.disabled = false);

    if (nodeData.type === 'file') {
      // Files cannot have children
      const addItem = args.items.find(item => item.id === 'add');
      if (addItem) addItem.disabled = true;
    }

    if (nodeData.type === 'readonly') {
      // Read-only items cannot be edited or deleted
      args.items.forEach(item => {
        if (item.id === 'edit' || item.id === 'delete') {
          item.disabled = true;
        }
      });
    }

    if (nodeData.type !== 'folder') {
      // Only folders can be compressed
      const compressItem = args.items.find(item => item.id === 'compress');
      if (compressItem) compressItem.disabled = true;
    }
  };

  return (
    <>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      />
      <ContextMenuComponent
        items={menuItems}
        target=".e-treeview .e-list-item"
        beforeOpen={handleBeforeOpen}
      />
    </>
  );
}

export default ConditionalMenuEnabling;
```

### Disabling Items by Permission

```tsx
function PermissionBasedMenuEnabling() {
  const treeRef = useRef(null);
  const [userRole, setUserRole] = useState('viewer');

  const data = [
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' }
  ];

  const menuItems = [
    { text: 'View', id: 'view', icon: 'e-icons e-eye' },
    { text: 'Edit', id: 'edit', icon: 'e-icons e-edit' },
    { text: 'Delete', id: 'delete', icon: 'e-icons e-trash' },
    { text: 'Share', id: 'share', icon: 'e-icons e-share' }
  ];

  const handleBeforeOpen = (args) => {
    // Reset items
    args.items.forEach(item => item.disabled = false);

    // Apply permissions
    const permissions = {
      viewer: ['view'],
      editor: ['view', 'edit'],
      admin: ['view', 'edit', 'delete', 'share']
    };

    const allowedActions = permissions[userRole] || [];

    args.items.forEach(item => {
      item.disabled = !allowedActions.includes(item.id);
    });
  };

  return (
    <>
      <div style={{ marginBottom: '20px' }}>
        <select value={userRole} onChange={(e) => setUserRole(e.target.value)}>
          <option value="viewer">Viewer</option>
          <option value="editor">Editor</option>
          <option value="admin">Admin</option>
        </select>
      </div>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      />
      <ContextMenuComponent
        items={menuItems}
        target=".e-treeview .e-list-item"
        beforeOpen={handleBeforeOpen}
      />
    </>
  );
}

export default PermissionBasedMenuEnabling;
```

---

## Node Operations via Context Menu

### Add Node Operation

```tsx
function AddNodeOperation() {
  const treeRef = useRef(null);
  const [treeData, setTreeData] = useState([
    { id: 1, name: 'Parent 1', hasChild: true },
    { id: 2, pid: 1, name: 'Child 1' }
  ]);
  const [nextId, setNextId] = useState(3);

  const menuItems = [
    { text: 'Add', id: 'add', icon: 'e-icons e-plus' },
    { text: 'Delete', id: 'delete', icon: 'e-icons e-trash' }
  ];

  const handleMenuSelect = (args) => {
    if (args.item.id === 'add') {
      const targetElement = args.element;
      const treeInstance = treeRef.current.ej2_instances[0];
      const parentNode = treeInstance.getNode(targetElement.id);

      // Create new item
      const newItem = {
        id: nextId,
        pid: parentNode.id,
        name: `New Item ${nextId}`
      };

      // Update parent to show children
      setTreeData(prev => {
        const updated = [...prev];
        const parent = updated.find(item => item.id === parentNode.id);
        if (parent) {
          parent.hasChild = true;
        }
        return [...updated, newItem];
      });

      setNextId(nextId + 1);
      console.log('Added new item:', newItem);
    }
  };

  return (
    <>
      <TreeViewComponent
        ref={treeRef}
        fields={{
          dataSource: treeData,
          id: 'id',
          parentID: 'pid',
          text: 'name',
          hasChildren: 'hasChild'
        }}
      />
      <ContextMenuComponent
        items={menuItems}
        target=".e-treeview .e-list-item"
        select={handleMenuSelect}
      />
    </>
  );
}

export default AddNodeOperation;
```

### Edit Node Operation

```tsx
function EditNodeOperation() {
  const treeRef = useRef(null);
  const [treeData, setTreeData] = useState([
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' }
  ]);

  const menuItems = [
    { text: 'Edit', id: 'edit', icon: 'e-icons e-edit' }
  ];

  const handleMenuSelect = (args) => {
    if (args.item.id === 'edit') {
      const targetElement = args.element;
      const treeInstance = treeRef.current.ej2_instances[0];
      
      // Start inline editing
      treeInstance.beginEdit(targetElement.id);
      console.log('Edit started for:', targetElement.id);
    }
  };

  const handleNodeEdited = (args) => {
    console.log('Node updated from', args.oldText, 'to', args.newText);
  };

  return (
    <>
      <TreeViewComponent
        ref={treeRef}
        fields={{
          dataSource: treeData,
          id: 'id',
          parentID: 'pid',
          text: 'name',
          hasChildren: 'hasChild'
        }}
        allowEditing={true}
        nodeEdited={handleNodeEdited}
      />
      <ContextMenuComponent
        items={menuItems}
        target=".e-treeview .e-list-item"
        select={handleMenuSelect}
      />
    </>
  );
}

export default EditNodeOperation;
```

### Delete Node Operation

```tsx
function DeleteNodeOperation() {
  const treeRef = useRef(null);
  const [treeData, setTreeData] = useState([
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' },
    { id: 3, name: 'Item 2' }
  ]);

  const menuItems = [
    { text: 'Delete', id: 'delete', icon: 'e-icons e-trash' }
  ];

  const handleMenuSelect = (args) => {
    if (args.item.id === 'delete') {
      const targetElement = args.element;
      const treeInstance = treeRef.current.ej2_instances[0];
      const nodeData = treeInstance.getNode(targetElement.id);

      if (confirm(`Delete "${nodeData.text}"?`)) {
        // Delete node and its children
        const childrenToDelete = treeData.filter(item => 
          item.pid === nodeData.id || item.id === nodeData.id
        );

        setTreeData(prev => 
          prev.filter(item => !childrenToDelete.includes(item))
        );

        console.log('Deleted:', nodeData.text);
      }
    }
  };

  return (
    <>
      <TreeViewComponent
        ref={treeRef}
        fields={{
          dataSource: treeData,
          id: 'id',
          parentID: 'pid',
          text: 'name',
          hasChildren: 'hasChild'
        }}
      />
      <ContextMenuComponent
        items={menuItems}
        target=".e-treeview .e-list-item"
        select={handleMenuSelect}
      />
    </>
  );
}

export default DeleteNodeOperation;
```

---

## Copy/Cut/Paste Patterns

### Copy and Paste Implementation

```tsx
function CopyPasteOperation() {
  const treeRef = useRef(null);
  const [treeData, setTreeData] = useState([
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' },
    { id: 3, name: 'Item 2' }
  ]);
  const [clipboard, setClipboard] = useState(null);
  const [nextId, setNextId] = useState(4);

  const menuItems = [
    { text: 'Copy', id: 'copy', icon: 'e-icons e-copy' },
    { text: 'Paste', id: 'paste', icon: 'e-icons e-paste' }
  ];

  const handleMenuSelect = (args) => {
    const targetElement = args.element;
    const treeInstance = treeRef.current.ej2_instances[0];
    const nodeData = treeInstance.getNode(targetElement.id);

    if (args.item.id === 'copy') {
      // Copy node data to clipboard
      setClipboard({
        sourceNode: nodeData,
        mode: 'copy'
      });
      console.log('Copied:', nodeData.text);
    } else if (args.item.id === 'paste' && clipboard) {
      // Paste node as child of target
      const sourceNode = clipboard.sourceNode;
      const newItem = {
        id: nextId,
        pid: nodeData.id,
        name: `${sourceNode.text} (copy)`,
        hasChild: sourceNode.hasChild
      };

      setTreeData(prev => {
        const updated = [...prev];
        const parent = updated.find(item => item.id === nodeData.id);
        if (parent) {
          parent.hasChild = true;
        }
        return [...updated, newItem];
      });

      setNextId(nextId + 1);
      console.log('Pasted:', newItem.name);
    }
  };

  const handleBeforeOpen = (args) => {
    // Disable paste if nothing to paste
    const pasteItem = args.items.find(item => item.id === 'paste');
    if (pasteItem) {
      pasteItem.disabled = !clipboard;
    }
  };

  return (
    <>
      <TreeViewComponent
        ref={treeRef}
        fields={{
          dataSource: treeData,
          id: 'id',
          parentID: 'pid',
          text: 'name',
          hasChildren: 'hasChild'
        }}
      />
      <ContextMenuComponent
        items={menuItems}
        target=".e-treeview .e-list-item"
        select={handleMenuSelect}
        beforeOpen={handleBeforeOpen}
      />
    </>
  );
}

export default CopyPasteOperation;
```

### Cut and Paste Implementation

```tsx
function CutPasteOperation() {
  const treeRef = useRef(null);
  const [treeData, setTreeData] = useState([
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' },
    { id: 3, name: 'Item 2' }
  ]);
  const [clipboard, setClipboard] = useState(null);

  const menuItems = [
    { text: 'Cut', id: 'cut', icon: 'e-icons e-cut' },
    { text: 'Paste', id: 'paste', icon: 'e-icons e-paste' }
  ];

  const handleMenuSelect = (args) => {
    const targetElement = args.element;
    const treeInstance = treeRef.current.ej2_instances[0];
    const nodeData = treeInstance.getNode(targetElement.id);

    if (args.item.id === 'cut') {
      // Cut node - mark for move
      setClipboard({
        sourceNode: nodeData,
        mode: 'cut'
      });
      // Visual indication
      targetElement.style.opacity = '0.5';
      console.log('Cut:', nodeData.text);
    } else if (args.item.id === 'paste' && clipboard) {
      const sourceNode = clipboard.sourceNode;
      
      if (clipboard.mode === 'cut') {
        // Move node
        setTreeData(prev => {
          const updated = prev.map(item => {
            if (item.id === sourceNode.id) {
              return { ...item, pid: nodeData.id };
            }
            return item;
          });

          // Update source parent
          const sourceParent = updated.find(item => item.id === sourceNode.pid);
          if (sourceParent) {
            const hasOtherChildren = updated.some(
              item => item.pid === sourceParent.id && item.id !== sourceNode.id
            );
            if (!hasOtherChildren) {
              sourceParent.hasChild = false;
            }
          }

          // Update target to show children
          const targetParent = updated.find(item => item.id === nodeData.id);
          if (targetParent) {
            targetParent.hasChild = true;
          }

          return updated;
        });
      }

      setClipboard(null);
      console.log('Pasted to:', nodeData.text);
    }
  };

  return (
    <>
      <TreeViewComponent
        ref={treeRef}
        fields={{
          dataSource: treeData,
          id: 'id',
          parentID: 'pid',
          text: 'name',
          hasChildren: 'hasChild'
        }}
      />
      <ContextMenuComponent
        items={menuItems}
        target=".e-treeview .e-list-item"
        select={handleMenuSelect}
      />
    </>
  );
}

export default CutPasteOperation;
```

---

## Data Coordination

### Managing Coordinated State

```tsx
function CoordinatedTreeAndMenu() {
  const treeRef = useRef(null);
  const contextMenuRef = useRef(null);
  const [selectedNodeId, setSelectedNodeId] = useState(null);
  const [operationInProgress, setOperationInProgress] = useState(false);

  const data = [
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' }
  ];

  const menuItems = [
    { text: 'Expand', id: 'expand', icon: 'e-icons e-expand' },
    { text: 'Collapse', id: 'collapse', icon: 'e-icons e-collapse' }
  ];

  const handleNodeClicked = (args) => {
    setSelectedNodeId(args.nodeData.id);
  };

  const handleMenuSelect = (args) => {
    setOperationInProgress(true);

    try {
      const treeInstance = treeRef.current.ej2_instances[0];
      const targetElement = args.element;

      if (args.item.id === 'expand') {
        treeInstance.expandAll([targetElement.id]);
      } else if (args.item.id === 'collapse') {
        treeInstance.collapseAll([targetElement.id]);
      }
    } finally {
      setOperationInProgress(false);
    }
  };

  const handleBeforeOpen = (args) => {
    // Update UI state based on target
    const treeInstance = treeRef.current.ej2_instances[0];
    const nodeData = treeInstance.getNode(args.element.id);
    setSelectedNodeId(nodeData.id);
  };

  return (
    <>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
        nodeClicked={handleNodeClicked}
        cssClass={operationInProgress ? 'operation-in-progress' : ''}
      />
      <ContextMenuComponent
        ref={contextMenuRef}
        items={menuItems}
        target=".e-treeview .e-list-item"
        select={handleMenuSelect}
        beforeOpen={handleBeforeOpen}
      />
      <div>Selected: {selectedNodeId}</div>
    </>
  );
}

export default CoordinatedTreeAndMenu;
```

---

## Menu Items with Icons

### Icon Configuration

```tsx
function MenuItemsWithIcons() {
  const menuItems = [
    {
      text: 'Add Item',
      id: 'add',
      icon: 'e-icons e-plus',
      title: 'Add new item'
    },
    {
      text: 'Edit Item',
      id: 'edit',
      icon: 'e-icons e-edit',
      title: 'Edit selected item'
    },
    {
      text: 'Delete Item',
      id: 'delete',
      icon: 'e-icons e-trash',
      title: 'Delete selected item'
    },
    {
      text: 'Refresh',
      id: 'refresh',
      icon: 'e-icons e-refresh',
      title: 'Refresh tree'
    }
  ];

  return (
    <ContextMenuComponent
      items={menuItems}
      target=".e-treeview .e-list-item"
      showIcon={true}
      cssClass="icon-menu"
    />
  );
}

export default MenuItemsWithIcons;
```

### Custom Icon Styling

```css
.icon-menu .e-menu-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.icon-menu .e-icons {
  font-size: 16px;
  min-width: 20px;
  text-align: center;
}

.icon-menu .e-icons.e-plus {
  color: #4caf50;
}

.icon-menu .e-icons.e-edit {
  color: #2196f3;
}

.icon-menu .e-icons.e-trash {
  color: #f44336;
}

.icon-menu .e-icons.e-refresh {
  color: #ff9800;
}

.icon-menu .e-menu-item:hover {
  background-color: #f5f5f5;
}
```

---

## Separators and Submenus

### Using Separators

```tsx
function MenuWithSeparators() {
  const menuItems = [
    { text: 'New', id: 'new', icon: 'e-icons e-plus' },
    { text: 'Open', id: 'open', icon: 'e-icons e-open' },
    { separator: true }, // Separator
    { text: 'Edit', id: 'edit', icon: 'e-icons e-edit' },
    { text: 'Delete', id: 'delete', icon: 'e-icons e-trash' },
    { separator: true },
    { text: 'Properties', id: 'props', icon: 'e-icons e-info' }
  ];

  return (
    <ContextMenuComponent
      items={menuItems}
      target=".e-treeview .e-list-item"
      showIcon={true}
    />
  );
}

export default MenuWithSeparators;
```

### Submenu Implementation

```tsx
function MenuWithSubmenus() {
  const menuItems = [
    {
      text: 'New',
      id: 'new',
      icon: 'e-icons e-plus',
      items: [
        { text: 'Folder', id: 'new-folder' },
        { text: 'File', id: 'new-file' }
      ]
    },
    {
      text: 'Open',
      id: 'open',
      icon: 'e-icons e-open'
    },
    { separator: true },
    {
      text: 'Transform',
      id: 'transform',
      icon: 'e-icons e-transform',
      items: [
        { text: 'Uppercase', id: 'uppercase' },
        { text: 'Lowercase', id: 'lowercase' },
        { text: 'Capitalize', id: 'capitalize' }
      ]
    }
  ];

  return (
    <ContextMenuComponent
      items={menuItems}
      target=".e-treeview .e-list-item"
      showIcon={true}
    />
  );
}

export default MenuWithSubmenus;
```

---

## Custom Menu Styling

### Menu CSS Customization

```tsx
function StyledContextMenu() {
  const menuItems = [
    { text: 'Add', id: 'add', icon: 'e-icons e-plus' },
    { text: 'Edit', id: 'edit', icon: 'e-icons e-edit' },
    { text: 'Delete', id: 'delete', icon: 'e-icons e-trash' }
  ];

  return (
    <ContextMenuComponent
      items={menuItems}
      target=".e-treeview .e-list-item"
      cssClass="custom-styled-menu"
      showIcon={true}
    />
  );
}

export default StyledContextMenu;
```

```css
.custom-styled-menu {
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border: 1px solid #e0e0e0;
  background: linear-gradient(to bottom, #ffffff, #fafafa);
}

.custom-styled-menu .e-menu-item {
  padding: 10px 16px;
  color: #212121;
  font-size: 14px;
  transition: all 0.2s ease;
  border-left: 4px solid transparent;
}

.custom-styled-menu .e-menu-item:hover {
  background-color: #e3f2fd;
  border-left-color: #1976d2;
  color: #1565c0;
}

.custom-styled-menu .e-menu-item.e-focused {
  background-color: #bbdefb;
  color: #0d47a1;
}

.custom-styled-menu .e-icons {
  margin-right: 8px;
  font-size: 16px;
}

.custom-styled-menu .e-separator {
  margin: 4px 0;
  height: 1px;
  background-color: #e0e0e0;
}

/* Submenu styling */
.custom-styled-menu .e-ul {
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
```

---

## Dynamic Menu Items

### Generating Menu Items Based on Node Type

```tsx
function DynamicMenuGeneration() {
  const treeRef = useRef(null);
  const [menuItems, setMenuItems] = useState([
    { text: 'Add', id: 'add', icon: 'e-icons e-plus' }
  ]);

  const data = [
    { id: 1, name: 'Folder', type: 'folder', hasChild: true },
    { id: 2, pid: 1, name: 'Document.pdf', type: 'pdf' },
    { id: 3, name: 'Image.jpg', type: 'image' }
  ];

  const generateMenuItems = (nodeData) => {
    const items = [];

    // Common items
    items.push({ text: 'Edit', id: 'edit', icon: 'e-icons e-edit' });
    items.push({ text: 'Delete', id: 'delete', icon: 'e-icons e-trash' });
    items.push({ separator: true });

    // Type-specific items
    if (nodeData.type === 'folder') {
      items.push({ text: 'Add Item', id: 'add', icon: 'e-icons e-plus' });
      items.push({ text: 'Compress', id: 'compress', icon: 'e-icons e-compress' });
    } else if (nodeData.type === 'pdf') {
      items.push({ text: 'Open in Viewer', id: 'open-viewer' });
      items.push({ text: 'Print', id: 'print', icon: 'e-icons e-print' });
    } else if (nodeData.type === 'image') {
      items.push({ text: 'Preview', id: 'preview' });
      items.push({ text: 'Rotate', id: 'rotate', icon: 'e-icons e-rotate' });
    }

    return items;
  };

  const handleBeforeOpen = (args) => {
    const treeInstance = treeRef.current.ej2_instances[0];
    const nodeData = treeInstance.getNode(args.element.id);
    
    if (nodeData) {
      const dynamicItems = generateMenuItems(nodeData);
      setMenuItems(dynamicItems);
    }
  };

  return (
    <>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      />
      <ContextMenuComponent
        items={menuItems}
        target=".e-treeview .e-list-item"
        beforeOpen={handleBeforeOpen}
        showIcon={true}
      />
    </>
  );
}

export default DynamicMenuGeneration;
```

---

## Real-World Patterns

### File Manager Context Menu

```tsx
function FileManagerContextMenu() {
  const treeRef = useRef(null);
  const [treeData, setTreeData] = useState([
    { id: 1, name: 'Documents', type: 'folder', hasChild: true },
    { id: 2, pid: 1, name: 'Resume.pdf', type: 'file' },
    { id: 3, pid: 1, name: 'Cover.docx', type: 'file' },
    { id: 4, name: 'Downloads', type: 'folder', hasChild: true }
  ]);

  const menuItems = [
    { text: 'New', id: 'new', icon: 'e-icons e-plus', items: [
      { text: 'Folder', id: 'new-folder' },
      { text: 'File', id: 'new-file' }
    ]},
    { separator: true },
    { text: 'Rename', id: 'rename', icon: 'e-icons e-rename' },
    { text: 'Cut', id: 'cut', icon: 'e-icons e-cut' },
    { text: 'Copy', id: 'copy', icon: 'e-icons e-copy' },
    { text: 'Paste', id: 'paste', icon: 'e-icons e-paste' },
    { separator: true },
    { text: 'Delete', id: 'delete', icon: 'e-icons e-trash' },
    { separator: true },
    { text: 'Properties', id: 'properties', icon: 'e-icons e-info' }
  ];

  const handleMenuSelect = (args) => {
    const targetElement = args.element;
    const treeInstance = treeRef.current.ej2_instances[0];
    const nodeData = treeInstance.getNode(targetElement.id);

    console.log(`Action: ${args.item.id} on ${nodeData.text}`);
  };

  return (
    <>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: treeData, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      />
      <ContextMenuComponent
        items={menuItems}
        target=".e-treeview .e-list-item"
        select={handleMenuSelect}
        showIcon={true}
      />
    </>
  );
}

export default FileManagerContextMenu;
```

---

## Performance Optimization

### Debouncing Menu Operations

```tsx
function OptimizedContextMenu() {
  const treeRef = useRef(null);
  const pendingOperationRef = useRef(null);

  const data = [
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' }
  ];

  const menuItems = [
    { text: 'Action', id: 'action' }
  ];

  const debouncedMenuSelect = (args, delay = 300) => {
    if (pendingOperationRef.current) {
      clearTimeout(pendingOperationRef.current);
    }

    pendingOperationRef.current = setTimeout(() => {
      console.log('Menu action executed:', args.item.id);
      // Perform menu operation
    }, delay);
  };

  const handleMenuSelect = (args) => {
    debouncedMenuSelect(args);
  };

  return (
    <>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      />
      <ContextMenuComponent
        items={menuItems}
        target=".e-treeview .e-list-item"
        select={handleMenuSelect}
      />
    </>
  );
}

export default OptimizedContextMenu;
```

---

## Troubleshooting

### Menu Not Appearing

```tsx
// Ensure target selector matches TreeView elements
function DebugContextMenu() {
  const treeRef = useRef(null);

  useEffect(() => {
    // Verify TreeView has correct class
    const items = document.querySelectorAll('.e-treeview .e-list-item');
    console.log('TreeView items found:', items.length);
  }, []);

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
    />
  );
}
```

### Menu Items Disabled Unexpectedly

```tsx
// Check beforeOpen handler
const handleBeforeOpen = (args) => {
  console.log('beforeOpen - items:', args.items);
  // Verify item properties
  args.items.forEach(item => {
    console.log(`Item: ${item.text}, disabled: ${item.disabled}`);
  });
};
```

---

## Best Practices

### ✅ Do's

- Use `beforeOpen` to dynamically enable/disable items
- Provide visual feedback for operations
- Group related items with separators
- Use icons for better UX
- Coordinate menu state with TreeView
- Validate operations before executing
- Handle errors gracefully

### ❌ Don'ts

- Avoid complex operations in event handlers
- Don't disable all items without reason
- Avoid menu items that don't apply to current node
- Don't forget to handle loading states
- Avoid duplicate context menus
- Don't modify data without updating TreeView

### Performance Tips

1. Memoize menu item generation
2. Use event delegation
3. Debounce rapid operations
4. Cache node references
5. Lazy-load menu items
