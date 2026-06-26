# How To: Enable Progress in Button — React ProgressButton

## Overview

Display a visual progress indicator within the button by setting the
[`enableProgress`](api.md#enableprogress--boolean) prop to `true`. When enabled, a background
fill extends across the button width as the operation progresses, giving users clear visual
feedback on task completion percentage.

---

## Example

```tsx
import { ProgressButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  return (
    <div>
      <ProgressButtonComponent content="Spin Left" enableProgress={true} />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('progress-button'));
```

---

## Key Points

- `enableProgress` defaults to `false`; the button shows only the spinner by default.
- The progress fill width is proportional to the elapsed `duration`.
- Combine with `cssClass="e-hide-spinner"` to show the progress bar without the spinner.
- Use the `duration` prop (default `2000` ms) to control how long the fill takes to reach 100 %.

---

## See Also

- [Hide spinner](how-to-hide-spinner.md)
- [Customize progress using cssClass](how-to-customize-progress-using-cssclass.md)
- [API — enableProgress](api.md#enableprogress--boolean)
