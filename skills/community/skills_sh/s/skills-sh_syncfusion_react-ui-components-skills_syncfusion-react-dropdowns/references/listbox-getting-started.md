# Getting Started with React ListBox

## Table of Contents
- [React Application Setup](#react-application-setup)
- [Installing Syncfusion Packages](#installing-syncfusion-packages)
- [Adding CSS References](#adding-css-references)
- [Creating Your First ListBox](#creating-your-first-listbox)
- [Running the Application](#running-the-application)
- [Troubleshooting](#troubleshooting)

---

## React Application Setup

### Using Vite (Recommended for Faster Development)

Vite provides a faster development environment with smaller bundle sizes compared to Create React App.

**Create a new React application with Vite:**

```bash
npm create vite@latest my-listbox-app -- --template react
cd my-listbox-app
npm install
```

**For TypeScript support:**

```bash
npm create vite@latest my-listbox-app -- --template react-ts
cd my-listbox-app
npm install
```

### Using Create React App (Alternative)

If you prefer Create React App:

```bash
npx create-react-app my-listbox-app
cd my-listbox-app
```

---

## Installing Syncfusion Packages

The ListBox component is part of the Syncfusion dropdowns package. Install it using npm:

```bash
npm install @syncfusion/ej2-react-dropdowns --save
```

The `--save` flag includes the package in your `package.json` dependencies.

**What gets installed:**
- ListBox component
- Related dropdown components (ComboBox, DropdownList, AutoComplete)
- Built-in styling system

---

## Adding CSS References

Syncfusion provides multiple theme options. Add CSS imports to your main app file or global CSS.

### Adding CSS to App.tsx (or App.jsx)

Import the required stylesheets at the top of your `src/App.tsx`:

```tsx
// Import Syncfusion CSS themes
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-react-inputs/styles/tailwind3.css';
import '@syncfusion/ej2-react-dropdowns/styles/tailwind3.css';

import App from './App';
```

### Or Add to App.css

Add these imports to your `src/App.css` file:

```css
@import '../node_modules/@syncfusion/ej2-base/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-react-inputs/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-react-dropdowns/styles/tailwind3.css';
```

Then import the CSS in your App component:

```tsx
import './App.css';
```

### Available Themes

Syncfusion provides multiple built-in themes:
- `tailwind3.css` (Tailwind - recommended)
- `material.css` (Material Design)
- `bootstrap5.css` (Bootstrap 5)
- `fluent.css` (Microsoft Fluent)
- `fabric.css` (Office Fabric)

---

## Creating Your First ListBox

### Basic ListBox with Static Data

Create a simple ListBox component in `src/App.tsx`:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import './App.css';

function App() {
  // Define list items
  const data = [
    { text: 'JavaScript', id: '1' },
    { text: 'TypeScript', id: '2' },
    { text: 'React', id: '3' },
    { text: 'Vue', id: '4' },
    { text: 'Angular', id: '5' },
    { text: 'Svelte', id: '6' }
  ];

  return (
    <div className="app-container">
      <h1>Programming Languages</h1>
      <ListBoxComponent 
        dataSource={data}
        fields={{ text: 'text', value: 'id' }}
      />
    </div>
  );
}

export default App;
```

### ListBox with Selection Handler

Add event handling to capture selected items:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import './App.css';

function App() {
  const data = [
    { text: 'JavaScript', id: '1' },
    { text: 'TypeScript', id: '2' },
    { text: 'React', id: '3' },
    { text: 'Vue', id: '4' }
  ];

  const handleChange = (e) => {
    console.log('Selected Item Value:', e.value);
    console.log('Selected Item(s):', e.items);
  };

  return (
    <div>
      <h1>Select a Language</h1>
      <ListBoxComponent 
        dataSource={data}
        fields={{ text: 'text', value: 'id' }}
        change={handleChange}
      />
    </div>
  );
}

export default App;
```

### ListBox with Multiple Selection

Enable multiple item selection:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useState } from 'react';
import './App.css';

function App() {
  const [selected, setSelected] = useState([]);

  const data = [
    { text: 'HTML', id: '1' },
    { text: 'CSS', id: '2' },
    { text: 'JavaScript', id: '3' },
    { text: 'TypeScript', id: '4' },
    { text: 'React', id: '5' }
  ];

  const handleChange = (e) => {
    setSelected(e.value);
    console.log('Selected:', e.value);
  };

  return (
    <div>
      <h1>Select Skills (Multiple)</h1>
      <ListBoxComponent 
        dataSource={data}
        fields={{ text: 'text', value: 'id' }}
        selectionSettings={{ mode: 'Multiple' }}
        change={handleChange}
      />
      <p>Selected: {selected.join(', ')}</p>
    </div>
  );
}

export default App;
```

---

## Running the Application

### For Vite Projects

Start the development server:

```bash
npm run dev
```

Output:
```
  VITE v5.0.0  ready in 345 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

Open http://localhost:5173/ in your browser to see your ListBox.

### For Create React App Projects

Start the development server:

```bash
npm start
```

This opens http://localhost:3000/ automatically in your browser.

---

## Troubleshooting

### Issue: Styles not loading (components appear unstyled)

**Solution:** Ensure CSS imports are at the top of your App component or in App.css:
```tsx
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-react-dropdowns/styles/tailwind3.css';
```

### Issue: ListBox component not rendering

**Solution:** Verify the import path and package installation:
```bash
npm list @syncfusion/ej2-react-dropdowns
```

Ensure dataSource is defined and fields mapping is correct.

### Issue: Data not displaying

**Solution:** Check your data structure matches the fields mapping:
```tsx
// Data structure
const data = [
  { text: 'Item 1', id: '1' }  // Must have 'text' and 'id'
];

// Fields mapping
fields={{ text: 'text', value: 'id' }}  // Maps to data properties
```

### Issue: Styling conflicts with other libraries

**Solution:** Increase CSS specificity or use CSS modules:
```tsx
import styles from './App.module.css';

<div className={styles.container}>
  <ListBoxComponent {...props} />
</div>
```

---

## Next Steps

- **Selection:** Learn single/multiple selection modes in [selection.md](selection.md)
- **Data Binding:** Explore dynamic data and grouping in [data-binding.md](data-binding.md)
- **Templates:** Create custom item layouts in [icons-and-templates.md](icons-and-templates.md)
- **Features:** Implement filtering, drag-drop, and more in [features.md](features.md)
- **Styling:** Customize appearance in [style-and-appearance.md](style-and-appearance.md)
