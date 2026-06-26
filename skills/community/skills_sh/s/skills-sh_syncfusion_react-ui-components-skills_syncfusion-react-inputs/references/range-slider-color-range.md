````markdown
# Color Range in React Slider

## Table of Contents
- [Overview](#overview)
- [ColorRangeDataModel Interface](#colorrangedatamodel-interface)
- [Basic Color Range Example](#basic-color-range-example)
- [Multi-Zone Color Range](#multi-zone-color-range)
- [Color Range with Range Slider](#color-range-with-range-slider)
- [Dynamic Color Range](#dynamic-color-range)
- [Real-World Patterns](#real-world-patterns)
- [Combining with Other Features](#combining-with-other-features)

## Overview

The `colorRange` property paints different sections of the slider track in distinct colors based on value zones. This is useful for:

- Visualizing risk levels (green/amber/red)
- Showing performance bands (poor/average/good/excellent)
- Indicating temperature zones
- Displaying quality or health metrics

**Import:**
```tsx
import { SliderComponent, ColorRangeDataModel } from '@syncfusion/ej2-react-inputs';
```

---

## ColorRangeDataModel Interface

Each object in the `colorRange` array must have:

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `color` | `string` | Yes | CSS color value (hex, rgb, named, etc.) |
| `start` | `number` | Yes | Starting value of the colored section |
| `end` | `number` | Yes | Ending value of the colored section |

```tsx
const colorRange: ColorRangeDataModel[] = [
  { color: '#ff4040', start: 0,  end: 33  },
  { color: '#ffb300', start: 34, end: 66  },
  { color: '#00c853', start: 67, end: 100 }
];
```

---

## Basic Color Range Example

Three-zone slider (red → amber → green):

```tsx
import * as React from 'react';
import { SliderComponent, ColorRangeDataModel, TooltipDataModel } from '@syncfusion/ej2-react-inputs';

function ColorRangeSlider() {
  const colorRange: ColorRangeDataModel[] = [
    { color: '#ff4040', start: 0,  end: 33  },   // Low — red
    { color: '#ffb300', start: 34, end: 66  },   // Mid — amber
    { color: '#00c853', start: 67, end: 100 }    // High — green
  ];

  const tooltip: TooltipDataModel = { isVisible: true, showOn: 'Always' };

  return (
    <div style={{ padding: '30px' }}>
      <SliderComponent
        id="color-slider"
        type="MinRange"
        value={50}
        min={0}
        max={100}
        colorRange={colorRange}
        tooltip={tooltip}
      />
    </div>
  );
}

export default ColorRangeSlider;
```

---

## Multi-Zone Color Range

Five performance bands:

```tsx
import * as React from 'react';
import { SliderComponent, ColorRangeDataModel } from '@syncfusion/ej2-react-inputs';

function PerformanceBandSlider() {
  const colorRange: ColorRangeDataModel[] = [
    { color: '#d32f2f', start: 0,  end: 19  },   // Very Poor — dark red
    { color: '#f57c00', start: 20, end: 39  },   // Poor — orange
    { color: '#fbc02d', start: 40, end: 59  },   // Average — yellow
    { color: '#388e3c', start: 60, end: 79  },   // Good — green
    { color: '#1565c0', start: 80, end: 100 }    // Excellent — blue
  ];

  const [score, setScore] = React.useState(60);

  function getLabel(val: number): string {
    if (val < 20) return 'Very Poor';
    if (val < 40) return 'Poor';
    if (val < 60) return 'Average';
    if (val < 80) return 'Good';
    return 'Excellent';
  }

  return (
    <div style={{ padding: '30px', maxWidth: 500 }}>
      <p>Score: {score} — {getLabel(score)}</p>
      <SliderComponent
        id="performance-slider"
        type="MinRange"
        value={score}
        min={0}
        max={100}
        step={1}
        colorRange={colorRange}
        tooltip={{ isVisible: true, showOn: 'Always' }}
        changed={(e) => setScore(e.value as number)}
      />
    </div>
  );
}

export default PerformanceBandSlider;
```

---

## Color Range with Range Slider

Apply color zones to a dual-handle `Range` slider:

```tsx
import * as React from 'react';
import { SliderComponent, ColorRangeDataModel } from '@syncfusion/ej2-react-inputs';

function RangeColorSlider() {
  const colorRange: ColorRangeDataModel[] = [
    { color: '#e53935', start: 0,   end: 250  },   // Budget — red
    { color: '#fb8c00', start: 251, end: 500  },   // Mid — orange
    { color: '#43a047', start: 501, end: 1000 }    // Premium — green
  ];

  const [priceRange, setPriceRange] = React.useState<number[]>([200, 700]);

  return (
    <div style={{ padding: '30px', maxWidth: 600 }}>
      <p>Price: ${priceRange[0]} – ${priceRange[1]}</p>
      <SliderComponent
        id="price-color-slider"
        type="Range"
        value={priceRange}
        min={0}
        max={1000}
        step={10}
        colorRange={colorRange}
        tooltip={{ isVisible: true, showOn: 'Always', format: 'C0' }}
        changed={(e) => setPriceRange(e.value as number[])}
      />
    </div>
  );
}

export default RangeColorSlider;
```

---

## Dynamic Color Range

Update color zones at runtime based on data:

```tsx
import * as React from 'react';
import { SliderComponent, ColorRangeDataModel } from '@syncfusion/ej2-react-inputs';

interface Zone {
  label: string;
  color: string;
  start: number;
  end: number;
}

function DynamicColorSlider() {
  const zones: Zone[] = [
    { label: 'Cold',   color: '#2196f3', start: -20, end: 0   },
    { label: 'Cool',   color: '#00bcd4', start: 1,   end: 15  },
    { label: 'Warm',   color: '#ff9800', start: 16,  end: 25  },
    { label: 'Hot',    color: '#f44336', start: 26,  end: 40  }
  ];

  const colorRange: ColorRangeDataModel[] = zones.map(z => ({
    color: z.color,
    start: z.start,
    end: z.end
  }));

  const [temp, setTemp] = React.useState(20);
  const currentZone = zones.find(z => temp >= z.start && temp <= z.end);

  return (
    <div style={{ padding: '30px', maxWidth: 500 }}>
      <p>Temperature: {temp}°C — {currentZone?.label ?? ''}</p>
      <SliderComponent
        id="temp-slider"
        type="MinRange"
        value={temp}
        min={-20}
        max={40}
        step={1}
        colorRange={colorRange}
        tooltip={{ isVisible: true, showOn: 'Always' }}
        changed={(e) => setTemp(e.value as number)}
      />
    </div>
  );
}

export default DynamicColorSlider;
```

---

## Real-World Patterns

### Pattern 1: Battery Level Indicator

```tsx
const batteryColors: ColorRangeDataModel[] = [
  { color: '#d32f2f', start: 0,  end: 20  },   // Critical — red
  { color: '#f57c00', start: 21, end: 50  },   // Low — orange
  { color: '#388e3c', start: 51, end: 100 }    // Good — green
];

<SliderComponent
  id="battery"
  type="MinRange"
  value={batteryLevel}
  min={0}
  max={100}
  colorRange={batteryColors}
  tooltip={{ isVisible: true, showOn: 'Always' }}
  readonly={true}   // Display only
/>
```

### Pattern 2: Risk Assessment Slider

```tsx
const riskColors: ColorRangeDataModel[] = [
  { color: '#4caf50', start: 0,  end: 30  },   // Low risk
  { color: '#ff9800', start: 31, end: 60  },   // Medium risk
  { color: '#f44336', start: 61, end: 100 }    // High risk
];

<SliderComponent
  id="risk-slider"
  type="MinRange"
  value={riskScore}
  min={0}
  max={100}
  colorRange={riskColors}
  ticks={{ placement: 'After', largeStep: 10 }}
  tooltip={{ isVisible: true, showOn: 'Always' }}
  changed={(e) => setRiskScore(e.value as number)}
/>
```

### Pattern 3: Score Distribution Range

```tsx
const scoreColors: ColorRangeDataModel[] = [
  { color: '#f44336', start: 0,  end: 49  },   // Fail
  { color: '#ff9800', start: 50, end: 59  },   // Pass
  { color: '#4caf50', start: 60, end: 74  },   // Good
  { color: '#2196f3', start: 75, end: 100 }    // Excellent
];

<SliderComponent
  id="score-slider"
  type="Range"
  value={[50, 80]}
  min={0}
  max={100}
  colorRange={scoreColors}
  tooltip={{ isVisible: true }}
/>
```

---

## Combining with Other Features

### Color Range + Ticks + Tooltip

```tsx
import * as React from 'react';
import {
  SliderComponent,
  ColorRangeDataModel,
  TicksDataModel,
  TooltipDataModel
} from '@syncfusion/ej2-react-inputs';

function FullFeaturedColorSlider() {
  const colorRange: ColorRangeDataModel[] = [
    { color: '#ff5252', start: 0,  end: 33  },
    { color: '#ffd740', start: 34, end: 66  },
    { color: '#69f0ae', start: 67, end: 100 }
  ];

  const ticks: TicksDataModel = {
    placement: 'After',
    largeStep: 10,
    smallStep: 5,
    showSmallTicks: false
  };

  const tooltip: TooltipDataModel = {
    isVisible: true,
    placement: 'Before',
    showOn: 'Always'
  };

  return (
    <SliderComponent
      id="featured-slider"
      type="MinRange"
      value={50}
      min={0}
      max={100}
      step={1}
      colorRange={colorRange}
      ticks={ticks}
      tooltip={tooltip}
    />
  );
}

export default FullFeaturedColorSlider;
```

### Color Range + Limits

```tsx
const colorRange: ColorRangeDataModel[] = [
  { color: '#43a047', start: 0,  end: 50  },
  { color: '#e53935', start: 51, end: 100 }
];

<SliderComponent
  id="limited-color"
  type="MinRange"
  value={30}
  min={0}
  max={100}
  colorRange={colorRange}
  limits={{ enabled: true, minStart: 10, minEnd: 70 }}
  tooltip={{ isVisible: true }}
/>
```

---

## Important Notes

1. **Zones should not overlap:** Each `start`–`end` range should be mutually exclusive for predictable rendering
2. **Complete coverage is optional:** You do not need to cover the entire slider range with color zones; uncovered sections use the default track color
3. **Works with all slider types:** `Default`, `MinRange`, and `Range` all support `colorRange`
4. **CSS color values accepted:** Use hex (`#ff4040`), rgb (`rgb(255, 64, 64)`), or named colors (`'red'`)
5. **Combine with `readonly` for display:** Use `readonly={true}` to show a color-coded indicator without interaction

## Next Steps

- See [api-reference.md](api-reference.md) for the `ColorRangeDataModel` interface spec
- Combine with [tooltips-and-ticks.md](tooltips-and-ticks.md) for enhanced visual feedback
- Add [formatting-and-limits.md](formatting-and-limits.md) to restrict movement within color zones
- Review [styling.md](styling.md) for further visual customization

````
