# Filtering & Search Behavior

## Table of Contents
- [Overview](#overview)
- [Enable Filtering](#enable-filtering)
- [Custom Filter Functions](#custom-filter-functions)
- [Search Configuration](#search-configuration)
- [Performance Optimization](#performance-optimization)
- [No Results Handling](#no-results-handling)

---

## Overview

Filtering allows users to search/find items by typing. The ComboBox provides:

- **Built-in filtering:** Case-insensitive text search by default
- **Custom filters:** Advanced filtering logic (regex, multiple fields)
- **Case sensitivity:** Option to match case exactly
- **Performance:** Handle 10,000+ items efficiently

---

## Enable Filtering

### Basic Filtering (Default Behavior)

```tsx
import { ComboBoxComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const sportsList = ['Cricket', 'Football', 'Tennis', 'Badminton', 'Volleyball'];

  return (
    <ComboBoxComponent 
      id="sports-combo"
      dataSource={sportsList}
      allowFiltering={true}           // Enable search box
      placeholder="Type to search..."
    />
  );
}
```

**User Behavior:**
1. User clicks dropdown → Search box appears
2. Types "foot" → Filters to show only "Football"
3. Selects result or continues typing

### With JSON Objects

```tsx
const employeeData = [
  { empId: 'EMP001', empName: 'Alice Johnson', department: 'Engineering' },
  { empId: 'EMP002', empName: 'Bob Smith', department: 'Sales' },
  { empId: 'EMP003', empName: 'Carol Davis', department: 'Engineering' }
];

const fields = { text: 'empName', value: 'empId' };

<ComboBoxComponent 
  id="emp-combo"
  dataSource={employeeData}
  fields={fields}
  allowFiltering={true}
  placeholder="Select an employee"
/>
```

---

## Custom Filter Functions

### Simple Custom Filter

Create filtering logic beyond text matching:

```tsx
export default function App() {
  const items = [
    { id: 1, name: 'Apple', category: 'Fruit' },
    { id: 2, name: 'Banana', category: 'Fruit' },
    { id: 3, name: 'Carrot', category: 'Vegetable' },
    { id: 4, name: 'Cucumber', category: 'Vegetable' }
  ];

  // Custom filter: search by name OR category
  const customFilter = (e) => {
    if (e.text === '') {
      e.updateData(items);
    } else {
      const searchText = e.text.toLowerCase();
      const filtered = items.filter(item =>
        item.name.toLowerCase().includes(searchText) ||
        item.category.toLowerCase().includes(searchText)
      );
      e.updateData(filtered);
    }
  };

  return (
    <ComboBoxComponent 
      id="items-combo"
      dataSource={items}
      fields={{ text: 'name', value: 'id' }}
      allowFiltering={true}
      filtering={customFilter}
      placeholder="Search by name or category..."
    />
  );
}
```

### Advanced: Regex-Based Filter

```tsx
const advancedFilter = (e) => {
  if (e.text === '') {
    e.updateData(items);
  } else {
    try {
      const regex = new RegExp(e.text, 'i');  // Case-insensitive regex
      const filtered = items.filter(item => regex.test(item.name));
      e.updateData(filtered);
    } catch (err) {
      // Invalid regex, return original data
      e.updateData(items);
    }
  }
};
```

### Debounced Filter (For Remote APIs)

Reduce API calls while user is typing:

```tsx
import { useState, useCallback } from 'react';
import { DataManager, WebApiAdaptor } from '@syncfusion/ej2-data';

export default function App() {
  const [dataManager] = useState(
    new DataManager({
      url: '/api/search',
      adaptor: new WebApiAdaptor()
    })
  );

  const debounce = (func, delay) => {
    let timeoutId;
    return (...args) => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => func(...args), delay);
    };
  };

  const debouncedFilter = useCallback(
    debounce((e) => {
      if (e.text.length > 2) {  // Only search if 3+ characters
        fetch(`/api/search?q=${e.text}`)
          .then(res => res.json())
          .then(data => e.updateData(data));
      }
    }, 500),  // Wait 500ms after user stops typing
    []
  );

  return (
    <ComboBoxComponent 
      id="search-combo"
      dataSource={dataManager}
      allowFiltering={true}
      filtering={debouncedFilter}
      placeholder="Type at least 3 characters..."
    />
  );
}
```

---

## Search Configuration

### Filter Operator Options

```tsx
<ComboBoxComponent 
  id="combo"
  dataSource={items}
  fields={{ text: 'name', value: 'id' }}
  allowFiltering={true}
  filterType="StartsWith"    // "Contains", "StartsWith", "EndsWith"
  placeholder="Select item"
/>
```

| filterType | Behavior | Example |
|-----------|----------|---------|
| `"Contains"` (default) | Match anywhere in text | "on" matches "London" |
| `"StartsWith"` | Match beginning | "Lon" matches "London" |
| `"EndsWith"` | Match ending | "don" matches "London" |

### Case-Sensitive Search

By default, filtering is case-insensitive. To enable case-sensitivity:

```tsx
const caseSensitiveFilter = (e) => {
  const searchText = e.text;
  const filtered = items.filter(item =>
    item.name.includes(searchText)  // No .toLowerCase()
  );
  e.updateData(filtered);
};

<ComboBoxComponent 
  filtering={caseSensitiveFilter}
  allowFiltering={true}
/>
```

### Minimum Characters Before Filter

Only filter after user types minimum characters:

```tsx
const minLengthFilter = (e) => {
  const MIN_CHARS = 2;
  
  if (e.text.length < MIN_CHARS) {
    // Show all items
    e.updateData(items);
  } else {
    const searchText = e.text.toLowerCase();
    const filtered = items.filter(item =>
      item.name.toLowerCase().includes(searchText)
    );
    e.updateData(filtered);
  }
};
```

---

## Performance Optimization

### Virtual Scrolling for Large Datasets

When you have 10,000+ items, use virtual scrolling to render only visible items:

```tsx
<ComboBoxComponent 
  id="large-combo"
  dataSource={largeDataset}
  allowFiltering={true}
  enableVirtualization={true}    // Render only visible items
  popupHeight="300px"
  placeholder="Searching 50,000 items..."
/>
```

**When to use:** >5,000 items AND filtering enabled

---

### Lazy Loading from API

Load items only when user searches:

```tsx
export default function App() {
  const [data, setData] = useState([]);

  const lazyFilter = (e) => {
    if (e.text.length > 1) {
      // Fetch from API with search term
      fetch(`/api/items?search=${e.text}&limit=100`)
        .then(res => res.json())
        .then(items => {
          e.updateData(items);
          setData(items);
        });
    } else {
      setData([]);
    }
  };

  return (
    <ComboBoxComponent 
      dataSource={data}
      allowFiltering={true}
      filtering={lazyFilter}
      placeholder="Type to load suggestions..."
    />
  );
}
```

---

## No Results Handling

### Show Custom Message When No Items Match

```tsx
const customFilter = (e) => {
  const searchText = e.text.toLowerCase();
  const filtered = items.filter(item =>
    item.name.toLowerCase().includes(searchText)
  );
  
  if (filtered.length === 0 && e.text.length > 0) {
    // Add message item
    filtered.push({
      id: 'no-results',
      name: `No results for "${e.text}"`,
      disabled: true
    });
  }
  
  e.updateData(filtered);
};
```

### Empty Template

Customize the UI when no items are found:

```tsx
const noRecordsTemplate = () => {
  return (
    <div className="no-records">
      <p>😕 No matching items found</p>
      <small>Try a different search term</small>
    </div>
  );
};

<ComboBoxComponent 
  allowFiltering={true}
  noRecordsTemplate={noRecordsTemplate}
/>
```

---

## Common Patterns

### Pattern 1: Search Multiple Fields

```tsx
const multiFieldFilter = (e) => {
  const searchText = e.text.toLowerCase();
  const filtered = items.filter(item => {
    return (
      item.name.toLowerCase().includes(searchText) ||
      item.email.toLowerCase().includes(searchText) ||
      item.phone.includes(searchText)
    );
  });
  e.updateData(filtered);
};
```

### Pattern 2: Highlight Matching Text

```tsx
const highlightFilter = (e) => {
  const searchText = e.text.toLowerCase();
  const filtered = items.filter(item =>
    item.name.toLowerCase().includes(searchText)
  );
  e.updateData(filtered);
};

const itemTemplate = (props) => {
  return (
    <span>
      {props.name.replace(
        new RegExp(searchText, 'gi'),
        match => `<strong>${match}</strong>`
      )}
    </span>
  );
};
```

### Pattern 3: Fetch Suggestions from API

```tsx
export default function App() {
  const fetchSuggestions = (e) => {
    if (e.text.length > 2) {
      // Debounce API calls
      setTimeout(() => {
        fetch(`/api/autocomplete?query=${e.text}`)
          .then(res => res.json())
          .then(suggestions => e.updateData(suggestions));
      }, 300);
    }
  };

  return (
    <ComboBoxComponent 
      allowFiltering={true}
      filtering={fetchSuggestions}
      placeholder="Type to get suggestions..."
    />
  );
}
```

---

## Filtering Checklist

- [ ] `allowFiltering={true}` set
- [ ] Filter behavior meets requirements (Contains, StartsWith, etc.)
- [ ] Custom filter function handles empty search
- [ ] Performance tested with actual data volume
- [ ] No results scenario handled gracefully
- [ ] API calls debounced (if using remote data)
- [ ] Mobile UX tested (responsive filter bar)

---

## Next Steps

- **Want to organize filtered results?** → See [grouping-and-sorting.md](grouping-and-sorting.md)
- **Show rich content in list?** → Check [templates-and-customization.md](templates-and-customization.md)
- **Large dataset issues?** → Read [advanced-features.md](advanced-features.md)
- **Styling the filter?** → Explore [styling-and-theming.md](styling-and-theming.md)
