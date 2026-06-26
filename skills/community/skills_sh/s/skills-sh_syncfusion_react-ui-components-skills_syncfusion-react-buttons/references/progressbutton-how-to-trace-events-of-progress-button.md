# How To: Trace Events of ProgressButton — React ProgressButton

## Overview

Monitor the ProgressButton lifecycle by binding handlers to its four events. This lets you
execute custom logic at each stage — from starting the operation, through incremental updates,
to completion or failure.

---

## Available Events

| Event | Trigger | Typical Use |
|---|---|---|
| [`begin`](api.md#begin--emittypeprogresseventargs) | Progress starts | Initialise state, set `step` or starting `percent` |
| [`progress`](api.md#progress--emittypeprogresseventargs) | At each interval during progress | Update indicators, modify `percent`, intermediate validation |
| [`end`](api.md#end--emittypeprogresseventargs) | Progress completes (100 %) | Show completion state, enable follow-up actions |
| [`fail`](api.md#fail--emittypeevent) | Progress operation is incomplete / fails | Show error message, revert UI |

---

## Full Event Trace Example

```tsx
import { ProgressButtonComponent, ProgressEventArgs } from '@syncfusion/ej2-react-splitbuttons';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';
import { useState } from 'react';

function App() {
  const [eventTrace, setEventTrace] = useState('');

  function begin(args: ProgressEventArgs): void {
    updateEventLog(args);
  }

  function end(args: ProgressEventArgs): void {
    updateEventLog(args);
  }

  function progress(args: ProgressEventArgs): void {
    updateEventLog(args);
  }

  function fail(args: Event): void {
    updateEventLog(args as any);
  }

  function updateEventLog(args: { name: string }): void {
    setEventTrace((prev) => prev + args.name + ' Event triggered. <br />');
  }

  function clearLog(): void {
    setEventTrace('');
  }

  return (
    <div className="control-section">
      <div className="progress-btn-section">
        <ProgressButtonComponent
          content="Progress"
          enableProgress={true}
          begin={begin}
          end={end}
          progress={progress}
          fail={fail}
        />
      </div>
      <div className="property-section">
        <table id="propertyTable" title="Event trace">
          <tbody>
            <tr>
              <th>Event trace:-</th>
            </tr>
            <tr>
              <td dangerouslySetInnerHTML={{ __html: eventTrace }} />
            </tr>
          </tbody>
        </table>
      </div>
      <ButtonComponent id="clear" cssClass="e-small" content="Clear" onClick={clearLog} />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('progress-button'));
```

---

## ProgressEventArgs Reference

The `begin`, `progress`, and `end` callbacks receive a
[`ProgressEventArgs`](api.md#progresseventargs) object with:

| Property | Type | Description |
|---|---|---|
| `name` | `string` | Event name: `"begin"`, `"progress"`, or `"end"` |
| `percent` | `number` | Current progress percentage (0–100); writable in `progress` handler |
| `step` | `number` | Increment step per interval; writable in `begin` handler |
| `currentDuration` | `number` | Elapsed duration in milliseconds |

The `fail` callback receives a plain `Event` object.

---

## Minimal Event Handler

```tsx
<ProgressButtonComponent
  content="Go"
  enableProgress={true}
  begin={(args) => console.log('begin', args.percent)}
  progress={(args) => console.log('progress', args.percent)}
  end={(args) => console.log('end', args.percent)}
  fail={(args) => console.error('fail', args)}
/>
```

---

## See Also

- [Change text content and styles during progress](how-to-change-text-content-and-styles-of-the-progressbutton-during-progress.md)
- [Spinner and Progress](spinner-and-progress.md)
- [API Reference](api.md)
