# Styling and Appearance in React ListBox

## Table of Contents
- [Built-in Themes](#built-in-themes)
- [CSS Customization](#css-customization)
- [Styling Items](#styling-items)
- [Responsive Design](#responsive-design)
- [CSS Variables](#css-variables)
- [Advanced Styling](#advanced-styling)
- [Troubleshooting](#troubleshooting)

---

## Built-in Themes

Syncfusion provides multiple pre-built themes. Import the theme CSS in your App.tsx:

### Tailwind 3 Theme (Recommended)

```tsx
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-react-inputs/styles/tailwind3.css';
import '@syncfusion/ej2-react-dropdowns/styles/tailwind3.css';
```

### Material Theme

```tsx
import '@syncfusion/ej2-base/styles/material.css';
import '@syncfusion/ej2-react-inputs/styles/material.css';
import '@syncfusion/ej2-react-dropdowns/styles/material.css';
```

### Bootstrap 5 Theme

```tsx
import '@syncfusion/ej2-base/styles/bootstrap5.css';
import '@syncfusion/ej2-react-inputs/styles/bootstrap5.css';
import '@syncfusion/ej2-react-dropdowns/styles/bootstrap5.css';
```

### Fluent (Microsoft) Theme

```tsx
import '@syncfusion/ej2-base/styles/fluent.css';
import '@syncfusion/ej2-react-inputs/styles/fluent.css';
import '@syncfusion/ej2-react-dropdowns/styles/fluent.css';
```

### Fabric (Office) Theme

```tsx
import '@syncfusion/ej2-base/styles/fabric.css';
import '@syncfusion/ej2-react-inputs/styles/fabric.css';
import '@syncfusion/ej2-react-dropdowns/styles/fabric.css';
```

---

## CSS Customization

### Override Component Styles

Use CSS to override Syncfusion default styles:

```css
/* Override ListBox container */
.e-listbox {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Override list items */
.e-listbox .e-list-item {
  padding: 12px 16px;
  font-size: 14px;
}

/* Override hover state */
.e-listbox .e-list-item:hover {
  background-color: #e3f2fd;
}

/* Override selected state */
.e-listbox .e-list-item.e-selected {
  background-color: #1976d2;
  color: white;
}
```

### Container Styling

```css
.e-listbox {
  border: 2px solid #ccc;
  border-radius: 6px;
  background-color: #f9f9f9;
}

.e-listbox:focus {
  border-color: #1976d2;
  box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.1);
}
```

### Item Styling

```css
/* Base item style */
.e-listbox .e-list-item {
  border-bottom: 1px solid #e0e0e0;
  transition: background-color 0.2s ease;
}

/* Hover state */
.e-listbox .e-list-item:hover {
  background-color: #f5f5f5;
}

/* Selected state */
.e-listbox .e-list-item.e-selected {
  background-color: #2196f3;
  color: white;
  font-weight: 500;
}

/* Focus state */
.e-listbox .e-list-item:focus {
  outline: 2px solid #2196f3;
  outline-offset: -2px;
}

/* Disabled state */
.e-listbox .e-list-item.e-disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

### Group Header Styling

```css
/* Group header */
.e-listbox .e-list-group-item {
  padding: 10px 16px;
  background-color: #e8e8e8;
  font-weight: 600;
  font-size: 12px;
  text-transform: uppercase;
  color: #424242;
}

/* Group header hover */
.e-listbox .e-list-group-item:hover {
  background-color: #d8d8d8;
}
```

---

## Styling Items

### Conditional Item Styling

Style items based on properties:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import './App.css';

function App() {
  const data = [
    { text: 'High Priority', id: '1', priority: 'high' },
    { text: 'Medium Priority', id: '2', priority: 'medium' },
    { text: 'Low Priority', id: '3', priority: 'low' }
  ];

  const itemTemplate = (props) => {
    return (
      <div className={`list-item priority-${props.priority}`}>
        {props.text}
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
.list-item {
  padding: 12px 16px;
  display: flex;
  align-items: center;
}

.list-item.priority-high {
  border-left: 4px solid #d32f2f;
  background-color: #ffebee;
}

.list-item.priority-medium {
  border-left: 4px solid #f57c00;
  background-color: #fff3e0;
}

.list-item.priority-low {
  border-left: 4px solid #388e3c;
  background-color: #f1f8e9;
}
```

### Custom Item Layout

```tsx
const itemTemplate = (props) => {
  return (
    <div style={{
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      padding: '12px 16px',
      borderBottom: '1px solid #eee'
    }}>
      <div>
        <div style={{ fontWeight: 'bold' }}>{props.text}</div>
        <div style={{ fontSize: '12px', color: '#999' }}>
          {props.subtitle}
        </div>
      </div>
      <span style={{
        backgroundColor: '#e3f2fd',
        color: '#1976d2',
        padding: '4px 8px',
        borderRadius: '4px',
        fontSize: '12px'
      }}>
        {props.tag}
      </span>
    </div>
  );
}
```

---

## Responsive Design

### Mobile-Friendly Sizing

Adapt ListBox for different screen sizes:

```css
/* Desktop */
.e-listbox {
  height: 300px;
  width: 400px;
}

/* Tablet */
@media (max-width: 768px) {
  .e-listbox {
    height: 250px;
    width: 100%;
  }
  
  .e-listbox .e-list-item {
    padding: 10px 12px;
    font-size: 13px;
  }
}

/* Mobile */
@media (max-width: 480px) {
  .e-listbox {
    height: 200px;
    width: 100%;
  }
  
  .e-listbox .e-list-item {
    padding: 8px 10px;
    font-size: 12px;
  }
}
```

### Fluid Width

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const data = [
    { text: 'Item 1', id: '1' },
    { text: 'Item 2', id: '2' }
  ];

  return (
    <div style={{ width: '100%', maxWidth: '500px' }}>
      <ListBoxComponent 
        dataSource={data}
        fields={{ text: 'text', value: 'id' }}
        style={{ width: '100%' }}
      />
    </div>
  );
}

export default App;
```

---

## CSS Variables

Override theme colors using CSS variables:

```css
/* Tailwind theme variables */
:root {
  --e-primary: #1976d2;
  --e-surface: #ffffff;
  --e-on-surface: #000000;
  --e-outline: #999999;
}

/* Override in component */
.custom-listbox {
  --e-primary: #d32f2f;
}
```

### Dark Mode

```css
/* Light mode (default) */
:root {
  --e-bg-color: #ffffff;
  --e-text-color: #000000;
  --e-border-color: #e0e0e0;
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  :root {
    --e-bg-color: #1e1e1e;
    --e-text-color: #ffffff;
    --e-border-color: #424242;
  }

  .e-listbox {
    background-color: var(--e-bg-color);
    color: var(--e-text-color);
    border-color: var(--e-border-color);
  }
}
```

---

## Advanced Styling

### Gradient Background

```css
.e-listbox {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.e-listbox .e-list-item {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 4px;
  margin: 4px 8px;
}
```

### Shadow and Elevation

```css
.e-listbox {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1),
              0 4px 8px rgba(0, 0, 0, 0.05);
  border-radius: 8px;
}

.e-listbox .e-list-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}
```

### Animation

```css
.e-listbox .e-list-item {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.e-listbox .e-list-item:hover {
  transform: translateX(4px);
  background-color: #f5f5f5;
}

.e-listbox .e-list-item.e-selected {
  animation: pulse 0.3s ease-out;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(25, 118, 210, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(25, 118, 210, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(25, 118, 210, 0);
  }
}
```

### Compact Size

```css
.e-listbox.compact {
  border-radius: 6px;
}

.e-listbox.compact .e-list-item {
  padding: 6px 10px;
  font-size: 13px;
}

.e-listbox.compact .e-list-group-item {
  padding: 6px 10px;
  font-size: 11px;
}
```

Usage:
```tsx
<div className="compact">
  <ListBoxComponent {...props} />
</div>
```

### Large Size

```css
.e-listbox.large {
  border-radius: 10px;
}

.e-listbox.large .e-list-item {
  padding: 16px 20px;
  font-size: 16px;
  line-height: 1.6;
}

.e-listbox.large .e-list-group-item {
  padding: 12px 20px;
  font-size: 14px;
}
```

---

## Troubleshooting

### Styles not applying
- Import CSS files before component render
- Check CSS specificity - Syncfusion styles are specific
- Use `!important` only as last resort
- Clear browser cache and rebuild

### Theme colors not changing
- Ensure theme CSS is imported once
- Don't import multiple themes
- Use CSS variables instead of inline styles
- Check CSS file path is correct

### Dark mode not working
- Verify `prefers-color-scheme: dark` media query
- Check browser/OS dark mode is enabled
- Use developer tools to test media query
- Ensure dark mode CSS is defined

### Responsive not triggering
- Verify media query breakpoints
- Test in actual mobile device, not just browser resize
- Check viewport meta tag: `<meta name="viewport" ... />`
- Use device emulation in browser DevTools

### Custom styles being overridden
- Use CSS modules to scope styles
- Increase specificity with parent class
- Place custom CSS after Syncfusion CSS imports
- Use CSS-in-JS library for component-scoped styles
