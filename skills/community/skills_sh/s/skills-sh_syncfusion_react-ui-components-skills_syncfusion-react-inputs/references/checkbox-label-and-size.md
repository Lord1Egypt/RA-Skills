# Label and Size — Syncfusion React CheckBox

Configure the checkbox caption text, label position, and display size.

---

## Label

Use the `label` property to define the caption for the CheckBox. This eliminates the need for separate `<label>` HTML elements.

```tsx
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  return (
    <CheckBoxComponent label="Accept Terms and Conditions" />
  );
}
export default App;
```

**Property:** `label` — `string`, defaults to `''`

---

## Label Position

Use the `labelPosition` property to place the label **before** or **after** the checkbox frame.

| Value | Behavior |
|-------|----------|
| `"After"` | Label appears to the **right** of the checkbox (default) |
| `"Before"` | Label appears to the **left** of the checkbox |

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

enableRipple(true);

function App() {
  return (
    <ul>
      {/* Label on the left */}
      <li><CheckBoxComponent label="Left Side Label" labelPosition="Before" /></li>

      {/* Label on the right (default) */}
      <li><CheckBoxComponent label="Right Side Label" checked={true} /></li>
    </ul>
  );
}
export default App;
```

**Property:** `labelPosition` — `'Before' | 'After'`, defaults to `'After'`

---

## Size

The CheckBox offers two size options:

| Size | How to Set |
|------|-----------|
| **Default** | No additional prop needed |
| **Small** | `cssClass="e-small"` |

Use small checkboxes in compact layouts, data tables, or dense form fields.

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

enableRipple(true);

function App() {
  return (
    <ul>
      {/* Small size */}
      <li><CheckBoxComponent label="Small" cssClass="e-small" /></li>

      {/* Default size */}
      <li><CheckBoxComponent label="Default" /></li>
    </ul>
  );
}
export default App;
```

**Property:** `cssClass` — `string`, defaults to `''`

---

## Combined Example

```tsx
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  return (
    <ul>
      <li><CheckBoxComponent label="Default size, label after" /></li>
      <li><CheckBoxComponent label="Default size, label before" labelPosition="Before" /></li>
      <li><CheckBoxComponent label="Small size, label after" cssClass="e-small" /></li>
      <li><CheckBoxComponent label="Small size, label before" cssClass="e-small" labelPosition="Before" /></li>
    </ul>
  );
}
export default App;
```

---

## HTML Sanitization for Label

By default, `enableHtmlSanitizer` is `true`, which sanitizes untrusted HTML in the `label` value. Set it to `false` only if you need to render trusted HTML content in the label.

```tsx
<CheckBoxComponent label="<b>Bold Label</b>" enableHtmlSanitizer={false} />
```

> Avoid disabling the sanitizer for user-generated content to prevent XSS vulnerabilities.
