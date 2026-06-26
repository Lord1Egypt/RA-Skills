---
name: syncfusion-react-dropdowns
description: Comprehensive guide for implementing Syncfusion React dropdown components including AutoComplete, ComboBox, DropDownList, ListBox, Mention, MultiSelect, and MultiColumn ComboBox. Use this when building selection interfaces, data binding, filtering, cascading dropdowns, custom templates, and accessible dropdown experiences in React applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Dropdowns"
---

# Implementing Syncfusion React Dropdowns

## AutoComplete

The AutoComplete component provides a matched suggestion list as the user types into an input field, allowing selection from the filtered results. It supports local and remote data, rich filtering options, templates, grouping, virtualization, and full accessibility.

### Documentation and Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/autocomplete-getting-started.md)
- Package installation (`@syncfusion/ej2-react-dropdowns`)
- CSS imports and theme configuration
- Basic component setup (functional and class components)
- Binding a simple string array
- Configuring popup height and width (`popupHeight`, `popupWidth`)

#### Data Binding
📄 **Read:** [references/data-binding.md](references/autocomplete-data-binding.md)
- Array of strings or numbers
- Array of objects with `fields` mapping (`value`, `groupBy`, `iconCss`)
- Array of complex/nested objects (dot-notation field mapping)
- Remote data with `DataManager` (ODataV4Adaptor, WebApiAdaptor)
- Using `query` property to filter/select remote data
- `sortOrder` for alphabetical ordering

#### Filtering
📄 **Read:** [references/filtering.md](references/autocomplete-filtering.md)
- Filter types: `StartsWith`, `EndsWith`, `Contains`
- `suggestionCount` – limit number of suggestions
- `minLength` – minimum characters before search triggers
- `ignoreCase` – case-sensitive filtering
- `ignoreAccent` – diacritics filtering
- `debounceDelay` – delay filtering to reduce requests
- Custom filtering with the `filtering` event

#### Grouping
📄 **Read:** [references/grouping.md](references/autocomplete-grouping.md)
- Grouping items using `fields.groupBy`
- Fixed and inline group headers
- Custom group header with `groupTemplate`

#### Templates
📄 **Read:** [references/templates.md](references/autocomplete-templates.md)
- `itemTemplate` – customize each list item
- `groupTemplate` – customize group header
- `headerTemplate` – static popup header
- `footerTemplate` – static popup footer
- `noRecordsTemplate` – message when no data found
- `actionFailureTemplate` – message on remote fetch failure

#### Value Binding
📄 **Read:** [references/value-binding.md](references/autocomplete-value-binding.md)
- Binding primitive values (string, number)
- Object binding with `allowObjectBinding`
- Presetting selected values with the `value` property

#### Virtualization
📄 **Read:** [references/virtual-scroll.md](references/autocomplete-virtual-scroll.md)
- `enableVirtualization` for large datasets
- Injecting the `VirtualScroll` service
- Virtual scrolling with local data, remote data, and grouping
- Customizing item count with `query.take()`

#### Disabled Items
📄 **Read:** [references/disabled-items.md](references/autocomplete-disabled-items.md)
- Disabling items via `fields.disabled`
- `disableItem` method for dynamic disabling
- Disabling the entire component with `enabled={false}`

#### Accessibility and Localization
📄 **Read:** [references/accessibility-localization.md](references/autocomplete-accessibility-localization.md)
- WAI-ARIA roles and attributes
- Keyboard navigation shortcuts
- RTL support (`enableRtl`)
- Localization with `L10n` (noRecordsTemplate, actionFailureTemplate text)
- WCAG 2.2 compliance overview

#### Styling and Customization
📄 **Read:** [references/styling.md](references/autocomplete-styling.md)
- CSS class targets for wrapper, icon, focus, placeholder, selection
- Float label customization
- Popup item appearance
- `cssClass` property for custom class injection
- Popup resize (`allowResize`)
- Mandatory asterisk styling

#### How-To: Autofill, Highlight, and Icons
📄 **Read:** [references/how-to.md](references/autocomplete-how-to.md)
- `autofill` – suggest first matched item on Arrow Down
- `highlight` – highlight typed characters in suggestion list
- Icon support with `fields.iconCss`

#### API Reference
📄 **Read:** [references/api.md](references/autocomplete-api.md)
- All properties with types, defaults, and descriptions
- All methods with parameters and return types
- All events with descriptions

### Quick Start Example

> **Installation:** Pin packages to a specific major version to reduce supply-chain risk.
> ```bash
> npm install @syncfusion/ej2-react-dropdowns@^33.x.x @syncfusion/ej2-react-inputs@^33.x.x @syncfusion/ej2-base@^33.x.x
> ```

```tsx
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns'; // ^33.x.x
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-react-inputs/styles/tailwind3.css';
import '@syncfusion/ej2-react-dropdowns/styles/tailwind3.css';

const sportsData: string[] = [
  'Badminton', 'Basketball', 'Cricket', 'Football',
  'Golf', 'Hockey', 'Rugby', 'Snooker', 'Tennis'
];

export default function App() {
  return (
    <AutoCompleteComponent
      id="sports-ac"
      dataSource={sportsData}
      placeholder="Find a game"
    />
  );
}
```

### Common Patterns

#### Object data source with field mapping
```tsx
const sportsData = [
  { id: 'Game1', game: 'Badminton' },
  { id: 'Game2', game: 'Basketball' },
];
const fields = { value: 'game' };

<AutoCompleteComponent dataSource={sportsData} fields={fields} placeholder="Find a game" />
```

#### Remote data binding (security-first)

> **Security:** Do not call arbitrary third-party URLs directly from client code. Route external API calls through a trusted server-side proxy that enforces allowed endpoints, authentication, rate limits, and response validation.

```tsx
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';

// Use a controlled server proxy endpoint here. Do not use public third-party URLs directly.
const customerData = new DataManager({
  adaptor: new ODataV4Adaptor(),
  crossDomain: true,
  url: 'https://your-trusted-proxy.example/api/customers'
});
const query = new Query().from('Customers').select(['ContactName', 'CustomerID']).take(6);
const fields = { value: 'ContactName' };

<AutoCompleteComponent
  dataSource={customerData}
  query={query}
  fields={fields}
  sortOrder="Ascending"
  placeholder="Find a customer" />
```

#### Filtering with custom options
```tsx
<AutoCompleteComponent
  dataSource={sportsData}
  filterType="StartsWith"
  minLength={2}
  suggestionCount={5}
  debounceDelay={300}
  ignoreCase={true}
  placeholder="Type to search"
/>
```

#### Accessing methods via ref
```tsx
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';
import { useRef } from 'react';

export default function App() {
  const acRef = useRef<AutoCompleteComponent>(null);

  return (
    <>
      <AutoCompleteComponent ref={acRef} dataSource={sportsData} placeholder="Find a game" />
      <button onClick={() => acRef.current?.showPopup()}>Open</button>
      <button onClick={() => acRef.current?.clear()}>Clear</button>
    </>
  );
}
```

## ComboBox

The ComboBox component provides a dropdown input that allows users to type to filter or select from a predefined list. It supports local and remote data binding, custom values, filtering, grouping, templates, virtual scrolling, and full accessibility.

### Component Overview

The ComboBox is a **specialized dropdown input** that bridges typed input fields with selection lists. Key characteristics:

- **Hybrid input:** User can type to filter OR select from dropdown
- **Smart filtering:** Default filter searches by text, customizable for complex scenarios
- **Flexible data:** Supports strings, JSON objects, OData, Web APIs, DataManager
- **Rich UI:** Templates for items, headers, footers, selected values, no-results states
- **Performance:** Virtual scrolling efficiently handles thousands of items
- **Global ready:** Built-in localization, RTL support, ARIA attributes
- **Accessible:** Full keyboard navigation, screen reader support

> **Installation:** Pin packages to a specific major version to reduce supply-chain risk.
> ```bash
> npm install @syncfusion/ej2-react-dropdowns@^33.x.x
> ```

---

### Documentation Navigation Guide

Choose your starting point based on your task:

#### Getting Started
📄 **Read:** [references/getting-started.md](references/combobox-getting-started.md)

When to read:
- Setting up ComboBox in a new project
- First-time component implementation
- Understanding basic usage (class vs functional components)
- Adding CSS imports and themes
- Enabling custom values

#### Data Binding & Sources
📄 **Read:** [references/data-binding.md](references/combobox-data-binding.md)

When to read:
- Binding local data (string arrays, JSON objects)
- Connecting to remote APIs (OData, Web API, DataManager)
- Mapping object fields (text, value, groupBy, iconCss)
- Handling complex data transformations
- Understanding data source configuration

#### Filtering & Search Behavior
📄 **Read:** [references/filtering-and-search.md](references/combobox-filtering-and-search.md)

When to read:
- Implementing text filtering
- Creating custom filter functions
- Configuring search behavior (case sensitivity, partial matching)
- Performance optimization for large datasets
- Handling no-results scenarios

#### Grouping & Sorting
📄 **Read:** [references/grouping-and-sorting.md](references/combobox-grouping-and-sorting.md)

When to read:
- Organizing items into logical groups
- Customizing group header appearance
- Applying sort orders (ascending/descending)
- Combining grouping with filtering
- Multi-level grouping scenarios

#### Templates & Customization
📄 **Read:** [references/templates-and-customization.md](references/combobox-templates-and-customization.md)

When to read:
- Creating custom item templates
- Displaying rich content (images, icons, descriptions)
- Header/footer templates (e.g., action buttons, summaries)
- Selected value template formatting
- CSS class-based styling and theme customization

#### Advanced Features
📄 **Read:** [references/advanced-features.md](references/combobox-advanced-features.md)

When to read:
- Virtual scrolling for large datasets (10,000+ items)
- Internationalization (i18n) and language switching
- RTL (right-to-left) support for Arabic/Hebrew
- Accessibility compliance (WCAG 2.1, ARIA attributes)
- Disabled states and multi-select workflows
- Keyboard shortcuts and focus management

#### Styling & Theming
📄 **Read:** [references/styling-and-theming.md](references/combobox-styling-and-theming.md)

When to read:
- Applying built-in Syncfusion themes (Material, Bootstrap, Tailwind)
- CSS variable customization for brand colors
- Theme Studio integration for design customization
- Responsive design patterns
- Dark mode / light mode support

#### Popup Resizing
📄 **Read:** [references/popup-resizing.md](references/combobox-popup-resizing.md)

When to read:
- Allowing users to dynamically resize the dropdown
- Saving resize preferences across sessions
- Handling long content with custom templates
- Mobile-friendly dropdown sizing

#### How-To Guide
📄 **Read:** [references/how-to-guide.md](references/combobox-how-to-guide.md)

When to read:
- Implementing autofill (auto-complete while typing)
- Creating cascading/dependent dropdowns (Country → State → City)
- Displaying icons in list items
- Common practical implementation scenarios

#### Troubleshooting
📄 **Read:** [references/troubleshooting.md](references/combobox-troubleshooting.md)

When to read:
- Performance issues (slow rendering, lag)
- Data binding problems
- Migration from EJ1 ComboBox
- Common edge cases and workarounds
- Debugging tips and community resources

#### API Reference
📄 **Read:** [references/api.md](references/combobox-api.md)

When to read:
- Looking up a specific property, method, or event name and its type
- Understanding default values for any configuration option
- Checking event argument shapes (`ChangeEventArgs`, `FilteringEventArgs`, etc.)
- Reviewing all available methods for programmatic control
- Exploring interface models (`FieldSettingsModel`, `PopupEventArgs`, etc.)

---

### Quick Start Example

#### Installation & Setup

> **Installation:** Pin packages to a specific major version to reduce supply-chain risk.
> ```bash
> npm install @syncfusion/ej2-react-dropdowns@^33.x.x
> ```

#### Basic ComboBox (Functional Component)

```tsx
import { ComboBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-react-dropdowns/styles/tailwind3.css';

export default function App() {
  const sportsList = ['Badminton', 'Cricket', 'Football', 'Golf', 'Tennis'];

  return (
    <ComboBoxComponent 
      id="combobox"
      dataSource={sportsList}
      placeholder="Select a sport"
      allowCustom={true}
    />
  );
}
```

#### With Data Binding (JSON Objects)

```tsx
export default function App() {
  const sportsData = [
    { Id: 'game1', Game: 'Badminton', Players: 2 },
    { Id: 'game2', Game: 'Football', Players: 11 },
    { Id: 'game3', Game: 'Cricket', Players: 11 }
  ];

  const fields = { text: 'Game', value: 'Id' };

  return (
    <ComboBoxComponent 
      id="combobox"
      dataSource={sportsData}
      fields={fields}
      placeholder="Select a game"
      change={(e) => console.log('Selected:', e.value)}
    />
  );
}
```

---

### Common Patterns

#### Pattern 1: Filtered Search for User Selection
**Problem:** User needs to find items in a list of 500+ entries.  
**Solution:** Use filtering with controlled input to display only matching items. For very large datasets (5,000+ items), combine with `enableVirtualization` and inject `VirtualScroll`.

```tsx
import { ComboBoxComponent, Inject, VirtualScroll } from '@syncfusion/ej2-react-dropdowns';

const [filterValue, setFilterValue] = useState('');

<ComboBoxComponent 
  dataSource={largeDataset}
  fields={{ text: 'name', value: 'id' }}
  filtering={(e) => filterByName(e, 'name')}
  change={(e) => setFilterValue(e.value)}
  allowFiltering={true}
  enableVirtualization={true}
  popupHeight="200px"
>
  <Inject services={[VirtualScroll]} />
</ComboBoxComponent>
```

#### Pattern 2: Grouped Categories
**Problem:** Items need to be organized by type for clarity.  
**Solution:** Use groupBy field mapping with data grouped by category.

```tsx
const categorizedData = [
  { Category: 'Sports', Item: 'Cricket', value: 1 },
  { Category: 'Sports', Item: 'Football', value: 2 },
  { Category: 'Games', Item: 'Chess', value: 3 },
  { Category: 'Games', Item: 'Carrom', value: 4 }
];

const fields = { 
  text: 'Item', 
  value: 'value', 
  groupBy: 'Category' 
};

<ComboBoxComponent dataSource={categorizedData} fields={fields} />
```

#### Pattern 3: Remote Data with Loading (security-first)
**Problem:** Fetch data from an API based on user search.

**Security-first solution:** Route external API requests through a trusted server-side proxy that validates and sanitizes responses. Do **not** embed third‑party URLs directly in client-side code.

```tsx
import { DataManager, WebApiAdaptor } from '@syncfusion/ej2-data';

// Use your server-side proxy here. The proxy should enforce allowed upstream hosts and
// sanitize responses before returning to the client.
const dataManager = new DataManager({
  url: 'https://your-trusted-proxy.example/api/search',
  adaptor: new WebApiAdaptor()
});

<ComboBoxComponent 
  dataSource={dataManager}
  fields={{ text: 'name', value: 'id' }}
  allowFiltering={true} />
```

#### Pattern 4: Custom Template for Rich Content
**Problem:** Display icons or additional info with each item.  
**Solution:** Use itemTemplate prop for custom HTML rendering.

```tsx
const itemTemplate = (props) => {
  return (
    <div className="flex items-center gap-2">
      <span className={`icon icon-${props.value}`}></span>
      <span>{props.name}</span>
      <small className="text-gray-500">({props.players} players)</small>
    </div>
  );
};

<ComboBoxComponent 
  dataSource={sportsData}
  itemTemplate={itemTemplate}
  fields={{ text: 'name', value: 'id' }}
/>
```

---

### Key Props Reference

| Prop | Type | Description | Common Use |
|------|------|-------------|-----------|
| `dataSource` | Array\|DataManager | Data items to display | All use cases |
| `fields` | FieldSettingsModel | Map data fields (text, value, groupBy, iconCss, disabled) | Complex data |
| `placeholder` | string | Hint text when empty | UX guidance |
| `allowCustom` | boolean | Allow user to enter custom values not in the list. Default: `true` | Open-ended input |
| `allowFiltering` | boolean | Enable filter bar (search box) in the popup. Default: `false` | Search capability |
| `enableVirtualization` | boolean | Enable virtual scrolling for large datasets. Requires `<Inject services={[VirtualScroll]} />`. Default: `false` | Large datasets (5,000+ items) |
| `sortOrder` | SortOrder | `'None'` \| `'Ascending'` \| `'Descending'`. Default: `null` | Sorted lists |
| `popupHeight` | string\|number | Dropdown height (e.g., `'300px'`). Default: `'300px'` | Layout control |
| `popupWidth` | string\|number | Dropdown width (e.g., `'100%'`). Default: `'100%'` | Layout control |
| `enabled` | boolean | Enable/disable component. Default: `true` | Conditional rendering |
| `readonly` | boolean | Prevent user input. Default: `false` | View-only mode |
| `showClearButton` | boolean | Show clear (×) button. Default: `true` | Allow clearing selection |
| `change` | EmitType\<ChangeEventArgs\> | Fires when selection changes | Event handling |
| `filtering` | EmitType\<FilteringEventArgs\> | Fires when user types; use for custom filter logic | Advanced search |
| `itemTemplate` | Function\|string | Custom item HTML for each list item | Rich UI |

---

### Next Steps

1. **New to ComboBox?** → Start with [getting-started.md](references/combobox-getting-started.md)
2. **Need specific data?** → Go to [data-binding.md](references/combobox-data-binding.md)
3. **Performance concerns?** → Check [advanced-features.md](references/combobox-advanced-features.md)
4. **Design customization?** → See [styling-and-theming.md](references/combobox-styling-and-theming.md)
5. **Common scenarios?** → Explore [how-to-guide.md](references/combobox-how-to-guide.md) (autofill, cascading, icons)
6. **Resizable dropdowns?** → Read [popup-resizing.md](references/combobox-popup-resizing.md)
7. **Stuck?** → Visit [troubleshooting.md](references/combobox-troubleshooting.md)
8. **Need full API details?** → See [api.md](references/combobox-api.md) for all properties, methods, events, and interface models

## DropDownList

The DropDownList component provides a list of predefined values from which users can select a single value. It supports local and remote data binding, filtering, grouping, custom templates, virtual scrolling, accessibility, and rich customization.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/dropdownlist-getting-started.md)
- Installation and package setup (`@syncfusion/ej2-react-dropdowns`)
- CSS imports with tailwind3 theme
- Basic DropDownList (functional and class components)
- Binding a data source
- Configuring popup height and width

#### Data Binding & Value Binding
📄 **Read:** [references/data-binding.md](references/dropdownlist-data-binding.md)
- Binding primitive arrays (strings, numbers)
- Binding JSON object arrays with `fields` mapping (`text`, `value`, `groupBy`, `iconCss`)
- Remote data with `DataManager` (OData, ODataV4, WebAPI adaptors)
- Value binding: preselecting values, binding primitive vs. complex objects
- Disabling individual items with `fields.disabled`

#### Filtering
📄 **Read:** [references/filtering.md](references/dropdownlist-filtering.md)
- Enabling `allowFiltering` for search-as-you-type
- Handling the `filtering` event with `updateData`
- **Preventing default filtering** — always set `args.preventDefaultAction = true` in custom handlers
- Filter types: `startswith`, `contains`, `endsWith`, case-sensitive options
- **Filtering by multiple fields** — use `Predicate` with `.or()` to match typed text against both `text` and `value` fields (or any combination)
- Remote/server-side filtering with minimum character guard
- Diacritics filtering (`ignoreAccent`), debounce delay
- Highlight filtered text, custom search logic

#### Grouping & Templates
📄 **Read:** [references/grouping-and-templates.md](references/dropdownlist-grouping-and-templates.md)
- Grouping items with the `groupBy` field
- Fixed and inline group headers
- Custom group header template
- Item template, value (selected) template
- Header and footer templates
- No-records and action-failure templates

#### Features & Configuration
📄 **Read:** [references/features-and-configuration.md](references/dropdownlist-features-and-configuration.md)
- Sorting (`sortOrder`: ascending, descending)
- Virtual scrolling for large lists (`enableVirtualization`)
- Popup resize (`allowResize`)
- Incremental search, clear button, readonly, disabled
- RTL support, Preact usage

#### Accessibility, Styling & Localization
📄 **Read:** [references/accessibility-styling-localization.md](references/dropdownlist-accessibility-styling-localization.md)
- WCAG 2.2 / Section 508 compliance
- Keyboard navigation shortcuts
- ARIA roles and attributes
- **`cssClass` prop** — scoped per-instance CSS class, multiple classes, conditional classes, built-in utility classes (`e-error`, `e-success`)
- CSS class customization (wrapper, icon, popup, list items, placeholder)
- Theming (tailwind3, material3, bootstrap5, fluent2)
- Localization (`L10n`, `noRecordsTemplate`, `actionFailureTemplate`)
- RTL layout (`enableRtl`)

#### API Reference
📄 **Read:** [references/api.md](references/dropdownlist-api.md)
- Complete properties reference with types, defaults, and usage examples
- All methods with signatures, parameters, and return types
- All events with argument interfaces and usage examples
- Interface details: `FieldSettingsModel`, `ChangeEventArgs`, `SelectEventArgs`, `PopupEventArgs`, `FilteringEventArgs`
- Quick-reference summary tables for properties, methods, and events

#### How-To Patterns
📄 **Read:** [references/how-to.md](references/dropdownlist-how-to.md)
- Add, remove, or modify items dynamically
- Cascading (dependent) dropdowns
- Multiple cascading dropdowns
- Remote data how-to
- Close popup on scroll, tooltip on items, icons in items
- Value change event, clearing selected value

---

### Quick Start Example

> **Installation:** Pin packages to a specific major version to reduce supply-chain risk.
> ```bash
> npm install @syncfusion/ej2-react-dropdowns@^33.x.x --save
> ```

```tsx
// 1. See pinned install command above.

// 2. CSS in src/App.css
// @import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
// @import "../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css";
// @import "../node_modules/@syncfusion/ej2-react-dropdowns/styles/tailwind3.css";

import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';
import './App.css';

export default function App() {
  const sportsData: string[] = ['Badminton', 'Cricket', 'Football', 'Golf', 'Tennis'];

  return (
    <DropDownListComponent
      id="ddlelement"
      dataSource={sportsData}
      placeholder="Select a game"
    />
  );
}
```

### Common Patterns

#### JSON Object Data with Fields Mapping
```tsx
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const countryData = [
    { Id: 'au', Country: 'Australia' },
    { Id: 'br', Country: 'Brazil' },
    { Id: 'cn', Country: 'China' },
    { Id: 'in', Country: 'India' },
  ];
  const fields = { text: 'Country', value: 'Id' };

  return (
    <DropDownListComponent
      dataSource={countryData}
      fields={fields}
      placeholder="Select a country"
    />
  );
}
```

#### Filtering (Search-as-you-type)
```tsx
import { DropDownListComponent, FilteringEventArgs } from '@syncfusion/ej2-react-dropdowns';
import { Query } from '@syncfusion/ej2-data';

export default function App() {
  const searchData = [
    { Index: 's1', Country: 'Alaska' },
    { Index: 's2', Country: 'California' },
    { Index: 's3', Country: 'Florida' },
  ];
  const fields = { text: 'Country', value: 'Index' };

  function onFiltering(args: FilteringEventArgs) {
    // Local example: updateData is applied against local `searchData` below.
    // For remote filtering, route requests through a trusted server proxy and
    // validate/sanitize responses before calling `updateData`.
    args.preventDefaultAction = true; // prevent built-in filter from running alongside custom logic
    let query = new Query();
    query = args.text !== '' ? query.where('Country', 'startswith', args.text, true) : query;
    args.updateData(searchData, query);
  }

  return (
    <DropDownListComponent
      dataSource={searchData}
      fields={fields}
      allowFiltering={true}
      filtering={onFiltering}
      placeholder="Select a country"
    />
  );
}
```

#### Preselect a Value
```tsx
<DropDownListComponent
  dataSource={sportsData}
  value="Cricket"
  placeholder="Select a game"
/>
```

#### Grouped Items
```tsx
const vegetableData = [
  { Vegetable: 'Cabbage', Category: 'Leafy and Salad', Id: 'item1' },
  { Vegetable: 'Chickpea', Category: 'Beans', Id: 'item6' },
  { Vegetable: 'Garlic',   Category: 'Bulb and Stem', Id: 'item9' },
];
const fields = { groupBy: 'Category', text: 'Vegetable', value: 'Id' };

<DropDownListComponent dataSource={vegetableData} fields={fields} placeholder="Select a vegetable" />
```

### Key Props

| Prop | Type | Purpose |
|---|---|---|
| `dataSource` | `any[] \| DataManager` | Data for the list items |
| `fields` | `FieldSettingsModel` | Maps `text`, `value`, `groupBy`, `iconCss`, `disabled` |
| `value` | `string \| number` | Selected/preselected value |
| `placeholder` | `string` | Input placeholder text |
| `allowFiltering` | `boolean` | Enables search filtering |
| `filtering` | `event` | Handler for custom filter logic |
| `popupHeight` | `string` | Popup list height (default auto) |
| `popupWidth` | `string` | Popup list width (default matches input) |
| `sortOrder` | `SortOrder` | `'None'`, `'Ascending'`, `'Descending'` |
| `enableVirtualization` | `boolean` | Virtual scroll for large data |
| `allowResize` | `boolean` | User-resizable popup |
| `enabled` | `boolean` | Enable/disable entire component |
| `readonly` | `boolean` | Read-only mode |
| `showClearButton` | `boolean` | Shows ✕ button to clear selection |
| `enableRtl` | `boolean` | Right-to-left layout |

### Common Use Cases

**Simple static list** → Pass `string[]` to `dataSource`, done.

**Data from API** → Use `DataManager` with `WebApiAdaptor`; read `references/data-binding.md`.

**Search/filter as user types** → Set `allowFiltering={true}`, handle `filtering` event; read `references/filtering.md`.

**Categorized items** → Map `groupBy` field; read `references/grouping-and-templates.md`.

**Custom item layout** → Use `itemTemplate`; read `references/grouping-and-templates.md`.

**Large dataset (10k+ items)** → Enable `enableVirtualization` + inject `VirtualScroll`; read `references/features-and-configuration.md`.

**Dependent dropdowns** → Reload second dropdown's `dataSource` on first's `change` event; read `references/how-to.md`.

## ListBox

The Syncfusion ListBox component displays a list of items in a scrollable container, enabling single or multiple selection. It supports local and remote data binding, drag-and-drop reordering, filtering, grouping, custom templates, dual-list transfer, and full accessibility.

### Documentation Guide

Navigate to specific topics based on your implementation needs:

#### Getting Started
📄 **Read:** [references/getting-started.md](references/listbox-getting-started.md)
- React app setup (Vite/Create React App)
- Installing Syncfusion packages
- CSS imports and theming
- Basic ListBox component creation
- Running the application

#### Selection & Events
📄 **Read:** [references/selection.md](references/listbox-selection.md)
- Single selection mode
- Multiple selection mode
- Selection events and handlers
- Programmatic selection management
- Working with selected items

#### Data Binding & Structure
📄 **Read:** [references/data-binding.md](references/listbox-data-binding.md)
- Array and object data binding
- Text and value properties
- Data source configuration
- Grouping data
- Hierarchical data structures

#### Custom Templates & Icons
📄 **Read:** [references/icons-and-templates.md](references/listbox-icons-and-templates.md)
- Icon rendering in items
- Custom item templates
- HTML content rendering
- Template variables and syntax
- Conditional rendering

#### Advanced Features
📄 **Read:** [references/features.md](references/listbox-features.md)
- Drag and drop functionality
- Filtering and search
- Sorting and grouping
- Dual ListBox (transfer list)
- Scroller configuration
- Item enable/disable

#### Styling & Appearance
📄 **Read:** [references/style-and-appearance.md](references/listbox-style-and-appearance.md)
- CSS class customization
- Theme integration
- Styling items and groups
- Responsive design
- Custom CSS variables

#### Accessibility
📄 **Read:** [references/accessibility.md](references/listbox-accessibility.md)
- WCAG 2.2 compliance
- Keyboard navigation
- ARIA attributes
- Screen reader support
- RTL (right-to-left) support

#### How-To Guides
📄 **Read:** [references/how-to-guides.md](references/listbox-how-to-guides.md)
- Add items dynamically
- Select items programmatically
- Enable/disable items
- Filter ListBox data
- Enable scroller for long lists
- Form integration & submission

#### Dual ListBox (Transfer)
📄 **Read:** [references/dual-list-box.md](references/listbox-dual-list-box.md)
- Two-way item transfer between lists
- Toolbar operations (move up/down, transfer)
- Permission and skill assignment patterns
- Custom styling and responsive design
- Capacity limits and validation

#### API Reference
📄 **Read:** [references/api.md](references/listbox-api.md)
- Complete list of all properties with types and defaults
- All public methods with parameter details and return types
- All events with full event argument interfaces
- Sub-interfaces: `SelectionSettingsModel`, `ToolbarSettingsModel`, `FieldSettingsModel`, `SourceDestinationModel`

---

### Quick Start Example

> **Installation:** Pin packages to a specific major version to reduce supply-chain risk.
> ```bash
> npm install @syncfusion/ej2-react-dropdowns@^33.x.x @syncfusion/ej2-base@^33.x.x
> ```

Basic ListBox with single selection:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns'; // ^33.x.x
import './App.css';

function App() {
  const data = [
    { text: 'JavaScript', id: '1' },
    { text: 'TypeScript', id: '2' },
    { text: 'React', id: '3' },
    { text: 'Vue', id: '4' },
    { text: 'Angular', id: '5' }
  ];

  const handleChange = (e) => {
    console.log('Selected:', e.value);
  };

  return (
    <ListBoxComponent 
      dataSource={data}
      fields={{ text: 'text', value: 'id' }}
      selectionSettings={{ mode: 'Single' }}
      change={handleChange}
    />
  );
}

export default App;
```

---

### Common Patterns

#### Multiple Selection
```tsx
<ListBoxComponent 
  dataSource={data}
  selectionSettings={{ mode: 'Multiple' }}
/>
```

#### Checkbox Selection
> **Requires injecting `CheckBoxSelection` service.**

```tsx
import { ListBoxComponent, SelectionSettingsModel, Inject, CheckBoxSelection } from '@syncfusion/ej2-react-dropdowns';

const selectionSettings: SelectionSettingsModel = { showCheckbox: true };

<ListBoxComponent dataSource={data} selectionSettings={selectionSettings}>
  <Inject services={[CheckBoxSelection]} />
</ListBoxComponent>
```

#### With Search/Filter
```tsx
<ListBoxComponent 
  dataSource={data}
  allowFiltering={true}
  filterBarPlaceholder="Search items"
/>
```

#### Custom Item Template
```tsx
const itemTemplate = (props) => {
  return (
    <div>
      <span className="icon">{props.icon}</span>
      <span>{props.text}</span>
    </div>
  );
}

<ListBoxComponent 
  dataSource={data}
  itemTemplate={itemTemplate}
/>
```

#### Grouping Items
```tsx
<ListBoxComponent 
  dataSource={groupedData}
  fields={{ text: 'text', groupBy: 'category' }}
/>
```

---

### Key Props & Configuration

| Prop | Purpose | Example |
|------|---------|---------|
| `dataSource` | Array of items to display | `[{ text: 'Item', id: '1' }]` |
| `fields` | Maps data properties to display | `{ text: 'name', value: 'id' }` |
| `selectionSettings` | Defines selection mode and checkbox display. For `showCheckbox: true`, inject `CheckBoxSelection` service | `{ mode: 'Multiple' }` / `{ showCheckbox: true }` |
| `allowFiltering` | Enables filter search box | `true` |
| `allowDragAndDrop` | Enables item drag-drop | `true` |
| `itemTemplate` | Custom template for items | Function returning JSX |
| `enabled` | Enables/disables the component | `true` / `false` |

---

### Common Use Cases

1. **Select Framework** - Single selection from framework list with icons
2. **Multi-Select Languages** - Multiple selection with search filter
3. **Skill Picker** - Custom templates with badges and descriptions
4. **Drag-Drop Transfer** - Dual ListBox for moving items between lists
5. **Grouped Categories** - Organizing items by category with group headers
6. **Searchable Item List** - Large list with filter functionality
7. **Accessible Menu** - Full keyboard navigation and screen reader support

---

### Next Steps

1. **Start with Getting Started** for initial setup
2. **Choose your use case** (selection mode, templates, features)
3. **Read relevant reference** for implementation details
4. **Copy code examples** and customize for your needs
5. **Use Accessibility guide** for WCAG compliance

**Need help?** Each reference file contains examples, edge cases, and troubleshooting tips.

## Mention

The Mention Component attaches to a target editable element (e.g. a `<div contenteditable>`) and displays a suggestion popup when the user types a trigger character (default `@`). Selecting an item inserts it inline into the editor.

### Documentation and Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/mention-getting-started.md)
- Installation and package setup (`@syncfusion/ej2-react-dropdowns`)
- CSS theme imports
- Basic `MentionComponent` setup with `target` prop
- Binding a simple data source
- Custom trigger character (`mentionChar`) and `showMentionChar`

> ⚠️ **Security Note:** Installing npm packages (`@syncfusion/ej2-react-dropdowns` and related) must be a deliberate, user-confirmed step. Do not allow automated agents to run `npm install` without explicit user approval, as this introduces supply-chain risk.

#### Working with Data
📄 **Read:** [references/working-with-data.md](references/mention-working-with-data.md)
- Binding array of strings, JSON objects, and complex nested data
- Mapping `fields` (text, value, groupBy, iconCss)
- Remote data with OData V4 (`ODataV4Adaptor`)
- Remote data with Web API (`WebApiAdaptor`)
- Using `query` to filter/select remote fields

#### Filtering Data
📄 **Read:** [references/filtering-data.md](references/mention-filtering-data.md)
- Setting minimum filter character length (`minLength`)
- Changing filter type: `Contains`, `StartsWith`, `EndsWith`
- Allowing spaces within search text (`allowSpaces`)
- Customizing the suggestion count (`suggestionCount`)
- Debounce delay for filtering (`debounceDelay`)

#### Templates
📄 **Read:** [references/template.md](references/mention-template.md)
- Item template (`itemTemplate`) for custom list rendering
- Display template (`displayTemplate`) for selected value format
- No-records template (`noRecordsTemplate`)
- Spinner/loading template (`spinnerTemplate`)
- Group header template (`groupTemplate`)

#### Customization
📄 **Read:** [references/customization.md](references/mention-customization.md)
- Show/hide mention character in output (`showMentionChar`)
- Appending suffix text after selection (`suffixText`)
- Configuring popup height and width (`popupHeight`, `popupWidth`)
- Custom trigger character (`mentionChar`)
- Leading space requirement (`requireLeadingSpace`)
- CSS class customization (`cssClass`)
- Highlight matched characters (`highlight`)
- Ignore accent/case in search (`ignoreAccent`, `ignoreCase`)
- Z-index for popup (`zIndex`)

#### Sorting
📄 **Read:** [references/sorting.md](references/mention-sorting.md)
- Sorting suggestion list: `Ascending`, `Descending`, `None`

#### Disabled Items
📄 **Read:** [references/disabled-items.md](references/mention-disabled-items.md)
- Disabling items via `fields.disabled`
- Dynamically disabling items with `disableItem()` method

#### Accessibility
📄 **Read:** [references/accessibility.md](references/mention-accessibility.md)
- WAI-ARIA attributes (`aria-selected`, `aria-activedescendent`, `aria-owns`)
- Keyboard navigation shortcuts
- WCAG 2.2 and Section 508 compliance
- RTL support (`enableRtl`)

#### Localization
📄 **Read:** [references/localization.md](references/mention-localization.md)
- Localizing the `noRecordsTemplate` text via `L10n`
- Setting `locale` property

#### API Reference
📄 **Read:** [references/api.md](references/mention-api.md)
- All properties, methods, and events
- `target`, `dataSource`, `fields`, `mentionChar`, `minLength`, `suggestionCount`
- Methods: `addItem`, `disableItem`, `getDataByValue`, `getItems`, `showPopup`, `hidePopup`, `search`, `destroy`
- Events: `select`, `change`, `filtering`, `beforeOpen`, `opened`, `closed`, `dataBound`, `actionBegin`, `actionComplete`, `actionFailure`

### Quick Start Example

```tsx
import { MentionComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

// CSS imports
// @import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
// @import "../node_modules/@syncfusion/ej2-react-dropdowns/styles/tailwind3.css";

function App() {
  const mentionTarget = '#commentBox';
  const users = [
    { Name: 'Selma Rose', EmailId: 'selma@example.com' },
    { Name: 'Robert', EmailId: 'robert@example.com' },
    { Name: 'William', EmailId: 'william@example.com' },
  ];
  const fields = { text: 'Name' };

  return (
    <div>
      <label>Comments</label>
      <div id="commentBox" placeholder="Type @ to mention a user"></div>
      <MentionComponent
        target={mentionTarget}
        dataSource={users}
        fields={fields}
      />
    </div>
  );
}

export default App;
```

### Common Patterns

#### Custom Trigger Character
Use `mentionChar` to trigger with `#` instead of `@`:
```tsx
<MentionComponent
  target="#editor"
  dataSource={tags}
  mentionChar="#"
  showMentionChar={true}
/>
```

#### Remote Data with Filtering (security-first)

```tsx
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';

// SECURITY: Do not call third-party endpoints from the browser. Use a server-side
// proxy that you control and that validates/sanitizes upstream responses.
const dataSource = new DataManager({
  url: 'https://your-trusted-proxy.example/api/mentions',
  adaptor: new ODataV4Adaptor(),
  crossDomain: true,
});
const query = new Query().from('Customers').select(['ContactName', 'CustomerID']).take(6);
const fields = { text: 'ContactName', value: 'CustomerID' };

<MentionComponent
  target="#editor"
  dataSource={dataSource}
  fields={fields}
  query={query}
  minLength={2}
  popupWidth="250px" />
```

#### Handling Selection Events
```tsx
import { SelectEventArgs } from '@syncfusion/ej2-react-dropdowns';

function onSelect(args: SelectEventArgs) {
  console.log('Selected item:', args.itemData);
  console.log('Selected text:', args.text);
}

<MentionComponent
  target="#editor"
  dataSource={users}
  fields={{ text: 'Name' }}
  select={onSelect}
/>
```

#### Popup Configuration
```tsx
<MentionComponent
  target="#editor"
  dataSource={data}
  fields={{ text: 'Name' }}
  popupHeight="200px"
  popupWidth="300px"
  suggestionCount={10}
  sortOrder="Ascending"
  suffixText="&nbsp;"
/>
```

### Key Props Summary

| Prop | Type | Default | Purpose |
|------|------|---------|---------|
| `target` | `string\|HTMLElement` | — | CSS selector or element for the editable area |
| `dataSource` | `array\|DataManager` | `[]` | Data for suggestions |
| `fields` | `FieldSettingsModel` | `{text:null,value:null}` | Maps data fields |
| `mentionChar` | `string` | `'@'` | Trigger character |
| `showMentionChar` | `boolean` | `false` | Prepend trigger char to inserted text |
| `minLength` | `number` | `0` | Min chars before search |
| `suggestionCount` | `number` | `25` | Max items in popup |
| `filterType` | `FilterType` | `'Contains'` | Filter match strategy |
| `allowSpaces` | `boolean` | `false` | Allow spaces in search |
| `sortOrder` | `SortOrder` | `'None'` | Sort direction |
| `popupHeight` | `string\|number` | `'300px'` | Popup height |
| `popupWidth` | `string\|number` | `'auto'` | Popup width |
| `suffixText` | `string` | `null` | Text appended after selection |
| `requireLeadingSpace` | `boolean` | `true` | Space required before trigger char |
| `highlight` | `boolean` | `false` | Highlight search characters |

## MultiSelect

A comprehensive skill for implementing the MultiSelect Dropdown component — enabling users to select multiple values from a list with support for filtering, grouping, templates, checkboxes, chips, virtual scrolling, and more.

### Component Overview

> **Installation:** Pin packages to a specific major version to reduce supply-chain risk.
> ```bash
> npm install @syncfusion/ej2-react-dropdowns@^33.x.x @syncfusion/ej2-base@^33.x.x @syncfusion/ej2-buttons@^33.x.x @syncfusion/ej2-inputs@^33.x.x
> ```

```tsx
import { MultiSelectComponent } from '@syncfusion/ej2-react-dropdowns'; // ^33.x.x
import '@syncfusion/ej2-react-dropdowns/styles/tailwind3.css';
// Also import base dependencies:
// @syncfusion/ej2-base/styles/tailwind3.css
// @syncfusion/ej2-buttons/styles/tailwind3.css
// @syncfusion/ej2-inputs/styles/tailwind3.css
```

**Package:** `@syncfusion/ej2-react-dropdowns`  
**Main component:** `MultiSelectComponent`  
**Checkbox module:** `CheckBoxSelection` (inject via `<Inject services={[CheckBoxSelection]} />`)  
**Virtual scroll module:** `VirtualScroll` (inject via `<Inject services={[VirtualScroll]} />`)

### Quick Start Example

```tsx
import { MultiSelectComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

export default function App() {
  const sportsData = ['Badminton', 'Basketball', 'Cricket', 'Football', 'Golf', 'Tennis'];

  return (
    <MultiSelectComponent
      id="multiselect"
      dataSource={sportsData}
      placeholder="Select sports"
    />
  );
}
```

With objects and field mapping:

```tsx
import { MultiSelectComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

export default function App() {
  const sportsData = [
    { id: 'game1', sports: 'Badminton' },
    { id: 'game2', sports: 'Football' },
    { id: 'game3', sports: 'Tennis' },
  ];
  const fields = { text: 'sports', value: 'id' };

  return (
    <MultiSelectComponent
      id="multiselect"
      dataSource={sportsData}
      fields={fields}
      placeholder="Select a game"
    />
  );
}
```

### Documentation and Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/multiselect-getting-started.md)
- Installation and package setup (Vite / CRA)
- CSS imports and theming
- Basic MultiSelect implementation (class & functional components)
- Binding a simple data source
- Popup height/width configuration

#### Data Binding
📄 **Read:** [references/data-binding.md](references/multiselect-data-binding.md)
- Array of strings vs array of objects
- Field mapping (`text`, `value`, `groupBy`, `iconCss`, `disabled`)
- Remote data via `DataManager` (OData, OData V4, Web API)
- JSON/JSONP formats
- Complex data binding gotchas

#### Grouping
📄 **Read:** [references/grouping.md](references/multiselect-grouping.md)
- Grouping items by category with `groupBy`
- Inline vs fixed group headers
- Group header templates
- Ordering and multi-level grouping

#### Filtering
📄 **Read:** [references/filtering.md](references/multiselect-filtering.md)
- Enabling `allowFiltering`
- Handling the `filtering` event
- Query API with `where()` conditions
- Filter types: startswith, contains, endswith
- Case sensitivity, multiple conditions, performance

#### Templates
📄 **Read:** [references/templates.md](references/multiselect-templates.md)
- Item templates for custom list item layouts
- Value/chip templates for selected display
- Group header templates
- Header, footer, no-records, and action-failure templates

#### Selection Modes and Features
📄 **Read:** [references/selection-and-features.md](references/multiselect-selection-and-features.md)
- Checkbox mode (inject `CheckBoxSelection`)
- Chip/tag display and the `tagging` event
- Custom values (`allowCustomValue`)
- Value binding (primitive and object types)
- Disabled items via `fields.disabled`
- Popup resizing (`allowResize`)
- Virtual scrolling for large datasets (inject `VirtualScroll`)

#### Accessibility, Styling, and Localization
📄 **Read:** [references/accessibility-styling-localization.md](references/multiselect-accessibility-styling-localization.md)
- WAI-ARIA attributes and keyboard shortcuts
- WCAG 2.2 / Section 508 / Screen reader support
- CSS customization (chips, wrapper, icon, delimiter)
- RTL support
- Localization with `L10n`

#### API Reference
📄 **Read:** [references/api.md](references/multiselect-api.md)
- Complete list of all properties with types, descriptions, and defaults
- All public methods with parameter details and return types
- All events with their argument types and trigger conditions

### Key Props Reference

| Prop | Type | When to Use |
|------|------|-------------|
| `dataSource` | `string[] \| object[] \| DataManager` | Always required — data to display |
| `fields` | `FieldSettingsModel` | When using object data; map `text`, `value`, `groupBy`, `disabled` |
| `mode` | `'Default' \| 'Box' \| 'CheckBox' \| 'Delimiter'` | Change selection display: chips (`Box`), checkboxes, or comma-delimited |
| `value` | `string[] \| number[] \| object[]` | Pre-select items on load |
| `allowFiltering` | `boolean` | Enable search-as-you-type filtering |
| `allowCustomValue` | `boolean` | Let users type values not in the list |
| `allowObjectBinding` | `boolean` | Return full objects as selected values instead of primitives |
| `enableVirtualization` | `boolean` | Use for 500+ items to improve performance |
| `allowResize` | `boolean` | Let users resize the popup |
| `popupHeight` | `string` | Limit popup list height (default: `300px`) |
| `popupWidth` | `string` | Set popup width (default: matches input) |
| `placeholder` | `string` | Input placeholder text |

### Common Use Cases

**Multi-tag input (chip display):**
→ Use `mode="Box"` (default). Each selection becomes a chip.

**Checkbox multi-selection:**
→ Use `mode="CheckBox"` and inject `CheckBoxSelection` module.

**Search/filter a long list:**
→ Set `allowFiltering={true}` and handle the `filtering` event for remote data.

**Pre-select values:**
→ Pass `value` prop as an array of value-field values: `value={['id1', 'id2']}`.

**Group by category:**
→ Add `groupBy` to the `fields` prop: `fields={{ text: 'name', value: 'id', groupBy: 'category' }}`.

**Large datasets (1000+ items):**
→ Set `enableVirtualization={true}` and inject `VirtualScroll` module.

**Disable specific options:**
→ Add a boolean `disabled` column to your data and map it: `fields={{ ..., disabled: 'isDisabled' }}`.

**Custom entry not in list:**
→ Set `allowCustomValue={true}`; handle `customValueSelection` event for custom actions.

### Decision Guide

```
User wants multiple selections?
  ├── Visual chips with filter → mode="Box" (default) + allowFiltering
  ├── Checkbox-style list      → mode="CheckBox" + Inject CheckBoxSelection
  └── Comma-separated display  → mode="Delimiter"

Data source type?
  ├── Simple strings/numbers   → Pass array directly to dataSource
  ├── Objects                  → Pass array + fields={{ text, value }}
  └── Remote API               → Use DataManager + allowFiltering + filtering event

List is very long?
  └── Yes (500+) → enableVirtualization={true} + Inject VirtualScroll

Need custom item layout?
  └── Use itemTemplate, valueTemplate, groupTemplate props

Need localization?
  └── Read references/accessibility-styling-localization.md
```

## MultiColumn ComboBox

The Syncfusion `MultiColumnComboBoxComponent` renders a combo box with a multi-column popup grid, enabling users to select from structured tabular data. It supports local and remote data, filtering, sorting, grouping, templates, virtualization, and full accessibility compliance.

**Package:** `@syncfusion/ej2-react-multicolumn-combobox`

### Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/multicolumn-combobox-getting-started.md)
- Installation and package setup
- CSS imports and theme configuration (Tailwind 3)
- Rendering the first `MultiColumnComboBoxComponent`
- Binding `dataSource`, `fields`, and `columns` with `ColumnDirective`
- Configuring `popupHeight` and `popupWidth`
- Minimal working example (functional and class components)

#### Columns
📄 **Read:** [references/columns.md](references/multicolumn-combobox-columns.md)
- Defining columns with `ColumnDirective` and `ColumnsDirective`
- `field`, `header`, `width` — core column properties
- `textAlign` for column text alignment
- `template` for cell-level custom rendering
- `displayAsCheckBox` for boolean columns
- `customAttributes` for column CSS customization
- `headerTemplate` for custom column headers
- `format` for data formatting

#### Data Binding
📄 **Read:** [references/data-binding.md](references/multicolumn-combobox-data-binding.md)
- Binding local object arrays via `dataSource`
- Remote data binding with `DataManager` and `WebApiAdaptor`
- Mapping `fields` (`text`, `value`, `groupBy`)
- Using `query` property for filtered/limited data sets
- OData, OData V4, Web API adaptor patterns

#### Filtering
📄 **Read:** [references/filtering.md](references/multicolumn-combobox-filtering.md)
- Enabling/disabling filtering with `allowFiltering`
- Changing filter mode with `filterType` (`StartsWith`, `EndsWith`, `Contains`)
- `filtering` event for custom filter logic
- Disabling filtering for read-only scenarios

#### Sorting
📄 **Read:** [references/sorting.md](references/multicolumn-combobox-sorting.md)
- Enabling sorting with `allowSorting`
- Setting initial sort order with `sortOrder` (`None`, `Ascending`, `Descending`)
- Sorting multiple columns with `sortType` (`OneColumn`, `MultipleColumns`)
- Clicking column headers to toggle sort direction

#### Grouping
📄 **Read:** [references/grouping.md](references/multicolumn-combobox-grouping.md)
- Grouping data with `fields.groupBy`
- Fixed group headers in popup
- Using `groupTemplate` to customize group headers

#### Templates
📄 **Read:** [references/templates.md](references/multicolumn-combobox-templates.md)
- `itemTemplate` for customizing each row
- `headerTemplate` (on `ColumnDirective`) for custom column headers
- `groupTemplate` for group header customization
- `footerTemplate` for popup footer content
- `noRecordsTemplate` for empty state display
- `actionFailureTemplate` for remote fetch error state

#### Items and Configuration
📄 **Read:** [references/items.md](references/multicolumn-combobox-items.md)
- Setting initial selection with `text`, `value`, `index`
- `placeholder` and `floatLabelType` for input label behavior
- `showClearButton` to allow clearing selection
- `disabled` and `readonly` states
- `width`, `popupWidth`, `popupHeight` for sizing
- `cssClass` for custom styling
- `htmlAttributes` for additional HTML attributes
- `gridSettings` for grid lines, row height, and alternate rows
- `query` for data constraints
- `addItems` method, `focusIn`, `focusOut`, `showPopup`, `hidePopup`

#### Virtualization
📄 **Read:** [references/virtualization.md](references/multicolumn-combobox-virtualization.md)
- Enabling `enableVirtualization` for large datasets
- Virtual scrolling with local and remote data
- Combining with `gridSettings.rowHeight`

#### Events
📄 **Read:** [references/events.md](references/multicolumn-combobox-events.md)
- `change` — fired when value changes or item is selected
- `select` — fired on item selection
- `open` / `close` — popup open/close lifecycle
- `filtering` — fired on character input for custom filtering
- `actionBegin` / `actionComplete` / `actionFailure` — data fetch lifecycle

#### API Reference
📄 **Read:** [references/api.md](references/multicolumn-combobox-api.md)
- Complete list of all properties with types and defaults
- All events with their argument types
- All methods: `addItems`, `focusIn`, `focusOut`, `getDataByValue`, `getItems`, `showPopup`, `hidePopup`
- `ColumnModel` properties
- `GridSettingsModel` properties
- `FieldSettingsModel` properties

#### Accessibility
📄 **Read:** [references/accessibility.md](references/multicolumn-combobox-accessibility.md)
- WCAG 2.2 and Section 508 compliance
- WAI-ARIA attributes (`role`, `aria-expanded`, `aria-selected`, etc.)
- Keyboard navigation shortcuts
- RTL support with `enableRtl`
- Screen reader support

#### Localization
📄 **Read:** [references/localization.md](references/multicolumn-combobox-localization.md)
- Localizing `noRecordsTemplate` text using `L10n`
- Setting `locale` property for culture-specific rendering
- Loading translation objects

### Quick Start

```tsx
import { MultiColumnComboBoxComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-multicolumn-combobox';
import * as React from 'react';
import './App.css';

// CSS in App.css:
// @import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
// @import "../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css";
// @import "../node_modules/@syncfusion/ej2-grids/styles/tailwind3.css";
// @import "../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css";
// @import "../node_modules/@syncfusion/ej2-react-multicolumn-combobox/styles/tailwind3.css";

function App() {
  const empData = [
    { EmpID: 1001, Name: 'Andrew Fuller', Designation: 'Team Lead', Country: 'England' },
    { EmpID: 1002, Name: 'Robert', Designation: 'Developer', Country: 'USA' },
    { EmpID: 1003, Name: 'Michael', Designation: 'HR', Country: 'Russia' },
  ];
  const fields = { text: 'Name', value: 'EmpID' };

  return (
    <MultiColumnComboBoxComponent
      id="multicolumn"
      dataSource={empData}
      fields={fields}
      placeholder="Select an employee"
    >
      <ColumnsDirective>
        <ColumnDirective field='EmpID' header='Employee ID' width={120} />
        <ColumnDirective field='Name' header='Name' width={120} />
        <ColumnDirective field='Designation' header='Designation' width={120} />
        <ColumnDirective field='Country' header='Country' width={100} />
      </ColumnsDirective>
    </MultiColumnComboBoxComponent>
  );
}
export default App;
```

### Common Patterns

#### Pre-select an item by text
```tsx
<MultiColumnComboBoxComponent dataSource={empData} fields={fields} text="Michael">
  {/* columns */}
</MultiColumnComboBoxComponent>
```

#### Enable filtering with Contains mode
```tsx
<MultiColumnComboBoxComponent
  dataSource={empData}
  fields={fields}
  allowFiltering={true}
  filterType="Contains"
>
  {/* columns */}
</MultiColumnComboBoxComponent>
```

#### Enable sorting (descending) with multi-column support
```tsx
import { SortOrder } from '@syncfusion/ej2-react-multicolumn-combobox';

<MultiColumnComboBoxComponent
  dataSource={empData}
  fields={fields}
  allowSorting={true}
  sortOrder={SortOrder.Descending}
  sortType="MultipleColumns"
>
  {/* columns */}
</MultiColumnComboBoxComponent>
```

#### Handle value change event
```tsx
<MultiColumnComboBoxComponent
  dataSource={empData}
  fields={fields}
  change={(args) => console.log('Selected:', args.value)}
>
  {/* columns */}
</MultiColumnComboBoxComponent>
```
