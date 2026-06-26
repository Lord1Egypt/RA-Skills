# Templates

## Table of Contents

- [Item Template](#item-template)
- [Value Template](#value-template)
- [Header Template](#header-template)
- [No Records Template](#no-records-template)
- [Action Failure Template](#action-failure-template)
- [Footer Template](#footer-template)
- [Template Expression Syntax](#template-expression-syntax)

## Item Template

Customize the content of each list item in the dropdown using `itemTemplate` property. This allows complex data display with custom formatting and styling.

### Basic Item Template

```jsx
const employeeData = [
  {
    id: 1,
    name: 'Michael Scott',
    position: 'Manager',
    parentId: null,
    expanded: true,
  },
  {
    id: 2,
    name: 'Dwight Schrute',
    position: 'Assistant Regional Manager',
    parentId: 1,
  },
  {
    id: 3,
    name: 'Jim Halpert',
    position: 'Sales Representative',
    parentId: 1,
  },
];

function App() {
  return (
    <DropDownTreeComponent
      fields={{
        dataSource: employeeData,
        value: 'id',
        text: 'name',
        parentValue: 'parentId',
      }}
      itemTemplate={(props) => (
        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          <span style={{ fontWeight: 'bold' }}>{props.name}</span>
          <span style={{ fontSize: '12px', color: '#999' }}>
            {props.position}
          </span>
        </div>
      )}
      placeholder="Select employee"
    />
  );
}

export default App;
```

### Styling with CSS Classes

```jsx
const itemTemplate = (props) => (
  <div className="employee-item">
    <div className="employee-name">{props.name}</div>
    <div className="employee-position">{props.position}</div>
  </div>
);

// CSS
const styles = `
  .employee-item {
    padding: 8px 0;
    border-bottom: 1px solid #eee;
  }
  
  .employee-name {
    font-weight: 600;
    color: #333;
  }
  
  .employee-position {
    font-size: 12px;
    color: #666;
  }
`;
```

### Complex Template with Status Indicator

```jsx
const projectData = [
  {
    id: 1,
    name: 'Website Redesign',
    status: 'In Progress',
    progress: 75,
    parentId: null,
  },
  {
    id: 2,
    name: 'Database Migration',
    status: 'Completed',
    progress: 100,
    parentId: 1,
  },
  {
    id: 3,
    name: 'API Development',
    status: 'Pending',
    progress: 0,
    parentId: 1,
  },
];

function App() {
  const getStatusColor = (status) => {
    switch (status) {
      case 'Completed':
        return '#4CAF50';
      case 'In Progress':
        return '#FFC107';
      case 'Pending':
        return '#F44336';
      default:
        return '#999';
    }
  };

  return (
    <DropDownTreeComponent
      fields={{
        dataSource: projectData,
        value: 'id',
        text: 'name',
        parentValue: 'parentId',
      }}
      itemTemplate={(props) => (
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 0' }}>
          <span>{props.name}</span>
          <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
            <div
              style={{
                width: '50px',
                height: '4px',
                backgroundColor: '#ddd',
                borderRadius: '2px',
                overflow: 'hidden',
              }}
            >
              <div
                style={{
                  width: `${props.progress}%`,
                  height: '100%',
                  backgroundColor: getStatusColor(props.status),
                }}
              />
            </div>
            <span
              style={{
                fontSize: '11px',
                fontWeight: 'bold',
                color: getStatusColor(props.status),
              }}
            >
              {props.status}
            </span>
          </div>
        </div>
      )}
      placeholder="Select project"
    />
  );
}

export default App;
```

## Value Template

Customize how selected values display in the input field using `valueTemplate` property.

### Basic Value Template

```jsx
<DropDownTreeComponent
  fields={{...}}
  valueTemplate={(props) => (
    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
      <span>👤</span>
      <span>{props.name}</span>
      <span style={{ fontSize: '12px', color: '#999' }}>
        ({props.position})
      </span>
    </div>
  )}
/>
```

### Count Summary

```jsx
const valueTemplate = (props) => {
  // For multiple selections, show count
  if (Array.isArray(props)) {
    return (
      <div>
        Selected: <strong>{props.length}</strong> items
      </div>
    );
  }
  // For single selection
  return <span>{props.name}</span>;
};

<DropDownTreeComponent
  fields={{...}}
  valueTemplate={valueTemplate}
  showCheckBox={true}
/>
```

### Custom Format

```jsx
const valueTemplate = (props) => {
  if (Array.isArray(props)) {
    const names = props.map(p => p.name).join(', ');
    return <span title={names}>{names.substring(0, 50)}...</span>;
  }
  return props.name;
};
```

## Header Template

Customize the popup header using `headerTemplate`. This appears statically above list items.

### Search Header

```jsx
const [searchText, setSearchText] = React.useState('');

<DropDownTreeComponent
  fields={{...}}
  headerTemplate={() => (
    <div style={{ padding: '10px' }}>
      <input
        type="text"
        placeholder="Search items..."
        value={searchText}
        onChange={(e) => setSearchText(e.target.value)}
        style={{
          width: '100%',
          padding: '8px',
          border: '1px solid #ddd',
          borderRadius: '4px',
        }}
      />
    </div>
  )}
/>
```

### Instructions Header

```jsx
<DropDownTreeComponent
  fields={{...}}
  headerTemplate={() => (
    <div style={{ padding: '12px', backgroundColor: '#f5f5f5', borderBottom: '1px solid #ddd' }}>
      <div style={{ fontSize: '14px', fontWeight: 'bold' }}>Select Categories</div>
      <div style={{ fontSize: '12px', color: '#666', marginTop: '4px' }}>
        Expand items to see subcategories
      </div>
    </div>
  )}
  showCheckBox={true}
/>
```

### Action Buttons Header

```jsx
<DropDownTreeComponent
  fields={{...}}
  headerTemplate={() => (
    <div style={{ padding: '10px', borderBottom: '1px solid #ddd', display: 'flex', gap: '8px' }}>
      <button
        onClick={() => treeRef.current && treeRef.current.clear()}
        style={{ flex: 1, padding: '6px', fontSize: '12px' }}
      >
        Clear All
      </button>
      <button
        onClick={() => {
          // Implement select all logic by updating controlled `value` or data source
        }}
        style={{ flex: 1, padding: '6px', fontSize: '12px' }}
      >
        Select All
      </button>
    </div>
  )}
  showCheckBox={true}
/>
```

## No Records Template

Display custom content when no items match the filter or when data is empty.

### Simple No Records Message

```jsx
<DropDownTreeComponent
  fields={{...}}
  allowFiltering={true}
  noRecordsTemplate={() => (
    <div style={{ padding: '20px', textAlign: 'center', color: '#999' }}>
      No matching items found
    </div>
  )}
/>
```

### Enhanced No Records Template

```jsx
const noRecordsTemplate = () => (
  <div style={{
    padding: '30px 20px',
    textAlign: 'center',
    backgroundColor: '#f9f9f9'
  }}>
    <div style={{ fontSize: '18px', marginBottom: '8px' }}>🔍</div>
    <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>No Results</div>
    <div style={{ fontSize: '12px', color: '#666' }}>
      Try a different search term or adjust filters
    </div>
  </div>
);

<DropDownTreeComponent
  fields={{...}}
  allowFiltering={true}
  noRecordsTemplate={noRecordsTemplate}
/>
```

## Action Failure Template

Display custom error message when data loading fails (remote data errors).

### Basic Error Message

```jsx
const actionFailureTemplate = () => (
  <div style={{
    padding: '20px',
    textAlign: 'center',
    color: '#d32f2f'
  }}>
    ❌ Failed to load items
  </div>
);

<DropDownTreeComponent
  fields={{
    dataSource: new DataManager({
      url: 'url',
      adaptor: new ODataV4Adaptor()
    }),
    value: 'id',
    text: 'name'
  }}
  actionFailureTemplate={actionFailureTemplate}
/>
```

### Error Template with Details

```jsx
const actionFailureTemplate = () => (
  <div style={{
    padding: '16px',
    backgroundColor: '#ffebee',
    borderLeft: '4px solid #d32f2f',
    borderRadius: '4px'
  }}>
    <div style={{
      fontWeight: 'bold',
      color: '#c62828',
      marginBottom: '8px'
    }}>
      ⚠️ Error Loading Data
    </div>
    <div style={{
      fontSize: '12px',
      color: '#c62828',
      lineHeight: '1.5'
    }}>
      Unable to connect to the server. Please check your internet connection
      and try again.
    </div>
  </div>
);

<DropDownTreeComponent
  fields={{...}}
  actionFailureTemplate={actionFailureTemplate}
/>
```

### Error Template with Retry

```jsx
import React, { useRef, useState } from 'react';
import { DropDownTreeComponent } from '@syncfusion/ej2-react-dropdowns';

function DropdownTreeWithRetry() {
  const treeRef = useRef(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleRetry = () => {
    setIsLoading(true);
    // Simulate retry with delay
    setTimeout(() => {
      if (treeRef.current) {
        treeRef.current.refresh();
      }
      setIsLoading(false);
    }, 2000);
  };

  const actionFailureTemplate = () => (
    <div style={{
      padding: '20px',
      textAlign: 'center',
      backgroundColor: '#fff3cd',
      borderRadius: '4px'
    }}>
      <div style={{
        fontSize: '14px',
        fontWeight: 'bold',
        color: '#856404',
        marginBottom: '12px'
      }}>
        Connection Failed
      </div>
      <button
        onClick={handleRetry}
        disabled={isLoading}
        style={{
          padding: '8px 16px',
          backgroundColor: '#ffc107',
          color: '#000',
          border: 'none',
          borderRadius: '4px',
          cursor: isLoading ? 'not-allowed' : 'pointer',
          fontWeight: 'bold',
          opacity: isLoading ? 0.6 : 1
        }}
      >
        {isLoading ? 'Retrying...' : 'Retry Connection'}
      </button>
    </div>
  );

  return (
    <DropDownTreeComponent
      ref={treeRef}
      fields={{
        dataSource: new DataManager({
          url: 'url',
          adaptor: new ODataV4Adaptor()
        }),
        value: 'id',
        text: 'name'
      }}
      actionFailureTemplate={actionFailureTemplate}
    />
  );
}

export default DropdownTreeWithRetry;
```

## Footer Template

Customize the popup footer using `footerTemplate`. This appears statically below list items.

### Count Summary Footer

```jsx
<DropDownTreeComponent
  fields={{...}}
  showCheckBox={true}
  footerTemplate={(props) => (
    <div style={{ padding: '10px', borderTop: '1px solid #ddd', backgroundColor: '#f9f9f9', fontSize: '12px', color: '#666' }}>
      Total items available: <strong>{data.length}</strong>
    </div>
  )}
/>
```

### Selection Count

```jsx
// Recommended: track selected count via `change` event and component state
const [selectedCount, setSelectedCount] = useState(0);

const handleChange = (e) => {
  setSelectedCount((e.value || []).length);
};

const footerTemplate = () => (
  <div style={{ padding: '10px', borderTop: '1px solid #ddd', display: 'flex', justifyContent: 'space-between', fontSize: '12px' }}>
    <span>Selected: <strong>{selectedCount}</strong></span>
    <span>Total: <strong>{data.length}</strong></span>
  </div>
);

<DropDownTreeComponent footerTemplate={footerTemplate} change={handleChange} showCheckBox={true} fields={{...}} />
```

### Actions Footer

```jsx
<DropDownTreeComponent
  fields={{...}}
  footerTemplate={() => (
    <div style={{ padding: '10px', borderTop: '1px solid #ddd', display: 'flex', gap: '8px' }}>
      <button
        onClick={() => console.log('Save selections')}
        style={{ flex: 1, padding: '8px', backgroundColor: '#4CAF50', color: 'white', border: 'none', borderRadius: '4px' }}
      >
        Confirm
      </button>
      <button
        onClick={() => console.log('Cancel')}
        style={{ flex: 1, padding: '8px', backgroundColor: '#f44336', color: 'white', border: 'none', borderRadius: '4px' }}
      >
        Cancel
      </button>
    </div>
  )}
/>
```

## Template Expression Syntax

### Basic Expression

Use curly braces `{...}` to access data properties:

```jsx
// In templates, access properties directly
itemTemplate={(props) => (
  <div>{props.id} - {props.name}</div>
)}
```

### Conditional Rendering

```jsx
itemTemplate={(props) => (
  <div>
    <span>{props.name}</span>
    {props.isNew && <span style={{ color: 'red', marginLeft: '8px' }}>NEW</span>}
  </div>
)}
```

### Array Access

```jsx
itemTemplate={(props) => (
  <div>
    {props.tags && props.tags.map((tag, i) => (
      <span key={i} style={{ marginRight: '4px' }}>{tag}</span>
    ))}
  </div>
)}
```

### Method Calls

```jsx
const formatPrice = (price) => `$${price.toFixed(2)}`;

itemTemplate={(props) => (
  <div>
    <span>{props.name}</span>
    <span style={{ float: 'right' }}>{formatPrice(props.price)}</span>
  </div>
)}
```

### Nested Object Access

```jsx
const data = [
  {
    id: 1,
    name: 'Item',
    details: { category: 'A', priority: 'High' }
  }
];

itemTemplate={(props) => (
  <div>
    <span>{props.name}</span>
    <span>{props.details?.category}</span>
  </div>
)}
```

### Template Type Flexibility

Templates accept both **function components** and **HTML strings**:

```jsx
// Function template (recommended)
itemTemplate={(props) => <div>{props.name}</div>}

// Or HTML string (JSX will convert)
itemTemplate="<div>${name}</div>"
```

## Complete Template Example

```jsx
import { DropDownTreeComponent } from '@syncfusion/ej2-react-dropdowns';
import { useRef } from 'react';
import '@syncfusion/ej2-dropdowns/styles/material.css';

const companyData = [
  {
    id: 1,
    name: 'Engineering',
    budget: 500000,
    headcount: 25,
    expanded: true,
  },
  {
    id: 2,
    name: 'Frontend Team',
    budget: 200000,
    headcount: 10,
    parentId: 1,
  },
  {
    id: 3,
    name: 'Backend Team',
    budget: 300000,
    headcount: 15,
    parentId: 1,
  },
  {
    id: 4,
    name: 'Sales',
    budget: 250000,
    headcount: 12,
    expanded: true,
  },
];

function App() {
  const treeRef = useRef(null);

  return (
    <div style={{ padding: '20px' }}>
      <h2>Department Selector with Templates</h2>
      <DropDownTreeComponent
        ref={treeRef}
        fields={{
          dataSource: companyData,
          value: 'id',
          text: 'name',
          parentValue: 'parentId',
        }}
        itemTemplate={(props) => (
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0' }}>
            <span>{props.name}</span>
            <span style={{ fontSize: '12px', color: '#999' }}>
              {props.headcount} people | ${props.budget.toLocaleString()}
            </span>
          </div>
        )}
        valueTemplate={(props) => (
          <div>
            <strong>{props.name}</strong>
            <span style={{ marginLeft: '8px', color: '#666', fontSize: '12px' }}>
              ({props.headcount} team members)
            </span>
          </div>
        )}
        headerTemplate={() => (
          <div style={{ padding: '10px', backgroundColor: '#f0f0f0', fontWeight: 'bold' }}>
            Select a Department
          </div>
        )}
        footerTemplate={() => (
          <div style={{ padding: '10px', borderTop: '1px solid #ddd', fontSize: '12px', color: '#999' }}>
            Total departments: {companyData.length}
          </div>
        )}
        placeholder="Choose department"
      />
    </div>
  );
}

export default App;
```
