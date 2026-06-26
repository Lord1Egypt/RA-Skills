# Advanced Features in Syncfusion React TreeView

## Table of Contents
1. [Overview](#overview)
2. [Load-On-Demand with Lazy Loading](#load-on-demand-with-lazy-loading)
3. [Load-On-Demand with Caching](#load-on-demand-with-caching)
4. [State Persistence](#state-persistence)
5. [RTL Support and Localization](#rtl-support-and-localization)
6. [Accordion Pattern](#accordion-pattern)
7. [Virtual Scrolling for Large Datasets](#virtual-scrolling-for-large-datasets)
8. [Keyboard Shortcuts](#keyboard-shortcuts)
9. [Event Cancellation Patterns](#event-cancellation-patterns)
10. [Performance Optimization](#performance-optimization)
11. [Custom Sorting and Filtering](#custom-sorting-and-filtering)
12. [Tooltip Integration](#tooltip-integration)
13. [Dynamic Icon Changing](#dynamic-icon-changing)
14. [Custom CSS Classes](#custom-css-classes)
15. [Ripple Effects](#ripple-effects)
16. [Multi-Language Support](#multi-language-support)
17. [Real-World Patterns](#real-world-patterns)
18. [Best Practices](#best-practices)

---

## Overview

Advanced TreeView features enable sophisticated applications with lazy-loaded hierarchies, stateful interactions, internationalization, and optimized performance. These features support enterprise scenarios like real-time data updates, massive datasets, and complex user workflows.

---

## Load-On-Demand with Lazy Loading

### Basic Load-On-Demand

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const initialData = [
  { id: '01', name: 'Users', hasChildren: true },
  { id: '02', name: 'Documents', hasChildren: true },
  { id: '03', name: 'Settings', hasChildren: false }
];

export default function BasicLoadOnDemandExample() {
  const treeRef = useRef(null);
  const [treeData, setTreeData] = useState(initialData);
  const [loadedNodes, setLoadedNodes] = useState(new Set());

  const fetchChildrenFromAPI = async (parentId) => {
    // Simulate API call
    const mockChildren = {
      '01': [
        { id: '01-1', name: 'Admin Users', parentID: '01', hasChildren: true },
        { id: '01-2', name: 'Regular Users', parentID: '01', hasChildren: true }
      ],
      '02': [
        { id: '02-1', name: 'Personal', parentID: '02', hasChildren: false },
        { id: '02-2', name: 'Shared', parentID: '02', hasChildren: false }
      ]
    };

    // Simulate network delay
    return new Promise(resolve => {
      setTimeout(() => {
        resolve(mockChildren[parentId] || []);
      }, 500);
    });
  };

  const handleNodeExpanding = async (args) => {
    const nodeId = args.node?.getAttribute('data-uid');

    // Skip if already loaded
    if (loadedNodes.has(nodeId)) return;

    args.cancel = true; // Prevent default expansion until data loads

    try {
      const children = await fetchChildrenFromAPI(nodeId);
      
      // Add children to data
      setTreeData([...treeData, ...children]);
      setLoadedNodes(new Set([...loadedNodes, nodeId]));

      // Trigger expansion after data is loaded
      setTimeout(() => {
        const node = treeRef.current?.getNode(nodeId);
        if (node) {
          node.querySelector('.e-icons')?.classList.remove('e-icon-expandable');
          node.querySelector('.e-icons')?.classList.add('e-icon-collapsible');
        }
      }, 100);
    } catch (error) {
      console.error('Error loading children:', error);
      alert('Failed to load items');
    }
  };

  return (
    <div>
      <p>Expand nodes to load children on-demand from API</p>
      <TreeViewComponent
        ref={treeRef}
        fields={{ 
          dataSource: treeData, 
          id: 'id', 
          text: 'name', 
          parentID: 'parentID',
          hasChildren: 'hasChildren'
        }}
        nodeExpanding={handleNodeExpanding}
      />
    </div>
  );
}
```

### Load-On-Demand with Loading State

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function LoadOnDemandWithStateExample() {
  const treeRef = useRef(null);
  const [treeData, setTreeData] = useState([]);
  const [loadingNodes, setLoadingNodes] = useState(new Set());
  const [errorNodes, setErrorNodes] = useState(new Set());

  const handleNodeExpanding = async (args) => {
    const nodeId = args.node?.getAttribute('data-uid');
    
    args.cancel = true;
    setLoadingNodes(new Set([...loadingNodes, nodeId]));

    try {
      // Simulate API call with possible failure
      const response = await fetch(`/api/children/${nodeId}`);
      const children = await response.json();

      setTreeData([...treeData, ...children]);
      setLoadingNodes(prev => {
        const updated = new Set(prev);
        updated.delete(nodeId);
        return updated;
      });
    } catch (error) {
      setErrorNodes(new Set([...errorNodes, nodeId]));
      setLoadingNodes(prev => {
        const updated = new Set(prev);
        updated.delete(nodeId);
        return updated;
      });
    }
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: treeData, id: 'id', text: 'name', parentID: 'parentID' }}
      nodeExpanding={handleNodeExpanding}
    />
  );
}
```

### Hierarchical Load-On-Demand

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function HierarchicalLoadOnDemandExample() {
  const treeRef = useRef(null);
  const [treeData, setTreeData] = useState([
    { id: '01', name: 'Company', hasChildren: true }
  ]);
  const [nodeHierarchy, setNodeHierarchy] = useState({});

  const getLoadLevel = (parentId) => {
    let level = 0;
    let current = parentId;
    while (nodeHierarchy[current]) {
      level++;
      current = nodeHierarchy[current];
    }
    return level;
  };

  const handleNodeExpanding = async (args) => {
    const nodeId = args.node?.getAttribute('data-uid');
    const level = getLoadLevel(nodeId);

    args.cancel = true;

    try {
      // Load different data based on level
      const children = await fetch(`/api/hierarchy-level-${level}/${nodeId}`)
        .then(r => r.json());

      // Update hierarchy mapping
      const newHierarchy = { ...nodeHierarchy };
      children.forEach(child => {
        newHierarchy[child.id] = nodeId;
      });
      setNodeHierarchy(newHierarchy);

      setTreeData([...treeData, ...children]);
    } catch (error) {
      console.error('Load error:', error);
    }
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: treeData, id: 'id', text: 'name', parentID: 'parentID' }}
      nodeExpanding={handleNodeExpanding}
    />
  );
}
```

---

## Load-On-Demand with Caching

### Simple Cache Strategy

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function CacheStrategyExample() {
  const treeRef = useRef(null);
  const [treeData, setTreeData] = useState([]);
  const cacheRef = useRef(new Map());

  const fetchChildrenWithCache = async (parentId) => {
    // Check cache first
    if (cacheRef.current.has(parentId)) {
      console.log('Cache hit for:', parentId);
      return cacheRef.current.get(parentId);
    }

    // Fetch from API
    console.log('Cache miss, fetching:', parentId);
    const children = await fetch(`/api/children/${parentId}`).then(r => r.json());

    // Store in cache
    cacheRef.current.set(parentId, children);

    // Implement LRU: remove oldest entry if cache is too large
    if (cacheRef.current.size > 50) {
      const firstKey = cacheRef.current.keys().next().value;
      cacheRef.current.delete(firstKey);
    }

    return children;
  };

  const handleNodeExpanding = async (args) => {
    const nodeId = args.node?.getAttribute('data-uid');
    args.cancel = true;

    try {
      const children = await fetchChildrenWithCache(nodeId);
      setTreeData([...treeData, ...children]);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const clearCache = () => {
    cacheRef.current.clear();
    console.log('Cache cleared');
  };

  return (
    <div>
      <button onClick={clearCache}>Clear Cache</button>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: treeData, id: 'id', text: 'name', parentID: 'parentID' }}
        nodeExpanding={handleNodeExpanding}
      />
    </div>
  );
}
```

### TTL-Based Cache

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function TTLCacheExample() {
  const treeRef = useRef(null);
  const [treeData, setTreeData] = useState([]);
  const cacheRef = useRef(new Map());
  const ttlRef = useRef(5 * 60 * 1000); // 5 minutes TTL

  const fetchWithTTLCache = async (parentId) => {
    const cached = cacheRef.current.get(parentId);

    if (cached && Date.now() - cached.timestamp < ttlRef.current) {
      console.log('Cache hit (valid):', parentId);
      return cached.data;
    }

    if (cached) {
      console.log('Cache expired:', parentId);
      cacheRef.current.delete(parentId);
    }

    console.log('Fetching fresh data:', parentId);
    const data = await fetch(`/api/children/${parentId}`).then(r => r.json());

    cacheRef.current.set(parentId, {
      data,
      timestamp: Date.now()
    });

    return data;
  };

  const handleNodeExpanding = async (args) => {
    const nodeId = args.node?.getAttribute('data-uid');
    args.cancel = true;

    try {
      const children = await fetchWithTTLCache(nodeId);
      setTreeData([...treeData, ...children]);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: treeData, id: 'id', text: 'name', parentID: 'parentID' }}
      nodeExpanding={handleNodeExpanding}
    />
  );
}
```

### Persistent Cache Storage

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function PersistentCacheExample() {
  const treeRef = useRef(null);
  const [treeData, setTreeData] = useState([]);
  const cacheKeyRef = useRef('treeview_cache');

  const getFromCache = (parentId) => {
    try {
      const cache = JSON.parse(localStorage.getItem(cacheKeyRef.current) || '{}');
      return cache[parentId];
    } catch {
      return null;
    }
  };

  const saveToCache = (parentId, data) => {
    try {
      const cache = JSON.parse(localStorage.getItem(cacheKeyRef.current) || '{}');
      cache[parentId] = {
        data,
        timestamp: Date.now(),
        version: 1
      };
      localStorage.setItem(cacheKeyRef.current, JSON.stringify(cache));
    } catch (error) {
      console.error('Cache save error:', error);
    }
  };

  const fetchWithPersistentCache = async (parentId) => {
    const cached = getFromCache(parentId);
    if (cached && Date.now() - cached.timestamp < 60 * 60 * 1000) { // 1 hour
      console.log('Cache hit (localStorage):', parentId);
      return cached.data;
    }

    const data = await fetch(`/api/children/${parentId}`).then(r => r.json());
    saveToCache(parentId, data);
    return data;
  };

  const handleNodeExpanding = async (args) => {
    const nodeId = args.node?.getAttribute('data-uid');
    args.cancel = true;

    try {
      const children = await fetchWithPersistentCache(nodeId);
      setTreeData([...treeData, ...children]);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const clearPersistentCache = () => {
    localStorage.removeItem(cacheKeyRef.current);
    console.log('Persistent cache cleared');
  };

  return (
    <div>
      <button onClick={clearPersistentCache}>Clear Persistent Cache</button>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: treeData, id: 'id', text: 'name', parentID: 'parentID' }}
        nodeExpanding={handleNodeExpanding}
      />
    </div>
  );
}
```

---

## State Persistence

### Enable Persistence

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Folder A', expanded: true },
  { id: '02', name: 'Item 1', parentID: '01' },
  { id: '03', name: 'Item 2', parentID: '01' },
  { id: '04', name: 'Folder B', expanded: false },
  { id: '05', name: 'Item 3', parentID: '04' }
];

export default function StatePersistenceExample() {
  const treeRef = useRef(null);

  return (
    <div>
      <p>State will be persisted to localStorage</p>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
        enablePersistence={true}
        persistenceId="my-treeview"  // Unique key for storage
      />
      <p>Try expanding/collapsing nodes and refreshing the page - state persists!</p>
    </div>
  );
}
```

### Custom State Persistence

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function CustomPersistenceExample() {
  const treeRef = useRef(null);
  const [saveStatus, setSaveStatus] = useState('');

  const saveTreeState = async () => {
    try {
      const state = {
        expanded: treeRef.current?.getExpandedNodes(),
        selected: treeRef.current?.getSelectedNodes(),
        checked: treeRef.current?.getCheckedNodes(),
        timestamp: new Date().toISOString()
      };

      // Save to server
      const response = await fetch('/api/save-treestate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(state)
      });

      if (response.ok) {
        setSaveStatus('State saved successfully');
        setTimeout(() => setSaveStatus(''), 3000);
      }
    } catch (error) {
      setSaveStatus('Error saving state');
      console.error('Save error:', error);
    }
  };

  const restoreTreeState = async () => {
    try {
      const response = await fetch('/api/load-treestate');
      const state = await response.json();

      if (state.expanded) {
        state.expanded.forEach(id => treeRef.current?.expandNode(id));
      }
      if (state.selected) {
        treeRef.current?.selectNodes(state.selected);
      }
      if (state.checked) {
        treeRef.current?.checkAll(state.checked);
      }

      setSaveStatus('State restored');
    } catch (error) {
      console.error('Restore error:', error);
    }
  };

  return (
    <div>
      <button onClick={saveTreeState}>Save State</button>
      <button onClick={restoreTreeState}>Restore State</button>
      <div>{saveStatus}</div>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
      />
    </div>
  );
}
```

---

## RTL Support and Localization

### Enable RTL

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const rtlData = [
  { id: '01', name: 'مشروع 1' }, // Arabic
  { id: '02', name: 'مهمة 1', parentID: '01' },
  { id: '03', name: 'مهمة 2', parentID: '01' }
];

export default function RTLSupportExample() {
  const treeRef = useRef(null);
  const [isRTL, setIsRTL] = useState(true);

  return (
    <div dir={isRTL ? 'rtl' : 'ltr'}>
      <button onClick={() => setIsRTL(!isRTL)}>
        Toggle RTL: {isRTL ? 'On' : 'Off'}
      </button>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: rtlData, id: 'id', text: 'name', parentID: 'parentID' }}
        enableRtl={isRTL}
      />
    </div>
  );
}
```

### Multi-Language Support

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const translations = {
  en: {
    'expand': 'Expand',
    'collapse': 'Collapse',
    'select': 'Select',
    'folder': 'Folder',
    'file': 'File'
  },
  es: {
    'expand': 'Expandir',
    'collapse': 'Contraer',
    'select': 'Seleccionar',
    'folder': 'Carpeta',
    'file': 'Archivo'
  },
  ar: {
    'expand': 'توسيع',
    'collapse': 'طي',
    'select': 'تحديد',
    'folder': 'مجلد',
    'file': 'ملف'
  }
};

const localizedData = {
  en: [
    { id: '01', name: 'Folder A' },
    { id: '02', name: 'File 1', parentID: '01' }
  ],
  es: [
    { id: '01', name: 'Carpeta A' },
    { id: '02', name: 'Archivo 1', parentID: '01' }
  ],
  ar: [
    { id: '01', name: 'مجلد أ' },
    { id: '02', name: 'ملف 1', parentID: '01' }
  ]
};

export default function MultiLanguageExample() {
  const treeRef = useRef(null);
  const [language, setLanguage] = useState('en');
  const currentData = localizedData[language];

  return (
    <div>
      <select value={language} onChange={(e) => setLanguage(e.target.value)}>
        <option value="en">English</option>
        <option value="es">Español</option>
        <option value="ar">العربية</option>
      </select>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: currentData, id: 'id', text: 'name', parentID: 'parentID' }}
        enableRtl={language === 'ar'}
      />
    </div>
  );
}
```

---

## Accordion Pattern

### TreeView as Accordion

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const accordionData = [
  { id: '01', name: 'Section 1', expanded: true },
  { id: '02', name: 'Content 1.1', parentID: '01' },
  { id: '03', name: 'Content 1.2', parentID: '01' },
  { id: '04', name: 'Section 2', expanded: false },
  { id: '05', name: 'Content 2.1', parentID: '04' },
  { id: '06', name: 'Content 2.2', parentID: '04' },
  { id: '07', name: 'Section 3', expanded: false }
];

export default function AccordionPatternExample() {
  const treeRef = useRef(null);

  const handleNodeExpanding = (args) => {
    // Only one node can be expanded at a time
    const allNodes = treeRef.current?.getAllNodes() || [];
    const expandedNodes = treeRef.current?.getExpandedNodes() || [];

    // Collapse all other parent nodes
    expandedNodes.forEach(nodeId => {
      const nodeData = accordionData.find(d => d.id === nodeId);
      if (nodeData && !nodeData.parentID) { // Only parent nodes
        const node = treeRef.current?.getNode(nodeId);
        if (node && nodeId !== args.node?.getAttribute('data-uid')) {
          treeRef.current?.collapseNode(node);
        }
      }
    });
  };

  return (
    <div>
      <p>Only one section can be expanded at a time (Accordion behavior)</p>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: accordionData, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
        nodeExpanding={handleNodeExpanding}
      />
    </div>
  );
}
```

### Collapse All Before Expand

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function CollapseBeforeExpandExample() {
  const treeRef = useRef(null);

  const handleNodeExpanding = (args) => {
    // Collapse all siblings first
    const parentId = args.node?.parentElement?.getAttribute('data-parent');
    const siblings = treeRef.current?.getChildren(parentId);

    if (siblings && siblings.length > 1) {
      siblings.forEach(siblingId => {
        if (siblingId !== args.node?.getAttribute('data-uid')) {
          treeRef.current?.collapseNode(siblingId);
        }
      });
    }
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
      nodeExpanding={handleNodeExpanding}
    />
  );
}
```

---

## Virtual Scrolling for Large Datasets

### Enable Virtualization

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function VirtualScrollingExample() {
  const treeRef = useRef(null);
  const [largeData] = useState(() => {
    // Generate large dataset
    const data = [];
    for (let i = 1; i <= 1000; i++) {
      data.push({
        id: String(i),
        name: `Item ${i}`,
        parentID: i > 1 ? String(Math.floor(Math.random() * (i - 1)) + 1) : null
      });
    }
    return data;
  });

  return (
    <div>
      <p>Virtualization enabled for efficient rendering of large datasets</p>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: largeData, id: 'id', text: 'name', parentID: 'parentID' }}
        allowVirtualization={true}
        virtualHeight={600}  // Height of scrollable area
      />
    </div>
  );
}
```

### Dynamic Virtual Height

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function DynamicVirtualHeightExample() {
  const treeRef = useRef(null);
  const [virtualHeight, setVirtualHeight] = useState(400);

  const adjustHeight = (newHeight) => {
    setVirtualHeight(newHeight);
  };

  return (
    <div>
      <div>
        <label>
          Virtual Height:
          <input
            type="range"
            min="200"
            max="800"
            value={virtualHeight}
            onChange={(e) => adjustHeight(parseInt(e.target.value))}
          />
          {virtualHeight}px
        </label>
      </div>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
        allowVirtualization={true}
        virtualHeight={virtualHeight}
      />
    </div>
  );
}
```

---

## Keyboard Shortcuts

### Custom Keyboard Handlers

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function KeyboardShortcutsExample() {
  const treeRef = useRef(null);

  const handleKeyDown = (e) => {
    const tree = treeRef.current;
    if (!tree) return;

    const selectedNode = tree.getSelectedNode();

    switch (e.key) {
      case 'Enter':
        // Open/expand selected node
        tree.expandNode(selectedNode);
        break;

      case 'Backspace':
        // Go to parent
        const parent = tree.getParent(selectedNode?.getAttribute('data-uid'));
        if (parent) {
          tree.selectNodes([parent]);
        }
        break;

      case 'Delete':
        // Delete selected node
        console.log('Delete:', selectedNode?.textContent);
        break;

      case 'c':
        if (e.ctrlKey) {
          e.preventDefault();
          console.log('Copy:', selectedNode?.textContent);
        }
        break;

      case 'x':
        if (e.ctrlKey) {
          e.preventDefault();
          console.log('Cut:', selectedNode?.textContent);
        }
        break;

      case 'v':
        if (e.ctrlKey) {
          e.preventDefault();
          console.log('Paste');
        }
        break;

      case '?':
        if (e.ctrlKey) {
          e.preventDefault();
          showKeyboardHelp();
        }
        break;

      default:
        break;
    }
  };

  const showKeyboardHelp = () => {
    alert(`Keyboard Shortcuts:
    Enter - Expand/Open
    Backspace - Go to parent
    Delete - Delete node
    Ctrl+C - Copy
    Ctrl+X - Cut
    Ctrl+V - Paste
    Ctrl+? - Show help`);
  };

  React.useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <div>
      <p>Try keyboard shortcuts: Enter, Backspace, Delete, Ctrl+C, etc.</p>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
        allowMultiSelection={true}
      />
    </div>
  );
}
```

### Accessibility Features

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function AccessibilityFeaturesExample() {
  const treeRef = useRef(null);

  return (
    <div>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
        // Accessibility attributes
        ariaLabel="Tree view navigation"
        role="tree"
        tabIndex={0}
      />
      <div aria-live="polite">
        <p>Use arrow keys to navigate, Enter to expand/collapse</p>
      </div>
    </div>
  );
}
```

---

## Event Cancellation Patterns

### Preventing Common Operations

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Item 1', collapsible: true },
  { id: '02', name: 'Item 2 (Locked)', parentID: '01', collapsible: false },
  { id: '03', name: 'Item 3', parentID: '01', collapsible: true }
];

export default function EventCancellationExample() {
  const treeRef = useRef(null);

  const handleNodeExpanding = (args) => {
    const nodeData = data.find(d => d.id === args.node?.getAttribute('data-uid'));
    if (!nodeData?.collapsible) {
      args.cancel = true;
      console.log('Expansion prevented');
    }
  };

  const handleNodeCollapsing = (args) => {
    const nodeData = data.find(d => d.id === args.node?.getAttribute('data-uid'));
    if (!nodeData?.collapsible) {
      args.cancel = true;
      console.log('Collapse prevented');
    }
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
      nodeExpanding={handleNodeExpanding}
      nodeCollapsing={handleNodeCollapsing}
    />
  );
}
```

---

## Performance Optimization

### Lazy Rendering

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function LazyRenderingExample() {
  const treeRef = useRef(null);
  const [renderLimit, setRenderLimit] = useState(100);

  // Only render first N items initially
  const getLimitedData = (data) => {
    return data.slice(0, renderLimit);
  };

  const loadMore = () => {
    setRenderLimit(renderLimit + 100);
  };

  return (
    <div>
      <button onClick={loadMore}>Load More Items</button>
      <p>Rendering: {renderLimit} items</p>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
      />
    </div>
  );
}
```

### Batch Operations

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function BatchOperationsExample() {
  const treeRef = useRef(null);

  const performBatchOperations = async () => {
    const operations = [
      { type: 'select', nodeIds: ['01', '02', '03'] },
      { type: 'expand', nodeIds: ['04', '05'] },
      { type: 'check', nodeIds: ['06', '07', '08'] }
    ];

    // Defer updates
    const tree = treeRef.current;

    for (const op of operations) {
      switch (op.type) {
        case 'select':
          tree?.selectNodes(op.nodeIds);
          break;
        case 'expand':
          op.nodeIds.forEach(id => tree?.expandNode(id));
          break;
        case 'check':
          tree?.checkAll(op.nodeIds);
          break;
      }
      // Small delay between batches
      await new Promise(resolve => setTimeout(resolve, 50));
    }
  };

  return (
    <div>
      <button onClick={performBatchOperations}>Perform Batch Operations</button>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
      />
    </div>
  );
}
```

### Memory Management

```tsx
import React, { useRef, useEffect } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function MemoryManagementExample() {
  const treeRef = useRef(null);
  const memoryRef = useRef({ nodesCreated: 0, nodesRemoved: 0 });

  useEffect(() => {
    return () => {
      // Cleanup on unmount
      treeRef.current = null;
      console.log('TreeView cleanup completed');
    };
  }, []);

  const clearUnusedNodes = () => {
    // Remove nodes that are not visible
    const nodes = treeRef.current?.getAllNodes() || [];
    const visibleNodes = new Set(treeRef.current?.getExpandedNodes());

    nodes.forEach(nodeId => {
      if (!visibleNodes.has(nodeId)) {
        // Mark for cleanup (implementation depends on use case)
        console.log('Cleanup node:', nodeId);
      }
    });
  };

  return (
    <div>
      <button onClick={clearUnusedNodes}>Clear Unused Nodes</button>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
      />
    </div>
  );
}
```

---

## Custom Sorting and Filtering

### Sorting Nodes

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const unsortedData = [
  { id: '01', name: 'Zebra', order: 3 },
  { id: '02', name: 'Apple', order: 1 },
  { id: '03', name: 'Mango', order: 2 }
];

export default function SortingExample() {
  const treeRef = useRef(null);
  const [sortOrder, setSortOrder] = useState('asc');

  const sortData = (data, order) => {
    return [...data].sort((a, b) => {
      if (order === 'asc') {
        return a.name.localeCompare(b.name);
      } else {
        return b.name.localeCompare(a.name);
      }
    });
  };

  const sortedData = sortData(unsortedData, sortOrder);

  return (
    <div>
      <button onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}>
        Sort: {sortOrder.toUpperCase()}
      </button>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: sortedData, id: 'id', text: 'name', parentID: 'parentID' }}
      />
    </div>
  );
}
```

### Filtering Nodes

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const allData = [
  { id: '01', name: 'Documents', type: 'folder' },
  { id: '02', name: 'Resume.pdf', parentID: '01', type: 'file', size: 45 },
  { id: '03', name: 'Cover.docx', parentID: '01', type: 'file', size: 32 },
  { id: '04', name: 'Photos', parentID: '01', type: 'folder' },
  { id: '05', name: 'Summer.jpg', parentID: '04', type: 'file', size: 256 }
];

export default function FilteringExample() {
  const treeRef = useRef(null);
  const [filterText, setFilterText] = useState('');
  const [filterType, setFilterType] = useState('all');

  const filterData = (data, text, type) => {
    return data.filter(item => {
      const matchesText = item.name.toLowerCase().includes(text.toLowerCase());
      const matchesType = type === 'all' || item.type === type;
      return matchesText && matchesType;
    });
  };

  const filteredData = filterData(allData, filterText, filterType);

  return (
    <div>
      <input
        type="text"
        placeholder="Search..."
        value={filterText}
        onChange={(e) => setFilterText(e.target.value)}
      />
      <select value={filterType} onChange={(e) => setFilterType(e.target.value)}>
        <option value="all">All</option>
        <option value="folder">Folders</option>
        <option value="file">Files</option>
      </select>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: filteredData, id: 'id', text: 'name', parentID: 'parentID' }}
      />
    </div>
  );
}
```

---

## Tooltip Integration

### Basic Tooltips

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';
import { TooltipComponent } from '@syncfusion/ej2-react-popups';

const data = [
  { id: '01', name: 'Desktop', tooltip: 'Main desktop folder' },
  { id: '02', name: 'Documents', parentID: '01', tooltip: 'Your documents' },
  { id: '03', name: 'Photos', parentID: '01', tooltip: 'Photo collection' }
];

export default function TooltipExample() {
  const treeRef = useRef(null);
  const [activeTooltip, setActiveTooltip] = React.useState(null);

  const handleNodeRendered = (args) => {
    const nodeData = data.find(d => d.id === args.node?.getAttribute('data-uid'));
    if (nodeData?.tooltip) {
      args.node?.setAttribute('title', nodeData.tooltip);
    }
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
      nodeRendered={handleNodeRendered}
    />
  );
}
```

### Advanced Tooltips with Rich Content

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const dataWithDetails = [
  { id: '01', name: 'Item 1', details: 'Created: 2024-01-15, Size: 120KB' },
  { id: '02', name: 'Item 2', parentID: '01', details: 'Modified: 2024-01-10, Type: PDF' }
];

export default function AdvancedTooltipExample() {
  const treeRef = useRef(null);

  const handleNodeMouseEnter = (args) => {
    const nodeData = dataWithDetails.find(
      d => d.id === args.node?.getAttribute('data-uid')
    );

    if (nodeData?.details) {
      const tooltip = document.createElement('div');
      tooltip.className = 'custom-tooltip';
      tooltip.textContent = nodeData.details;
      tooltip.style.cssText = `
        position: absolute;
        background: #333;
        color: white;
        padding: 8px;
        border-radius: 4px;
        font-size: 12px;
        z-index: 1000;
      `;
      document.body.appendChild(tooltip);
    }
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: dataWithDetails, id: 'id', text: 'name', parentID: 'parentID' }}
    />
  );
}
```

---

## Dynamic Icon Changing

### Change Icons Based on State

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Online', status: 'online', iconClass: 'e-icons e-check-circle' },
  { id: '02', name: 'Offline', status: 'offline', iconClass: 'e-icons e-close-circle' },
  { id: '03', name: 'Away', status: 'away', iconClass: 'e-icons e-clock' }
];

export default function DynamicIconExample() {
  const treeRef = useRef(null);
  const [nodeStatuses, setNodeStatuses] = React.useState({});

  const handleNodeRendered = (args) => {
    const nodeId = args.node?.getAttribute('data-uid');
    const nodeData = data.find(d => d.id === nodeId);

    if (nodeData?.iconClass) {
      const icon = args.node?.querySelector('.e-icons');
      if (icon) {
        icon.className = nodeData.iconClass;
      }
    }
  };

  const changeNodeStatus = (nodeId, newStatus) => {
    const node = treeRef.current?.getNode(nodeId);
    const icon = node?.querySelector('.e-icons');

    const statusIcons = {
      online: 'e-icons e-check-circle',
      offline: 'e-icons e-close-circle',
      away: 'e-icons e-clock'
    };

    if (icon) {
      icon.className = statusIcons[newStatus] || 'e-icons e-folder';
    }

    setNodeStatuses({ ...nodeStatuses, [nodeId]: newStatus });
  };

  return (
    <div>
      <button onClick={() => changeNodeStatus('01', 'offline')}>
        Set Item 1 Offline
      </button>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', iconCss: 'iconClass' }}
        nodeRendered={handleNodeRendered}
      />
    </div>
  );
}
```

---

## Custom CSS Classes

### Apply Custom Styling

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';
import './custom-treeview.css';

const data = [
  { id: '01', name: 'Important Item', priority: 'high' },
  { id: '02', name: 'Normal Item', priority: 'normal' },
  { id: '03', name: 'Low Priority', priority: 'low' }
];

export default function CustomCSSExample() {
  const treeRef = useRef(null);

  const handleNodeRendered = (args) => {
    const nodeData = data.find(d => d.id === args.node?.getAttribute('data-uid'));
    
    if (nodeData?.priority) {
      args.node?.classList.add(`priority-${nodeData.priority}`);
    }
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
      cssClass="custom-treeview"
      nodeRendered={handleNodeRendered}
    />
  );
}
```

```css
/* custom-treeview.css */
.custom-treeview .priority-high {
  background-color: #FFEBEE;
  border-left: 3px solid #F44336;
}

.custom-treeview .priority-high > .e-full-row {
  font-weight: bold;
  color: #C62828;
}

.custom-treeview .priority-normal {
  background-color: #F5F5F5;
}

.custom-treeview .priority-low {
  opacity: 0.6;
  color: #999;
}
```

---

## Ripple Effects

### Add Ripple Animation

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';
import './ripple-effect.css';

const data = [
  { id: '01', name: 'Item 1' },
  { id: '02', name: 'Item 2', parentID: '01' }
];

export default function RippleEffectExample() {
  const treeRef = useRef(null);

  const handleNodeClicked = (args) => {
    // Add ripple effect
    const ripple = document.createElement('span');
    ripple.className = 'ripple';
    args.node?.appendChild(ripple);

    setTimeout(() => ripple.remove(), 600);
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
      nodeSelected={handleNodeClicked}
      cssClass="ripple-treeview"
    />
  );
}
```

```css
/* ripple-effect.css */
.ripple-treeview .ripple {
  position: absolute;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.6);
  transform: scale(0);
  animation: ripple-animation 0.6s ease-out;
  pointer-events: none;
}

@keyframes ripple-animation {
  to {
    transform: scale(4);
    opacity: 0;
  }
}
```

---

## Multi-Language Support

### Language Switching

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const i18n = {
  en: {
    folders: 'Folders',
    files: 'Files',
    documents: 'Documents',
    downloads: 'Downloads'
  },
  fr: {
    folders: 'Dossiers',
    files: 'Fichiers',
    documents: 'Documents',
    downloads: 'Téléchargements'
  },
  de: {
    folders: 'Ordner',
    files: 'Dateien',
    documents: 'Dokumente',
    downloads: 'Downloads'
  }
};

const createLocalizedData = (language) => {
  return [
    { id: '01', name: i18n[language].documents },
    { id: '02', name: 'Resume.pdf', parentID: '01' },
    { id: '03', name: i18n[language].downloads }
  ];
};

export default function MultiLanguageSupportExample() {
  const treeRef = useRef(null);
  const [language, setLanguage] = useState('en');

  return (
    <div>
      <select value={language} onChange={(e) => setLanguage(e.target.value)}>
        <option value="en">English</option>
        <option value="fr">Français</option>
        <option value="de">Deutsch</option>
      </select>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: createLocalizedData(language), id: 'id', text: 'name', parentID: 'parentID' }}
      />
    </div>
  );
}
```

---

## Real-World Patterns

### Example 1: File System Manager

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function FileSystemManagerExample() {
  const treeRef = useRef(null);
  const [currentPath, setCurrentPath] = useState('/');
  const [selectedFile, setSelectedFile] = useState(null);

  const handleNodeSelected = (args) => {
    const nodeData = {
      id: args.node?.getAttribute('data-uid'),
      name: args.node?.textContent,
      path: currentPath + args.node?.textContent
    };
    setSelectedFile(nodeData);
  };

  const handleNodeDoubleClick = (args) => {
    setCurrentPath(currentPath + args.node?.textContent + '/');
  };

  return (
    <div style={{ display: 'flex' }}>
      <div style={{ flex: 1 }}>
        <div style={{ padding: '10px', backgroundColor: '#f0f0f0' }}>
          <p>Path: {currentPath}</p>
        </div>
        <TreeViewComponent
          ref={treeRef}
          fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
          allowDragAndDrop={true}
          nodeSelected={handleNodeSelected}
        />
      </div>
      <div style={{ flex: 1, padding: '20px', backgroundColor: '#fafafa' }}>
        {selectedFile && (
          <div>
            <h3>File Details</h3>
            <p>Name: {selectedFile.name}</p>
            <p>Path: {selectedFile.path}</p>
          </div>
        )}
      </div>
    </div>
  );
}
```

### Example 2: Category Browser with Filtering

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function CategoryBrowserExample() {
  const treeRef = useRef(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState(null);

  const hierarchicalData = [
    { id: '01', name: 'Electronics' },
    { id: '02', name: 'Smartphones', parentID: '01' },
    { id: '03', name: 'Laptops', parentID: '01' },
    { id: '04', name: 'Clothing' },
    { id: '05', name: 'Men', parentID: '04' },
    { id: '06', name: 'Women', parentID: '04' }
  ];

  const filterData = hierarchicalData.filter(item =>
    item.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div>
      <input
        type="text"
        placeholder="Search categories..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
      />
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: filterData, id: 'id', text: 'name', parentID: 'parentID' }}
        nodeSelected={(args) => setSelectedCategory(args.node?.textContent)}
      />
      {selectedCategory && <p>Selected: {selectedCategory}</p>}
    </div>
  );
}
```

### Example 3: Dependency Tree

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function DependencyTreeExample() {
  const treeRef = useRef(null);

  const dependencyData = [
    { id: '01', name: 'app-root', version: '1.0.0' },
    { id: '02', name: 'react', parentID: '01', version: '18.2.0' },
    { id: '03', name: 'react-dom', parentID: '01', version: '18.2.0' },
    { id: '04', name: '@syncfusion/ej2-react-navigations', parentID: '01', version: '22.1.0' }
  ];

  const handleNodeSelected = (args) => {
    const nodeId = args.node?.getAttribute('data-uid');
    const nodeData = dependencyData.find(d => d.id === nodeId);
    console.log('Selected dependency:', nodeData);
  };

  return (
    <div>
      <h3>Project Dependencies</h3>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: dependencyData, id: 'id', text: 'name', parentID: 'parentID' }}
        nodeSelected={handleNodeSelected}
      />
    </div>
  );
}
```

---

## Best Practices

1. **Use load-on-demand for large datasets** - Improves initial load time
2. **Implement caching strategies** - Reduces server requests
3. **Enable state persistence** - Better user experience
4. **Support RTL and localization** - Global accessibility
5. **Use virtual scrolling** - Efficient rendering of massive datasets
6. **Provide keyboard shortcuts** - Improves productivity
7. **Optimize event handlers** - Debounce and throttle operations
8. **Use batch operations** - Better performance
9. **Implement proper error handling** - Graceful degradation
10. **Test performance** - Monitor tree complexity
11. **Sanitize user input** - Security best practice
12. **Document custom implementations** - Maintainability
13. **Use accessibility features** - ARIA labels and roles
14. **Monitor memory usage** - Cleanup unused nodes
15. **Provide visual feedback** - Loading states, animations, tooltips

