# Floating Label in React TextArea Component

## Table of Contents
- [Overview](#overview)
- [Float Label Types](#float-label-types)
- [Auto Floating Label](#auto-floating-label)
- [Always Floating Label](#always-floating-label)
- [Never Floating Label](#never-floating-label)
- [Localization](#localization)
- [Styling Floating Labels](#styling-floating-labels)

## Overview

The floating label functionality enhances user experience by displaying placeholder text that automatically floats above the TextArea when the user interacts with it. This provides a clean, modern interface that maintains context while the user types.

The `floatLabelType` property controls this behavior with three options: `Auto`, `Always`, and `Never`.

## Float Label Types

### Auto Floating Label

The placeholder text floats above the TextArea when it receives focus or when the user begins typing. The label returns to its initial placeholder position when focus is lost and the TextArea is empty.

**Best for:** General form fields where you want minimal visual clutter until interaction begins.

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <div className='wrap'>
      <TextAreaComponent 
        id='default' 
        placeholder='Enter your comments'
        floatLabelType='Auto'
      />
    </div>
  );
}

export default App;
```

**Behavior:**
- Initial state: Placeholder visible inside the TextArea
- On focus: Placeholder floats above the field
- After typing: Placeholder stays floating
- On blur with empty field: Placeholder returns to original position
- On blur with content: Placeholder remains floating

### Always Floating Label

The placeholder text always remains floating above the TextArea, regardless of focus or content state.

**Best for:** Forms where you want persistent labels for accessibility and clarity.

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <div className='wrap'>
      <TextAreaComponent 
        id='default' 
        placeholder='Enter your comments'
        floatLabelType='Always'
      />
    </div>
  );
}

export default App;
```

**Behavior:**
- The label is always visible above the TextArea
- Never returns to placeholder position
- Provides consistent visual layout

### Never Floating Label

The placeholder text never floats. It remains in its default position inside the TextArea and disappears when the user starts typing.

**Best for:** Compact interfaces where visual space is limited or when using alternative labeling methods.

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <div className='wrap'>
      <TextAreaComponent 
        id='default' 
        placeholder='Enter your comments'
        floatLabelType='Never'
      />
    </div>
  );
}

export default App;
```

**Behavior:**
- Placeholder remains inside the TextArea
- Never floats above the field
- Disappears when user types

## Combining with Other Features

### Floating Label with Max Length

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='feedback'
      placeholder='Your feedback'
      floatLabelType='Auto'
      maxLength={500}
      showClearButton={true}
    />
  );
}

export default App;
```

### Floating Label with Validation States

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const [isValid, setIsValid] = useState(true);

  const handleChange = (args) => {
    setIsValid((args.value || '').length > 0);
  };

  return (
    <TextAreaComponent 
      id='message'
      placeholder='Enter message'
      floatLabelType='Auto'
      cssClass={isValid ? 'e-success' : 'e-error'}
      change={handleChange}
    />
  );
}

export default App;
```

### Floating Label with Custom Sizing

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='description'
      placeholder='Product description'
      floatLabelType='Always'
      rows={6}
      cols={50}
      cssClass='e-outline'
    />
  );
}

export default App;
```

## Localization

### Placeholder with Localization

Use the `locale` property to localize placeholder text to different cultures:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='comments'
      placeholder='Veuillez entrer vos commentaires'
      locale='fr-BE'
      floatLabelType='Auto'
    />
  );
}

export default App;
```

### Load Translation for German Culture

Use the `L10n` class to load translation objects for specific cultures:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { L10n } from '@syncfusion/ej2-base';
import * as React from 'react';
import './App.css';

// Load German locale strings
L10n.load({
  'de-DE': {
    'textarea': { 'placeholder': 'Geben Sie Ihre Kommentare ein' }
  }
});

function App() {
  return (
    <TextAreaComponent 
      id='comments'
      locale='de-DE'
      floatLabelType='Auto'
    />
  );
}

export default App;
```

### Load French Locale

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { L10n } from '@syncfusion/ej2-base';
import * as React from 'react';
import './App.css';

L10n.load({
  'fr-FR': {
    'textarea': { 'placeholder': 'Entrez vos commentaires' }
  }
});

function App() {
  return (
    <TextAreaComponent 
      id='feedback'
      locale='fr-FR'
      floatLabelType='Auto'
    />
  );
}

export default App;
```

### Multiple Locales

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { L10n } from '@syncfusion/ej2-base';
import { useState } from 'react';
import * as React from 'react';
import './App.css';

L10n.load({
  'de-DE': {
    'textarea': { 'placeholder': 'Geben Sie Ihre Kommentare ein' }
  },
  'fr-FR': {
    'textarea': { 'placeholder': 'Entrez vos commentaires' }
  },
  'es-ES': {
    'textarea': { 'placeholder': 'Ingrese sus comentarios' }
  }
});

function App() {
  const [locale, setLocale] = useState('en-US');

  return (
    <div>
      <div>
        <button onClick={() => setLocale('en-US')}>English</button>
        <button onClick={() => setLocale('de-DE')}>German</button>
        <button onClick={() => setLocale('fr-FR')}>French</button>
        <button onClick={() => setLocale('es-ES')}>Spanish</button>
      </div>
      <TextAreaComponent 
        id='message'
        locale={locale}
        floatLabelType='Auto'
      />
    </div>
  );
}

export default App;
```

## Styling Floating Labels

### Change Floating Label Color

You can customize the floating label color for different validation states:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <div>
      <TextAreaComponent 
        id='success'
        placeholder='Success state'
        floatLabelType='Auto'
        cssClass='e-success'
      />
      <TextAreaComponent 
        id='warning'
        placeholder='Warning state'
        floatLabelType='Auto'
        cssClass='e-warning'
      />
    </div>
  );
}

export default App;
```

Add this CSS to your stylesheet:

```css
/* For Success state */
.e-float-input.e-success label.e-float-text,
.e-float-input.e-success input:focus ~ label.e-float-text,
.e-float-input.e-success textarea:focus ~ label.e-float-text {
  color: #22b24b;
}

/* For Warning state */
.e-float-input.e-warning label.e-float-text,
.e-float-input.e-warning input:focus ~ label.e-float-text,
.e-float-input.e-warning textarea:focus ~ label.e-float-text {
  color: #ffca1c;
}
```

## Best Practices

- **Auto** for standard forms - provides modern UX with minimal clutter
- **Always** for accessibility-critical applications - ensures labels are always visible
- **Never** when using separate label elements - avoids duplicate labeling
- Always provide meaningful placeholder text
- Use localization for multi-language support
- Combine with `cssClass` for proper styling
- Test with keyboard navigation for accessibility

## Common Issues

**Label not floating:**
- Ensure `floatLabelType` is set correctly (not default 'Never')
- Check that placeholder text is provided
- Verify CSS is properly imported

**Label stuck in floating position:**
- This is expected behavior - ensure appropriate `floatLabelType`
- For 'Auto', label returns only when field is empty and unfocused

**Localization not working:**
- Verify `L10n.load()` is called before component renders
- Check locale code matches exactly (case-sensitive)
- Ensure 'textarea' key is present in locale object
