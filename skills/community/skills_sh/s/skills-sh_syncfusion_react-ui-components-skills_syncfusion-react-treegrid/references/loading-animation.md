---
name: loading-animation
description: 'Loading Animation in React TreeGrid - built-in spinner, custom animations, loading state management, and CSS styling.'
---

# Loading Animation

## Table of Contents
- [Built-in Spinner](#built-in-spinner)
- [Custom Loading Spinner](#custom-loading-spinner)
- [Loading State Management](#loading-state-management)
- [Loading Animation Customization CSS](#loading-animation-customization-css)
- [Common Patterns](#common-patterns)
- [Key APIs](#key-apis)

## Built-in Spinner:

```tsx
import React, { useEffect, useState } from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const [data, setData] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const treeGridRef = React.useRef();

  useEffect(() => {
    // Show loading
    setIsLoading(true);
    
    // Simulate data fetch
    setTimeout(() => {
      setData([
        { TaskID: 1, TaskName: 'Planning', Children: [] }
      ]);
      setIsLoading(false);
    }, 2000);
  }, []);

  return (
    <TreeGridComponent
      ref={treeGridRef}
      dataSource={data}
      childMapping="Children"
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
      </ColumnsDirective>
    </TreeGridComponent>
  );
}
```

## Custom Loading Spinner

Display custom loading animation:

```tsx

import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const [isLoading, setIsLoading] = React.useState(false);
  const treeGridRef = React.useRef();

  const showLoadingSpinner = () => {
    setIsLoading(true);
    // Simulate operation
    setTimeout(() => setIsLoading(false), 2000);
  };

  return (
    <div>
      {isLoading && (
        <div style={{
          position: 'fixed',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          zIndex: 1000,
          textAlign: 'center'
        }}>
          <div style={{
            width: '50px',
            height: '50px',
            border: '4px solid #f3f3f3',
            borderTop: '4px solid #3498db',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite'
          }} />
          <p>Loading...</p>
        </div>
      )}
      <TreeGridComponent ref={treeGridRef} dataSource={[]} childMapping="Children">
        <ColumnsDirective>
          <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
        </ColumnsDirective>
      </TreeGridComponent>
    </div>
  );
}
```

## Loading State Management

Control loading based on data operations:

```tsx

<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  rowDataBound={(args) => {
    if (args.rowIndex === 0) {
      // Hide loading on first row
      setIsLoading(false);
    }
  }}
  load={() => {
    // Show loading when TreeGrid loads
    setIsLoading(true);
  }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
</TreeGridComponent>
```

## Loading Animation Customization CSS

Add loading animation with CSS:

```tsx
import React from 'react';

const LoadingSpinner = () => (
  <style>{`
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    
    .loading-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.3);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1000;
    }
    
    .spinner {
      width: 50px;
      height: 50px;
      border: 4px solid #f3f3f3;
      border-top: 4px solid #3498db;
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }
  `}</style>
);

export default function App() {
  const [isLoading, setIsLoading] = React.useState(false);

  return (
    <>
      <LoadingSpinner />
      {isLoading && (
        <div className="loading-overlay">
          <div className="spinner" />
        </div>
      )}
    </>
  );
}
```

## Key APIs

| Property/Event | Type | Description |
|---|---|---|
| `load` | event | Fired when TreeGrid initializes |
| `rowDataBound` | event | Fired when row data binds |
| `actionComplete` | event | Fired when action completes |
| `actionFailure` | event | Fired when action fails |

## Common Patterns

1. **Initial Load**: Show spinner during data fetch
2. **Operation States**: Show spinner during add/edit/delete
3. **Custom Messages**: Display operation status
4. **Timeout Handling**: Hide spinner after timeout

