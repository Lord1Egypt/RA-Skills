# ProgressButton API Reference

> **Source:** https://ej2.syncfusion.com/react/documentation/api/progress-button/  
> **Package:** `@syncfusion/ej2-react-splitbuttons`  
> **Component:** `ProgressButtonComponent`

## Table of Contents

1. [ProgressButtonComponent](#progressbuttoncomponent)
   - [Properties](#properties)
   - [Methods](#methods)
   - [Events](#events)
2. [SpinSettingsModel](#spinsettingsmodel)
3. [AnimationSettingsModel](#animationsettingsmodel)
4. [ProgressEventArgs](#progresseventargs)
5. [Enums](#enums)
   - [SpinPosition](#spinposition)
   - [AnimationEffect](#animationeffect)
   - [IconPosition](#iconposition)
6. [Import Paths](#import-paths)

---

## ProgressButtonComponent

`ProgressButtonComponent` represents the React ProgressButton Component.

### Minimal usage

```tsx
import { ProgressButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

<ProgressButtonComponent content="Progress Button" />
```

---

### Properties

#### `animationSettings` — `AnimationSettingsModel`

Specifies the animation settings for content transitions during progress.  
See [AnimationSettingsModel](#animationsettingsmodel) for property details.

**Default:** `{}`

```tsx
<ProgressButtonComponent
  content="Animate"
  animationSettings={{ effect: 'SlideLeft', duration: 500, easing: 'linear' }}
/>
```

---

#### `content` — `string`

Defines the text content displayed on the progress button element.

**Default:** `""`

```tsx
<ProgressButtonComponent content="Submit" />
```

---

#### `cssClass` — `string`

Specifies the root CSS class applied to the progress button. Used for customisation of
appearance, button type, style, and size. Multiple space-separated classes are allowed.

**Default:** `""`

Built-in utility classes:
- `e-primary` — primary style
- `e-success` — success style
- `e-info` — info style
- `e-warning` — warning style
- `e-danger` — danger style
- `e-outline` — outline style
- `e-flat` — flat style
- `e-hide-spinner` — hides the spinner (shows only the progress bar fill)
- `e-vertical` — fills progress vertically (top to bottom)
- `e-progress-top` — positions the progress fill at the top edge
- `e-round` — round button style

```tsx
<ProgressButtonComponent content="Upload" cssClass="e-primary e-hide-spinner" />
```

---

#### `disabled` — `boolean`

Enables or disables the progress button. When `true`, the button cannot be interacted with.

**Default:** `false`

```tsx
<ProgressButtonComponent content="Disabled" disabled={true} />
```

---

#### `duration` — `number`

Specifies the total duration (in milliseconds) of the progress animation from 0 % to 100 %.

**Default:** `2000`

```tsx
<ProgressButtonComponent content="Long task" enableProgress={true} duration={8000} />
```

---

#### `enableHtmlSanitizer` — `boolean`

When `true`, the component sanitises any suspected untrusted HTML strings in `content` before rendering.

**Default:** `true`

---

#### `enablePersistence` — `boolean`

Enable or disable persisting the component's state between page reloads.

**Default:** `false`

---

#### `enableProgress` — `boolean`

Enables or disables the background filler progress bar UI inside the button. When `true`, a
fill extends across the button width (or height when using `e-vertical`) as the operation advances.

**Default:** `false`

```tsx
<ProgressButtonComponent content="Upload" enableProgress={true} />
```

---

#### `enableRtl` — `boolean`

Enable or disable rendering the component in right-to-left direction.

**Default:** `false`

---

#### `iconCss` — `string`

Defines one or more CSS class names (space-separated) used to include an icon on the button.
Supports font icons and sprite images.

**Default:** `""`

```tsx
<ProgressButtonComponent content="Download" iconCss="e-btn-sb-icon e-download" />
```

---

#### `iconPosition` — `string | IconPosition`

Positions the icon relative to the button text. Possible values:

| Value | Description |
|---|---|
| `Left` | Icon on the left of the text (default) |
| `Right` | Icon on the right of the text |
| `Top` | Icon above the text |
| `Bottom` | Icon below the text |

**Default:** `IconPosition.Left`

```tsx
<ProgressButtonComponent content="Next" iconCss="e-icons e-arrow-right" iconPosition="Right" />
```

---

#### `isPrimary` — `boolean`

When `true`, enhances the visual appearance of the button with a primary style treatment.

**Default:** `false`

---

#### `isToggle` — `boolean`

When `true`, the button behaves as a toggle. Clicking changes its state from normal to active.

**Default:** `false`

---

#### `spinSettings` — `SpinSettingsModel`

Specifies the spinner and its related properties (position, width, template).  
See [SpinSettingsModel](#spinsettingsmodel) for property details.

**Default:** `{}`

```tsx
<ProgressButtonComponent
  content="Submit"
  spinSettings={{ position: 'Right', width: 20 }}
/>
```

---

### Methods

#### `click()` — `void`

Programmatically clicks the button element (native method).

```tsx
progressBtnRef.current?.click();
```

---

#### `destroy()` — `void`

Destroys the widget and cleans up all event listeners and DOM modifications.

```tsx
progressBtnRef.current?.destroy();
```

---

#### `focusIn()` — `void`

Sets focus on the ProgressButton element (native method).

```tsx
progressBtnRef.current?.focusIn();
```

---

#### `progressComplete()` — `void`

Immediately completes the button progress, jumping to 100 % and triggering the `end` event.

```tsx
progressBtnRef.current?.progressComplete();
```

---

#### `start(percent?: number)` — `void`

Starts the button progress. If `percent` is supplied, progress begins from that value.

| Parameter | Type | Description |
|---|---|---|
| `percent` | `number` *(optional)* | Starting percentage for progress |

```tsx
progressBtnRef.current?.start();      // start from 0
progressBtnRef.current?.start(50);    // start from 50 %
```

---

#### `stop()` — `void`

Stops / pauses the button progress at its current percentage. Use `start()` to resume.

```tsx
progressBtnRef.current?.stop();
```

---

### Events

#### `begin` — `EmitType<ProgressEventArgs>`

Triggers when the progress starts. Use to initialise parameters or update UI at start.

```tsx
<ProgressButtonComponent
  content="Go"
  enableProgress={true}
  begin={(args: ProgressEventArgs) => {
    console.log('Started at', args.percent, '%');
    args.step = 20; // customise step size here
  }}
/>
```

---

#### `created` — `EmitType<Event>`

Triggers once the component rendering is completed.

```tsx
<ProgressButtonComponent content="Go" created={() => console.log('Component ready')} />
```

---

#### `end` — `EmitType<ProgressEventArgs>`

Triggers when the progress reaches 100 % and completes.

```tsx
<ProgressButtonComponent
  content="Go"
  enableProgress={true}
  end={(args: ProgressEventArgs) => console.log('Done at', args.percent, '%')}
/>
```

---

#### `fail` — `EmitType<Event>`

Triggers when the progress operation is incomplete / fails.

```tsx
<ProgressButtonComponent content="Go" fail={(args: Event) => console.error('Failed', args)} />
```

---

#### `progress` — `EmitType<ProgressEventArgs>`

Triggers at intervals during progress. Use to update indicators, modify `percent`, or perform
intermediate logic.

```tsx
<ProgressButtonComponent
  content="Go"
  enableProgress={true}
  progress={(args: ProgressEventArgs) => {
    if (args.percent === 40) {
      args.percent = 90; // jump progress to 90 % at 40 %
    }
  }}
/>
```

---

## SpinSettingsModel

**Source:** https://ej2.syncfusion.com/react/documentation/api/progress-button/spinSettingsModel/

Interface for a class `SpinSettings`.

### Properties

#### `position` — `SpinPosition`

Specifies the position of the spinner relative to button content.

| Value | Description |
|---|---|
| `Left` | Spinner to the left of text (default) |
| `Right` | Spinner to the right of text |
| `Top` | Spinner above text |
| `Bottom` | Spinner below text |
| `Center` | Spinner centred over the button |

```tsx
const spinSettings: SpinSettingsModel = { position: 'Right' };
```

---

#### `template` — `string | Function`

Specifies the HTML/SVG template content to display as the spinner. Replaces the default
animated spinner with custom markup.

```tsx
const spinSettings: SpinSettingsModel = {
  template: '<div class="custom-spinner"></div>'
};
```

---

#### `width` — `string | number`

Sets the width (size) of the spinner. Accepts a pixel number or CSS string value.

```tsx
const spinSettings: SpinSettingsModel = { width: 20 };       // 20px
const spinSettings: SpinSettingsModel = { width: '1.5rem' };  // CSS value
```

---

## AnimationSettingsModel

**Source:** https://ej2.syncfusion.com/react/documentation/api/progress-button/animationSettingsModel/

Interface for a class `AnimationSettings`.

### Properties

#### `duration` — `number`

Specifies the duration (in milliseconds) of the content animation.

```tsx
const animationSettings: AnimationSettingsModel = { duration: 500 };
```

---

#### `easing` — `string`

Specifies the CSS animation timing function (easing) for the animation.

```tsx
const animationSettings: AnimationSettingsModel = { easing: 'linear' };
// also: 'ease', 'ease-in', 'ease-out', 'ease-in-out', or cubic-bezier values
```

---

#### `effect` — `AnimationEffect`

Specifies the animation effect applied to button content during progress.  
See [AnimationEffect](#animationeffect) for all values.

```tsx
const animationSettings: AnimationSettingsModel = { effect: 'SlideLeft' };
```

---

## ProgressEventArgs

**Source:** https://ej2.syncfusion.com/react/documentation/api/progress-button/progressEventArgs/

Interface for progress event arguments. Received in `begin`, `progress`, and `end` event handlers.

### Properties

#### `currentDuration` — `number` *(read-only)*

Indicates the elapsed duration of the progress in milliseconds.

#### `name` — `string` *(read-only)*

Specifies the name of the event (e.g., `"begin"`, `"progress"`, `"end"`).

#### `percent` — `number` *(read/write)*

Indicates the current state of progress as a percentage (0–100).  
You can **write** to this property inside `progress` event handlers to jump progress to a custom value.

```tsx
progress={(args: ProgressEventArgs) => {
  if (args.percent === 40) args.percent = 90; // skip ahead
}}
```

#### `step` — `number` *(read/write)*

Specifies the interval (step size) for each progress increment. Writing this in the `begin`
event controls how granularly the progress bar advances.

```tsx
begin={(args: ProgressEventArgs) => {
  args.step = 20; // advance 5 steps to complete (100 / 20 = 5 increments)
}}
```

---

## Enums

### SpinPosition

Possible values for `SpinSettingsModel.position`:

| Value | Description |
|---|---|
| `Left` | Spinner to the left of text content (default) |
| `Right` | Spinner to the right of text content |
| `Top` | Spinner above text content |
| `Bottom` | Spinner below text content |
| `Center` | Spinner centred over the button |

---

### AnimationEffect

Possible values for `AnimationSettingsModel.effect`:

| Value | Description |
|---|---|
| `None` | No animation |
| `SlideLeft` | Content slides from right to left |
| `SlideRight` | Content slides from left to right |
| `SlideUp` | Content slides upward |
| `SlideDown` | Content slides downward |
| `ZoomIn` | Content scales up (zooms in) |
| `ZoomOut` | Content scales down (zooms out) |

---

### IconPosition

Possible values for `ProgressButtonComponent.iconPosition`:

| Value | Description |
|---|---|
| `Left` | Icon to the left of text (default) |
| `Right` | Icon to the right of text |
| `Top` | Icon above text |
| `Bottom` | Icon below text |

---

## Import Paths

```tsx
// Component and model types
import {
  ProgressButtonComponent,
  SpinSettingsModel,
  AnimationSettingsModel,
  ProgressEventArgs
} from '@syncfusion/ej2-react-splitbuttons';

// CSS (choose one theme)
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-buttons/styles/tailwind3.css';
import '@syncfusion/ej2-popups/styles/tailwind3.css';
import '@syncfusion/ej2-splitbuttons/styles/tailwind3.css';
```

> Other available themes: `material.css`, `material3.css`, `bootstrap5.css`, `fluent.css`, `highcontrast.css`.
