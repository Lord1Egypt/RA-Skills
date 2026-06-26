# Spin Buttons & Step Control

This guide covers spinner arrows (up/down buttons), step increments, and keyboard navigation.

## Table of Contents
- [Overview](#overview)
- [Enabling/Disabling Spin Buttons](#enablingdisabling-spin-buttons)
- [Step Property](#step-property)
- [Controlling Spinner Behavior](#controlling-spinner-behavior)
- [Keyboard Navigation](#keyboard-navigation)
- [Precision with Steps](#precision-with-steps)
- [Complete Examples](#complete-examples)

## Overview

The spinner buttons (up/down arrows) are interactive controls that allow users to increment and decrement values. They are highly customizable:

- **Show/Hide:** Control visibility with `showSpinButton`
- **Step size:** Set increment amount with `step` property
- **Bounds:** Respect min/max ranges automatically
- **Keyboard:** Arrow Up/Down keys work when focused
- **Accessibility:** Full keyboard and screen reader support

## Enabling/Disabling Spin Buttons

### Show Spin Buttons (Default)

By default, NumericTextBox displays the spinner buttons:

```jsx
<NumericTextBoxComponent
  value={10}
  showSpinButton={true}  // Default, can be omitted
/>
```

**Visual:** Up arrow (▲) and down arrow (▼) buttons appear on the right side.

### Hide Spin Buttons

To create a text-only numeric input without spinners:

```jsx
<NumericTextBoxComponent
  value={10}
  showSpinButton={false}  // Hide spinner buttons
/>
```

**Use case:** 
- Text fields where users prefer direct typing
- Mobile-optimized interfaces
- Accessibility-focused interfaces where keyboard is primary

## Step Property

The `step` property defines the increment amount when using spinner buttons or arrow keys.

### Default Step (1)

```jsx
<NumericTextBoxComponent
  value={10}
  // step={1} is default
  // Clicking up arrow: 10 → 11 → 12 → ...
/>
```

### Custom Step Values

```jsx
// Step by 5
<NumericTextBoxComponent
  value={0}
  step={5}  // Increments: 0 → 5 → 10 → 15 → ...
/>

// Step by 10
<NumericTextBoxComponent
  value={50}
  step={10}  // Increments: 50 → 60 → 70 → ...
/>

// Step by 0.1 for decimals
<NumericTextBoxComponent
  value={1.0}
  step={0.1}
  decimals={1}
  // Increments: 1.0 → 1.1 → 1.2 → ...
/>
```

### Practical Examples

**Quantity (step by 1):**
```jsx
<NumericTextBoxComponent
  value={1}
  step={1}
  min={1}
  max={100}
/>
```

**Price (step by 0.01):**
```jsx
<NumericTextBoxComponent
  value={9.99}
  step={0.01}
  decimals={2}
  format="c2"
/>
```

**Percentage (step by 5):**
```jsx
<NumericTextBoxComponent
  value={50}
  step={5}
  min={0}
  max={100}
/>
```

## Controlling Spinner Behavior

### Respecting Min/Max Bounds

Spinner buttons automatically respect min/max boundaries:

```jsx
<NumericTextBoxComponent
  value={98}
  min={0}
  max={100}
  step={5}
  strictMode={true}  // Enforce boundaries
/>
```

**Behavior:**
- At value 98, clicking up arrow increments to 100 (max)
- Next click doesn't go beyond 100
- At value 0 (min), down arrow has no effect

### Combining with strictMode

With `strictMode={false}`, out-of-range values are allowed:

```jsx
<NumericTextBoxComponent
  value={95}
  min={0}
  max={100}
  step={10}
  strictMode={false}  // Allow overflow
/>
```

**Behavior:**
- Value 95 + step 10 = 105 (exceeds max, but allowed)
- Useful for temporary overages or special logic

## Keyboard Navigation

NumericTextBox supports standard keyboard shortcuts:

### Arrow Up
- Increments value by `step` amount
- Works when component is focused
- Respects min/max bounds

### Arrow Down
- Decrements value by `step` amount
- Works when component is focused
- Respects min/max bounds

### Example with Keyboard Demo

```jsx
import React, { useState } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function KeyboardDemo() {
  const [value, setValue] = useState(10);

  return (
    <div style={{ padding: '20px' }}>
      <h3>Keyboard Navigation Demo</h3>
      <p>Click the input and use Arrow Up/Down keys</p>
      
      <NumericTextBoxComponent
        value={value}
        change={(e) => setValue(e.value)}
        step={1}
        min={0}
        max={20}
        showSpinButton={true}
      />

      <p>Current Value: {value}</p>
      <p style={{ fontSize: '12px', color: '#666' }}>
        Try: Click input → Arrow Up/Down to change value
      </p>
    </div>
  );
}
```

## Precision with Steps

When using decimal steps, control precision with the `decimals` property:

### Example: Price with $0.25 Steps

```jsx
<NumericTextBoxComponent
  value={9.99}
  step={0.25}
  decimals={2}
  format="c2"
  min={0}
  // Increments: 9.99 → 10.24 → 10.49 → 10.74 → 10.99 → ...
/>
```

### Example: Temperature with 0.1 Steps

```jsx
<NumericTextBoxComponent
  value={20.0}
  step={0.1}
  decimals={1}
  min={-50}
  max={50}
  // Increments: 20.0 → 20.1 → 20.2 → ...
/>
```

### Avoiding Floating-Point Rounding

Be aware of floating-point precision issues:

```jsx
// Problem: 0.1 + 0.2 ≠ 0.3 in JavaScript
// Use validateDecimalOnType to handle this

<NumericTextBoxComponent
  value={0.1}
  step={0.2}
  decimals={1}
  validateDecimalOnType={true}
  // Internal rounding ensures accuracy
/>
```

## Complete Examples

### Example 1: Shopping Cart Quantity

A quantity picker with spinner buttons:

```jsx
import React, { useState } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function CartQuantity() {
  const [quantity, setQuantity] = useState(1);
  const pricePerUnit = 29.99;

  return (
    <div style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '4px' }}>
      <h3>Shopping Cart Item</h3>
      
      <div style={{ marginBottom: '15px' }}>
        <p><strong>Product:</strong> Premium Widget</p>
        <p><strong>Price per unit:</strong> ${pricePerUnit}</p>
      </div>

      <div style={{ marginBottom: '15px' }}>
        <label><strong>Quantity:</strong></label>
        <NumericTextBoxComponent
          value={quantity}
          change={(e) => setQuantity(e.value)}
          min={1}
          max={999}
          step={1}
          showSpinButton={true}
          decimals={0}
        />
      </div>

      <div style={{ 
        padding: '10px', 
        backgroundColor: '#f9f9f9', 
        borderRadius: '4px' 
      }}>
        <p><strong>Total:</strong> ${(quantity * pricePerUnit).toFixed(2)}</p>
      </div>
    </div>
  );
}
```

### Example 2: Temperature Control

A temperature input with 0.5-degree steps:

```jsx
import React, { useState } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function TemperatureControl() {
  const [temp, setTemp] = useState(20);

  const getStatus = () => {
    if (temp < 0) return 'Freezing';
    if (temp < 15) return 'Cold';
    if (temp < 25) return 'Comfortable';
    if (temp < 35) return 'Warm';
    return 'Hot';
  };

  return (
    <div style={{ padding: '20px' }}>
      <h3>Room Temperature Control</h3>

      <NumericTextBoxComponent
        value={temp}
        change={(e) => setTemp(e.value)}
        min={-50}
        max={60}
        step={0.5}
        decimals={1}
      />

      <p style={{ marginTop: '15px' }}>
        <strong>Temperature:</strong> {temp}°C
      </p>
      <p>
        <strong>Status:</strong> <span style={{ 
          color: temp < 0 ? 'blue' : temp < 25 ? 'green' : 'red' 
        }}>
          {getStatus()}
        </span>
      </p>
      <p style={{ fontSize: '12px', color: '#666' }}>
        Use spinner buttons or arrow keys to adjust temperature
      </p>
    </div>
  );
}
```

### Example 3: Volume Control

A slider-like volume control with percentage steps:

```jsx
import React, { useState } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function VolumeControl() {
  const [volume, setVolume] = useState(50);

  const getIcon = () => {
    if (volume === 0) return '🔇';
    if (volume < 33) return '🔈';
    if (volume < 66) return '🔉';
    return '🔊';
  };

  return (
    <div style={{ padding: '20px' }}>
      <h3>Audio Volume</h3>

      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <span style={{ fontSize: '24px' }}>{getIcon()}</span>
        
        <NumericTextBoxComponent
          value={volume}
          change={(e) => setVolume(e.value)}
          min={0}
          max={100}
          step={10}
          decimals={0}
          width="100px"
        />
      </div>

      <p style={{ marginTop: '15px' }}>
        Volume: <strong>{volume}%</strong>
      </p>
      <p style={{ fontSize: '12px', color: '#666' }}>
        Click spinner buttons or use Arrow Up/Down (step by 10)
      </p>
    </div>
  );
}
```

### Example 4: Rating with Limited Steps

A rating system (1-5 stars) with spinner buttons:

```jsx
import React, { useState } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function RatingControl() {
  const [rating, setRating] = useState(3);

  const getRatingLabel = () => {
    const labels = {
      1: '⭐ Poor',
      2: '⭐⭐ Fair',
      3: '⭐⭐⭐ Good',
      4: '⭐⭐⭐⭐ Very Good',
      5: '⭐⭐⭐⭐⭐ Excellent'
    };
    return labels[rating] || '';
  };

  return (
    <div style={{ padding: '20px' }}>
      <h3>Product Rating</h3>

      <NumericTextBoxComponent
        value={rating}
        onChange={(e) => setRating(e.value)}
        min={1}
        max={5}
        step={1}
        decimals={0}
        showSpinButton={true}
      />

      <p style={{ marginTop: '15px', fontSize: '18px' }}>
        {getRatingLabel()}
      </p>
      <p style={{ fontSize: '12px', color: '#666' }}>
        Use spinner buttons or arrow keys to rate (1-5)
      </p>
    </div>
  );
}
```

## Common Issues

### Spinner Buttons Not Appearing
**Problem:** Spinner arrows don't show

**Solution:** Check that `showSpinButton` is not set to false:
```jsx
<NumericTextBoxComponent
  value={10}
  showSpinButton={true}  // Explicitly enable or omit
/>
```

### Step Size Too Large
**Problem:** Spinner increments by wrong amount

**Solution:** Set correct `step` value:
```jsx
<NumericTextBoxComponent
  value={10}
  step={5}  // Change this value
/>
```

### Keyboard Arrows Not Working
**Problem:** Arrow Up/Down keys don't change value

**Solution:**
1. Ensure component is focused (click in the input)
2. Check that `readonly` is not true
3. Verify no other JavaScript is capturing key events

## Next Steps

- **Decimal Precision:** See [precision-decimals.md](precision-decimals.md) for `decimals` and `validateDecimalOnType`
- **Formatting:** See [formats-and-validation.md](formats-and-validation.md) for format specifiers
- **Styling:** See [adornments-and-styling.md](adornments-and-styling.md) for prefix/suffix text
- **Accessibility:** See [globalization-accessibility.md](globalization-accessibility.md) for keyboard and screen reader support
