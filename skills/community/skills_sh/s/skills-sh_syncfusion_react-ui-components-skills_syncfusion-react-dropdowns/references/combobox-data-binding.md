# Data Binding in ComboBox

## Table of Contents
- [Overview](#overview)
- [Local Data Binding](#local-data-binding)
- [Remote Data Binding](#remote-data-binding)
- [Field Mapping](#field-mapping)
- [DataManager Configuration](#datamanager-configuration)
- [Common Patterns](#common-patterns)

---

## Overview

The ComboBox `dataSource` property accepts multiple data types:

| Data Type | When to Use | Example |
|-----------|------------|---------|
| **Array of strings** | Simple lists, no metadata | `['Red', 'Green', 'Blue']` |
| **Array of objects** | Complex data, multiple fields | `[{id: 1, name: 'Apple', color: 'red'}]` |
| **DataManager** | Remote APIs (OData, Web API) | Connect to backend services |
| **URL** | Direct API endpoint | `'/api/items'` |

---

## Local Data Binding

### Array of Strings (Simplest)

Use when you have a simple list of values where text and value are the same.

```tsx
import { ComboBoxComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const colorsList = ['Red', 'Green', 'Blue', 'Yellow', 'Orange'];

  return (
    <ComboBoxComponent 
      id="color-combo"
      dataSource={colorsList}
      placeholder="Select a color"
    />
  );
}
```

**When value is selected:**
```tsx
change={(e) => {
  console.log('Selected:', e.value);  // Output: "Red"
}}
```

---

### Array of Objects (Recommended for Apps)

Use when items have multiple fields (ID, name, description, etc.).

#### Single Key-Value Mapping

```tsx
const gamesData = [
  { GameId: 'game1', GameName: 'Chess' },
  { GameId: 'game2', GameName: 'Carrom' },
  { GameId: 'game3', GameName: 'Badminton' }
];

const fields = {
  text: 'GameName',    // Display this field
  value: 'GameId'      // Use this as value
};

<ComboBoxComponent 
  id="games-combo"
  dataSource={gamesData}
  fields={fields}
  placeholder="Select a game"
  change={(e) => {
    console.log('Selected ID:', e.value);     // "game1"
    console.log('Selected Item:', e.itemData);  // { GameId: 'game1', GameName: 'Chess' }
  }}
/>
```

#### Multiple Field Mapping

```tsx
const employeeData = [
  { 
    empId: 'EMP001', 
    empName: 'Alice Johnson', 
    department: 'Engineering',
    iconCss: 'icon-engineer'
  },
  { 
    empId: 'EMP002', 
    empName: 'Bob Smith', 
    department: 'Sales',
    iconCss: 'icon-sales'
  }
];

const fields = {
  text: 'empName',           // Display name
  value: 'empId',            // Hidden value
  groupBy: 'department',     // Group by department (see grouping doc)
  iconCss: 'iconCss'         // Icon for each item
};

<ComboBoxComponent 
  id="emp-combo"
  dataSource={employeeData}
  fields={fields}
  placeholder="Select employee"
/>
```

---

## Remote Data Binding

### Using DataManager with Web API

For data from backend APIs, use Syncfusion's DataManager:

```tsx
import { ComboBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { DataManager, WebApiAdaptor } from '@syncfusion/ej2-data';

export default function App() {
  const dataManager = new DataManager({
    url: 'url',
    adaptor: new WebApiAdaptor()
  });

  const fields = {
    text: 'name',
    value: 'id'
  };

  return (
    <ComboBoxComponent 
      id="sports-combo"
      dataSource={dataManager}
      fields={fields}
      placeholder="Loading sports..."
      allowFiltering={true}
    />
  );
}
```

**Response Expected:**
```json
[
  { "id": 1, "name": "Cricket" },
  { "id": 2, "name": "Football" },
  { "id": 3, "name": "Tennis" }
]
```

---

### OData Service (Legacy APIs)

For OData v3/v4 endpoints:

```tsx
import { DataManager, ODataAdaptor } from '@syncfusion/ej2-data';

const dataManager = new DataManager({
  url: 'url',
  adaptor: new ODataAdaptor()
});

<ComboBoxComponent 
  id="products-combo"
  dataSource={dataManager}
  fields={{ text: 'ProductName', value: 'ProductID' }}
  placeholder="Select a product"
/>
```

---

## Field Mapping

### All Available Fields

```tsx
const fields = {
  // Display field (shown in input and list)
  text: 'displayName',
  
  // Hidden value (used in forms and callbacks)
  value: 'id',
  
  // Group items by this field (creates section headers)
  groupBy: 'category',
  
  // CSS class for each item (for icons, styling)
  iconCss: 'cssClassName',
  
  // Nested object access using dot notation
  text: 'employee.name',
  value: 'employee.id'
};

<ComboBoxComponent 
  dataSource={complexData}
  fields={fields}
/>
```

### Nested Object Access

If your data has nested properties:

```tsx
const userData = [
  {
    id: 1,
    profile: {
      name: 'Alice',
      company: 'TechCorp'
    }
  },
  {
    id: 2,
    profile: {
      name: 'Bob',
      company: 'DevInc'
    }
  }
];

const fields = {
  text: 'profile.name',      // Access nested field
  value: 'id'
};

<ComboBoxComponent 
  dataSource={userData}
  fields={fields}
/>
```

---

## DataManager Configuration

### Configure Request Parameters

```tsx
import { Query } from '@syncfusion/ej2-data';

const dataManager = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor()
});

<ComboBoxComponent 
  id="items-combo"
  dataSource={dataManager}
  query={new Query().select(['id', 'name']).take(10)}  // Select specific fields, limit to 10
  placeholder="Select an item"
/>
```

### With Headers/Authentication

```tsx
const dataManager = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor(),
  headers: [
    { 'Authorization': 'Bearer YOUR_TOKEN' },
    { 'X-Custom-Header': 'value' }
  ]
});
```

### With Query Parameters

```tsx
import { Query } from '@syncfusion/ej2-data';

const query = new Query()
  .select(['id', 'name', 'category'])
  .where('status', 'equal', 'active')
  .sortBy('name')
  .take(50);

<ComboBoxComponent 
  dataSource={dataManager}
  query={query}
/>
```

---

## Common Patterns

### Pattern 1: Dynamic Data Source Update

Change data based on user selection in another component:

```tsx
export default function App() {
  const [selectedDept, setSelectedDept] = useState('');
  const [employees, setEmployees] = useState([]);

  const departments = ['Engineering', 'Sales', 'HR'];

  const handleDeptChange = (e) => {
    setSelectedDept(e.value);
    // Fetch employees for selected department
    fetchEmployees(e.value).then(setEmployees);
  };

  return (
    <div>
      <ComboBoxComponent 
        dataSource={departments}
        change={handleDeptChange}
        placeholder="Select department"
      />
      <ComboBoxComponent 
        dataSource={employees}
        fields={{ text: 'name', value: 'id' }}
        placeholder="Select employee"
        enabled={!!selectedDept}
      />
    </div>
  );
}
```

### Pattern 2: Transform Data Before Display

Map raw API data to display-friendly format:

```tsx
const rawData = [
  { user_id: 1, user_name: 'Alice', dept_id: 'D001' },
  { user_id: 2, user_name: 'Bob', dept_id: 'D002' }
];

const transformedData = rawData.map(item => ({
  value: item.user_id,
  text: `${item.user_name} (Dept: ${item.dept_id})`,
  originalData: item
}));

<ComboBoxComponent 
  dataSource={transformedData}
  fields={{ text: 'text', value: 'value' }}
/>
```

### Pattern 3: Static + Dynamic Data

Combine static defaults with dynamically loaded data:

```tsx
export default function App() {
  const [dataSource, setDataSource] = useState(['Select an option', 'Loading...']);

  useEffect(() => {
    // Load data from API
    fetch('/api/items')
      .then(res => res.json())
      .then(data => setDataSource(data.map(item => item.name)));
  }, []);

  return (
    <ComboBoxComponent 
      dataSource={dataSource}
      placeholder="Select an item"
    />
  );
}
```

---

## Data Binding Checklist

- [ ] Data source set with `dataSource` prop
- [ ] Fields mapped correctly (text, value match your data structure)
- [ ] For objects, fields object includes `text` and `value`
- [ ] For nested data, using dot notation (e.g., `'user.name'`)
- [ ] Remote data uses appropriate DataManager adaptor
- [ ] API endpoint returns correct data format
- [ ] `change` handler captures selected value correctly
- [ ] No console errors about undefined fields

---

## Next Steps

- **Need to filter this data?** → See [filtering-and-search.md](filtering-and-search.md)
- **Want to organize data?** → Check [grouping-and-sorting.md](grouping-and-sorting.md)
- **Show more info per item?** → Explore [templates-and-customization.md](templates-and-customization.md)
- **Large dataset performance?** → Read [advanced-features.md](advanced-features.md)
