# Inline Editing in Syncfusion React TreeView

## Table of Contents
1. [Overview](#overview)
2. [Enabling Inline Editing](#enabling-inline-editing)
3. [Edit Triggers](#edit-triggers)
4. [Edit Events](#edit-events)
5. [Input Validation During Editing](#input-validation-during-editing)
6. [Confirm and Cancel Edit](#confirm-and-cancel-edit)
7. [BeforeEdit Event for Validation](#beforeedit-event-for-validation)
8. [AfterEdit Event for Save](#afteredit-event-for-save)
9. [Preventing Edit Operations](#preventing-edit-operations)
10. [Edit Methods](#edit-methods)
11. [Edit with Validation Examples](#edit-with-validation-examples)
12. [Text Input Sanitization](#text-input-sanitization)
13. [Server-Side Validation](#server-side-validation)
14. [Real-World Examples](#real-world-examples)
15. [Troubleshooting](#troubleshooting)

---

## Overview

Inline editing allows users to directly modify tree node text without navigating to separate dialogs. Syncfusion React TreeView provides:
- Multiple edit triggers (double-click, F2 key, programmatic)
- Full event lifecycle with validation hooks
- Confirmation and cancellation controls
- Input sanitization capabilities
- Server-side validation integration
- Custom edit behaviors

---

## Enabling Inline Editing

### Basic Inline Editing Setup

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Desktop' },
  { id: '02', name: 'Documents', parentID: '01' },
  { id: '03', name: 'Resume.docx', parentID: '02' },
  { id: '04', name: 'CoverLetter.docx', parentID: '02' }
];

export default function BasicInlineEditingExample() {
  const treeRef = useRef(null);

  const handleNodeEdited = (args) => {
    console.log('Node edited:', {
      node: args.node,
      oldText: args.oldText,
      newText: args.newText
    });
  };

  return (
    <div>
      <p>Double-click a node to edit, or press F2 when a node is selected</p>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
        allowEditing={true}
        nodeEdited={handleNodeEdited}
      />
    </div>
  );
}
```

### Edit with Custom Styling

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';
import './inline-edit.css';

const data = [
  { id: '01', name: 'Project Name' },
  { id: '02', name: 'Task 1', parentID: '01' },
  { id: '03', name: 'Task 2', parentID: '01' }
];

export default function StyledEditingExample() {
  const treeRef = useRef(null);

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
      allowEditing={true}
      cssClass="custom-inline-edit"
    />
  );
}
```

```css
/* inline-edit.css */
.custom-inline-edit .e-input {
  border: 2px solid #2196F3;
  border-radius: 4px;
  padding: 6px;
  font-size: 14px;
}

.custom-inline-edit .e-input:focus {
  box-shadow: 0 0 8px rgba(33, 150, 243, 0.5);
  outline: none;
}

.custom-inline-edit .e-list-item.e-editing > .e-full-row {
  background-color: #F5F5F5;
  border-left: 3px solid #2196F3;
}
```

---

## Edit Triggers

### Double-Click to Edit

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Click me twice to edit' },
  { id: '02', name: 'Try me too', parentID: '01' },
  { id: '03', name: 'Or edit me', parentID: '01' }
];

export default function DoubleClickEditExample() {
  const treeRef = useRef(null);

  const handleNodeEditing = (args) => {
    console.log('Edit started by double-click on:', args.node?.textContent);
  };

  return (
    <div>
      <p>Double-click any node to start editing</p>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
        allowEditing={true}
        nodeEditing={handleNodeEditing}
      />
    </div>
  );
}
```

### F2 Key to Edit

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Select and press F2' },
  { id: '02', name: 'Or double-click', parentID: '01' },
  { id: '03', name: 'Both work', parentID: '01' }
];

export default function F2EditExample() {
  const treeRef = useRef(null);

  const handleKeyDown = (e) => {
    // F2 key - edit current selection
    if (e.key === 'F2') {
      const selectedNode = treeRef.current?.getSelectedNode();
      if (selectedNode) {
        treeRef.current?.beginEdit(selectedNode);
      }
    }
  };

  React.useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <div>
      <p>Select a node and press F2 to edit</p>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
        allowEditing={true}
      />
    </div>
  );
}
```

### Programmatic Edit Trigger

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Item 1' },
  { id: '02', name: 'Item 2', parentID: '01' },
  { id: '03', name: 'Item 3', parentID: '01' }
];

export default function ProgrammaticEditExample() {
  const treeRef = useRef(null);

  const startEditingNode = (nodeId) => {
    const node = treeRef.current?.getNode(nodeId);
    if (node) {
      treeRef.current?.beginEdit(node);
    }
  };

  const startEditingSelected = () => {
    const selectedNode = treeRef.current?.getSelectedNode();
    if (selectedNode) {
      treeRef.current?.beginEdit(selectedNode);
    }
  };

  return (
    <div>
      <button onClick={startEditingSelected}>Edit Selected Node</button>
      <button onClick={() => startEditingNode('02')}>Edit Item 2</button>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
        allowEditing={true}
      />
    </div>
  );
}
```

### Custom Edit Trigger with Button

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Project', expanded: true },
  { id: '02', name: 'Task 1', parentID: '01' },
  { id: '03', name: 'Task 2', parentID: '01' }
];

export default function CustomEditTriggerExample() {
  const treeRef = useRef(null);
  const [editingNodeId, setEditingNodeId] = useState(null);

  const handleNodeSelected = (args) => {
    setEditingNodeId(args.node?.getAttribute('data-uid'));
  };

  const triggerEdit = () => {
    if (editingNodeId) {
      const node = treeRef.current?.getNode(editingNodeId);
      treeRef.current?.beginEdit(node);
    } else {
      alert('Please select a node first');
    }
  };

  return (
    <div>
      <button onClick={triggerEdit}>Rename Selected</button>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
        allowEditing={true}
        nodeSelected={handleNodeSelected}
      />
    </div>
  );
}
```

---

## Edit Events

### nodeEditing Event - Before Edit Starts

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Editable Item' },
  { id: '02', name: 'Read-Only Item', readOnly: true },
  { id: '03', name: 'System Item', system: true }
];

export default function NodeEditingEventExample() {
  const treeRef = useRef(null);

  const handleNodeEditing = (args) => {
    const nodeData = data.find(d => d.id === args.node?.getAttribute('data-uid'));

    // Prevent editing read-only items
    if (nodeData?.readOnly) {
      args.cancel = true;
      console.log('Cannot edit read-only item');
      return;
    }

    // Prevent editing system items
    if (nodeData?.system) {
      args.cancel = true;
      alert('System items cannot be edited');
      return;
    }

    console.log('Edit allowed for:', nodeData?.name);
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
      allowEditing={true}
      nodeEditing={handleNodeEditing}
    />
  );
}
```

### nodeEdited Event - After Edit Completes

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const initialData = [
  { id: '01', name: 'Project Alpha' },
  { id: '02', name: 'Task 1', parentID: '01' },
  { id: '03', name: 'Task 2', parentID: '01' }
];

export default function NodeEditedEventExample() {
  const treeRef = useRef(null);
  const [editHistory, setEditHistory] = useState([]);
  const [treeData, setTreeData] = useState(initialData);

  const handleNodeEdited = (args) => {
    const nodeId = args.node?.getAttribute('data-uid');
    const oldName = args.oldText;
    const newName = args.newText;

    // Update data
    const updated = treeData.map(item =>
      item.id === nodeId ? { ...item, name: newName } : item
    );
    setTreeData(updated);

    // Log edit history
    const editEntry = {
      timestamp: new Date().toLocaleTimeString(),
      nodeId,
      oldName,
      newName,
      status: 'completed'
    };
    setEditHistory([...editHistory, editEntry]);

    console.log('Edit completed:', editEntry);
  };

  return (
    <div>
      <div style={{ marginBottom: '20px' }}>
        <h3>Edit History</h3>
        <ul>
          {editHistory.map((entry, i) => (
            <li key={i}>
              [{entry.timestamp}] "{entry.oldName}" → "{entry.newName}"
            </li>
          ))}
        </ul>
      </div>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: treeData, id: 'id', text: 'name', parentID: 'parentID' }}
        allowEditing={true}
        nodeEdited={handleNodeEdited}
      />
    </div>
  );
}
```

---

## Input Validation During Editing

### Real-Time Character Validation

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Item1', pattern: 'alphanumeric' },
  { id: '02', name: 'item_2', parentID: '01', pattern: 'alphanumeric_underscore' },
  { id: '03', name: 'item-3', parentID: '01', pattern: 'alphanumeric_dash' }
];

export default function RealTimeValidationExample() {
  const treeRef = useRef(null);
  const inputRef = useRef(null);

  const getPattern = (nodeData) => {
    switch (nodeData?.pattern) {
      case 'alphanumeric':
        return /^[a-zA-Z0-9]*$/;
      case 'alphanumeric_underscore':
        return /^[a-zA-Z0-9_]*$/;
      case 'alphanumeric_dash':
        return /^[a-zA-Z0-9-]*$/;
      default:
        return /^.*/;
    }
  };

  const handleNodeEditing = (args) => {
    const nodeData = data.find(d => d.id === args.node?.getAttribute('data-uid'));
    const pattern = getPattern(nodeData);

    // Create input with validation
    setTimeout(() => {
      const input = args.node?.querySelector('input');
      if (input) {
        input.addEventListener('input', (e) => {
          if (!pattern.test(e.target.value)) {
            e.target.style.borderColor = 'red';
            e.target.title = `Pattern: ${nodeData?.pattern}`;
          } else {
            e.target.style.borderColor = 'green';
          }
        });
      }
    }, 0);
  };

  return (
    <div>
      <p>Try editing with pattern constraints</p>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
        allowEditing={true}
        nodeEditing={handleNodeEditing}
      />
    </div>
  );
}
```

### Length Validation

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Short Name', maxLength: 10 },
  { id: '02', name: 'Very Long Item Name', parentID: '01', maxLength: 30 },
  { id: '03', name: 'Medium', parentID: '01', maxLength: 15 }
];

export default function LengthValidationExample() {
  const treeRef = useRef(null);

  const handleNodeEditing = (args) => {
    const nodeData = data.find(d => d.id === args.node?.getAttribute('data-uid'));
    const maxLength = nodeData?.maxLength || 50;

    setTimeout(() => {
      const input = args.node?.querySelector('input');
      if (input) {
        input.maxLength = maxLength;
        input.placeholder = `Max ${maxLength} characters`;
        
        input.addEventListener('input', (e) => {
          const remaining = maxLength - e.target.value.length;
          e.target.title = `${remaining} characters remaining`;
        });
      }
    }, 0);
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
      allowEditing={true}
      nodeEditing={handleNodeEditing}
    />
  );
}
```

### Unique Name Validation

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const initialData = [
  { id: '01', name: 'Documents' },
  { id: '02', name: 'Photos', parentID: '01' },
  { id: '03', name: 'Videos', parentID: '01' }
];

export default function UniqueNameValidationExample() {
  const treeRef = useRef(null);
  const [treeData] = React.useState(initialData);

  const isNameUnique = (newName, excludeId) => {
    return !treeData.some(item => 
      item.name.toLowerCase() === newName.toLowerCase() && item.id !== excludeId
    );
  };

  const handleNodeEditing = (args) => {
    setTimeout(() => {
      const input = args.node?.querySelector('input');
      if (input) {
        input.addEventListener('input', (e) => {
          if (!isNameUnique(e.target.value, args.node?.getAttribute('data-uid'))) {
            e.target.style.borderColor = 'red';
            e.target.title = 'Name already exists';
          } else {
            e.target.style.borderColor = 'green';
          }
        });
      }
    }, 0);
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: treeData, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
      allowEditing={true}
      nodeEditing={handleNodeEditing}
    />
  );
}
```

---

## Confirm and Cancel Edit

### Enter Key to Confirm

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Double-click to edit' },
  { id: '02', name: 'Press Enter to save', parentID: '01' },
  { id: '03', name: 'Press Escape to cancel', parentID: '01' }
];

export default function ConfirmEditExample() {
  const treeRef = useRef(null);

  const handleNodeEditing = (args) => {
    setTimeout(() => {
      const input = args.node?.querySelector('input');
      if (input) {
        input.focus();
        input.addEventListener('keydown', (e) => {
          if (e.key === 'Enter') {
            e.preventDefault();
            treeRef.current?.endEdit();
            console.log('Edit confirmed');
          }
        });
      }
    }, 0);
  };

  return (
    <div>
      <p>Enter = Save, Escape = Cancel</p>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
        allowEditing={true}
        nodeEditing={handleNodeEditing}
      />
    </div>
  );
}
```

### Escape Key to Cancel

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Edit me' },
  { id: '02', name: 'Press Escape to cancel', parentID: '01' },
  { id: '03', name: 'Or click outside', parentID: '01' }
];

export default function CancelEditExample() {
  const treeRef = useRef(null);

  const handleNodeEditing = (args) => {
    setTimeout(() => {
      const input = args.node?.querySelector('input');
      if (input) {
        input.addEventListener('keydown', (e) => {
          if (e.key === 'Escape') {
            e.preventDefault();
            // Cancel edit by ending without saving
            const selectedNode = treeRef.current?.getSelectedNode();
            treeRef.current?.clearSelection();
            treeRef.current?.selectNodes([selectedNode]);
            console.log('Edit cancelled');
          }
        });
      }
    }, 0);
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
      allowEditing={true}
      nodeEditing={handleNodeEditing}
    />
  );
}
```

### Blur to Confirm Automatically

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Item 1' },
  { id: '02', name: 'Item 2', parentID: '01' }
];

export default function BlurConfirmExample() {
  const treeRef = useRef(null);
  const [confirmMode, setConfirmMode] = useState('blur'); // blur, manual

  const handleNodeEditing = (args) => {
    setTimeout(() => {
      const input = args.node?.querySelector('input');
      if (input) {
        input.focus();

        if (confirmMode === 'blur') {
          // Auto-confirm on blur
          input.addEventListener('blur', () => {
            treeRef.current?.endEdit();
          });
        } else {
          // Manual confirmation
          input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
              treeRef.current?.endEdit();
            } else if (e.key === 'Escape') {
              // Cancel without saving
            }
          });
        }
      }
    }, 0);
  };

  return (
    <div>
      <label>
        <input
          type="radio"
          checked={confirmMode === 'blur'}
          onChange={() => setConfirmMode('blur')}
        />
        Auto-confirm on blur
      </label>
      <label>
        <input
          type="radio"
          checked={confirmMode === 'manual'}
          onChange={() => setConfirmMode('manual')}
        />
        Manual (Enter/Escape)
      </label>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
        allowEditing={true}
        nodeEditing={handleNodeEditing}
      />
    </div>
  );
}
```

---

## BeforeEdit Event for Validation

### Advanced Pre-Edit Validation

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'System Folder', system: true },
  { id: '02', name: 'User Folder', system: false },
  { id: '03', name: 'Read-Only', system: false, readOnly: true }
];

export default function BeforeEditValidationExample() {
  const treeRef = useRef(null);

  const canEditNode = (nodeData) => {
    // Check if system file
    if (nodeData?.system) {
      return { allowed: false, reason: 'System files cannot be edited' };
    }

    // Check if read-only
    if (nodeData?.readOnly) {
      return { allowed: false, reason: 'This item is read-only' };
    }

    return { allowed: true };
  };

  const handleNodeEditing = (args) => {
    const nodeId = args.node?.getAttribute('data-uid');
    const nodeData = data.find(d => d.id === nodeId);

    const validation = canEditNode(nodeData);
    if (!validation.allowed) {
      args.cancel = true;
      alert(validation.reason);
    }
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
      allowEditing={true}
      nodeEditing={handleNodeEditing}
    />
  );
}
```

---

## AfterEdit Event for Save

### Save Changes to Backend

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Folder A' },
  { id: '02', name: 'File 1.txt', parentID: '01' },
  { id: '03', name: 'File 2.txt', parentID: '01' }
];

export default function SaveToBackendExample() {
  const treeRef = useRef(null);
  const [saveStatus, setSaveStatus] = useState('');

  const saveChange = async (nodeId, oldName, newName) => {
    try {
      setSaveStatus('Saving...');
      
      // Simulated API call
      const response = await fetch('/api/rename-node', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nodeId,
          oldName,
          newName,
          timestamp: new Date().toISOString()
        })
      });

      if (response.ok) {
        setSaveStatus('Saved successfully');
        setTimeout(() => setSaveStatus(''), 3000);
      } else {
        setSaveStatus('Save failed');
        throw new Error('Save failed');
      }
    } catch (error) {
      setSaveStatus(`Error: ${error.message}`);
      console.error('Save error:', error);
    }
  };

  const handleNodeEdited = (args) => {
    const nodeId = args.node?.getAttribute('data-uid');
    saveChange(nodeId, args.oldText, args.newText);
  };

  return (
    <div>
      <div style={{ 
        padding: '10px', 
        backgroundColor: '#E8F5E9', 
        marginBottom: '10px',
        borderRadius: '4px'
      }}>
        {saveStatus || 'Ready'}
      </div>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
        allowEditing={true}
        nodeEdited={handleNodeEdited}
      />
    </div>
  );
}
```

### Rollback on Save Failure

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function RollbackOnFailureExample() {
  const treeRef = useRef(null);
  const originalNameRef = useRef('');

  const handleNodeEditing = (args) => {
    // Store original name before edit
    originalNameRef.current = args.node?.textContent;
  };

  const handleNodeEdited = async (args) => {
    const nodeId = args.node?.getAttribute('data-uid');
    const newName = args.newText;

    try {
      // Try to save
      const response = await fetch('/api/rename-node', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nodeId, newName })
      });

      if (!response.ok) {
        throw new Error('Save failed');
      }
    } catch (error) {
      console.error('Rollback needed:', error);
      
      // Rollback by reverting the node text
      const node = treeRef.current?.getNode(nodeId);
      if (node) {
        node.textContent = originalNameRef.current;
      }

      alert('Save failed. Changes have been reverted.');
    }
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
      allowEditing={true}
      nodeEditing={handleNodeEditing}
      nodeEdited={handleNodeEdited}
    />
  );
}
```

---

## Preventing Edit Operations

### Disable Editing for Specific Users

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Content A' },
  { id: '02', name: 'Content B', parentID: '01' }
];

export default function UserPermissionEditExample() {
  const treeRef = useRef(null);
  const [userRole, setUserRole] = useState('viewer');

  const canEdit = (role) => {
    return ['editor', 'admin'].includes(role);
  };

  const handleNodeEditing = (args) => {
    if (!canEdit(userRole)) {
      args.cancel = true;
      alert(`Role "${userRole}" cannot edit nodes`);
    }
  };

  return (
    <div>
      <select value={userRole} onChange={(e) => setUserRole(e.target.value)}>
        <option value="viewer">Viewer</option>
        <option value="editor">Editor</option>
        <option value="admin">Admin</option>
      </select>
      <p>Current role: {userRole}</p>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
        allowEditing={true}
        nodeEditing={handleNodeEditing}
      />
    </div>
  );
}
```

### Disable Editing During Certain Hours

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function TimeRestrictedEditExample() {
  const treeRef = useRef(null);

  const isEditingAllowed = () => {
    const now = new Date();
    const hour = now.getHours();
    
    // Allow editing only during business hours (9 AM - 5 PM)
    return hour >= 9 && hour < 17;
  };

  const handleNodeEditing = (args) => {
    if (!isEditingAllowed()) {
      args.cancel = true;
      alert('Editing is only allowed during business hours (9 AM - 5 PM)');
    }
  };

  return (
    <div>
      <p>Editing allowed: {isEditingAllowed() ? 'Yes' : 'No'}</p>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
        allowEditing={true}
        nodeEditing={handleNodeEditing}
      />
    </div>
  );
}
```

---

## Edit Methods

### beginEdit() Method

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Item 1' },
  { id: '02', name: 'Item 2', parentID: '01' },
  { id: '03', name: 'Item 3', parentID: '01' }
];

export default function BeginEditExample() {
  const treeRef = useRef(null);

  const editNode = (nodeId) => {
    const node = treeRef.current?.getNode(nodeId);
    if (node) {
      treeRef.current?.beginEdit(node);
      console.log('Edit started for node:', nodeId);
    }
  };

  const editSelected = () => {
    const selectedNode = treeRef.current?.getSelectedNode();
    if (selectedNode) {
      treeRef.current?.beginEdit(selectedNode);
    } else {
      alert('Please select a node first');
    }
  };

  return (
    <div>
      <button onClick={editSelected}>Edit Selected</button>
      <button onClick={() => editNode('02')}>Edit Item 2</button>
      <button onClick={() => editNode('03')}>Edit Item 3</button>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
        allowEditing={true}
      />
    </div>
  );
}
```

### endEdit() Method

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Item 1' },
  { id: '02', name: 'Item 2', parentID: '01' },
  { id: '03', name: 'Item 3', parentID: '01' }
];

export default function EndEditExample() {
  const treeRef = useRef(null);
  const [isEditing, setIsEditing] = useState(false);

  const handleNodeEditing = () => {
    setIsEditing(true);
  };

  const handleNodeEdited = () => {
    setIsEditing(false);
  };

  const confirmEdit = () => {
    treeRef.current?.endEdit();
  };

  const cancelEdit = () => {
    // Clicking outside or pressing Escape cancels
    setIsEditing(false);
  };

  return (
    <div>
      {isEditing && (
        <div>
          <button onClick={confirmEdit}>Save</button>
          <button onClick={cancelEdit}>Cancel</button>
        </div>
      )}
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
        allowEditing={true}
        nodeEditing={handleNodeEditing}
        nodeEdited={handleNodeEdited}
      />
    </div>
  );
}
```

---

## Edit with Validation Examples

### Complete Validation Workflow

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Documents', type: 'folder' },
  { id: '02', name: 'Resume.pdf', parentID: '01', type: 'file' },
  { id: '03', name: 'Photo.jpg', parentID: '01', type: 'file' }
];

export default function CompleteValidationWorkflowExample() {
  const treeRef = useRef(null);
  const [validationErrors, setValidationErrors] = useState({});

  const validateNewName = (newName, nodeType) => {
    const errors = [];

    // Empty check
    if (!newName || newName.trim() === '') {
      errors.push('Name cannot be empty');
    }

    // Length check
    if (newName.length > 50) {
      errors.push('Name cannot exceed 50 characters');
    }

    // Invalid characters
    if (/[<>:"|?*]/.test(newName)) {
      errors.push('Name contains invalid characters');
    }

    // Reserved names
    if (['CON', 'PRN', 'AUX', 'NUL'].includes(newName.toUpperCase())) {
      errors.push('Name is reserved and cannot be used');
    }

    // File extension validation
    if (nodeType === 'file' && !newName.includes('.')) {
      errors.push('File must have an extension');
    }

    return errors;
  };

  const handleNodeEditing = (args) => {
    const nodeData = data.find(d => d.id === args.node?.getAttribute('data-uid'));
  };

  const handleNodeEdited = (args) => {
    const nodeId = args.node?.getAttribute('data-uid');
    const nodeData = data.find(d => d.id === nodeId);
    const errors = validateNewName(args.newText, nodeData?.type);

    if (errors.length > 0) {
      setValidationErrors({ ...validationErrors, [nodeId]: errors });
      args.cancel = true;
      alert('Validation errors:\n' + errors.join('\n'));
    } else {
      setValidationErrors({ ...validationErrors, [nodeId]: [] });
    }
  };

  return (
    <div>
      {Object.entries(validationErrors).map(([nodeId, errors]) =>
        errors.length > 0 && (
          <div key={nodeId} style={{ color: 'red', marginBottom: '10px' }}>
            {errors.map(err => <div key={err}>• {err}</div>)}
          </div>
        )
      )}
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
        allowEditing={true}
        nodeEditing={handleNodeEditing}
        nodeEdited={handleNodeEdited}
      />
    </div>
  );
}
```

---

## Text Input Sanitization

### HTML and XSS Prevention

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function HTMLSanitizationExample() {
  const treeRef = useRef(null);

  const sanitizeInput = (input) => {
    // Remove potentially dangerous characters and HTML
    return input
      .replace(/[<>]/g, '')  // Remove angle brackets
      .replace(/javascript:/gi, '')  // Remove javascript protocol
      .replace(/on\w+\s*=/gi, '')  // Remove event handlers
      .trim();
  };

  const handleNodeEdited = (args) => {
    const sanitized = sanitizeInput(args.newText);
    
    if (sanitized !== args.newText) {
      // Update the node with sanitized text
      const node = args.node;
      node.textContent = sanitized;
      console.log('Input sanitized:', args.newText, '->', sanitized);
    }
  };

  return (
    <div>
      <p>Try entering HTML or script tags - they will be stripped</p>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
        allowEditing={true}
        nodeEdited={handleNodeEdited}
      />
    </div>
  );
}
```

### Special Character Handling

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function SpecialCharacterExample() {
  const treeRef = useRef(null);

  const sanitizeSpecialChars = (input) => {
    const specialChars = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;'
    };

    return input.replace(/[&<>"']/g, char => specialChars[char]);
  };

  const handleNodeEditing = (args) => {
    setTimeout(() => {
      const input = args.node?.querySelector('input');
      if (input) {
        input.addEventListener('input', (e) => {
          // Real-time preview
          const sanitized = sanitizeSpecialChars(e.target.value);
          if (sanitized !== e.target.value) {
            e.target.title = `Sanitized: ${sanitized}`;
          }
        });
      }
    }, 0);
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
      allowEditing={true}
      nodeEditing={handleNodeEditing}
    />
  );
}
```

### Trimming and Whitespace Handling

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function TrimWhitespaceExample() {
  const treeRef = useRef(null);

  const handleNodeEdited = (args) => {
    const trimmed = args.newText.trim();
    const multipleSpaces = /\s{2,}/g;
    const normalized = trimmed.replace(multipleSpaces, ' ');

    if (normalized !== args.newText) {
      args.node.textContent = normalized;
      console.log('Whitespace normalized');
    }
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
      allowEditing={true}
      nodeEdited={handleNodeEdited}
    />
  );
}
```

---

## Server-Side Validation

### API Validation Integration

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function ServerValidationExample() {
  const treeRef = useRef(null);
  const [validationErrors, setValidationErrors] = useState({});

  const validateOnServer = async (nodeId, newName) => {
    try {
      const response = await fetch('/api/validate-name', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nodeId,
          newName,
          timestamp: new Date().toISOString()
        })
      });

      const result = await response.json();
      return result.valid ? { valid: true } : { valid: false, errors: result.errors };
    } catch (error) {
      console.error('Validation error:', error);
      return { valid: false, errors: ['Server validation failed'] };
    }
  };

  const handleNodeEdited = async (args) => {
    const nodeId = args.node?.getAttribute('data-uid');
    const validation = await validateOnServer(nodeId, args.newText);

    if (!validation.valid) {
      args.cancel = true;
      setValidationErrors({ ...validationErrors, [nodeId]: validation.errors });
      alert('Validation failed:\n' + validation.errors.join('\n'));
    } else {
      setValidationErrors({ ...validationErrors, [nodeId]: [] });
    }
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
      allowEditing={true}
      nodeEdited={handleNodeEdited}
    />
  );
}
```

### Debounced Validation

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function DebouncedValidationExample() {
  const treeRef = useRef(null);
  const validationTimeoutRef = useRef(null);

  const debounceValidation = (nodeId, newName, callback) => {
    clearTimeout(validationTimeoutRef.current);
    
    validationTimeoutRef.current = setTimeout(async () => {
      try {
        const response = await fetch('/api/validate-name', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ nodeId, newName })
        });

        const result = await response.json();
        callback(result.valid, result.errors || []);
      } catch (error) {
        callback(false, ['Validation error']);
      }
    }, 500); // Wait 500ms after last keystroke
  };

  const handleNodeEditing = (args) => {
    setTimeout(() => {
      const input = args.node?.querySelector('input');
      if (input) {
        input.addEventListener('input', (e) => {
          const nodeId = args.node?.getAttribute('data-uid');
          debounceValidation(nodeId, e.target.value, (valid, errors) => {
            if (valid) {
              e.target.style.borderColor = 'green';
            } else {
              e.target.style.borderColor = 'red';
              e.target.title = errors.join(', ');
            }
          });
        });
      }
    }, 0);
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
      allowEditing={true}
      nodeEditing={handleNodeEditing}
    />
  );
}
```

---

## Real-World Examples

### Example 1: File Rename with Extension Protection

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const fileData = [
  { id: '01', name: 'Documents', type: 'folder' },
  { id: '02', name: 'report.pdf', parentID: '01', type: 'file', extension: '.pdf' },
  { id: '03', name: 'script.js', parentID: '01', type: 'file', extension: '.js' }
];

export default function FileRenameExample() {
  const treeRef = useRef(null);
  const [renameLog, setRenameLog] = useState([]);

  const handleNodeEdited = (args) => {
    const nodeId = args.node?.getAttribute('data-uid');
    const nodeData = fileData.find(d => d.id === nodeId);

    if (nodeData?.type === 'file') {
      // Ensure extension is preserved
      const baseName = args.newText.split('.')[0];
      const extension = nodeData?.extension;
      const fullName = baseName + extension;

      if (fullName !== args.newText) {
        args.node.textContent = fullName;
      }

      setRenameLog([...renameLog, {
        old: args.oldText,
        new: fullName,
        time: new Date().toLocaleTimeString()
      }]);
    }
  };

  return (
    <div style={{ display: 'flex', gap: '20px' }}>
      <div style={{ flex: 1 }}>
        <TreeViewComponent
          ref={treeRef}
          fields={{ dataSource: fileData, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
          allowEditing={true}
          nodeEdited={handleNodeEdited}
        />
      </div>
      <div style={{ flex: 1 }}>
        <h3>Rename Log</h3>
        {renameLog.map((log, i) => (
          <div key={i} style={{ fontSize: '12px', marginBottom: '5px' }}>
            {log.time}: "{log.old}" → "{log.new}"
          </div>
        ))}
      </div>
    </div>
  );
}
```

### Example 2: Dynamic Form Field Renaming

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const formData = [
  { id: '01', name: 'Form Fields', expanded: true },
  { id: '02', name: 'username', parentID: '01', required: true },
  { id: '03', name: 'email', parentID: '01', required: true },
  { id: '04', name: 'phone', parentID: '01', required: false }
];

export default function FormFieldRenameExample() {
  const treeRef = useRef(null);

  const handleNodeEdited = (args) => {
    const nodeId = args.node?.getAttribute('data-uid');
    const nodeData = formData.find(d => d.id === nodeId);

    // Validate field name format
    if (!/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(args.newText)) {
      args.node.textContent = args.oldText;
      alert('Field name must start with letter or underscore, contain only alphanumeric and underscores');
      return;
    }

    // Update form schema
    console.log(`Field renamed: ${args.oldText} → ${args.newText}`);
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: formData, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
      allowEditing={true}
      nodeEdited={handleNodeEdited}
    />
  );
}
```

### Example 3: Code Identifier Refactoring

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const codeStructure = [
  { id: '01', name: 'myFunction', type: 'function' },
  { id: '02', name: 'myVariable', type: 'variable' },
  { id: '03', name: 'MyClass', type: 'class' }
];

export default function CodeRefactoringExample() {
  const treeRef = useRef(null);

  const getNamingConvention = (type) => {
    switch (type) {
      case 'function': return /^[a-z][a-zA-Z0-9]*$/; // camelCase
      case 'variable': return /^[a-z_][a-zA-Z0-9_]*$/; // snake_case or camelCase
      case 'class': return /^[A-Z][a-zA-Z0-9]*$/; // PascalCase
      default: return /^.*/;
    }
  };

  const handleNodeEdited = (args) => {
    const nodeId = args.node?.getAttribute('data-uid');
    const nodeData = codeStructure.find(d => d.id === nodeId);
    const convention = getNamingConvention(nodeData?.type);

    if (!convention.test(args.newText)) {
      args.node.textContent = args.oldText;
      
      const expectedFormat = {
        function: 'camelCase (e.g., myFunction)',
        variable: 'snake_case or camelCase',
        class: 'PascalCase (e.g., MyClass)'
      };
      
      alert(`${nodeData?.type} must use ${expectedFormat[nodeData?.type] || 'valid format'}`);
    }
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: codeStructure, id: 'id', text: 'name', parentID: 'parentID' }}
      allowEditing={true}
      nodeEdited={handleNodeEdited}
    />
  );
}
```

---

## Troubleshooting

### Issue: Double-click not triggering edit

**Solution:** Ensure `allowEditing` is enabled:

```tsx
<TreeViewComponent
  allowEditing={true}  // Must be explicitly true
  fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
/>
```

### Issue: Changes not being saved

**Solution:** Implement `nodeEdited` event:

```tsx
const handleNodeEdited = (args) => {
  console.log('Old:', args.oldText);
  console.log('New:', args.newText);
  // Save the changes
};

<TreeViewComponent nodeEdited={handleNodeEdited} />
```

### Issue: Validation not working

**Solution:** Set `args.cancel = true` in event handler:

```tsx
const handleNodeEdited = (args) => {
  if (!isValid(args.newText)) {
    args.cancel = true;  // This reverts the change
  }
};
```

### Issue: Edit input not visible

**Solution:** Check z-index and CSS conflicts:

```tsx
<TreeViewComponent
  cssClass="custom-edit"
  allowEditing={true}
/>
```

```css
.custom-edit .e-input {
  z-index: 1000;
  position: relative;
}
```

---

## Best Practices

1. **Always validate input** - Prevent invalid data from being saved
2. **Provide clear error messages** - Help users understand what's wrong
3. **Use sanitization** - Prevent XSS and injection attacks
4. **Implement server-side validation** - Don't trust client-side validation alone
5. **Log all edits** - Essential for audit trails
6. **Provide undo/redo** - Better user experience
7. **Handle errors gracefully** - Rollback on server failure
8. **Use consistent naming rules** - Enforce standards automatically
9. **Provide keyboard shortcuts** - Improve accessibility
10. **Test edge cases** - Empty strings, special characters, very long names

