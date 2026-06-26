# Checkbox & Multi-Selection

## Table of Contents

- [Basic Checkbox Support](#basic-checkbox-support)
- [Multi-Selection Workflow](#multi-selection-workflow)
- [Auto-Check Hierarchy](#auto-check-hierarchy)
- [Select All Feature](#select-all-feature)
- [Getting Selected Values](#getting-selected-values)
- [Clearing Selection](#clearing-selection)

## Basic Checkbox Support

Enable checkboxes for multi-selection by setting `showCheckBox` property to true.

### Enable Checkboxes

```jsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={{
    dataSource: data,
    value: 'id',
    text: 'name',
    parentValue: 'parentId',
  }}
  showCheckBox={true}
  placeholder="Select multiple items"
/>
```

**What happens when enabled:**
- Checkbox appears before each item text
- Multiple items can be selected simultaneously
- Selected items remain checked even when popup closes
- Display shows selected items (or count if many)

### Example - Product Selection

```jsx
const products = [
  { id: '1', name: 'Electronics', expanded: true },
  { id: '2', name: 'Laptops', parentId: '1' },
  { id: '3', name: 'Desktops', parentId: '1' },
  { id: '4', name: 'Phones', parentId: '1' },
  { id: '5', name: 'Appliances' },
  { id: '6', name: 'Refrigerators', parentId: '5' },
];

function App() {
  return (
    <DropDownTreeComponent
      id="productTree"
      fields={{
        dataSource: products,
        value: 'id',
        text: 'name',
        parentValue: 'parentId',
      }}
      showCheckBox={true}
      placeholder="Select products"
    />
  );
}
```

## Multi-Selection Workflow

### User Interactions

1. **Click dropdown** → Opens tree with checkboxes
2. **Check items** → Click checkbox or item to select
3. **Expand/collapse** → Click arrow to show/hide children
4. **Multiple selections** → Check multiple items at different levels
5. **Close popup** → Selection persists and displays in input

### Display Behavior

**Single selection:** Shows the item text
```
Selected: "Laptops"
```

**Multiple selections:** Shows item count or comma-separated list
```
Selected: "Laptops, Desktops, Phones" 
// or
Selected: "+2 more.." (if many items)
```

### Access Selected Values

Use the `change` event (recommended) to track selected values, or keep the component controlled via a `value` state.

```jsx
import { useState } from 'react';

function App() {
  const [selectedNodes, setSelectedNodes] = useState([]);

  const handleChange = (e) => {
    // e.value contains the array of selected values in checkbox/multi-select modes
    setSelectedNodes(e.value || []);
  };

  return (
    <>
      <DropDownTreeComponent
        fields={{...}}
        showCheckBox={true}
        change={handleChange}
      />
      <button onClick={() => console.log('Selected:', selectedNodes)}>Get Selected</button>
    </>
  );
}
```

## Auto-Check Hierarchy

Enable hierarchical parent-child checkbox synchronization with `autoCheck` property.

### Without Auto-Check (Default)

```jsx
<DropDownTreeComponent
  showCheckBox={true}
  // Parent and child checkboxes are independent
/>
```

Parent and child checkboxes work independently:
- Checking parent does NOT check children
- Checking child does NOT affect parent
- User must manually manage relationships

### With Auto-Check

```jsx
<DropDownTreeComponent
  showCheckBox={true}
  treeSettings={{
    autoCheck: true,
  }}
/>
```

**Auto-Check Rules:**

1. **Check parent → All children checked**
   ```
   ✓ Electronics
     ✓ Laptops
     ✓ Phones
     ✓ Tablets
   ```

2. **Uncheck parent → All children unchecked**
   ```
   ☐ Electronics
     ☐ Laptops
     ☐ Phones
     ☐ Tablets
   ```

3. **Some children checked → Parent shows intermediate state**
   ```
   ◐ Electronics (partially checked)
     ✓ Laptops (checked)
     ☐ Phones (unchecked)
     ✓ Tablets (checked)
   ```

4. **All children checked → Parent automatically checked**
   ```
   ✓ Electronics
     ✓ Laptops
     ✓ Phones
     ✓ Tablets
   ```

### Complete Example

```jsx
const categoryData = [
  { id: '1', name: 'Electronics', expanded: true },
  { id: '2', name: 'Laptops', parentId: '1' },
  { id: '3', name: 'HP', parentId: '2' },
  { id: '4', name: 'Dell', parentId: '2' },
  { id: '5', name: 'Phones', parentId: '1' },
  { id: '6', name: 'iPhone', parentId: '5' },
  { id: '7', name: 'Samsung', parentId: '5' },
];

function App() {
  const [checked, setChecked] = useState([]);

  const handleChange = (e) => {
    setChecked(e.value || []);
  };

  return (
    <div style={{ padding: '20px' }}>
      <DropDownTreeComponent
        id="categoryTree"
        fields={{
          dataSource: categoryData,
          value: 'id',
          text: 'name',
          parentValue: 'parentId',
        }}
        showCheckBox={true}
        treeSettings={{ autoCheck: true }}
        placeholder="Select categories with auto-check"
        change={handleChange}
      />
      <button 
        onClick={() => console.log('Checked nodes:', checked)}
        style={{ marginTop: '10px', padding: '8px 16px' }}
      >
        Get Selected Items
      </button>
    </div>
  );
}

export default App;
```

## Select All Feature

Enable "Select All" checkbox in popup header to quickly select/deselect all items.

### Enable Select All

```jsx
<DropDownTreeComponent
  showCheckBox={true}
  showSelectAll={true}
  placeholder="Select items"
/>
```

**Behavior:**
- Checkbox appears in popup header
- Click to select/deselect ALL items
- Works independently of autoCheck setting
- Useful for large trees with many items

### Default Text

By default displays:
- **Check header:** "Select All"
- **Uncheck header:** "Unselect All"

### Customize Text

```jsx
<DropDownTreeComponent
  showCheckBox={true}
  showSelectAll={true}
  selectAllText="✓ Select Everything"
  unSelectAllText="✗ Deselect Everything"
/>
```

### Example - Survey Form

```jsx
const surveyOptions = [
  { id: '1', name: 'Category A', expanded: true },
  { id: '2', name: 'Option A1', parentId: '1' },
  { id: '3', name: 'Option A2', parentId: '1' },
  { id: '4', name: 'Option A3', parentId: '1' },
  { id: '5', name: 'Category B', expanded: true },
  { id: '6', name: 'Option B1', parentId: '5' },
  { id: '7', name: 'Option B2', parentId: '5' },
];

function App() {
  return (
    <div>
      <h3>Select your preferences</h3>
      <DropDownTreeComponent
        id="surveyTree"
        fields={{
          dataSource: surveyOptions,
          value: 'id',
          text: 'name',
          parentValue: 'parentId',
        }}
        showCheckBox={true}
        showSelectAll={true}
        selectAllText="Check All Preferences"
        unSelectAllText="Clear All Preferences"
        placeholder="Choose multiple options"
        treeSettings={{
          autoCheck: true,
        }}
      />
    </div>
  );
}

export default App;
```

## Getting Selected Values

### Method 1: Use the `change` event (recommended)

```jsx
const handleChange = (e) => {
  console.log('Checked node IDs:', e.value || []);
};

<DropDownTreeComponent change={handleChange} showCheckBox={true} {...props} />
```

### Method 2: Read the change event payload

```jsx
const handleChange = (e) => {
  // e.value contains selected IDs (array) in checkbox/multi-select modes
  console.log('Selected values:', e.value || []);
};

<DropDownTreeComponent change={handleChange} showCheckBox={true} {...props} />
```

### Method 3: Map selected IDs to full data objects using `e.value`

```jsx
const handleChange = (e) => {
  const checkedIds = e.value || [];
  const selectedItems = data.filter(item => checkedIds.includes(item.id.toString()));
  console.log('Full selected data:', selectedItems);
};

<DropDownTreeComponent change={handleChange} showCheckBox={true} {...props} />
```

## Clearing Selection

### Clear All Selections

```jsx
// Recommended: call the component `clear()` method via ref, or control `value` via state
const dropdownRef = useRef(null);

const handleClear = () => {
  // If you have a ref to the DropDownTree component instance, call clear()
  dropdownRef.current && dropdownRef.current.clear();
  // Or update the controlled `value` state to an empty array
  // setValue([]);
};

<>
  <DropDownTreeComponent ref={dropdownRef} {...props} />
  <button onClick={handleClear}>Clear All</button>
</>
```

### Programmatic Selection

```jsx
// Use a controlled `value` prop or set component properties instead of modifying internals
const [value, setValue] = useState([]);

const handleSelectSpecific = () => {
  setValue(['2', '5', '7']); // Set specific IDs
};

return (
  <>
    <DropDownTreeComponent value={value} fields={{...}} showCheckBox={true} />
    <button onClick={handleSelectSpecific}>Select Laptops & Phones</button>
  </>
);
```

### Use Cases

**Clear selection:**
- User clicks reset button
- Form submission complete
- Filter changed

**Programmatic selection:**
- Pre-select defaults for user
- Restore previous selections
- Implement filter or quick-select buttons
