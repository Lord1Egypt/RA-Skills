# Labels in React Rating Component

Show the current rating value as a label and control its position and format.

---

## Showing the Label

Set `showLabel={true}` to display a label showing the current rating value.

```tsx
import { RatingComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div className="wrap">
      <RatingComponent id="rating" value={3} showLabel={true} />
    </div>
  );
}
export default App;
```

- Default is `false` (label hidden).
- By default the label appears to the **Right** of the rating.

---

## Label Position

Use `labelPosition` to control where the label appears. Import the `LabelPosition` enum for type safety.

**Supported positions:** `Top`, `Bottom`, `Left`, `Right`

```tsx
import { RatingComponent, LabelPosition } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div className="wrap">
      <label>Left</label><br />
      <RatingComponent id="rating1" value={3} showLabel={true} labelPosition={LabelPosition.Left} /><br />

      <label>Right</label><br />
      <RatingComponent id="rating2" value={3} showLabel={true} labelPosition={LabelPosition.Right} /><br />

      <label>Top</label><br />
      <RatingComponent id="rating3" value={3} showLabel={true} labelPosition={LabelPosition.Top} /><br />

      <label>Bottom</label><br />
      <RatingComponent id="rating4" value={3} showLabel={true} labelPosition={LabelPosition.Bottom} /><br />
    </div>
  );
}
export default App;
```

You can also pass string values: `labelPosition="Left"`, `labelPosition="Top"`, etc.

---

## Label Template

Use `labelTemplate` to display custom content in the label. The current `value` is available in the template context.

```tsx
import { RatingComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div className="wrap">
      <RatingComponent
        id="rating"
        value={3}
        showLabel={true}
        labelTemplate="<span>${value} out of 5</span>"
      />
    </div>
  );
}
export default App;
```

- Template string uses `${value}` to inject the current rating value.
- The label updates dynamically as the user changes the rating.

---

## Common Patterns

| Goal | Configuration |
|------|---------------|
| Show numeric value | `showLabel={true}` |
| Label above the rating | `labelPosition={LabelPosition.Top}` |
| Label below the rating | `labelPosition={LabelPosition.Bottom}` |
| Show "X out of 5" | `labelTemplate="<span>${value} out of 5</span>"` |
| Show descriptive text | Custom `labelTemplate` with conditional logic |
