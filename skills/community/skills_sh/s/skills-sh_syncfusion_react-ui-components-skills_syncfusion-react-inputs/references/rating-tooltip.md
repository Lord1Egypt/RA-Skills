# Tooltip in React Rating Component

Display contextual tooltips when users hover over rating items.

---

## Enabling Tooltips

Set `showTooltip={true}` to show tooltips on item hover. The default value is `true`, so tooltips are shown out of the box.

```tsx
import { RatingComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div className="wrap">
      <RatingComponent id="rating" value={3} showTooltip={true} />
    </div>
  );
}
export default App;
```

To hide tooltips:

```tsx
<RatingComponent id="rating" value={3} showTooltip={false} />
```

---

## Custom Tooltip Content (tooltipTemplate)

Use `tooltipTemplate` to replace the default tooltip with custom content. The current `value` is available in the template context.

**String template:**

```tsx
import { RatingComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div className="wrap">
      <RatingComponent
        id="rating"
        value={3}
        showTooltip={true}
        tooltipTemplate="<span>${value} Star</span>"
      />
    </div>
  );
}
export default App;
```

**Function template (conditional content by value):**

```tsx
import { RatingComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  function tooltipTemplate(props: { value: number }) {
    const labels: Record<number, string> = {
      1: 'Angry',
      2: 'Sad',
      3: 'Neutral',
      4: 'Good',
      5: 'Happy',
    };
    return <b>{labels[props.value] ?? props.value}</b>;
  }

  return (
    <div className="wrap">
      <RatingComponent
        id="rating"
        value={3}
        showTooltip={true}
        tooltipTemplate={tooltipTemplate}
      />
    </div>
  );
}
export default App;
```

---

## Tooltip Appearance (cssClass)

Customize the tooltip's visual style using `cssClass` and targeting the Syncfusion tooltip CSS classes:

```tsx
<RatingComponent
  id="rating"
  value={3}
  showTooltip={true}
  cssClass="customtooltip"
/>
```

```css
.customtooltip.e-tooltip-wrap {
  background-color: #333;
  border-color: #333;
  border-radius: 4px;
}
.customtooltip.e-tooltip-wrap .e-tip-content {
  color: #fff;
  font-size: 14px;
}
```

---

## Common Patterns

| Goal | Configuration |
|------|---------------|
| Show value as tooltip | `showTooltip={true}` (default) |
| Hide tooltips | `showTooltip={false}` |
| Show descriptive text | `tooltipTemplate` with value-based labels |
| Style the tooltip | `cssClass="customtooltip"` + CSS overrides |
