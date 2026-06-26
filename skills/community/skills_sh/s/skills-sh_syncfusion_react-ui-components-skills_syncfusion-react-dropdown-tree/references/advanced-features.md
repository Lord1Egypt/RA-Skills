# Advanced Features & API Reference

## Table of Contents

- [All Component Properties](#all-component-properties)
- [Property Examples](#property-examples)
- [Methods & Public APIs](#methods--public-apis)
- [Events & Event Arguments](#events--event-arguments)
- [Performance Optimization](#performance-optimization)
- [CSS Customization](#css-customization)

## All Component Properties

### Essential Properties

| Property | Type | Default | Description | Example |
|----------|------|---------|-------------|---------|
| `id` | string | - | Unique component identifier | `id="dropdowntree"` |
| `placeholder` | string | "" | Input placeholder text | `placeholder="Select item"` |
| `enabled` | boolean | true | Enable/disable component | `enabled={true}` |
| `width` | string \| number | "100%" | Component width | `width="300px"` |

### Selection Properties

| Property | Type | Default | Description | Example |
|----------|------|---------|-------------|---------|
| `showCheckBox` | boolean | false | Show checkboxes for multi-select | `showCheckBox={true}` |
| `showSelectAll` | boolean | false | Show Select All checkbox | `showSelectAll={true}` |
| `selectAllText` | string | "Select All" | Select All label | `selectAllText="Check All"` |
| `unSelectAllText` | string | "Unselect All" | Unselect All label | `unSelectAllText="Uncheck All"` |
| `allowMultiSelection` | boolean | false | Enable Ctrl/Shift multi-select | `allowMultiSelection={true}` |

### Template Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `itemTemplate` | string \| Function \| JSX | null | Custom item rendering |
| `valueTemplate` | string \| Function \| JSX | null | Custom selected value display |
| `headerTemplate` | string \| Function \| JSX | null | Custom header |
| `footerTemplate` | string \| Function \| JSX | null | Custom footer |
| `noRecordsTemplate` | string \| Function \| JSX | null | Empty state template |
| `actionFailureTemplate` | string \| Function \| JSX | null | Error state template |

### Filtering Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `allowFiltering` | boolean | false | Enable search/filter bar |
| `filterType` | "StartsWith" \| "EndsWith" \| "Contains" | "StartsWith" | Filter matching type |
| `filterBarPlaceholder` | string | "" | Filter bar placeholder |
| `ignoreCase` | boolean | true | Case-insensitive filtering |
| `ignoreAccent` | boolean | false | Ignore diacritics |

### Display Mode Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `mode` | "Default" \| "Delimiter" \| "Custom" | "Default" | Display mode for selections |
| `delimiterChar` | string | ", " | Delimiter for selected items |
| `customTemplate` | string | "${value.length} item(s) selected" | Custom template for selections |

### Localization & RTL Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `locale` | string | "en" | Culture/locale code |
| `enableRtl` | boolean | false | Enable right-to-left layout |
| `enablePersistence` | boolean | false | Persist state in localStorage |

### Data Binding Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `fields` | FieldsModel | - | Data source and field mapping |
| `sortOrder` | "Ascending" \| "Descending" \| "None" | "None" | Item sorting order |

### Popup & Animation Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `popupHeight` | string \| number | "300px" | Dropdown popup height |
| `popupWidth` | string \| number | "100%" | Dropdown popup width |
| `destroyPopupOnHide` | boolean | true | Destroy popup on close |

### Styling Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `cssClass` | string | "" | Custom CSS classes |
| `htmlAttributes` | object | {} | HTML attributes |

### Advanced Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `changeOnBlur` | boolean | true | Fire change event on blur |
| `enableHtmlSanitizer` | boolean | true | Sanitize HTML in templates |
| `floatLabelType` | "Never" \| "Always" \| "Auto" | "Never" | Floating label behavior |

---

## Property Examples

### Essential Properties Examples

**Basic Component Setup**
```tsx
<DropDownTreeComponent
  id="myDropdownTree"
  placeholder="Select an item"
  enabled={true}
  width="300px"
  fields={fields}
/>
```

### Selection Properties Examples

**Checkboxes with Select All**
```tsx
<DropDownTreeComponent
  id="dropdowntree"
  showCheckBox={true}
  showSelectAll={true}
  selectAllText="Select All Items"
  unSelectAllText="Unselect All"
  fields={fields}
/>
```

**Multi-Selection with Ctrl/Shift**
```tsx
<DropDownTreeComponent
  id="dropdowntree"
  allowMultiSelection={true}
  fields={fields}
/>
```

### Template Properties Examples

**Custom Item Template**
```tsx
const itemTemplate = (props) => {
  return (
    <div style={{ padding: '5px' }}>
      <span style={{ marginRight: '10px' }}>🎯</span>
      {props.text}
    </div>
  );
};

<DropDownTreeComponent
  id="dropdowntree"
  itemTemplate={itemTemplate}
  fields={fields}
/>
```

**Custom Value Template**
```tsx
const valueTemplate = (props) => {
  const values = props.value || [];
  return (
    <div style={{ color: '#007bff' }}>
      Selected: {values.length} item(s)
    </div>
  );
};

<DropDownTreeComponent
  id="dropdowntree"
  valueTemplate={valueTemplate}
  fields={fields}
/>
```

**Custom Header Template**
```tsx
const headerTemplate = () => (
  <div style={{
    padding: '10px',
    backgroundColor: '#f0f0f0',
    borderBottom: '1px solid #ddd'
  }}>
    <strong>Available Options</strong>
  </div>
);

<DropDownTreeComponent
  id="dropdowntree"
  headerTemplate={headerTemplate}
  fields={fields}
/>
```

**Custom Footer Template**
```tsx
const footerTemplate = () => (
  <div style={{
    padding: '10px',
    backgroundColor: '#f0f0f0',
    borderTop: '1px solid #ddd',
    textAlign: 'center'
  }}>
    <small>Total items: {data.length}</small>
  </div>
);

<DropDownTreeComponent
  id="dropdowntree"
  footerTemplate={footerTemplate}
  fields={fields}
/>
```

**No Records Template**
```tsx
const noRecordsTemplate = () => (
  <div style={{ padding: '20px', textAlign: 'center', color: '#999' }}>
    <p>No matching items found</p>
  </div>
);

<DropDownTreeComponent
  id="dropdowntree"
  noRecordsTemplate={noRecordsTemplate}
  fields={fields}
/>
```

**Action Failure Template (Error State)**
```tsx
const actionFailureTemplate = () => (
  <div style={{
    padding: '20px',
    textAlign: 'center',
    color: '#d32f2f',
    backgroundColor: '#ffebee'
  }}>
    <div style={{ fontSize: '14px', fontWeight: 'bold' }}>⚠️ Failed to load items</div>
    <div style={{ fontSize: '12px', marginTop: '8px' }}>
      Connection error. Please try again later.
    </div>
  </div>
);

<DropDownTreeComponent
  id="dropdowntree"
  actionFailureTemplate={actionFailureTemplate}
  fields={fields}
/>
```

**Action Failure Template with Retry Button**
```tsx
const [isRetrying, setIsRetrying] = React.useState(false);

const actionFailureTemplate = () => (
  <div style={{
    padding: '16px',
    textAlign: 'center',
    backgroundColor: '#fff3cd',
    borderLeft: '4px solid #ffc107'
  }}>
    <div style={{ fontSize: '13px', fontWeight: '600', color: '#856404' }}>
      Unable to load data
    </div>
    <div style={{ fontSize: '12px', color: '#856404', marginTop: '4px' }}>
      {isRetrying ? 'Retrying...' : 'Server connection failed'}
    </div>
    <button
      onClick={() => {
        setIsRetrying(true);
        // Trigger data refresh after 2 seconds
        setTimeout(() => {
          treeRef.current?.refresh();
          setIsRetrying(false);
        }, 2000);
      }}
      style={{
        marginTop: '10px',
        padding: '6px 12px',
        backgroundColor: '#ffc107',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        fontSize: '12px',
        fontWeight: '600'
      }}
      disabled={isRetrying}
    >
      {isRetrying ? 'Retrying...' : 'Retry'}
    </button>
  </div>
);

<DropDownTreeComponent
  ref={treeRef}
  id="dropdowntree"
  actionFailureTemplate={actionFailureTemplate}
  fields={{
    dataSource: new DataManager({
      url: 'url',
      adaptor: new ODataV4Adaptor()
    }),
    value: 'id',
    text: 'name'
  }}
/>
```

### Filtering Properties Examples

**Basic Filtering**
```tsx
<DropDownTreeComponent
  id="dropdowntree"
  allowFiltering={true}
  filterType="Contains"
  filterBarPlaceholder="Type to search..."
  fields={fields}
/>
```

**Case-Insensitive Filtering**
```tsx
<DropDownTreeComponent
  id="dropdowntree"
  allowFiltering={true}
  filterType="StartsWith"
  ignoreCase={true}
  fields={fields}
/>
```

**Ignore Accent Filtering**
```tsx
<DropDownTreeComponent
  id="dropdowntree"
  allowFiltering={true}
  filterType="Contains"
  ignoreAccent={true}
  ignoreCase={true}
  fields={fields}
/>
```

### Display Mode Properties Examples

**Default Display Mode**
```tsx
<DropDownTreeComponent
  id="dropdowntree"
  mode="Default"
  showCheckBox={true}
  fields={fields}
/>
```

**Delimiter Display Mode**
```tsx
<DropDownTreeComponent
  id="dropdowntree"
  mode="Delimiter"
  delimiterChar=" | "
  showCheckBox={true}
  fields={fields}
/>
```

**Custom Display Mode**
```tsx
<DropDownTreeComponent
  id="dropdowntree"
  mode="Custom"
  customTemplate="${value.length} items selected out of 50"
  showCheckBox={true}
  fields={fields}
/>
```

### Localization & RTL Properties Examples

**Enable RTL (Right-to-Left)**
```tsx
<DropDownTreeComponent
  id="dropdowntree"
  enableRtl={true}
  locale="ar"
  fields={fields}
/>
```

**Localization with Culture - German**
```tsx
<DropDownTreeComponent
  id="dropdowntree"
  locale="de"  // German
  fields={fields}
/>
```

**Multi-Language Localization Setup**
```tsx
import { DropDownTreeComponent } from '@syncfusion/ej2-react-dropdowns';
import { L10n } from '@syncfusion/ej2-base';
import React, { useState } from 'react';

// Define localization for multiple languages
L10n.load({
  'es': {
    'dropdowntree': {
      'noRecordsTemplate': 'No se encontraron registros',
      'actionFailureTemplate': 'Error al cargar datos',
      'overflowCountTemplate': 'y ${count} más',
      'totalCountTemplate': '${count} elementos seleccionados'
    }
  },
  'fr': {
    'dropdowntree': {
      'noRecordsTemplate': 'Aucun enregistrement trouvé',
      'actionFailureTemplate': 'Erreur de chargement des données',
      'overflowCountTemplate': 'et ${count} plus',
      'totalCountTemplate': '${count} éléments sélectionnés'
    }
  },
  'de': {
    'dropdowntree': {
      'noRecordsTemplate': 'Keine Datensätze gefunden',
      'actionFailureTemplate': 'Fehler beim Laden von Daten',
      'overflowCountTemplate': 'und ${count} weitere',
      'totalCountTemplate': '${count} Elemente ausgewählt'
    }
  }
});

function MultiLanguageDropdownTree() {
  const [locale, setLocale] = useState('en');

  return (
    <div style={{ padding: '20px' }}>
      <div style={{ marginBottom: '20px' }}>
        <label>Select Language: </label>
        <select 
          value={locale} 
          onChange={(e) => setLocale(e.target.value)}
          style={{ padding: '6px' }}
        >
          <option value="en">English</option>
          <option value="es">Español (Spanish)</option>
          <option value="fr">Français (French)</option>
          <option value="de">Deutsch (German)</option>
        </select>
      </div>

      <DropDownTreeComponent
        id="dropdowntree"
        locale={locale}
        showCheckBox={true}
        showSelectAll={true}
        allowFiltering={true}
        fields={fields}
        placeholder={locale === 'en' ? 'Select item' : 'Seleccionar'}
      />
    </div>
  );
}

export default MultiLanguageDropdownTree;
```

**Custom Localization Text**
```tsx
<DropDownTreeComponent
  id="dropdowntree"
  locale="custom"
  noRecordsTemplate="Nenhum resultado encontrado (Portuguese)"
  actionFailureTemplate="Falha ao carregar dados"
  selectAllText="Selecionar Tudo"
  unSelectAllText="Desselecionar Tudo"
  fields={fields}
/>
```

**Locale with RTL Support (Arabic)**
```tsx
import { enableRtl, L10n } from '@syncfusion/ej2-base';

// Enable RTL globally
enableRtl(true);

// Add Arabic localization
L10n.load({
  'ar': {
    'dropdowntree': {
      'noRecordsTemplate': 'لم يتم العثور على سجلات',
      'actionFailureTemplate': 'خطأ في تحميل البيانات',
      'overflowCountTemplate': 'و ${count} أكثر',
      'totalCountTemplate': '${count} عناصر محددة'
    }
  }
});

<div dir="rtl" lang="ar">
  <DropDownTreeComponent
    id="dropdowntree"
    locale="ar"
    enableRtl={true}
    placeholder="اختر عنصراً"
    fields={arabicData}
  />
</div>
```

**Language Switcher Component**
```tsx
import { DropDownTreeComponent } from '@syncfusion/ej2-react-dropdowns';
import { L10n } from '@syncfusion/ej2-base';
import React, { useState } from 'react';

// Pre-load multiple locales
L10n.load({
  'it': {
    'dropdowntree': {
      'noRecordsTemplate': 'Nessun record trovato',
      'actionFailureTemplate': 'Errore nel caricamento dei dati'
    }
  },
  'pt': {
    'dropdowntree': {
      'noRecordsTemplate': 'Nenhum registro encontrado',
      'actionFailureTemplate': 'Erro ao carregar dados'
    }
  },
  'ja': {
    'dropdowntree': {
      'noRecordsTemplate': 'レコードが見つかりません',
      'actionFailureTemplate': 'データの読み込みに失敗しました'
    }
  }
});

const LANGUAGE_LABELS = {
  'en': { name: 'English', flag: '🇺🇸' },
  'es': { name: 'Español', flag: '🇪🇸' },
  'fr': { name: 'Français', flag: '🇫🇷' },
  'de': { name: 'Deutsch', flag: '🇩🇪' },
  'it': { name: 'Italiano', flag: '🇮🇹' },
  'pt': { name: 'Português', flag: '🇵🇹' },
  'ja': { name: '日本語', flag: '🇯🇵' }
};

function LanguageSwitcher() {
  const [currentLocale, setCurrentLocale] = useState('en');

  return (
    <div style={{ padding: '20px' }}>
      <div style={{
        display: 'flex',
        gap: '10px',
        marginBottom: '20px',
        flexWrap: 'wrap'
      }}>
        {Object.entries(LANGUAGE_LABELS).map(([code, { name, flag }]) => (
          <button
            key={code}
            onClick={() => setCurrentLocale(code)}
            style={{
              padding: '8px 16px',
              backgroundColor: currentLocale === code ? '#007bff' : '#f0f0f0',
              color: currentLocale === code ? 'white' : 'black',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontWeight: currentLocale === code ? 'bold' : 'normal'
            }}
          >
            {flag} {name}
          </button>
        ))}
      </div>

      <DropDownTreeComponent
        id="dropdowntree"
        locale={currentLocale}
        showCheckBox={true}
        allowFiltering={true}
        fields={fields}
      />
    </div>
  );
}

export default LanguageSwitcher;
```

**Persist Selection State**
```tsx
<DropDownTreeComponent
  id="dropdowntree"
  enablePersistence={true}
  fields={fields}
/>
```

### Data Binding & Sorting Examples

**With Sorting**
```tsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  sortOrder="Ascending"
/>
```

### Popup & Animation Properties Examples

**Custom Popup Dimensions**
```tsx
<DropDownTreeComponent
  id="dropdowntree"
  popupHeight="500px"
  popupWidth="400px"
  fields={fields}
/>
```

**Destroy Popup on Hide**
```tsx
<DropDownTreeComponent
  id="dropdowntree"
  destroyPopupOnHide={true}
  fields={fields}
/>
```

### Styling Properties Examples

**Custom CSS Classes**
```tsx
<DropDownTreeComponent
  id="dropdowntree"
  cssClass="premium-theme dark-mode"
  fields={fields}
/>

<style>
  {`
    .premium-theme {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .dark-mode .e-ddtree {
      background-color: #2d2d2d;
      color: #fff;
    }
  `}
</style>
```

**HTML Attributes**
```tsx
<DropDownTreeComponent
  id="dropdowntree"
  htmlAttributes={{
    'data-test-id': 'dropdown-tree-1',
    'aria-label': 'Select items from tree',
    'title': 'Click to expand options'
  }}
  fields={fields}
/>
```

### Advanced Properties Examples

**Change on Blur**
```tsx
<DropDownTreeComponent
  id="dropdowntree"
  changeOnBlur={true}
  fields={fields}
/>
```

**Enable HTML Sanitizer**
```tsx
<DropDownTreeComponent
  id="dropdowntree"
  enableHtmlSanitizer={true}
  itemTemplate={(props) => (
    <div dangerouslySetInnerHTML={{__html: props.text}} />
  )}
  fields={fields}
/>
```

**Floating Label Behavior**
```tsx
// Never show floating label
<DropDownTreeComponent
  id="dropdowntree"
  floatLabelType="Never"
  placeholder="Select item"
  fields={fields}
/>

// Always show floating label
<DropDownTreeComponent
  id="dropdowntree"
  floatLabelType="Always"
  placeholder="Item Selection"
  fields={fields}
/>

// Auto - show floating label only when selected
<DropDownTreeComponent
  id="dropdowntree"
  floatLabelType="Auto"
  placeholder="Choose from list"
  fields={fields}
/>
```

---

## Methods & Public APIs

### Getting Selected Values

#### getValue()

Returns array of currently selected values.

```tsx
const treeRef = React.useRef(null);

const handleGetValue = () => {
  const selectedValues = treeRef.current.getValue();
  console.log('Selected values:', selectedValues); // string[]
};
```

#### getSelectedNodes()

Returns array of selected item objects with all properties.

```tsx
const handleGetSelectedNodes = () => {
  const selectedNodes = treeRef.current.getSelectedNodes();
  selectedNodes.forEach(node => {
    console.log('Node:', node.id, node.name);
  });
};
```

#### getCheckedNodes()

Returns array of checked items (when checkboxes enabled).

```tsx
const handleGetCheckedNodes = () => {
  const checkedNodes = treeRef.current.getCheckedNodes();
  checkedNodes.forEach(node => {
    console.log('Checked:', node.name);
  });
};
```

### Setting Selections

#### setValue(value)

Set selected values programmatically.

```tsx
treeRef.current.setValue(['id1', 'id3', 'id5']);
```

#### setCheckedNodes(nodes)

Set checked nodes programmatically (with checkboxes).

```tsx
treeRef.current.setCheckedNodes(['id2', 'id4']);
```

### Clearing Selections

#### clearSelection()

Clear all selected items.

```tsx
treeRef.current.clearSelection();
```

### Text & Display

#### getText()

Get display text of selected items.

```tsx
const text = treeRef.current.getText();
console.log('Selected text:', text);
```

### Tree Expansion

#### expandAll()

Expand all collapsible nodes.

```tsx
treeRef.current.expandAll();
```

#### collapseAll()

Collapse all expanded nodes.

```tsx
treeRef.current.collapseAll();
```

#### expandNode(nodeId)

Expand specific node by value.

```tsx
treeRef.current.expandNode('parent_id');
```

#### collapseNode(nodeId)

Collapse specific node by value.

```tsx
treeRef.current.collapseNode('parent_id');
```

### Enable/Disable

#### disable()

Disable the component.

```tsx
treeRef.current.disable();
```

#### enable()

Enable the component.

```tsx
treeRef.current.enable();
```

### Data Refresh

#### refresh()

Refresh the component and reload data.

```tsx
treeRef.current.refresh();
```

## Events & Event Arguments

### change Event

Fires when selected value changes. Provides old and new values.

```tsx
const handleChange = (args) => {
  console.log('Old values:', args.oldValue);  // string[]
  console.log('New values:', args.value);     // string[]
  console.log('Is user interaction:', args.isInteracted); // boolean
  console.log('Root element:', args.element);  // HTMLElement
};

<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  onChange={handleChange}
/>
```

**ChangeEventArgs Properties:**
- `e` (MouseEvent | KeyboardEvent) - Original event
- `element` (HTMLElement) - Root component element
- `isInteracted` (boolean) - User-triggered vs programmatic
- `oldValue` (string[]) - Previous selected values
- `value` (string[]) - Current selected values

### select Event

Fires when an item is selected or deselected.

```tsx
const handleSelect = (args) => {
  console.log('Action:', args.action);        // 'select' or 'unselect'
  console.log('Is user interaction:', args.isInteracted);
  console.log('Item element:', args.item);    // HTMLLIElement
  console.log('Item data:', args.itemData);   // { [key: string]: Object }
};

<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  onSelect={handleSelect}
/>
```

**SelectEventArgs Properties:**
- `action` (string) - 'select' or 'unselect'
- `isInteracted` (boolean) - User vs programmatic
- `item` (HTMLLIElement) - Selected DOM element
- `itemData` ({[key: string]: Object}) - Item data object

### dataBound Event

Fires after data binding is complete.

```tsx
const handleDataBound = (args) => {
  console.log('Data loaded:', args.data);  // { [key: string]: Object }[]
};

<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  onDataBound={handleDataBound}
/>
```

**DataBoundEventArgs Properties:**
- `data` ({[key: string]: Object}[]) - Bound data array

### filtering Event

Fires during filter/search operation. Allows custom filtering logic.

```tsx
const handleFiltering = (args) => {
  console.log('Filter text:', args.text);
  console.log('Can prevent default:', args.preventDefaultAction);
  
  // Custom filtering logic
  if (args.text.length < 2) {
    args.preventDefaultAction = true;
  }
};

<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  allowFiltering={true}
  onFiltering={handleFiltering}
/>
```

**FilteringEventArgs Properties:**
- `cancel` (boolean) - Cancel filtering
- `event` (Event) - Input event object
- `fields` (FieldsModel) - Current field config
- `preventDefaultAction` (boolean) - Override default filtering
- `text` (string) - Filter text input

### beforeOpen Event

Fires before popup opens.

```tsx
const handleBeforeOpen = (args) => {
  console.log('Popup about to open');
  // args.cancel = true; // Prevent opening
};

<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  onBeforeOpen={handleBeforeOpen}
/>
```

### popup Event

Fires when popup visibility changes.

```tsx
const handlePopup = (args) => {
  console.log('Popup action:', args.action); // 'open' or 'close'
};

<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  onPopup={handlePopup}
/>
```

### focus Event

Fires when component receives focus.

```tsx
const handleFocus = (args) => {
  console.log('Component focused');
};

<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  onFocus={handleFocus}
/>
```

### keyPress Event

Fires when user presses a key.

```tsx
const handleKeyPress = (args) => {
  console.log('Key pressed:', args.key);
};

<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  onKeyPress={handleKeyPress}
/>
```

## Performance Optimization

### Lazy Loading Strategy

```tsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={remoteFields}
  treeSettings={{ 
    loadOnDemand: true  // Load only parent level initially
  }}
  placeholder="Loads children on demand"
/>
```

**Benefits:**
- Initial load time reduced by 50-80%
- Lower bandwidth consumption
- Better for 1000+ items
- Caching of expanded nodes

### Virtual Scrolling

Enable high-performance rendering for large lists:

```tsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  popupHeight="400px"  // Fixed height for scrolling
  allowFiltering={true}  // Help users narrow down items
/>
```

### Data Filtering Client-Side

Implement custom filtering for pre-loaded data:

```tsx
const handleFiltering = (args) => {
  if (args.text.length >= 2) {
    args.preventDefaultAction = false;
  }
};
```

### Remote Data Optimization

```tsx
const query = new Query()
  .from('Employees')
  .select('EmployeeID,FirstName')  // Only needed fields
  .take(50);  // Limit records

const fields = {
  dataSource: new DataManager({
    url: 'url',
    adaptor: new ODataV4Adaptor,
    pageSize: 50
  }),
  query: query,
  value: 'EmployeeID',
  text: 'FirstName'
};
```

## CSS Customization

### Custom CSS Classes

```tsx
<DropDownTreeComponent
  id="dropdowntree"
  fields={fields}
  cssClass="my-custom-tree"
/>
```

### CSS Selectors for Styling

```css
/* Root element */
.e-ddtree {
  width: 300px;
}

/* Input field */
.e-ddtree .e-input-filter {
  border-radius: 4px;
}

/* Popup list */
.e-ddtree .e-tree-popup {
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

/* Tree items */
.e-ddtree .e-list-item {
  padding: 10px;
}

/* Selected item */
.e-ddtree .e-list-item.e-active {
  background-color: #007bff;
  color: white;
}

/* Custom class */
.my-custom-tree .e-list-item {
  min-height: 40px;
  border-bottom: 1px solid #f0f0f0;
}
```

### Complete Styling Example

```tsx
<div style={{
  padding: '20px',
  borderRadius: '8px',
  boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
}}>
  <DropDownTreeComponent
    id="dropdowntree"
    fields={fields}
    cssClass="styled-tree"
    popupHeight="350px"
    width="100%"
    placeholder="Select from list"
  />
</div>

<style>
  {`
    .styled-tree {
      border-radius: 4px;
      border: 2px solid #007bff;
    }
    
    .styled-tree .e-list-item {
      padding: 12px;
      transition: all 0.2s;
    }
    
    .styled-tree .e-list-item:hover {
      background-color: #f0f8ff;
    }
    
    .styled-tree .e-list-item.e-active {
      background-color: #007bff;
      color: white;
      border-radius: 4px;
    }
  `}
</style>
```

## Best Practices

1. **Use refs for method calls**: Prefer refs over direct DOM manipulation
2. **Handle events for UI updates**: Use event handlers for data changes
3. **Implement error boundaries**: Wrap component for error handling
4. **Lazy load large datasets**: Always use `loadOnDemand` for 1000+ items
5. **Memoize expensive functions**: Use `useCallback` for event handlers
6. **Test keyboard navigation**: Ensure accessibility with keyboard
7. **Monitor performance**: Use React DevTools profiler on large lists

## Complete Example with All Features

```tsx
import { DropDownTreeComponent } from '@syncfusion/ej2-react-dropdowns';
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';
import * as React from 'react';

function AdvancedDropdownTree() {
  const treeRef = React.useRef(null);
  const [selectedValues, setSelectedValues] = React.useState([]);

  const remoteData = new DataManager({
    url: 'url',
    adaptor: new ODataV4Adaptor,
    crossDomain: true,
  });

  const query = new Query().from('Employees').select('EmployeeID,FirstName').take(10);
  const query1 = new Query().from('Orders').select('OrderID,EmployeeID,ShipName').take(5);

  const fields = {
    dataSource: remoteData,
    query: query,
    value: 'EmployeeID',
    text: 'FirstName',
    hasChildren: 'EmployeeID',
    child: {
      dataSource: remoteData,
      query: query1,
      value: 'OrderID',
      parentValue: 'EmployeeID',
      text: 'ShipName'
    }
  };

  const handleChange = (args) => {
    setSelectedValues(args.value);
  };

  const handleGetValues = () => {
    const values = treeRef.current.getValue();
    console.log('Current values:', values);
  };

  return (
    <div style={{ padding: '20px' }}>
      <DropDownTreeComponent
        ref={treeRef}
        id="dropdowntree"
        fields={fields}
        showCheckBox={true}
        treeSettings={{ loadOnDemand: true, autoCheck: true }}
        allowFiltering={true}
        filterType="Contains"
        mode="Custom"
        customTemplate="${value.length} item(s) selected"
        onChange={handleChange}
        placeholder="Select employees"
      />
      <button onClick={handleGetValues} style={{ marginTop: '10px' }}>
        Get Selected Values
      </button>
      <p>Selected: {selectedValues.join(', ')}</p>
    </div>
  );
}

export default AdvancedDropdownTree;
```
