# Tooltips and Ticks

## Table of Contents
- [Tooltips Overview](#tooltips-overview)
- [Tooltip Placement](#tooltip-placement)
- [Tooltip Visibility Modes](#tooltip-visibility-modes)
- [Ticks Overview](#ticks-overview)
- [Tick Steps](#tick-steps)
- [Tick Placement](#tick-placement)
- [Small Ticks](#small-ticks)
- [Combined Tooltips and Ticks](#combined-tooltips-and-ticks)
- [Advanced Examples](#advanced-examples)

## Tooltips Overview

Tooltips display the current slider value when interacting with the handle. They provide visual feedback of the selected value.

### Basic Tooltip

```tsx
import React from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';

function TooltipExample() {
  return (
    <SliderComponent
      id="slider"
      value={30}
      tooltip={{ isVisible: true }}
    />
  );
}

export default TooltipExample;
```

### Tooltip Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `isVisible` | `boolean` | `false` | Enable/disable tooltip |
| `placement` | `'Before' \| 'After'` | `'After'` | Position above or below slider |
| `showOn` | `'Always' \| 'Focus' \| 'Click'` | `'Focus'` | When to display |
| `format` | `string` | - | Format string (e.g., 'C2', 'P0') |

## Tooltip Placement

### Before Placement

Tooltip displays above (horizontal) or left of (vertical) the handle.

```tsx
<SliderComponent
  id="slider"
  value={50}
  tooltip={{
    isVisible: true,
    placement: 'Before'
  }}
/>
```

### After Placement

Tooltip displays below (horizontal) or right of (vertical) the handle.

```tsx
<SliderComponent
  id="slider"
  value={50}
  tooltip={{
    isVisible: true,
    placement: 'After'
  }}
/>
```

### Choosing Placement

- **Before:** Better for top-aligned content, minimizes layout shift
- **After:** Default, standard positioning below slider track
- **Test:** Choose based on surrounding UI elements

## Tooltip Visibility Modes

### Focus Mode

Tooltip displays only when slider is focused or handle is being dragged. User can tab to slider with keyboard.

```tsx
<SliderComponent
  id="slider"
  value={50}
  tooltip={{
    isVisible: true,
    showOn: 'Focus'  // Default
  }}
/>
```

**Use case:** Standard forms, dense interfaces

### Always Mode

Tooltip always visible, even when slider is not interacting.

```tsx
<SliderComponent
  id="slider"
  value={50}
  tooltip={{
    isVisible: true,
    showOn: 'Always'
  }}
/>
```

**Use case:** Important values, informational displays

### Click Mode

Tooltip displays only when user clicks the slider handle.

```tsx
<SliderComponent
  id="slider"
  value={50}
  tooltip={{
    isVisible: true,
    showOn: 'Click'
  }}
/>
```

**Use case:** Minimal UI, values not critical until selection

## Ticks Overview

Ticks are scale markers on the slider track showing major and minor value points. They help users see available positions and step intervals.

### Basic Ticks

```tsx
<SliderComponent
  id="slider"
  value={50}
  ticks={{
    placement: 'After',
    largeStep: 20,
    smallStep: 5
  }}
/>
```

### Tick Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `placement` | `'Before' \| 'After'` | `'After'` | Above or below track |
| `largeStep` | `number` | - | Major tick interval |
| `smallStep` | `number` | - | Minor tick interval |
| `showSmallTicks` | `boolean` | `false` | Show minor ticks |

## Tick Steps

### Large Step Only

Display major ticks at specified intervals.

```tsx
<SliderComponent
  id="slider"
  value={50}
  min={0}
  max={100}
  ticks={{
    placement: 'After',
    largeStep: 25  // Ticks at 0, 25, 50, 75, 100
  }}
/>
```

**Visually:**
```
|----0----●----25----50----75----100
 ◆        ◆        ◆        ◆       ◆
```

### Large and Small Steps

Show both major and minor tick marks.

```tsx
<SliderComponent
  id="slider"
  value={50}
  min={0}
  max={100}
  ticks={{
    placement: 'After',
    largeStep: 20,    // Major at 20, 40, 60, 80, 100
    smallStep: 5,     // Minor at 5, 10, 15, 25, ...
    showSmallTicks: true
  }}
/>
```

**Visually:**
```
|0  ●●● 20  ●●● 40  ●●● 60  ●●● 80  ●●● 100
 ◆ ◇ ◇ ◇ ◆ ◇ ◇ ◇ ◆ ◇ ◇ ◇ ◆ ◇ ◇ ◇ ◆
 Major    Minor    Major    Minor
```

### Small Steps Without Showing

Configure step intervals for dragging without visual ticks.

```tsx
<SliderComponent
  id="slider"
  value={50}
  step={5}         // Drag moves in 5-unit increments
  // No ticks configured
/>
```

## Tick Placement

### Before Placement

Ticks display above (horizontal) or left of (vertical) the track.

```tsx
<SliderComponent
  id="slider"
  value={50}
  ticks={{
    placement: 'Before',
    largeStep: 20
  }}
/>
```

### After Placement (Default)

Ticks display below (horizontal) or right of (vertical) the track.

```tsx
<SliderComponent
  id="slider"
  value={50}
  ticks={{
    placement: 'After',
    largeStep: 20
  }}
/>
```

## Small Ticks

### Displaying Small Ticks

Enable minor ticks with `showSmallTicks: true`.

```tsx
<SliderComponent
  id="slider"
  value={50}
  ticks={{
    placement: 'After',
    largeStep: 20,
    smallStep: 5,
    showSmallTicks: true  // Enable minor ticks
  }}
/>
```

### Without Small Ticks (Default)

```tsx
<SliderComponent
  id="slider"
  value={50}
  ticks={{
    placement: 'After',
    largeStep: 20,
    smallStep: 5
    // showSmallTicks: false (default)
  }}
/>
```

Only major ticks display even though smallStep is defined.

## Combined Tooltips and Ticks

### Standard Combination

Tooltip shows handle value, ticks show scale.

```tsx
import React from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';

function CombinedExample() {
  return (
    <SliderComponent
      id="slider"
      value={50}
      min={0}
      max={100}
      step={5}
      tooltip={{
        isVisible: true,
        placement: 'Before',
        showOn: 'Always'
      }}
      ticks={{
        placement: 'After',
        largeStep: 25,
        smallStep: 5,
        showSmallTicks: true
      }}
    />
  );
}

export default CombinedExample;
```

### Range Slider with Tooltips and Ticks

```tsx
<SliderComponent
  id="range-slider"
  type="Range"
  value={[25, 75]}
  min={0}
  max={100}
  tooltip={{
    isVisible: true,
    placement: 'Before',
    showOn: 'Always'
  }}
  ticks={{
    placement: 'After',
    largeStep: 20,
    smallStep: 10,
    showSmallTicks: true
  }}
/>
```

Each handle shows its own tooltip.

## Advanced Examples

### Price Slider with Currency Format

```tsx
import React, { useState } from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';

function PricingSlider() {
  const [price, setPrice] = useState(500);

  return (
    <div style={{ padding: '20px' }}>
      <h3>Price Range</h3>
      <SliderComponent
        id="price-slider"
        type="Range"
        value={[100, 1000]}
        min={0}
        max={5000}
        step={100}
        change={(e) => setPrice((e.value as number[])[0])}
        tooltip={{
          isVisible: true,
          placement: 'Before',
          showOn: 'Always',
          format: 'C0'  // Currency format
        }}
        ticks={{
          placement: 'After',
          largeStep: 1000,
          smallStep: 100,
          showSmallTicks: false
        }}
      />
    </div>
  );
}

export default PricingSlider;
```

### Percentage Slider

```tsx
<SliderComponent
  id="percentage"
  type="MinRange"
  value={0.65}
  min={0}
  max={1}
  step={0.05}
  tooltip={{
    isVisible: true,
    format: 'P0'  // Percentage format
  }}
  ticks={{
    placement: 'After',
    largeStep: 0.2,
    smallStep: 0.05,
    showSmallTicks: true,
    format: 'P0'
  }}
/>
```

### Volume Control with Steps

```tsx
<SliderComponent
  id="volume"
  type="Default"
  value={50}
  min={0}
  max={100}
  step={5}  // 5% increments
  tooltip={{
    isVisible: true,
    showOn: 'Always',
    placement: 'Before'
  }}
  ticks={{
    placement: 'After',
    largeStep: 25,
    smallStep: 5,
    showSmallTicks: true
  }}
/>
```

### Scale with Labels

For custom labels on ticks, use the `renderingTicks` event:

```tsx
import React from 'react';
import { SliderComponent, SliderTickEventArgs } from '@syncfusion/ej2-react-inputs';

function LabeledScaleSlider() {
  const weekDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  function renderingTicksHandler(args: SliderTickEventArgs) {
    args.text = weekDays[parseInt(args.value.toString())];
  }

  return (
    <SliderComponent
      id="labeled-slider"
      min={0}
      max={6}
      value={3}
      step={1}
      ticks={{
        placement: 'After',
        largeStep: 1,
        format: 'N0'
      }}
      renderingTicks={renderingTicksHandler.bind(this) as any}
    />
  );
}

export default LabeledScaleSlider;
```

### No Ticks, Just Tooltip

Clean minimal interface with value feedback.

```tsx
<SliderComponent
  id="slider"
  value={50}
  tooltip={{
    isVisible: true,
    placement: 'Before',
    showOn: 'Always'
  }}
  // No ticks configured
/>
```

### Ticks Only, No Tooltip

Show scale but tooltip only on focus.

```tsx
<SliderComponent
  id="slider"
  value={50}
  tooltip={{
    isVisible: true,
    showOn: 'Focus'  // Only show on focus
  }}
  ticks={{
    placement: 'After',
    largeStep: 20,
    smallStep: 5,
    showSmallTicks: true
  }}
/>
```

## Tooltip Custom Formatting

### Using Format Strings

Common format strings with examples:

```tsx
// Currency (C) - Shows currency symbol
format: 'C2'  // $50.00
format: 'C0'  // $50

// Percentage (P) - Shows percentage
format: 'P0'  // 50%
format: 'P2'  // 50.00%

// Number (N) - Shows with separators
format: 'N0'  // 1,234
format: 'N2'  // 1,234.56

// No format (default)
// Shows raw number: 50
```

### Currency Format Example

```tsx
<SliderComponent
  id="currency"
  type="Range"
  value={[100, 900]}
  min={0}
  max={1000}
  tooltip={{
    isVisible: true,
    format: 'C0'  // Display as currency
  }}
/>
```

Displays: `$100 - $900`

### Percentage Format Example

```tsx
<SliderComponent
  id="percentage"
  type="MinRange"
  value={0.75}
  min={0}
  max={1}
  step={0.01}
  tooltip={{
    isVisible: true,
    format: 'P0'
  }}
/>
```

Displays: `75%`

## Best Practices

### Tooltip + Ticks Guidelines

1. **Always visible values:** Use `showOn: 'Always'` for important values
2. **Form inputs:** Use `showOn: 'Focus'` to reduce visual clutter
3. **Scale display:** Include ticks for large ranges (0-1000)
4. **Dense ranges:** Skip ticks for small ranges (0-10)
5. **Mobile:** Place tooltips on top (Before) to avoid cutoff

### Common Patterns

| Pattern | Tooltip | Ticks | Use Case |
|---------|---------|-------|----------|
| **Minimal** | Focus only | None | Form input |
| **Standard** | Always | Major only | Dashboard |
| **Detailed** | Always | Major + Minor | Analytics |
| **Clean** | Always visible | None | Showcase/demo |

## Troubleshooting

### Tooltip Not Showing

**Problem:** `tooltip={{ isVisible: true }}` doesn't display

**Solution:** Check `showOn` property:
```tsx
tooltip={{
  isVisible: true,
  showOn: 'Always'  // Force always visible
}}
```

### Ticks Not Displaying

**Problem:** Configured ticks don't appear

**Solution:** Ensure `largeStep` divides evenly:
```tsx
// ✅ Works: 100 ÷ 20 = 5 ticks
largeStep: 20

// ❌ Confusing: 100 ÷ 30 = 3.33... ticks
largeStep: 30
```

### Format String Not Working

**Problem:** Format like `'C2'` doesn't format value

**Solution:** May need custom event handler:
```tsx
function tooltipChangeHandler(args: SliderTooltipEventArgs) {
  args.text = '$' + args.value;
}

<SliderComponent tooltipChange={tooltipChangeHandler.bind(this) as any} />
```

## Next Steps

1. Configure appropriate tooltip visibility for your use case
2. Add ticks if showing a scale helps users
3. Consider formatting for special value types (currency, percentage)
4. Review [styling.md](styling.md) to customize appearance
5. Test keyboard navigation in [accessibility.md](accessibility.md)
