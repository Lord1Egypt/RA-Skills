---
name: react-jsmind-usage
description: Use when integrating @frank17008/react-jsmind npm package into React applications
---

# ReactJsMind Integration

## Overview
React wrapper around jsMind for rendering interactive mind maps. Helps developers quickly integrate the npm package with correct imports, types, and configuration.

## When to Use
- Developer asks "how to install and use react-jsmind"
- Developer reports "mind map not showing"
- Developer needs ref methods (getData, addNode, screenShot)
- Developer confused about data format or types

## Installation

```bash
npm install @frank17008/react-jsmind
# or
yarn add @frank17008/react-jsmind
```

No need to install jsmind separately - it's a peer dependency.

## Core Pattern - Basic Integration

```tsx
import React, { useRef } from 'react'
import ReactJsMind from '@frank17008/react-jsmind'
import type { JsMindRefValue, JsMindData } from '@frank17008/react-jsmind'
import '@frank17008/react-jsmind/dist/esm/index.min.css' // REQUIRED for styling

const App = () => {
  const mindRef = useRef<JsMindRefValue | null>(null)

  // Correct data format - MUST include meta and format
  const mindData: JsMindData = {
    meta: { name: '思维导图', author: 'Your Name', version: '1.0' },
    format: 'node_tree',
    data: {
      id: 'root',
      topic: '中心主题',
      children: [
        { id: '1', topic: '分支1' },
        { id: '2', topic: '分支2' },
      ],
    },
  }

  return (
    <div style={{ width: '100%', height: 600 }}>  // REQUIRED: parent must have explicit size
      <ReactJsMind
        ref={mindRef}
        data={mindData}
        options={{ editable: true }}
        onClick={(node) => console.log('Clicked:', node)}
      />
    </div>
  )
}

export default App
```

## Quick Reference

### Types (import from @frank17008/react-jsmind)
| Type | Usage |
|------|-------|
| `JsMindRefValue` | Ref type for useRef |
| `JsMindData` | Data object with meta/format/data |
| `TreeNode` | Single node with id/topic/children |
| `ArrayTreeNode` | Array format node with parentid |

### Ref Methods
```tsx
mindRef.current?.getData()           // Get current data
mindRef.current?.getSelectedNode()   // Get selected node
mindRef.current?.screenShot()        // Export as PNG
mindRef.current?.expandAll()         // Expand all nodes
mindRef.current?.addNode(parent, 'id', 'topic', {}, 'right')  // Add node
mindRef.current?.removeNode(node)   // Remove node
mindRef.current?.setNodeColor(nodeId, '#ff0000', '#ffffff')   // Set colors
```

### Data Formats
- **Tree format** (node_tree): `{ id, topic, children: [...] }`
- **Array format** (node_array): `{ id, topic, parentid }` with `isroot` for root

## Common Mistakes

### Mistake 1: Missing CSS Import
```tsx
// ❌ WRONG - no styling
import ReactJsMind from '@frank17008/react-jsmind'

// ✅ CORRECT
import ReactJsMind from '@frank17008/react-jsmind'
import '@frank17008/react-jsmind/dist/esm/index.min.css'
```

### Mistake 2: Wrong Type Name
```tsx
// ❌ WRONG
const ref = useRef<JsMindRef>(null)

// ✅ CORRECT
const ref = useRef<JsMindRefValue | null>(null)
```

### Mistake 3: Missing Container Size
```tsx
// ❌ WRONG - container has no size
<ReactJsMind data={data} />

// ✅ CORRECT - parent must have explicit width/height
<div style={{ width: '100%', height: 600 }}>
  <ReactJsMind data={data} />
</div>
```

### Mistake 4: Incomplete Data Object
```tsx
// ❌ WRONG - passing TreeNode directly
<ReactJsMind data={{ id: 'root', topic: 'Root' }} />

// ✅ CORRECT - wrap in JsMindData with meta and format
<ReactJsMind data={{
  meta: { name: 'demo' },
  format: 'node_tree',
  data: { id: 'root', topic: 'Root' }
}} />
```

## Data Format Examples

### Tree Format (Recommended)
```tsx
const data: JsMindData = {
  meta: { name: 'My Mind Map', version: '1.0' },
  format: 'node_tree',
  data: {
    id: 'root',
    topic: 'Main Topic',
    expanded: true,
    children: [
      { id: '1', topic: 'Child 1', direction: 'left' },
      { id: '2', topic: 'Child 2', direction: 'right', children: [
        { id: '2-1', topic: 'Grandchild' }
      ]},
    ],
  },
}
```

### Array Format
```tsx
const data: JsMindData = {
  meta: { name: 'My Mind Map' },
  format: 'node_array',
  data: [
    { id: 'root', topic: 'Main', parentid: null, isroot: true },
    { id: '1', topic: 'Child 1', parentid: 'root' },
    { id: '2', topic: 'Child 2', parentid: 'root' },
  ],
}
```

## Troubleshooting

### "Mind map not showing"
1. Check parent container has explicit width/height
2. Verify CSS is imported: `import '@frank17008/react-jsmind/dist/esm/index.min.css'`
3. Ensure data format includes meta and format fields

### "TypeScript errors"
1. Use `JsMindRefValue` not `JsMindRef`
2. Import types: `import type { JsMindRefValue, JsMindData } from '@frank17008/react-jsmind'`

### "screenShot not working"
1. Ensure container has rendered first
2. Check dom-to-image dependency is installed