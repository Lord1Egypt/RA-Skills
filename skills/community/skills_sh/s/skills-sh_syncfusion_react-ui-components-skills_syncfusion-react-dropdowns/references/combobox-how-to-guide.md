# How-To Guide: Common ComboBox Scenarios

## Table of Contents
- [Autofill While Typing](#autofill-while-typing)
- [Cascading ComboBoxes](#cascading-comboboxes)
- [Display Icons in Items](#display-icons-in-items)

---

## Autofill While Typing

### Overview

The autofill feature automatically completes your input by matching typed characters against available options. As you type, the ComboBox suggests the first matching item. Perfect for quickly selecting from known values.

**When to use:**
- User knows approximate values but wants fast selection
- Reducing typing effort (e.g., "F" auto-fills to "Football")
- Guided data entry

### Basic Autofill

```tsx
import { ComboBoxComponent } from '@syncfusion/ej2-react-dropdowns';

export default class App extends React.Component<{}, {}> {
  private sportsData: string[] = ['Badminton', 'Cricket', 'Football', 'Golf', 'Tennis'];

  public render() {
    return (
      <ComboBoxComponent 
        id="sports-combo"
        dataSource={this.sportsData}
        autofill={true}              // ← Enable autofill
        placeholder="Type 'F' to auto-fill"
      />
    );
  }
}
```

**User Interaction:**
1. User types "Fo"
2. Combo auto-completes to "Football"
3. User can press Enter to accept or continue typing
4. If no match, autofill does nothing

### Autofill with Objects

```tsx
const employeeData = [
  { id: 1, name: 'Alice Johnson' },
  { id: 2, name: 'Bob Smith' },
  { id: 3, name: 'Carol Davis' }
];

const fields = { text: 'name', value: 'id' };

export default function App() {
  return (
    <ComboBoxComponent 
      dataSource={employeeData}
      fields={fields}
      autofill={true}
      placeholder="Type 'Al' to find Alice"
    />
  );
}
```

### Combining Autofill with Filtering

```tsx
<ComboBoxComponent 
  dataSource={items}
  autofill={true}           // Auto-completes typed text
  allowFiltering={true}     // Shows filtered results
  placeholder="Search and auto-fill"
/>
```

**Behavior:**
- Autofill suggests first matching item
- Filtering shows all matching items
- User can select from suggestions or type custom value

---

## Cascading ComboBoxes

### Overview

Cascading ComboBoxes create dependent dropdowns where selecting a value in one ComboBox filters options in another. Common use case: Country → State → City selection.

**When to use:**
- Hierarchical data (Country/State/City)
- Parent-child relationships
- Conditional selections
- Progressive refinement

### Basic Cascading Pattern

```tsx
import { Query } from '@syncfusion/ej2-data';
import { ComboBoxComponent } from '@syncfusion/ej2-react-dropdowns';

export default class App extends React.Component<{}, {}> {
  private countryObj: ComboBoxComponent;
  private stateObj: ComboBoxComponent;

  // Country data
  private countryData = [
    { CountryName: 'United States', CountryId: '1' },
    { CountryName: 'Australia', CountryId: '2' }
  ];

  // State data with CountryId reference
  private stateData = [
    { StateName: 'New York', CountryId: '1', StateId: '101' },
    { StateName: 'Virginia', CountryId: '1', StateId: '102' },
    { StateName: 'Tasmania', CountryId: '2', StateId: '105' }
  ];

  private countryField = { value: 'CountryId', text: 'CountryName' };
  private stateField = { value: 'StateId', text: 'StateName' };

  constructor(props) {
    super(props);
    this.onCountryChange = this.onCountryChange.bind(this);
  }

  // When country changes, filter states
  public onCountryChange() {
    // Query states by selected country
    this.stateObj.query = new Query().where('CountryId', 'equal', this.countryObj.value);
    
    // Enable state dropdown
    this.stateObj.enabled = true;
    
    // Clear previous selection
    this.stateObj.value = null;
    this.stateObj.text = null;
  }

  public render() {
    return (
      <div>
        {/* Country ComboBox */}
        <ComboBoxComponent 
          id="country"
          ref={(scope) => { this.countryObj = scope; }}
          fields={this.countryField}
          dataSource={this.countryData}
          placeholder="Select Country"
          change={this.onCountryChange}
        />

        <br /><br />

        {/* State ComboBox - Initially disabled */}
        <ComboBoxComponent 
          id="state"
          ref={(scope) => { this.stateObj = scope; }}
          enabled={false}           // Disabled until country selected
          fields={this.stateField}
          dataSource={this.stateData}
          placeholder="Select State"
        />
      </div>
    );
  }
}
```

### Three-Level Cascading (Country → State → City)

```tsx
export default class App extends React.Component<{}, {}> {
  private countryObj: ComboBoxComponent;
  private stateObj: ComboBoxComponent;
  private cityObj: ComboBoxComponent;

  // Data with hierarchical relationships
  private countryData = [
    { CountryName: 'United States', CountryId: '1' },
    { CountryName: 'Australia', CountryId: '2' }
  ];

  private stateData = [
    { StateName: 'New York', CountryId: '1', StateId: '101' },
    { StateName: 'Virginia', CountryId: '1', StateId: '102' },
    { StateName: 'Tasmania', CountryId: '2', StateId: '105' }
  ];

  private cityData = [
    { CityName: 'Albany', StateId: '101', CityId: 201 },
    { CityName: 'Beacon', StateId: '101', CityId: 202 },
    { CityName: 'Hobart', StateId: '105', CityId: 213 }
  ];

  private countryField = { value: 'CountryId', text: 'CountryName' };
  private stateField = { value: 'StateId', text: 'StateName' };
  private cityField = { value: 'CityId', text: 'CityName' };

  constructor(props) {
    super(props);
    this.onCountryChange = this.onCountryChange.bind(this);
    this.onStateChange = this.onStateChange.bind(this);
  }

  public onCountryChange() {
    // Filter states by country
    this.stateObj.query = new Query().where('CountryId', 'equal', this.countryObj.value);
    this.stateObj.enabled = true;
    this.stateObj.value = null;
    this.stateObj.text = null;

    // Clear city selection
    this.cityObj.value = null;
    this.cityObj.text = null;
    this.cityObj.enabled = false;
  }

  public onStateChange() {
    // Filter cities by state
    this.cityObj.query = new Query().where('StateId', 'equal', this.stateObj.value);
    this.cityObj.enabled = true;
    this.cityObj.value = null;
    this.cityObj.text = null;
  }

  public render() {
    return (
      <div>
        <ComboBoxComponent 
          id="country"
          ref={(scope) => { this.countryObj = scope; }}
          fields={this.countryField}
          dataSource={this.countryData}
          placeholder="Select Country"
          change={this.onCountryChange}
        />

        <ComboBoxComponent 
          id="state"
          ref={(scope) => { this.stateObj = scope; }}
          enabled={false}
          fields={this.stateField}
          dataSource={this.stateData}
          placeholder="Select State"
          change={this.onStateChange}
        />

        <ComboBoxComponent 
          id="city"
          ref={(scope) => { this.cityObj = scope; }}
          enabled={false}
          fields={this.cityField}
          dataSource={this.cityData}
          placeholder="Select City"
        />
      </div>
    );
  }
}
```

### Functional Component with Hooks

```tsx
import { useState } from 'react';
import { Query } from '@syncfusion/ej2-data';

export default function App() {
  const [countryValue, setCountryValue] = useState('');
  const [stateValue, setStateValue] = useState('');
  const [filteredStates, setFilteredStates] = useState([]);
  const [stateEnabled, setStateEnabled] = useState(false);

  const countryData = [
    { id: '1', name: 'USA' },
    { id: '2', name: 'Australia' }
  ];

  const stateData = [
    { id: '101', name: 'New York', countryId: '1' },
    { id: '102', name: 'Virginia', countryId: '1' },
    { id: '105', name: 'Tasmania', countryId: '2' }
  ];

  const handleCountryChange = (e) => {
    setCountryValue(e.value);
    // Filter states by selected country
    const filtered = stateData.filter(s => s.countryId === e.value);
    setFilteredStates(filtered);
    setStateEnabled(true);
    setStateValue('');  // Clear state selection
  };

  return (
    <div>
      <ComboBoxComponent 
        dataSource={countryData}
        fields={{ text: 'name', value: 'id' }}
        change={handleCountryChange}
        placeholder="Select Country"
      />
      
      <ComboBoxComponent 
        dataSource={filteredStates}
        fields={{ text: 'name', value: 'id' }}
        value={stateValue}
        enabled={stateEnabled}
        placeholder="Select State"
      />
    </div>
  );
}
```

---

## Display Icons in Items

### Overview

Show icons or images alongside text in ComboBox items using the `iconCss` field. Perfect for visual indicators, status symbols, or category icons.

**When to use:**
- Status indicators (Open, Closed, Pending)
- Category icons (Document, Folder, Image)
- Action indicators (Edit, Delete, Archive)

### Basic Icon Display

```tsx
import { ComboBoxComponent } from '@syncfusion/ej2-react-dropdowns';

export default class App extends React.Component<{}, {}> {
  private sortData = [
    { Class: 'asc-sort', Type: 'Sort A to Z', Id: '1' },
    { Class: 'dsc-sort', Type: 'Sort Z to A', Id: '2' },
    { Class: 'filter', Type: 'Filter', Id: '3' },
    { Class: 'clear', Type: 'Clear', Id: '4' }
  ];

  private fields = { 
    text: 'Type',
    value: 'Id',
    iconCss: 'Class'        // ← Map icon CSS class
  };

  public render() {
    return (
      <ComboBoxComponent 
        id="sort-combo"
        dataSource={this.sortData}
        fields={this.fields}
        placeholder="Select an action"
      />
    );
  }
}
```

**CSS for Icons:**
```css
.asc-sort::before {
  content: '⬆ ';
  color: #0066cc;
}

.dsc-sort::before {
  content: '⬇ ';
  color: #0066cc;
}

.filter::before {
  content: '🔍 ';
}

.clear::before {
  content: '🗑️ ';
}
```

### Status Icons with Colors

```tsx
const statusData = [
  { status: 'Open', iconCss: 'status-open', id: 1 },
  { status: 'In Progress', iconCss: 'status-progress', id: 2 },
  { status: 'Closed', iconCss: 'status-closed', id: 3 }
];

const fields = { text: 'status', value: 'id', iconCss: 'iconCss' };
```

**CSS:**
```css
.status-open {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: #4caf50;
  display: inline-block;
  margin-right: 8px;
}

.status-progress {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: #ff9800;
  display: inline-block;
  margin-right: 8px;
}

.status-closed {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: #f44336;
  display: inline-block;
  margin-right: 8px;
}
```

### Font Awesome Icons

```tsx
const data = [
  { name: 'Document', iconCss: 'fa fa-file', id: 1 },
  { name: 'Folder', iconCss: 'fa fa-folder', id: 2 },
  { name: 'Image', iconCss: 'fa fa-image', id: 3 },
  { name: 'Settings', iconCss: 'fa fa-cog', id: 4 }
];

// Include Font Awesome in HTML:
// <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">

<ComboBoxComponent 
  dataSource={data}
  fields={{ text: 'name', value: 'id', iconCss: 'iconCss' }}
/>
```

### Combined with Templates

```tsx
const productData = [
  { name: 'Product A', icon: 'fa fa-star', rating: 5, id: 1 },
  { name: 'Product B', icon: 'fa fa-heart', rating: 4, id: 2 }
];

const itemTemplate = (props) => {
  return (
    <div className="item-with-icon">
      <i className={props.icon}></i>
      <span>{props.name}</span>
      <small>⭐ {props.rating}</small>
    </div>
  );
};

<ComboBoxComponent 
  dataSource={productData}
  fields={{ text: 'name', value: 'id', iconCss: 'icon' }}
  itemTemplate={itemTemplate}
/>
```

---

## Common Patterns Summary

| Scenario | Reference | Solution |
|----------|-----------|----------|
| Auto-complete typing | Autofill | Enable `autofill={true}` |
| Dependent selections | Cascading | Use `change` event + `Query` to filter |
| Visual indicators | Icons | Map `iconCss` field in fields object |
| Combine features | Multiple | Can use autofill + filtering, cascading + icons, etc. |

---

## Next Steps

- **Need more template control?** → See [templates-and-customization.md](templates-and-customization.md)
- **Performance with large data?** → Check [advanced-features.md](advanced-features.md)
- **Styling icons/cascades?** → Read [styling-and-theming.md](styling-and-theming.md)
