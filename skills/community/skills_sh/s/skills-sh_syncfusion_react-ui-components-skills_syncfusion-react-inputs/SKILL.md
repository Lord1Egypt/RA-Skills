---
name: syncfusion-react-inputs
description: Comprehensive guide for implementing Syncfusion React input components including Uploader, NumericTextBox, TextBox, TextArea, CheckBox, OTP Input, Signature, RangeSlider, ColorPicker, MaskedTextBox, and Rating. Use this when building file upload UIs with async/chunk uploads, drag-and-drop functionality, numeric inputs with validation and formatting, text inputs with floating labels, custom adornments, form integration, accessibility compliance, and styling in React applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Inputs"
---

# Implementing Syncfusion React Inputs

## Uploader

The Syncfusion React **UploaderComponent** provides a rich file upload control with async upload, drag-and-drop, chunk upload with pause/resume/cancel, validation, templates, form integration, and accessibility support.

### Navigation Guide

> 🛑 **Agentic use:** Do not execute multiple steps autonomously. Confirm with the user before each action (install, run, file creation).

#### Getting Started
📄 **Read:** [references/getting-started.md](references/uploader-getting-started.md)
- Installing `@syncfusion/ej2-react-inputs` 🛑 *STOP — Do not install packages autonomously. Ask the user to run: `npm install @syncfusion/ej2-react-inputs`. Verify with `npm audit`*
- License registration
- Basic `UploaderComponent` usage in JSX/TSX
- CSS theme imports
- Drop area configuration
- Success and failure event handling

#### Asynchronous Upload
📄 **Read:** [references/async-upload.md](references/uploader-async-upload.md)
- `asyncSettings` with `saveUrl` and `removeUrl`
- Multiple vs. single file upload (`multiple`)
- Auto upload vs. manual upload (`autoUpload`)
- Sequential upload (`sequentialUpload`)
- Preloaded files (`files` property)
- Adding custom HTTP headers via `uploading`/`removing` events
- Server-side save/remove action examples

#### Chunk Upload
📄 **Read:** [references/chunk-upload.md](references/uploader-chunk-upload.md)
- Enabling chunk upload with `asyncSettings.chunkSize`
- Retry configuration (`retryCount`, `retryAfterDelay`)
- Pause and resume chunked uploads (`pause`, `resume` methods)
- Cancel uploads (`cancel` method)
- `chunkSuccess` and `chunkFailure` events
- Server-side chunk handling (C#)

#### Validation
📄 **Read:** [references/validation.md](references/uploader-validation.md)
- Allowed file extensions (`allowedExtensions`)
- File size limits (`minFileSize`, `maxFileSize`)
- Maximum file count using `selected` event
- Duplicate file prevention
- Drag-and-drop image validation

#### File Sources
📄 **Read:** [references/file-source.md](references/uploader-file-source.md)
- Clipboard paste upload
- Directory/folder upload (`directoryUpload`)
- Drag-and-drop with custom drop area (`dropArea`)
- Customizing drop area appearance

#### Templates and Customization
📄 **Read:** [references/template-customization.md](references/uploader-template-customization.md)
- File list `template` property
- Custom upload UI with `showFileList: false`
- Customizing action buttons (`buttons` property)
- Progress bar customization
- Hiding the default drop area
- Style and appearance overrides

#### Advanced How-To Scenarios
📄 **Read:** [references/advanced-how-to.md](references/uploader-advanced-how-to.md)
- Programmatic file upload (`upload` method, `getFilesData`)
- Invisible/background upload
- Image preview before uploading
- Resize images before upload
- Sort selected files
- Check file size / MIME type before upload
- Confirm dialog before file removal
- Open/edit uploaded files
- Trigger file browser from external button
- Convert uploaded image to binary
- JWT authentication for secure upload ⚠️ *Never hardcode tokens. Retrieve from a secure session store at runtime. Do not log request headers or token values.*
- Form support (HTML form, template-driven, reactive)
- Localization (custom locale strings)
- Accessibility and keyboard navigation

#### API Reference
📄 **Read:** [references/api.md](references/uploader-api.md)
- All properties (`allowedExtensions`, `asyncSettings`, `autoUpload`, `buttons`, `cssClass`, `directoryUpload`, `dropArea`, `dropEffect`, `enabled`, `files`, `htmlAttributes`, `locale`, `maxFileSize`, `minFileSize`, `multiple`, `sequentialUpload`, `showFileList`, `template`, and more)
- All methods (`upload`, `remove`, `cancel`, `pause`, `resume`, `retry`, `clearAll`, `getFilesData`, `bytesToSize`, `createFileList`, `sortFileList`)
- All events (`uploading`, `success`, `failure`, `selected`, `removing`, `change`, `progress`, `chunkSuccess`, `chunkFailure`, `chunkUploading`, `actionComplete`, `beforeRemove`, `beforeUpload`, `canceling`, `clearing`, `fileListRendering`, `pausing`, `resuming`, `created`)

### Quick Start Example

```tsx
import { UploaderComponent } from '@syncfusion/ej2-react-inputs';
import '@syncfusion/ej2-base/styles/material.css';
import '@syncfusion/ej2-buttons/styles/material.css';
import '@syncfusion/ej2-inputs/styles/material.css';
import '@syncfusion/ej2-popups/styles/material.css';
import '@syncfusion/ej2-react-inputs/styles/material.css';

function App() {
  // ⚠️ Replace with your own server-side endpoints.
  // Never use third-party demo URLs in production — files will be sent to that external server.
  const asyncSettings = {
    saveUrl: '/api/upload/save',
    removeUrl: '/api/upload/remove'
  };

  const onSuccess = (args: any) => {
    console.log('Upload operation:', args.operation, 'File:', args.file.name);
  };

  const onFailure = (args: any) => {
    console.error('Upload failed:', args.file.name);
  };

  return (
    <UploaderComponent
      asyncSettings={asyncSettings}
      autoUpload={false}
      success={onSuccess}
      failure={onFailure}
    />
  );
}
```

### Common Patterns

#### Auto Upload with Validation
```tsx
<UploaderComponent
  asyncSettings={{ saveUrl: '/api/upload/save', removeUrl: '/api/upload/remove' }}
  allowedExtensions=".pdf,.doc,.docx"
  maxFileSize={5000000}
  multiple={true}
/>
```

#### Manual Upload with Custom Buttons
```tsx
<UploaderComponent
  asyncSettings={{ saveUrl: '/api/upload/save', removeUrl: '/api/upload/remove' }}
  autoUpload={false}
  buttons={{ browse: 'Choose File', clear: 'Clear All', upload: 'Upload All' }}
/>
```

#### Chunk Upload for Large Files
```tsx
<UploaderComponent
  asyncSettings={{
    saveUrl: '/api/upload/save',
    removeUrl: '/api/upload/remove',
    chunkSize: 500000   // 500 KB chunks
  }}
/>
```

### Key Decision Guide

| Need | Property/Event |
|---|---|
| Server URLs | `asyncSettings.saveUrl` + `asyncSettings.removeUrl` |
| Auto vs manual upload | `autoUpload` (default: `true`) |
| Large file upload | `asyncSettings.chunkSize` |
| Restrict file types | `allowedExtensions` |
| Limit file size | `maxFileSize` / `minFileSize` |
| Preload files from server | `files` prop |
| Upload one at a time | `sequentialUpload: true` |
| Entire folder upload | `directoryUpload: true` |
| Custom drop target | `dropArea` |
| Custom file list UI | `template` or `showFileList: false` |
| Add auth headers | `uploading` event → `args.currentRequest.setRequestHeader()` |
| Send extra form data | `uploading` event → `args.customFormData` |

## NumericTextBox

The Syncfusion React **NumericTextBoxComponent** is a specialized input control for numeric data entry with support for number formatting (currency, percentage, scientific notation), min/max range validation, spin buttons, decimal precision control, internationalization, RTL languages, and full WCAG 2.2 accessibility compliance.

### Documentation & Navigation Guide

> 🛑 **Agentic use:** Do not execute multiple steps autonomously. Confirm with the user before each action (install, run, file creation).

When the user needs help with NumericTextBox, guide them to the appropriate reference:

#### Getting Started
📄 **Read:** [references/getting-started.md](references/numerictextbox-getting-started.md)
- Installation and package setup
- CSS imports and themes
- React component import and basic JSX
- Creating your first NumericTextBox
- Running the application

#### Formats & Validation
📄 **Read:** [references/formats-and-validation.md](references/numerictextbox-formats-and-validation.md)
- Standard format specifiers (currency, percentage, number, scientific)
- Custom number formats with # and 0 patterns
- Range validation with min and max properties
- strictMode for enforcing valid ranges
- Real-world formatting examples

#### Spin Buttons & Step Control
📄 **Read:** [references/spin-buttons-and-step.md](references/numerictextbox-spin-buttons-and-step.md)
- Enabling/disabling spin button arrows
- Step property for increment values
- Customizing spin button appearance and behavior
- Precision with step increments
- Keyboard shortcuts (Arrow Up/Down)

#### Adornments & Styling
📄 **Read:** [references/adornments-and-styling.md](references/numerictextbox-adornments-and-styling.md)
- Prefix and suffix text (units, currency symbols)
- CSS classes and custom styling
- Placeholder, disabled, and readonly states
- Focus and blur event handling
- Theme customization and appearance options

#### Precision & Decimals
📄 **Read:** [references/precision-decimals.md](references/numerictextbox-precision-decimals.md)
- decimals property for controlling decimal places
- validateDecimalOnType for real-time precision validation
- Maintaining trailing zeros in display
- Rounding behavior and edge cases
- Precision during input vs display

#### Two-Way Binding & Forms
📄 **Read:** [references/two-way-binding-forms.md](references/numerictextbox-two-way-binding-forms.md)
- Two-way value binding in React (value prop + onChange)
- Controlled component patterns
- React state management
- React Hook Form integration
- Form validation with NumericTextBox

#### Globalization & Accessibility
📄 **Read:** [references/globalization-accessibility.md](references/numerictextbox-globalization-accessibility.md)
- Internationalization and locale support
- Right-to-Left (RTL) language support
- WCAG 2.2 accessibility compliance
- Keyboard navigation and shortcuts
- Screen reader support with ARIA attributes
- Focus management and color contrast

#### API Reference
📄 **Read:** [references/api.md](references/numerictextbox-api.md)
- Complete properties reference (value, min, max, step, format, decimals, etc.)
- Methods reference (increment, decrement, getText, focusIn, focusOut, destroy, etc.)
- Events reference with full argument types (change, blur, focus, created, destroyed)

### Quick Start Example

Here's a minimal working example to get started:

```jsx
import React, { useState } from 'react';
import { NumericTextBoxComponent } from '@syncfusion/ej2-react-inputs';
import '@syncfusion/ej2-base/styles/material3.css';
import '@syncfusion/ej2-buttons/styles/material3.css';
import '@syncfusion/ej2-inputs/styles/material3.css';

export default function App() {
  const [value, setValue] = useState(10);

  return (
    <div style={{ padding: '20px' }}>
      <h3>Enter a Number</h3>
      <NumericTextBoxComponent
        value={value}
        onChange={(e) => setValue(e.value)}
        min={0}
        max={100}
        step={1}
      />
      <p>Current Value: {value}</p>
    </div>
  );
}
```

**Key points:**
- Import `NumericTextBoxComponent` from `@syncfusion/ej2-react-inputs`
- Import required CSS themes (material3 in this example)
- Use `value` prop for the current numeric value
- Use `onChange` event to update React state
- Add `min`, `max`, `step` for validation and controls

### Common Patterns

#### 1. Currency Input
```jsx
<NumericTextBoxComponent
  value={99.99}
  format="c2"
  min={0}
  placeholder="Enter amount"
/>
```

#### 2. Percentage Input
```jsx
<NumericTextBoxComponent
  value={50}
  format="p"
  min={0}
  max={100}
/>
```

#### 3. Integer-Only Input
```jsx
<NumericTextBoxComponent
  value={10}
  decimals={0}
  step={1}
  min={0}
/>
```

#### 4. Bounded Range with Validation
```jsx
<NumericTextBoxComponent
  value={25}
  min={0}
  max={100}
  strictMode={true}
  placeholder="0-100"
/>
```

#### 5. Form Field with Label
```jsx
<div>
  <label>Product Quantity:</label>
  <NumericTextBoxComponent
    value={qty}
    onChange={(e) => setQty(e.value)}
    min={1}
    step={1}
    prefix="Units: "
  />
</div>
```

### Key Properties Reference

| Property | Type | Purpose |
|----------|------|---------|
| `value` | number | Current numeric value |
| `min` | number | Minimum allowed value |
| `max` | number | Maximum allowed value |
| `step` | number | Increment/decrement step (default: 1) |
| `decimals` | number | Number of decimal places when focused |
| `format` | string | Number format (n2, c2, p2, e2, etc.) |
| `currency` | string | ISO 4217 currency code (e.g., 'USD', 'EUR') |
| `placeholder` | string | Placeholder text when empty |
| `floatLabelType` | FloatLabelType | Float label behavior ('Never', 'Always', 'Auto') |
| `readonly` | boolean | Prevent user input |
| `enabled` | boolean | Enable or disable the control (default: true) |
| `strictMode` | boolean | Enforce min/max validation (default: true) |
| `validateDecimalOnType` | boolean | Restrict decimal length during typing |
| `showSpinButton` | boolean | Show/hide spinner arrows (default: true) |
| `showClearButton` | boolean | Show/hide clear icon |
| `allowMouseWheel` | boolean | Enable mouse wheel increment/decrement (default: true) |
| `cssClass` | string | Additional CSS classes for custom styling |
| `width` | number \| string | Width of the component |

### Common Use Cases

**1. Shopping Cart - Quantity Input**
- Integer-only, min=1, step=1, spinner for easy adjustment

**2. Price Calculator - Currency Field**
- format="c2", min=0, prefix="$", two decimal places

**3. Rating or Score - 0-100 Range**
- min=0, max=100, strictMode=true, no decimals

**4. Discount Percentage**
- format="p", min=0, max=100, two decimal places

**5. Measurement Input**
- decimals=2, suffix=" cm", min=0, spinner for precision

**6. Financial Form**
- format="c2", validation, form integration, accessibility

### Next Steps

1. **Package requirement:** The packages `@syncfusion/ej2-react-inputs`, `@syncfusion/ej2-base`, and `@syncfusion/ej2-buttons` must be present in your project's `package.json`. Confirm they are already installed and that your lockfile (e.g., `package-lock.json` or `yarn.lock`) pins their versions for supply-chain integrity. When adding them, use an explicit version range such as `@syncfusion/ej2-react-inputs@^27.x.x` to avoid unpinned dependency risks.
2. **Getting Started reference:** For installation details and basic setup, see [references/getting-started.md](references/numerictextbox-getting-started.md).
3. **Choose your reference:** Based on your use case (formatting, validation, forms, etc.), navigate to the relevant reference section above.
4. **Review examples:** Each reference contains ready-to-use code samples that can be adapted to your requirements.
5. **Customize:** Modify the examples to fit your specific use case and application needs.

---

For detailed implementation guidance, navigate to the appropriate reference file above.

## TextBox

The TextBox component is a lightweight input control that captures user text input with support for floating labels, validation states, icons, and advanced features. This skill guides you through implementing, configuring, and customizing the TextBox component in React applications.

### Navigation Guide

> 🛑 **Agentic use:** Do not execute multiple steps autonomously. Confirm with the user before each action (install, run, file creation).

#### Getting Started
📄 **Read:** [references/getting-started.md](references/textbox-getting-started.md)
- Vite setup for React development
- Installing `@syncfusion/ej2-react-inputs` package 🛑 *STOP — Do not install packages autonomously. Ask the user to run: `npm install @syncfusion/ej2-react-inputs`. Pin a specific version (e.g., `@syncfusion/ej2-react-inputs@28.x.x`) and verify with `npm audit`*
- Adding CSS imports and themes
- Creating your first TextBox component
- Adding icons and floating labels
- Running the development server 🛑 *STOP — Do not start the dev server autonomously. Ask the user to run: `npm run dev`*

#### Features and Groups
📄 **Read:** [references/features-and-groups.md](references/textbox-features-and-groups.md)
- Floating label behavior (Never, Always, Auto)
- Icons with `addIcon()` method (prepend/append)
- Clear button with `showClearButton` property
- Rounded corner with `e-corner` CSS class
- Disabled state with `enabled={false}`
- Multi-line textbox creation
- TextBox with clear button and floating label combinations

#### Styling and Sizing
📄 **Read:** [references/styling-and-sizing.md](references/textbox-styling-and-sizing.md)
- Three predefined sizes: Normal, Small (`e-small`), Large (`e-bigger`)
- Applying size classes via `cssClass` property
- Rounded corner with `e-corner` CSS class
- CSS customization for TextBox wrapper and floating label
- Custom CSS classes and themes
- Responsive design patterns

#### Multiline TextBox
📄 **Read:** [references/multiline-textbox.md](references/textbox-multiline-textbox.md)
- Creating multiline/textarea inputs with `multiline={true}`
- Floating labels with multiline
- Auto-resizing textboxes
- Disabling resize functionality
- Limiting text length with `htmlAttributes={{ maxlength: '...' }}`
- Character counting and display

#### Validation and States
📄 **Read:** [references/validation-and-states.md](references/textbox-validation-and-states.md)
- Error, warning, and success validation states via `cssClass`
- Applying validation classes (`e-error`, `e-warning`, `e-success`)
- Disabled state with `enabled={false}` (not `disabled`)
- Read-only state with `readonly={true}`
- Differences between disabled and read-only
- Dynamic color changes based on values using `input` event

#### Advanced Features
📄 **Read:** [references/advanced-features.md](references/textbox-advanced-features.md)
- Adornments: `prependTemplate` and `appendTemplate` properties
- Interactive adornments (password toggle, delete button)
- React functional components with hooks
- `useState`, `useEffect`, `useRef`, `useReducer` integration
- Event handling (created, input, change events)
- Form validation patterns

#### Accessibility and Migration
📄 **Read:** [references/accessibility-and-migration.md](references/textbox-accessibility-and-migration.md)
- WCAG 2.2, Section 508, and WAI-ARIA compliance
- Screen reader support and ARIA attributes
- Right-to-Left (RTL) support with `enableRtl` property
- Keyboard navigation support
- Migrating from CSS TextBox to React component
- Before/after code comparison

#### API Reference
📄 **Read:** [references/api.md](references/textbox-api.md)
- All properties: `placeholder`, `floatLabelType`, `value`, `type`, `cssClass`, `multiline`, `showClearButton`, `enabled`, `readonly`, `enableRtl`, `enablePersistence`, `autocomplete`, `htmlAttributes`, `locale`, `width`, `prependTemplate`, `appendTemplate`
- Methods: `addIcon`, `addAttributes`, `removeAttributes`, `focusIn`, `focusOut`, `destroy`, `getPersistData`
- Events: `created`, `destroyed`, `change`, `input`, `focus`, `blur`

### Quick Start

#### Basic TextBox with Floating Label

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import './App.css';

export default function App() {
  return (
    <TextBoxComponent 
      placeholder="Enter your name" 
      floatLabelType="Auto"
    />
  );
}
```

#### TextBox with Icon

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useRef } from 'react';

export default function App() {
  const textboxRef = useRef(null);

  const handleCreate = () => {
    if (textboxRef.current) {
      textboxRef.current.addIcon('append', 'e-icons e-input-popup-date');
    }
  };

  return (
    <TextBoxComponent
      placeholder="Enter date"
      floatLabelType="Auto"
      ref={textboxRef}
      created={handleCreate}
    />
  );
}
```

#### TextBox with Clear Button

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function App() {
  return (
    <TextBoxComponent
      placeholder="Enter your email"
      floatLabelType="Auto"
      showClearButton={true}
    />
  );
}
```

#### Multiline TextBox

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function App() {
  return (
    <TextBoxComponent
      multiline={true}
      placeholder="Enter your address"
      floatLabelType="Auto"
    />
  );
}
```

### Common Patterns

#### Form with Validation States

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

export default function ValidationForm() {
  const [cssClass, setCssClass] = useState('');

  return (
    <div>
      <TextBoxComponent
        placeholder="Enter username"
        cssClass={cssClass}
        floatLabelType="Auto"
        input={(e: any) => {
          if (!e.value) setCssClass('');
          else if (e.value.length < 3) setCssClass('e-error');
          else if (e.value.length < 6) setCssClass('e-warning');
          else setCssClass('e-success');
        }}
      />
    </div>
  );
}
```

#### Password TextBox with Toggle

```tsx
import * as React from 'react';
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useRef, useState } from 'react';

export default function PasswordInput() {
  const textboxRef = useRef<TextBoxComponent>(null);
  const [isVisible, setIsVisible] = useState(false);

  const toggleVisibility = () => {
    if (textboxRef.current) {
      const newVisibility = !isVisible;
      textboxRef.current.type = newVisibility ? 'text' : 'password';
      setIsVisible(newVisibility);
    }
  };

  function appendTemplate(): JSX.Element {
    return (
      <>
        <span className="e-input-separator"></span>
        <span
          className={`e-icons ${isVisible ? 'e-eye-slash' : 'e-eye'}`}
          onClick={toggleVisibility}
          style={{ cursor: 'pointer' }}
        ></span>
      </>
    );
  }

  return (
    <TextBoxComponent
      ref={textboxRef}
      type="password"
      placeholder="Enter password"
      floatLabelType="Auto"
      appendTemplate={appendTemplate}
    />
  );
}
```

#### Email Input with Unit Label

```tsx
import * as React from 'react';
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function EmailInput() {
  function prependTemplate(): JSX.Element {
    return (
      <>
        <span className="e-icons e-user"></span>
        <span className="e-input-separator"></span>
      </>
    );
  }

  function appendTemplate(): JSX.Element {
    return (
      <>
        <span className="e-input-separator"></span>
        <span>.com</span>
      </>
    );
  }

  return (
    <TextBoxComponent
      type="email"
      placeholder="Enter email"
      floatLabelType="Auto"
      prependTemplate={prependTemplate}
      appendTemplate={appendTemplate}
    />
  );
}
```

#### Rounded Corner TextBox

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function RoundedCornerTextBox() {
  return (
    <TextBoxComponent
      placeholder="Enter Date"
      cssClass="e-corner"
    />
  );
}
```

#### Disabled TextBox

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function DisabledTextBox() {
  return (
    <TextBoxComponent
      placeholder="Enter Name"
      enabled={false}
    />
  );
}
```

#### RTL TextBox

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function RTLTextBox() {
  return (
    <TextBoxComponent
      placeholder="أدخل اسمك"
      floatLabelType="Auto"
      enableRtl={true}
    />
  );
}
```

#### Auto-sizing Multiline TextBox

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useRef } from 'react';

export default function AutoSizeTextbox() {
  const textboxRef = useRef(null);

  const handleInput = () => {
    if (textboxRef.current) {
      const elem = textboxRef.current.respectiveElement;
      elem.style.height = 'auto';
      elem.style.height = elem.scrollHeight + 'px';
    }
  };

  const handleCreate = () => {
    if (textboxRef.current) {
      textboxRef.current.addAttributes({ rows: 1 });
    }
    handleInput();
  };

  return (
    <TextBoxComponent
      multiline={true}
      placeholder="Enter your message"
      floatLabelType="Auto"
      ref={textboxRef}
      created={handleCreate}
      input={handleInput}
    />
  );
}
```

### Key Properties

| Property | Type | Purpose |
|----------|------|---------|
| `placeholder` | `string` | Hint text shown when input is empty |
| `floatLabelType` | `"Never" \| "Always" \| "Auto"` | Label animation behavior |
| `value` | `string` | Sets the content of the TextBox |
| `type` | `string` | Input type (`text`, `password`, `email`, `number`, etc.) |
| `multiline` | `boolean` | Convert to textarea for multi-line input |
| `showClearButton` | `boolean` | Display clear button when input has value |
| `cssClass` | `string` | Apply CSS classes for sizing/validation/appearance (e.g., `"e-error"`, `"e-small"`, `"e-corner"`) |
| `enabled` | `boolean` | Enable (`true`) or disable (`false`) input interaction |
| `readonly` | `boolean` | Allow selection but prevent editing |
| `enableRtl` | `boolean` | Enable right-to-left rendering |
| `enablePersistence` | `boolean` | Persist value state between page reloads ⚠️ *Stores data in browser storage — enable only with explicit user consent* |
| `autocomplete` | `string` | Control browser autocomplete (`"on"` \| `"off"`) |
| `htmlAttributes` | `{ [key: string]: string }` | Pass additional HTML attributes (e.g., `{ maxlength: '200' }`) |
| `locale` | `string` | Override global culture/localization value |
| `width` | `number \| string` | Set component width |
| `prependTemplate` | `() => JSX.Element` | Render element before input |
| `appendTemplate` | `() => JSX.Element` | Render element after input |

### Key Events

| Event | Arguments | Purpose |
|-------|-----------|---------|
| `created` | `Object` | Fires after component initialization |
| `destroyed` | `Object` | Fires when component is destroyed |
| `change` | `ChangedEventArgs` | Fires when value changes on focus-out |
| `input` | `InputEventArgs` | Fires on every keystroke |
| `focus` | `FocusInEventArgs` | Fires when TextBox gains focus |
| `blur` | `FocusOutEventArgs` | Fires when TextBox loses focus |

### Related Documentation

> **ℹ️ External links below are for manual reference only.** Do not auto-fetch these URLs in an agentic pipeline without explicit user consent.

- [Syncfusion React TextBox Component Demo](https://ej2.syncfusion.com/react/demos/#/tailwind3/textboxes/default) *(external)*
- [React TextBox API Reference](https://ej2.syncfusion.com/react/documentation/api/textbox/) *(external)*
- [Syncfusion React Inputs Package](https://www.npmjs.com/package/@syncfusion/ej2-react-inputs) *(external — verify before installing)*
- [React Functional Components](./references/textbox-advanced-features.md)

## CheckBox

The Syncfusion React `CheckBoxComponent` is a graphical UI element that allows users to select one or more options. It supports **checked**, **unchecked**, and **indeterminate** states, flexible label positioning, size variants, full accessibility compliance, and rich CSS customization.

**Package:** `@syncfusion/ej2-react-buttons`

---

### Navigation Guide

> 🛑 **Agentic use:** Do not execute multiple steps autonomously. Confirm with the user before each action (install, run, file creation).

#### Getting Started
📄 **Read:** [references/getting-started.md](references/checkbox-getting-started.md)
- Installing `@syncfusion/ej2-react-buttons` 🛑 *STOP — Do not install packages autonomously. Ask the user to run: `npm install @syncfusion/ej2-react-buttons --save`. Verify with `npm audit`*
- CSS theme imports for Tailwind3
- Minimal `CheckBoxComponent` setup
- Running the Vite/React app 🛑 *STOP — Do not start the dev server autonomously. Ask the user to run: `npm run dev`*

#### States (Checked, Unchecked, Indeterminate, Disabled)
📄 **Read:** [references/states.md](references/checkbox-states.md)
- Setting `checked={true}` for checked state
- Setting `indeterminate={true}` for indeterminate state
- Setting `disabled={true}` for disabled state
- Combined state examples

#### Label and Size
📄 **Read:** [references/label-and-size.md](references/checkbox-label-and-size.md)
- `label` prop for caption text
- `labelPosition` (`"Before"` / `"After"`)
- Small size via `cssClass="e-small"`
- Default vs. small size examples

#### Style and Appearance
📄 **Read:** [references/style-and-appearance.md](references/checkbox-style-and-appearance.md)
- Available CSS classes for overriding checkbox styles
- Color variant customization (primary, success, warning, danger, info)
- Custom frame shapes (round checkbox)
- Custom check icon
- Theme Studio integration

#### Accessibility and RTL
📄 **Read:** [references/accessibility.md](references/checkbox-accessibility.md)
- WCAG 2.2 / Section 508 compliance
- WAI-ARIA attributes (`aria-disabled`)
- Keyboard navigation (Space key)
- Right-to-left (`enableRtl`) support
- Screen reader support

#### How-To Guides
📄 **Read:** [references/how-to.md](references/checkbox-how-to.md)
- Name and value in form submission
- Enabling right-to-left display
- Building customized checkbox variants

#### API Reference
📄 **Read:** [references/api.md](references/checkbox-api.md)
- All properties: `checked`, `cssClass`, `disabled`, `enableHtmlSanitizer`, `enablePersistence`, `enableRtl`, `htmlAttributes`, `indeterminate`, `label`, `labelPosition`, `locale`, `name`, `value`
- Methods: `click()`, `destroy()`, `focusIn()`
- Events: `change`, `created`

---

### Quick Start

```bash
npm install @syncfusion/ej2-react-buttons --save
# Then run: npm audit
```

```css
/* src/App.css */
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
```

```tsx
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <div>
      <CheckBoxComponent label="Accept Terms" />
    </div>
  );
}
export default App;
```

---

### Common Patterns

#### Controlled Checkbox with Change Handler
```tsx
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';
import { ChangeEventArgs } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  const [isChecked, setIsChecked] = React.useState(false);

  const handleChange = (args: ChangeEventArgs) => {
    setIsChecked(args.checked);
  };

  return (
    <CheckBoxComponent
      label="Subscribe to newsletter"
      checked={isChecked}
      change={handleChange}
    />
  );
}
export default App;
```

#### Parent / Children with Indeterminate State
```tsx
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  return (
    <ul>
      {/* Parent: indeterminate when some children are selected */}
      <li><CheckBoxComponent label="Select All" indeterminate={true} /></li>
      <li><CheckBoxComponent label="Option A" checked={true} /></li>
      <li><CheckBoxComponent label="Option B" /></li>
    </ul>
  );
}
export default App;
```

#### Form Submission with Name and Value
```tsx
import { CheckBoxComponent, ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  return (
    <form>
      <CheckBoxComponent name="hobby" value="Reading" label="Reading" checked={true} />
      <CheckBoxComponent name="hobby" value="Gaming" label="Gaming" />
      <ButtonComponent isPrimary={true}>Submit</ButtonComponent>
    </form>
  );
}
export default App;
```

---

### Key Props at a Glance

| Prop | Type | Default | Purpose |
|------|------|---------|---------|
| `label` | `string` | `''` | Caption text next to checkbox |
| `checked` | `boolean` | `false` | Checked state |
| `indeterminate` | `boolean` | `false` | Indeterminate (partial) state |
| `disabled` | `boolean` | `false` | Disabled state |
| `labelPosition` | `'Before' \| 'After'` | `'After'` | Label placement |
| `cssClass` | `string` | `''` | Custom CSS class(es) |
| `name` | `string` | `''` | Form field name |
| `value` | `string` | `''` | Form field value |
| `enableRtl` | `boolean` | `false` | Right-to-left rendering |
| `enablePersistence` | `boolean` | `false` | Persist state across reloads ⚠️ *Stores data in browser storage — enable only with explicit user consent* |

---

## Signature

The Syncfusion React `SignatureComponent` renders a canvas-based signature pad that captures smooth handwritten signatures using variable-width bezier curves. It supports drawing, saving (PNG/JPEG/SVG/base64/blob), loading existing signatures, undo/redo history, customizable stroke and background appearance, and full accessibility compliance.

**Package:** `@syncfusion/ej2-react-inputs`

---

### Navigation Guide

> 🛑 **Agentic use:** Do not execute multiple steps autonomously. Confirm with the user before each action (install, run, file creation).

#### Getting Started
📄 **Read:** [references/getting-started.md](references/signature-getting-started.md)
- Installing `@syncfusion/ej2-react-inputs` 🛑 *STOP — Do not install packages autonomously. Ask the user to run: `npm install @syncfusion/ej2-react-inputs --save`. Verify with `npm audit`*
- CSS theme imports (Tailwind3)
- Minimal `SignatureComponent` setup
- Running the application 🛑 *STOP — Do not start the dev server autonomously. Ask the user to run: `npm run dev`*

#### Customization
📄 **Read:** [references/customization.md](references/signature-customization.md)
- Stroke width: `maxStrokeWidth`, `minStrokeWidth`, `velocity`
- Stroke color: `strokeColor`
- Background color: `backgroundColor`
- Background image: `backgroundImage`

#### Open and Save
📄 **Read:** [references/open-save.md](references/signature-open-save.md)
- Load signature from base64 or URL (`load`)
- Save as base64 (`getSignature`)
- Save as Blob (`saveAsBlob`, `getBlob`)
- Save as image file — PNG, JPEG, SVG (`save`)
- Save with background (`saveWithBackground`)

#### User Interaction
📄 **Read:** [references/user-interaction.md](references/signature-user-interaction.md)
- Undo/redo strokes (`undo`, `redo`, `canUndo`, `canRedo`)
- Clear the canvas (`clear`, `isEmpty`)
- Disabled state (`disabled`)
- Read-only mode (`isReadOnly`)
- Draw text as signature (`draw`)
- Keyboard shortcuts (Ctrl+Z, Ctrl+Y, Ctrl+S, Delete)

#### Toolbar Integration
📄 **Read:** [references/toolbar-integration.md](references/signature-toolbar-integration.md)
- Integrating with Syncfusion `ToolbarComponent`
- Wiring undo, redo, clear, and save toolbar buttons
- Stroke color picker using `ColorPickerComponent`
- Background color picker integration
- Stroke width dropdown with `DropDownListComponent`
- Enabling/disabling toolbar buttons based on signature state

#### Accessibility
📄 **Read:** [references/accessibility.md](references/signature-accessibility.md)
- WCAG 2.2 / Section 508 compliance
- Keyboard interaction (Ctrl+Z, Ctrl+Y, Ctrl+S, Delete)
- Screen reader and mobile device support

#### API Reference
📄 **Read:** [references/api.md](references/signature-api.md)
- All properties: `backgroundColor`, `backgroundImage`, `disabled`, `enablePersistence`, `isReadOnly`, `maxStrokeWidth`, `minStrokeWidth`, `saveWithBackground`, `strokeColor`, `velocity`
- All methods: `canRedo`, `canUndo`, `clear`, `destroy`, `draw`, `getBlob`, `getSignature`, `isEmpty`, `load`, `redo`, `refresh`, `save`, `saveAsBlob`, `undo`
- Events: `beforeSave`, `change`, `created`

---

### Quick Start

```bash
npm install @syncfusion/ej2-react-inputs --save
# Then run: npm audit
```

```css
/* src/App.css */
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css";
```

```tsx
import { SignatureComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <div>
      <SignatureComponent id="signature" />
    </div>
  );
}
export default App;
```

---

### Common Patterns

#### Signature with Undo/Redo/Clear Controls
```tsx
import { SignatureComponent, SignatureChangeEventArgs } from '@syncfusion/ej2-react-inputs';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import { useRef } from 'react';

function App() {
  const sigRef = React.useRef<SignatureComponent>(null);
  const [canUndo, setCanUndo] = React.useState(false);
  const [canRedo, setCanRedo] = React.useState(false);
  const [isEmpty, setIsEmpty] = React.useState(true);

  function handleChange(args: SignatureChangeEventArgs) {
    if (sigRef.current) {
      setCanUndo(sigRef.current.canUndo());
      setCanRedo(sigRef.current.canRedo());
      setIsEmpty(sigRef.current.isEmpty());
    }
  }

  return (
    <div>
      <ButtonComponent disabled={!canUndo} onClick={() => sigRef.current?.undo()}>Undo</ButtonComponent>
      <ButtonComponent disabled={!canRedo} onClick={() => sigRef.current?.redo()}>Redo</ButtonComponent>
      <ButtonComponent disabled={isEmpty} onClick={() => sigRef.current?.clear()}>Clear</ButtonComponent>
      <SignatureComponent id="signature" ref={sigRef} change={handleChange} />
    </div>
  );
}
export default App;
```

#### Save Signature as PNG
```tsx
import { SignatureComponent } from '@syncfusion/ej2-react-inputs';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  const sigRef = React.useRef<SignatureComponent>(null);

  function saveSignature() {
    sigRef.current?.save('Png', 'MySignature');
  }

  return (
    <div>
      <SignatureComponent id="signature" ref={sigRef} />
      <ButtonComponent onClick={saveSignature}>Save as PNG</ButtonComponent>
    </div>
  );
}
export default App;
```

---

### Key Props at a Glance

| Prop | Type | Default | Purpose |
|------|------|---------|---------|
| `strokeColor` | `string` | `'#000000'` | Pen/stroke color (hex, rgb, or name) |
| `backgroundColor` | `string` | `''` | Canvas background color |
| `backgroundImage` | `string` | `''` | Canvas background image URL |
| `maxStrokeWidth` | `number` | `2` | Maximum stroke thickness |
| `minStrokeWidth` | `number` | `0.5` | Minimum stroke thickness |
| `velocity` | `number` | `0.7` | Controls stroke width variation |
| `disabled` | `boolean` | `false` | Disables the component |
| `isReadOnly` | `boolean` | `false` | Prevents drawing, allows focus |
| `saveWithBackground` | `boolean` | `true` | Include background when saving |
| `enablePersistence` | `boolean` | `false` | Persist state across page reloads ⚠️ *Stores signature data (biometric input) in browser storage — enable only with explicit user consent and applicable privacy disclosures* |

---

## OTP Input

A focused input component for collecting one-time passwords, PINs, and verification codes. Renders a configurable number of individual character input fields with full keyboard navigation, accessibility support, and visual styling modes.

### Quick Start

```tsx
import { OtpInputComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <div id="container">
      <OtpInputComponent id="otpinput" />
    </div>
  );
}

export default App;
```

**CSS (src/App.css):**
```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css";
```

**Install:**
```bash
npm install @syncfusion/ej2-react-inputs --save
```

### Common Patterns

#### 6-digit OTP with verification callback

```tsx
import { OtpInputComponent, OtpChangedEventArgs } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  const handleValueChanged = (args: OtpChangedEventArgs) => {
    console.log('Complete OTP:', args.value);
    // Call your API verification here
  };

  return (
    <OtpInputComponent
      id="otpinput"
      length={6}
      autoFocus={true}
      valueChanged={handleValueChanged}
    />
  );
}
```

#### Password-masked OTP with error state

```tsx
import { OtpInputComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <OtpInputComponent
      id="otpinput"
      type="password"
      length={6}
      cssClass="e-error"
      placeholder="*"
    />
  );
}
```

#### Alphanumeric OTP with separator

```tsx
import { OtpInputComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <OtpInputComponent
      id="otpinput"
      type="text"
      length={6}
      separator="-"
      textTransform="uppercase"
      stylingMode="filled"
    />
  );
}
```

### Key Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `length` | `number` | `4` | Number of OTP input fields |
| `value` | `string \| number` | `''` | Current OTP value |
| `type` | `'number' \| 'text' \| 'password'` | `'number'` | Input character type |
| `stylingMode` | `'outlined' \| 'filled' \| 'underlined'` | `'outlined'` | Visual style variant |
| `placeholder` | `string` | `''` | Hint character(s) per field |
| `separator` | `string` | `''` | Character between fields |
| `cssClass` | `string` | `''` | Custom/predefined CSS class (`e-success`, `e-warning`, `e-error`) |
| `disabled` | `boolean` | `false` | Disables user input |
| `autoFocus` | `boolean` | `false` | Auto-focuses on render |
| `enableRtl` | `boolean` | `false` | Right-to-left layout |
| `textTransform` | `'none' \| 'uppercase' \| 'lowercase'` | `'none'` | Case transformation |
| `ariaLabels` | `string[]` | `[]` | Per-field ARIA labels |
| `htmlAttributes` | `{ [key: string]: string }` | `{}` | Extra HTML attributes |

### Navigation Guide

#### Installation, Setup & Basic Usage
📄 **Read:** [references/getting-started.md](references/otp-input-getting-started.md)
- npm install and Vite project setup
- CSS theme imports
- Minimal working example
- Setting OTP length
- Setting a default value
- Auto-focus on load
- Troubleshooting

#### Input Types, Styling & Visual Configuration
📄 **Read:** [references/configuration.md](references/otp-input-configuration.md)
- Input types: number, text, password
- Styling modes: outlined, filled, underlined
- Placeholder text (single/per-field)
- Separator characters
- Disabled state
- CSS class customization (`e-success`, `e-warning`, `e-error`)
- RTL support
- Text transform (uppercase/lowercase)
- State persistence

#### Events & Interaction Handling
📄 **Read:** [references/events.md](references/otp-input-events.md)
- `created` event (post-render init)
- `focus` and `blur` events with `OtpFocusEventArgs`
- `input` event for real-time tracking with `OtpInputEventArgs`
- `valueChanged` event for OTP submission with `OtpChangedEventArgs`
- Programmatic focus via `focusIn()` / `focusOut()` methods
- Patterns: conditional submit button, verification feedback

#### Accessibility
📄 **Read:** [references/accessibility.md](references/otp-input-accessibility.md)
- WCAG 2.2, Section 508 compliance
- WAI-ARIA roles and attributes
- Keyboard navigation shortcuts
- Per-field `ariaLabels` configuration
- `htmlAttributes` for custom accessibility metadata
- RTL support
- Axe-core and accessibility-checker validation

#### Full API Reference
📄 **Read:** [references/api.md](references/otp-input-api.md)
- All properties with types, defaults, and examples
- Methods: `destroy()`, `focusIn()`, `focusOut()`
- All events and their argument interfaces
- Type enumerations: `OtpInputType`, `OtpInputStyle`, `TextTransform`
- Event argument interfaces: `OtpFocusEventArgs`, `OtpInputEventArgs`, `OtpChangedEventArgs`

### Decision Guide

**Which type to use?**
- User enters digits only → `type="number"` (default)
- User enters letters + digits → `type="text"`
- Input should be hidden/masked → `type="password"`

**Which event to use?**
- Trigger verification when OTP is fully entered → `valueChanged`
- Track partial input in real time → `input`
- Know when user clicks into/out of a field → `focus` / `blur`

**Which styling mode?**
- Standard forms → `outlined` (default)
- Card/dashboard UI → `filled`
- Material Design forms → `underlined`

**Visual feedback after verification?**
- Correct OTP → set `cssClass="e-success"`
- Wrong OTP → set `cssClass="e-error"`
- Pending/caution → set `cssClass="e-warning"`

## TextArea

The TextArea component enables efficient collection of multiline text input in forms and applications. It provides essential features for user feedback, comments, descriptions, and any scenario requiring extended text input.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/textarea-getting-started.md)
- Installation and npm setup
- Vite/React project configuration
- Basic TextArea implementation
- CSS imports and theming
- Getting and setting values with properties, state, and events

#### Core Features & Content
📄 **Read:** [references/value-and-content.md](references/textarea-value-and-content.md)
- Setting initial values with property and state
- Getting current value from textarea
- Value binding patterns
- Change detection and state management

#### Floating Labels & Placeholders
📄 **Read:** [references/floating-label.md](references/textarea-floating-label.md)
- Floating label types (Auto, Always, Never)
- Placeholder behavior during user interaction
- Localization with floating labels
- Placeholder text translations for different cultures

#### Adornments (Custom Elements)
📄 **Read:** [references/adornments.md](references/textarea-adornments.md)
- Adding icons, buttons, or text before/after textarea
- Prepend and append templates
- Adornment flow and orientation (horizontal/vertical)
- Common use cases: character count, formatting tools, validation icons

#### Form Integration
📄 **Read:** [references/form-support.md](references/textarea-form-support.md)
- HTML form submission with textarea
- Name attribute and form data
- FormValidator integration for validation rules
- Required fields, min/max length constraints
- Validation messaging and error states

#### Content Constraints
📄 **Read:** [references/max-length.md](references/textarea-max-length.md)
- Enforcing character limits with maxLength
- Preventing user input beyond limit
- User feedback on character restrictions
- Edge cases and best practices

#### Sizing & Dimensions
📄 **Read:** [references/rows-columns-sizing.md](references/textarea-rows-columns-sizing.md)
- Setting visible height with rows property
- Setting visible width with cols property
- Responsive sizing strategies
- Controlling textarea dimensions

#### Resize Behavior
📄 **Read:** [references/resize.md](references/textarea-resize.md)
- Resize modes: Vertical, Horizontal, Both, None
- User-controlled resizing
- Width customization
- Layout considerations for fixed-size textareas

#### Styling & Appearance
📄 **Read:** [references/styling-appearance.md](references/textarea-styling-appearance.md)
- Size classes (e-small, e-bigger)
- Filled and outline appearance modes
- Custom CSS with cssClass property
- Disabled and read-only states
- Validation state styling (success, warning, error)
- Clear button configuration
- Color customization and rounded corners

#### Events & User Interaction
📄 **Read:** [references/events.md](references/textarea-events.md)
- created: Initialization event
- input: Real-time value change detection
- change: Value change with focus-out
- focus: Focus gained
- blur: Focus lost
- destroyed: Component cleanup
- Event args and usage patterns

#### Methods & Programmatic Control
📄 **Read:** [references/methods.md](references/textarea-methods.md)
- focusIn(): Programmatically set focus
- focusOut(): Remove focus
- getPersistData(): Retrieve persistence state
- addAttributes(): Add HTML attributes dynamically
- removeAttributes(): Remove HTML attributes
- destroy(): Clean up component

#### Complete API Reference
📄 **Read:** [references/api.md](references/textarea-api.md)
- All properties with descriptions and defaults
- All methods with parameters and return types
- All events with arg types
- Type definitions and enums
- Usage examples for each API

### Quick Start

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  const [textValue, setTextValue] = React.useState('');

  const handleChange = (args) => {
    console.log('TextArea value changed:', args.value);
  };

  return (
    <div className='wrap'>
      <TextAreaComponent
        id='default'
        placeholder='Enter your comments'
        value={textValue}
        change={handleChange}
        floatLabelType='Auto'
        rows={5}
        cols={40}
      />
    </div>
  );
}

export default App;
```

### Common Patterns

#### Pattern 1: Form with Validation
```typescript
<TextAreaComponent
  name='comments'
  placeholder='Your feedback'
  floatLabelType='Auto'
  required={true}
  maxLength={500}
  showClearButton={true}
/>
```

#### Pattern 2: Controlled Component with State
```typescript
const [value, setValue] = React.useState('');

<TextAreaComponent
  value={value}
  input={(args) => setValue(args.value)}
/>
```

#### Pattern 3: Styled with Custom CSS
```typescript
<TextAreaComponent
  placeholder='Enter text'
  cssClass='e-outline e-small'
  floatLabelType='Auto'
/>
```

#### Pattern 4: Disabled & Read-Only States
```typescript
<TextAreaComponent placeholder='Disabled' enabled={false} />
<TextAreaComponent placeholder='Read-only' readonly={true} />
```

#### Pattern 5: With Adornments
```typescript
<TextAreaComponent
  placeholder='Message'
  prependTemplate={() => <span className='icon'>📝</span>}
  appendTemplate={() => <button>Send</button>}
/>
```

### Key Props Summary

| Prop | Purpose | Common Values |
|------|---------|----------------|
| `value` | Set/get textarea content | string |
| `placeholder` | Hint text | string |
| `rows` | Visible height in lines | 3-10 |
| `cols` | Visible width in characters | 30-80 |
| `floatLabelType` | Floating behavior | 'Auto', 'Always', 'Never' |
| `maxLength` | Character limit | number |
| `resizeMode` | User resizing | 'Both', 'Vertical', 'Horizontal', 'None' |
| `enabled` | Enable/disable input | boolean |
| `readonly` | Read-only mode | boolean |
| `cssClass` | Custom styling | 'e-outline', 'e-small', 'e-filled' |
| `showClearButton` | Display clear button | boolean |

## Slider (RangeSlider)

A comprehensive guide for implementing the Syncfusion Essential JS 2 `SliderComponent` in React applications. Supports single-value (`Default`), min-range fill (`MinRange`), and dual-handle range selection (`Range`) with tooltips, ticks, limits, color ranges, custom values, formatting, accessibility, events, and more.

**Package:** `@syncfusion/ej2-react-inputs`

### Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/range-slider-getting-started.md)
- Installation and package setup
- Basic implementation of three slider types
- CSS imports and theme setup
- Minimal working example
- Initial configuration

#### Types and Orientation
📄 **Read:** [references/types-and-orientation.md](references/range-slider-types-and-orientation.md)
- Three slider types: Default, MinRange, Range
- Understanding shadow/fill behavior
- Horizontal vs vertical orientation
- Type selection guide
- Code examples for each type

#### Tooltips and Ticks
📄 **Read:** [references/tooltips-and-ticks.md](references/range-slider-tooltips-and-ticks.md)
- Tooltip configuration and placement
- Tooltip visibility modes (Always, Focus, Click)
- Tick marks and scale display
- largeStep and smallStep configuration
- Small tick visibility
- Combined tooltip + ticks examples

#### Formatting and Limits
📄 **Read:** [references/formatting-and-limits.md](references/range-slider-formatting-and-limits.md)
- Value formatting (currency, percentages, custom formats)
- Using the format API
- Slider limits and restricted ranges
- Handle locking (start/end fixed)
- Min/max bounds per handle
- Edge cases and constraint handling

#### Styling and Customization
📄 **Read:** [references/styling.md](references/range-slider-styling.md)
- CSS selectors for track, handle, limits, ticks, buttons
- Customizing track color and height
- Handle styling (color, border, size)
- Theme integration and built-in themes
- CSS variable customization
- Advanced styling patterns

#### Accessibility
📄 **Read:** [references/accessibility.md](references/range-slider-accessibility.md)
- WCAG 2.2 and Section 508 compliance
- WAI-ARIA attributes and roles (`role="slider"`, `aria-valuemin`, `aria-valuemax`, `aria-valuenow`, `aria-orientation`)
- Keyboard navigation (Arrow keys, Home, End, Page Up/Down)
- Screen reader support and `aria-live` regions
- Focus management and color contrast requirements
- Mobile touch accessibility

#### Color Range
📄 **Read:** [references/color-range.md](references/range-slider-color-range.md)
- `colorRange` property and `ColorRangeDataModel` interface
- Three-zone and multi-zone patterns (red/amber/green)
- Color range with `Range` type (dual handles)
- Dynamic color zones based on runtime data
- Real-world: battery, risk, performance, score patterns
- Combining `colorRange` with `limits`, `ticks`, and `tooltip`

#### Events and Methods
📄 **Read:** [references/events-and-methods.md](references/range-slider-events-and-methods.md)
- `change` event — continuous value updates while dragging
- `changed` event — final committed value on drag release
- `created` event — post-render initialization
- `renderingTicks` — customize tick label text per tick
- `renderedTicks` — post-process tick DOM after all ticks render
- `tooltipChange` — customize tooltip display text
- `reposition()` method — when and how to call
- `destroy()` method — cleanup and removal
- React `ref` patterns for programmatic control
- Common patterns: API sync, conditional logic, live preview

#### API Reference
📄 **Read:** [references/api-reference.md](references/range-slider-api-reference.md)
- All official `SliderComponent` properties: `value`, `type`, `min`, `max`, `step`, `orientation`, `ticks`, `tooltip`, `limits`, `colorRange`, `customValues`, `showButtons`, `enableAnimation`, `enabled`, `readonly`, `cssClass`, `width`, `enableRtl`, `enablePersistence`, `enableHtmlSanitizer`, `locale`
- Official methods: `reposition()`, `destroy()`
- All official events with correct argument interfaces: `change`, `changed`, `created`, `renderingTicks`, `renderedTicks`, `tooltipChange`
- Interface: `TicksDataModel` — `placement` (`'Before'`/`'After'`/`'Both'`/`'None'`), `largeStep`, `smallStep`, `showSmallTicks`, `format`
- Interface: `TooltipDataModel` — `isVisible`, `placement`, `showOn` (`'Always'`/`'Focus'`/`'Click'`), `format`, `cssClass`
- Interface: `LimitDataModel` — `enabled`, `minStart`, `minEnd`, `maxStart`, `maxEnd`, `startHandleFixed`, `endHandleFixed`
- Interface: `ColorRangeDataModel` — `color`, `start`, `end`
- Interface: `SliderChangeEventArgs` — `value`, `previousValue`, `action`, `isInteracted`, `text`
- Interface: `SliderTickEventArgs` — `value`, `text`, `tickElement`
- Interface: `SliderTickRenderedEventArgs` — `ticksWrapper`, `tickElements`
- Interface: `SliderTooltipEventArgs` — `value`, `text`
- Enum: `SliderType` (`'Default'` | `'MinRange'` | `'Range'`)
- Enum: `SliderOrientation` (`'Horizontal'` | `'Vertical'`)

### Quick Start

#### Basic Single Value Slider

```tsx
import React from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';
import '@syncfusion/ej2-react-inputs/styles/material.css';

function App() {
  return (
    <div>
      <SliderComponent 
        id="slider" 
        value={30}
        min={0}
        max={100}
      />
    </div>
  );
}
export default App;
```

#### Range Slider (Two Handles)

```tsx
import React from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';
import '@syncfusion/ej2-react-inputs/styles/material.css';

function App() {
  const [range, setRange] = React.useState([30, 70]);

  return (
    <div>
      <SliderComponent 
        id="range-slider" 
        type="Range"
        value={range}
        change={(e) => setRange(e.value)}
        min={0}
        max={100}
      />
    </div>
  );
}
export default App;
```

#### Price Range Selector

```tsx
import React from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';
import '@syncfusion/ej2-react-inputs/styles/material.css';

function PriceRangeSelector() {
  const [priceRange, setPriceRange] = React.useState([100, 500]);
  
  const tooltip = {
    placement: 'Before',
    isVisible: true,
    format: 'C2'  // Currency format
  };

  return (
    <div>
      <h3>Price Range: ${priceRange[0]} - ${priceRange[1]}</h3>
      <SliderComponent 
        id="price-slider"
        type="Range"
        value={priceRange}
        change={(e) => setPriceRange(e.value)}
        min={0}
        max={1000}
        step={10}
        tooltip={tooltip}
      />
    </div>
  );
}
export default PriceRangeSelector;
```

### Common Patterns

#### Pattern 1: Single Value with Ticks
Use Default type for simple numeric selection with visual scale.

```tsx
<SliderComponent
  id="default-slider"
  value={40}
  min={0}
  max={100}
  step={5}
  ticks={{
    placement: 'After',
    largeStep: 20,
    smallStep: 5,
    showSmallTicks: true
  }}
/>
```

#### Pattern 2: Range with Fixed Limits
Use Range type with limits to restrict handle movement to specific areas.

```tsx
<SliderComponent
  id="limited-range"
  type="Range"
  value={[25, 75]}
  limits={{
    enabled: true,
    minStart: 10,
    minEnd: 40,
    maxStart: 60,
    maxEnd: 90
  }}
  tooltip={{ isVisible: true }}
/>
```

#### Pattern 3: Formatted Values (Currency)
Display values as currency using format API.

```tsx
<SliderComponent
  id="currency-slider"
  type="Range"
  value={[1000, 5000]}
  min={0}
  max={10000}
  step={100}
  tooltip={{
    isVisible: true,
    format: 'C0'  // Currency without decimals
  }}
  ticks={{
    placement: 'After',
    largeStep: 2000,
    format: 'C0'
  }}
/>
```

#### Pattern 4: Vertical Orientation
Display slider vertically for space-constrained layouts.

```tsx
<div style={{ height: '300px', width: '100px' }}>
  <SliderComponent
    id="vertical-slider"
    value={50}
    orientation="Vertical"
    tooltip={{ isVisible: true }}
  />
</div>
```

#### Pattern 5: With Increment/Decrement Buttons
Add buttons to manually adjust slider values.

```tsx
<SliderComponent
  id="button-slider"
  type="Range"
  value={[30, 70]}
  showButtons={true}
  tooltip={{ isVisible: true }}
/>
```

#### Pattern 6: Color Range (Zones)
Paint distinct color sections on the slider track using `colorRange`.

```tsx
import { ColorRangeDataModel } from '@syncfusion/ej2-react-inputs';

const colorRange: ColorRangeDataModel[] = [
  { color: '#ff4040', start: 0,  end: 33  },   // Low zone — red
  { color: '#ffb300', start: 34, end: 66  },   // Mid zone — amber
  { color: '#00c853', start: 67, end: 100 }    // High zone — green
];

<SliderComponent
  id="color-slider"
  type="MinRange"
  value={50}
  colorRange={colorRange}
  tooltip={{ isVisible: true, showOn: 'Always' }}
/>
```

#### Pattern 7: Custom Value Scale
Use non-numeric labels as slider values with `customValues`.

```tsx
<SliderComponent
  id="size-slider"
  customValues={['XS', 'S', 'M', 'L', 'XL', 'XXL']}
  value="M"
  tooltip={{ isVisible: true }}
/>
```

#### Pattern 8: Read-Only Display
Show a locked slider for informational display.

```tsx
<SliderComponent
  id="status-slider"
  type="MinRange"
  value={65}
  min={0}
  max={100}
  readonly={true}
  tooltip={{ isVisible: true, showOn: 'Always' }}
  ticks={{ placement: 'After', largeStep: 20 }}
/>
```

### Key Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `value` | `number \| number[]` | `null` | Single value or `[start, end]` array for Range type |
| `type` | `'Default' \| 'MinRange' \| 'Range'` | `'Default'` | Slider mode |
| `min` | `number` | `0` | Minimum selectable value |
| `max` | `number` | `100` | Maximum selectable value |
| `step` | `number` | `1` | Value increment/decrement per step |
| `orientation` | `'Horizontal' \| 'Vertical'` | `'Horizontal'` | Slider direction |
| `tooltip` | `TooltipDataModel` | `{ isVisible: false }` | Tooltip configuration |
| `ticks` | `TicksDataModel` | `{ placement: 'before' }` | Tick marks configuration |
| `limits` | `LimitDataModel` | `{ enabled: false }` | Thumb movement restrictions |
| `colorRange` | `ColorRangeDataModel[]` | `[]` | Color zones on the track |
| `customValues` | `string[] \| number[]` | `null` | Custom value scale (ignores min/max/step) |
| `showButtons` | `boolean` | `false` | Show +/- increment/decrement buttons |
| `enabled` | `boolean` | `true` | Enable or disable the slider |
| `readonly` | `boolean` | `false` | Read-only display mode |
| `enableRtl` | `boolean` | `false` | Right-to-left layout |
| `width` | `number \| string` | `null` | Slider element width |
| `cssClass` | `string` | `''` | Custom CSS classes on root element |

### Type Comparison

| Type | Handles | Fill Behavior | Use Case |
|------|---------|---------------|----------|
| **Default** | 1 | No fill | Simple numeric selection |
| **MinRange** | 1 | Fill from min | Visual progress/level indicator |
| **Range** | 2 | Fill between handles | Min/max range selection |

### Common Use Cases

#### Budget Range Selector
Select min and max budget with step increments and currency formatting.
→ Use `type="Range"`, `step={50}`, format `'C0'`, tooltip enabled

#### Time Range Picker
Select time window (hours, minutes, days).
→ Use `type="Range"`, custom formatting via `renderingTicks` event

#### Volume/Brightness Control
Single handle adjustment with immediate feedback.
→ Use `type="Default"`, no ticks, always-visible tooltip

#### Score/Rating Range
MinRange mode with shadow showing current level.
→ Use `type="MinRange"`, `min={0}`, `max={10}`, step-based

#### Product Filter
Multiple product categories with price ranges.
→ Use `type="Range"`, limits for each category, event handlers

### Events

| Event | Trigger | Usage |
|-------|---------|-------|
| `created` | Component created and rendered | One-time setup operations |
| `change` | Value changing while dragging | Real-time feedback (continuous) |
| `changed` | Drag complete (thumb released) | Capture final committed value |
| `tooltipChange` | Tooltip about to render | Custom tooltip text formatting |
| `renderingTicks` | Each tick being rendered | Custom tick label text |
| `renderedTicks` | All ticks rendered | Post-process tick DOM elements |

> **⚠️ Note:** The official event for continuous updates while dragging is `change`, not `changing`. The event fired after drag completes is `changed`. Do NOT use `onChange` prop (that is a React native input prop). Use `change` and `changed` directly.

### Troubleshooting Quick Links

**Component not displaying?** → Check CSS imports and theme in [getting-started.md](references/range-slider-getting-started.md)

**Values not updating?** → Use `change` (continuous) or `changed` (on release) events — NOT `onChange`

**Formatting not working?** → See format API examples in [formatting-and-limits.md](references/range-slider-formatting-and-limits.md)

**Accessibility issues?** → Refer to [accessibility.md](references/range-slider-accessibility.md) for ARIA and keyboard support

**Vertical slider not rendering?** → Wrap in a container with explicit `height` (e.g., `style={{ height: '300px' }}`)

**Range type with single value?** → Always pass `value={[start, end]}` array for `type="Range"`

**Color zones not showing?** → Check `colorRange` array has valid `start`/`end`/`color` properties

### Next Steps

1. Choose your slider type based on use case (`Default`, `MinRange`, or `Range`)
2. Read [getting-started.md](references/range-slider-getting-started.md) for installation
3. Navigate to specific reference for your feature needs
4. Test with examples from reference files
5. Customize styling using [styling.md](references/range-slider-styling.md)
6. Ensure accessibility following [accessibility.md](references/range-slider-accessibility.md)
7. Verify all API usage against [api-reference.md](references/range-slider-api-reference.md)

> **⚠️ Critical:** Only use APIs explicitly listed in [references/api-reference.md](references/range-slider-api-reference.md). Do **not** reference `onChange` (use `change`/`changed`), `toggle()`, `open()`, `close()`, or any undocumented methods.

## ColorPicker

The Syncfusion React ColorPicker lets users pick colors via a visual picker (HSV + opacity) or a palette of swatches. It renders as a SplitButton by default (opens a popup) or inline, and supports RGB, HSV, and Hex color formats.

**Package:** `@syncfusion/ej2-react-inputs`  
**Component:** `<ColorPickerComponent>`

### Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/colorpicker-getting-started.md)
- Installation with Vite or Create React App
- npm package setup
- CSS theme imports
- Minimal working example
- Running the application

#### Modes and Color Value
📄 **Read:** [references/modes-and-value.md](references/colorpicker-modes-and-value.md)
- Inline rendering vs popup (SplitButton)
- Picker mode vs Palette mode
- Setting initial color value (hex codes)
- Opacity support
- Rendering palette alone (locking mode)

#### Palette Features
📄 **Read:** [references/palette-features.md](references/colorpicker-palette-features.md)
- Custom color palettes (`presetColors`)
- Custom palette tile rendering (`beforeTileRender`)
- No-color / clear color support (`noColor`)
- Custom no-color option
- Recent colors display (`showRecentColors`)
- Palette column count (`columns`)

#### UI Customization
📄 **Read:** [references/ui-customization.md](references/colorpicker-ui-customization.md)
- Hide the input value area
- Custom picker handle
- Custom primary button with icon
- Display hex code in input element
- Hide control buttons (Apply/Cancel)
- CSS class overrides and Theme Studio
- Excel-like custom UI with SplitButton and Dialog

#### Integration and Advanced
📄 **Read:** [references/integration-and-advanced.md](references/colorpicker-integration-and-advanced.md)
- Embedding ColorPicker in a DropDownButton
- Popup toggle control
- State persistence across page reloads
- Mode switcher visibility and events
- Disabled state

#### Localization and RTL
📄 **Read:** [references/localization-and-rtl.md](references/colorpicker-localization-and-rtl.md)
- Localizing Apply / Cancel / ModeSwitcher labels
- Loading translation objects with `L10n`
- Right-to-left rendering (`enableRtl`)

#### Accessibility
📄 **Read:** [references/accessibility.md](references/colorpicker-accessibility.md)
- WCAG 2.2 / Section 508 compliance
- WAI-ARIA attributes
- Keyboard navigation shortcuts
- Accessibility validation

#### API Reference
📄 **Read:** [references/api.md](references/colorpicker-api.md)
- All properties with types and defaults
- All methods with signatures
- All events with payload types

---

### Quick Start

```bash
npm install @syncfusion/ej2-react-inputs --save
```

```css
/* src/App.css */
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-inputs/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-splitbuttons/styles/tailwind3.css";
```

```tsx
import { ColorPickerComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <div id="container">
      <div className="wrap">
        <h4>Choose Color</h4>
        <ColorPickerComponent id="color-picker" />
      </div>
    </div>
  );
}
export default App;
```

---

### Common Patterns

#### Inline picker (no popup)
```tsx
<ColorPickerComponent inline={true} showButtons={false} />
```

#### Palette-only mode
```tsx
<ColorPickerComponent mode="Palette" modeSwitcher={false} showButtons={false} />
```

#### Set initial color + handle changes
```tsx
import { ColorPickerEventArgs } from '@syncfusion/ej2-react-inputs';

function App() {
  function onChange(args: ColorPickerEventArgs): void {
    console.log(args.currentValue.hex);  // e.g. "#ff5733"
    console.log(args.currentValue.rgba); // e.g. "rgba(255,87,51,1)"
  }
  return <ColorPickerComponent value="#ff5733" change={onChange} />;
}
```

#### Custom palette with preset colors
```tsx
const presets: { [key: string]: string[] } = {
  'brand': ['#0078d4', '#106ebe', '#005a9e', '#004578'],
  'accents': ['#e81123', '#ff8c00', '#00b294', '#68217a']
};

<ColorPickerComponent
  mode="Palette"
  presetColors={presets}
  columns={4}
  modeSwitcher={false}
  inline={true}
  showButtons={false}
/>
```

#### Disable opacity slider
```tsx
<ColorPickerComponent enableOpacity={false} />
```

#### No-color support (clear selection)
```tsx
<ColorPickerComponent
  mode="Palette"
  noColor={true}
  modeSwitcher={false}
  showButtons={false}
/>
```

#### Localization (German)
```tsx
import { L10n } from '@syncfusion/ej2-base';

L10n.load({
  'de-DE': {
    'colorpicker': { Apply: 'Anwenden', Cancel: 'Abbrechen', ModeSwitcher: 'Modus wechseln' }
  }
});

<ColorPickerComponent locale="de-DE" />
```

---

### Key Props

| Prop | Type | Default | Purpose |
|------|------|---------|---------|
| `value` | `string` | `'#008000ff'` | Initial color (3/4/6/8 digit hex) |
| `mode` | `'Picker' \| 'Palette'` | `'Picker'` | Which panel to show initially |
| `inline` | `boolean` | `false` | Render component directly (no popup) |
| `showButtons` | `boolean` | `true` | Show Apply/Cancel buttons |
| `modeSwitcher` | `boolean` | `true` | Show mode switcher button |
| `noColor` | `boolean` | `false` | Add a "no color" tile to palette |
| `presetColors` | `object` | `null` | Custom color groups for palette |
| `columns` | `number` | `10` | Palette columns count |
| `enableOpacity` | `boolean` | `true` | Show opacity slider |
| `showRecentColors` | `boolean` | `false` | Show recent color tiles (palette only) |
| `disabled` | `boolean` | `false` | Disable the component |
| `cssClass` | `string` | `''` | Custom CSS class on root element |
| `enableRtl` | `boolean` | `false` | Right-to-left rendering |
| `locale` | `string` | `''` | Locale string for localization |

## MaskedTextBox

The Syncfusion React MaskedTextBox component enforces a specific input format by applying a mask pattern, guiding users to enter data in the correct structure. It is ideal for phone numbers, postal codes, dates, IP addresses, product keys, and any scenario where input must follow a predefined format.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/maskedtextbox-getting-started.md)
- Installation via npm (`@syncfusion/ej2-react-inputs`)
- Vite / Create-React-App setup
- CSS imports for theming
- Rendering a basic MaskedTextBox
- Setting the `mask` property for format enforcement

#### Mask Configuration
📄 **Read:** [references/mask-configuration.md](references/maskedtextbox-mask-configuration.md)
- Standard mask element tokens (0, 9, #, L, ?, &, C, A, a, <, >, |, \)
- Custom characters via `customCharacters` property
- Regular expression masks for flexible patterns (e.g., IP addresses)
- Prompt character customization via `promptChar`

#### Adornments (Prepend / Append Elements)
📄 **Read:** [references/adornments.md](references/maskedtextbox-adornments.md)
- Adding icons or buttons before/after the input with `prependTemplate` and `appendTemplate`
- Entry guidance, quick actions, and context labels
- Class and functional component examples

#### React Hooks Integration
📄 **Read:** [references/react-hooks.md](references/maskedtextbox-react-hooks.md)
- Controlled component with `useState`
- Auto-focus on mount using `useEffect` + `useRef` + `focusIn()`
- Multiple masked inputs with `useReducer`
- Handling the `change` event in functional components

#### Style, Appearance & Customization
📄 **Read:** [references/style-and-customization.md](references/maskedtextbox-style-and-customization.md)
- Custom styling with `cssClass`
- CSS overrides for wrapper, hover, and focus states
- Setting cursor position on focus using the `focus` event (`selectionStart`, `selectionEnd`)
- Displaying numeric keypad on mobile with `type="tel"`
- `floatLabelType` options (Never, Always, Auto)

#### Form Validation
📄 **Read:** [references/form-validation.md](references/maskedtextbox-form-validation.md)
- Integrating with Syncfusion `FormValidator`
- Defining custom validation rules using `ej2_instances`
- Custom error placement with `customPlacement`
- Checking for incomplete masked values using `promptChar`

#### API Reference
📄 **Read:** [references/api.md](references/maskedtextbox-api.md)
- All properties: `mask`, `value`, `placeholder`, `floatLabelType`, `promptChar`, `customCharacters`, `cssClass`, `enabled`, `readonly`, `showClearButton`, `enableRtl`, `enablePersistence`, `htmlAttributes`, `locale`, `width`, `prependTemplate`, `appendTemplate`
- Methods: `focusIn()`, `focusOut()`, `getMaskedValue()`, `destroy()`, `getPersistData()`
- Events: `change`, `focus`, `blur`, `created`, `destroyed`

### Quick Start

```tsx
import * as React from 'react';
import { MaskedTextBoxComponent } from '@syncfusion/ej2-react-inputs';
import '../node_modules/@syncfusion/ej2-base/styles/tailwind3.css';
import '../node_modules/@syncfusion/ej2-react-inputs/styles/tailwind3.css';

export default function App() {
  return (
    <MaskedTextBoxComponent
      mask="000-000-0000"
      placeholder="Enter phone number"
      floatLabelType="Auto"
    />
  );
}
```

### Common Patterns

#### Phone Number Input
```tsx
<MaskedTextBoxComponent mask="000-000-0000" placeholder="Phone" floatLabelType="Always" />
```

#### IP Address with Regex Mask
```tsx
<MaskedTextBoxComponent
  mask="[0-2][0-9][0-9].[0-2][0-9][0-9].[0-2][0-9][0-9].[0-2][0-9][0-9]"
  placeholder="IP Address (ex: 212.212.111.222)"
  floatLabelType="Always"
/>
```

#### Custom AM/PM Time Input
```tsx
const chars = { P: 'P,A,p,a', M: 'M,m' };
<MaskedTextBoxComponent
  mask="00:00 >PM"
  customCharacters={chars}
  placeholder="Time (ex: 10:00 PM)"
  floatLabelType="Always"
/>
```

#### Read Masked Value Programmatically
```tsx
const maskRef = React.useRef(null);
// Later:
const maskedVal = maskRef.current.getMaskedValue(); // e.g., "123-456-7890"
const rawVal = maskRef.current.value;               // e.g., "1234567890"
```

#### Controlled Input with Change Event
```tsx
const [phone, setPhone] = React.useState('');
<MaskedTextBoxComponent
  mask="000-000-0000"
  value={phone}
  change={(e) => setPhone(e.value)}
  placeholder="Phone"
  floatLabelType="Auto"
/>
```

## Rating

The Syncfusion React `RatingComponent` lets users select a rating value from a set of visual symbols (stars by default). It supports **precision modes**, **custom templates**, **tooltips**, **labels**, **reset**, **read-only/disabled** states, full **accessibility** compliance, and rich CSS customization.

**Package:** `@syncfusion/ej2-react-inputs`

---

### Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/rating-getting-started.md)
- Installing `@syncfusion/ej2-react-inputs`
- CSS theme imports for Tailwind3
- Minimal `RatingComponent` setup
- Setting the initial `value` property
- Running the Vite/React app

#### Selection and Reset
📄 **Read:** [references/selection.md](references/rating-selection.md)
- Setting a rating value with `value`
- Minimum rating value with `min`
- Single-selection mode with `enableSingleSelection`
- Show/hide reset button with `allowReset`
- Programmatic `reset()` method

#### Precision Modes
📄 **Read:** [references/precision-modes.md](references/rating-precision-modes.md)
- `PrecisionType.Full` — whole number increments
- `PrecisionType.Half` — 0.5 increments
- `PrecisionType.Quarter` — 0.25 increments
- `PrecisionType.Exact` — 0.1 increments
- Combining precision with initial value

#### Appearance and Customization
📄 **Read:** [references/appearance.md](references/rating-appearance.md)
- Controlling item count with `itemsCount`
- Disabling the component with `disabled`
- Hiding/showing the component with `visible`
- Read-only mode with `readOnly`
- CSS customization with `cssClass` (border color, fill color, item spacing, icon)
- Changing rating icon via CSS

#### Labels
📄 **Read:** [references/labels.md](references/rating-labels.md)
- Showing the current value label with `showLabel`
- `labelPosition` options: Top, Bottom, Left, Right
- Custom label content with `labelTemplate`

#### Tooltip
📄 **Read:** [references/tooltip.md](references/rating-tooltip.md)
- Enabling tooltips with `showTooltip`
- Custom tooltip content with `tooltipTemplate`
- Tooltip appearance via `cssClass`

#### Templates
📄 **Read:** [references/templates.md](references/rating-templates.md)
- `emptyTemplate` for unrated items
- `fullTemplate` for rated items
- Emoji rating symbols
- SVG icon rating symbols
- PNG image rating symbols
- Precision support in templates via `--rating-value`

#### Events
📄 **Read:** [references/events.md](references/rating-events.md)
- `beforeItemRender` — customize items before render
- `created` — after component initialization
- `onItemHover` — track hovered items
- `valueChanged` — react to user rating changes

#### Accessibility
📄 **Read:** [references/accessibility.md](references/rating-accessibility.md)
- WCAG 2.2 / Section 508 / ADA compliance
- WAI-ARIA attributes (`role=slider`, `aria-valuemin/max/now`)
- Keyboard navigation shortcuts
- RTL support with `enableRtl`
- Screen reader support

#### API Reference
📄 **Read:** [references/api.md](references/rating-api.md)
- All properties, methods, and events with types and defaults
- `RatingItemEventArgs`, `RatingHoverEventArgs`, `RatingChangedEventArgs`
- `LabelPosition` and `PrecisionType` enums

---

### Quick Start

```bash
npm install @syncfusion/ej2-react-inputs --save
```

```css
/* src/App.css */
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-inputs/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css";
```

```tsx
import { RatingComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <RatingComponent id="rating" value={3} />
  );
}
export default App;
```

---

### Common Patterns

#### Rating with value change handler
```tsx
import { RatingComponent, RatingChangedEventArgs } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  const [rating, setRating] = React.useState(3);

  const handleValueChanged = (args: RatingChangedEventArgs) => {
    setRating(args.value);
  };

  return (
    <RatingComponent
      id="rating"
      value={rating}
      valueChanged={handleValueChanged}
    />
  );
}
export default App;
```

#### Half-precision rating with label
```tsx
import { RatingComponent, PrecisionType } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <RatingComponent
      id="rating"
      value={3.5}
      precision={PrecisionType.Half}
      showLabel={true}
    />
  );
}
export default App;
```

#### Read-only rating (display only)
```tsx
import { RatingComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <RatingComponent id="rating" value={4} readOnly={true} showTooltip={false} />
  );
}
export default App;
```

#### Rating with reset button
```tsx
import { RatingComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <RatingComponent id="rating" value={3} allowReset={true} />
  );
}
export default App;
```

---

### Key Props at a Glance

| Prop | Type | Default | Purpose |
|------|------|---------|---------|
| `value` | `number` | `0.0` | Current rating value |
| `itemsCount` | `number` | `5` | Number of rating items |
| `min` | `number` | `0.0` | Minimum selectable value |
| `precision` | `PrecisionType \| string` | `Full` | Rating granularity |
| `allowReset` | `boolean` | `false` | Show reset button |
| `readOnly` | `boolean` | `false` | Prevent user interaction |
| `disabled` | `boolean` | `false` | Disable the component |
| `visible` | `boolean` | `true` | Show/hide the component |
| `showLabel` | `boolean` | `false` | Show current value label |
| `labelPosition` | `LabelPosition \| string` | `Right` | Label placement |
| `showTooltip` | `boolean` | `true` | Show hover tooltips |
| `enableSingleSelection` | `boolean` | `false` | Only one item selected |
| `enableAnimation` | `boolean` | `true` | Hover animation |
| `enableRtl` | `boolean` | `false` | Right-to-left mode |
| `cssClass` | `string` | `''` | Custom CSS class |

---
