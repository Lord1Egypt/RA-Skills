# Formats & Validation

This guide covers number formatting, range validation, and strict mode enforcement.

## Table of Contents
- [Overview](#overview)
- [Standard Format Specifiers](#standard-format-specifiers)
- [Custom Number Formats](#custom-number-formats)
- [Currency Input](#currency-input)
- [Percentage Input](#percentage-input)
- [Range Validation](#range-validation)
- [strictMode Property](#strictmode-property)
- [Examples & Edge Cases](#examples--edge-cases)

## Overview

NumericTextBox provides powerful formatting and validation capabilities:

- **Format specifiers** - Control how numbers display (currency, percentage, scientific)
- **Custom formats** - Create application-specific number patterns
- **Min/Max validation** - Restrict input to a numeric range
- **Strict mode** - Enforce boundaries or allow out-of-range values
- **Decimal control** - Manage precision and decimal places

The `format` property controls display, while `min`, `max`, and `strictMode` control validation.

## Standard Format Specifiers

NumericTextBox supports standard .NET number format specifiers:

### Number Format (n)

Displays the number with thousand separators and specified decimals.

```jsx
<NumericTextBoxComponent
  value={1234.56}
  format="n2"  // Shows: 1,234.56
/>
```

**Specifier breakdown:**
- `n` = number format
- `2` = decimal places

**Examples:**
- `format="n0"` → 1,235 (no decimals, rounded)
- `format="n1"` → 1,234.6 (one decimal)
- `format="n2"` → 1,234.56 (two decimals)
- `format="n3"` → 1,234.567 (three decimals)

### Currency Format (c)

Displays the number with currency symbol and specified decimals.

```jsx
<NumericTextBoxComponent
  value={99.99}
  format="c2"  // Shows: $99.99 (locale-dependent)
/>
```

**Note:** Currency symbol depends on your locale. For US English, `$` is used.

**Examples:**
- `format="c0"` → $100 (no decimals)
- `format="c2"` → $99.99 (two decimals)
- `format="c3"` → $99.999 (three decimals)

### Percentage Format (p)

Displays the number as a percentage (multiplies by 100).

```jsx
<NumericTextBoxComponent
  value={0.5}
  format="p"  // Shows: 50%
/>
```

**Behavior:**
- Input value 0.5 displays as 50%
- Two decimals shown by default

**Examples:**
- `format="p0"` → 50% (no decimals)
- `format="p2"` → 50.00% (two decimals)
- `value={0.123}` with `format="p2"` → 12.30%

### Scientific Notation (e)

Displays the number in scientific notation.

```jsx
<NumericTextBoxComponent
  value={1234.56}
  format="e2"  // Shows: 1.23e+003
/>
```

**Examples:**
- `format="e0"` → 1e+003
- `format="e2"` → 1.23e+003
- `format="e4"` → 1.2346e+003

## Custom Number Formats

Create custom formats using `#` (optional digit) and `0` (required digit):

### Pattern Symbols

| Symbol | Meaning |
|--------|---------|
| `0` | Required digit (shows 0 if not supplied) |
| `#` | Optional digit (omitted if not supplied) |
| `.` | Decimal separator |
| `,` | Thousand separator |

### Examples

**Format: `###,##0.##`**
- Shows thousand separators
- Optional decimal places (hidden if zero)

```jsx
<NumericTextBoxComponent
  value={1234.5}
  format="###,##0.##"  // Shows: 1,234.5
/>

<NumericTextBoxComponent
  value={1234}
  format="###,##0.##"  // Shows: 1,234 (no .00)
/>
```

**Format: `###,##0.00`**
- Shows thousand separators
- Always shows two decimal places

```jsx
<NumericTextBoxComponent
  value={1234.5}
  format="###,##0.00"  // Shows: 1,234.50
/>
```

**Format: `0000`**
- Pads with leading zeros

```jsx
<NumericTextBoxComponent
  value={42}
  format="0000"  // Shows: 0042
/>

<NumericTextBoxComponent
  value={123}
  format="0000"  // Shows: 0123
/>
```

**Format: `##0.00%`**
- Custom percentage with two decimals

```jsx
<NumericTextBoxComponent
  value={0.125}
  format="##0.00%"  // Shows: 12.50%
/>
```

## Currency Input

For monetary values, use currency format with validation:

### Simple Currency Field

```jsx
import React, { useState } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function PriceInput() {
  const [price, setPrice] = useState(99.99);

  return (
    <div style={{ padding: '20px' }}>
      <label>Product Price:</label>
      <NumericTextBoxComponent
        value={price}
        change={(e) => setPrice(e.value)}
        format="c2"
        min={0}
        decimals={2}
        placeholder="$0.00"
      />
      <p>Price: {price}</p>
    </div>
  );
}
```

### Multiple Currencies

To support different currencies, control the format dynamically:

```jsx
import React, { useState } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function CurrencyConverter() {
  const [amount, setAmount] = useState(100);
  const [currency, setCurrency] = useState('USD');

  const currencyFormats = {
    'USD': 'c2',      // $100.00
    'EUR': 'c2',      // €100.00 (locale-dependent)
    'GBP': 'c2',      // £100.00
    'JPY': 'c0',      // ¥100 (no decimals)
  };

  return (
    <div style={{ padding: '20px' }}>
      <select 
        value={currency}
        onChange={(e) => setCurrency(e.target.value)}
      >
        <option>USD</option>
        <option>EUR</option>
        <option>GBP</option>
        <option>JPY</option>
      </select>

      <NumericTextBoxComponent
        value={amount}
        change={(e) => setAmount(e.value)}
        format={currencyFormats[currency]}
        min={0}
        decimals={currency === 'JPY' ? 0 : 2}
      />
    </div>
  );
}
```

## Percentage Input

For percentage values:

### Basic Percentage

```jsx
<NumericTextBoxComponent
  value={25}           // Display as 25%
  format="p0"          // No decimals: 25%
  min={0}
  max={100}
/>
```

### Percentage with Decimals

```jsx
<NumericTextBoxComponent
  value={25.5}         // Display as 25.50%
  format="p2"          // Two decimals: 25.50%
  min={0}
  max={100}
/>
```

**Important:** When using `format="p"`, the `value` should be the percentage number (0-100), not decimal (0-1).

## Range Validation

Restrict input to a numeric range using `min` and `max`:

### Basic Range

```jsx
<NumericTextBoxComponent
  value={50}
  min={0}              // Minimum value
  max={100}            // Maximum value
  step={5}
/>
```

### Age Validation (18-120)

```jsx
<NumericTextBoxComponent
  value={30}
  min={18}
  max={120}
  placeholder="Enter age"
/>
```

### Rating (1-5)

```jsx
<NumericTextBoxComponent
  value={3}
  min={1}
  max={5}
  decimals={0}
  step={1}
/>
```

## strictMode Property

The `strictMode` property controls how out-of-range values are handled:

### strictMode = true (default)

When `strictMode={true}`, values outside the range are corrected to fit:

```jsx
<NumericTextBoxComponent
  value={150}
  min={0}
  max={100}
  strictMode={true}    // Default behavior
/>
```

**Behavior:**
- User enters 150 → Auto-corrects to 100 (max)
- User enters -50 → Auto-corrects to 0 (min)
- Spinner buttons are bounded (won't go beyond range)

### strictMode = false

When `strictMode={false}`, values can exceed the range, but validation warnings may appear:

```jsx
<NumericTextBoxComponent
  value={150}
  min={0}
  max={100}
  strictMode={false}   // Allow out-of-range values
/>
```

**Behavior:**
- User can enter 150 even if max=100
- Useful for temporary overflow or special cases
- Validation can be handled programmatically

## Examples & Edge Cases

### Complete Form with Validation

```jsx
import React, { useState } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function BudgetForm() {
  const [income, setIncome] = useState(50000);
  const [savings, setSavings] = useState(5000);
  const [expense, setExpense] = useState(30000);
  const [errors, setErrors] = useState({});

  const handleValidation = () => {
    const newErrors = {};
    if (income < 0) newErrors.income = 'Income must be positive';
    if (savings > income) newErrors.savings = 'Savings cannot exceed income';
    if (expense > income) newErrors.expense = 'Expenses cannot exceed income';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  return (
    <div style={{ padding: '20px', maxWidth: '400px' }}>
      <h2>Monthly Budget</h2>

      <div style={{ marginBottom: '15px' }}>
        <label>Annual Income:</label>
        <NumericTextBoxComponent
          value={income}
          change={(e) => setIncome(e.value)}
          format="c2"
          min={0}
          decimals={2}
        />
        {errors.income && <p style={{ color: 'red' }}>{errors.income}</p>}
      </div>

      <div style={{ marginBottom: '15px' }}>
        <label>Savings Goal:</label>
        <NumericTextBoxComponent
          value={savings}
          change={(e) => setSavings(e.value)}
          format="c2"
          min={0}
          max={income}
          strictMode={true}
          decimals={2}
        />
        {errors.savings && <p style={{ color: 'red' }}>{errors.savings}</p>}
      </div>

      <div style={{ marginBottom: '15px' }}>
        <label>Planned Expenses:</label>
        <NumericTextBoxComponent
          value={expense}
          change={(e) => setExpense(e.value)}
          format="c2"
          min={0}
          max={income}
          strictMode={true}
          decimals={2}
        />
        {errors.expense && <p style={{ color: 'red' }}>{errors.expense}</p>}
      </div>

      <p>
        <strong>Remaining:</strong> {((income - expense - savings).toFixed(2))}
      </p>

      <button onClick={handleValidation}>Validate Budget</button>
    </div>
  );
}
```

### Edge Case: Zero Padding

```jsx
// Invoice number format with leading zeros
<NumericTextBoxComponent
  value={42}
  format="0000"        // Always 4 digits: 0042
  min={1}
  max={9999}
/>

// ZIP code format
<NumericTextBoxComponent
  value={1234}
  format="00000"       // Always 5 digits: 01234
/>
```

### Edge Case: Large Numbers

```jsx
// Large numbers with thousand separators
<NumericTextBoxComponent
  value={1500000}
  format="###,##0"     // Shows: 1,500,000
  min={0}
  decimals={0}
/>
```

## Next Steps

- **Decimal Control:** See [precision-decimals.md](precision-decimals.md) for decimal places and rounding
- **Spin Buttons:** See [spin-buttons-and-step.md](spin-buttons-and-step.md) for increment control
- **Forms:** See [two-way-binding-forms.md](two-way-binding-forms.md) for form integration
- **Styling:** See [adornments-and-styling.md](adornments-and-styling.md) for prefix/suffix and appearance
