# Styling and Appearance in React TextArea Component

## Table of Contents
- [Size Classes](#size-classes)
- [Filled and Outline Modes](#filled-and-outline-modes)
- [Custom CSS](#custom-css)
- [Disabled and Read-Only States](#disabled-and-read-only-states)
- [Validation States](#validation-states)
- [Clear Button](#clear-button)
- [Color Customization](#color-customization)
- [Advanced Styling](#advanced-styling)

## Size Classes

Apply size variations using CSS classes to adjust the TextArea appearance.

### Small TextArea

Add the `e-small` class for a compact textarea:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <div>
      <h4>Small TextArea</h4>
      <div className='e-input-group e-small'>
        <textarea 
          className='e-input' 
          placeholder='Small textarea'
        ></textarea>
      </div>
    </div>
  );
}

export default App;
```

With TextAreaComponent:

```typescript
<TextAreaComponent 
  id='small'
  placeholder='Small textarea'
  cssClass='e-small'
/>
```

### Bigger TextArea

Add the `e-bigger` class for an enlarged textarea:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='bigger'
      placeholder='Bigger textarea'
      cssClass='e-bigger'
    />
  );
}

export default App;
```

### Normal TextArea (Default)

No class needed - default size applies automatically.

## Filled and Outline Modes

Syncfusion TextArea supports two appearance modes: filled and outline. These are available with Material themes.

### Outline Mode

The outline style displays a border around the textarea:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='outlined'
      placeholder='Outlined'
      floatLabelType='Auto'
      cssClass='e-outline'
    />
  );
}

export default App;
```

### Filled Mode

The filled style displays a background color with the textarea:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='filled'
      placeholder='Filled'
      floatLabelType='Auto'
      cssClass='e-filled'
    />
  );
}

export default App;
```

### Combining Size and Mode

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <div>
      <TextAreaComponent 
        id='small-outline'
        placeholder='Small outline'
        cssClass='e-small e-outline'
        floatLabelType='Auto'
      />

      <TextAreaComponent 
        id='big-filled'
        placeholder='Bigger filled'
        cssClass='e-bigger e-filled'
        floatLabelType='Auto'
      />
    </div>
  );
}

export default App;
```

## Custom CSS

Apply custom styling using the `cssClass` property:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='custom'
      placeholder='Enter comments'
      floatLabelType='Auto'
      cssClass='custom-textarea'
    />
  );
}

export default App;
```

With CSS:

```css
.custom-textarea.e-field {
  background-color: #f5f5f5;
  border-color: #2196F3;
  border-radius: 8px;
}

.custom-textarea.e-field:focus {
  background-color: #ffffff;
  box-shadow: 0 0 8px rgba(33, 150, 243, 0.3);
}
```

## Disabled and Read-Only States

### Disabled State

Prevent user interaction using the `enabled` property:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='disabled'
      placeholder='This is disabled'
      enabled={false}
    />
  );
}

export default App;
```

The disabled textarea appears grayed out and cannot be interacted with.

### Read-Only State

Prevent editing but allow selection using the `readonly` property:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='readonly'
      value='This content cannot be edited'
      readonly={true}
    />
  );
}

export default App;
```

Users can select and copy read-only content but cannot edit it.

### Toggle States

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const [isEnabled, setIsEnabled] = useState(true);

  return (
    <div>
      <button onClick={() => setIsEnabled(!isEnabled)}>
        {isEnabled ? 'Disable' : 'Enable'}
      </button>

      <TextAreaComponent 
        id='togglable'
        placeholder='Toggle enabled state'
        enabled={isEnabled}
      />
    </div>
  );
}

export default App;
```

## Validation States

Apply validation styling using CSS classes:

### Success State

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='success'
      placeholder='Valid input'
      cssClass='e-success'
      floatLabelType='Auto'
    />
  );
}

export default App;
```

### Warning State

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='warning'
      placeholder='Warning state'
      cssClass='e-warning'
      floatLabelType='Auto'
    />
  );
}

export default App;
```

### Error State

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='error'
      placeholder='Error input'
      cssClass='e-error'
      floatLabelType='Auto'
    />
  );
}

export default App;
```

### Dynamic Validation Styling

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const [text, setText] = useState('');

  const getValidationClass = () => {
    if (text.length === 0) return '';
    if (text.length < 10) return 'e-warning';
    return 'e-success';
  };

  return (
    <TextAreaComponent 
      id='validated'
      value={text}
      input={(args) => setText(args.value || '')}
      placeholder='Type to validate'
      cssClass={getValidationClass()}
      floatLabelType='Auto'
    />
  );
}

export default App;
```

## Clear Button

Display a button to clear textarea content:

### Static Clear Button

Show clear button always:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='clearable'
      placeholder='Enter text'
      showClearButton={true}
      cssClass='e-static-clear'
    />
  );
}

export default App;
```

### Conditional Clear Button

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const [text, setText] = useState('');

  return (
    <TextAreaComponent 
      id='conditional-clear'
      value={text}
      input={(args) => setText(args.value || '')}
      placeholder='Enter text'
      showClearButton={text.length > 0}
    />
  );
}

export default App;
```

## Color Customization

### Background and Text Color

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='styled'
      placeholder='Custom colors'
      cssClass='custom-colors'
    />
  );
}

export default App;
```

CSS:

```css
.custom-colors.e-field {
  background-color: #fff8f0;
  color: #333333;
}

.custom-colors.e-field::placeholder {
  color: #999999;
}

.custom-colors.e-field:focus {
  background-color: #fffaf7;
  border-color: #ff6b35;
}
```

### Floating Label Color

Change floating label color for validation states:

```css
/* Success state floating label */
.e-float-input.e-success label.e-float-text,
.e-float-input.e-success textarea:focus ~ label.e-float-text {
  color: #22b24b;
}

/* Warning state floating label */
.e-float-input.e-warning label.e-float-text,
.e-float-input.e-warning textarea:focus ~ label.e-float-text {
  color: #ffca1c;
}

/* Error state floating label */
.e-float-input.e-error label.e-float-text,
.e-float-input.e-error textarea:focus ~ label.e-float-text {
  color: #d32f2f;
}
```

## Advanced Styling

### Rounded Corners

Add rounded corners by applying the `e-corner` class:

```typescript
import * as React from 'react';

function App() {
  return (
    <div className='e-input-group e-corner'>
      <textarea 
        className='e-input'
        placeholder='Rounded corners'
      ></textarea>
    </div>
  );
}

export default App;
```

### Custom Font and Spacing

```css
.custom-textarea.e-field {
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 14px;
  line-height: 1.6;
  padding: 12px 16px;
}
```

### Focus Effects

```css
.custom-textarea.e-field {
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.custom-textarea.e-field:focus {
  box-shadow: 0 4px 12px rgba(33, 150, 243, 0.2);
  transform: translateY(-2px);
}
```

### Mandatory Asterisk

Add asterisk to placeholder for required fields:

```css
.e-float-input.e-control-wrapper .e-float-text::after {
  content: '*';
  color: red;
  margin-left: 4px;
}
```

With TextArea:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='required'
      placeholder='Your comments'
      floatLabelType='Auto'
      cssClass='required-field'
    />
  );
}

export default App;
```

### Disabled Appearance

```css
.e-input:disabled,
.e-field:disabled {
  background-color: #f5f5f5;
  color: #9e9e9e;
  cursor: not-allowed;
  opacity: 0.6;
}
```

## Complete Themed Example

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [theme, setTheme] = useState('light');

  const getThemeClass = () => {
    return theme === 'dark' ? 'textarea-dark' : 'textarea-light';
  };

  return (
    <div className={getThemeClass()}>
      <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
        Toggle Theme
      </button>

      <TextAreaComponent 
        id='themed'
        value={text}
        input={(args) => setText(args.value || '')}
        placeholder='Enter text'
        cssClass={`${getThemeClass()} e-outline`}
        floatLabelType='Auto'
        showClearButton={text.length > 0}
      />
    </div>
  );
}

export default App;
```

CSS:

```css
/* Light theme */
.textarea-light.e-field {
  background-color: #ffffff;
  color: #333333;
  border-color: #cccccc;
}

/* Dark theme */
.textarea-dark.e-field {
  background-color: #2d2d2d;
  color: #e0e0e0;
  border-color: #555555;
}

.textarea-dark.e-field::placeholder {
  color: #888888;
}
```

## Best Practices

- Use outline mode for modern, clean designs
- Apply validation classes consistently across forms
- Ensure sufficient color contrast for accessibility
- Test styling on different themes (Material, Bootstrap, Tailwind)
- Use CSS transitions for smooth state changes
- Maintain consistent sizing across form fields
- Test disabled/readonly states for visual distinction
- Document custom CSS classes for team consistency
