---
name: syncfusion-react-dropdown-tree
description: Implement Syncfusion React Dropdown Tree component for hierarchical data selection with dropdown interaction. Use this when working with multi-select checkboxes, lazy loading, remote OData integration, custom templates, keyboard navigation, RTL support, or localized interfaces. Supports auto-check hierarchy, filtering, tree settings, comprehensive event handling, and full accessibility.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Dropdowns"
---

# Implementing Dropdown Tree

The Dropdown Tree component displays hierarchical data in a collapsible tree structure within a dropdown interface. It combines tree navigation with dropdown accessibility, supporting multi-selection via checkboxes, lazy loading for large datasets, comprehensive customization through templates and events, filtering, and full accessibility with RTL and localization support.

## When to Use This Skill

Use Dropdown Tree **immediately** when you need to:

- **Display hierarchical data** - Show nested categories, organizational structures, file trees, or department hierarchies
- **Enable multi-selection** - Allow users to select multiple items with checkbox support or keyboard modifiers
- **Support lazy loading** - Optimize performance with large datasets by loading children on demand
- **Customize display** - Use templates to format items, headers, footers, selected values, or error states
- **Implement filtering** - Enable search functionality with configurable filter types (StartsWith, EndsWith, Contains)
- **Ensure accessibility** - Provide WAI-ARIA compliance, keyboard navigation, and screen reader support
- **Support multiple languages** - Localize UI with customizable keys and RTL support
- **Bind remote data** - Integrate with OData, OData V4, Web APIs, or other remote data services
- **Handle complex selection logic** - Use events, auto-check hierarchy, or selective node disabling

## Component Overview

The Dropdown Tree features:

- **Hierarchical display**: Local (hierarchical/self-referential) and remote data sources with flexible binding
- **Multi-selection modes**: Checkboxes with auto-check, multi-select with Ctrl/Shift keys, single select (default)
- **Flexible templates**: Item, value, header, footer, noRecords, and actionFailure templates for custom rendering
- **Performance optimization**: Lazy loading (load-on-demand) for efficient large dataset handling
- **Search & filtering**: Built-in filter bar with configurable filter types and case sensitivity options
- **Comprehensive events**: change, select, dataBound, filtering, beforeOpen, focus, keyPress, and popup events
- **Accessibility**: Full WAI-ARIA (roles, attributes), keyboard navigation, screen reader support, WCAG 2.2 compliance
- **Localization**: Multi-language support with 4 customizable keys and locale override
- **RTL support**: Right-to-left layout rendering
- **Tree settings**: Advanced configuration (expandOn, autoCheck, loadOnDemand, checkDisabledChildren)
- **Field mapping**: Flexible data structure support (value, text, child, parentValue, expanded, hasChildren, selectable, iconCss, imageUrl, htmlAttributes)
- **Display modes**: Default, Delimiter, and Custom modes for selected items

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package dependencies (npm install command)
- React/TypeScript project setup (Vite and Create React App)
- Basic component implementation and initialization
- CSS imports and theme configuration
- First render and minimal working example

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Local data binding (hierarchical and self-referential structures)
- Remote data with DataManager and various adaptors (OData, OData V4, WebAPI, URL)
- Field mapping for value, text, child, parentValue, expanded, hasChildren
- Load on demand (lazy loading) for large datasets
- Preventing node selection with selectable field
- Query configuration for remote data services

### Checkbox & Multi-Selection
📄 **Read:** [references/checkbox-selection.md](references/checkbox-selection.md)
- Enabling checkbox support with `showCheckBox` property
- Multi-selection workflow and accessing selected values
- Auto-check hierarchical behavior (parent-child synchronization)
- Select All feature with customizable `selectAllText` and `unSelectAllText`
- Intermediate checkbox states for partial selection
- CheckDisabledChildren behavior for disabled nodes

### Templates
📄 **Read:** [references/templates.md](references/templates.md)
- Item template for custom list item rendering
- Value template for selected display customization
- Header template for static content above items
- Footer template for static content below items
- NoRecords template for empty state handling
- ActionFailure template for error state handling
- CustomTemplate for multi-select display customization
- Template expression syntax and data access patterns

### Multi-Selection & Filtering
📄 **Read:** [references/multi-selection-filtering.md](references/multi-selection-filtering.md)
- `allowMultiSelection` property and Ctrl/Shift keyboard interaction
- Display modes: Default, Delimiter, Custom
- `delimiterChar` and `mode` configuration
- `allowFiltering` and filter bar implementation
- Filter types: StartsWith, EndsWith, Contains
- `filterBarPlaceholder` customization
- `ignoreCase` and `ignoreAccent` options

### Tree Settings & Configuration
📄 **Read:** [references/tree-settings.md](references/tree-settings.md)
- `loadOnDemand` for lazy loading implementation
- `autoCheck` for hierarchical checkbox synchronization
- `expandOn` behavior (Auto, Click, DblClick, None)
- `checkDisabledChildren` for disabled node handling
- Tree expansion and collapse control

### Field Mapping & Custom Data Structures
📄 **Read:** [references/field-mapping.md](references/field-mapping.md)
- Core fields: value, text, dataSource, child, parentValue
- Node state fields: expanded, hasChildren, selected, selectable
- Display enhancement fields: iconCss, imageUrl, htmlAttributes
- Query and tableName for remote data
- Nested field mapping for hierarchical data

### Advanced Features & API Reference
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Properties (60+ properties with descriptions and examples)
- Methods (getSelectedNodes, getCheckedNodes, setCheckedNodes, etc.)
- Events (change, select, dataBound, filtering, beforeOpen, focus, keyPress, popup)
- Event arguments (EventArgs structures with property descriptions)
- Styling and CSS customization
- Performance optimization techniques

### Accessibility & Localization
📄 **Read:** [references/accessibility-localization.md](references/accessibility-localization.md)
- WCAG 2.2 and Section 508 compliance standards
- WAI-ARIA attributes and roles (listbox, treeitem, checkbox, group, etc.)
- Keyboard navigation shortcuts (Alt+Down, Arrow keys, Enter, Space, etc.)
- Screen reader and assistive technology support
- Localization keys (noRecordsTemplate, actionFailureTemplate, overflowCountTemplate, totalCountTemplate)
- Culture customization with locale property
- RTL (Right-to-Left) language support with enableRtl

## Quick Start

### Basic Dropdown Tree with Hierarchical Data

```jsx
import { DropDownTreeComponent } from '@syncfusion/ej2-react-dropdowns';
import '@syncfusion/ej2-dropdowns/styles/material.css';

function App() {
  const data = [
    { id: '1', name: 'Electronics', expanded: true },
    { id: '2', name: 'Laptops', parentId: '1' },
    { id: '3', name: 'Phones', parentId: '1' },
    { id: '4', name: 'Appliances' },
  ];

  return (
    <DropDownTreeComponent
      id="dropdowntree"
      fields={{ dataSource: data, value: 'id', text: 'name', parentValue: 'parentId', hasChildren: 'hasChild' }}
      placeholder="Select an item"
    />
  );
}

export default App;
```

### With Checkboxes and Auto-Check

```jsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={{ dataSource: data, value: 'id', text: 'name', parentValue: 'parentId', hasChildren: 'hasChild' }}
  showCheckBox={true}
  showSelectAll={true}
  treeSettings={{ autoCheck: true }}
  placeholder="Select items"
/>
```

### With Filtering

```jsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={{ dataSource: data, value: 'id', text: 'name', parentValue: 'parentId' }}
  allowFiltering={true}
  filterType="Contains"
  filterBarPlaceholder="Search items..."
  placeholder="Select an item"
/>
```

### With Custom Templates

```jsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={{ dataSource: data, value: 'id', text: 'name', parentValue: 'parentId' }}
  itemTemplate={(props) => (
    <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
      <span>{props.name}</span>
      <small style={{ color: '#999' }}>({props.category})</small>
    </div>
  )}
  valueTemplate={(props) => <span>{props.name}</span>}
  placeholder="Select item"
/>
```

## Common Patterns

### Pattern 1: Self-Referential Data Binding

For flat data structures with parent references:

```jsx
const data = [
  { id: 1, name: 'Discover Music', hasChild: true, expanded: true },
  { id: 2, pid: 1, name: 'Hot Singles' },
  { id: 3, pid: 1, name: 'Rising Artists' },
  { id: 7, name: 'Sales and Events', hasChild: true },
  { id: 8, pid: 7, name: '100 Albums' },
];

<DropDownTreeComponent
  id="dropdowntree"
  fields={{
    dataSource: data,
    value: 'id',
    text: 'name',
    parentValue: 'pid',
    hasChildren: 'hasChild',
  }}
/>
```

### Pattern 2: Event Handling for Selection Changes

```jsx
const handleChange = (args) => {
  console.log('Old values:', args.oldValue); // string[]
  console.log('New values:', args.value); // string[]
  console.log('User interaction:', args.isInteracted); // boolean
};

const handleSelect = (args) => {
  console.log('Action:', args.action); // 'select' or 'unselect'
  console.log('Item data:', args.itemData); // object
};

<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  onChange={handleChange}
  onSelect={handleSelect}
/>
```

### Pattern 3: Multi-Select with Auto-Check

```jsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  showCheckBox={true}
  treeSettings={{ autoCheck: true }}
  mode="Default"
  delimiterChar=", "
  placeholder="Select multiple items"
/>
```

### Pattern 4: Lazy Loading for Large Datasets

```jsx
const remoteData = new DataManager({
  url: 'url',
  adaptor: new UrlAdaptor(),
});

<DropDownTreeComponent
  id="dropdowntree"
  fields={{ dataSource: remoteData, value: 'id', text: 'name', hasChildren: 'hasChild' }}
  treeSettings={{ loadOnDemand: true }}
  placeholder="Loading..."
/>
```

### Pattern 5: Custom Item Styling with IconCss

```jsx
const data = [
  { id: 1, name: 'Documents', iconCss: 'e-folder', hasChild: true },
  { id: 2, pid: 1, name: 'Resume.pdf', iconCss: 'e-pdf' },
  { id: 3, pid: 1, name: 'Report.docx', iconCss: 'e-docx' },
];

<DropDownTreeComponent
  id="dropdowntree"
  fields={{
    dataSource: data,
    value: 'id',
    text: 'name',
    iconCss: 'iconCss',
    parentValue: 'pid',
    hasChildren: 'hasChild',
  }}
/>
```

### Pattern 6: RTL & Localization Support

```jsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  enableRtl={true}
  locale="ar"
  placeholder="اختر عنصرا"
/>
```

## Key Props Overview

| Property | Type | Description |
|----------|------|-------------|
| **Core** |
| `id` | string | Unique identifier for the component |
| `fields` | FieldsModel | Data source and field mapping configuration |
| `placeholder` | string | Input placeholder text |
| `enabled` | boolean | Enable/disable component (default: true) |
| **Selection** |
| `showCheckBox` | boolean | Enable checkbox multi-selection (default: false) |
| `showSelectAll` | boolean | Show Select All checkbox (default: false) |
| `selectAllText` | string | "Select All" label text |
| `unSelectAllText` | string | "Unselect All" label text |
| `allowMultiSelection` | boolean | Enable multi-selection with Ctrl/Shift keys |
| **Templates** |
| `itemTemplate` | string \| Function | Custom item rendering |
| `valueTemplate` | string \| Function | Custom selected value display |
| `headerTemplate` | string \| Function | Custom header content |
| `footerTemplate` | string \| Function | Custom footer content |
| `noRecordsTemplate` | string \| Function | Empty state template |
| `actionFailureTemplate` | string \| Function | Error state template |
| **Filtering** |
| `allowFiltering` | boolean | Enable search/filter bar (default: false) |
| `filterType` | TreeFilterType | Filter type: StartsWith, EndsWith, Contains |
| `filterBarPlaceholder` | string | Filter bar placeholder text |
| `ignoreCase` | boolean | Case-insensitive filtering (default: true) |
| `ignoreAccent` | boolean | Ignore diacritics in filtering |
| **Tree Settings** |
| `treeSettings` | TreeSettingsModel | Tree behavior configuration (autoCheck, loadOnDemand, expandOn) |
| **Display** |
| `mode` | string | Display mode: Default, Delimiter, Custom |
| `delimiterChar` | string | Delimiter for multi-select (default: ", ") |
| `customTemplate` | string | Custom multi-select display template |
| **Localization & RTL** |
| `locale` | string | Culture code (default: "en") |
| `enableRtl` | boolean | Enable Right-to-Left layout |
| `enablePersistence` | boolean | Persist state between page reloads |
| **Styling** |
| `cssClass` | string | CSS class for root and popup |
| `width` | string \| number | Component width |
| `popupHeight` | string \| number | Popup height |
| `htmlAttributes` | object | HTML attributes for the component |

## Decision Guide

**Choosing Data Binding:**
- **Local hierarchical** - Nested JSON objects with `child` property for small-to-medium datasets
- **Local self-referential** - Flat arrays with `parentValue` field for structured data
- **Remote with DataManager** - OData/Web API for large datasets, dynamic loading, real-time data

**Choosing Selection Mode:**
- **Single select** - Default (no checkboxes, no multi-select), read-only visual selection
- **Checkboxes** - `showCheckBox={true}` for explicit multi-selection
- **Multi-select** - `allowMultiSelection={true}` for Ctrl/Shift keyboard selection
- **Auto-check** - Combine checkboxes with `treeSettings={{ autoCheck: true }}` for hierarchy sync

**Choosing Template:**
- **itemTemplate** - Custom formatting per tree item (name + description, icons, badges)
- **valueTemplate** - Custom display in input field (combined text, formatted values)
- **headerTemplate** - Static controls above list (instructions, search help, custom controls)
- **footerTemplate** - Static content below list (count summary, action buttons)
- **noRecordsTemplate** - Empty state when no data or search yields no results
- **actionFailureTemplate** - Error message when data fetch fails

**When to Use Lazy Loading:**
- Large datasets (1000+ items)
- Performance-critical applications
- Data fetched from remote API with pagination
- Hierarchies with many levels

**When to Use Filtering:**
- Large datasets requiring search
- User-friendly discovery of items
- Reducing cognitive load for selection

## Next Steps

- **Get started** → Read [getting-started.md](references/getting-started.md)
- **Bind data** → Read [data-binding.md](references/data-binding.md)
- **Add checkboxes** → Read [checkbox-selection.md](references/checkbox-selection.md)
- **Enable filtering** → Read [multi-selection-filtering.md](references/multi-selection-filtering.md)
- **Configure trees** → Read [tree-settings.md](references/tree-settings.md)
- **Map fields** → Read [field-mapping.md](references/field-mapping.md)
- **Customize** → Read [templates.md](references/templates.md)
- **Access APIs** → Read [advanced-features.md](references/advanced-features.md)
- **Enhance UX** → Read [accessibility-localization.md](references/accessibility-localization.md)
