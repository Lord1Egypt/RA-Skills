# Multi-Selection & Filtering

## Table of Contents
- [Multi-Selection with Ctrl/Shift Keys](#multi-selection-with-ctrlshift-keys)
- [Display Modes](#display-modes)
- [Enabling Filtering](#enabling-filtering)
- [Filter Types](#filter-types)
- [Filter Configuration Options](#filter-configuration-options)
- [Custom Filtering](#custom-filtering)

## Multi-Selection with Ctrl/Shift Keys

The Dropdown Tree supports multi-selection using keyboard modifiers without requiring checkboxes. This is distinct from checkbox-based selection and allows users to select multiple items by:
- **Ctrl+Click** to toggle individual selections
- **Shift+Click** to select a range of items

### Enable Multi-Selection

```tsx
import { DropDownTreeComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

function App() {
  const data = [
    { id: 1, name: 'Discover Music', hasChild: true, expanded: true },
    { id: 2, pid: 1, name: 'Hot Singles' },
    { id: 3, pid: 1, name: 'Rising Artists' },
    { id: 4, pid: 1, name: 'Live Music' },
  ];

  const fields = { 
    dataSource: data, 
    value: 'id', 
    text: 'name', 
    parentValue: 'pid', 
    hasChildren: 'hasChild' 
  };

  return (
    <DropDownTreeComponent
      id="dropdowntree"
      fields={fields}
      allowMultiSelection={true}
      placeholder="Select multiple items with Ctrl/Shift"
    />
  );
}

export default App;
```

**Key Differences from Checkboxes:**
- No visible checkboxes
- Selection via Ctrl/Shift keys only
- More subtle UI, suitable for minimal interfaces
- Cannot show all selections in input (limited to mode setting)

## Display Modes

The `mode` property controls how selected items are displayed in the input field. Combined with `allowMultiSelection` or `showCheckBox`, it provides different visual representations.

### Mode: Default

Shows all selected item values separated by a delimiter character (default: comma and space).

```tsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  allowMultiSelection={true}
  mode="Default"
  delimiterChar=", "
  placeholder="Select multiple items"
/>
```

**Display Example:** `"Hot Singles, Rising Artists, Live Music"`

### Mode: Delimiter

Displays selected items with a custom delimiter. Similar to Default but emphasizes custom formatting.

```tsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  showCheckBox={true}
  mode="Delimiter"
  delimiterChar=" | "
  placeholder="Select items"
/>
```

**Display Example:** `"Hot Singles | Rising Artists | Live Music"`

### Mode: Custom

Displays a custom template instead of showing all selected values. Useful for space-constrained UIs or custom display logic.

```tsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  showCheckBox={true}
  mode="Custom"
  customTemplate="${value.length} item(s) selected"
  placeholder="Select items"
/>
```

**Display Example:** `"3 item(s) selected"`

### Custom Template Syntax

The `customTemplate` property supports variable interpolation:

```tsx
// Count format
customTemplate="${value.length} item(s) selected"

// Formatted count
customTemplate="Selected: ${value.length}"

// With custom styling function
customTemplate={function(value) {
  return value.length > 3 
    ? `${value.length} items selected` 
    : value.join(', ');
}}
```

## Enabling Filtering

The filter feature allows users to search through tree items as they type. Enable it with the `allowFiltering` property.

### Basic Filtering

```tsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  allowFiltering={true}
  filterBarPlaceholder="Search items..."
  placeholder="Select an item"
/>
```

**Result:**
- Filter bar appears above the tree items
- User types to search
- Items matching the filter remain visible
- Non-matching items are hidden

### Filtering with Custom Placeholder

```tsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  allowFiltering={true}
  filterBarPlaceholder="Type to find..."
  placeholder="Select from dropdown"
/>
```

## Filter Types

The `filterType` property determines the matching strategy for search queries.

### StartsWith (Default)

Matches items that start with the search text.

```tsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  allowFiltering={true}
  filterType="StartsWith"
  placeholder="Search by starting text"
/>
```

**Example:**
- Search: "Hot" → Matches: "Hot Singles"
- Search: "Singles" → No match

### EndsWith

Matches items that end with the search text.

```tsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  allowFiltering={true}
  filterType="EndsWith"
  placeholder="Search by ending text"
/>
```

**Example:**
- Search: "Singles" → Matches: "Hot Singles"
- Search: "Hot" → No match

### Contains

Matches items containing the search text anywhere in the item.

```tsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  allowFiltering={true}
  filterType="Contains"
  placeholder="Search anywhere in item"
/>
```

**Example:**
- Search: "ing" → Matches: "Rising Artists", "Live Music", "Hot Singles"
- Search: "Live" → Matches: "Live Music"

## Filter Configuration Options

### Case-Sensitive Filtering

By default, filtering is case-insensitive. Enable case sensitivity with `ignoreCase={false}`.

```tsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  allowFiltering={true}
  ignoreCase={false}
  filterType="Contains"
  placeholder="Case-sensitive search"
/>
```

**Example:**
- Search: "hot" → No match (requires "Hot")
- Search: "Hot" → Matches: "Hot Singles"

### Ignore Diacritics/Accents

By default, diacritics are considered. Set `ignoreAccent={true}` to ignore them.

```tsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  allowFiltering={true}
  ignoreAccent={true}
  filterType="Contains"
  placeholder="Accent-insensitive search"
/>
```

**Example:**
- Search: "cafe" → Matches: "café", "cafe", "Café"
- Search: "é" → Matches: "Café" only

### Combined Filter Options

```tsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  allowFiltering={true}
  filterType="Contains"
  ignoreCase={true}
  ignoreAccent={true}
  filterBarPlaceholder="Search (any case, any accent)..."
  placeholder="Select item"
/>
```

## Custom Filtering

Handle custom filtering logic using the `onFiltering` event. This allows you to implement custom filter algorithms or external data sources.

### Custom Filtering Event

```tsx
import { DropDownTreeComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

function App() {
  const data = [
    { id: 1, name: 'Discover Music', hasChild: true, expanded: true },
    { id: 2, pid: 1, name: 'Hot Singles' },
    { id: 3, pid: 1, name: 'Rising Artists' },
  ];

  const fields = { dataSource: data, value: 'id', text: 'name', parentValue: 'pid', hasChildren: 'hasChild' };

  const handleFiltering = (args) => {
    console.log('Filter text:', args.text); // User's search input
    console.log('Can prevent default filtering:', args.preventDefaultAction);
    
    // Implement custom filtering
    if (args.text.length > 3) {
      // Only filter if more than 3 characters
      args.preventDefaultAction = false;
    } else {
      // Show all if less than 3 characters
      args.preventDefaultAction = true;
    }
  };

  return (
    <DropDownTreeComponent
      id="dropdowntree"
      fields={fields}
      allowFiltering={true}
      onFiltering={handleFiltering}
      placeholder="Type to filter"
    />
  );
}

export default App;
```

### Prevent Default Filtering

Set `preventDefaultAction = true` to override the default filter behavior completely.

```tsx
const handleFiltering = (args) => {
  // Prevent default filtering
  args.preventDefaultAction = true;
  
  // Implement your own logic
  // Update the data source manually
  // Reset filtering, etc.
};
```

### Filtering Event Properties

The filtering event provides:
- `text` (string) - The filter text entered by user
- `event` (Event) - The input event object
- `fields` (FieldsModel) - Current field configuration
- `preventDefaultAction` (boolean) - Flag to prevent default filtering
- `cancel` (boolean) - Cancel the filtering operation

## Combining Multi-Selection & Filtering

Using multi-selection with filtering provides a powerful search and select interface.

```tsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  showCheckBox={true}
  allowFiltering={true}
  filterType="Contains"
  mode="Custom"
  customTemplate="${value.length} item(s) selected"
  treeSettings={{ autoCheck: true }}
  filterBarPlaceholder="Search and select..."
  placeholder="Select multiple items"
/>
```

**User Experience:**
1. User types in filter bar to narrow down items
2. Checkboxes visible on filtered results
3. User checks/unchecks items to select
4. Selected items counted in custom template
5. Auto-check synchronizes parent-child relationships

## Best Practices

1. **Choose appropriate filter type**: Use "Contains" for general search, "StartsWith" for predictable prefixes
2. **Combine with search bar**: Provide clear visual feedback when filter bar is available
3. **Handle large datasets**: Use filtering with lazy loading for performance
4. **Consider user intent**: For hierarchical data, preserve hierarchy visibility even when filtering
5. **Test localization**: Some languages may require specific filter configurations

## Troubleshooting

**Issue:** Filter bar not appearing
- **Solution:** Ensure `allowFiltering={true}` is set

**Issue:** Filtering not working on remote data
- **Solution:** Implement custom filtering with `onFiltering` event or handle on server-side

**Issue:** Partial items visible after filtering
- **Solution:** Adjust `filterType` or implement custom logic in `onFiltering`

**Issue:** Filter bar placeholder not showing
- **Solution:** Set `filterBarPlaceholder` property explicitly
