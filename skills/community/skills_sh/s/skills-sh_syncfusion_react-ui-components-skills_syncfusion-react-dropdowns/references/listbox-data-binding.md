# Data Binding in React ListBox

## Table of Contents
- [Basic Data Structure](#basic-data-structure)
- [Fields Mapping](#fields-mapping)
- [Dynamic Data](#dynamic-data)
- [Grouping Data](#grouping-data)
- [Data from API](#data-from-api)
- [Common Patterns](#common-patterns)
- [Troubleshooting](#troubleshooting)

---

## Basic Data Structure

### Simple Array

The simplest data structure is an array of objects with text and value:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const data = [
    { text: 'HTML', id: '1' },
    { text: 'CSS', id: '2' },
    { text: 'JavaScript', id: '3' },
    { text: 'TypeScript', id: '4' }
  ];

  return (
    <ListBoxComponent 
      dataSource={data}
      fields={{ text: 'text', value: 'id' }}
    />
  );
}

export default App;
```

### Array of Strings (Simple Alternative)

For simple lists without IDs:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const data = ['JavaScript', 'TypeScript', 'React', 'Vue'];

  return (
    <ListBoxComponent 
      dataSource={data}
    />
  );
}

export default App;
```

---

## Fields Mapping

### Text and Value Mapping

Map data properties to display and internal values:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  // Data with different property names
  const data = [
    { name: 'JavaScript', code: 'js' },
    { name: 'TypeScript', code: 'ts' },
    { name: 'React', code: 'react' }
  ];

  return (
    <ListBoxComponent 
      dataSource={data}
      fields={{ 
        text: 'name',      // Display this property
        value: 'code'      // Use this as value
      }}
    />
  );
}

export default App;
```

### Using Icon Field

Add icons to list items using custom icons:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const data = [
    { text: 'JavaScript', id: '1', icon: '⚙️' },
    { text: 'React', id: '2', icon: '⚛️' },
    { text: 'Vue', id: '3', icon: '💚' }
  ];

  return (
    <ListBoxComponent 
      dataSource={data}
      fields={{ 
        text: 'text', 
        value: 'id',
        iconCss: 'icon'  // CSS class or icon field
      }}
    />
  );
}

export default App;
```

### Complex Object Fields

Work with nested or complex data:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const data = [
    { 
      id: '1', 
      language: { name: 'JavaScript', version: 'ES2024' },
      category: 'Language'
    },
    { 
      id: '2', 
      language: { name: 'React', version: '18.2' },
      category: 'Framework'
    }
  ];

  // For nested fields, construct the path
  const displayText = data.map(item => ({
    ...item,
    displayName: `${item.language.name} (${item.language.version})`
  }));

  return (
    <ListBoxComponent 
      dataSource={displayText}
      fields={{ text: 'displayName', value: 'id' }}
    />
  );
}

export default App;
```

---

## Dynamic Data

### Update Data After Load

Change the data source after component mounts:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useRef, useState } from 'react';

function App() {
  const listBoxRef = useRef();
  const [data, setData] = useState([
    { text: 'Item 1', id: '1' },
    { text: 'Item 2', id: '2' }
  ]);

  const addItem = () => {
    const newItem = { 
      text: `Item ${data.length + 1}`, 
      id: String(data.length + 1) 
    };
    setData([...data, newItem]);
    
    // Update ListBox
    if (listBoxRef.current) {
      listBoxRef.current.dataSource = [...data, newItem];
    }
  };

  return (
    <div>
      <ListBoxComponent 
        ref={listBoxRef}
        dataSource={data}
        fields={{ text: 'text', value: 'id' }}
      />
      <button onClick={addItem}>Add Item</button>
    </div>
  );
}

export default App;
```

### Replace All Data

Completely replace the data source:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useRef } from 'react';

function App() {
  const listBoxRef = useRef();

  const initialData = [
    { text: 'Frontend', id: '1' },
    { text: 'Backend', id: '2' }
  ];

  const backendData = [
    { text: 'Node.js', id: '1' },
    { text: 'Python', id: '2' },
    { text: 'Go', id: '3' }
  ];

  const switchCategory = () => {
    if (listBoxRef.current) {
      listBoxRef.current.dataSource = backendData;
    }
  };

  return (
    <div>
      <ListBoxComponent 
        ref={listBoxRef}
        dataSource={initialData}
        fields={{ text: 'text', value: 'id' }}
      />
      <button onClick={switchCategory}>Show Backend Languages</button>
    </div>
  );
}

export default App;
```

---

## Grouping Data

### Group Items by Category

Organize items into visual groups:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const data = [
    { text: 'JavaScript', id: '1', category: 'Language' },
    { text: 'TypeScript', id: '2', category: 'Language' },
    { text: 'React', id: '3', category: 'Framework' },
    { text: 'Vue', id: '4', category: 'Framework' },
    { text: 'Node.js', id: '5', category: 'Runtime' },
    { text: 'Deno', id: '6', category: 'Runtime' }
  ];

  return (
    <ListBoxComponent 
      dataSource={data}
      fields={{ 
        text: 'text', 
        value: 'id',
        groupBy: 'category'  // Group by this field
      }}
    />
  );
}

export default App;
```

---

## Data from API

### Fetch Data on Component Load

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useEffect, useState } from 'react';

function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate API call
    const fetchData = async () => {
      try {
        const response = await fetch('/api/languages');
        const result = await response.json();
        setData(result);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <p>Loading...</p>;

  return (
    <ListBoxComponent 
      dataSource={data}
      fields={{ text: 'text', value: 'id' }}
    />
  );
}

export default App;
```

### Mock API Example

```tsx
// Mock API endpoint data
const mockLanguages = [
  { text: 'JavaScript', id: '1', year: 1995 },
  { text: 'TypeScript', id: '2', year: 2012 },
  { text: 'Python', id: '3', year: 1989 },
  { text: 'Go', id: '4', year: 2009 }
];

// Simulate async API call
const fetchLanguages = () => 
  new Promise(resolve => {
    setTimeout(() => resolve(mockLanguages), 500);
  });

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchLanguages().then(setData);
  }, []);

  return (
    <ListBoxComponent 
      dataSource={data}
      fields={{ text: 'text', value: 'id' }}
    />
  );
}

export default App;
```

---

## Common Patterns

### Array of String IDs and Text

Simple case with just strings:

```tsx
const categories = ['Web', 'Mobile', 'Desktop', 'AI/ML'];

<ListBoxComponent dataSource={categories} />
```

### Custom Object Transformation

Transform API response to ListBox format:

```tsx
const apiResponse = [
  { name: 'JavaScript', version: '2024' },
  { name: 'React', version: '18' }
];

const transformed = apiResponse.map((item, index) => ({
  text: `${item.name} (v${item.version})`,
  id: String(index)
}));

<ListBoxComponent 
  dataSource={transformed}
  fields={{ text: 'text', value: 'id' }}
/>
```

### Hierarchical Data with Grouping

```tsx
const skillsByCategory = [
  { category: 'Frontend', skills: ['HTML', 'CSS', 'JavaScript'] },
  { category: 'Backend', skills: ['Node.js', 'Python', 'Go'] }
];

const flatData = skillsByCategory.flatMap(cat =>
  cat.skills.map((skill, idx) => ({
    text: skill,
    id: `${cat.category}-${idx}`,
    category: cat.category
  }))
);

<ListBoxComponent 
  dataSource={flatData}
  fields={{ 
    text: 'text', 
    value: 'id',
    groupBy: 'category'
  }}
/>
```

---

## Troubleshooting

### Data not displaying
- Ensure `dataSource` is an array: `[{ text: '...', id: '...' }]`
- Check `fields` mapping matches your data properties
- Data might be undefined if fetching async - use loading state

### Icons not showing
- Icons need to be defined in data: `{ text: '...', icon: 'icon-class' }`
- Map with `fields={{ iconCss: 'icon' }}`
- Or use emoji directly in text field

### Grouping not working
- Add `groupBy` property to fields
- Grouping property must exist in all data items
- Items are grouped by exact value match

### API data not loading
- Check network request in browser DevTools
- Ensure API endpoint returns correct JSON format
- Handle errors in try-catch or .catch()
- Verify CORS headers if cross-domain API

### Performance issues with large datasets
- Consider pagination or virtual scrolling
- Use filtering to reduce visible items
- Load data in chunks rather than all at once
