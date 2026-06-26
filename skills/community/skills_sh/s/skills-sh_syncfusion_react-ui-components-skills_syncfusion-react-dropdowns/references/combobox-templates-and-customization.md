# Templates & Customization

## Table of Contents
- [Overview](#overview)
- [Item Templates](#item-templates)
- [Header & Footer Templates](#header--footer-templates)
- [No Records Template](#no-records-template)
- [CSS Customization](#css-customization)
- [Advanced Examples](#advanced-examples)

---

## Overview

Templates allow you to customize the visual presentation of ComboBox items and container. Instead of plain text, you can display:

- Icons, images, and rich content
- Multi-line information with descriptions
- Styled badges, pills, or custom layouts
- Dynamic content based on data properties

---

## Item Templates

### Basic Item Template

Display each item with custom HTML:

```tsx
import { ComboBoxComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const employeeData = [
    { id: 1, name: 'Alice Johnson', avatar: '👩‍💼', dept: 'Engineering' },
    { id: 2, name: 'Bob Smith', avatar: '👨‍💼', dept: 'Sales' },
    { id: 3, name: 'Carol Davis', avatar: '👩‍💼', dept: 'HR' }
  ];

  const itemTemplate = (props) => {
    return (
      <div className="item-wrapper">
        <span className="avatar">{props.avatar}</span>
        <div>
          <div className="name">{props.name}</div>
          <small className="dept">{props.dept}</small>
        </div>
      </div>
    );
  };

  return (
    <ComboBoxComponent 
      id="emp-combo"
      dataSource={employeeData}
      fields={{ text: 'name', value: 'id' }}
      itemTemplate={itemTemplate}
      placeholder="Select an employee"
    />
  );
}
```

**CSS:**
```css
.item-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px;
}

.avatar {
  font-size: 24px;
}

.name {
  font-weight: 500;
}

.dept {
  color: #999;
  display: block;
  font-size: 12px;
}
```

### Template with Conditional Styling

```tsx
const statusTemplate = (props) => {
  const statusColor = {
    'Active': 'green',
    'Inactive': 'gray',
    'Pending': 'orange'
  };

  return (
    <div className="status-item">
      <span>{props.name}</span>
      <span 
        className="status-badge"
        style={{ backgroundColor: statusColor[props.status] }}
      >
        {props.status}
      </span>
    </div>
  );
};

<ComboBoxComponent 
  dataSource={userData}
  itemTemplate={statusTemplate}
/>
```

---

## Header & Footer Templates

### Header Template (Top of Dropdown)

Add information or actions at the top of dropdown:

```tsx
const headerTemplate = () => {
  return (
    <div className="dropdown-header">
      <h4>Select an Option</h4>
      <small>Showing available items</small>
    </div>
  );
};

<ComboBoxComponent 
  dataSource={items}
  headerTemplate={headerTemplate}
  placeholder="Choose..."
/>
```

**Use cases:**
- Instructions ("Type to filter")
- Count ("10 items available")
- Clear button or quick actions

### Footer Template (Bottom of Dropdown)

Add actions or information at bottom:

```tsx
const footerTemplate = () => {
  return (
    <div className="dropdown-footer">
      <button onClick={() => console.log('Create new')}>
        + Create New Item
      </button>
    </div>
  );
};

<ComboBoxComponent 
  dataSource={items}
  footerTemplate={footerTemplate}
/>
```

**Use cases:**
- "Add new" button for creating items
- Summary ("Selected 3 of 10")
- Help link or documentation

---

## No Records Template

### Custom "No Results" Message

Display when filtering returns no items:

```tsx
const noRecordsTemplate = () => {
  return (
    <div className="no-records">
      <div className="icon">🔍</div>
      <p>No items found</p>
      <small>Try a different search term</small>
    </div>
  );
};

<ComboBoxComponent 
  dataSource={items}
  allowFiltering={true}
  noRecordsTemplate={noRecordsTemplate}
/>
```

**CSS:**
```css
.no-records {
  text-align: center;
  padding: 20px;
  color: #999;
}

.no-records .icon {
  font-size: 32px;
  margin-bottom: 10px;
}

.no-records p {
  margin: 5px 0;
  font-weight: 500;
}
```

---

## CSS Customization

### Override Component Styles

Customize appearance using CSS selectors:

```css
/* Input field */
.e-combobox .e-input {
  border: 2px solid #ddd;
  border-radius: 6px;
  padding: 10px;
  font-size: 16px;
}

.e-combobox .e-input:focus {
  border-color: #0066cc;
  box-shadow: 0 0 5px rgba(0, 102, 204, 0.3);
}

/* Dropdown list container */
.e-combobox .e-dropdown-popup {
  border: 1px solid #ddd;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* List items */
.e-combobox .e-list-item {
  padding: 12px;
  border-bottom: 1px solid #f0f0f0;
}

.e-combobox .e-list-item:hover {
  background-color: #f5f5f5;
}

.e-combobox .e-list-item.e-active {
  background-color: #e3f2fd;
  color: #0066cc;
}

/* Group headers */
.e-combobox .e-list-group-item {
  background-color: #f9f9f9;
  font-weight: 600;
  padding: 8px 12px;
  border-top: 1px solid #e0e0e0;
}
```

### CSS Variables for Theming

Use CSS custom properties for easy theme switching:

```css
:root {
  --combo-primary-color: #0066cc;
  --combo-border-color: #ddd;
  --combo-hover-bg: #f5f5f5;
  --combo-active-bg: #e3f2fd;
  --combo-border-radius: 6px;
}

.e-combobox .e-input {
  border: 2px solid var(--combo-border-color);
  border-radius: var(--combo-border-radius);
}

.e-combobox .e-input:focus {
  border-color: var(--combo-primary-color);
}

.e-combobox .e-list-item:hover {
  background-color: var(--combo-hover-bg);
}

/* Switch themes */
body.dark-mode {
  --combo-primary-color: #4da6ff;
  --combo-border-color: #444;
  --combo-hover-bg: #333;
  --combo-active-bg: #1a3a52;
}
```

---

## Advanced Examples

### Example 1: Product Selection with Price

```tsx
const productData = [
  { id: 1, name: 'Laptop', price: '$1,200', category: 'Electronics' },
  { id: 2, name: 'Mouse', price: '$25', category: 'Electronics' },
  { id: 3, name: 'Desk Chair', price: '$350', category: 'Furniture' }
];

const productTemplate = (props) => {
  return (
    <div className="product-item">
      <div className="product-info">
        <strong>{props.name}</strong>
        <small className="category">{props.category}</small>
      </div>
      <div className="product-price">{props.price}</div>
    </div>
  );
};

<ComboBoxComponent 
  dataSource={productData}
  fields={{ text: 'name', value: 'id' }}
  itemTemplate={productTemplate}
/>
```

**CSS:**
```css
.product-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
}

.product-info {
  flex: 1;
}

.product-info strong {
  display: block;
}

.category {
  color: #999;
  font-size: 12px;
}

.product-price {
  font-weight: 600;
  color: #0066cc;
  min-width: 80px;
  text-align: right;
}
```

### Example 2: Country Selection with Flags

```tsx
const countryData = [
  { code: 'US', name: 'United States', flag: '🇺🇸' },
  { code: 'UK', name: 'United Kingdom', flag: '🇬🇧' },
  { code: 'CA', name: 'Canada', flag: '🇨🇦' },
  { code: 'AU', name: 'Australia', flag: '🇦🇺' }
];

const countryTemplate = (props) => {
  return (
    <div className="country-item">
      <span className="flag">{props.flag}</span>
      <span className="name">{props.name}</span>
      <span className="code">{props.code}</span>
    </div>
  );
};

<ComboBoxComponent 
  dataSource={countryData}
  fields={{ text: 'name', value: 'code' }}
  itemTemplate={countryTemplate}
/>
```

**CSS:**
```css
.country-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px;
}

.flag {
  font-size: 20px;
}

.name {
  flex: 1;
}

.code {
  color: #999;
  font-size: 12px;
  font-weight: 500;
}
```

### Example 3: Multi-Field Display with Status

```tsx
const ticketData = [
  { id: 'TKT001', title: 'Login error', priority: 'High', status: 'Open' },
  { id: 'TKT002', title: 'Dashboard lag', priority: 'Medium', status: 'In Progress' },
  { id: 'TKT003', title: 'Typo fix', priority: 'Low', status: 'Closed' }
];

const priorityColor = { 'High': 'red', 'Medium': 'orange', 'Low': 'green' };
const statusIcon = { 'Open': '🔴', 'In Progress': '🟡', 'Closed': '🟢' };

const ticketTemplate = (props) => {
  return (
    <div className="ticket-item">
      <div className="ticket-header">
        <strong>{props.id}</strong>
        <span className="status">{statusIcon[props.status]}</span>
      </div>
      <div className="ticket-title">{props.title}</div>
      <div className="ticket-meta">
        <span
          className="priority-badge"
          style={{ borderLeftColor: priorityColor[props.priority] }}
        >
          {props.priority}
        </span>
      </div>
    </div>
  );
};

<ComboBoxComponent 
  dataSource={ticketData}
  fields={{ text: 'title', value: 'id' }}
  itemTemplate={ticketTemplate}
/>
```

---

## Template Checklist

- [ ] itemTemplate function returns valid JSX/HTML
- [ ] Template accesses correct data properties
- [ ] CSS styles applied and responsive
- [ ] Performance acceptable (avoid complex calculations in template)
- [ ] No console errors from template rendering
- [ ] Selected value displays correctly
- [ ] Mobile/responsive tested

---

## Next Steps

- **Need virtual scrolling for performance?** → See [advanced-features.md](advanced-features.md)
- **Want theme integration?** → Check [styling-and-theming.md](styling-and-theming.md)
- **Grouping with templates?** → Read [grouping-and-sorting.md](grouping-and-sorting.md)
- **Troubleshooting template issues?** → Visit [troubleshooting.md](troubleshooting.md)
