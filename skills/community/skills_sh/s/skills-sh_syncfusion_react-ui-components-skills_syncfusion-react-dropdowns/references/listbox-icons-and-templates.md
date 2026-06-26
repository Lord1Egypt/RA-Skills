# Icons and Templates in React ListBox

## Table of Contents
- [Adding Icons](#adding-icons)
- [Item Templates](#item-templates)
- [Template Syntax](#template-syntax)
- [Advanced Examples](#advanced-examples)
- [Troubleshooting](#troubleshooting)

---

## Adding Icons

### Emoji Icons in Text

Simple approach using emoji directly:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const data = [
    { text: '⚙️ JavaScript', id: '1' },
    { text: '📘 TypeScript', id: '2' },
    { text: '⚛️ React', id: '3' },
    { text: '💚 Vue', id: '4' }
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

### Icon Font Classes

Use icon font libraries like Font Awesome or Material Icons:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import './App.css';

function App() {
  const data = [
    { text: 'JavaScript', id: '1', icon: 'fa-js' },
    { text: 'React', id: '2', icon: 'fa-react' },
    { text: 'Vue', id: '3', icon: 'fa-vuejs' }
  ];

  return (
    <ListBoxComponent 
      dataSource={data}
      fields={{ 
        text: 'text', 
        value: 'id',
        iconCss: 'icon'
      }}
    />
  );
}

export default App;
```

**CSS for icon classes:**
```css
.fa-js::before { content: '⚙️'; margin-right: 8px; }
.fa-react::before { content: '⚛️'; margin-right: 8px; }
.fa-vuejs::before { content: '💚'; margin-right: 8px; }
```

---

## Item Templates

### Basic Item Template

Customize how each item displays:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const data = [
    { text: 'JavaScript', id: '1', level: 'Advanced' },
    { text: 'React', id: '2', level: 'Intermediate' },
    { text: 'Vue', id: '3', level: 'Beginner' }
  ];

  const itemTemplate = (props) => {
    return (
      <div style={{ padding: '8px' }}>
        <span>{props.text}</span>
        <span style={{ marginLeft: '10px', color: '#999' }}>
          ({props.level})
        </span>
      </div>
    );
  }

  return (
    <ListBoxComponent 
      dataSource={data}
      fields={{ text: 'text', value: 'id' }}
      itemTemplate={itemTemplate}
    />
  );
}

export default App;
```

### Template with Icon and Details

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const data = [
    { 
      text: 'JavaScript', 
      id: '1', 
      icon: '⚙️',
      description: 'Dynamic language for web'
    },
    { 
      text: 'React', 
      id: '2', 
      icon: '⚛️',
      description: 'UI library with components'
    }
  ];

  const itemTemplate = (props) => {
    return (
      <div style={{ display: 'flex', alignItems: 'center', padding: '8px' }}>
        <span style={{ fontSize: '20px', marginRight: '12px' }}>
          {props.icon}
        </span>
        <div>
          <div style={{ fontWeight: 'bold' }}>{props.text}</div>
          <div style={{ fontSize: '12px', color: '#666' }}>
            {props.description}
          </div>
        </div>
      </div>
    );
  }

  return (
    <ListBoxComponent 
      dataSource={data}
      fields={{ text: 'text', value: 'id' }}
      itemTemplate={itemTemplate}
    />
  );
}

export default App;
```

### Template with Badge

Add status badges to items:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import './App.css';

function App() {
  const data = [
    { text: 'JavaScript', id: '1', status: 'Stable' },
    { text: 'TypeScript', id: '2', status: 'Stable' },
    { text: 'React 19', id: '3', status: 'Beta' }
  ];

  const itemTemplate = (props) => {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '8px'
      }}>
        <span>{props.text}</span>
        <span className={`badge badge-${props.status.toLowerCase()}`}>
          {props.status}
        </span>
      </div>
    );
  }

  return (
    <ListBoxComponent 
      dataSource={data}
      fields={{ text: 'text', value: 'id' }}
      itemTemplate={itemTemplate}
    />
  );
}

export default App;
```

**CSS:**
```css
.badge {
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: bold;
}

.badge-stable {
  background-color: #d4edda;
  color: #155724;
}

.badge-beta {
  background-color: #fff3cd;
  color: #856404;
}
```

---

---

## Template Syntax

### Accessing Template Properties

Templates receive the item data as props:

```tsx
const itemTemplate = (props) => {
  return (
    <div>
      {/* Access any property from your data object */}
      <p>Text: {props.text}</p>
      <p>ID: {props.id}</p>
      <p>Custom Field: {props.customField}</p>
    </div>
  );
}
```

### Conditional Rendering in Template

```tsx
const itemTemplate = (props) => {
  return (
    <div style={{ padding: '8px' }}>
      {props.level === 'Advanced' && <span>⭐</span>}
      {props.text}
    </div>
  );
}
```

### Template with Inline Styles

```tsx
const itemTemplate = (props) => {
  return (
    <div style={{
      padding: '12px',
      borderBottom: '1px solid #eee',
      display: 'flex',
      justifyContent: 'space-between'
    }}>
      <span>{props.text}</span>
      <span style={{ color: '#999' }}>{props.description}</span>
    </div>
  );
}
```

### Template with CSS Classes

```tsx
import './App.css';

const itemTemplate = (props) => {
  return (
    <div className={`list-item ${props.status}`}>
      {props.text}
    </div>
  );
}

// CSS
// .list-item { padding: 8px; }
// .list-item.active { background-color: #e3f2fd; }
// .list-item.inactive { opacity: 0.6; }
```

---

## Advanced Examples

### Rich Media Template

Display images, icons, and multi-line content:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const data = [
    {
      id: '1',
      name: 'React',
      logo: '⚛️',
      version: '18.2',
      downloads: '18M/week'
    },
    {
      id: '2',
      name: 'Vue',
      logo: '💚',
      version: '3.3',
      downloads: '8M/week'
    }
  ];

  const itemTemplate = (props) => {
    return (
      <div style={{
        display: 'grid',
        gridTemplateColumns: '50px 1fr auto',
        gap: '12px',
        alignItems: 'center',
        padding: '12px',
        borderBottom: '1px solid #f0f0f0'
      }}>
        <div style={{ fontSize: '32px' }}>{props.logo}</div>
        <div>
          <div style={{ fontWeight: 'bold', fontSize: '14px' }}>
            {props.name}
          </div>
          <div style={{ fontSize: '12px', color: '#666' }}>
            v{props.version} • {props.downloads}
          </div>
        </div>
        <div style={{ textAlign: 'right', fontSize: '12px', color: '#999' }}>
          Popular
        </div>
      </div>
    );
  }

  return (
    <ListBoxComponent 
      dataSource={data}
      fields={{ text: 'name', value: 'id' }}
      itemTemplate={itemTemplate}
    />
  );
}

export default App;
```

### Checkbox Template

Custom template with checkbox-like appearance:

```tsx
const itemTemplate = (props) => {
  return (
    <div style={{ 
      display: 'flex', 
      alignItems: 'center',
      padding: '8px'
    }}>
      <input 
        type="checkbox" 
        style={{ marginRight: '8px', cursor: 'pointer' }}
      />
      <span>{props.text}</span>
    </div>
  );
}
```

### Search Highlight in Template

Highlight matching search text (if implementing custom filter):

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useState } from 'react';

function App() {
  const [searchText, setSearchText] = useState('');
  const data = [
    { text: 'JavaScript', id: '1' },
    { text: 'TypeScript', id: '2' }
  ];

  const itemTemplate = (props) => {
    const regex = new RegExp(`(${searchText})`, 'gi');
    const parts = props.text.split(regex);

    return (
      <div style={{ padding: '8px' }}>
        {parts.map((part, i) =>
          regex.test(part) ? (
            <mark key={i} style={{ backgroundColor: 'yellow' }}>
              {part}
            </mark>
          ) : (
            <span key={i}>{part}</span>
          )
        )}
      </div>
    );
  };

  return (
    <div>
      <input 
        value={searchText}
        onChange={(e) => setSearchText(e.target.value)}
        placeholder="Search..."
      />
      <ListBoxComponent 
        dataSource={data}
        fields={{ text: 'text', value: 'id' }}
        itemTemplate={itemTemplate}
      />
    </div>
  );
}

export default App;
```

---

## Troubleshooting

### Template not rendering
- Ensure template function returns valid JSX
- Check `itemTemplate` prop is passed correctly
- Verify data properties are accessible in template

### Icons not showing
- Check if icon class exists in CSS
- Verify iconCss field mapping: `fields={{ iconCss: 'icon' }}`
- Ensure icon property exists in all data items

### Template styling issues
- Inline styles take precedence
- Use `!important` if CSS class not overriding
- Check z-index for overlapping elements
