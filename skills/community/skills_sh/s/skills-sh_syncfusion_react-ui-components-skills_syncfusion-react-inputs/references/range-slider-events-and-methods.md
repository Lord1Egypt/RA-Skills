````markdown
# Events and Methods

## Table of Contents
- [Events Overview](#events-overview)
- [change Event](#change-event)
- [changed Event](#changed-event)
- [created Event](#created-event)
- [renderingTicks Event](#renderingticks-event)
- [renderedTicks Event](#renderedticks-event)
- [tooltipChange Event](#tooltipchange-event)
- [Methods Overview](#methods-overview)
- [reposition Method](#reposition-method)
- [destroy Method](#destroy-method)
- [Using ref for Programmatic Control](#using-ref-for-programmatic-control)
- [Common Patterns](#common-patterns)

---

## Events Overview

The `SliderComponent` fires these events. All events are bound via JSX props using camelCase names.

| Event | Prop Name | Fires When | Args Interface |
|-------|-----------|------------|----------------|
| `change` | `change` | Value changes **while** dragging | `SliderChangeEventArgs` |
| `changed` | `changed` | Drag complete (thumb released) | `SliderChangeEventArgs` |
| `created` | `created` | Component first rendered | `Event` (Object) |
| `renderingTicks` | `renderingTicks` | Each tick is being rendered | `SliderTickEventArgs` |
| `renderedTicks` | `renderedTicks` | All ticks are rendered | `SliderTickRenderedEventArgs` |
| `tooltipChange` | `tooltipChange` | Tooltip value is about to show | `SliderTooltipEventArgs` |

> **⚠️ Important:** Do NOT use `onChange` (that is the native React `<input>` prop). Use `change` and `changed` directly on `SliderComponent`.

---

## change Event

**Prop:** `change`  
**Args:** `SliderChangeEventArgs`  
**Fires:** Continuously while the user is dragging the slider thumb. Use this for real-time feedback.

### SliderChangeEventArgs Properties

| Property | Type | Description |
|----------|------|-------------|
| `value` | `number \| number[]` | Current slider value(s) |
| `previousValue` | `number \| number[]` | Value before this change |
| `action` | `string` | Action applied (e.g., `'SliderMove'`) |
| `isInteracted` | `boolean` | `true` if user interaction; `false` if programmatic |
| `text` | `string` | Formatted tooltip text |

### Basic Example

```tsx
import * as React from 'react';
import { SliderComponent, SliderChangeEventArgs } from '@syncfusion/ej2-react-inputs';

function RealTimeSlider() {
  const [liveValue, setLiveValue] = React.useState(50);

  const handleChange = (args: SliderChangeEventArgs) => {
    setLiveValue(args.value as number);
    console.log('action:', args.action);
    console.log('isInteracted:', args.isInteracted);
  };

  return (
    <div>
      <p aria-live="polite">Live value: {liveValue}</p>
      <SliderComponent
        id="live-slider"
        value={50}
        min={0}
        max={100}
        change={handleChange}
      />
    </div>
  );
}
export default RealTimeSlider;
```

---

## changed Event

**Prop:** `changed`  
**Args:** `SliderChangeEventArgs`  
**Fires:** Once, after the user **releases** the thumb (drag complete). Use this to commit the final value (e.g., API calls, state updates).

### Basic Example

```tsx
import * as React from 'react';
import { SliderComponent, SliderChangeEventArgs } from '@syncfusion/ej2-react-inputs';

function CommitSlider() {
  const [committedValue, setCommittedValue] = React.useState<number | number[]>(50);

  const handleChanged = (args: SliderChangeEventArgs) => {
    setCommittedValue(args.value);
    console.log('Final value committed:', args.value);
    // Safe to call API here — fires only once per drag
  };

  return (
    <div>
      <p>Committed: {JSON.stringify(committedValue)}</p>
      <SliderComponent
        id="commit-slider"
        type="Range"
        value={[20, 80]}
        min={0}
        max={100}
        changed={handleChanged}
      />
    </div>
  );
}
export default CommitSlider;
```

### change vs changed: When to Use Each

| Use Case | Event to Use |
|----------|-------------|
| Update display label while dragging | `change` |
| Submit form on final selection | `changed` |
| Make API call on value change | `changed` |
| Animate based on current value | `change` |
| Persist slider value to state | Either (`changed` preferred) |

---

## created Event

**Prop:** `created`  
**Args:** `Event` (generic Object)  
**Fires:** Once, after the slider has been fully rendered in the DOM.

### Basic Example

```tsx
import * as React from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';

function SliderWithCreated() {
  const sliderRef = React.useRef<SliderComponent>(null);

  const handleCreated = () => {
    console.log('Slider is ready and in the DOM');
    // Safe to access DOM elements here
    const track = document.getElementById('init-slider')?.querySelector('.e-range');
    console.log('Track element:', track);
  };

  return (
    <SliderComponent
      ref={sliderRef}
      id="init-slider"
      value={30}
      created={handleCreated}
    />
  );
}
export default SliderWithCreated;
```

---

## renderingTicks Event

**Prop:** `renderingTicks`  
**Args:** `SliderTickEventArgs`  
**Fires:** For each tick element **while it is being rendered**. Mutate `args.text` to replace the tick label.

### SliderTickEventArgs Properties

| Property | Type | Description |
|----------|------|-------------|
| `value` | `number` | Numeric value of this tick |
| `text` | `string` | Tick label text — **mutable** (override to customize) |
| `tickElement` | `Element` | The DOM element being rendered |

### Custom Tick Labels (Months)

```tsx
import * as React from 'react';
import { SliderComponent, SliderTickEventArgs, TicksDataModel } from '@syncfusion/ej2-react-inputs';

function MonthSlider() {
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  const ticks: TicksDataModel = { placement: 'After', largeStep: 1 };

  const handleRenderingTicks = (args: SliderTickEventArgs) => {
    // args.value is 1–12, map to month name
    args.text = months[Number(args.value) - 1];
  };

  return (
    <SliderComponent
      id="month-slider"
      min={1}
      max={12}
      value={6}
      step={1}
      ticks={ticks}
      renderingTicks={handleRenderingTicks}
    />
  );
}
export default MonthSlider;
```

### Custom Tick Labels (Date Values)

```tsx
import * as React from 'react';
import { SliderComponent, SliderTickEventArgs, TicksDataModel } from '@syncfusion/ej2-react-inputs';

function DateSlider() {
  const min = new Date('2024-01-01').getTime();
  const max = new Date('2024-12-31').getTime();
  const step = 24 * 60 * 60 * 1000 * 30;  // ~30 days in ms

  const ticks: TicksDataModel = { placement: 'After', largeStep: step };

  const handleRenderingTicks = (args: SliderTickEventArgs) => {
    const date = new Date(Number(args.value));
    args.text = date.toLocaleDateString('en-US', { month: 'short' });
  };

  return (
    <SliderComponent
      id="date-slider"
      min={min}
      max={max}
      step={step}
      value={min}
      ticks={ticks}
      renderingTicks={handleRenderingTicks}
    />
  );
}
export default DateSlider;
```

---

## renderedTicks Event

**Prop:** `renderedTicks`  
**Args:** `SliderTickRenderedEventArgs`  
**Fires:** Once, after **all** tick elements have been rendered. Use this to post-process tick DOM (e.g., replace text, add icons).

### SliderTickRenderedEventArgs Properties

| Property | Type | Description |
|----------|------|-------------|
| `ticksWrapper` | `HTMLElement` | The `<ul>` container wrapping all tick `<li>` elements |
| `tickElements` | `HTMLElement[]` | Array of all rendered tick `<li>` elements |

### Add Labels to Large Ticks

```tsx
import * as React from 'react';
import {
  SliderComponent,
  SliderTickRenderedEventArgs,
  TicksDataModel
} from '@syncfusion/ej2-react-inputs';

function LabeledTickSlider() {
  const ticks: TicksDataModel = { placement: 'Both', largeStep: 20, smallStep: 5 };
  const labels = ['Very Poor', 'Poor', 'Average', 'Good', 'Very Good', 'Excellent'];

  const handleRenderedTicks = (args: SliderTickRenderedEventArgs) => {
    const largeTicks = args.ticksWrapper.getElementsByClassName('e-large');
    Array.from(largeTicks).forEach((tick, i) => {
      const bottomLabel = tick.querySelectorAll('.e-tick-both')[1] as HTMLElement;
      if (bottomLabel && labels[i]) {
        bottomLabel.innerText = labels[i];
      }
    });
  };

  return (
    <SliderComponent
      id="labeled-slider"
      type="MinRange"
      value={60}
      min={0}
      max={100}
      step={1}
      ticks={ticks}
      renderedTicks={handleRenderedTicks}
    />
  );
}
export default LabeledTickSlider;
```

---

## tooltipChange Event

**Prop:** `tooltipChange`  
**Args:** `SliderTooltipEventArgs`  
**Fires:** Before the tooltip content is rendered/updated. Mutate `args.text` to customize the tooltip display text.

### SliderTooltipEventArgs Properties

| Property | Type | Description |
|----------|------|-------------|
| `value` | `number \| number[]` | Current slider value(s) |
| `text` | `string` | Tooltip display text — **mutable** (override to customize) |

### Custom Tooltip Text

```tsx
import * as React from 'react';
import { SliderComponent, SliderTooltipEventArgs, TooltipDataModel } from '@syncfusion/ej2-react-inputs';

function CustomTooltipSlider() {
  const tooltip: TooltipDataModel = { isVisible: true, placement: 'Before', showOn: 'Always' };

  const handleTooltipChange = (args: SliderTooltipEventArgs) => {
    args.text = `${args.value}°C`;   // Append unit
  };

  return (
    <SliderComponent
      id="temp-slider"
      value={25}
      min={-10}
      max={50}
      tooltip={tooltip}
      tooltipChange={handleTooltipChange}
    />
  );
}
export default CustomTooltipSlider;
```

### Date Tooltip

```tsx
function DateTooltipSlider() {
  const min = new Date('2024-01-01').getTime();
  const max = new Date('2024-12-31').getTime();
  const step = 86400000;  // 1 day in ms

  const tooltip: TooltipDataModel = { isVisible: true, showOn: 'Always' };

  const handleTooltipChange = (args: SliderTooltipEventArgs) => {
    const date = new Date(Number(args.value));
    args.text = date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  return (
    <SliderComponent
      id="date-tooltip-slider"
      min={min}
      max={max}
      step={step}
      value={min}
      tooltip={tooltip}
      tooltipChange={handleTooltipChange}
    />
  );
}
```

### Range Tooltip Customization

For `type="Range"`, `args.value` is `number[]`:

```tsx
const handleTooltipChange = (args: SliderTooltipEventArgs) => {
  if (Array.isArray(args.value)) {
    args.text = `$${args.value[0]} – $${args.value[1]}`;
  } else {
    args.text = `$${args.value}`;
  }
};
```

---

## Methods Overview

| Method | Returns | Description |
|--------|---------|-------------|
| `reposition()` | `void` | Recalculates and repositions the slider |
| `destroy()` | `void` | Removes slider from DOM and unbinds events |

---

## reposition Method

**Signature:** `reposition(): void`

Call `reposition()` after the slider's parent container changes size (e.g., a hidden tab becomes visible, a modal opens, a sidebar expands).

### Example

```tsx
import * as React from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';

function RepositionExample() {
  const sliderRef = React.useRef<SliderComponent>(null);
  const [visible, setVisible] = React.useState(false);

  const handleShow = () => {
    setVisible(true);
    // After state update and DOM render, reposition the slider
    setTimeout(() => {
      sliderRef.current?.reposition();
    }, 50);
  };

  return (
    <div>
      <button onClick={handleShow}>Show Slider Panel</button>
      {visible && (
        <div style={{ width: '400px', padding: '20px' }}>
          <SliderComponent
            ref={sliderRef}
            id="reposition-slider"
            value={50}
          />
        </div>
      )}
    </div>
  );
}
export default RepositionExample;
```

### When to Call reposition

- Tab panel tab becomes active
- Accordion section expands
- Modal/dialog opens containing a slider
- Parent container width changes via CSS
- Responsive layout breakpoint triggers

---

## destroy Method

**Signature:** `destroy(): void`

Removes the slider from the DOM and unbinds all event listeners and internal references.

### Example

```tsx
import * as React from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';

function DestroyExample() {
  const sliderRef = React.useRef<SliderComponent>(null);
  const [destroyed, setDestroyed] = React.useState(false);

  const handleDestroy = () => {
    sliderRef.current?.destroy();
    setDestroyed(true);
  };

  return (
    <div>
      {!destroyed && (
        <SliderComponent
          ref={sliderRef}
          id="destroy-slider"
          value={50}
        />
      )}
      <button onClick={handleDestroy} disabled={destroyed}>
        {destroyed ? 'Destroyed' : 'Destroy Slider'}
      </button>
    </div>
  );
}
export default DestroyExample;
```

---

## Using ref for Programmatic Control

Access `SliderComponent` instance methods via React `ref`:

```tsx
import * as React from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';

function ProgrammaticSlider() {
  const sliderRef = React.useRef<SliderComponent>(null);

  // Trigger reposition when parent layout changes
  const handleResize = () => {
    sliderRef.current?.reposition();
  };

  // Clean up when done
  const handleCleanup = () => {
    sliderRef.current?.destroy();
  };

  return (
    <div>
      <SliderComponent
        ref={sliderRef}
        id="prog-slider"
        value={50}
        min={0}
        max={100}
      />
      <button onClick={handleResize}>Reposition</button>
      <button onClick={handleCleanup}>Destroy</button>
    </div>
  );
}
export default ProgrammaticSlider;
```

---

## Common Patterns

### Pattern 1: Complete Event Handling

```tsx
import * as React from 'react';
import {
  SliderComponent,
  SliderChangeEventArgs,
  SliderTickEventArgs,
  SliderTooltipEventArgs,
  TicksDataModel,
  TooltipDataModel
} from '@syncfusion/ej2-react-inputs';

function FullEventSlider() {
  const [liveDisplay, setLiveDisplay] = React.useState(50);
  const [committed, setCommitted] = React.useState(50);

  const ticks: TicksDataModel = { placement: 'After', largeStep: 10 };
  const tooltip: TooltipDataModel = { isVisible: true, showOn: 'Always' };

  // Fires while dragging — update preview
  const onChange = (args: SliderChangeEventArgs) => {
    setLiveDisplay(args.value as number);
  };

  // Fires on release — commit final value
  const onChanged = (args: SliderChangeEventArgs) => {
    setCommitted(args.value as number);
    // e.g., call an API
    console.log('Saved:', args.value);
  };

  // Fires on init
  const onCreated = () => {
    console.log('Slider ready');
  };

  // Customize each tick
  const onRenderingTicks = (args: SliderTickEventArgs) => {
    if (Number(args.value) === 0)  args.text = 'Min';
    if (Number(args.value) === 100) args.text = 'Max';
  };

  // Customize tooltip text
  const onTooltipChange = (args: SliderTooltipEventArgs) => {
    args.text = `${args.value}%`;
  };

  return (
    <div>
      <p>Preview: {liveDisplay}% | Saved: {committed}%</p>
      <SliderComponent
        id="full-event-slider"
        type="MinRange"
        value={50}
        min={0}
        max={100}
        step={1}
        ticks={ticks}
        tooltip={tooltip}
        change={onChange}
        changed={onChanged}
        created={onCreated}
        renderingTicks={onRenderingTicks}
        tooltipChange={onTooltipChange}
      />
    </div>
  );
}
export default FullEventSlider;
```

### Pattern 2: API Sync on Value Change

```tsx
function ApiSyncSlider() {
  const [value, setValue] = React.useState(50);
  const [saving, setSaving] = React.useState(false);

  const handleChanged = async (args: SliderChangeEventArgs) => {
    const newValue = args.value as number;
    setValue(newValue);
    setSaving(true);
    try {
      // Simulate API call
      await fetch('/api/settings', {
        method: 'POST',
        body: JSON.stringify({ volume: newValue })
      });
    } finally {
      setSaving(false);
    }
  };

  return (
    <div>
      <SliderComponent
        id="api-slider"
        value={value}
        changed={handleChanged}
      />
      {saving && <span>Saving...</span>}
    </div>
  );
}
```

### Pattern 3: Conditional Event Logic

```tsx
function ConditionalSlider() {
  const [rangeValue, setRangeValue] = React.useState([20, 80]);
  const [warning, setWarning] = React.useState('');

  const handleChanged = (args: SliderChangeEventArgs) => {
    const [min, max] = args.value as number[];
    setRangeValue([min, max]);

    // Business logic based on range
    const spread = max - min;
    if (spread < 10) {
      setWarning('Selected range is too narrow (minimum 10 units)');
    } else if (spread > 80) {
      setWarning('Selected range is very wide');
    } else {
      setWarning('');
    }
  };

  return (
    <div>
      <SliderComponent
        id="conditional-slider"
        type="Range"
        value={rangeValue}
        min={0}
        max={100}
        changed={handleChanged}
        tooltip={{ isVisible: true }}
      />
      {warning && <p style={{ color: 'orange' }}>{warning}</p>}
    </div>
  );
}
```

---

## Next Steps

- Check [api-reference.md](api-reference.md) for all event argument interface definitions
- See [tooltips-and-ticks.md](tooltips-and-ticks.md) for combining `renderingTicks` with tooltip formatting
- Review [formatting-and-limits.md](formatting-and-limits.md) for the `tooltipChange` format API
- Read [accessibility.md](accessibility.md) for `aria-live` region patterns with events

````
