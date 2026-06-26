# Precision & Decimals

This guide covers decimal places, precision control, rounding behavior, and edge cases.

## Table of Contents
- [Overview](#overview)
- [decimals Property](#decimals-property)
- [validateDecimalOnType Property](#validatedecimalontype-property)
- [Trailing Zeros](#trailing-zeros)
- [Rounding Behavior](#rounding-behavior)
- [Precision Edge Cases](#precision-edge-cases)
- [Practical Examples](#practical-examples)

## Overview

NumericTextBox provides fine-grained control over decimal precision:

- **decimals:** Maximum number of decimal places allowed
- **validateDecimalOnType:** Real-time validation while typing
- **Trailing zeros:** Display or hide zeros after the decimal point
- **Rounding:** Automatic or manual control of rounding behavior
- **Edge cases:** Handle floating-point precision issues

## decimals Property

The `decimals` property controls the maximum number of decimal places:

### No Decimals (Integer Only)

```jsx
<NumericTextBoxComponent
  value={10}
  decimals={0}  // Only whole numbers allowed
  // Input: 42.99 → Stored as 42
/>
```

**Use cases:**
- Quantity fields
- Counting (items, people, votes)
- Age or years

### Single Decimal Place

```jsx
<NumericTextBoxComponent
  value={9.5}
  decimals={1}  // One decimal place maximum
  // Input: 3.567 → Displays as 3.5
/>
```

**Use cases:**
- Ratings (0.5 stars)
- Temperature (20.5°C)
- Single precision measurements

### Two Decimal Places (Default for Currency)

```jsx
<NumericTextBoxComponent
  value={99.99}
  decimals={2}  // Two decimal places maximum
  format="c2"
  // Input: 3.567 → Displays as 3.57
/>
```

**Use cases:**
- Currency/money ($99.99)
- Prices
- Financial calculations

### Three or More Decimals

```jsx
<NumericTextBoxComponent
  value={3.14159}
  decimals={3}  // Three decimal places
  // Input: 3.14159 → Stored as 3.142
/>
```

**Use cases:**
- Scientific measurements
- Precise calculations
- Exchange rates

### Dynamic Decimals

```jsx
import React, { useState } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function DynamicDecimals() {
  const [value, setValue] = useState(10);
  const [precision, setPrecision] = useState(2);

  return (
    <div style={{ padding: '20px' }}>
      <div style={{ marginBottom: '15px' }}>
        <label>Precision (decimal places):</label>
        <select 
          value={precision}
          onChange={(e) => setPrecision(parseInt(e.target.value))}
        >
          <option value={0}>0 (Integer)</option>
          <option value={1}>1</option>
          <option value={2}>2</option>
          <option value={3}>3</option>
          <option value={4}>4</option>
        </select>
      </div>

      <div>
        <label>Value:</label>
        <NumericTextBoxComponent
          value={value}
          onChange={(e) => setValue(e.value)}
          decimals={precision}
        />
      </div>

      <p>Current value: {value.toFixed(precision)}</p>
    </div>
  );
}
```

## validateDecimalOnType Property

The `validateDecimalOnType` property controls whether decimals are validated in real-time:

### validateDecimalOnType = true (Strict)

When `true`, decimal validation happens as you type:

```jsx
<NumericTextBoxComponent
  value={10.00}
  decimals={2}
  validateDecimalOnType={true}  // Strict validation
  // User types: 3.567
  // Result: Only 3.56 can be entered (rejects 7 during typing)
/>
```

**Behavior:**
- User cannot type more decimals than allowed
- Keystroke blocked if it exceeds decimal limit
- Input is constrained during typing

### validateDecimalOnType = false (Loose)

When `false`, decimal validation happens only on blur (when leaving field):

```jsx
<NumericTextBoxComponent
  value={10.00}
  decimals={2}
  validateDecimalOnType={false}  // Loose validation
  // User types: 3.567
  // While typing: 3.567 is displayed
  // On blur: Rounds to 3.57
/>
```

**Behavior:**
- User can type more decimals than allowed
- Value is corrected when field loses focus
- Better for copy-paste operations

### Choosing Between Strict and Loose

**Use `validateDecimalOnType={true}` for:**
- Financial inputs where precision is critical
- Fields where incorrect values cause problems
- Real-time validation is preferred

**Use `validateDecimalOnType={false}` for:**
- User-friendly interfaces where typing shouldn't be restricted
- Scientific input where users may paste values
- Copy-paste operations need to work smoothly

## Trailing Zeros

### Displaying Trailing Zeros

By default, trailing zeros may not display. Control this with formatting:

```jsx
// Without trailing zeros
<NumericTextBoxComponent
  value={99}
  decimals={2}
  // Displays: 99 (not 99.00)
/>

// With trailing zeros
<NumericTextBoxComponent
  value={99}
  decimals={2}
  format="n2"  // Shows: 99.00
/>

// Currency always shows zeros
<NumericTextBoxComponent
  value={99}
  format="c2"  // Shows: $99.00
/>
```

### Practical Example: Price Display

```jsx
import React, { useState } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function PriceDisplay() {
  const [price, setPrice] = useState(99.5);

  return (
    <div style={{ padding: '20px' }}>
      <h3>Product Price</h3>

      <div style={{ marginBottom: '15px' }}>
        <label><strong>Without Trailing Zeros:</strong></label>
        <p style={{ fontSize: '18px' }}>Price: {price}</p>
      </div>

      <div style={{ marginBottom: '15px' }}>
        <label><strong>With Trailing Zeros (format="c2"):</strong></label>
        <NumericTextBoxComponent
          value={price}
          onChange={(e) => setPrice(e.value)}
          format="c2"
          decimals={2}
        />
      </div>

      <div style={{
        padding: '10px',
        backgroundColor: '#f5f5f5',
        borderRadius: '4px'
      }}>
        <p><strong>Displayed:</strong> ${price.toFixed(2)}</p>
      </div>
    </div>
  );
}
```

## Rounding Behavior

### Standard Rounding

By default, NumericTextBox uses banker's rounding (round to nearest even):

```jsx
<NumericTextBoxComponent
  value={3.125}
  decimals={2}
  // Result: 3.12 (rounds down to even)
/>

<NumericTextBoxComponent
  value={3.135}
  decimals={2}
  // Result: 3.14 (rounds up to even)
/>
```

### Manual Rounding

For custom rounding logic, handle in onChange:

```jsx
import React, { useState } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function CustomRounding() {
  const [value, setValue] = useState(3.125);

  const handleChange = (e) => {
    // Custom rounding: always round half up
    const roundHalfUp = (num, decimals) => {
      const factor = Math.pow(10, decimals);
      return Math.round(num * factor) / factor;
    };

    const rounded = roundHalfUp(e.value, 2);
    setValue(rounded);
  };

  return (
    <div style={{ padding: '20px' }}>
      <label>Custom Rounding (Always Round Half Up):</label>
      <NumericTextBoxComponent
        value={value}
        onChange={handleChange}
        decimals={2}
      />
      <p>Value: {value.toFixed(2)}</p>
    </div>
  );
}
```

## Precision Edge Cases

### Floating-Point Arithmetic Issues

JavaScript floating-point can cause precision issues:

```jsx
// Problem: 0.1 + 0.2 ≠ 0.3
console.log(0.1 + 0.2);  // 0.30000000000000004

// Solution: Use validateDecimalOnType and formatting
<NumericTextBoxComponent
  value={0.1}
  decimals={2}
  validateDecimalOnType={true}
  format="n2"  // Handles display precision
/>
```

### Very Large Numbers

With large numbers, precision diminishes:

```jsx
<NumericTextBoxComponent
  value={123456789.123456}
  decimals={6}
  // Large numbers lose decimal precision
  // JavaScript's Number type has limits
/>
```

### Very Small Numbers

Very small decimal numbers can cause issues:

```jsx
<NumericTextBoxComponent
  value={0.000001}
  decimals={6}
  // Display as: 0.000001
/>
```

## Practical Examples

### Example 1: Currency Input (2 Decimals)

```jsx
import React, { useState } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function CurrencyInput() {
  const [amount, setAmount] = useState(99.99);

  return (
    <div style={{ padding: '20px', maxWidth: '400px' }}>
      <h3>Invoice Amount</h3>

      <NumericTextBoxComponent
        value={amount}
        onChange={(e) => setAmount(e.value)}
        format="c2"
        decimals={2}
        validateDecimalOnType={true}
        min={0}
        placeholder="0.00"
      />

      <p style={{ marginTop: '15px' }}>
        <strong>Amount:</strong> ${amount.toFixed(2)}
      </p>
    </div>
  );
}
```

### Example 2: Scientific Precision (4 Decimals)

```jsx
import React, { useState } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function ScientificInput() {
  const [measurement, setMeasurement] = useState(1.2345);

  return (
    <div style={{ padding: '20px', maxWidth: '400px' }}>
      <h3>Scientific Measurement</h3>

      <NumericTextBoxComponent
        value={measurement}
        change={(e) => setMeasurement(e.value)}
        decimals={4}
        validateDecimalOnType={true}
        placeholder="0.0000"
      />

      <p style={{ marginTop: '15px' }}>
        <strong>Measurement:</strong> {measurement.toFixed(4)} mm
      </p>
    </div>
  );
}
```

### Example 3: Rating with Half Stars (1 Decimal)

```jsx
import React, { useState } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function RatingInput() {
  const [rating, setRating] = useState(4.5);

  const getRatingStars = (value) => {
    const full = Math.floor(value);
    const half = value % 1 !== 0 ? '½' : '';
    return '⭐'.repeat(full) + half;
  };

  return (
    <div style={{ padding: '20px', maxWidth: '400px' }}>
      <h3>Product Rating</h3>

      <NumericTextBoxComponent
        value={rating}
        onChange={(e) => setRating(e.value)}
        decimals={1}
        min={0}
        max={5}
        step={0.5}
        validateDecimalOnType={true}
      />

      <p style={{ marginTop: '15px', fontSize: '24px' }}>
        {getRatingStars(rating)} ({rating})
      </p>
    </div>
  );
}
```

### Example 4: Percentage with Precision (2 Decimals)

```jsx
import React, { useState } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function PercentageInput() {
  const [percentage, setPercentage] = useState(33.33);

  return (
    <div style={{ padding: '20px', maxWidth: '400px' }}>
      <h3>Discount Percentage</h3>

      <NumericTextBoxComponent
        value={percentage}
        change={(e) => setPercentage(e.value)}
        decimals={2}
        validateDecimalOnType={true}
        min={0}
        max={100}
        format="n2"
      />

      <p style={{ marginTop: '15px' }}>
        Discount: {percentage.toFixed(2)}%
      </p>
    </div>
  );
}
```

### Example 5: Integer-Only Input (0 Decimals)

```jsx
import React, { useState } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function QuantityInput() {
  const [quantity, setQuantity] = useState(10);

  return (
    <div style={{ padding: '20px', maxWidth: '400px' }}>
      <h3>Item Quantity</h3>

      <NumericTextBoxComponent
        value={quantity}
        onChange={(e) => setQuantity(e.value)}
        decimals={0}
        validateDecimalOnType={true}
        min={0}
        max={9999}
        step={1}
      />

      <p style={{ marginTop: '15px' }}>
        <strong>Quantity:</strong> {quantity} units
      </p>
    </div>
  );
}
```

## Common Issues

### Trailing Zeros Not Displaying
**Problem:** Price shows 99 instead of 99.00

**Solution:** Use currency or number format:
```jsx
<NumericTextBoxComponent
  value={99}
  decimals={2}
  format="c2"  // or "n2"
/>
```

### Too Many Decimals Accepted
**Problem:** User types 3.567 when only 2 allowed

**Solution:** Enable strict validation:
```jsx
<NumericTextBoxComponent
  value={3.56}
  decimals={2}
  validateDecimalOnType={true}  // Strict
/>
```

### Rounding Issues
**Problem:** 0.1 + 0.2 displays incorrectly

**Solution:** Use formatting and validation:
```jsx
<NumericTextBoxComponent
  value={0.3}
  decimals={1}
  format="n1"
  validateDecimalOnType={true}
/>
```

## Next Steps

- **Formats:** See [formats-and-validation.md](formats-and-validation.md) for number formatting
- **Validation:** See [formats-and-validation.md](formats-and-validation.md) for min/max ranges
- **Forms:** See [two-way-binding-forms.md](two-way-binding-forms.md) for form integration
- **How-To:** See [how-to-guide.md](how-to-guide.md) for trailing zeros recipe
