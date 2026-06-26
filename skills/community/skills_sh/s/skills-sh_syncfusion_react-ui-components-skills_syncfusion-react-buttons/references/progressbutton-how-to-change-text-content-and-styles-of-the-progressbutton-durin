# How To: Change Text Content and Styles During Progress — React ProgressButton

## Overview

Update the ProgressButton's label text and visual appearance while progress is active by
modifying component state inside the [`begin`](api.md#begin--emittypeprogresseventargs) and
[`end`](api.md#end--emittypeprogresseventargs) event handlers. This provides real-time
status feedback to users during long-running operations.

---

## Pattern

Use React `useState` to hold the mutable `content` and `cssClass` values, then call the
state updater from inside the event callbacks to trigger re-renders.

---

## Example — Upload flow with status feedback

```tsx
import { ProgressButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';
import { useState } from 'react';

function App() {
  const [content, setContent] = useState('Upload');
  const [cssClass, setCssClass] = useState('e-hide-spinner');

  function begin(): void {
    setContent('Uploading...');
    setCssClass('e-hide-spinner e-info');
  }

  function end(): void {
    setContent('Success');
    setCssClass('e-hide-spinner e-success');
    // Reset to initial state after a short delay
    setTimeout(() => {
      setContent('Upload');
      setCssClass('e-hide-spinner');
    }, 500);
  }

  return (
    <ProgressButtonComponent
      content={content}
      enableProgress={true}
      cssClass={cssClass}
      duration={4000}
      begin={begin}
      end={end}
    />
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('progress-button'));
```

---

## How It Works

| Stage | `content` | `cssClass` |
|---|---|---|
| Initial | `Upload` | `e-hide-spinner` |
| `begin` fires | `Uploading...` | `e-hide-spinner e-info` (blue) |
| `end` fires | `Success` | `e-hide-spinner e-success` (green) |
| After 500 ms | `Upload` | `e-hide-spinner` (reset) |

---

## Extending the Pattern

You can also react to the `progress` event for incremental text updates:

```tsx
function progress(args: ProgressEventArgs): void {
  setContent(`Uploading... ${args.percent}%`);
}
```

---

## See Also

- [Trace events of ProgressButton](how-to-trace-events-of-progress-button.md)
- [Spinner and Progress](spinner-and-progress.md)
- [API — begin event](api.md#begin--emittypeprogresseventargs)
- [API — end event](api.md#end--emittypeprogresseventargs)
