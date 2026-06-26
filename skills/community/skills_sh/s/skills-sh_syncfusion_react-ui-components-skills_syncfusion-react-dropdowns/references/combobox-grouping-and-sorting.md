# Grouping & Sorting

## Table of Contents
- [Grouping Overview](#grouping-overview)
- [Basic Grouping](#basic-grouping)
- [Sorting Options](#sorting-options)
- [Combined Grouping & Sorting](#combined-grouping--sorting)
- [Custom Group Headers](#custom-group-headers)

---

## Grouping Overview

Grouping organizes list items into logical categories with section headers. This improves usability for large datasets by grouping related items together.

**When to use:**
- Department/category organization (e.g., Engineering, Sales, HR)
- Geographic grouping (e.g., USA, Europe, Asia)
- Type-based grouping (e.g., Fruits, Vegetables)
- Status-based grouping (e.g., Active, Inactive)

---

## Basic Grouping

### Enable Grouping with `groupBy` Field

```tsx
import { ComboBoxComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const employeeData = [
    { id: 'emp1', name: 'Alice Johnson', department: 'Engineering' },
    { id: 'emp2', name: 'Bob Smith', department: 'Sales' },
    { id: 'emp3', name: 'Carol Davis', department: 'Engineering' },
    { id: 'emp4', name: 'David Lee', department: 'Sales' },
    { id: 'emp5', name: 'Eve Wilson', department: 'HR' }
  ];

  const fields = {
    text: 'name',
    value: 'id',
    groupBy: 'department'    // ← Group by this field
  };

  return (
    <ComboBoxComponent 
      id="emp-combo"
      dataSource={employeeData}
      fields={fields}
      placeholder="Select an employee"
    />
  );
}
```

**Result:**
```
Engineering
  - Alice Johnson
  - Carol Davis
Sales
  - Bob Smith
  - David Lee
HR
  - Eve Wilson
```

### Grouping with Simple Data

For simple arrays, create objects with groupBy field:

```tsx
const fruitData = [
  { name: 'Apple', category: 'Red Fruits' },
  { name: 'Cherry', category: 'Red Fruits' },
  { name: 'Banana', category: 'Yellow Fruits' },
  { name: 'Mango', category: 'Yellow Fruits' }
];

const fields = {
  text: 'name',
  value: 'name',
  groupBy: 'category'
};

<ComboBoxComponent 
  dataSource={fruitData}
  fields={fields}
/>
```

---

## Sorting Options

### Sort Data

Control item order in dropdown using `sortOrder`:

```tsx
<ComboBoxComponent 
  id="combo"
  dataSource={items}
  sortOrder="Ascending"     // "Ascending" or "Descending"
  placeholder="Sorted A-Z"
/>
```

**Available options:**
- `"Ascending"` - A to Z, 0 to 9 (default alphabetical)
- `"Descending"` - Z to A, 9 to 0

### Example with Sorting

```tsx
const sportsList = ['Volleyball', 'Tennis', 'Badminton', 'Cricket'];

<ComboBoxComponent 
  id="sports-combo"
  dataSource={sportsList}
  sortOrder="Ascending"     // Shows: Badminton, Cricket, Tennis, Volleyball
  placeholder="Select a sport"
/>
```

---

## Combined Grouping & Sorting

### Grouped AND Sorted Data

```tsx
const productData = [
  { id: 'prod1', name: 'Laptop', category: 'Electronics', price: 1200 },
  { id: 'prod2', name: 'Mouse', category: 'Electronics', price: 25 },
  { id: 'prod3', name: 'Apple', category: 'Fruits', price: 5 },
  { id: 'prod4', name: 'Banana', category: 'Fruits', price: 3 },
  { id: 'prod5', name: 'Carrot', category: 'Vegetables', price: 2 }
];

const fields = {
  text: 'name',
  value: 'id',
  groupBy: 'category'
};

<ComboBoxComponent 
  id="products-combo"
  dataSource={productData}
  fields={fields}
  sortOrder="Ascending"    // Items within groups sorted A-Z
  placeholder="Select a product"
/>
```

**Result:**
```
Electronics
  - Laptop
  - Mouse
Fruits
  - Apple
  - Banana
Vegetables
  - Carrot
```

### Sort Groups by Name

The groups appear in the order they first appear in data. To sort group headers:

```tsx
// Manually organize data with groups in desired order
const sortedByGroup = [
  // Electronics group first
  { name: 'Laptop', category: 'Electronics' },
  { name: 'Mouse', category: 'Electronics' },
  // Fruits group second
  { name: 'Apple', category: 'Fruits' },
  { name: 'Banana', category: 'Fruits' },
  // Vegetables group last
  { name: 'Carrot', category: 'Vegetables' }
];
```

---

## Custom Group Headers

### Style Group Headers

Use CSS to customize group header appearance:

```css
/* In your CSS file */
.e-list-group-item {
  background-color: #f0f0f0;
  font-weight: bold;
  padding: 10px;
  border-top: 2px solid #ddd;
}

.e-list-group-item::before {
  content: '📁 ';  /* Add icon before group name */
}
```

### Custom Group Template

Create advanced group headers with icons or counts:

```tsx
const groupTemplate = (props) => {
  // Count items in this group
  const groupItems = productData.filter(
    item => item.category === props.category
  );
  
  return (
    <div className="group-header">
      <strong>{props.category}</strong>
      <span className="item-count">({groupItems.length})</span>
    </div>
  );
};

<ComboBoxComponent 
  dataSource={productData}
  fields={{ text: 'name', value: 'id', groupBy: 'category' }}
  groupTemplate={groupTemplate}
/>
```

**CSS:**
```css
.group-header {
  display: flex;
  justify-content: space-between;
  padding: 8px 12px;
  background-color: #e8f4f8;
  font-weight: 600;
}

.item-count {
  color: #666;
  font-size: 0.9em;
}
```

---

## Common Patterns

### Pattern 1: Group by Status

```tsx
const taskData = [
  { id: 1, title: 'Design UI', status: 'Completed' },
  { id: 2, title: 'Fix bugs', status: 'In Progress' },
  { id: 3, title: 'Write tests', status: 'Completed' },
  { id: 4, title: 'Deploy', status: 'Pending' },
  { id: 5, title: 'Review code', status: 'In Progress' }
];

const fields = {
  text: 'title',
  value: 'id',
  groupBy: 'status'
};

// Order groups logically: In Progress → Pending → Completed
const orderedData = taskData.sort((a, b) => {
  const order = { 'In Progress': 0, 'Pending': 1, 'Completed': 2 };
  return order[a.status] - order[b.status];
});

<ComboBoxComponent 
  dataSource={orderedData}
  fields={fields}
  placeholder="Select a task"
/>
```

### Pattern 2: Hierarchical Grouping (2-Level)

ComboBox supports one level of grouping. For multi-level grouping, use `itemTemplate`:

```tsx
const itemTemplate = (props) => {
  const { category, subcategory, name } = props;
  return (
    <div className={`item item-${category}`}>
      {subcategory && <div className="subcategory">{subcategory}</div>}
      <div className="item-name">{name}</div>
    </div>
  );
};

<ComboBoxComponent 
  dataSource={hierarchicalData}
  itemTemplate={itemTemplate}
/>
```

### Pattern 3: Sorted Groups with Count

```tsx
const getGroupCount = (group) => {
  return productData.filter(p => p.category === group).length;
};

const sortedWithCounts = productData
  .sort((a, b) => a.name.localeCompare(b.name))  // Sort items
  .sort((a, b) => {
    // Then sort by group
    const order = ['Electronics', 'Fruits', 'Vegetables'];
    return order.indexOf(a.category) - order.indexOf(b.category);
  });

<ComboBoxComponent 
  dataSource={sortedWithCounts}
  fields={{ text: 'name', value: 'id', groupBy: 'category' }}
/>
```

---

## Grouping & Sorting Checklist

- [ ] `groupBy` field specified in fields object
- [ ] Data contains the groupBy field for all items
- [ ] Groups display in expected order
- [ ] Sorting applied (ascending/descending)
- [ ] Group headers are visible and styled appropriately
- [ ] No empty groups (check data for null/undefined in groupBy field)
- [ ] Performance acceptable with grouped data

---

## Next Steps

- **Show more info per item?** → Check [templates-and-customization.md](templates-and-customization.md)
- **Large grouped datasets?** → See [advanced-features.md](advanced-features.md)
- **Styling groups?** → Explore [styling-and-theming.md](styling-and-theming.md)
- **Filtering grouped items?** → Read [filtering-and-search.md](filtering-and-search.md)
