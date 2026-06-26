# Localization and Accessibility

## Table of Contents
- [Localization Overview](#localization-overview)
- [Culture Configuration](#culture-configuration)
- [WCAG 2.2 Compliance](#wcag-22-compliance)
- [Keyboard Interaction](#keyboard-interaction)
- [ARIA Attributes](#aria-attributes)
- [Screen Reader Support](#screen-reader-support)
- [Focus Management](#focus-management)
- [Testing Accessibility](#testing-accessibility)

## Localization Overview

The Dialog component supports localization for:
- Close icon title text
- Button text (if using culture-specific locales)

### Supported Locales

The Dialog works with any culture/locale string supported by JavaScript. Common examples:
- `en` - English
- `de` - German
- `fr` - French
- `es` - Spanish
- `pt` - Portuguese
- `ru` - Russian
- `ar` - Arabic
- `zh` - Chinese
- `ja` - Japanese
- `ko` - Korean
- `hi` - Hindi
- `id` - Indonesian
- `th` - Thai
- `vi` - Vietnamese
- `pt-BR` - Brazilian Portuguese
- `zh-CN` - Simplified Chinese
- `zh-TW` - Traditional Chinese

## Culture Configuration

### Basic Culture Setting

```jsx
import React, { useRef } from 'react';
import { DialogComponent } from '@syncfusion/ej2-react-popups';
import { setCulture } from '@syncfusion/ej2-base';
import './App.css';

export default function App() {
  const dialogRef = useRef(null);

  // Set culture globally
  setCulture('de');  // German

  return (
    <div id="dialog-target" style={{ position: 'relative' }}>
      <button onClick={() => dialogRef.current?.show()}>Open</button>

      <DialogComponent
        ref={dialogRef}
        header="Dialog"
        showCloseIcon={true}
        target="#dialog-target"
      >
        Close icon title will be in German
      </DialogComponent>
    </div>
  );
}
```

### Culture Switcher

```jsx
export function LocalizedDialog() {
  const dialogRef = useRef(null);
  const [culture, setCultureState] = React.useState('en');

  const handleCultureChange = (newCulture) => {
    setCultureState(newCulture);
    setCulture(newCulture);
  };

  const cultures = ['en', 'de', 'fr', 'es', 'pt', 'ar', 'zh', 'ja'];

  return (
    <div id="dialog-target" style={{ position: 'relative' }}>
      <div style={{ padding: '20px', marginBottom: '20px' }}>
        <label>Select Language:</label>
        <select
          value={culture}
          onChange={(e) => handleCultureChange(e.target.value)}
          style={{ marginLeft: '10px', padding: '5px' }}
        >
          {cultures.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
      </div>

      <button onClick={() => dialogRef.current?.show()}>Open Dialog</button>

      <DialogComponent
        ref={dialogRef}
        header={`Dialog (${culture})`}
        showCloseIcon={true}
        target="#dialog-target"
        buttons={[
          {
            buttonModel: { content: 'OK', isPrimary: true, cssClass: 'e-flat' },
            click: () => dialogRef.current?.hide(),
          },
        ]}
      >
        The close button title is localized to <strong>{culture}</strong>
      </DialogComponent>
    </div>
  );
}
```

### Localized Header and Content

The close icon title is automatically localized based on the `locale` property. You can customize by changing locale:

```jsx
<DialogComponent
  header="Dialog Title"
  showCloseIcon={true}
  locale="de"  // German - close icon title becomes "Schließen"
>
  Content
</DialogComponent>
```

Note: `closeIconTitle` is not a valid DialogComponent property. Localization happens through the `locale` property.

### RTL Support

```jsx
<div dir="rtl" style={{ textAlign: 'right' }}>
  <DialogComponent
    header="حوار"  // Arabic "Dialog"
    showCloseIcon={true}
  >
    محتوى الحوار  {/* Dialog content in Arabic */}
  </DialogComponent>
</div>
```

## WCAG 2.2 Compliance

The Syncfusion Dialog component is built with accessibility in mind and supports WCAG 2.2 Level AA compliance:

### Compliance Features
- ✓ Perceivable: High contrast, semantic HTML
- ✓ Operable: Keyboard navigation, focus management
- ✓ Understandable: Clear labels, logical structure
- ✓ Robust: ARIA support, screen reader compatible

### Enable Accessibility

Ensure your implementation follows these patterns:

```jsx
// ✅ GOOD: Accessible dialog
<DialogComponent
  header="Confirmation"  // Clear, descriptive header
  showCloseIcon={true}   // Close button visible
  isModal={true}         // Clear focus scope
  buttons={[
    {
      buttonModel: { 
        content: 'OK', 
        isPrimary: true,
        id: 'confirm-btn'  // ID for testing
      },
      click: handleConfirm,
    },
  ]}
>
  <p>Clear, descriptive message</p>
</DialogComponent>
```

## Keyboard Interaction

The Dialog supports full keyboard navigation:

### Tab Navigation

- **Tab** - Move focus to next element
- **Shift + Tab** - Move focus to previous element
- **Focus cycling** - Tab cycles through all dialog elements

```jsx
<DialogComponent
  showCloseIcon={true}
  isModal={true}
>
  <input placeholder="First input" />
  <input placeholder="Second input" />
  <button>Action Button</button>
</DialogComponent>
```

**Keyboard flow:**
1. Tab: Header → Close button
2. Tab: Close button → First input
3. Tab: First input → Second input
4. Tab: Second input → Action button
5. Tab: Action button → Close button (cycles)

### Enter Key

- **Enter** on button - Activates button
- **Enter** on focused element - Activates it

```jsx
<DialogComponent buttons={[
  {
    buttonModel: { content: 'Submit', isPrimary: true },
    click: () => console.log('Submitted'),
  },
]}>
  <input autoFocus />  {/* Gets initial focus */}
</DialogComponent>
```

### Escape Key

- **Escape** - Closes the dialog (if not prevented with closeOnEscape={false})

```jsx
<DialogComponent
  closeOnEscape={true}  // Default: true - allows Escape key to close
  beforeClose={(e) => {
    if (e.isInteracted) {
      console.log('Dialog closed via Escape or close button');
    }
  }}
>
  Press Escape to close
</DialogComponent>

// To prevent Escape from closing:
<DialogComponent
  closeOnEscape={false}
>
  Escape key will not close this dialog
</DialogComponent>
```

### Arrow Keys (in Calendar Views)

Not typically used in Dialog, but custom content can handle them.

## ARIA Attributes

The Dialog automatically includes ARIA attributes. Enhance with custom attributes:

### Dialog ARIA Roles

The DialogComponent automatically includes proper ARIA attributes:

```jsx
<DialogComponent
  header="Confirmation"
  // ARIA attributes added automatically:
  // role="dialog"
  // aria-modal="true"
  // header text becomes aria-label
>
  Content
</DialogComponent>
```

The `header` property automatically becomes the `aria-label` for the dialog.

### Labeling Dialog

The header text serves as the ARIA label:

```jsx
<DialogComponent
  header="Are you sure?"  // Becomes aria-label
  isModal={true}
>
  This action will delete the item
</DialogComponent>
```

### Button Labeling

Buttons automatically get aria-labels from their content:

```jsx
const buttons = [
  {
    buttonModel: {
      content: 'Delete',  // Becomes aria-label
      id: 'delete-btn'
    },
    click: () => {},
  },
];

// HTML output:
// <button id="delete-btn">Delete</button>
// aria-label is auto-generated from content
```

### Semantic Content Structure

Use semantic HTML inside dialog content for better accessibility:

```jsx
<DialogComponent
  header="User Settings"
>
  <div>
    <h2>Customize Your Settings</h2>
    <p>Adjust your preferences below</p>
    <form>
      <label htmlFor="username">Username:</label>
      <input id="username" type="text" />
      
      <label htmlFor="email">Email:</label>
      <input id="email" type="email" />
    </form>
  </div>
</DialogComponent>
```

**Note:** Don't add `aria-label` prop directly to DialogComponent - use semantic header and content structure instead.

## Screen Reader Support

### Testing with Screen Readers

**NVDA (Windows - Free):**
- Download from https://www.nvaccess.org/
- Start NVDA and navigate dialog with arrow keys

**JAWS (Windows):**
- Professional screen reader
- Navigate with arrow keys and shortcuts

**VoiceOver (macOS/iOS):**
- Built-in; enable: System Preferences → Accessibility → VoiceOver
- Navigate with VO (Control + Option) + arrow keys

**TalkBack (Android):**
- Built-in accessibility feature
- Enable: Settings → Accessibility → TalkBack

### Accessible Dialog Example

```jsx
export function AccessibleDialog() {
  const dialogRef = useRef(null);

  const buttons = [
    {
      buttonModel: {
        content: 'Confirm',
        isPrimary: true,
        cssClass: 'e-flat',
        id: 'confirm-btn'
      },
      click: () => {
        console.log('Confirmed');
        dialogRef.current?.hide();
      },
    },
    {
      buttonModel: {
        content: 'Cancel',
        cssClass: 'e-flat',
        id: 'cancel-btn'
      },
      click: () => dialogRef.current?.hide(),
    },
  ];

  return (
    <div id="dialog-target" style={{ position: 'relative' }}>
      <button 
        onClick={() => dialogRef.current?.show()}
      >
        Open Dialog
      </button>

      <DialogComponent
        ref={dialogRef}
        header="Confirm Action"
        buttons={buttons}
        showCloseIcon={true}
        isModal={true}
        target="#dialog-target"
      >
        <p>Please confirm that you want to proceed.</p>
      </DialogComponent>
    </div>
  );
}
```

## Focus Management

### Initial Focus

```jsx
const dialogRef = useRef(null);
const inputRef = useRef(null);

const handleOpen = () => {
  dialogRef.current?.show();
  // Move focus to specific element after dialog opens
  setTimeout(() => inputRef.current?.focus(), 0);
};

<DialogComponent
  ref={dialogRef}
  open={handleOpen}
>
  <input ref={inputRef} autoFocus placeholder="Gets focus" />
</DialogComponent>
```

### Trap Focus in Modal

```jsx
<DialogComponent
  isModal={true}
  closeOnEscape={true}
>
  {/* Focus is automatically trapped within modal */}
  <input placeholder="First" />
  <input placeholder="Second" />
  <button>Action</button>
</DialogComponent>
```

### Return Focus on Close

```jsx
const triggerButtonRef = useRef(null);

const handleClose = () => {
  dialogRef.current?.hide();
  // Return focus to trigger button
  triggerButtonRef.current?.focus();
};

<>
  <button
    ref={triggerButtonRef}
    onClick={() => dialogRef.current?.show()}
  >
    Open
  </button>

  <DialogComponent
    ref={dialogRef}
    beforeClose={handleClose}
  >
    Content
  </DialogComponent>
</>
```

## Testing Accessibility

### Manual Testing Checklist

- [ ] **Keyboard Navigation**: Can you navigate all elements with Tab/Shift+Tab?
- [ ] **Escape Key**: Does Escape close the dialog?
- [ ] **Enter Key**: Do buttons activate with Enter?
- [ ] **Focus Visible**: Is focus indicator clearly visible?
- [ ] **Initial Focus**: Does focus go to appropriate element on open?
- [ ] **Modal Trap**: Does Tab cycle within modal, not parent?
- [ ] **Labels**: Does every control have clear label/text?
- [ ] **Color**: Is content visible without relying on color alone?

### Automated Testing with Axe

```bash
npm install --save-dev @axe-core/react
```

```jsx
import { axe } from '@axe-core/react';

export function AccessibilityTest() {
  const dialogRef = useRef(null);

  React.useEffect(() => {
    axe(document).then(results => {
      if (results.violations.length) {
        console.error('Accessibility violations:', results.violations);
      }
    });
  }, []);

  return (
    <div id="dialog-target">
      <DialogComponent ref={dialogRef}>
        Content to test
      </DialogComponent>
    </div>
  );
}
```

### Testing with Jest and Testing Library

```jsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('Dialog is keyboard accessible', async () => {
  const user = userEvent.setup();
  render(
    <DialogComponent header="Test">
      <button>Action</button>
    </DialogComponent>
  );

  // Tab to button
  await user.keyboard('{Tab}');
  expect(screen.getByRole('button', { name: /Action/i })).toHaveFocus();

  // Press Enter
  await user.keyboard('{Enter}');
  // Verify action occurred
});
```

## Best Practices Summary

### ✅ DO
- Use semantic HTML in dialog content
- Provide clear, descriptive headers
- Include close button (showCloseIcon={true})
- Support keyboard navigation
- Test with actual screen readers
- Use ARIA labels for custom content
- Manage focus appropriately
- Provide high contrast colors

### ❌ DON'T
- Use color alone to convey information
- Make interactive elements too small
- Trap keyboard focus in modeless dialogs
- Use auto-playing audio/video
- Disable default keyboard shortcuts
- Create nested focus traps
- Forget to test on real devices

**Next:** Choose another reference topic based on your needs.
