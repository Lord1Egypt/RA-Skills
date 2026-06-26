# Styling & Theming

## Table of Contents
- [Built-in Themes](#built-in-themes)
- [Theme Customization](#theme-customization)
- [CSS Variables](#css-variables)
- [Responsive Design](#responsive-design)
- [Dark Mode](#dark-mode)
- [Theme Studio](#theme-studio)

---

## Built-in Themes

Syncfusion ComboBox comes with several professional themes. Choose one based on your design system.

### Available Themes

| Theme | CSS File | Best For |
|-------|----------|----------|
| **Tailwind** | `tailwind3.css` | Modern, utility-first design |
| **Bootstrap** | `bootstrap5.css` | Bootstrap projects |
| **Fluent** | `fluent.css` | Microsoft Office-like UI |
| **Fabric** | `fabric.css` | Microsoft Fabric Design System |
| **Material** | `material.css` | Google Material Design |
| **Highcontrast** | `highcontrast.css` | Accessibility, high contrast |

### Apply a Theme

```tsx
import { ComboBoxComponent } from '@syncfusion/ej2-react-dropdowns';

// Import ONE theme (in App.css or App.tsx)
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-react-inputs/styles/tailwind3.css';
import '@syncfusion/ej2-react-dropdowns/styles/tailwind3.css';

export default function App() {
  const items = ['Option 1', 'Option 2', 'Option 3'];

  return (
    <ComboBoxComponent 
      id="combo"
      dataSource={items}
      placeholder="Select an option"
    />
  );
}
```

**CSS Import Location:** `App.css` (or any global stylesheet)

### Switch Themes Dynamically

```tsx
import { useState } from 'react';
import { ComboBoxComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const [theme, setTheme] = useState('tailwind');

  const applyTheme = (newTheme) => {
    setTheme(newTheme);
    document.body.className = `e-${newTheme}`;  // Apply to body
  };

  return (
    <div>
      <div className="theme-selector">
        <button onClick={() => applyTheme('tailwind')}>Tailwind</button>
        <button onClick={() => applyTheme('bootstrap')}>Bootstrap</button>
        <button onClick={() => applyTheme('fluent')}>Fluent</button>
      </div>
      
      <ComboBoxComponent 
        id="combo"
        dataSource={items}
      />
    </div>
  );
}
```

---

## Theme Customization

### Override Theme Variables

Most themes use CSS custom properties (variables) that you can override:

```css
/* In your global CSS file (after Syncfusion imports) */

:root {
  /* Syncfusion theme variables */
  --sf-primary-color: #0066cc;           /* Primary brand color */
  --sf-border-color: #ddd;               /* Border colors */
  --sf-background-color: #ffffff;        /* Background */
  --sf-text-color: #333;                 /* Text color */
  --sf-hover-background: #f5f5f5;        /* Hover state */
}

/* For Tailwind theme specifically */
.e-tailwind {
  --sf-primary: #0066cc;
}

/* For Bootstrap theme specifically */
.e-bootstrap .e-combobox .e-input {
  border: 1px solid var(--sf-border-color);
}
```

### Custom Color Scheme

```css
/* Brand-specific customization */
:root {
  --combo-primary: #007bff;              /* Your brand blue */
  --combo-success: #28a745;              /* Success green */
  --combo-danger: #dc3545;               /* Error red */
  --combo-warning: #ffc107;              /* Warning yellow */
  --combo-border-radius: 8px;            /* Rounded corners */
}

/* Apply custom colors */
.e-combobox .e-input {
  border: 2px solid var(--combo-primary);
  border-radius: var(--combo-border-radius);
}

.e-combobox .e-list-item.e-active {
  background-color: var(--combo-primary);
}

.e-combobox .e-list-item:hover {
  background-color: rgba(0, 123, 255, 0.1);
}
```

---

## CSS Variables

### Common Syncfusion Variables

```css
/* These variables work across all Syncfusion components */

:root {
  /* Colors */
  --sf-primary: #0066cc;
  --sf-accent: #ff6b6b;
  --sf-success: #51cf66;
  --sf-warning: #ffd93d;
  --sf-danger: #ff6b6b;
  
  /* Sizing */
  --sf-font-size: 14px;
  --sf-line-height: 1.5;
  --sf-border-radius: 4px;
  
  /* Spacing */
  --sf-padding: 8px;
  --sf-margin: 16px;
  
  /* Transitions */
  --sf-transition-duration: 200ms;
}

/* Apply to ComboBox */
.e-combobox .e-input {
  font-size: var(--sf-font-size);
  border-radius: var(--sf-border-radius);
  padding: var(--sf-padding);
}

.e-combobox .e-list-item.e-active {
  background-color: var(--sf-primary);
  transition: background-color var(--sf-transition-duration);
}
```

---

## Responsive Design

### Mobile-Friendly Styling

```css
/* Desktop (default) */
.e-combobox {
  width: 300px;
  font-size: 14px;
}

/* Tablet */
@media (max-width: 768px) {
  .e-combobox {
    width: 100%;
    font-size: 16px;  /* Prevents zoom on iOS */
  }
  
  .e-combobox .e-dropdown-popup {
    max-height: 200px;  /* Less vertical space on mobile */
  }
}

/* Mobile */
@media (max-width: 480px) {
  .e-combobox {
    width: 100%;
  }
  
  .e-combobox .e-dropdown-popup {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    border-radius: 12px 12px 0 0;
    max-height: 60vh;
  }
}
```

### Responsive ComboBox Implementation

```tsx
export default function App() {
  return (
    <div className="combo-container">
      <ComboBoxComponent 
        id="responsive-combo"
        dataSource={items}
        popupWidth="100%"             // Fill container width
        placeholder="Select..."
      />
    </div>
  );
}
```

**CSS:**
```css
.combo-container {
  width: 100%;
  max-width: 500px;  /* Max width on large screens */
}
```

---

## Dark Mode

### Implement Dark Mode Toggle

```tsx
import { useState } from 'react';
import { ComboBoxComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const [isDarkMode, setIsDarkMode] = useState(false);

  const toggleDarkMode = () => {
    const newMode = !isDarkMode;
    setIsDarkMode(newMode);
    
    if (newMode) {
      document.documentElement.classList.add('dark-mode');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark-mode');
      localStorage.setItem('theme', 'light');
    }
  };

  return (
    <div>
      <button onClick={toggleDarkMode}>
        {isDarkMode ? '☀️ Light' : '🌙 Dark'}
      </button>
      
      <ComboBoxComponent 
        id="combo"
        dataSource={items}
      />
    </div>
  );
}
```

### Dark Mode CSS

```css
/* Light mode (default) */
:root {
  --bg-color: #ffffff;
  --text-color: #333;
  --border-color: #ddd;
  --hover-bg: #f5f5f5;
}

/* Dark mode */
:root.dark-mode {
  --bg-color: #1e1e1e;
  --text-color: #f0f0f0;
  --border-color: #444;
  --hover-bg: #333;
}

/* Apply to ComboBox */
.e-combobox .e-input {
  background-color: var(--bg-color);
  color: var(--text-color);
  border-color: var(--border-color);
}

.e-combobox .e-list-item:hover {
  background-color: var(--hover-bg);
}

.e-combobox .e-list-item {
  color: var(--text-color);
}
```

---

## Theme Studio

### Customize Themes with Theme Studio

Syncfusion Theme Studio is a web-based tool for creating custom themes without coding:

1. **Visit:** [Syncfusion Theme Studio](https://ej2.syncfusion.com/themestudio)
2. **Select:** Dropdown component
3. **Customize:** Colors, fonts, spacing
4. **Download:** Custom CSS file

### Use Custom Theme

```tsx
import { ComboBoxComponent } from '@syncfusion/ej2-react-dropdowns';

// Import custom theme from Theme Studio
import './my-custom-theme.css';

export default function App() {
  return (
    <ComboBoxComponent 
      id="combo"
      dataSource={items}
    />
  );
}
```

---

## Advanced Styling Examples

### Example 1: Gradient Border Effect

```css
.e-combobox .e-input {
  border: 2px solid;
  border-image: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-image-slice: 1;
  padding: 10px;
}

.e-combobox .e-input:focus {
  box-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
}
```

### Example 2: Glass Morphism Effect

```css
.e-combobox .e-dropdown-popup {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
}

.e-combobox .e-list-item:hover {
  background: rgba(0, 0, 0, 0.1);
}
```

### Example 3: Animated Underline

```css
.e-combobox .e-input {
  border: none;
  border-bottom: 2px solid #ddd;
  transition: border-color 200ms ease;
}

.e-combobox .e-input:focus {
  border-bottom-color: #0066cc;
  box-shadow: 0 2px 4px rgba(0, 102, 204, 0.3);
}
```

### Example 4: Custom Dropdown Icon

```css
.e-combobox .e-dropdown-icon::before {
  content: '▼';
  font-size: 12px;
}

/* Rotate on open */
.e-combobox.e-popup-open .e-dropdown-icon::before {
  transform: rotate(180deg);
  transition: transform 200ms;
}
```

---

## Styling Checklist

- [ ] Theme CSS imported in App.css
- [ ] Custom colors defined with CSS variables
- [ ] Mobile responsive tested (@media queries)
- [ ] Dark mode toggle functional
- [ ] Color contrast meets WCAG standards (4.5:1)
- [ ] Hover/focus states visible
- [ ] Styling doesn't break functionality
- [ ] All states tested (default, hover, focus, disabled, open)

---

## Next Steps

- **Having rendering issues?** → Check [troubleshooting.md](troubleshooting.md)
- **Want rich item display?** → See [templates-and-customization.md](templates-and-customization.md)
- **Global theme setup?** → Read [getting-started.md](getting-started.md)
