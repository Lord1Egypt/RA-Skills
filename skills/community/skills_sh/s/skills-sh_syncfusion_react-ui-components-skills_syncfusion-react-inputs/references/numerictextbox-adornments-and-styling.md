# Adornments & Styling

This guide covers prefix/suffix text, CSS styling, appearance customization, and component states.

## Table of Contents
- [Overview](#overview)
- [Prefix & Suffix](#prefix--suffix)
- [CSS Customization](#css-customization)
- [Component States](#component-states)
- [Theme Customization](#theme-customization)
- [Styling Examples](#styling-examples)

## Overview

NumericTextBox provides multiple ways to customize appearance:

- **Prefix/Suffix:** Add text before or after the number (units, symbols)
- **CSS classes:** Apply custom styles via `className` prop
- **Inline styles:** Direct `style` prop for quick styling
- **States:** Visual feedback for disabled, readonly, focus
- **Themes:** Material3, Bootstrap5, Fabric, and more

## Prefix & Suffix

Note: The explicit `prefix` and `suffix` properties are not supported by `NumericTextBoxComponent` in this API. To add adornments or unit labels, use format patterns (for currency/percentage), or use `appendTemplate` / `prependTemplate` to provide custom DOM templates that render beside the input.

### Recommended alternatives
- Currency/percentage: use `format` (`c2`, `p2`, etc.) and `locale`/`currency` for proper symbols.
- Custom HTML: use `appendTemplate` / `prependTemplate` to render icons or text next to the input.

### Practical Example: Product Information (using templates and supported APIs)

```jsx
import React, { useState } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function ProductInfo() {
  const [weight, setWeight] = useState(2.5);
  const [price, setPrice] = useState(99.99);
  const [quantity, setQuantity] = useState(10);

  const weightSuffix = () => (<span className="e-input-group-text">kg</span>);

  return (
    <div style={{ padding: '20px', maxWidth: '400px' }}>
      <h3>Product Specification</h3>

      <div style={{ marginBottom: '15px' }}>
        <label>Weight:</label>
        <NumericTextBoxComponent
          value={weight}
          change={(e) => setWeight(e.value)}
          appendTemplate={weightSuffix}
          decimals={1}
        />
      </div>

      <div style={{ marginBottom: '15px' }}>
        <label>Price:</label>
        <NumericTextBoxComponent
          value={price}
          change={(e) => setPrice(e.value)}
          format="c2"
          currency="USD"
          min={0}
          decimals={2}
        />
      </div>

      <div style={{ marginBottom: '15px' }}>
        <label>In Stock:</label>
        <NumericTextBoxComponent
          value={quantity}
          change={(e) => setQuantity(e.value)}
          min={0}
          decimals={0}
        />
      </div>
    </div>
  );
}
```

## CSS Customization

### Inline Styles

Use the `style` prop for direct CSS:

```jsx
<NumericTextBoxComponent
  value={10}
  style={{
    width: '200px',
    fontSize: '16px',
    padding: '8px',
    borderRadius: '4px'
  }}
/>
```

### CSS Classes

Apply custom styles via `className`:

```jsx
<NumericTextBoxComponent
  value={10}
  className="custom-input"
/>
```

Then define CSS:

```css
.custom-input {
  width: 200px;
  font-size: 16px;
  padding: 8px;
  border-radius: 4px;
  border: 2px solid #0066cc;
}
```

### Width Customization

```jsx
// Fixed width
<NumericTextBoxComponent value={10} style={{ width: '150px' }} />

// Full width
<NumericTextBoxComponent value={10} style={{ width: '100%' }} />

// Using className
<NumericTextBoxComponent 
  value={10} 
  className="full-width"
/>
```

```css
.full-width {
  width: 100%;
  box-sizing: border-box;
}
```

### Font and Text Styling

```jsx
<NumericTextBoxComponent
  value={10}
  style={{
    fontSize: '18px',
    fontWeight: 'bold',
    color: '#333',
    textAlign: 'right'
  }}
/>
```

### Border and Background

```jsx
<NumericTextBoxComponent
  value={10}
  style={{
    border: '2px solid #ccc',
    borderRadius: '8px',
    backgroundColor: '#f9f9f9',
    padding: '10px'
  }}
/>
```

## Component States

### Disabled State

Disable user interaction:

```jsx
<NumericTextBoxComponent
  value={10}
  disabled={true}
  // Input is grayed out, not clickable
/>
```

**Styling disabled state:**

```jsx
<NumericTextBoxComponent
  value={10}
  disabled={true}
  style={{
    backgroundColor: '#f0f0f0',
    color: '#ccc',
    opacity: '0.6'
  }}
/>
```

### Readonly State

Allow reading but prevent editing:

```jsx
<NumericTextBoxComponent
  value={10}
  readonly={true}
  // Can see value, but can't edit
/>
```

### Placeholder

Show hint text when empty:

```jsx
<NumericTextBoxComponent
  value={null}
  placeholder="Enter amount"
  // Displays: Enter amount (in gray)
/>
```

### Focus State

Style based on focus:

```jsx
import React, { useState } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function FocusExample() {
  const [focused, setFocused] = useState(false);
  const [value, setValue] = useState(10);

  return (
    <div>
      <NumericTextBoxComponent
        value={value}
        onChange={(e) => setValue(e.value)}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        style={{
          borderColor: focused ? '#0066cc' : '#ccc',
          borderWidth: '2px',
          boxShadow: focused ? '0 0 8px rgba(0, 102, 204, 0.3)' : 'none',
          transition: 'all 0.3s'
        }}
      />
      <p>{focused ? 'Input focused' : 'Input not focused'}</p>
    </div>
  );
}
```

## Theme Customization

### Available Themes

NumericTextBox includes several built-in themes:

```jsx
// Import one theme
import '@syncfusion/ej2-base/styles/material3.css';
import '@syncfusion/ej2-inputs/styles/material3.css';

// Available themes:
// - material3 (modern, rounded)
// - material (classic Material Design)
// - bootstrap5 (Bootstrap 5 style)
// - bootstrap4 (Bootstrap 4 style)
// - fabric (Microsoft Fabric style)
// - highcontrast (accessibility focused)
```

### Switching Themes

To switch themes, change the CSS import:

```jsx
// Current
import '@syncfusion/ej2-inputs/styles/material3.css';

// Change to
import '@syncfusion/ej2-inputs/styles/bootstrap5.css';
```

### Custom Theme Variables

Override theme variables with CSS:

```css
:root {
  --primary-color: #0066cc;
  --focus-color: #004499;
  --border-color: #ddd;
}

.e-numerictextbox input {
  border-color: var(--border-color);
}

.e-numerictextbox input:focus {
  border-color: var(--focus-color);
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
}
```

## Styling Examples

### Example 1: Form Input with Label

```jsx
import React, { useState } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function FormInput() {
  const [price, setPrice] = useState(99.99);

  return (
    <div style={{ maxWidth: '400px' }}>
      <div style={{ marginBottom: '15px' }}>
        <label style={{
          display: 'block',
          marginBottom: '5px',
          fontWeight: 'bold',
          color: '#333'
        }}>
          Product Price
        </label>
        
        <NumericTextBoxComponent
          value={price}
          onChange={(e) => setPrice(e.value)}
          format="c2"
          min={0}
          placeholder="Enter price"
          style={{
            width: '100%',
            padding: '10px',
            fontSize: '16px',
            borderRadius: '4px',
            border: '1px solid #ddd'
          }}
        />
        
        <p style={{
          marginTop: '5px',
          fontSize: '12px',
          color: '#666'
        }}>
          Enter the product price in USD
        </p>
      </div>
    </div>
  );
}
```

### Example 2: Card-Based Input

```jsx
import React, { useState } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function CardInput() {
  const [value, setValue] = useState(50);

  return (
    <div style={{
      padding: '20px',
      border: '1px solid #e0e0e0',
      borderRadius: '8px',
      backgroundColor: '#fafafa',
      boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)'
    }}>
      <h3 style={{ marginTop: 0, marginBottom: '15px' }}>
        Enter Amount
      </h3>

      <NumericTextBoxComponent
        value={value}
        onChange={(e) => setValue(e.value)}
        prefix="$"
        min={0}
        max={1000}
        decimals={2}
        style={{
          width: '100%',
          padding: '12px',
          fontSize: '18px',
          borderRadius: '6px',
          border: '2px solid #e0e0e0'
        }}
      />

      <div style={{
        marginTop: '15px',
        padding: '10px',
        backgroundColor: '#e3f2fd',
        borderRadius: '4px',
        color: '#1976d2'
      }}>
        <strong>Amount:</strong> ${value.toFixed(2)}
      </div>
    </div>
  );
}
```

### Example 3: Inline Input with Icon

```jsx
import React, { useState } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function InlineInput() {
  const [weight, setWeight] = useState(75);

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
      <span style={{ fontSize: '24px' }}>⚖️</span>
      
      <NumericTextBoxComponent
        value={weight}
        onChange={(e) => setWeight(e.value)}
        suffix=" kg"
        min={0}
        max={500}
        decimals={1}
        style={{
          padding: '8px',
          fontSize: '16px',
          borderRadius: '4px',
          border: '1px solid #ddd'
        }}
      />

      <span style={{ color: '#666', fontSize: '14px' }}>
        {weight > 100 ? 'Heavy' : weight > 50 ? 'Medium' : 'Light'}
      </span>
    </div>
  );
}
```

### Example 4: Responsive Design

```jsx
import React, { useState } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function ResponsiveInput() {
  const [value, setValue] = useState(10);

  return (
    <div style={{
      maxWidth: '600px',
      margin: '0 auto',
      padding: '20px'
    }}>
      <style>{`
        @media (max-width: 600px) {
          .responsive-input {
            width: 100%;
          }
        }
        
        @media (min-width: 601px) {
          .responsive-input {
            width: 50%;
          }
        }
      `}</style>

      <label style={{ display: 'block', marginBottom: '8px' }}>
        <strong>Quantity</strong>
      </label>

      <NumericTextBoxComponent
        value={value}
        onChange={(e) => setValue(e.value)}
        className="responsive-input"
        min={1}
        max={100}
        decimals={0}
      />
    </div>
  );
}
```

## Next Steps

- **Formats:** See [formats-and-validation.md](formats-and-validation.md) for prefix/suffix with formats
- **Spin Buttons:** See [spin-buttons-and-step.md](spin-buttons-and-step.md) for interactive controls
- **Accessibility:** See [globalization-accessibility.md](globalization-accessibility.md) for accessible styling
- **How-To:** See [how-to-guide.md](how-to-guide.md) for customization recipes
