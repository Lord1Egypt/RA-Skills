# Common How-To Guides for React ListBox

## Table of Contents
- [Add Items Dynamically](#add-items-dynamically)
- [Select Items Programmatically](#select-items-programmatically)
- [Enable or Disable Items](#enable-or-disable-items)
- [Filter ListBox Data](#filter-listbox-data)
- [Enable Scroller](#enable-scroller)
- [Form Integration & Submit](#form-integration--submit)

---

## Add Items Dynamically

### Add Single or Multiple Items

Use the `addItems` method to add new items to the ListBox:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { useRef } from 'react';

function App() {
  const listBoxRef = useRef();

  const data = [
    { text: 'JavaScript', id: 'list-01' },
    { text: 'React', id: 'list-02' },
    { text: 'Vue', id: 'list-03' }
  ];

  const addNewItems = () => {
    // Add single item
    if (listBoxRef.current) {
      listBoxRef.current.addItems([
        { text: 'TypeScript', id: 'list-04' },
        { text: 'Angular', id: 'list-05' }
      ]);
    }
  };

  return (
    <div>
      <ListBoxComponent 
        ref={listBoxRef}
        dataSource={data}
        fields={{ text: 'text', value: 'id' }}
      />
      <ButtonComponent onClick={addNewItems}>
        Add TypeScript & Angular
      </ButtonComponent>
    </div>
  );
}

export default App;
```

### Prevent Duplicate Items

Check if item exists before adding:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useRef } from 'react';

function App() {
  const listBoxRef = useRef();
  const data = [{ text: 'Item 1', id: '1' }];

  const addIfNotExists = (newItem) => {
    if (listBoxRef.current) {
      // Check if item already exists
      const exists = data.find(item => item.id === newItem.id);
      if (!exists) {
        listBoxRef.current.addItems([newItem]);
        console.log('Item added');
      } else {
        console.log('Item already exists');
      }
    }
  };

  return (
    <div>
      <ListBoxComponent 
        ref={listBoxRef}
        dataSource={data}
        fields={{ text: 'text', value: 'id' }}
      />
      <button onClick={() => addIfNotExists({ text: 'Item 2', id: '2' })}>
        Add Item 2
      </button>
    </div>
  );
}

export default App;
```

### Add Items from Array Input

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useState, useRef } from 'react';

function App() {
  const listBoxRef = useRef();
  const [inputValue, setInputValue] = useState('');

  const handleAddItem = () => {
    if (inputValue.trim()) {
      const newItem = {
        text: inputValue,
        id: Date.now().toString()
      };
      if (listBoxRef.current) {
        listBoxRef.current.addItems([newItem]);
        setInputValue('');
      }
    }
  };

  return (
    <div>
      <input
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        placeholder="Enter item text"
        onKeyPress={(e) => e.key === 'Enter' && handleAddItem()}
      />
      <button onClick={handleAddItem}>Add Item</button>
      
      <ListBoxComponent 
        ref={listBoxRef}
        dataSource={[]}
        fields={{ text: 'text', value: 'id' }}
      />
    </div>
  );
}

export default App;
```

---

## Select Items Programmatically

### Select Single Item

Use `selectItems` method to select specific items:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { useRef } from 'react';

function App() {
  const listBoxRef = useRef();

  const data = [
    { text: 'JavaScript', id: '1' },
    { text: 'TypeScript', id: '2' },
    { text: 'React', id: '3' },
    { text: 'Vue', id: '4' }
  ];

  const selectTypeScript = () => {
    if (listBoxRef.current) {
      // Pass text value; use isValue=true to select by value instead
      listBoxRef.current.selectItems(['TypeScript']);
    }
  };

  return (
    <div>
      <ListBoxComponent 
        ref={listBoxRef}
        dataSource={data}
        fields={{ text: 'text', value: 'id' }}
      />
      <ButtonComponent onClick={selectTypeScript}>
        Select TypeScript
      </ButtonComponent>
    </div>
  );
}

export default App;
```

### Select Multiple Items

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useRef } from 'react';

function App() {
  const listBoxRef = useRef();

  const data = [
    { text: 'HTML', id: '1' },
    { text: 'CSS', id: '2' },
    { text: 'JavaScript', id: '3' },
    { text: 'React', id: '4' }
  ];

  const selectMultiple = () => {
    if (listBoxRef.current) {
      // Pass text values; set isValue=true as third argument to select by value
      listBoxRef.current.selectItems(['CSS', 'JavaScript', 'React']);
    }
  };

  return (
    <div>
      <ListBoxComponent 
        ref={listBoxRef}
        dataSource={data}
        fields={{ text: 'text', value: 'id' }}
        selectionSettings={{ mode: 'Multiple' }}
      />
      <button onClick={selectMultiple}>
        Select CSS, JavaScript, React
      </button>
    </div>
  );
}

export default App;
```

### Auto-Select on Component Load

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useEffect, useRef } from 'react';

function App() {
  const listBoxRef = useRef();

  const data = [
    { text: 'Option A', id: '1' },
    { text: 'Option B', id: '2' },
    { text: 'Option C', id: '3' }
  ];

  useEffect(() => {
    // Auto-select on component creation using text value
    if (listBoxRef.current) {
      listBoxRef.current.selectItems(['Option B']);
    }
  }, []);

  return (
    <ListBoxComponent 
      ref={listBoxRef}
      dataSource={data}
      fields={{ text: 'text', value: 'id' }}
    />
  );
}

export default App;
```

---

## Enable or Disable Items

### Disable Specific Items

Some items cannot be selected:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { useState } from 'react';

function App() {
  const [data, setData] = useState([
    { text: 'Free Feature', id: '1', disabled: false },
    { text: 'Premium Feature', id: '2', disabled: true },
    { text: 'Another Free Feature', id: '3', disabled: false }
  ]);

  const togglePremiumAccess = () => {
    setData(prevData =>
      prevData.map(item =>
        item.id === '2' ? { ...item, disabled: !item.disabled } : item
      )
    );
  };

  return (
    <div>
      <ListBoxComponent 
        dataSource={data}
        fields={{ 
          text: 'text', 
          value: 'id',
          disabled: 'disabled'
        }}
      />
      <ButtonComponent onClick={togglePremiumAccess}>
        Toggle Premium Access
      </ButtonComponent>
    </div>
  );
}

export default App;
```

### Disable All Items

Use the `enableItems` method to disable or enable all items by passing their text values:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useRef } from 'react';

function App() {
  const listBoxRef = useRef();

  const data = [
    { text: 'Item 1', id: '1' },
    { text: 'Item 2', id: '2' },
    { text: 'Item 3', id: '3' }
  ];

  const allTexts = data.map(item => item.text);

  const disableAllItems = () => {
    if (listBoxRef.current) {
      listBoxRef.current.enableItems(allTexts, false);
    }
  };

  const enableAllItems = () => {
    if (listBoxRef.current) {
      listBoxRef.current.enableItems(allTexts, true);
    }
  };

  return (
    <div>
      <ListBoxComponent 
        ref={listBoxRef}
        dataSource={data}
        fields={{ text: 'text', value: 'id' }}
      />
      <button onClick={disableAllItems}>Disable All</button>
      <button onClick={enableAllItems}>Enable All</button>
    </div>
  );
}

export default App;
```

---

## Filter ListBox Data

### Real-time Text Filter

Filter items as user types:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useRef, useState } from 'react';
import { Query } from '@syncfusion/ej2-data';

function App() {
  const listBoxRef = useRef();
  const [searchText, setSearchText] = useState('');

  const allData = [
    { text: 'JavaScript', id: '1' },
    { text: 'TypeScript', id: '2' },
    { text: 'React', id: '3' },
    { text: 'Vue', id: '4' },
    { text: 'Angular', id: '5' }
  ];

  const handleFilterChange = (e) => {
    setSearchText(e.target.value);
    
    if (listBoxRef.current) {
      // Filter using Query
      listBoxRef.current.filter(
        allData,
        new Query().where('text', 'contains', e.target.value, true)
      );
    }
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Search..."
        value={searchText}
        onChange={handleFilterChange}
      />
      <ListBoxComponent 
        ref={listBoxRef}
        dataSource={allData}
        fields={{ text: 'text', value: 'id' }}
      />
    </div>
  );
}

export default App;
```

### Filter by Category

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useState, useRef } from 'react';

function App() {
  const listBoxRef = useRef();
  const [selectedCategory, setSelectedCategory] = useState('All');

  const allData = [
    { text: 'JavaScript', id: '1', category: 'Language' },
    { text: 'TypeScript', id: '2', category: 'Language' },
    { text: 'React', id: '3', category: 'Framework' },
    { text: 'Vue', id: '4', category: 'Framework' }
  ];

  const filterByCategory = (category) => {
    setSelectedCategory(category);
    
    if (listBoxRef.current) {
      const filtered = category === 'All'
        ? allData
        : allData.filter(item => item.category === category);
      
      listBoxRef.current.dataSource = filtered;
    }
  };

  return (
    <div>
      <div>
        <button onClick={() => filterByCategory('All')}>All</button>
        <button onClick={() => filterByCategory('Language')}>Languages</button>
        <button onClick={() => filterByCategory('Framework')}>Frameworks</button>
      </div>
      
      <ListBoxComponent 
        ref={listBoxRef}
        dataSource={allData}
        fields={{ text: 'text', value: 'id' }}
      />
    </div>
  );
}

export default App;
```

### Clear Filter

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useRef } from 'react';

function App() {
  const listBoxRef = useRef();

  const allData = [
    { text: 'Item 1', id: '1' },
    { text: 'Item 2', id: '2' },
    { text: 'Item 3', id: '3' }
  ];

  const clearFilter = () => {
    if (listBoxRef.current) {
      listBoxRef.current.dataSource = allData;
    }
  };

  return (
    <div>
      <ListBoxComponent 
        ref={listBoxRef}
        dataSource={allData}
        fields={{ text: 'text', value: 'id' }}
        allowFiltering={true}
      />
      <button onClick={clearFilter}>Clear Filter</button>
    </div>
  );
}

export default App;
```

---

## Enable Scroller

### Set ListBox Height

Enable scrolling by setting explicit height:

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

### Responsive Scroller Height

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import './App.css';

function App() {
  const data = Array.from({ length: 30 }, (_, i) => ({
    text: `Item ${i + 1}`,
    id: String(i + 1)
  }));

  return (
    <div className="listbox-container">
      <ListBoxComponent 
        dataSource={data}
        fields={{ text: 'text', value: 'id' }}
        height="100%"
      />
    </div>
  );
}

export default App;
```

**CSS:**
```css
.listbox-container {
  height: 300px;
  /* On mobile: */
}

@media (max-width: 480px) {
  .listbox-container {
    height: 200px;
  }
}
```

---

## Form Integration & Submit

### ListBox in Form with Validation

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useState } from 'react';

function App() {
  const [selected, setSelected] = useState(null);
  const [error, setError] = useState(null);

  const data = [
    { text: 'JavaScript', id: '1' },
    { text: 'React', id: '2' },
    { text: 'Vue', id: '3' }
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!selected) {
      setError('Please select a framework');
      return;
    }
    
    setError(null);
    console.log('Form submitted with:', selected);
    // Submit to API
  };

  const handleChange = (e) => {
    setSelected(e.value);
    setError(null);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="framework">Select Framework:</label>
        <ListBoxComponent 
          id="framework"
          dataSource={data}
          fields={{ text: 'text', value: 'id' }}
          change={handleChange}
          aria-required="true"
        />
        {error && <span className="error">{error}</span>}
      </div>
      
      <button type="submit">Submit</button>
    </form>
  );
}

export default App;
```

### Multiple Selection Form Submit

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useRef } from 'react';

function App() {
  const listBoxRef = useRef();

  const data = [
    { text: 'HTML', id: '1' },
    { text: 'CSS', id: '2' },
    { text: 'JavaScript', id: '3' },
    { text: 'React', id: '4' }
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const selected = listBoxRef.current.value;
    
    if (!selected || selected.length === 0) {
      alert('Please select at least one skill');
      return;
    }
    
    console.log('Selected skills:', selected);
    
    // Send to server
    const formData = new FormData();
    formData.append('skills', JSON.stringify(selected));
    
    // Example API call:
    // fetch('/api/submit-form', { method: 'POST', body: formData })
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>Select Your Skills:</label>
      <ListBoxComponent 
        ref={listBoxRef}
        dataSource={data}
        fields={{ text: 'text', value: 'id' }}
        selectionSettings={{ mode: 'Multiple' }}
      />
      <button type="submit">Submit Form</button>
    </form>
  );
}

export default App;
```

### Get Form Data on Submit

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useRef } from 'react';

function App() {
  const listBoxRef = useRef();

  const handleFormSubmit = (e) => {
    e.preventDefault();
    
    // Get selected values
    const selectedValue = listBoxRef.current.value;
    
    // Get all form data
    const formData = {
      framework: selectedValue,
      timestamp: new Date().toISOString()
    };
    
    console.log('Form Data:', formData);
    
    // Validate
    if (!formData.framework) {
      alert('Please make a selection');
      return;
    }
    
    // Submit
    // sendToServer(formData);
  };

  const data = [
    { text: 'React', id: '1' },
    { text: 'Vue', id: '2' },
    { text: 'Angular', id: '3' }
  ];

  return (
    <form onSubmit={handleFormSubmit}>
      <fieldset>
        <legend>Choose Framework</legend>
        
        <ListBoxComponent 
          ref={listBoxRef}
          dataSource={data}
          fields={{ text: 'text', value: 'id' }}
        />
      </fieldset>
      
      <button type="submit">Submit</button>
      <button type="reset">Clear</button>
    </form>
  );
}

export default App;
```

---

## Troubleshooting

### addItems not working
- Ensure ListBox ref is properly assigned
- Use `const newItem = { text: '...', id: '...' }`
- Check that you're calling on the ListBox instance

### selectItems doesn't select
- Pass item text values by default: `selectItems(['TypeScript'])`
- To select by value field, pass `true` as the third argument: `selectItems(['2'], true)`
- For multiple selection, pass an array: `['Item 1', 'Item 2']`
- Ensure mode is 'Multiple' for multi-select

### Filter returns no results
- Check Query syntax and field names
- Use case-insensitive: `.where('text', 'contains', searchText, true)`
- Ensure data property exists in all items

### Disabled items still selectable
- Add `disabled` property to data: `{ text: '...', disabled: true }`
- Map with fields: `fields={{ disabled: 'disabled' }}`
- Make sure property name matches

### Form submission not capturing selection
- Use ref to access ListBox: `listBoxRef.current.value`
- Pass onChange handler and maintain state
- Validate before submit: `if (!selected) { error }`
