# OTP Input Accessibility

## Table of Contents
- [Accessibility Standards](#accessibility-standards)
- [WAI-ARIA Attributes](#wai-aria-attributes)
- [Keyboard Navigation](#keyboard-navigation)
- [ARIA Labels per Field](#aria-labels-per-field)
- [HTML Attributes](#html-attributes)
- [RTL Support](#rtl-support)
- [Ensuring Accessibility in Tests](#ensuring-accessibility-in-tests)

---

## Accessibility Standards

The Syncfusion React OTP Input component meets the following accessibility standards out of the box:

| Standard | Support |
|----------|---------|
| WCAG 2.2 | ✅ Supported |
| Section 508 | ✅ Supported |
| Screen Reader | ✅ Supported |
| Right-to-Left | ✅ Supported |
| Color Contrast | ✅ Sufficient contrast ratios |
| Mobile Device | ✅ Supported |
| Keyboard Navigation | ✅ Full support |
| Accessibility Checker | ✅ Validated |
| Axe-core Validation | ✅ Validated |

---

## WAI-ARIA Attributes

The OTP Input renders the following ARIA roles and attributes automatically:

| Attribute | Purpose |
|-----------|---------|
| `role="group"` | Groups all input fields together as a single logical widget |
| `aria-label` | Provides a text label for each individual OTP input field |

These are applied automatically without additional configuration. Use `ariaLabels` to override default label text.

---

## Keyboard Navigation

Users can navigate and interact with the OTP input using the keyboard:

| Key | Action |
|-----|--------|
| `Left Arrow` | Moves focus to the previous input field |
| `Right Arrow` | Moves focus to the next input field |
| `Tab` | Shifts focus to the next input field |
| `Shift + Tab` | Shifts focus to the previous input field |

---

## ARIA Labels per Field

Provide custom ARIA labels for each input field using the `ariaLabels` property. This is important for screen reader users who need descriptive labels for each field.

```tsx
import { OtpInputComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  const ariaLabels = ['First digit', 'Second digit', 'Third digit', 'Fourth digit'];

  return (
    <div id="container">
      <OtpInputComponent id="otpinput" value={1234} ariaLabels={ariaLabels} />
    </div>
  );
}

export default App;
```

> **Best practice:** Always provide `ariaLabels` with meaningful descriptions. Use `['Digit 1 of 6', 'Digit 2 of 6', ...]` for screen reader users to understand their position within the OTP.

For a 6-digit OTP:

```tsx
const ariaLabels = [
  'Digit 1 of 6',
  'Digit 2 of 6',
  'Digit 3 of 6',
  'Digit 4 of 6',
  'Digit 5 of 6',
  'Digit 6 of 6',
];
<OtpInputComponent id="otpinput" length={6} ariaLabels={ariaLabels} />
```

---

## HTML Attributes

Use the `htmlAttributes` property to add any additional HTML attributes to the OTP Input component element. This provides extra flexibility for accessibility annotations, test IDs, or custom metadata.

```tsx
import { OtpInputComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  const htmlAttributes: { [key: string]: string } = {
    title: 'One-Time Password',
    'data-testid': 'otp-field',
  };

  return (
    <div id="container">
      <OtpInputComponent id="otpinput" value={1234} htmlAttributes={htmlAttributes} />
    </div>
  );
}

export default App;
```

Useful `htmlAttributes` for accessibility:
- `title`: Tooltip text for the group
- `aria-describedby`: Link to an instruction element
- `data-*`: Test automation attributes

---

## RTL Support

Enable right-to-left rendering for users in RTL languages (Arabic, Hebrew, Farsi, etc.):

```tsx
import { OtpInputComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div id="container">
      <OtpInputComponent id="otpinput" enableRtl={true} />
    </div>
  );
}

export default App;
```

> When `enableRtl` is `true`, the input fields render from right to left and keyboard navigation is reversed accordingly.

---

## Ensuring Accessibility in Tests

The OTP Input is validated with these tools:
- **[accessibility-checker](https://www.npmjs.com/package/accessibility-checker)** — automated WCAG rule checking
- **[axe-core](https://www.npmjs.com/package/axe-core)** — industry-standard accessibility testing engine

To test accessibility in your own project:

```bash
npm install axe-core --save-dev
```

```tsx
import axe from 'axe-core';

// Run after component renders
axe.run(document.getElementById('container'), (err, results) => {
  if (err) throw err;
  console.log('Violations:', results.violations);
});
```

See [Syncfusion Accessibility Documentation](https://ej2.syncfusion.com/react/documentation/common/accessibility) for full guidance.
