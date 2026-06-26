# Spinner and Progress — React ProgressButton

## Table of Contents

1. [Spinner](#spinner)
   - [Change spinner position](#change-spinner-position)
   - [Change spinner size](#change-spinner-size)
   - [Spinner template](#spinner-template)
   - [Full spinner configuration example](#full-spinner-configuration-example)
2. [Progress](#progress)
   - [Enable background progress fill](#enable-background-progress-fill)
   - [Content animation](#content-animation)
   - [Change step of the ProgressButton](#change-step-of-the-progressbutton)
   - [Change progress dynamically](#change-progress-dynamically)
   - [Start and stop methods](#start-and-stop-methods)

---

## Spinner

The spinner is the animated rotating indicator displayed while progress is active. It is
controlled via the `spinSettings` prop, which accepts a [`SpinSettingsModel`](api.md#spinsettingsmodel).

### Change spinner position

Set [`spinSettings.position`](api.md#position--spinposition) to reposition the spinner relative
to the button text. Available values: `Left` (default), `Right`, `Top`, `Bottom`, `Center`.

```tsx
import { ProgressButtonComponent, SpinSettingsModel } from '@syncfusion/ej2-react-splitbuttons';
import * as React from 'react';

function App() {
  const spinSettings: SpinSettingsModel = { position: 'Right' };

  return <ProgressButtonComponent content="Submit" spinSettings={spinSettings} />;
}
export default App;
```

---

### Change spinner size

Set [`spinSettings.width`](api.md#width--string--number) to scale the spinner. Accepts a pixel
number or a CSS string.

```tsx
import { ProgressButtonComponent, SpinSettingsModel } from '@syncfusion/ej2-react-splitbuttons';
import * as React from 'react';

function App() {
  const spinSettings: SpinSettingsModel = { width: 20 }; // 20 px — smaller than default

  return <ProgressButtonComponent content="Submit" spinSettings={spinSettings} />;
}
export default App;
```

---

### Spinner template

Replace the default animated spinner with custom HTML or SVG markup via
[`spinSettings.template`](api.md#template--string--function).

```tsx
import { ProgressButtonComponent, SpinSettingsModel } from '@syncfusion/ej2-react-splitbuttons';
import * as React from 'react';

function App() {
  const spinSettings: SpinSettingsModel = {
    template: '<div class="custom-spinner"></div>'
  };

  return <ProgressButtonComponent content="Submit" spinSettings={spinSettings} />;
}
export default App;
```

Add the corresponding CSS to animate your template:

```css
.custom-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid #fff;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
```

---

### Full spinner configuration example

Combines position, width, and template in one `spinSettings` object:

```tsx
import { ProgressButtonComponent, SpinSettingsModel } from '@syncfusion/ej2-react-splitbuttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  const spinSettings: SpinSettingsModel = {
    position: 'Right',
    width: 20,
    template: '<div class="template"></div>'
  };

  return <ProgressButtonComponent content="Submit" spinSettings={spinSettings} />;
}
export default App;
ReactDom.render(<App />, document.getElementById('progress-button'));
```

---

## Progress

### Enable background progress fill

Set [`enableProgress`](api.md#enableprogress--boolean) to `true` to show a background fill that
advances across the button as the operation runs. See also:
[how-to-enable-progress-in-button.md](how-to-enable-progress-in-button.md).

```tsx
<ProgressButtonComponent content="Upload" enableProgress={true} duration={4000} />
```

---

### Content animation

Animate the button text/content during progress using the `animationSettings` prop, which accepts
an [`AnimationSettingsModel`](api.md#animationsettingsmodel).

Key properties:
- [`effect`](api.md#effect--animationeffect) — `None` | `SlideLeft` | `SlideRight` | `SlideUp` | `SlideDown` | `ZoomIn` | `ZoomOut`
- [`duration`](api.md#duration--number-1) — animation duration in ms
- [`easing`](api.md#easing--string) — CSS easing function string

Pair with `spinSettings.position = 'Center'` to centre the spinner while content animates:

```tsx
import {
  AnimationSettingsModel,
  ProgressButtonComponent,
  SpinSettingsModel
} from '@syncfusion/ej2-react-splitbuttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  const spinSettings: SpinSettingsModel = { position: 'Center' };
  const animationSettings: AnimationSettingsModel = {
    effect: 'SlideLeft',
    duration: 500,
    easing: 'linear'
  };

  return (
    <ProgressButtonComponent
      content="Slide Left"
      enableProgress={true}
      spinSettings={spinSettings}
      animationSettings={animationSettings}
    />
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('progress-button'));
```

---

### Change step of the ProgressButton

Control progress granularity by setting [`args.step`](api.md#step--number-readwrite) in the
[`begin`](api.md#begin--emittypeprogresseventargs) event handler. A `step` of `20` means the
progress bar advances in 5 increments (100 ÷ 20).

```tsx
import { ProgressButtonComponent, ProgressEventArgs } from '@syncfusion/ej2-react-splitbuttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  function begin(args: ProgressEventArgs): void {
    args.step = 20;
  }

  return (
    <ProgressButtonComponent
      content="Progress Step"
      enableProgress={true}
      begin={begin}
      cssClass="e-hide-spinner"
    />
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('progress-button'));
```

> The `e-hide-spinner` CSS class removes the spinner, leaving only the progress bar fill.

---

### Change progress dynamically

Modify [`args.percent`](api.md#percent--number-readwrite) inside the
[`progress`](api.md#progress--emittypeprogresseventargs) event handler to jump the progress
to any value based on application logic.

```tsx
import { ProgressButtonComponent, ProgressEventArgs } from '@syncfusion/ej2-react-splitbuttons';
import { useState } from 'react';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  const [content, setContent] = useState('Progress');

  function begin(args: ProgressEventArgs): void {
    setContent('Progress ' + args.percent + '%');
  }

  function progress(args: ProgressEventArgs): void {
    setContent('Progress ' + args.percent + '%');
    if (args.percent === 40) {
      args.percent = 90; // jump to 90 % when 40 % is reached
    }
  }

  function end(args: ProgressEventArgs): void {
    setContent('Progress ' + args.percent + '%');
  }

  return (
    <ProgressButtonComponent
      content={content}
      enableProgress={true}
      duration={15000}
      begin={begin}
      progress={progress}
      end={end}
      cssClass="e-hide-spinner"
    />
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('progress-button'));
```

---

### Start and stop methods

Use the [`start()`](api.md#startpercent-number--void) and [`stop()`](api.md#stop--void) methods
to programmatically pause and resume progress. Access them via a component ref.

```tsx
import { ProgressButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import { useState } from 'react';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  let progressBtn: ProgressButtonComponent;
  const [content, setContent] = useState('Download');
  const [iconCss, setIconCss] = useState('e-btn-sb-icon e-download');

  function end(): void {
    setContent('Download');
    setIconCss('e-btn-sb-icon e-download');
  }

  function clickHandler(): void {
    if (content === 'Download') {
      setContent('Pause');
      setIconCss('e-btn-sb-icon e-pause');
    } else if (content === 'Pause') {
      setContent('Resume');
      setIconCss('e-btn-sb-icon e-play');
      progressBtn.stop();
    } else if (content === 'Resume') {
      setContent('Pause');
      setIconCss('e-btn-sb-icon e-pause');
      progressBtn.start();
    }
  }

  return (
    <ProgressButtonComponent
      content={content}
      enableProgress={true}
      duration={4000}
      iconCss={iconCss}
      end={end}
      cssClass="e-hide-spinner"
      onClick={clickHandler}
      ref={(scope) => { progressBtn = scope as ProgressButtonComponent; }}
    />
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('progress-button'));
```

> Use [`progressComplete()`](api.md#progresscomplete--void) to instantly complete progress
> without waiting for the duration to elapse.

---

## See Also

- [Hide spinner](how-to-hide-spinner.md)
- [Customize ProgressButton using cssClass](how-to-customize-progress-using-cssclass.md)
- [API Reference](api.md)
