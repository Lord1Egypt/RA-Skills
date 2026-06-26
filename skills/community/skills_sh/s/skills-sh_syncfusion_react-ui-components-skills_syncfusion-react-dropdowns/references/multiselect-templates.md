# Templates in Syncfusion React MultiSelect

## Table of Contents
- [Overview](#overview)
- [Item Template](#item-template)
- [Value Template](#value-template)
- [Group Template](#group-template)
- [Header and Footer Templates](#header-and-footer-templates)
- [No Records and Action Failure Templates](#no-records-and-action-failure-templates)
- [Template Performance Tips](#template-performance-tips)

---

## Overview

Templates allow you to replace the default rendering of every visual zone in the MultiSelect. Use templates when:
- Items should show images, icons, or multi-column layouts
- Selected values (chips) should display custom content
- Group headers need custom formatting
- The popup needs a custom header or footer (e.g., "Add new item" button)
- You want branded "No results" messaging

| Template Prop | Customizes |
|--------------|-----------|
| `itemTemplate` | Each item in the dropdown list |
| `valueTemplate` | Each selected chip/tag in the input |
| `groupTemplate` | Group category header rows |
| `headerTemplate` | Static header at the top of the popup |
| `footerTemplate` | Static footer at the bottom of the popup |
| `noRecordsTemplate` | Content when no items match |
| `actionFailureTemplate` | Content when remote data load fails |

---

## Item Template

Customize how each list item is rendered inside the popup. Receives the data item as its argument:

```tsx
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';
import { MultiSelectComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

export default function App() {
  const employeeData = new DataManager({
    adaptor: new ODataV4Adaptor(),
    crossDomain: true,
    url: 'url',
  });
  const query = new Query().from('Employees').select(['FirstName', 'City', 'EmployeeID']).take(6);
  const fields = { text: 'FirstName', value: 'EmployeeID' };

  // Two-column layout: name on the left, city on the right
  const itemTemplate = (data: any) => {
    return (
      <span>
        <span style={{ fontWeight: 'bold' }}>{data.FirstName}</span>
        <span style={{ float: 'right', color: '#888' }}>{data.City}</span>
      </span>
    );
  };

  return (
    <MultiSelectComponent
      id="mtselement"
      dataSource={employeeData}
      query={query}
      fields={fields}
      itemTemplate={itemTemplate}
      placeholder="Select an employee"
    />
  );
}
```

---

## Value Template

Customize how each selected item is displayed as a chip in the input field. Receives the selected data item:

```tsx
import { MultiSelectComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

export default function App() {
  const employeeData = [
    { id: 'e1', name: 'Alice', avatar: '👩' },
    { id: 'e2', name: 'Bob',   avatar: '👨' },
    { id: 'e3', name: 'Carol', avatar: '👩‍💼' },
  ];
  const fields = { text: 'name', value: 'id' };

  // Show emoji avatar before the name in the chip
  const valueTemplate = (data: any) => {
    return (<span>{data.avatar} {data.name}</span>);
  };

  return (
    <MultiSelectComponent
      id="mtselement"
      dataSource={employeeData}
      fields={fields}
      valueTemplate={valueTemplate}
      mode="Box"
      placeholder="Select employees"
    />
  );
}
```

---

## Group Template

Customize group category headers in the popup list. See also [grouping.md](grouping.md):

```tsx
const groupTemplate = (data: any) => {
  return (
    <div style={{ padding: '4px 8px', background: '#f0f4ff', fontWeight: 600 }}>
      📁 {data.category}
    </div>
  );
};

<MultiSelectComponent
  id="mtselement"
  dataSource={vegetableData}
  fields={{ text: 'vegetable', value: 'id', groupBy: 'category' }}
  groupTemplate={groupTemplate}
  placeholder="Select a vegetable"
/>
```

---

## Header and Footer Templates

Add static content at the top or bottom of the popup — useful for a "Select All" option, action buttons, or count display:

```tsx
import { MultiSelectComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

export default function App() {
  const sportsData = ['Badminton', 'Cricket', 'Football', 'Golf', 'Tennis', 'Hockey'];

  const headerTemplate = () => {
    return (
      <div style={{ padding: '8px 12px', borderBottom: '1px solid #ddd', fontWeight: 'bold' }}>
        🏆 Select Sports
      </div>
    );
  };

  const footerTemplate = () => {
    return (
      <div style={{ padding: '8px 12px', borderTop: '1px solid #ddd', color: '#666', fontSize: '12px' }}>
        Showing {sportsData.length} items
      </div>
    );
  };

  return (
    <MultiSelectComponent
      id="mtselement"
      dataSource={sportsData}
      headerTemplate={headerTemplate}
      footerTemplate={footerTemplate}
      placeholder="Select sports"
    />
  );
}
```

---

## No Records and Action Failure Templates

Customize what appears when filtering returns no results, or when a remote data request fails:

```tsx
import { L10n } from '@syncfusion/ej2-base';
import { MultiSelectComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

// Custom JSX templates
const noRecordsTemplate = () => {
  return (
    <div style={{ padding: '12px', textAlign: 'center', color: '#999' }}>
      😕 No matching items found
    </div>
  );
};

const actionFailureTemplate = () => {
  return (
    <div style={{ padding: '12px', color: 'red' }}>
      ⚠️ Failed to load data. Please try again.
    </div>
  );
};

export default function App() {
  return (
    <MultiSelectComponent
      id="mtselement"
      dataSource={[]}
      allowFiltering={true}
      noRecordsTemplate={noRecordsTemplate}
      actionFailureTemplate={actionFailureTemplate}
      placeholder="Search items"
    />
  );
}
```

For text-only customization without JSX, use localization — see [accessibility-styling-localization.md](accessibility-styling-localization.md).

---

## Template Performance Tips

- **Keep templates simple:** Avoid heavy computation or nested components inside templates — they render for every visible item.
- **Avoid anonymous functions in JSX props:** Extract template functions outside the render cycle to prevent unnecessary re-renders.
- **Combine with virtual scrolling for large lists:** When using `itemTemplate` with 1000+ items, enable `enableVirtualization={true}` and inject `VirtualScroll` to minimize DOM nodes rendered.

```tsx
// ✅ Good — function defined outside component
const itemTemplate = (data: any) => { return <span>{data.name}</span>; };

export default function App() {
  return <MultiSelectComponent itemTemplate={itemTemplate} ... />;
}

// ❌ Avoid — new function created on every render
export default function App() {
  return <MultiSelectComponent itemTemplate={(data) => <span>{data.name}</span>} ... />;
}
```

## See Also

- [Grouping](grouping.md) — group headers and the `groupTemplate`
- [Filtering](filtering.md) — no-records behavior with filtering
- [Accessibility & Styling](accessibility-styling-localization.md) — text-based no-records via localization
- [Selection and Features](selection-and-features.md) — chip customization via `tagging` event
