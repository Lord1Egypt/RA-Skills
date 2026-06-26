````markdown
# Slider API Reference

Authoritative API reference for the Syncfusion React Slider component (`SliderComponent`), based on the official documentation at:  
https://ej2.syncfusion.com/react/documentation/api/slider/index-default

## Table of Contents
- [Properties](#properties)
- [Methods](#methods)
- [Events](#events)
- [Interface: TicksDataModel](#interface-ticksdatamodel)
- [Interface: TooltipDataModel](#interface-tooltipdatamodel)
- [Interface: LimitDataModel](#interface-limitdatamodel)
- [Interface: ColorRangeDataModel](#interface-colorrangedatamodel)
- [Interface: SliderChangeEventArgs](#interface-sliderchangeeventargs)
- [Interface: SliderTickEventArgs](#interface-slidertickeventargs)
- [Interface: SliderTickRenderedEventArgs](#interface-slidertickrenderedeventargs)
- [Interface: SliderTooltipEventArgs](#interface-slidertooltipeventargs)
- [Enum: SliderType](#enum-slidertype)
- [Enum: SliderOrientation](#enum-sliderorientation)
- [Complete Working Example](#complete-working-example)

---

## Properties

These are the **only** officially documented properties on `SliderComponent`.

### colorRange
**Type:** `ColorRangeDataModel[]`  
**Default:** `[]`

Specifies an array of color range objects that paint different sections of the slider track in distinct colors based on value ranges.

```tsx
import * as React from 'react';
import { SliderComponent, ColorRangeDataModel } from '@syncfusion/ej2-react-inputs';

export default class App extends React.Component<{}, {}> {
  public colorRange: ColorRangeDataModel[] = [
    { color: '#ff0000', start: 0,  end: 33 },
    { color: '#ffff00', start: 34, end: 66 },
    { color: '#00ff00', start: 67, end: 100 }
  ];
  render() {
    return (
      <SliderComponent id="slider" value={30} colorRange={this.colorRange} />
    );
  }
}
```

Defaults to `[]`

---

### cssClass
**Type:** `string`  
**Default:** `''`

Specifies custom CSS class names (space-separated) added to the root slider element for bespoke styling.

```tsx
<SliderComponent id="slider" value={30} cssClass="custom-slider" />
```

---

### customValues
**Type:** `string[] | number[]`  
**Default:** `null`

Specifies an array of custom values. When set, `min`, `max`, and `step` are ignored; the slider uses these values as its scale.

```tsx
<SliderComponent
  id="size-slider"
  customValues={['XS', 'S', 'M', 'L', 'XL', 'XXL']}
  value="M"
/>
```

---

### enableAnimation
**Type:** `boolean`  
**Default:** `true`

Enables or disables the animation when dragging the slider thumb.

```tsx
<SliderComponent id="slider" value={30} enableAnimation={false} />
```

---

### enableHtmlSanitizer
**Type:** `boolean`  
**Default:** `true`

When `true`, sanitizes untrusted HTML strings before rendering them. Set to `false` only when you fully control the content.

```tsx
<SliderComponent id="slider" value={30} enableHtmlSanitizer={true} />
```

---

### enablePersistence
**Type:** `boolean`  
**Default:** `false`

Enables persistence of the component's state between page reloads (saved in browser storage).

```tsx
<SliderComponent id="slider" value={30} enablePersistence={true} />
```

---

### enableRtl
**Type:** `boolean`  
**Default:** `false`

Renders the component in right-to-left direction when `true`. Required for RTL/Arabic/Hebrew UI.

```tsx
<SliderComponent id="slider" value={30} enableRtl={true} />
```

---

### enabled
**Type:** `boolean`  
**Default:** `true`

Enables or disables the slider. When `false`, the slider is visible but not interactive.

```tsx
<SliderComponent id="slider" value={30} enabled={false} />
```

---

### limits
**Type:** `LimitDataModel`  
**Default:** `{ enabled: false }`

Specifies the limits within which the slider thumb(s) can move. Refer to [`LimitDataModel`](#interface-limitdatamodel) for properties.

```tsx
<SliderComponent
  id="slider"
  type="MinRange"
  value={30}
  limits={{ enabled: true, minStart: 10, minEnd: 40 }}
/>
```

---

### locale
**Type:** `string`  
**Default:** `''`

Overrides the global culture and localization value for this component. Default global culture is `'en-US'`.

```tsx
<SliderComponent id="slider" value={30} locale="fr-FR" />
```

---

### max
**Type:** `number`  
**Default:** `100`

Gets/Sets the maximum value of the slider.

```tsx
<SliderComponent id="slider" value={50} min={0} max={200} />
```

---

### min
**Type:** `number`  
**Default:** `0`

Gets/Sets the minimum value of the slider.

```tsx
<SliderComponent id="slider" value={50} min={10} max={100} />
```

---

### orientation
**Type:** `SliderOrientation`  
**Default:** `'Horizontal'`

Specifies whether to render the slider in vertical or horizontal orientation.

| Value | Effect |
|-------|--------|
| `'Horizontal'` | Slider renders left-to-right (default) |
| `'Vertical'` | Slider renders bottom-to-top |

```tsx
<div style={{ height: '300px' }}>
  <SliderComponent id="slider" value={50} orientation="Vertical" />
</div>
```

> **Note:** Always wrap a vertical slider in a container with explicit `height`.

---

### readonly
**Type:** `boolean`  
**Default:** `false`

When `true`, renders the slider in read-only mode. The slider displays values but does not respond to user interaction.

```tsx
<SliderComponent id="slider" value={30} readonly={true} />
```

---

### showButtons
**Type:** `boolean`  
**Default:** `false`

Shows increment/decrement buttons at each end of the slider for stepwise value changes.

```tsx
<SliderComponent id="slider" value={30} showButtons={true} />
```

---

### step
**Type:** `number`  
**Default:** `1`

Specifies the step value. The slider value changes by this amount when dragging, pressing arrow keys, or clicking the increment/decrement buttons.

```tsx
<SliderComponent id="slider" value={30} step={5} />
```

---

### ticks
**Type:** `TicksDataModel`  
**Default:** `{ placement: 'before' }`

Configures the tick marks displayed on the slider scale. Refer to [`TicksDataModel`](#interface-ticksdatamodel) for properties.

```tsx
<SliderComponent
  id="slider"
  value={30}
  ticks={{ placement: 'After', largeStep: 20, smallStep: 5, showSmallTicks: true }}
/>
```

---

### tooltip
**Type:** `TooltipDataModel`  
**Default:** `{ placement: 'Before', isVisible: false, showOn: 'Focus', format: null }`

Specifies the visibility and position of the tooltip over the slider element. Refer to [`TooltipDataModel`](#interface-tooltipdatamodel) for properties.

```tsx
<SliderComponent
  id="slider"
  value={30}
  tooltip={{ isVisible: true, placement: 'After', showOn: 'Always' }}
/>
```

---

### type
**Type:** `SliderType`  
**Default:** `'Default'`

Defines the type of slider. See [`SliderType`](#enum-slidertype) for values.

```tsx
import * as React from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  return (
    <div>
      <SliderComponent id="default"  type="Default"  value={30} />
      <SliderComponent id="minrange" type="MinRange" value={30} />
      <SliderComponent id="range"    type="Range"    value={[30, 70]} />
    </div>
  );
}
export default App;
```

---

### value
**Type:** `number | number[]`  
**Default:** `null`

The current value of the slider. Provide a single `number` for `Default`/`MinRange` types; provide `[start, end]` array for `Range` type.

```tsx
{/* Single value */}
<SliderComponent id="single" value={50} />

{/* Range value */}
<SliderComponent id="range" type="Range" value={[20, 80]} />
```

---

### width
**Type:** `number | string`  
**Default:** `null`

Specifies the width of the slider. Accepts CSS dimension values (e.g., `'400px'`, `'100%'`) or plain numbers (treated as pixels).

```tsx
<SliderComponent id="slider" value={50} width="400px" />
```

---

## Methods

These are the **only** officially documented methods on `SliderComponent`.

### destroy

Removes the component from the DOM and detaches all its related event handlers. Also removes attributes and classes.

```tsx
destroy(): void
```

```tsx
import React, { useRef } from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  const sliderRef = useRef<SliderComponent>(null);

  const handleDestroy = () => {
    sliderRef.current?.destroy();
  };

  return (
    <div>
      <SliderComponent ref={sliderRef} id="slider" value={50} />
      <button onClick={handleDestroy}>Destroy Slider</button>
    </div>
  );
}
export default App;
```

---

### reposition

Repositions the slider. Call this after programmatic layout changes (e.g., parent container resized, hidden tab becomes visible).

```tsx
reposition(): void
```

```tsx
import React, { useRef } from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  const sliderRef = useRef<SliderComponent>(null);

  const handleReposition = () => {
    sliderRef.current?.reposition();
  };

  return (
    <div>
      <SliderComponent ref={sliderRef} id="slider" value={50} />
      <button onClick={handleReposition}>Reposition</button>
    </div>
  );
}
export default App;
```

---

## Events

Bind these events in JSX using camelCase prop names.

### change
**Arguments:** `SliderChangeEventArgs`

Fires whenever the slider value changes — **while** dragging the thumb (continuous updates).

```tsx
import * as React from 'react';
import { SliderComponent, SliderChangeEventArgs } from '@syncfusion/ej2-react-inputs';

function App() {
  const handleChange = (args: SliderChangeEventArgs) => {
    console.log('Changing value:', args.value);
    console.log('Previous value:', args.previousValue);
    console.log('Is user interaction:', args.isInteracted);
  };

  return <SliderComponent id="slider" value={30} change={handleChange} />;
}
export default App;
```

---

### changed
**Arguments:** `SliderChangeEventArgs`

Fires when the slider value change is **complete** — after the user releases the thumb. Use this for final value capture.

```tsx
import * as React from 'react';
import { SliderComponent, SliderChangeEventArgs } from '@syncfusion/ej2-react-inputs';

function App() {
  const handleChanged = (args: SliderChangeEventArgs) => {
    console.log('Final value:', args.value);
  };

  return <SliderComponent id="slider" value={30} changed={handleChanged} />;
}
export default App;
```

---

### created
**Arguments:** `Event` (Object)

Fires once, after the slider component has been successfully created and rendered.

```tsx
function App() {
  const handleCreated = () => {
    console.log('Slider is ready');
  };

  return <SliderComponent id="slider" value={30} created={handleCreated} />;
}
```

---

### renderedTicks
**Arguments:** `SliderTickRenderedEventArgs`

Fires after all tick elements have been rendered on the slider. Use this to post-process tick DOM elements (e.g., replace text, add icons).

```tsx
import * as React from 'react';
import { SliderComponent, SliderTickRenderedEventArgs, TicksDataModel } from '@syncfusion/ej2-react-inputs';

function App() {
  const ticks: TicksDataModel = { placement: 'Both', largeStep: 20, smallStep: 5 };

  const handleRenderedTicks = (args: SliderTickRenderedEventArgs) => {
    const largeTicks = args.ticksWrapper.getElementsByClassName('e-large');
    const labels = ['Very Poor', 'Poor', 'Average', 'Good', 'Very Good', 'Excellent'];
    Array.from(largeTicks).forEach((tick, i) => {
      const tickBoth = tick.querySelectorAll('.e-tick-both')[1] as HTMLElement;
      if (tickBoth) tickBoth.innerText = labels[i];
    });
  };

  return (
    <SliderComponent
      id="slider"
      value={[30, 70]}
      ticks={ticks}
      renderedTicks={handleRenderedTicks}
    />
  );
}
export default App;
```

---

### renderingTicks
**Arguments:** `SliderTickEventArgs`

Fires for each tick element **while** it is being rendered. Use this to customize the label text of individual ticks dynamically.

```tsx
import * as React from 'react';
import { SliderComponent, SliderTickEventArgs, TicksDataModel } from '@syncfusion/ej2-react-inputs';

function App() {
  const ticks: TicksDataModel = { placement: 'After', largeStep: 1 };
  const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  const handleRenderingTicks = (args: SliderTickEventArgs) => {
    args.text = days[Number(args.value)];
  };

  return (
    <SliderComponent
      id="slider"
      min={0}
      max={6}
      value={3}
      ticks={ticks}
      renderingTicks={handleRenderingTicks}
    />
  );
}
export default App;
```

---

### tooltipChange
**Arguments:** `SliderTooltipEventArgs`

Fires when the tooltip value is about to be rendered. Use this to customize what text the tooltip displays.

```tsx
import * as React from 'react';
import { SliderComponent, SliderTooltipEventArgs, TooltipDataModel } from '@syncfusion/ej2-react-inputs';

function App() {
  const tooltip: TooltipDataModel = { isVisible: true, placement: 'Before' };

  const handleTooltipChange = (args: SliderTooltipEventArgs) => {
    // Append unit to displayed tooltip text
    args.text = `${args.value}°C`;
  };

  return (
    <SliderComponent
      id="slider"
      value={30}
      tooltip={tooltip}
      tooltipChange={handleTooltipChange}
    />
  );
}
export default App;
```

---

## Interface: TicksDataModel

Properties for the `ticks` prop object.

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `placement` | `'Before' \| 'After' \| 'Both' \| 'None'` | `'Before'` | Position of ticks relative to the track |
| `largeStep` | `number` | — | Interval between major (large) ticks |
| `smallStep` | `number` | — | Interval between minor (small) ticks |
| `showSmallTicks` | `boolean` | `false` | Whether to show minor ticks |
| `format` | `string` | — | Format string for tick labels (e.g. `'C2'`, `'P0'`) |

```tsx
const ticks: TicksDataModel = {
  placement: 'After',
  largeStep: 20,
  smallStep: 5,
  showSmallTicks: true,
  format: 'N0'
};
```

**Placement values:**
- `'Before'` — Ticks above (horizontal) or left of (vertical) the track
- `'After'` — Ticks below (horizontal) or right of (vertical) the track
- `'Both'` — Ticks on both sides of the track
- `'None'` — No ticks rendered

---

## Interface: TooltipDataModel

Properties for the `tooltip` prop object.

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `isVisible` | `boolean` | `false` | Show or hide the tooltip |
| `placement` | `'Before' \| 'After'` | `'Before'` | Position relative to the track |
| `showOn` | `'Always' \| 'Focus' \| 'Click'` | `'Focus'` | When to display the tooltip |
| `format` | `string` | `null` | Format string for tooltip value (e.g. `'C2'`, `'P0'`) |
| `cssClass` | `string` | — | Custom CSS classes on the tooltip element |

```tsx
const tooltip: TooltipDataModel = {
  isVisible: true,
  placement: 'Before',
  showOn: 'Always',
  format: 'C2',
  cssClass: 'custom-tooltip'
};
```

**showOn values:**
- `'Always'` — Tooltip always visible
- `'Focus'` — Tooltip visible when focused or dragging (default)
- `'Click'` — Tooltip visible only when clicking the handle

---

## Interface: LimitDataModel

Properties for the `limits` prop object.

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `enabled` | `boolean` | `false` | Enable or disable limit functionality |
| `minStart` | `number` | — | Minimum position for the first handle |
| `minEnd` | `number` | — | Maximum position for the first handle |
| `maxStart` | `number` | — | Minimum position for the second handle |
| `maxEnd` | `number` | — | Maximum position for the second handle |
| `startHandleFixed` | `boolean` | `false` | Lock (fix) the first handle |
| `endHandleFixed` | `boolean` | `false` | Lock (fix) the second handle |

```tsx
import { LimitDataModel } from '@syncfusion/ej2-react-inputs';

// Single handle limits (Default/MinRange)
const singleLimits: LimitDataModel = {
  enabled: true,
  minStart: 10,
  minEnd: 40
};

// Range limits (Range type — both handles)
const rangeLimits: LimitDataModel = {
  enabled: true,
  minStart: 10,
  minEnd: 40,
  maxStart: 60,
  maxEnd: 90
};

// Lock both handles
const lockedLimits: LimitDataModel = {
  enabled: true,
  startHandleFixed: true,
  endHandleFixed: true
};
```

> **Note:** `maxStart` and `maxEnd` apply to the **second** handle in a Range slider. They have no effect for `Default` or `MinRange` types.

---

## Interface: ColorRangeDataModel

Properties for objects in the `colorRange` prop array.

| Property | Type | Description |
|----------|------|-------------|
| `color` | `string` | CSS color value to paint the track section |
| `start` | `number` | Starting value of the colored section |
| `end` | `number` | Ending value of the colored section |

```tsx
import { ColorRangeDataModel } from '@syncfusion/ej2-react-inputs';

const colorRange: ColorRangeDataModel[] = [
  { color: '#ff4040', start: 0,  end: 25 },   // Red zone
  { color: '#ffb300', start: 26, end: 50 },   // Amber zone
  { color: '#2e7d32', start: 51, end: 100 }   // Green zone
];

<SliderComponent id="slider" value={30} colorRange={colorRange} />
```

---

## Interface: SliderChangeEventArgs

Argument object for `change` and `changed` events.

| Property | Type | Description |
|----------|------|-------------|
| `value` | `number \| number[]` | Current value of the slider |
| `previousValue` | `number \| number[]` | Previous value before the change |
| `action` | `string` | Action applied on the slider (e.g., `'SliderMove'`) |
| `isInteracted` | `boolean` | `true` if triggered by user interaction; `false` if programmatic |
| `text` | `string` | Current formatted text displayed in tooltip |

```tsx
import { SliderChangeEventArgs } from '@syncfusion/ej2-react-inputs';

const handleChange = (args: SliderChangeEventArgs) => {
  console.log('value:', args.value);
  console.log('previousValue:', args.previousValue);
  console.log('action:', args.action);
  console.log('isInteracted:', args.isInteracted);
  console.log('text:', args.text);
};
```

---

## Interface: SliderTickEventArgs

Argument object for the `renderingTicks` event. Fires for each tick during rendering.

| Property | Type | Description |
|----------|------|-------------|
| `value` | `number` | The numeric value of the tick |
| `text` | `string` | The label text displayed on the tick (can be overwritten) |
| `tickElement` | `Element` | The DOM element of the tick |

```tsx
import { SliderTickEventArgs } from '@syncfusion/ej2-react-inputs';

const handleRenderingTicks = (args: SliderTickEventArgs) => {
  // Customize tick label
  args.text = `${args.value} units`;
};
```

---

## Interface: SliderTickRenderedEventArgs

Argument object for the `renderedTicks` event. Fires after all ticks are rendered.

| Property | Type | Description |
|----------|------|-------------|
| `ticksWrapper` | `HTMLElement` | The container `<div>` wrapping all tick elements |
| `tickElements` | `HTMLElement[]` | Array of all rendered tick `<li>` elements |

```tsx
import { SliderTickRenderedEventArgs } from '@syncfusion/ej2-react-inputs';

const handleRenderedTicks = (args: SliderTickRenderedEventArgs) => {
  const largeTicks = args.ticksWrapper.getElementsByClassName('e-large');
  console.log('Total large ticks:', largeTicks.length);
  console.log('All tick elements:', args.tickElements);
};
```

---

## Interface: SliderTooltipEventArgs

Argument object for the `tooltipChange` event.

| Property | Type | Description |
|----------|------|-------------|
| `value` | `number \| number[]` | Current value(s) of the slider |
| `text` | `string` | The text shown in the tooltip (can be overwritten) |

```tsx
import { SliderTooltipEventArgs } from '@syncfusion/ej2-react-inputs';

const handleTooltipChange = (args: SliderTooltipEventArgs) => {
  // Override the tooltip display text
  args.text = `${args.value}%`;
};
```

---

## Enum: SliderType

Valid string values for the `type` property:

| Value | Handles | Fill | Description |
|-------|---------|------|-------------|
| `'Default'` | 1 | None | Simple single value selection (default) |
| `'MinRange'` | 1 | Start to handle | Shows fill from minimum value to current handle |
| `'Range'` | 2 | Between handles | Selects a range with two handles |

```tsx
// Default (single value, no fill)
<SliderComponent id="s1" type="Default" value={30} />

// MinRange (single value, fill from min)
<SliderComponent id="s2" type="MinRange" value={30} />

// Range (two values, fill between)
<SliderComponent id="s3" type="Range" value={[30, 70]} />
```

---

## Enum: SliderOrientation

Valid string values for the `orientation` property:

| Value | Description |
|-------|-------------|
| `'Horizontal'` | Slider renders left-to-right (default) |
| `'Vertical'` | Slider renders bottom-to-top; requires parent container with fixed `height` |

---

## Complete Working Example

A concise reference showing all commonly used properties and events together:

```tsx
import * as React from 'react';
import {
  SliderComponent,
  SliderChangeEventArgs,
  SliderTickEventArgs,
  SliderTooltipEventArgs,
  SliderTickRenderedEventArgs,
  TicksDataModel,
  TooltipDataModel,
  LimitDataModel,
  ColorRangeDataModel
} from '@syncfusion/ej2-react-inputs';

// CSS imports (use one theme)
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-buttons/styles/tailwind3.css';
import '@syncfusion/ej2-popups/styles/tailwind3.css';
import '@syncfusion/ej2-react-inputs/styles/tailwind3.css';

interface State {
  value: number;
  rangeValue: number[];
}

export default class App extends React.Component<{}, State> {
  private sliderRef = React.createRef<SliderComponent>();

  public ticks: TicksDataModel = {
    placement: 'After',
    largeStep: 20,
    smallStep: 5,
    showSmallTicks: true
  };

  public tooltip: TooltipDataModel = {
    isVisible: true,
    placement: 'Before',
    showOn: 'Always',
    format: 'N0'
  };

  public limits: LimitDataModel = {
    enabled: true,
    minStart: 10,
    minEnd: 80
  };

  public colorRange: ColorRangeDataModel[] = [
    { color: '#ff4040', start: 0,  end: 33 },
    { color: '#ffb300', start: 34, end: 66 },
    { color: '#00c853', start: 67, end: 100 }
  ];

  constructor(props: {}) {
    super(props);
    this.state = { value: 40, rangeValue: [20, 80] };
  }

  // Fires while dragging
  onChange = (args: SliderChangeEventArgs) => {
    console.log('Changing:', args.value, '| Previous:', args.previousValue);
  };

  // Fires on drag complete
  onChanged = (args: SliderChangeEventArgs) => {
    if (typeof args.value === 'number') {
      this.setState({ value: args.value });
    } else {
      this.setState({ rangeValue: args.value as number[] });
    }
  };

  // Fires on creation
  onCreated = () => {
    console.log('Slider created');
  };

  // Customize each tick label while rendering
  onRenderingTicks = (args: SliderTickEventArgs) => {
    args.text = `${args.value}u`;
  };

  // Post-process tick DOM after all ticks rendered
  onRenderedTicks = (args: SliderTickRenderedEventArgs) => {
    console.log('Tick wrapper:', args.ticksWrapper);
    console.log('Tick elements count:', args.tickElements.length);
  };

  // Customize tooltip text
  onTooltipChange = (args: SliderTooltipEventArgs) => {
    args.text = `${args.value} units`;
  };

  // Programmatic reposition
  handleReposition = () => {
    this.sliderRef.current?.reposition();
  };

  render() {
    return (
      <div style={{ padding: 24, maxWidth: 600 }}>
        {/* Single-value MinRange slider with all features */}
        <h3>MinRange Slider</h3>
        <SliderComponent
          ref={this.sliderRef}
          id="full-slider"
          type="MinRange"
          value={this.state.value}
          min={0}
          max={100}
          step={5}
          ticks={this.ticks}
          tooltip={this.tooltip}
          limits={this.limits}
          colorRange={this.colorRange}
          showButtons={true}
          enableAnimation={true}
          change={this.onChange}
          changed={this.onChanged}
          created={this.onCreated}
          renderingTicks={this.onRenderingTicks}
          renderedTicks={this.onRenderedTicks}
          tooltipChange={this.onTooltipChange}
        />
        <p>Selected: {this.state.value}</p>

        {/* Range slider */}
        <h3>Range Slider</h3>
        <SliderComponent
          id="range-slider"
          type="Range"
          value={this.state.rangeValue}
          min={0}
          max={100}
          step={1}
          tooltip={{ isVisible: true, showOn: 'Always' }}
          changed={this.onChanged}
        />
        <p>Range: {this.state.rangeValue[0]} – {this.state.rangeValue[1]}</p>

        {/* Vertical slider */}
        <h3>Vertical Slider</h3>
        <div style={{ height: 250 }}>
          <SliderComponent
            id="vertical-slider"
            orientation="Vertical"
            value={50}
            tooltip={{ isVisible: true }}
          />
        </div>

        <button onClick={this.handleReposition}>Reposition</button>
      </div>
    );
  }
}
```

---

> **⚠️ Important:** Only use the properties, methods, and events documented above. The following are **not** part of the official `SliderComponent` API and must not be used:
> - `onChange` prop (use `change` or `changed`)
> - `onCreated` prop (use `created`)
> - Any jQuery-style methods
> - `open()`, `close()`, `toggle()` — these do not exist on `SliderComponent`

````
