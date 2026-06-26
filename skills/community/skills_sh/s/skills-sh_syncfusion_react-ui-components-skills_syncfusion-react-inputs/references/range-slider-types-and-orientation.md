# Types and Orientation

## Table of Contents
- [Slider Types Overview](#slider-types-overview)
- [Default Type](#default-type)
- [MinRange Type](#minrange-type)
- [Range Type](#range-type)
- [Type Comparison](#type-comparison)
- [Orientation](#orientation)
- [Horizontal Slider](#horizontal-slider)
- [Vertical Slider](#vertical-slider)
- [Combining Types and Orientation](#combining-types-and-orientation)

## Slider Types Overview

The RangeSlider component supports three types, each with different handle counts and fill behaviors:

| Type | Handles | Fill | Use Case |
|------|---------|------|----------|
| **Default** | 1 | No | Simple single value selection |
| **MinRange** | 1 | Yes | Progress/level indicator with visual fill |
| **Range** | 2 | Yes | Min/max range selection |

## Default Type

The Default type provides a simple single-handle slider for selecting one value within a range.

### Characteristics

- **Single handle:** One draggable point on the track
- **No fill:** No colored shadow or fill area
- **Use:** Simple numeric selection (age, quantity, rating)

### Basic Example

```tsx
import React, { useState } from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';

function DefaultSliderExample() {
  const [value, setValue] = useState(30);

  return (
    <div>
      <h3>Age Selector</h3>
      <p>Selected Age: {value}</p>
      <SliderComponent
        id="age-slider"
        type="Default"
        value={value}
        change={(e) => setValue(e.value as number)}
        min={18}
        max={80}
        step={1}
      />
    </div>
  );
}

export default DefaultSliderExample;
```

### Common Patterns

**Quantity Selector:**
```tsx
<SliderComponent
  id="quantity"
  type="Default"
  value={1}
  min={1}
  max={100}
  step={1}
  tooltip={{ isVisible: true }}
/>
```

**Volume Control:**
```tsx
<SliderComponent
  id="volume"
  type="Default"
  value={50}
  min={0}
  max={100}
  step={5}
  tooltip={{
    isVisible: true,
    placement: 'Before'
  }}
/>
```

## MinRange Type

The MinRange type uses a single handle with a colored fill from the start (min) value to the current handle position.

### Characteristics

- **Single handle:** One draggable point
- **Fill from min:** Colored shadow/fill from minimum to handle position
- **Visual feedback:** Shows progress or level clearly
- **Use:** Progress bars, level indicators, completion percentage

### Basic Example

```tsx
import React, { useState } from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';

function MinRangeExample() {
  const [progress, setProgress] = useState(40);

  return (
    <div>
      <h3>Download Progress</h3>
      <p>Progress: {progress}%</p>
      <SliderComponent
        id="progress-slider"
        type="MinRange"
        value={progress}
        change={(e) => setProgress(e.value as number)}
        min={0}
        max={100}
        step={1}
        tooltip={{ isVisible: true }}
      />
    </div>
  );
}

export default MinRangeExample;
```

### Visual Difference

```
Default Slider:
|●----- No fill --------|

MinRange Slider:
|■■■●----- Fill to handle --------|
  ↑ colored fill from min

Range Slider:
|---○■■■■■■●-----| Two handles, fill between
    ↑       ↑
```

### Common Patterns

**Task Completion Level:**
```tsx
<SliderComponent
  id="completion"
  type="MinRange"
  value={75}
  min={0}
  max={100}
  step={5}
  tooltip={{
    isVisible: true,
    format: 'P0'  // Display as percentage
  }}
/>
```

**Brightness Level:**
```tsx
<SliderComponent
  id="brightness"
  type="MinRange"
  value={70}
  min={0}
  max={100}
  step={10}
/>
```

**Storage Usage:**
```tsx
<SliderComponent
  id="storage"
  type="MinRange"
  value={65}  // 65GB used
  min={0}
  max={256}
  step={5}
  tooltip={{ isVisible: true }}
/>
```

## Range Type

The Range type provides two handles for selecting a minimum and maximum value range.

### Characteristics

- **Two handles:** Start and end draggable points
- **Fill between handles:** Colored fill between the two selected values
- **Use:** Price ranges, date ranges, score ranges, any min-max selection

### Basic Example

```tsx
import React, { useState } from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';

function RangeSliderExample() {
  const [priceRange, setPriceRange] = useState([100, 500]);

  return (
    <div>
      <h3>Price Range Filter</h3>
      <p>Price: ${priceRange[0]} - ${priceRange[1]}</p>
      <SliderComponent
        id="price-range"
        type="Range"
        value={priceRange}
        change={(e) => setPriceRange(e.value as number[])}
        min={0}
        max={1000}
        step={10}
        tooltip={{ isVisible: true }}
      />
    </div>
  );
}

export default RangeSliderExample;
```

### Handle Behavior

**First Handle (Start):** Restricted by max value of first handle and min value of second handle

**Second Handle (End):** Restricted by min value of second handle and max value of first handle

**Example:**
```tsx
// If first handle at 30, second handle can't go below 30
// If second handle at 70, first handle can't go above 70
<SliderComponent
  id="range"
  type="Range"
  value={[30, 70]}
  min={0}
  max={100}
/>
```

### Common Patterns

**Age Range Filter:**
```tsx
<SliderComponent
  id="age-range"
  type="Range"
  value={[18, 65]}
  min={0}
  max={100}
  step={5}
  tooltip={{ isVisible: true }}
/>
```

**Date Range Selector:**
```tsx
// Note: For actual dates, use DateRangePicker component
// For numeric day range:
<SliderComponent
  id="date-range"
  type="Range"
  value={[1, 30]}
  min={1}
  max={31}
  step={1}
  tooltip={{ isVisible: true }}
/>
```

**Score Range Filter:**
```tsx
<SliderComponent
  id="score-range"
  type="Range"
  value={[3, 5]}
  min={1}
  max={5}
  step={0.5}
  tooltip={{ isVisible: true }}
/>
```

## Type Comparison

### Full Comparison Table

```tsx
// Default - Single value, no fill
<SliderComponent
  id="default"
  type="Default"
  value={50}
  tooltip={{ isVisible: true }}
/>

// MinRange - Single value with fill from min
<SliderComponent
  id="minrange"
  type="MinRange"
  value={50}
  tooltip={{ isVisible: true }}
/>

// Range - Two values with fill between
<SliderComponent
  id="range"
  type="Range"
  value={[30, 70]}
  tooltip={{ isVisible: true }}
/>
```

### When to Use Each Type

**Use Default when:**
- Selecting a single, independent value
- No need to show progress or level
- Simple input (age, quantity, rating)
- UI space is limited to single handle

**Use MinRange when:**
- Need visual progress/level indicator
- Single value but with context (progress %, completion)
- Want fill from minimum to selection
- Similar use case to progress bar

**Use Range when:**
- Selecting min and max values
- Filtering by range (prices, dates, scores)
- Need two correlated values
- Show range as interval on track

## Orientation

### Horizontal Slider

Default orientation - slider displays left-to-right.

```tsx
<SliderComponent
  id="horizontal"
  value={50}
  orientation="Horizontal"
  // or omit, as Horizontal is default
/>
```

**Good for:**
- Standard layouts
- Desktop/tablet interfaces
- Wide containers

### Vertical Slider

Display slider top-to-bottom for space-constrained layouts.

```tsx
<div style={{ height: '400px', width: '100px' }}>
  <SliderComponent
    id="vertical"
    value={50}
    orientation="Vertical"
  />
</div>
```

**Important:** Wrap vertical slider in a container with defined `height`. Otherwise, slider won't have space to render.

### Vertical Slider Example

```tsx
import React, { useState } from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';

function VerticalSliderExample() {
  const [volume, setVolume] = useState(50);

  return (
    <div style={{ display: 'flex', gap: '40px', padding: '20px' }}>
      {/* Horizontal */}
      <div>
        <h3>Horizontal</h3>
        <SliderComponent
          id="horizontal"
          value={volume}
          change={(e) => setVolume(e.value as number)}
        />
      </div>

      {/* Vertical */}
      <div style={{ height: '300px' }}>
        <h3>Vertical</h3>
        <SliderComponent
          id="vertical"
          value={volume}
          change={(e) => setVolume(e.value as number)}
          orientation="Vertical"
        />
      </div>
    </div>
  );
}

export default VerticalSliderExample;
```

### Keyboard Behavior

**Horizontal:**
- Right Arrow: Increase value
- Left Arrow: Decrease value

**Vertical:**
- Up Arrow: Increase value
- Down Arrow: Decrease value
- Home/End: Move to min/max

## Combining Types and Orientation

### All Combinations Example

```tsx
import React from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';

function AllCombinations() {
  return (
    <div style={{ padding: '20px' }}>
      <div style={{ marginBottom: '30px' }}>
        <h3>Horizontal Sliders</h3>
        <p>Default</p>
        <SliderComponent id="h-default" type="Default" value={40} />
        
        <p>MinRange</p>
        <SliderComponent id="h-minrange" type="MinRange" value={40} />
        
        <p>Range</p>
        <SliderComponent id="h-range" type="Range" value={[30, 70]} />
      </div>

      <div style={{ display: 'flex', gap: '50px' }}>
        <div style={{ height: '300px' }}>
          <h3>Vertical Default</h3>
          <SliderComponent
            id="v-default"
            type="Default"
            value={40}
            orientation="Vertical"
          />
        </div>

        <div style={{ height: '300px' }}>
          <h3>Vertical MinRange</h3>
          <SliderComponent
            id="v-minrange"
            type="MinRange"
            value={40}
            orientation="Vertical"
          />
        </div>

        <div style={{ height: '300px' }}>
          <h3>Vertical Range</h3>
          <SliderComponent
            id="v-range"
            type="Range"
            value={[30, 70]}
            orientation="Vertical"
          />
        </div>
      </div>
    </div>
  );
}

export default AllCombinations;
```

### Recommendations

- **Desktop:** Use horizontal orientation (standard, familiar)
- **Mobile:** Consider vertical for space efficiency
- **Type selection:** Choose based on value count (1 vs 2) and visual feedback needs
- **Space:** Vertical sliders need at least 200px height to display properly

## Common Pitfalls

### Forgetting Container Height for Vertical

**❌ This won't work:**
```tsx
<SliderComponent orientation="Vertical" />
```

**✅ Do this instead:**
```tsx
<div style={{ height: '300px' }}>
  <SliderComponent orientation="Vertical" />
</div>
```

### Range Type with Single Value

**❌ Incorrect:**
```tsx
<SliderComponent type="Range" value={50} />  // Should be [50, 50]
```

**✅ Correct:**
```tsx
<SliderComponent type="Range" value={[30, 70]} />
```

### Confusing MinRange with Range

**MinRange = progress:** Shows fill from min to handle
**Range = interval:** Shows fill between two handles

## Next Steps

1. Choose appropriate type for your use case
2. Add tooltips from [tooltips-and-ticks.md](tooltips-and-ticks.md)
3. Configure limits if needed from [formatting-and-limits.md](formatting-and-limits.md)
4. Style with [styling.md](styling.md)
5. Test accessibility with [accessibility.md](accessibility.md)
