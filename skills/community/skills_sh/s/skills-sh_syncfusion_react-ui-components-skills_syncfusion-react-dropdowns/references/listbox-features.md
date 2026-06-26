# Advanced Features in React ListBox

## Table of Contents
- [Filtering and Search](#filtering-and-search)
- [Sorting and Grouping](#sorting-and-grouping)
- [Drag and Drop](#drag-and-drop)
- [Dual ListBox (Transfer)](#dual-listbox-transfer)
- [Scroller Configuration](#scroller-configuration)
- [Enable/Disable Items](#enabledisable-items)
- [Common Patterns](#common-patterns)
- [Troubleshooting](#troubleshooting)

---

## Filtering and Search

### Enable Built-in Filter

Add a search input above the list:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const data = [
    { text: 'JavaScript', id: '1' },
    { text: 'TypeScript', id: '2' },
    { text: 'React', id: '3' },
    { text: 'Vue', id: '4' }
  ];

  return (
    <ListBoxComponent 
      dataSource={data}
      fields={{ text: 'text', value: 'id' }}
      allowFiltering={true}
      filterBarPlaceholder="Search languages"
    />
  );
}

export default App;
```

### Custom Filter

Implement custom filtering logic:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useState } from 'react';

function App() {
  const allData = [
    { text: 'JavaScript', id: '1', category: 'Language' },
    { text: 'React', id: '2', category: 'Framework' },
    { text: 'TypeScript', id: '3', category: 'Language' },
    { text: 'Vue', id: '4', category: 'Framework' }
  ];

  const [searchText, setSearchText] = useState('');

  const filteredData = allData.filter(item =>
    item.text.toLowerCase().includes(searchText.toLowerCase())
  );

  return (
    <div>
      <input
        type="text"
        placeholder="Search..."
        value={searchText}
        onChange={(e) => setSearchText(e.target.value)}
      />
      <ListBoxComponent 
        dataSource={filteredData}
        fields={{ text: 'text', value: 'id' }}
      />
    </div>
  );
}

export default App;
```

### Filter by Category

Filter items based on category selection:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useState } from 'react';

function App() {
  const allData = [
    { text: 'JavaScript', id: '1', category: 'Language' },
    { text: 'TypeScript', id: '2', category: 'Language' },
    { text: 'React', id: '3', category: 'Framework' },
    { text: 'Vue', id: '4', category: 'Framework' }
  ];

  const [selectedCategory, setSelectedCategory] = useState('All');

  const filteredData = selectedCategory === 'All'
    ? allData
    : allData.filter(item => item.category === selectedCategory);

  return (
    <div>
      <div>
        <button onClick={() => setSelectedCategory('All')}>All</button>
        <button onClick={() => setSelectedCategory('Language')}>Languages</button>
        <button onClick={() => setSelectedCategory('Framework')}>Frameworks</button>
      </div>
      <ListBoxComponent 
        dataSource={filteredData}
        fields={{ text: 'text', value: 'id' }}
      />
    </div>
  );
}

export default App;
```

---

## Sorting and Grouping

### Group by Category

Organize items by category:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const data = [
    { text: 'HTML', id: '1', type: 'Markup' },
    { text: 'CSS', id: '2', type: 'Styling' },
    { text: 'JavaScript', id: '3', type: 'Programming' },
    { text: 'TypeScript', id: '4', type: 'Programming' }
  ];

  return (
    <ListBoxComponent 
      dataSource={data}
      fields={{ 
        text: 'text', 
        value: 'id',
        groupBy: 'type'
      }}
    />
  );
}

export default App;
```

### Sort Items Using Built-in sortOrder

Use the `sortOrder` property to sort the data source automatically:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const data = [
    { text: 'Vue', id: '1' },
    { text: 'JavaScript', id: '2' },
    { text: 'React', id: '3' },
    { text: 'Angular', id: '4' }
  ];

  return (
    <ListBoxComponent 
      dataSource={data}
      fields={{ text: 'text', value: 'id' }}
      sortOrder="Ascending"
    />
  );
}

export default App;
```

### Sort Descending

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const data = [
    { text: 'React', id: '1' },
    { text: 'Vue', id: '2' },
    { text: 'Angular', id: '3' }
  ];

  return (
    <ListBoxComponent 
      dataSource={data}
      fields={{ text: 'text', value: 'id' }}
      sortOrder="Descending"
    />
  );
}

export default App;
```

---

## Drag and Drop

### Enable Drag and Drop

Allow users to reorder items:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const data = [
    { text: 'Item 1', id: '1' },
    { text: 'Item 2', id: '2' },
    { text: 'Item 3', id: '3' },
    { text: 'Item 4', id: '4' }
  ];

  const handleDragStart = (e) => {
    console.log('Dragging:', e);
  };

  const handleDrop = (e) => {
    console.log('Dropped:', e);
  };

  return (
    <ListBoxComponent 
      dataSource={data}
      fields={{ text: 'text', value: 'id' }}
      allowDragAndDrop={true}
      dragStart={handleDragStart}
      drop={handleDrop}
    />
  );
}

export default App;
```

### Reordering with State

Track reordered items:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useState } from 'react';

function App() {
  const [data, setData] = useState([
    { text: 'Priority 1', id: '1' },
    { text: 'Priority 2', id: '2' },
    { text: 'Priority 3', id: '3' }
  ]);

  const handleDrop = (e) => {
    // Update data order when dropped
    const newData = [...data];
    const [removed] = newData.splice(e.previousIndex, 1);
    newData.splice(e.currentIndex, 0, removed);
    setData(newData);
  };

  return (
    <div>
      <ListBoxComponent 
        dataSource={data}
        fields={{ text: 'text', value: 'id' }}
        allowDragAndDrop={true}
        drop={handleDrop}
      />
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}

export default App;
```

### Between Two ListBoxes

Transfer items between two lists using the `scope` prop and `drag`/`drop` events:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const available = [
    { text: 'Item A', id: '1' },
    { text: 'Item B', id: '2' },
    { text: 'Item C', id: '3' }
  ];

  const selected = [
    { text: 'Item D', id: '4' }
  ];

  const handleDrop = (e) => {
    // e.source.currentData — items in source after drop
    // e.destination.currentData — items in destination after drop
    console.log('Source after drop:', e.source.currentData);
    console.log('Destination after drop:', e.destination.currentData);
  };

  return (
    <div style={{ display: 'flex', gap: '20px' }}>
      <div>
        <h3>Available</h3>
        <ListBoxComponent 
          dataSource={available}
          fields={{ text: 'text', value: 'id' }}
          allowDragAndDrop={true}
          scope="#selected-list"
          drop={handleDrop}
        />
      </div>
      <div>
        <h3>Selected</h3>
        <ListBoxComponent 
          id="selected-list"
          dataSource={selected}
          fields={{ text: 'text', value: 'id' }}
          allowDragAndDrop={true}
        />
      </div>
    </div>
  );
}

export default App;
```

---

## Dual ListBox (Transfer)

### Two-Way Transfer

Create a dual ListBox for selecting/deselecting items:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useState } from 'react';

function App() {
  const [available, setAvailable] = useState([
    { text: 'HTML', id: '1' },
    { text: 'CSS', id: '2' },
    { text: 'JavaScript', id: '3' },
    { text: 'React', id: '4' },
    { text: 'Vue', id: '5' }
  ]);

  const [selected, setSelected] = useState([]);

  const moveToSelected = () => {
    // In production: get selected items from ListBox ref
    const item = available[0];
    setSelected([...selected, item]);
    setAvailable(available.filter(i => i.id !== item.id));
  };

  const moveToAvailable = () => {
    const item = selected[0];
    setAvailable([...available, item]);
    setSelected(selected.filter(i => i.id !== item.id));
  };

  return (
    <div style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
      <div>
        <h3>Available</h3>
        <ListBoxComponent 
          dataSource={available}
          fields={{ text: 'text', value: 'id' }}
          height="300px"
        />
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        <button onClick={moveToSelected}>→ Add</button>
        <button onClick={moveToAvailable}>← Remove</button>
      </div>

      <div>
        <h3>Selected</h3>
        <ListBoxComponent 
          dataSource={selected}
          fields={{ text: 'text', value: 'id' }}
          height="300px"
        />
      </div>
    </div>
  );
}

export default App;
```

---

## Scroller Configuration

### Set ListBox Height

Control the visible area with height:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const data = Array.from({ length: 50 }, (_, i) => ({
    text: `Item ${i + 1}`,
    id: String(i + 1)
  }));

  return (
    <ListBoxComponent 
      dataSource={data}
      fields={{ text: 'text', value: 'id' }}
      height="300px"
    />
  );
}

export default App;
```

---

## Enable/Disable Items

### Disable Specific Items

Some items cannot be selected:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const data = [
    { text: 'JavaScript', id: '1', disabled: false },
    { text: 'TypeScript (Coming Soon)', id: '2', disabled: true },
    { text: 'React', id: '3', disabled: false },
    { text: 'Vue (Deprecated)', id: '4', disabled: true }
  ];

  return (
    <ListBoxComponent 
      dataSource={data}
      fields={{ 
        text: 'text', 
        value: 'id',
        disabled: 'disabled'
      }}
    />
  );
}

export default App;
```

### Dynamically Enable/Disable

Toggle item availability based on state:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useState } from 'react';

function App() {
  const [data, setData] = useState([
    { text: 'Free Feature', id: '1', disabled: false },
    { text: 'Pro Feature', id: '2', disabled: true }
  ]);

  const toggleProFeatures = () => {
    setData(data.map(item => ({
      ...item,
      disabled: !item.disabled
    })));
  };

  return (
    <div>
      <button onClick={toggleProFeatures}>Toggle Pro Features</button>
      <ListBoxComponent 
        dataSource={data}
        fields={{ 
          text: 'text', 
          value: 'id',
          disabled: 'disabled'
        }}
      />
    </div>
  );
}

export default App;
```

---

## Common Patterns

### Search with Filter

Combine search input with filtering:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useState } from 'react';

function App() {
  const allData = [
    { text: 'JavaScript', id: '1' },
    { text: 'TypeScript', id: '2' },
    { text: 'React', id: '3' }
  ];

  const [search, setSearch] = useState('');
  const filtered = allData.filter(item =>
    item.text.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <input
        placeholder="Search..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
      <ListBoxComponent 
        dataSource={filtered}
        fields={{ text: 'text', value: 'id' }}
        allowFiltering={true}
      />
    </div>
  );
}

export default App;
```

### Grouped and Filtered

Group items while supporting search:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useState } from 'react';

function App() {
  const allData = [
    { text: 'JavaScript', id: '1', category: 'Language' },
    { text: 'TypeScript', id: '2', category: 'Language' },
    { text: 'React', id: '3', category: 'Framework' }
  ];

  const [search, setSearch] = useState('');
  const filtered = allData.filter(item =>
    item.text.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <input
        placeholder="Search..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
      <ListBoxComponent 
        dataSource={filtered}
        fields={{ 
          text: 'text', 
          value: 'id',
          groupBy: 'category'
        }}
      />
    </div>
  );
}

export default App;
```

---

## Troubleshooting

### Drag and drop not working
- Ensure `allowDragAndDrop={true}`
- Items must have unique IDs
- Check that event handlers are defined
- May need explicit styling for drop target

### Filtering shows no results
- Check data property names match field mapping
- Ensure search is case-insensitive
- Verify data contains the search term

### Grouping not displaying
- Add `groupBy` property to fields
- All items must have the grouping property
- Verify property exists in all data items

### Scroller not appearing
- Set explicit height: `height="300px"`
- Ensure data has enough items to scroll
- Check CSS doesn't override height
