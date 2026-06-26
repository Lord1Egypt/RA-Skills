# SplitButton Customization

## Table of Contents
- [Custom CSS Styling](#custom-css-styling)
- [Theming](#theming)
- [Custom Templates](#custom-templates)
- [Responsive Design](#responsive-design)
- [Animations and Transitions](#animations-and-transitions)
- [Advanced Customization](#advanced-customization)
- [Best Practices](#best-practices)

## Custom CSS Styling

### Inline Styles

Apply styles directly to the component.

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function InlineStyles() {
  const items = [{ text: 'Option 1' }, { text: 'Option 2' }];

  return (
    <SplitButtonComponent
      items={items}
      style={{
        backgroundColor: '#ff6b6b',
        color: 'white',
        borderRadius: '8px',
        padding: '10px 20px',
        fontSize: '16px'
      }}
    >
      Custom Styled
    </SplitButtonComponent>
  );
}

export default InlineStyles;
```

### CSS Classes

Define custom CSS classes and apply them via `cssClass`.

```tsx
// styles.css
.custom-splitbutton {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  border-radius: 8px;
  font-weight: 600;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  transition: transform 0.2s ease;
}

.custom-splitbutton:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.custom-splitbutton-item {
  padding: 12px 16px;
  border-bottom: 1px solid #eee;
}

.custom-splitbutton-item:last-child {
  border-bottom: none;
}
```

```tsx
// Component.tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import './styles.css';

function CustomStyled() {
  const items = [
    { text: 'Option 1' },
    { text: 'Option 2' },
    { text: 'Option 3' }
  ];

  return (
    <SplitButtonComponent
      items={items}
      cssClass="custom-splitbutton"
    >
      Custom Styled
    </SplitButtonComponent>
  );
}

export default CustomStyled;
```

### CSS Modules

Use CSS modules for scoped styling.

```tsx
// styles.module.css
.button {
  background: #007bff;
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
  font-weight: 500;
}

.button:hover {
  background: #0056b3;
}

.dropdown {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
```

```tsx
// Component.tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import styles from './styles.module.css';

function CssModulesExample() {
  const items = [{ text: 'Option 1' }, { text: 'Option 2' }];

  return (
    <SplitButtonComponent
      items={items}
      cssClass={styles.button}
    >
      Styled
    </SplitButtonComponent>
  );
}

export default CssModulesExample;
```

## Theming

### Built-in Themes

Import and use Syncfusion built-in themes.

```tsx
// Material3 theme (default, recommended)
import '@syncfusion/ej2-react-splitbuttons/styles/material3.css';

// Bootstrap 5 theme
import '@syncfusion/ej2-react-splitbuttons/styles/bootstrap5.css';

// Fluent theme
import '@syncfusion/ej2-react-splitbuttons/styles/fluent.css';

// Tailwind theme
import '@syncfusion/ej2-react-splitbuttons/styles/tailwind.css';

// Fabric theme
import '@syncfusion/ej2-react-splitbuttons/styles/fabric.css';
```

### Theme Variables (CSS Custom Properties)

Override theme variables using CSS custom properties.

```css
/* Override theme colors */
:root {
  /* Primary color */
  --primary-color: #007bff;
  
  /* Button background */
  --button-bg: #f5f5f5;
  
  /* Button text color */
  --button-text: #333;
  
  /* Hover background */
  --button-hover-bg: #e9e9e9;
  
  /* Border color */
  --button-border: #ddd;
  
  /* Disabled opacity */
  --disabled-opacity: 0.6;
}
```

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import '@syncfusion/ej2-react-splitbuttons/styles/material3.css';
import './theme-variables.css';

function ThemedButton() {
  const items = [{ text: 'Option 1' }, { text: 'Option 2' }];

  return (
    <SplitButtonComponent
      items={items}
      cssClass="e-primary"
    >
      Themed
    </SplitButtonComponent>
  );
}

export default ThemedButton;
```

### Dark Mode

Implement dark mode styling.

```css
/* Light mode (default) */
:root {
  --bg-color: #ffffff;
  --text-color: #333333;
  --border-color: #dddddd;
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  :root {
    --bg-color: #1e1e1e;
    --text-color: #ffffff;
    --border-color: #444444;
  }
}

/* Or with class */
.dark-theme {
  --bg-color: #1e1e1e;
  --text-color: #ffffff;
  --border-color: #444444;
}
```

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import { useState, useEffect } from 'react';

function DarkModeButton() {
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    const root = document.documentElement;
    if (isDarkMode) {
      root.classList.add('dark-theme');
    } else {
      root.classList.remove('dark-theme');
    }
  }, [isDarkMode]);

  const items = [{ text: 'Option 1' }, { text: 'Option 2' }];

  return (
    <div>
      <label>
        <input
          type="checkbox"
          checked={isDarkMode}
          onChange={(e) => setIsDarkMode(e.target.checked)}
        />
        Dark Mode
      </label>
      <SplitButtonComponent
        items={items}
        cssClass="e-primary"
      >
        Button
      </SplitButtonComponent>
    </div>
  );
}

export default DarkModeButton;
```

## Custom Templates

### Item Template

Create custom item templates for dropdown menu.

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function CustomItemTemplate() {
  const items = [
    { text: 'Save', icon: '💾', color: '#4CAF50' },
    { text: 'Edit', icon: '✏️', color: '#2196F3' },
    { text: 'Delete', icon: '🗑️', color: '#f44336' }
  ];

  const itemTemplate = (props: any) => {
    return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        padding: '8px 12px',
        gap: '10px'
      }}>
        <span style={{ fontSize: '18px' }}>{props.icon}</span>
        <span style={{ flex: 1 }}>{props.text}</span>
        <span style={{
          backgroundColor: props.color,
          color: 'white',
          borderRadius: '12px',
          padding: '2px 8px',
          fontSize: '11px',
          fontWeight: 'bold'
        }}>
          Action
        </span>
      </div>
    );
  };

  return (
    <SplitButtonComponent
      items={items}
      itemTemplate={itemTemplate}
      cssClass="e-primary"
    >
      Actions
    </SplitButtonComponent>
  );
}

export default CustomItemTemplate;
```

### Image Template

Include images in dropdown items.

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function ImageTemplate() {
  const items = [
    { text: 'PNG', ext: 'png', image: '🖼️' },
    { text: 'JPG', ext: 'jpg', image: '🖼️' },
    { text: 'SVG', ext: 'svg', image: '🎨' },
    { text: 'PDF', ext: 'pdf', image: '📄' }
  ];

  const itemTemplate = (props: any) => {
    return (
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <span style={{ fontSize: '24px' }}>{props.image}</span>
        <div>
          <div style={{ fontWeight: 500 }}>{props.text}</div>
          <small style={{ color: '#999' }}>.{props.ext}</small>
        </div>
      </div>
    );
  };

  return (
    <SplitButtonComponent
      items={items}
      itemTemplate={itemTemplate}
      cssClass="e-primary"
      iconCss="e-icons e-download"
    >
      Export
    </SplitButtonComponent>
  );
}

export default ImageTemplate;
```

### Rich Content Template

Complex templates with multiple elements.

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function RichContentTemplate() {
  const items = [
    {
      text: 'New Document',
      desc: 'Create a blank document',
      icon: '📄',
      shortcut: 'Ctrl+N'
    },
    {
      text: 'Open File',
      desc: 'Open an existing document',
      icon: '📂',
      shortcut: 'Ctrl+O'
    },
    {
      text: 'Recent',
      desc: 'Access recently opened files',
      icon: '⏱️',
      shortcut: 'Ctrl+R'
    }
  ];

  const itemTemplate = (props: any) => {
    return (
      <div style={{
        padding: '10px',
        borderBottom: '1px solid #eee',
        cursor: 'pointer',
        transition: 'background 0.2s'
      }}>
        <div style={{ display: 'flex', alignItems: 'flex-start', gap: '12px' }}>
          <span style={{ fontSize: '24px' }}>{props.icon}</span>
          <div style={{ flex: 1 }}>
            <div style={{ fontWeight: 600, marginBottom: '4px' }}>
              {props.text}
            </div>
            <div style={{ fontSize: '12px', color: '#666', marginBottom: '4px' }}>
              {props.desc}
            </div>
            <div style={{ fontSize: '11px', color: '#999' }}>
              {props.shortcut}
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <SplitButtonComponent
      items={items}
      itemTemplate={itemTemplate}
      cssClass="e-primary"
      iconCss="e-icons e-menu"
    >
      File
    </SplitButtonComponent>
  );
}

export default RichContentTemplate;
```

## Responsive Design

### Mobile-Friendly SplitButton

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import { useEffect, useState } from 'react';

function ResponsiveSplitButton() {
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const items = [
    { text: 'Save', iconCss: 'e-icons e-save' },
    { text: 'Save As', iconCss: 'e-icons e-save-as' },
    { text: 'Share', iconCss: 'e-icons e-share' }
  ];

  return (
    <SplitButtonComponent
      items={items}
      cssClass={isMobile ? 'e-small' : 'e-primary'}
      iconPosition={isMobile ? 'Left' : 'Left'}
    >
      {isMobile ? '⋯' : 'Save'}
    </SplitButtonComponent>
  );
}

export default ResponsiveSplitButton;
```

### CSS Media Queries

```css
/* Desktop styles */
.split-button {
  padding: 10px 20px;
  font-size: 14px;
}

/* Tablet styles */
@media (max-width: 768px) {
  .split-button {
    padding: 8px 16px;
    font-size: 13px;
  }
}

/* Mobile styles */
@media (max-width: 480px) {
  .split-button {
    padding: 6px 12px;
    font-size: 12px;
    width: 100%;
  }
}
```

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import './responsive.css';

function ResponsiveWithCSS() {
  const items = [
    { text: 'Option 1' },
    { text: 'Option 2' },
    { text: 'Option 3' }
  ];

  return (
    <SplitButtonComponent
      items={items}
      cssClass="split-button e-primary"
    >
      Menu
    </SplitButtonComponent>
  );
}

export default ResponsiveWithCSS;
```

## Animations and Transitions

### Fade Animation

```css
.split-button-popup.fade-in {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
```

### Scale Animation

```css
.split-button-popup.scale-in {
  animation: scaleIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
```

### Slide Animation

```css
.split-button-popup.slide-down {
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### Ripple Effect

```css
.split-button::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  transform: translate(-50%, -50%);
  animation: ripple 0.6s ease-out;
}

@keyframes ripple {
  to {
    width: 300px;
    height: 300px;
    opacity: 0;
  }
}
```

## Advanced Customization

### Custom Dropdown Width

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import { useRef } from 'react';

function CustomDropdownWidth() {
  const splitBtnRef = useRef<SplitButtonComponent>(null);

  const handleOpen = (args: any) => {
    const popup = args.element?.querySelector('.e-dropdown-popup');
    if (popup) {
      popup.style.minWidth = '300px';
    }
  };

  const items = [
    { text: 'This is a longer option text that needs more space' },
    { text: 'Another option' }
  ];

  return (
    <SplitButtonComponent
      ref={splitBtnRef}
      items={items}
      open={handleOpen}
      cssClass="e-primary"
    >
      Custom Width
    </SplitButtonComponent>
  );
}

export default CustomDropdownWidth;
```

### Custom Positioning

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import { useRef } from 'react';

function CustomPositioning() {
  const splitBtnRef = useRef<SplitButtonComponent>(null);

  const handleBeforeOpen = (args: any) => {
    const popup = args.element?.querySelector('.e-dropdown-popup');
    if (popup) {
      // Custom positioning logic
      popup.style.position = 'fixed';
      popup.style.top = 'auto';
      popup.style.bottom = '60px';
    }
  };

  const items = [{ text: 'Option 1' }, { text: 'Option 2' }];

  return (
    <SplitButtonComponent
      ref={splitBtnRef}
      items={items}
      beforeOpen={handleBeforeOpen}
      cssClass="e-primary"
    >
      Custom Position
    </SplitButtonComponent>
  );
}

export default CustomPositioning;
```

### Theming with Styled Components

```tsx
import styled from 'styled-components';
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

const StyledSplitButton = styled(SplitButtonComponent)`
  && {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    color: white;
    border-radius: 8px;
    
    &:hover {
      box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    &:active {
      transform: scale(0.98);
    }
  }
`;

function StyledComponentsExample() {
  const items = [{ text: 'Option 1' }, { text: 'Option 2' }];

  return (
    <StyledSplitButton items={items}>
      Styled with Styled Components
    </StyledSplitButton>
  );
}

export default StyledComponentsExample;
```

## Best Practices

### Performance Optimization

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import { useMemo, useCallback } from 'react';

function OptimizedSplitButton() {
  // Memoize items to prevent unnecessary re-renders
  const items = useMemo(() => [
    { text: 'Option 1' },
    { text: 'Option 2' }
  ], []);

  // Use useCallback for event handlers
  const handleSelect = useCallback((args: any) => {
    console.log('Selected:', args.item.text);
  }, []);

  return (
    <SplitButtonComponent
      items={items}
      select={handleSelect}
      cssClass="e-primary"
    >
      Optimized
    </SplitButtonComponent>
  );
}

export default OptimizedSplitButton;
```

### Accessibility Considerations

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function AccessibleCustomization() {
  const items = [
    { text: 'Save', title: 'Save current document (Ctrl+S)' },
    { text: 'Save As', title: 'Save with new name (Ctrl+Shift+S)' }
  ];

  return (
    <SplitButtonComponent
      items={items}
      cssClass="e-primary"
      title="File actions"
      role="button"
      aria-label="File menu with save options"
      aria-haspopup="menu"
    >
      File
    </SplitButtonComponent>
  );
}

export default AccessibleCustomization;
```

### Consistent Styling Strategy

```tsx
// Define a theme constant
const buttonTheme = {
  primary: 'e-primary',
  success: 'e-success',
  danger: 'e-danger'
};

const buttonSizes = {
  small: 'e-small',
  normal: '',
  large: 'e-large'
};

// Use in components
function ThemedButton({ variant = 'primary', size = 'normal' }) {
  const items = [{ text: 'Option 1' }, { text: 'Option 2' }];

  return (
    <SplitButtonComponent
      items={items}
      cssClass={`${buttonTheme[variant]} ${buttonSizes[size]}`}
    >
      Button
    </SplitButtonComponent>
  );
}

export default ThemedButton;
```

## Next Steps

- **Features** → Read [splitbutton-features.md](splitbutton-features.md) for more examples
- **API Reference** → Read [api-reference.md](api-reference.md) for complete documentation
- **Accessibility** → Read [accessibility.md](accessibility.md) for WCAG compliance
