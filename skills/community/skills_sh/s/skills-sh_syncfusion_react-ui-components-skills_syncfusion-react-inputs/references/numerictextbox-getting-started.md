# Getting Started with NumericTextBox

This guide covers installation, setup, and creating your first NumericTextBox in a React application.

## Installation

### Step 1: Install the Package

Install the Syncfusion React Inputs package which includes NumericTextBox:

```bash
npm install @syncfusion/ej2-react-inputs
```

This installs:
- `@syncfusion/ej2-react-inputs` - React wrapper
- `@syncfusion/ej2-inputs` - Core component
- Dependencies: `@syncfusion/ej2-base`, `@syncfusion/ej2-buttons`, `@syncfusion/ej2-popups`

### Step 2: Add CSS Themes

Add the Material3 theme (or your preferred theme) to your `src/index.js` or main application file:

```jsx
// Import base theme first
import '@syncfusion/ej2-base/styles/material3.css';
import '@syncfusion/ej2-buttons/styles/material3.css';
import '@syncfusion/ej2-inputs/styles/material3.css';
import '@syncfusion/ej2-popups/styles/material3.css';
import '@syncfusion/ej2-angular-splitbuttons/styles/material3.css';
```

**Available themes:** `material3`, `material`, `bootstrap5`, `bootstrap4`, `fabric`, `highcontrast`

## Basic Implementation

### Minimal NumericTextBox

Here's the simplest working example:

```jsx
import React from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function App() {
  return (
    <div style={{ padding: '20px' }}>
      <NumericTextBoxComponent value={10} />
    </div>
  );
}
```

**What happens:**
- NumericTextBox renders with default value 10
- Spinner buttons appear by default
- Click up/down arrows to increment/decrement
- Type numbers directly into the field

### With State Management

To use NumericTextBox with React state:

```jsx
import React, { useState } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function App() {
  const [value, setValue] = useState(25);

  const handleChange = (e) => {
    setValue(e.value);
    console.log('New value:', e.value);
  };

  return (
    <div style={{ padding: '20px' }}>
      <h3>Enter a Number</h3>
      <NumericTextBoxComponent
        value={value}
        change={handleChange}
      />
      <p>Current value: {value}</p>
    </div>
  );
}
```

**Key points:**
- `value` prop sets initial value
- `onChange` event fires when value changes
- Event object has `value` property with new number
- Update React state to make component controlled

## Common Properties

### Essential Props

```jsx
<NumericTextBoxComponent
  value={10}              // Current numeric value
  min={0}                 // Minimum allowed value
  max={100}               // Maximum allowed value
  step={1}                // Increment step for spinner
  placeholder="Enter"     // Placeholder text
  decimals={2}            // Number of decimal places
  format="c2"             // Number format (c=currency, 2=decimals)
  strictMode={true}       // Enforce min/max validation
  readonly={false}        // Prevent editing
  enabled={true}          // Enable or disable control (false = disabled)
  showSpinButton={true}   // Show/hide spinner arrows
/>
```

## Complete Example: Quantity Input

Here's a practical example with quantity input for a shopping cart:

```jsx
import React, { useState } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';
import '@syncfusion/ej2-base/styles/material3.css';
import '@syncfusion/ej2-buttons/styles/material3.css';
import '@syncfusion/ej2-inputs/styles/material3.css';

export default function ProductQuantity() {
  const [quantity, setQuantity] = useState(1);
  const price = 29.99;

  const handleQuantityChange = (e) => {
    setQuantity(e.value);
  };

  return (
    <div style={{ padding: '30px', maxWidth: '400px' }}>
      <h2>Product Order</h2>
      
      <div style={{ marginBottom: '15px' }}>
        <label style={{ display: 'block', marginBottom: '5px' }}>
          <strong>Product:</strong> Widget Pro
        </label>
        <label style={{ display: 'block', marginBottom: '5px' }}>
          <strong>Price:</strong> ${price}
        </label>
      </div>

      <div style={{ marginBottom: '15px' }}>
        <label style={{ display: 'block', marginBottom: '8px' }}>
          <strong>Quantity:</strong>
        </label>
        <NumericTextBoxComponent
          value={quantity}
          change={handleQuantityChange}
          min={1}
          max={100}
          step={1}
          decimals={0}
          showSpinButton={true}
        />
      </div>

      <div style={{ 
        padding: '15px', 
        backgroundColor: '#f5f5f5', 
        borderRadius: '4px' 
      }}>
        <p>
          <strong>Total:</strong> ${(quantity * price).toFixed(2)}
        </p>
        <p>
          <small>Quantity: {quantity} × ${price} = ${(quantity * price).toFixed(2)}</small>
        </p>
      </div>

      <button 
        onClick={() => console.log(`Ordered ${quantity} units`)}
        style={{
          padding: '10px 20px',
          backgroundColor: '#0066cc',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
          marginTop: '15px'
        }}
      >
        Add to Cart
      </button>
    </div>
  );
}
```

**Output:**
- Product name and price display
- NumericTextBox for quantity (1-100, no decimals)
- Spin buttons for easy adjustment
- Real-time total calculation
- Add to Cart button

## Running Your Application

After setting up the component, run:

```bash
npm start
```

The application opens in your browser at `http://localhost:3000`.

**Verify the NumericTextBox:**
- Input field appears with default value
- Spinner buttons are visible (unless disabled)
- Click arrows to increment/decrement
- Type directly into the field
- Format and validation apply as configured

## Troubleshooting

### CSS Not Loading
**Problem:** Component appears unstyled or buttons look wrong

**Solution:** Verify CSS imports in order:
```jsx
import '@syncfusion/ej2-base/styles/material3.css';           // Load first
import '@syncfusion/ej2-buttons/styles/material3.css';
import '@syncfusion/ej2-inputs/styles/material3.css';         // Load before component CSS
import '@syncfusion/ej2-popups/styles/material3.css';
```

### Component Not Responding
**Problem:** Spinner clicks don't work or value doesn't update

**Solution:** 
1. Ensure `onChange` handler updates state
2. Check `value` prop is set correctly
3. Verify `readonly` is not true
4. Check browser console for errors

### Value Not Persisting
**Problem:** Entered values reset or don't save

**Solution:**
- Use `change` event to update React state
- Ensure component is controlled (has `value` prop)
- Example: `<NumericTextBoxComponent value={state} change={(e) => setState(e.value)} />`

## Next Steps

- **Formatting:** See [formats-and-validation.md](formats-and-validation.md) for currency, percentage, and custom formats
- **Validation:** Learn min/max ranges and strictMode in [formats-and-validation.md](formats-and-validation.md)
- **Forms:** Integrate with React forms in [two-way-binding-forms.md](two-way-binding-forms.md)
- **Accessibility:** WCAG compliance and keyboard support in [globalization-accessibility.md](globalization-accessibility.md)
