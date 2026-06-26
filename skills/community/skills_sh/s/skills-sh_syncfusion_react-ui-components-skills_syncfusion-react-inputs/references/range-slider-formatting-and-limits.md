# Formatting and Limits

## Table of Contents
- [Value Formatting](#value-formatting)
- [Format API](#format-api)
- [Custom Formatting with Events](#custom-formatting-with-events)
- [Slider Limits Overview](#slider-limits-overview)
- [Default and MinRange Limits](#default-and-minrange-limits)
- [Range Slider Limits](#range-slider-limits)
- [Handle Locking](#handle-locking)
- [Real-World Examples](#real-world-examples)

## Value Formatting

Formatting displays slider values in specific formats (currency, percentage, etc.) in tooltips and ticks.

### Where Formatting Applies

Formatting can be applied to:
1. **Tooltip values** - What displays when hovering/dragging
2. **Tick labels** - What displays under tick marks
3. **Both together** - Consistent formatting throughout

## Format API

The Format API provides predefined formatting styles using standard format strings.

### Available Format Strings

| Format | Example | Use Case |
|--------|---------|----------|
| `C` or `C0` | $50 | Currency (no decimals) |
| `C2` | $50.00 | Currency (2 decimals) |
| `P` or `P0` | 50% | Percentage |
| `P2` | 50.00% | Percentage (2 decimals) |
| `N` or `N0` | 1,234 | Number with separators |
| `N2` | 1,234.56 | Number (2 decimals) |

### Currency Format Example

```tsx
import React from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';

function CurrencySlider() {
  const [price, setPrice] = React.useState(500);

  return (
    <div>
      <h3>Product Price: {price}</h3>
      <SliderComponent
        id="price-slider"
        value={price}
        change={(e) => setPrice(e.value as number)}
        min={10}
        max={1000}
        step={10}
        tooltip={{
          isVisible: true,
          format: 'C0'  // Currency format
        }}
        ticks={{
          placement: 'After',
          largeStep: 200,
          format: 'C0'  // Same format on ticks
        }}
      />
    </div>
  );
}

export default CurrencySlider;
```

**Display:** `$10`, `$210`, `$410`, etc.

### Percentage Format Example

```tsx
<SliderComponent
  id="discount-slider"
  type="Range"
  value={[0.1, 0.5]}
  min={0}
  max={1}
  step={0.05}
  tooltip={{
    isVisible: true,
    format: 'P0'  // 10%, 50%
  }}
  ticks={{
    placement: 'After',
    largeStep: 0.2,
    format: 'P0'
  }}
/>
```

**Display:** `0%`, `20%`, `40%`, `60%`, `80%`, `100%`

### Number Format Example

```tsx
<SliderComponent
  id="quantity-slider"
  type="Range"
  value={[1000, 5000]}
  min={0}
  max={10000}
  step={100}
  tooltip={{
    isVisible: true,
    format: 'N0'  // 1,000 5,000
  }}
/>
```

**Display:** `1,000`, `5,000`

## Custom Formatting with Events

For complex formatting beyond standard formats, use event handlers.

### Using renderingTicks Event

Customize how tick labels are formatted:

```tsx
import React from 'react';
import { SliderComponent, SliderTickEventArgs } from '@syncfusion/ej2-react-inputs';

function CustomTickFormatSlider() {
  const monthNames = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
  ];

  function renderingTicksHandler(args: SliderTickEventArgs) {
    const monthIndex = parseInt(args.value.toString()) - 1;
    args.text = monthNames[monthIndex];
  }

  return (
    <SliderComponent
      id="month-slider"
      min={1}
      max={12}
      value={6}
      ticks={{
        placement: 'After',
        largeStep: 1
      }}
      renderingTicks={renderingTicksHandler.bind(this) as any}
    />
  );
}

export default CustomTickFormatSlider;
```

**Display:** `Jan`, `Feb`, `Mar`, etc.

### Using tooltipChange Event

Customize tooltip formatting:

```tsx
import React from 'react';
import { SliderComponent, SliderTooltipEventArgs } from '@syncfusion/ej2-react-inputs';

function CustomTooltipSlider() {
  function tooltipChangeHandler(args: SliderTooltipEventArgs) {
    const value = args.value as number;
    const percentage = Math.round((value / 100) * 100);
    args.text = `${percentage}% Complete`;
  }

  return (
    <SliderComponent
      id="progress-slider"
      type="MinRange"
      value={75}
      min={0}
      max={100}
      tooltip={{
        isVisible: true,
        showOn: 'Always'
      }}
      tooltipChange={tooltipChangeHandler.bind(this) as any}
    />
  );
}

export default CustomTooltipSlider;
```

**Display:** `75% Complete`

## Slider Limits Overview

Limits restrict slider handle movement to specific ranges. Useful for preventing invalid selections.

### Limit Properties

| Property | Type | Purpose |
|----------|------|---------|
| `enabled` | `boolean` | Enable/disable limits |
| `minStart` | `number` | Min position for first handle |
| `minEnd` | `number` | Max position for first handle |
| `maxStart` | `number` | Min position for second handle |
| `maxEnd` | `number` | Max position for second handle |
| `startHandleFixed` | `boolean` | Lock first handle |
| `endHandleFixed` | `boolean` | Lock second handle |

### Visual Indication

When limits are enabled, restricted areas appear darkened:

```
Unrestricted: |●----- Available area --------|
Limited:      |◼◼◼●----- Available area -----●◼◼◼|
              Restricted          Limited          Restricted
```

## Default and MinRange Limits

### Single Handle Limits

For Default or MinRange sliders, use `minStart`, `minEnd`, and `startHandleFixed`:

```tsx
import React from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';

function LimitedSingleSlider() {
  return (
    <div>
      <h3>Default Slider with Limits</h3>
      <SliderComponent
        id="limited-default"
        type="Default"
        value={30}
        min={0}
        max={100}
        limits={{
          enabled: true,
          minStart: 10,    // Can't go below 10
          minEnd: 40       // Can't go above 40
        }}
        tooltip={{ isVisible: true }}
      />
    </div>
  );
}

export default LimitedSingleSlider;
```

**Effect:** Handle restricted to 10-40 range, even though slider range is 0-100.

### Lock Single Handle

Prevent any movement of the single handle:

```tsx
<SliderComponent
  id="locked-slider"
  type="Default"
  value={50}
  limits={{
    enabled: true,
    startHandleFixed: true  // Handle can't move
  }}
  tooltip={{ isVisible: true }}
/>
```

## Range Slider Limits

### Limit Each Handle Separately

Control movement of first and second handles independently:

```tsx
import React from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';

function LimitedRangeSlider() {
  return (
    <SliderComponent
      id="limited-range"
      type="Range"
      value={[30, 70]}
      min={0}
      max={100}
      limits={{
        enabled: true,
        minStart: 10,     // First handle: min 10
        minEnd: 40,       // First handle: max 40
        maxStart: 60,     // Second handle: min 60
        maxEnd: 90        // Second handle: max 90
      }}
      tooltip={{ isVisible: true }}
    />
  );
}

export default LimitedRangeSlider;
```

**Effect:**
- First handle can move: 10-40
- Second handle can move: 60-90
- Gap between handles maintained: 60-10 = 50 units minimum

### Price Range with Limits

```tsx
<SliderComponent
  id="price-range-limited"
  type="Range"
  value={[100, 900]}
  min={0}
  max={1000}
  step={50}
  limits={{
    enabled: true,
    minStart: 50,      // Min price: $50
    minEnd: 400,       // Min price max: $400
    maxStart: 600,     // Max price min: $600
    maxEnd: 1000       // Max price: $1000
  }}
  tooltip={{
    isVisible: true,
    format: 'C0'
  }}
/>
```

**Result:** Users can select $50-$400 and $600-$1000 ranges, but can't set first handle above $400 or second handle below $600.

## Handle Locking

### Lock Both Handles (Range)

Make range selection read-only:

```tsx
<SliderComponent
  id="locked-range"
  type="Range"
  value={[30, 70]}
  limits={{
    enabled: true,
    startHandleFixed: true,   // First handle locked
    endHandleFixed: true      // Second handle locked
  }}
  tooltip={{ isVisible: true }}
/>
```

**Effect:** Handles display but cannot be dragged.

### Lock Only First Handle

```tsx
<SliderComponent
  id="first-locked"
  type="Range"
  value={[30, 70]}
  limits={{
    enabled: true,
    startHandleFixed: true    // First handle locked
    // endHandleFixed not set, so second can move
  }}
/>
```

### Lock Only Second Handle

```tsx
<SliderComponent
  id="second-locked"
  type="Range"
  value={[30, 70]}
  limits={{
    enabled: true,
    endHandleFixed: true      // Second handle locked
    // startHandleFixed not set, so first can move
  }}
/>
```

## Real-World Examples

### Budget Range with Limits

```tsx
import React, { useState } from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';

function BudgetRangeSelector() {
  const [budget, setBudget] = useState([10000, 50000]);

  return (
    <div style={{ padding: '20px' }}>
      <h3>Project Budget Range</h3>
      <p>
        Minimum: ${budget[0].toLocaleString()}
      </p>
      <p>
        Maximum: ${budget[1].toLocaleString()}
      </p>
      <SliderComponent
        id="budget-slider"
        type="Range"
        value={budget}
        change={(e) => setBudget(e.value as number[])}
        min={5000}
        max={100000}
        step={1000}
        limits={{
          enabled: true,
          minStart: 5000,      // Min possible: $5,000
          minEnd: 30000,       // Min range max: $30,000
          maxStart: 40000,     // Max range min: $40,000
          maxEnd: 100000       // Max possible: $100,000
        }}
        tooltip={{
          isVisible: true,
          format: 'C0'
        }}
        ticks={{
          placement: 'After',
          largeStep: 20000,
          format: 'C0'
        }}
      />
    </div>
  );
}

export default BudgetRangeSelector;
```

### Discount Percentage Range

```tsx
<SliderComponent
  id="discount-range"
  type="Range"
  value={[0.05, 0.20]}
  min={0}
  max={0.50}
  step={0.01}
  limits={{
    enabled: true,
    minStart: 0,        // Minimum discount: 0%
    minEnd: 0.25,       // Max discount on min: 25%
    maxStart: 0.25,     // Min discount on max: 25%
    maxEnd: 0.50        // Maximum discount: 50%
  }}
  tooltip={{
    isVisible: true,
    format: 'P0'
  }}
/>
```

### Temperature Range (Fixed Spread)

Ensure minimum 5-degree spread between handles:

```tsx
<SliderComponent
  id="temp-range"
  type="Range"
  value={[65, 75]}
  min={50}
  max={100}
  step={1}
  limits={{
    enabled: true,
    minStart: 50,       // Min temp: 50°F
    minEnd: 70,         // Low can't exceed 70°F
    maxStart: 75,       // High starts at 75°F minimum
    maxEnd: 100         // Max temp: 100°F
  }}
  tooltip={{ isVisible: true }}
/>
```

### Read-Only Display

Show fixed range for informational purposes:

```tsx
<SliderComponent
  id="status-display"
  type="Range"
  value={[20, 80]}
  min={0}
  max={100}
  limits={{
    enabled: true,
    startHandleFixed: true,   // Both locked
    endHandleFixed: true
  }}
  tooltip={{
    isVisible: true,
    showOn: 'Always'
  }}
  ticks={{
    placement: 'After',
    largeStep: 20,
    showSmallTicks: true
  }}
/>
```

## Common Patterns

### Pattern 1: Prevent Invalid Range

Ensure minimum gap between handles:

```tsx
// Prevent selection with less than 10 units between handles
limits={{
  enabled: true,
  minStart: 0,
  minEnd: 40,      // If first handle at 40, second starts at 50
  maxStart: 50,    // 50 - 40 = 10 unit minimum gap
  maxEnd: 100
}}
```

### Pattern 2: Category Constraints

Different limits for different product categories:

```tsx
const categoryLimits = {
  budget: { minStart: 0, minEnd: 500, maxStart: 500, maxEnd: 1000 },
  standard: { minStart: 500, minEnd: 2000, maxStart: 2000, maxEnd: 5000 },
  premium: { minStart: 5000, minEnd: 10000, maxStart: 10000, maxEnd: 50000 }
};

// Use with:
limits={{
  enabled: true,
  ...categoryLimits[selectedCategory]
}}
```

### Pattern 3: Disabled Range

Lock slider to show information only:

```tsx
<SliderComponent
  id="stats-display"
  type="Range"
  value={[40, 60]}
  limits={{
    enabled: true,
    startHandleFixed: true,
    endHandleFixed: true
  }}
  disabled={true}  // Additional: disable entire component
/>
```

## Edge Cases

### Overlapping Handles

When limits allow handles to touch or overlap:

```tsx
// First handle can be at 40-50, second at 40-60
// They can overlap at 40-50 range
limits={{
  enabled: true,
  minStart: 40,
  minEnd: 50,
  maxStart: 40,
  maxEnd: 60
}}
```

**Note:** Second handle will move first handle out of overlap automatically.

### No Gap Between Limits

When `minEnd` equals `maxStart`:

```tsx
limits={{
  enabled: true,
  minEnd: 50,      // First handle max
  maxStart: 50     // Second handle min
}}
```

First handle stops at 50, second starts at 50. Can't change order.

## Troubleshooting

### Limits Not Working

**Problem:** `limits={{ enabled: true }}` has no effect

**Solution:** Verify properties are set:
```tsx
limits={{
  enabled: true,         // Must be true
  minStart: 10,          // Required for Default/MinRange
  minEnd: 40,
  // OR for Range:
  maxStart: 60,
  maxEnd: 90
}}
```

### Handles Won't Move

**Problem:** Handles appear but can't drag

**Solution:** Check if fixed:
```tsx
limits={{
  startHandleFixed: false,  // Should be false to allow dragging
  endHandleFixed: false
}}
```

## Next Steps

1. Apply formatting to match your data type (currency, percentage, etc.)
2. Add limits if restricting selections is needed
3. Test with events to verify formatting works
4. Review [styling.md](styling.md) for visual customization
5. Test accessibility in [accessibility.md](accessibility.md)
