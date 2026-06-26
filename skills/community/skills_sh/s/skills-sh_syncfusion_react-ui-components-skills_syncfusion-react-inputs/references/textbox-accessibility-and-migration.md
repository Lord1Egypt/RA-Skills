# Accessibility and Migration

## Table of Contents

- [Accessibility Overview](#accessibility-overview)
- [WCAG and Standards Compliance](#wcag-and-standards-compliance)
- [WAI-ARIA Implementation](#wai-aria-implementation)
- [Screen Reader Support](#screen-reader-support)
- [Keyboard Navigation](#keyboard-navigation)
- [Right-to-Left Support](#right-to-left-support)
- [Migration from CSS TextBox](#migration-from-css-textbox)

## Accessibility Overview

The Syncfusion React TextBox component is built with accessibility as a core feature, enabling all users—including those using assistive technologies—to interact effectively. The component complies with:

- **WCAG 2.2** - Web Content Accessibility Guidelines Level AA
- **Section 508** - U.S. Federal accessibility requirement
- **WAI-ARIA** - Web Accessibility Initiative Accessible Rich Internet Applications
- **Mobile devices** - Touch-friendly, accessible on all devices

### Accessibility Compliance Matrix

| Criterion | Support |
|-----------|---------|
| WCAG 2.2 | ✓ Full compliance |
| Section 508 | ✓ Full compliance |
| Screen Readers | ✓ Full support |
| RTL Support | ✓ Full support |
| Color Contrast | ✓ WCAG AA standard |
| Mobile Support | ✓ Touch-optimized |
| Keyboard Navigation | ✓ Full support |
| Accessibility Checker | ✓ Validated |
| Axe-core | ✓ Validated |

## WCAG and Standards Compliance

### Color Contrast

TextBox components meet WCAG AA standards for color contrast (4.5:1 minimum for normal text, 3:1 for large text).

**Ensure proper contrast in custom CSS:**

```css
/* Good: High contrast */
.e-input {
  background-color: #FFFFFF;
  color: #000000;  /* 21:1 contrast ratio */
}

/* Avoid: Low contrast */
.e-input {
  background-color: #F8F8F8;
  color: #E8E8E8;  /* Too low contrast */
}
```

### Text Sizing

Provide readable font sizes:

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function AccessibleTextBox() {
  return (
    <TextBoxComponent
      placeholder="Minimum 16px on mobile"
      floatLabelType="Auto"
      style={{ fontSize: '16px' }} // Prevents mobile zoom-on-focus
    />
  );
}
```

### Focus Indicators

Ensure visible focus indicators for keyboard users:

```css
.e-input:focus,
.e-float-input input:focus {
  outline: 3px solid #2196F3;
  outline-offset: 2px;
}
```

## WAI-ARIA Implementation

### ARIA Attributes

The TextBox automatically implements WAI-ARIA attributes:

| Attribute | Value | Purpose |
|-----------|-------|---------|
| `role` | `textbox` | Identifies element as textbox |
| `aria-placeholder` | text | Short hint when empty |
| `aria-labelledby` | id | Links to floating label |
| `aria-invalid` | true/false | Indicates validation state |
| `aria-describedby` | id | Links to error message |

### Manual ARIA Implementation

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useRef } from 'react';

export default function AccessibleTextBox() {
  const textboxRef = useRef<TextBoxComponent>(null);

  return (
    <>
      <label id="name-label" htmlFor="name-input">
        Full Name *
      </label>
      
      <TextBoxComponent
        id="name-input"
        ref={textboxRef}
        placeholder="Enter your full name"
        floatLabelType="Auto"
        htmlAttributes={{
          'aria-labelledby': 'name-label',
          'aria-required': 'true',
          'aria-describedby': 'name-error'
        }}
      />

      <div id="name-error" role="alert">
        {/* Error message appears here */}
      </div>
    </>
  );
}
```

### Error Messages with ARIA

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

export default function AccessibleValidation() {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');

  const handleChange = (e: any) => {
    const value = e.value;
    setEmail(value);

    // Validate and set error
    if (value && !value.includes('@')) {
      setError('Email must contain @ symbol');
    } else {
      setError('');
    }
  };

  return (
    <>
      <label htmlFor="email-input">Email Address *</label>
      
      <TextBoxComponent
        id="email-input"
        type="email"
        placeholder="your@email.com"
        floatLabelType="Auto"
        value={email}
        change={handleChange}
        cssClass={error ? 'e-error' : ''}
        htmlAttributes={{
          'aria-invalid': error ? 'true' : 'false',
          ...(error ? { 'aria-describedby': 'email-error' } : {})
        }}
      />

      {error && (
        <div id="email-error" role="alert" style={{ color: '#F44336', marginTop: '5px' }}>
          {error}
        </div>
      )}
    </>
  );
}
```

## Screen Reader Support

### Proper Labeling

Always provide explicit labels for TextBox inputs:

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function ScreenReaderFriendly() {
  return (
    <div>
      <label htmlFor="username">Username</label>
      <TextBoxComponent
        id="username"
        placeholder="Enter your username"
        floatLabelType="Auto"
      />
    </div>
  );
}
```

**Screen reader announces:** "Username, input field, placeholder: Enter your username"

### Form Legends

Group related inputs with `<fieldset>` and `<legend>`:

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function AccessibleForm() {
  return (
    <form>
      <fieldset>
        <legend>Personal Information</legend>

        <div>
          <label htmlFor="first-name">First Name *</label>
          <TextBoxComponent
            id="first-name"
            placeholder="First name"
            floatLabelType="Auto"
            htmlAttributes={{ 'aria-required': 'true' }}
          />
        </div>

        <div>
          <label htmlFor="last-name">Last Name *</label>
          <TextBoxComponent
            id="last-name"
            placeholder="Last name"
            floatLabelType="Auto"
            htmlAttributes={{ 'aria-required': 'true' }}
          />
        </div>
      </fieldset>

      <fieldset>
        <legend>Contact Information</legend>

        <div>
          <label htmlFor="email">Email *</label>
          <TextBoxComponent
            id="email"
            type="email"
            placeholder="your@email.com"
            floatLabelType="Auto"
            htmlAttributes={{ 'aria-required': 'true' }}
          />
        </div>
      </fieldset>
    </form>
  );
}
```

### Helper Text and Instructions

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function HelpfulTextBox() {
  return (
    <div>
      <label htmlFor="password">Password</label>
      
      <p id="password-hint" style={{ fontSize: '14px', color: '#666' }}>
        Must be at least 8 characters with letters and numbers
      </p>

      <TextBoxComponent
        id="password"
        type="password"
        placeholder="Enter your password"
        floatLabelType="Auto"
        htmlAttributes={{ 'aria-describedby': 'password-hint' }}
      />
    </div>
  );
}
```

## Keyboard Navigation

### Tab Order

TextBox is automatically part of the tab order:

```tsx
<form>
  <TextBoxComponent placeholder="First field" floatLabelType="Auto" />
  <TextBoxComponent placeholder="Second field" floatLabelType="Auto" />
  <TextBoxComponent placeholder="Third field" floatLabelType="Auto" />
  {/* Tab order: 1 → 2 → 3 */}
</form>
```

### Keyboard Events

Use the native `htmlAttributes` property to attach keyboard event handlers via standard HTML attributes, or wrap the TextBoxComponent in a container with `onKeyDown`:

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useRef } from 'react';

export default function KeyboardSupport() {
  const textboxRef = useRef<TextBoxComponent>(null);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
    if (e.key === 'Enter') {
      console.log('Enter pressed');
    }
    if (e.key === 'Escape') {
      console.log('Escape pressed');
      if (textboxRef.current) {
        textboxRef.current.value = '';
      }
    }
  };

  return (
    <div onKeyDown={handleKeyDown}>
      <TextBoxComponent
        placeholder="Press Enter or Escape"
        floatLabelType="Auto"
        ref={textboxRef}
      />
    </div>
  );
}
```

### Focus Management

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useRef, useEffect } from 'react';

export default function FocusManagement() {
  const firstInputRef = useRef<TextBoxComponent>(null);
  const secondInputRef = useRef<TextBoxComponent>(null);

  useEffect(() => {
    // Auto-focus first input on mount
    firstInputRef.current?.focusIn();
  }, []);

  return (
    <form>
      <div>
        <label htmlFor="input1">First Input</label>
        <TextBoxComponent
          id="input1"
          ref={firstInputRef}
          placeholder="Tab to next field"
          floatLabelType="Auto"
        />
      </div>

      <div>
        <label htmlFor="input2">Second Input</label>
        <TextBoxComponent
          id="input2"
          ref={secondInputRef}
          placeholder="Second field"
          floatLabelType="Auto"
        />
      </div>
    </form>
  );
}
```

## Right-to-Left Support

### Enable RTL

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function RTLTextBox() {
  return (
    <div dir="rtl">
      <label htmlFor="arabic-input">الاسم (Name)</label>
      <TextBoxComponent
        id="arabic-input"
        placeholder="أدخل اسمك"
        floatLabelType="Auto"
      />
    </div>
  );
}
```

### RTL with CSS

```css
[dir="rtl"] .e-input-group,
[dir="rtl"] .e-float-input {
  direction: rtl;
  text-align: right;
}

[dir="rtl"] .e-input {
  direction: rtl;
}
```

## Migration from CSS TextBox

### Before: CSS TextBox

Traditional approach using HTML and CSS:

```html
<!-- Normal TextBox -->
<div class="e-input-group">
  <input class="e-input" type="text" placeholder="Enter Value" />
</div>

<!-- Floating Label TextBox -->
<div class="e-float-input">
  <input type="text" required />
  <span class="e-float-line"></span>
  <label class="e-float-text">Enter Value</label>
</div>

<!-- TextBox with clear button (manual JavaScript required) -->
<div class="e-input-group">
  <input class="e-input" type="text" placeholder="Enter Value" required />
  <span class="e-clear-icon"></span>
</div>
```

**Disadvantages:**
- Manual DOM manipulation required
- No built-in event handling
- Duplicate HTML structure
- More CSS code needed
- Error handling requires JavaScript

### After: React TextBox Component

Modern approach using React component:

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

// Normal TextBox
<TextBoxComponent 
  placeholder="Enter Value"
  floatLabelType="Never"
/>

// Floating Label TextBox
<TextBoxComponent 
  placeholder="Enter Value"
  floatLabelType="Auto"
/>

// TextBox with clear button
<TextBoxComponent 
  placeholder="Enter Value"
  floatLabelType="Auto"
  showClearButton={true}
/>
```

**Advantages:**
- ✓ Built-in functionality
- ✓ Automatic event handling
- ✓ Cleaner syntax
- ✓ Less code duplication
- ✓ Better accessibility
- ✓ Easier state management

### Migration Comparison

#### Normal Input

**CSS Version:**
```html
<div class="e-input-group">
  <input class="e-input" type="text" placeholder="Enter Name" />
</div>
```

**React Version:**
```tsx
<TextBoxComponent 
  placeholder="Enter Name"
  floatLabelType="Never"
/>
```

**Benefit:** 1 line vs 3 lines (67% reduction)

#### Floating Label Input

**CSS Version:**
```html
<div class="e-float-input">
  <input type="text" required />
  <span class="e-float-line"></span>
  <label class="e-float-text">Enter Name</label>
</div>
```

**React Version:**
```tsx
<TextBoxComponent 
  placeholder="Enter Name"
  floatLabelType="Auto"
/>
```

**Benefit:** 1 line vs 5 lines (80% reduction)

#### Clear Button

**CSS Version:**
```html
<div class="e-float-input e-input-group">
  <input type="text" required value="Clear Input" />
  <span class="e-float-line"></span>
  <label class="e-float-text">Enter Value</label>
  <span class="e-clear-icon"></span>
</div>
<!-- JavaScript required for clear button functionality -->
<script>
  document.querySelector('.e-clear-icon').addEventListener('click', function() {
    document.querySelector('input').value = '';
  });
</script>
```

**React Version:**
```tsx
<TextBoxComponent 
  placeholder="Enter Value"
  floatLabelType="Auto"
  showClearButton={true}
/>
```

**Benefit:** 1 line vs 10+ lines with JavaScript

#### Validation States

**CSS Version:**
```html
<!-- Error state -->
<div class="e-float-input e-error">
  <input type="text" required />
  <span class="e-float-line"></span>
  <label class="e-float-text">Email</label>
</div>

<!-- Warning state -->
<div class="e-float-input e-warning">
  <input type="text" required />
  <span class="e-float-line"></span>
  <label class="e-float-text">Email</label>
</div>

<!-- Success state -->
<div class="e-float-input e-success">
  <input type="text" required />
  <span class="e-float-line"></span>
  <label class="e-float-text">Email</label>
</div>
```

**React Version:**
```tsx
<TextBoxComponent 
  placeholder="Email"
  floatLabelType="Auto"
  cssClass="e-error"
/>

<TextBoxComponent 
  placeholder="Email"
  floatLabelType="Auto"
  cssClass="e-warning"
/>

<TextBoxComponent 
  placeholder="Email"
  floatLabelType="Auto"
  cssClass="e-success"
/>
```

### Complete Migration Example

**Before (CSS TextBox):**

```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="ej2.css">
</head>
<body>
  <div class="e-float-input">
    <input id="name" type="text" required />
    <span class="e-float-line"></span>
    <label class="e-float-text">Name</label>
  </div>

  <div class="e-float-input">
    <input id="email" type="email" required />
    <span class="e-float-line"></span>
    <label class="e-float-text">Email</label>
  </div>

  <button onclick="submitForm()">Submit</button>

  <script>
    function submitForm() {
      const name = document.getElementById('name').value;
      const email = document.getElementById('email').value;
      console.log('Form:', { name, email });
    }
  </script>
</body>
</html>
```

**After (React TextBox):**

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

export default function App() {
  const [formData, setFormData] = useState({ name: '', email: '' });

  const handleSubmit = () => {
    console.log('Form:', formData);
  };

  return (
    <div>
      <TextBoxComponent
        placeholder="Name"
        floatLabelType="Auto"
        value={formData.name}
        change={(e) => setFormData({ ...formData, name: e.value })}
      />

      <TextBoxComponent
        placeholder="Email"
        floatLabelType="Auto"
        type="email"
        value={formData.email}
        change={(e) => setFormData({ ...formData, email: e.value })}
      />

      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
}
```

**Code Reduction:** ~50% less code

## See Also

- [Getting Started](./getting-started.md) - Setup and installation
- [Features and Groups](./features-and-groups.md) - Floating labels and icons
- [Validation and States](./validation-and-states.md) - Input validation
- [Advanced Features](./advanced-features.md) - React hooks integration
