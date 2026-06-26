# Complete API Reference for React TextArea Component

## Table of Contents
- [Properties](#properties)
- [Methods](#methods)
- [Events](#events)
- [Type Definitions](#type-definitions)
- [Usage Examples](#usage-examples)

## Properties

### value

Sets or gets the content of the TextArea.

```typescript
<TextAreaComponent value='Initial content' />
```

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `value` | string | null | TextArea content |

### placeholder

Sets the hint text displayed inside the TextArea when it's empty.

```typescript
<TextAreaComponent placeholder='Enter your feedback' />
```

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `placeholder` | string | null | Placeholder text |

### rows

Sets the visible height of the TextArea, measured in lines.

```typescript
<TextAreaComponent rows={5} />
```

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `rows` | number | undefined | Number of visible lines |

### cols

Sets the visible width of the TextArea, measured in average character widths.

```typescript
<TextAreaComponent cols={50} />
```

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `cols` | number | undefined | Number of character widths |

### maxLength

Specifies the maximum number of characters allowed in the TextArea.

```typescript
<TextAreaComponent maxLength={500} />
```

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `maxLength` | number | undefined | Maximum character limit |

**Behavior:**
- Input is prevented when limit is reached
- Paste content is truncated to fit
- Existing content can be edited freely

### enabled

Specifies whether the TextArea is enabled for user interaction.

```typescript
<TextAreaComponent enabled={false} />
```

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `enabled` | boolean | true | Enable/disable interaction |

**When false:**
- Appears grayed out
- No user input allowed
- Cannot receive focus

### readonly

Specifies whether the TextArea is in read-only mode. Users can select and copy but not edit.

```typescript
<TextAreaComponent readonly={true} />
```

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `readonly` | boolean | false | Read-only mode |

**When true:**
- Content cannot be modified
- Content can be selected and copied
- Can receive focus

### floatLabelType

Specifies the floating label behavior for the placeholder text.

```typescript
<TextAreaComponent floatLabelType='Auto' />
```

| Value | Behavior |
|-------|----------|
| `Never` | Placeholder never floats (default) |
| `Auto` | Placeholder floats on focus or input |
| `Always` | Placeholder always floats |

### resizeMode

Specifies how the TextArea can be resized by the user.

```typescript
<TextAreaComponent resizeMode='Both' />
```

| Value | Behavior |
|-------|----------|
| `Both` | User can resize both dimensions (default) |
| `Vertical` | User can only resize height |
| `Horizontal` | User can only resize width |
| `None` | Resizing disabled |

### width

Sets the width of the TextArea component.

```typescript
<TextAreaComponent width='400px' />
<TextAreaComponent width='100%' />
```

| Type | Example |
|------|---------|
| `number` | `400` (pixels) |
| `string` | `'400px'`, `'100%'` |

### cssClass

Adds custom CSS classes to the TextArea for custom styling.

```typescript
<TextAreaComponent cssClass='e-outline e-small custom-style' />
```

**Built-in Classes:**
- `e-small` - Smaller size
- `e-bigger` - Larger size
- `e-outline` - Outline mode
- `e-filled` - Filled mode
- `e-success` - Success validation state
- `e-warning` - Warning validation state
- `e-error` - Error validation state

### showClearButton

Shows a button to clear the TextArea content.

```typescript
<TextAreaComponent showClearButton={true} />
```

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `showClearButton` | boolean | false | Display clear button |

### prependTemplate

HTML template or JSX element to prepend before the TextArea.

```typescript
<TextAreaComponent 
  prependTemplate={() => <span className='icon'>📝</span>}
/>
```

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `prependTemplate` | string \| function \| JSX.Element | null | Prepend content |

### appendTemplate

HTML template or JSX element to append after the TextArea.

```typescript
<TextAreaComponent 
  appendTemplate={() => <button>Send</button>}
/>
```

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `appendTemplate` | string \| function \| JSX.Element | null | Append content |

### adornmentFlow

Controls where adornments (prepend/append) appear around the TextArea.

```typescript
<TextAreaComponent adornmentFlow='Horizontal' />
```

| Value | Behavior |
|-------|----------|
| `Horizontal` | Prepend on left, append on right |
| `Vertical` | Prepend above, append below |

### adornmentOrientation

Controls how items are arranged within each adornment section.

```typescript
<TextAreaComponent adornmentOrientation='Horizontal' />
```

| Value | Behavior |
|-------|----------|
| `Horizontal` | Items in a row |
| `Vertical` | Items in a column |

### enablePersistence

Enables or disables persisting TextArea state across sessions.

```typescript
<TextAreaComponent enablePersistence={true} />
```

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `enablePersistence` | boolean | false | Persist state |

**When true:**
- Component state saved to browser storage
- State restored on page reload

### enableRtl

Enables or disables right-to-left rendering direction.

```typescript
<TextAreaComponent enableRtl={true} />
```

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `enableRtl` | boolean | false | Right-to-left direction |

### locale

Sets the culture/language for the TextArea component.

```typescript
<TextAreaComponent locale='de-DE' />
```

| Common Locales |
|---|
| `en-US` (English, USA) |
| `de-DE` (German) |
| `fr-FR` (French) |
| `es-ES` (Spanish) |
| `ja-JP` (Japanese) |

### htmlAttributes

Adds additional HTML attributes to the TextArea element.

```typescript
<TextAreaComponent 
  htmlAttributes={{
    'data-testid': 'feedback-field',
    'aria-label': 'User feedback'
  }}
/>
```

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `htmlAttributes` | { [key: string]: string } | {} | Custom HTML attributes |

---

## Methods

### focusIn()

Sets focus to the TextArea, enabling keyboard interaction.

```typescript
textareaRef.current?.focusIn();
```

**Returns:** void

**Example:**
```typescript
const handleFocus = () => {
  textareaRef.current?.focusIn();
};
```

### focusOut()

Removes focus from the TextArea.

```typescript
textareaRef.current?.focusOut();
```

**Returns:** void

**Example:**
```typescript
const handleBlur = () => {
  textareaRef.current?.focusOut();
};
```

### getPersistData()

Retrieves properties needed for persistence state.

```typescript
const persistData = textareaRef.current?.getPersistData();
```

**Returns:** string

**Example:**
```typescript
const saveState = () => {
  const data = textareaRef.current?.getPersistData();
  localStorage.setItem('textareaState', data || '');
};
```

### addAttributes()

Adds multiple HTML attributes to the TextArea element dynamically.

```typescript
textareaRef.current?.addAttributes({
  'data-testid': 'textarea',
  'aria-label': 'Feedback'
});
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `attributes` | { [key: string]: string } | Attributes to add |

**Returns:** void

**Example:**
```typescript
const addAccessibility = () => {
  textareaRef.current?.addAttributes({
    'aria-required': 'true',
    'aria-describedby': 'help-text',
    'role': 'textbox'
  });
};
```

### removeAttributes()

Removes multiple HTML attributes from the TextArea element.

```typescript
textareaRef.current?.removeAttributes(['data-testid', 'aria-label']);
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `attributes` | string[] | Attribute names to remove |

**Returns:** void

**Example:**
```typescript
const removeAttrs = () => {
  textareaRef.current?.removeAttributes([
    'data-validation',
    'title'
  ]);
};
```

### destroy()

Removes the component from the DOM and detaches all event handlers. Maintains the original textarea element.

```typescript
textareaRef.current?.destroy();
```

**Returns:** void

**Example:**
```typescript
useEffect(() => {
  return () => {
    textareaRef.current?.destroy();
  };
}, []);
```

---

## Events

### created

Fired when the TextArea component is created and initialized.

```typescript
<TextAreaComponent created={() => console.log('Created')} />
```

**Type:** EmitType<Object>

**Use Cases:**
- Initialize related UI elements
- Set initial focus
- Load data

### input

Fired every time the user types or modifies the TextArea value.

```typescript
<TextAreaComponent 
  input={(args: InputEventArgs) => console.log(args.value)}
/>
```

**Type:** EmitType<InputEventArgs>

**Args:**
```typescript
interface InputEventArgs {
  value: string;       // Current textarea value
  keyCode: number;     // Keyboard key code
  isComposed: boolean; // Composition event flag
}
```

**Use Cases:**
- Real-time character counting
- Auto-save
- Input validation

### change

Fired when the content changes and focus is lost.

```typescript
<TextAreaComponent 
  change={(args: ChangedEventArgs) => console.log(args.value)}
/>
```

**Type:** EmitType<ChangedEventArgs>

**Args:**
```typescript
interface ChangedEventArgs {
  value: string;          // New textarea value
  isInteracted: boolean;  // User-initiated change
  previousValue: string;  // Previous value
}
```

**Use Cases:**
- Form submission
- Database save
- Validation after editing

### focus

Fired when the TextArea gains focus.

```typescript
<TextAreaComponent 
  focus={(args: FocusInEventArgs) => console.log('Focused')}
/>
```

**Type:** EmitType<FocusInEventArgs>

**Args:**
```typescript
interface FocusInEventArgs {
  value: string;  // Current textarea value
}
```

**Use Cases:**
- Show help text
- Highlight related fields
- Analytics logging

### blur

Fired when focus is lost.

```typescript
<TextAreaComponent 
  blur={(args: FocusOutEventArgs) => console.log('Blurred')}
/>
```

**Type:** EmitType<FocusOutEventArgs>

**Args:**
```typescript
interface FocusOutEventArgs {
  value: string;  // Current textarea value
}
```

**Use Cases:**
- Validation
- Trim whitespace
- Format content

### destroyed

Fired when the TextArea component is destroyed.

```typescript
<TextAreaComponent 
  destroyed={() => console.log('Destroyed')}
/>
```

**Type:** EmitType<Object>

**Use Cases:**
- Cleanup event listeners
- Clear timers
- Save final state

---

## Type Definitions

### AdornmentsDirection

```typescript
type AdornmentsDirection = 'Horizontal' | 'Vertical';
```

Used for `adornmentFlow` and `adornmentOrientation` properties.

### FloatLabelType

```typescript
type FloatLabelType = 'Never' | 'Auto' | 'Always';
```

Used for `floatLabelType` property.

### Resize

```typescript
type Resize = 'Both' | 'Vertical' | 'Horizontal' | 'None';
```

Used for `resizeMode` property.

### InputEventArgs

```typescript
interface InputEventArgs {
  value: string;
  keyCode: number;
  isComposed: boolean;
}
```

Event args for `input` event.

### ChangedEventArgs

```typescript
interface ChangedEventArgs {
  value: string;
  isInteracted: boolean;
  previousValue: string;
}
```

Event args for `change` event.

### FocusInEventArgs

```typescript
interface FocusInEventArgs {
  value: string;
}
```

Event args for `focus` event.

### FocusOutEventArgs

```typescript
interface FocusOutEventArgs {
  value: string;
}
```

Event args for `blur` event.

---

## Usage Examples

### Basic Setup

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <TextAreaComponent 
      id='textarea'
      placeholder='Enter text'
      rows={5}
      cols={40}
    />
  );
}

export default App;
```

### Full-Featured Form Field

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';

function App() {
  const [value, setValue] = useState('');

  return (
    <TextAreaComponent 
      id='feedback'
      placeholder='Your feedback'
      value={value}
      input={(args) => setValue(args.value || '')}
      floatLabelType='Auto'
      maxLength={500}
      rows={6}
      cols={50}
      enabled={true}
      showClearButton={true}
      cssClass='e-outline'
    />
  );
}

export default App;
```

### With All Event Handlers

```typescript
<TextAreaComponent
  id='complete'
  placeholder='Enter text'
  created={() => console.log('Component created')}
  input={(args) => console.log('Input:', args.value)}
  change={(args) => console.log('Changed:', args.value)}
  focus={(args) => console.log('Focused')}
  blur={(args) => console.log('Blurred')}
  destroyed={() => console.log('Component destroyed')}
/>
```

### With Adornments

```typescript
<TextAreaComponent
  id='adorned'
  placeholder='Message'
  prependTemplate={() => <span>📝</span>}
  appendTemplate={() => <button>Send</button>}
  adornmentFlow='Horizontal'
  adornmentOrientation='Horizontal'
/>
```

### With Accessibility

```typescript
<TextAreaComponent
  id='accessible'
  placeholder='Feedback'
  htmlAttributes={{
    'aria-label': 'User feedback form',
    'aria-describedby': 'help-text',
    'aria-required': 'true'
  }}
  floatLabelType='Always'
/>
```

### With Persistence

```typescript
<TextAreaComponent
  id='persistent'
  placeholder='Your draft'
  enablePersistence={true}
  value={savedValue}
/>
```

---

## Import Statement

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
```

## Package

- **Package:** @syncfusion/ej2-react-inputs
- **Version:** Latest (Check npm for current version)
- **License:** SEE LICENSE IN license
