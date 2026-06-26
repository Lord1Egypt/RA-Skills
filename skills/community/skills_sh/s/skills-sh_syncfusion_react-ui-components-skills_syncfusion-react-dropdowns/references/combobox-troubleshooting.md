# Troubleshooting

## Table of Contents
- [Common Issues](#common-issues)
- [Performance Problems](#performance-problems)
- [Data Binding Issues](#data-binding-issues)
- [UI/Styling Issues](#uistyling-issues)
- [Migration from EJ1](#migration-from-ej1)
- [Debugging Tips](#debugging-tips)

---

## Common Issues

### Issue 1: ComboBox Not Rendering

**Symptoms:** Component doesn't appear on page or shows as blank

**Causes & Solutions:**

```tsx
// ❌ WRONG: Missing imports
export default function App() {
  return <ComboBoxComponent dataSource={items} />;
}

// ✅ CORRECT: Import component
import { ComboBoxComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  return <ComboBoxComponent dataSource={items} />;
}

// ❌ WRONG: Missing CSS
// App.tsx (no CSS imported)

// ✅ CORRECT: Import CSS
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-react-dropdowns/styles/tailwind3.css';
```

**Checklist:**
- [ ] Component imported from `@syncfusion/ej2-react-dropdowns`
- [ ] CSS files imported in App.css or App.tsx
- [ ] Component has `id` prop
- [ ] `dataSource` prop provided
- [ ] No JavaScript errors in console

---

### Issue 2: Data Not Showing in Dropdown

**Symptoms:** Dropdown appears but list is empty

**Causes & Solutions:**

```tsx
// ❌ WRONG: Missing field mapping for objects
const employees = [
  { employeeId: 1, employeeName: 'Alice' }
];

<ComboBoxComponent 
  dataSource={employees}
  placeholder="Select employee"
  // Missing fields object!
/>

// ✅ CORRECT: Provide field mapping
const fields = {
  text: 'employeeName',
  value: 'employeeId'
};

<ComboBoxComponent 
  dataSource={employees}
  fields={fields}
  placeholder="Select employee"
/>

// ❌ WRONG: Incorrect field names
const fields = { text: 'name', value: 'id' };  // Data has 'employeeName', 'employeeId'

// ✅ CORRECT: Match your data structure
const fields = { text: 'employeeName', value: 'employeeId' };
```

**Debugging:**

```tsx
// Log the data to verify structure
console.log('dataSource:', items);
console.log('Field mapping:', fields);

// Verify field names exist in data
items.forEach(item => {
  console.log(fields.text, '→', item[fields.text]);
  console.log(fields.value, '→', item[fields.value]);
});
```

---

### Issue 3: Change Event Not Firing

**Symptoms:** `change` callback never executes

**Causes & Solutions:**

```tsx
// ❌ WRONG: Change handler not provided
<ComboBoxComponent 
  dataSource={items}
  // No change handler!
/>

// ✅ CORRECT: Add change handler
const handleChange = (e) => {
  console.log('Selected value:', e.value);
  console.log('Selected item data:', e.itemData);
};

<ComboBoxComponent 
  dataSource={items}
  change={handleChange}
/>

// ✅ ALSO CORRECT: Inline handler
<ComboBoxComponent 
  dataSource={items}
  change={(e) => console.log('Selected:', e.value)}
/>

// ❌ WRONG: Handler not bound (class component issue)
export default class App extends React.Component {
  handleChange(e) {  // Not bound!
    console.log(e.value);
  }
  
  render() {
    return <ComboBoxComponent change={this.handleChange} />;
  }
}

// ✅ CORRECT: Bind in constructor
export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.handleChange = this.handleChange.bind(this);  // Bind
  }
  
  render() {
    return <ComboBoxComponent change={this.handleChange} />;
  }
}
```

---

## Performance Problems

### Issue 4: Dropdown is Slow with Large Data

**Symptoms:** Lag when opening dropdown, scrolling is sluggish, freezes

**Causes & Solutions:**

```tsx
// ❌ WRONG: 50,000 items, no virtual scrolling
<ComboBoxComponent 
  dataSource={50000items}
  // Virtual scrolling disabled!
/>

// ✅ CORRECT: Enable virtual scrolling
<ComboBoxComponent 
  dataSource={50000items}
  enableVirtualization={true}    // ← Critical for performance
  popupHeight="300px"
  allowFiltering={true}
/>

// ✅ ALSO: Use DataManager for remote data
import { DataManager, WebApiAdaptor } from '@syncfusion/ej2-data';

const dataManager = new DataManager({
  url: '/api/items',
  adaptor: new WebApiAdaptor()
});

<ComboBoxComponent 
  dataSource={dataManager}
  enableVirtualization={true}
/>
```

**Performance Checklist:**
- [ ] Virtual scrolling enabled for >5,000 items
- [ ] Filtering implemented to reduce visible items
- [ ] Remote data uses pagination/lazy loading
- [ ] Complex templates optimized
- [ ] No unnecessary re-renders

---

### Issue 5: High Memory Usage

**Symptoms:** App consumes lot of RAM, browser tab unresponsive

**Solutions:**

```tsx
// ✅ Use virtual scrolling (prevents DOM bloat)
<ComboBoxComponent 
  enableVirtualization={true}
  popupHeight="300px"
/>

// ✅ Lazy load data
export default function App() {
  const [items, setItems] = useState([]);

  const handleFilter = (e) => {
    if (e.text.length > 2) {
      // Load only matching items
      fetch(`/api/search?q=${e.text}`)
        .then(res => res.json())
        .then(data => e.updateData(data));
    }
  };

  return (
    <ComboBoxComponent 
      filtering={handleFilter}
      allowFiltering={true}
    />
  );
}

// ✅ Debounce filter calls
const debounce = (func, delay) => {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => func(...args), delay);
  };
};

const debouncedFilter = debounce((e) => {
  // Filter logic
}, 500);
```

---

## Data Binding Issues

### Issue 6: Selected Value Not Updating

**Symptoms:** `value` prop set but selection doesn't show

**Causes & Solutions:**

```tsx
// ❌ WRONG: Using value for controlled component but not updating
export default function App() {
  const [selected, setSelected] = useState('');

  return (
    <ComboBoxComponent 
      value={selected}
      dataSource={items}
      // Missing change handler!
    />
  );
}

// ✅ CORRECT: Update state in change handler
export default function App() {
  const [selected, setSelected] = useState('');

  return (
    <ComboBoxComponent 
      value={selected}
      dataSource={items}
      change={(e) => setSelected(e.value)}  // Update state
    />
  );
}

// ❌ WRONG: Value type mismatch
const items = [
  { id: 1, name: 'Item 1' },
  { id: 2, name: 'Item 2' }
];

const fields = { text: 'name', value: 'id' };

<ComboBoxComponent 
  value="1"                    // String "1"
  fields={fields}
  dataSource={items}
/>

// ✅ CORRECT: Match type
<ComboBoxComponent 
  value={1}                    // Number 1
  fields={fields}
  dataSource={items}
/>
```

---

### Issue 7: Remote Data Not Loading

**Symptoms:** DataManager URL called but no results show

**Causes & Solutions:**

```tsx
// ❌ WRONG: Incorrect API response format
const dataManager = new DataManager({
  url: '/api/items',  // API returns: { items: [...] }
  adaptor: new WebApiAdaptor()
});

// ✅ CORRECT: API should return array directly
// GET /api/items → [{ id: 1, name: 'Item 1' }, ...]

// ✅ IF API returns object with nested array, pre-process data in state
export default function App() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    fetch('/api/items')
      .then(res => res.json())
      .then(data => {
        // Extract the nested array before binding
        setItems(data.items || data);
      });
  }, []);

  return (
    <ComboBoxComponent 
      dataSource={items}
      fields={{ text: 'name', value: 'id' }}
    />
  );
}

// ❌ WRONG: Authentication not provided
const dataManager = new DataManager({
  url: '/api/secure/items'  // Requires auth token
});

// ✅ CORRECT: Add headers for auth
const dataManager = new DataManager({
  url: '/api/secure/items',
  adaptor: new WebApiAdaptor(),
  headers: [
    { 'Authorization': `Bearer ${authToken}` }
  ]
});
```

---

## UI/Styling Issues

### Issue 8: Styles Not Applying

**Symptoms:** CSS not working, component looks plain

**Causes & Solutions:**

```tsx
// ❌ WRONG: CSS imported in component
export default function App() {
  import '@syncfusion/ej2-react-dropdowns/styles/tailwind3.css';
  return <ComboBoxComponent />;
}

// ✅ CORRECT: Import CSS globally
// App.css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-dropdowns/styles/tailwind3.css";

// App.tsx
import './App.css';

// ❌ WRONG: Multiple themes imported
import '@syncfusion/ej2-react-dropdowns/styles/tailwind3.css';
import '@syncfusion/ej2-react-dropdowns/styles/bootstrap5.css';  // Conflict!

// ✅ CORRECT: Import ONE theme
import '@syncfusion/ej2-react-dropdowns/styles/tailwind3.css';
```

---

### Issue 9: Dropdown Popup Positioned Incorrectly

**Symptoms:** Popup appears in wrong location or cut off

**Causes & Solutions:**

```tsx
// ❌ WRONG: Parent container has overflow hidden
<div style={{ overflow: 'hidden', height: '100px' }}>
  <ComboBoxComponent dataSource={items} />
  {/* Popup gets clipped! */}
</div>

// ✅ CORRECT: Remove overflow from parent
<div style={{ overflow: 'visible' }}>
  <ComboBoxComponent dataSource={items} />
</div>

// ✅ OR: Use zIndex to layer popup
<ComboBoxComponent 
  dataSource={items}
  popupHeight="300px"
  style={{ zIndex: 1000 }}
/>

// CSS:
.e-combobox .e-dropdown-popup {
  z-index: 1001;  /* Higher than other content */
}
```

---

## Migration from EJ1

### Issue 10: EJ1 Code Not Working in EJ2

**Symptoms:** Old code throws errors

**Solutions:**

| EJ1 | EJ2 |
|-----|-----|
| `<input id="combo" />` with `$("#combo").ejComboBox(...)` | `<ComboBoxComponent />` JSX |
| `fields: { text: 'text', value: 'value' }` | `fields={{ text: 'text', value: 'value' }}` |
| `watermark` prop | `placeholder` prop |
| `dataSource` as JavaScript array | `dataSource` can be array, DataManager, or URL |
| `select` event | `change` event |
| jQuery plugin API | React component props & callbacks |

**Migration Example:**

```javascript
// ❌ EJ1 Code
$('#combo').ejComboBox({
  dataSource: items,
  fields: { text: 'name', value: 'id' },
  watermark: 'Choose...',
  select: function(e) {
    console.log('Selected:', e.value);
  }
});

// ✅ EJ2 Code
import { ComboBoxComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  return (
    <ComboBoxComponent 
      id="combo"
      dataSource={items}
      fields={{ text: 'name', value: 'id' }}
      placeholder="Choose..."
      change={(e) => console.log('Selected:', e.value)}
    />
  );
}
```

---

## Debugging Tips

### Enable Debug Logging

```tsx
// Verbose logging for troubleshooting
const handleChange = (e) => {
  console.group('ComboBox Change Event');
  console.log('Event:', e);
  console.log('Value:', e.value);
  console.log('Item Data:', e.itemData);
  console.log('Previous Item Data:', e.previousItemData);
  console.log('Is Interacted:', e.isInteracted);
  console.groupEnd();
};

<ComboBoxComponent 
  dataSource={items}
  change={handleChange}
/>
```

### Check Browser Console

```
1. Open DevTools (F12)
2. Go to Console tab
3. Look for errors (red X icon)
4. Add console.log() statements to trace execution
5. Check Network tab for API failures
```

### React DevTools

```
1. Install React DevTools browser extension
2. Select ComboBoxComponent in React Components tree
3. Check props and state values
4. Verify re-render frequency
```

### Network Issues (Remote Data)

```
1. Open Network tab in DevTools
2. Check API call to /api/endpoint
3. Verify response status (200 OK)
4. Check response data format (should be array)
5. Look for CORS errors if cross-origin
```

---

## Quick Troubleshooting Checklist

- [ ] Component imported correctly
- [ ] CSS files imported
- [ ] `dataSource` contains data
- [ ] Field names match data structure
- [ ] `change` handler updates state (if controlled)
- [ ] No JavaScript errors in console
- [ ] Performance tested (virtual scrolling enabled?)
- [ ] Network requests succeeding (if remote data)
- [ ] Styles applying correctly

---

## Getting Help

**Syncfusion Resources:**
- 📖 [Official Documentation](https://ej2.syncfusion.com/react/documentation/combo-box/getting-started/)
- 🐛 [Report Issues](https://www.syncfusion.com/support)
- 💬 [Community Forum](https://www.syncfusion.com/forums)
- 📧 [Contact Support](https://www.syncfusion.com/support/directtrac)

**When Reporting Issues:**
- Include minimal reproducible example (CodeSandbox, StackBlitz)
- Browser & OS information
- Error messages from console
- Steps to reproduce
- Expected vs actual behavior

---

## Next Steps

- **Still stuck?** → Check [advanced-features.md](advanced-features.md)
- **Performance issues?** → See virtual scrolling section above
- **Styling problems?** → Read [styling-and-theming.md](styling-and-theming.md)
