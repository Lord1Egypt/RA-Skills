# Tree Settings & Configuration

## Table of Contents
- [TreeSettings Overview](#treesettings-overview)
- [Auto Check Behavior](#auto-check-behavior)
- [Load On Demand (Lazy Loading)](#load-on-demand-lazy-loading)
- [Expand On Behavior](#expand-on-behavior)
- [Check Disabled Children](#check-disabled-children)
- [Complete Configuration Examples](#complete-configuration-examples)

## TreeSettings Overview

The `treeSettings` property is a `TreeSettingsModel` object that configures advanced tree behavior. It allows fine-tuning how the tree expands, collapses, checks items, and loads data.

### Basic TreeSettings Configuration

```tsx
const treeSettings = {
  autoCheck: true,           // Synchronize parent-child checkbox states
  loadOnDemand: false,       // Load all data upfront
  expandOn: 'Auto',          // Expand on double-click or tap
  checkDisabledChildren: false // Don't check disabled child nodes
};

<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  treeSettings={treeSettings}
/>
```

## Auto Check Behavior

When `autoCheck` is enabled, checking a parent automatically checks all children, and unchecking a parent unchecks all children. This creates hierarchical checkbox synchronization.

### Enable Auto Check

```tsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  showCheckBox={true}
  treeSettings={{ autoCheck: true }}
  placeholder="Select with hierarchy sync"
/>
```

### Auto Check States

The Dropdown Tree implements three checkbox states:

1. **Checked** - Parent is checked, all children are checked
2. **Unchecked** - Parent is unchecked, all children are unchecked
3. **Intermediate** - Parent has mixed state (some children checked, some unchecked)

```tsx
import { DropDownTreeComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

function App() {
  const data = [
    { id: 1, name: 'Fruits', hasChild: true, expanded: true },
    { id: 2, pid: 1, name: 'Apple' },
    { id: 3, pid: 1, name: 'Orange' },
    { id: 4, pid: 1, name: 'Banana' },
    { id: 5, name: 'Vegetables', hasChild: true },
    { id: 6, pid: 5, name: 'Carrot' },
    { id: 7, pid: 5, name: 'Cucumber' },
  ];

  const fields = { 
    dataSource: data, 
    value: 'id', 
    text: 'name', 
    parentValue: 'pid', 
    hasChildren: 'hasChild' 
  };

  const handleSelect = (args) => {
    console.log('Item:', args.itemData.name);
    console.log('Action:', args.action); // 'select' or 'unselect'
  };

  return (
    <DropDownTreeComponent
      id="dropdowntree"
      fields={fields}
      showCheckBox={true}
      treeSettings={{ autoCheck: true }}
      onSelect={handleSelect}
      placeholder="Select items"
    />
  );
}

export default App;
```

### Auto Check Workflow

1. User checks parent "Fruits" → All children (Apple, Orange, Banana) automatically checked
2. User unchecks child "Apple" → Parent "Fruits" becomes intermediate state
3. User checks "Apple" again → Parent "Fruits" returns to fully checked
4. All children checked → Parent automatically becomes checked

### Disable Auto Check for Specific Nodes

To prevent auto-check on specific nodes, use the `selectable` field:

```tsx
const data = [
  { id: 1, name: 'Fruits', hasChild: true, expanded: true },
  { id: 2, pid: 1, name: 'Apple' },
  { id: 3, pid: 1, name: 'Orange', selectable: false }, // Cannot be checked
];
```

## Load On Demand (Lazy Loading)

Load on demand (lazy loading) improves performance by loading only parent nodes initially and fetching child nodes when the parent is expanded.

### Enable Load On Demand

```tsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  treeSettings={{ loadOnDemand: true }}
  placeholder="Data loads as you expand"
/>
```

### How Lazy Loading Works

1. **Initial load**: Only root-level items displayed
2. **User expands a parent**: Child items fetched from data source
3. **Child level expanded**: Next-level children fetched (if applicable)
4. **Repeated**: Process continues for deeper hierarchy levels

### Lazy Loading with Remote Data

```tsx
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';
import { DropDownTreeComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const data = new DataManager({
    url: 'url',
    adaptor: new ODataV4Adaptor,
    crossDomain: true,
  });

  const query = new Query().from('Employees').select('EmployeeID,FirstName,Title').take(10);
  
  const query1 = new Query()
    .from('Orders')
    .select('OrderID,EmployeeID,ShipName')
    .take(10);

  const fields = {
    dataSource: data,
    query: query,
    value: 'EmployeeID',
    text: 'FirstName',
    hasChildren: 'EmployeeID',
    child: {
      dataSource: data,
      query: query1,
      value: 'OrderID',
      parentValue: 'EmployeeID',
      text: 'ShipName'
    }
  };

  return (
    <DropDownTreeComponent
      id="dropdowntree"
      fields={fields}
      treeSettings={{ loadOnDemand: true }}
      placeholder="Lazy loading from server"
    />
  );
}

export default App;
```

### Performance Considerations

- **Reduce initial payload**: Only first-level items loaded
- **Faster initial render**: Component displays quicker
- **Network requests**: Additional requests made when expanding nodes
- **Caching**: Expanded nodes cached, no re-fetch on re-expand
- **Best for**: 1000+ items, deeply nested hierarchies, remote data

## Expand On Behavior

The `expandOn` property controls which user action triggers expand/collapse of parent nodes.

### ExpandOn: Auto (Default)

- Desktop: Double-click to expand/collapse
- Mobile: Single tap to expand/collapse

```tsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  treeSettings={{ expandOn: 'Auto' }}
/>
```

### ExpandOn: Click

Single-click/tap on any parent expands or collapses it. Works consistently on desktop and mobile.

```tsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  treeSettings={{ expandOn: 'Click' }}
/>
```

### ExpandOn: DblClick

Double-click required to expand/collapse. Single-click selects the item.

```tsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  treeSettings={{ expandOn: 'DblClick' }}
/>
```

### ExpandOn: None

No expand/collapse on user interaction. Tree expansion must be controlled programmatically or via `expanded` field.

```tsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  treeSettings={{ expandOn: 'None' }}
/>
```

### Setting Initial Expanded State

Use the `expanded` field in data to control which nodes are initially expanded:

```tsx
const data = [
  { id: 1, name: 'Fruits', hasChild: true, expanded: true }, // Initially expanded
  { id: 2, pid: 1, name: 'Apple' },
  { id: 3, id: 'Vegetables', hasChild: true, expanded: false }, // Initially collapsed
  { id: 4, pid: 3, name: 'Carrot' },
];
```

## Check Disabled Children

The `checkDisabledChildren` property determines whether disabled child nodes are checked when their parent is checked.

### Default Behavior (checkDisabledChildren: false)

Disabled children are NOT checked when parent is checked.

```tsx
const data = [
  { id: 1, name: 'Fruits', hasChild: true, expanded: true },
  { id: 2, pid: 1, name: 'Apple' },
  { id: 3, pid: 1, name: 'Orange', selectable: false }, // Disabled
];

<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  showCheckBox={true}
  treeSettings={{ autoCheck: true, checkDisabledChildren: false }}
/>
```

**Result:**
- User checks "Fruits" → Only "Apple" checked (not "Orange" as it's disabled)

### Enable Check Disabled Children

When enabled, disabled children are also checked when parent is checked.

```tsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  showCheckBox={true}
  treeSettings={{ autoCheck: true, checkDisabledChildren: true }}
/>
```

**Result:**
- User checks "Fruits" → Both "Apple" and "Orange" checked (including disabled)
- "Orange" remains visually disabled but is marked as checked in data

### Use Cases for Check Disabled Children

**Example 1: Track all selections regardless of state**
```tsx
treeSettings={{ checkDisabledChildren: true }}
```

**Example 2: Restrict user interaction but track in data**
```tsx
const data = [
  { id: 1, name: 'Admin', hasChild: true },
  { id: 2, pid: 1, name: 'Delete Users', selectable: false }, // User can't interact but can be checked via parent
];
```

## Complete Configuration Examples

### Example 1: Optimal for User-Friendly Multi-Select

```tsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  showCheckBox={true}
  showSelectAll={true}
  treeSettings={{
    autoCheck: true,
    loadOnDemand: false,
    expandOn: 'Click',
    checkDisabledChildren: false
  }}
  placeholder="Select items with automatic hierarchy"
/>
```

### Example 2: High-Performance with Remote Data

```tsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={remoteFields}
  treeSettings={{
    autoCheck: false,
    loadOnDemand: true,
    expandOn: 'Click',
    checkDisabledChildren: false
  }}
  placeholder="Lazy-loaded remote data"
/>
```

### Example 3: Programmatic Control Only

```tsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  showCheckBox={true}
  treeSettings={{
    autoCheck: false,
    loadOnDemand: false,
    expandOn: 'None',
    checkDisabledChildren: true
  }}
  placeholder="Fully programmatically controlled"
/>
```

### Example 4: Accessibility-Focused Configuration

```tsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  showCheckBox={true}
  treeSettings={{
    autoCheck: true,
    loadOnDemand: false,
    expandOn: 'Click', // Single-click for accessibility
    checkDisabledChildren: false
  }}
  allowFiltering={true}
  filterBarPlaceholder="Search items..."
  placeholder="Accessible multi-select dropdown"
/>
```

## Best Practices

1. **Use autoCheck with checkboxes**: Simplifies user interaction and data management
2. **Enable loadOnDemand for large datasets**: Improves initial load performance
3. **Choose expandOn carefully**: 'Click' is most accessible, 'Auto' is standard
4. **Test with keyboard navigation**: Ensure tree behavior works with keyboard
5. **Document tree behavior**: Clear UX communication about expand/collapse mechanics

## Troubleshooting

**Issue:** Parent doesn't auto-check when all children are checked manually
- **Solution:** Ensure `autoCheck: true` in treeSettings

**Issue:** Children nodes still loading after parent expands
- **Solution:** Verify remote data source configuration and network requests

**Issue:** Disabled children preventing parent check action
- **Solution:** Consider `checkDisabledChildren: true` or remove from data

**Issue:** Double-click not expanding nodes on mobile
- **Solution:** Change `expandOn` from 'Auto' or 'DblClick' to 'Click'
