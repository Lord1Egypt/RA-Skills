# How To: Customize Progress Using cssClass — React ProgressButton

## Overview

Customize the progress bar appearance using CSS classes applied through the
[`cssClass`](api.md#cssclass--string) prop. These classes change the fill direction, position,
and style of the progress animation.

---

## Built-in cssClass Modifiers

| Class | Effect |
|---|---|
| `e-vertical` | Progress fills vertically — top to bottom |
| `e-progress-top` | Progress fill is anchored to the top edge of the button |
| `e-hide-spinner` | Hides the spinner (combine with the above for clean bar-only look) |

---

## Examples

### Vertical progress

```tsx
import { ProgressButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  return (
    <ProgressButtonComponent
      content="Vertical Progress"
      enableProgress={true}
      cssClass="e-hide-spinner e-vertical"
      duration={4000}
    />
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('progress-button'));
```

---

### Progress at the top edge

```tsx
<ProgressButtonComponent
  content="Progress Top"
  enableProgress={true}
  cssClass="e-hide-spinner e-progress-top"
  duration={4000}
/>
```

---

### Reverse (right-to-left) progress

Add a custom class name and define CSS to achieve a right-to-left fill effect:

```tsx
<ProgressButtonComponent
  content="Reverse Progress"
  enableProgress={true}
  cssClass="e-hide-spinner e-reverse-progress"
  duration={4000}
/>
```

```css
/* Override fill direction for reverse effect */
.e-progress-btn.e-reverse-progress .e-progress-wrapper {
  right: 0;
  left: auto;
}
```

---

### All three together

```tsx
function App() {
  return (
    <div>
      <ProgressButtonComponent
        content="Vertical Progress"
        enableProgress={true}
        cssClass="e-hide-spinner e-vertical"
        duration={4000}
      />
      <ProgressButtonComponent
        content="Progress Top"
        enableProgress={true}
        cssClass="e-hide-spinner e-progress-top"
        duration={4000}
      />
      <ProgressButtonComponent
        content="Reverse Progress"
        enableProgress={true}
        cssClass="e-hide-spinner e-reverse-progress"
        duration={4000}
      />
    </div>
  );
}
```

---

## See Also

- [Style and Appearance](style-and-appearance.md)
- [Hide spinner](how-to-hide-spinner.md)
- [API — cssClass](api.md#cssclass--string)
