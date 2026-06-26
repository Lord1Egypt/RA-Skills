# How To: Hide Spinner — React ProgressButton

## Overview

Remove the animated spinner icon from the ProgressButton by adding the `e-hide-spinner` CSS
class to the [`cssClass`](api.md#cssclass--string) prop. This creates a cleaner look when you
want to show only the progress bar fill without the spinning visual indicator.

---

## Example

```tsx
import { ProgressButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  return (
    <ProgressButtonComponent
      content="Progress"
      enableProgress={true}
      cssClass="e-hide-spinner"
    />
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('progress-button'));
```

---

## Combining with Other Classes

`e-hide-spinner` is a utility class and composes with any other `cssClass` values:

```tsx
// Hide spinner + primary style
<ProgressButtonComponent
  content="Upload"
  enableProgress={true}
  cssClass="e-hide-spinner e-primary"
  duration={4000}
/>

// Hide spinner + vertical progress fill
<ProgressButtonComponent
  content="Vertical"
  enableProgress={true}
  cssClass="e-hide-spinner e-vertical"
  duration={4000}
/>
```

---

## See Also

- [Customize progress using cssClass](how-to-customize-progress-using-cssclass.md)
- [Style and Appearance](style-and-appearance.md)
- [API — cssClass](api.md#cssclass--string)
