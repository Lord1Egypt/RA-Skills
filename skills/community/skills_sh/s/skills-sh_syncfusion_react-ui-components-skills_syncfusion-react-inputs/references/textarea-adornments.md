# Adornments in React TextArea Component

## Table of Contents
- [Overview](#overview)
- [Adding Adornments](#adding-adornments)
- [Adornment Flow](#adornment-flow)
- [Adornment Orientation](#adornment-orientation)
- [Common Use Cases](#common-use-cases)
- [Advanced Examples](#advanced-examples)

## Overview

Adornments enable custom elements (icons, text labels, buttons, or complex HTML) to be added before or after the TextArea. Using `prependTemplate` and `appendTemplate` properties, combined with `adornmentFlow` and `adornmentOrientation`, you can create flexible, visually rich layouts.

**Common Use Cases:**
- Visual context indicators (edit icons, status icons)
- Formatting tools (bold, italic, underline buttons)
- Action buttons (send, save, clear)
- Character count displays
- Validation status icons

## Adding Adornments

### Prepend Template (Before TextArea)

Add custom HTML or JSX content before the TextArea:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  const prependIcon = () => (
    <span className='prepend-icon'>📝</span>
  );

  return (
    <TextAreaComponent 
      id='textarea'
      placeholder='Enter your message'
      prependTemplate={prependIcon}
    />
  );
}

export default App;
```

### Append Template (After TextArea)

Add custom content after the TextArea:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  const appendButton = () => (
    <button className='send-btn'>Send</button>
  );

  return (
    <TextAreaComponent 
      id='message'
      placeholder='Type your message'
      appendTemplate={appendButton}
    />
  );
}

export default App;
```

### Both Prepend and Append

Combine prepend and append templates:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  const prependContent = () => (
    <span className='icon'>✏️</span>
  );

  const appendContent = () => (
    <div>
      <button className='clear-btn'>Clear</button>
      <button className='submit-btn'>Submit</button>
    </div>
  );

  return (
    <TextAreaComponent 
      id='form-textarea'
      placeholder='Enter feedback'
      prependTemplate={prependContent}
      appendTemplate={appendContent}
      floatLabelType='Auto'
    />
  );
}

export default App;
```

## Adornment Flow

The `adornmentFlow` property defines where adornments appear around the TextArea.

### Horizontal Flow

Prepend appears on the left, append appears on the right.

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  const prependContent = () => <span>Icon</span>;
  const appendContent = () => <button>Action</button>;

  return (
    <TextAreaComponent 
      id='textarea'
      prependTemplate={prependContent}
      appendTemplate={appendContent}
      adornmentFlow='Horizontal'
      placeholder='Message'
    />
  );
}

export default App;
```

**Layout:**
```
┌─────────────────────────────────────────┐
│ Icon │     TextArea Content      │ Action│
└─────────────────────────────────────────┘
```

### Vertical Flow

Prepend appears above, append appears below.

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  const prependContent = () => <span>📋</span>;
  const appendContent = () => <button>Send</button>;

  return (
    <TextAreaComponent 
      id='textarea'
      prependTemplate={prependContent}
      appendTemplate={appendContent}
      adornmentFlow='Vertical'
      placeholder='Message'
    />
  );
}

export default App;
```

**Layout:**
```
┌──────────────────────────────┐
│          📋                  │
├──────────────────────────────┤
│     TextArea Content         │
├──────────────────────────────┤
│         Send Button          │
└──────────────────────────────┘
```

## Adornment Orientation

The `adornmentOrientation` property controls how items are arranged within each adornment section.

### Horizontal Orientation

Items are displayed in a row:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  const appendContent = () => (
    <div className='button-group'>
      <button>Bold</button>
      <button>Italic</button>
      <button>Underline</button>
    </div>
  );

  return (
    <TextAreaComponent 
      id='editor'
      appendTemplate={appendContent}
      adornmentOrientation='Horizontal'
      placeholder='Edit text here'
    />
  );
}

export default App;
```

**Layout:**
```
TextArea Content | [Bold] [Italic] [Underline]
```

### Vertical Orientation

Items are displayed in a column:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  const appendContent = () => (
    <div className='toolbar'>
      <button>✓ Save</button>
      <button>⟲ Redo</button>
      <button>↶ Undo</button>
    </div>
  );

  return (
    <TextAreaComponent 
      id='document'
      appendTemplate={appendContent}
      adornmentOrientation='Vertical'
      placeholder='Document content'
    />
  );
}

export default App;
```

**Layout:**
```
┌─────────────────────────────┬─────────┐
│  TextArea Content           │ ✓ Save  │
│                             ├─────────┤
│                             │ ⟲ Redo  │
│                             ├─────────┤
│                             │ ↶ Undo  │
└─────────────────────────────┴─────────┘
```

## Common Use Cases

### Character Count Display

Show remaining characters as append content:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const [charCount, setCharCount] = useState(0);
  const maxChars = 500;

  const appendContent = () => (
    <div className='char-count'>
      {charCount} / {maxChars}
    </div>
  );

  return (
    <TextAreaComponent 
      id='feedback'
      maxLength={maxChars}
      appendTemplate={appendContent}
      input={(args) => setCharCount((args.value || '').length)}
      placeholder='Your feedback'
    />
  );
}

export default App;
```

### Validation Status Icon

Show success/error status:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const [isValid, setIsValid] = useState(false);

  const appendContent = () => (
    <span className={isValid ? 'icon-success' : 'icon-error'}>
      {isValid ? '✓' : '✗'}
    </span>
  );

  const handleChange = (args) => {
    setIsValid((args.value || '').length > 0);
  };

  return (
    <TextAreaComponent 
      id='message'
      appendTemplate={appendContent}
      change={handleChange}
      placeholder='Enter message'
    />
  );
}

export default App;
```

### Formatting Toolbar

Add text formatting options:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useRef } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const textareaRef = useRef(null);

  const appendContent = () => (
    <div className='toolbar'>
      <button onClick={() => insertFormat('**', '**')}>Bold</button>
      <button onClick={() => insertFormat('*', '*')}>Italic</button>
      <button onClick={() => insertFormat('~~', '~~')}>Strike</button>
    </div>
  );

  const insertFormat = (before, after) => {
    if (textareaRef.current) {
      const textarea = textareaRef.current;
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const text = textarea.value;
      const selectedText = text.substring(start, end);
      const newText = 
        text.substring(0, start) + 
        before + selectedText + after + 
        text.substring(end);
      textarea.value = newText;
    }
  };

  return (
    <TextAreaComponent 
      ref={textareaRef}
      id='editor'
      appendTemplate={appendContent}
      placeholder='Write here'
    />
  );
}

export default App;
```

### Action Buttons

Add multiple action buttons:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const [text, setText] = useState('');

  const appendContent = () => (
    <div className='actions'>
      <button onClick={() => setText('')}>Clear</button>
      <button onClick={() => handleSubmit()}>Send</button>
    </div>
  );

  const handleSubmit = () => {
    console.log('Submitted:', text);
    setText('');
  };

  return (
    <TextAreaComponent 
      id='message'
      value={text}
      input={(args) => setText(args.value || '')}
      appendTemplate={appendContent}
      placeholder='Your message'
    />
  );
}

export default App;
```

## Advanced Examples

### Multi-Row Layout with Both Adornments

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  const prependContent = () => (
    <div className='left-icons'>
      <span title='Edit'>✏️</span>
      <span title='Attachments'>📎</span>
    </div>
  );

  const appendContent = () => (
    <div className='right-actions'>
      <button className='action-btn'>Preview</button>
      <button className='action-btn'>Submit</button>
      <button className='action-btn'>Save</button>
    </div>
  );

  return (
    <TextAreaComponent 
      id='rich-text'
      prependTemplate={prependContent}
      appendTemplate={appendContent}
      adornmentFlow='Vertical'
      adornmentOrientation='Horizontal'
      placeholder='Create your content'
      rows={8}
    />
  );
}

export default App;
```

### Contextual Adornments

Dynamically show/hide adornments based on state:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const [isFocused, setIsFocused] = useState(false);
  const [text, setText] = useState('');

  const appendContent = () => (
    isFocused && text.length > 0 && (
      <button onClick={() => setText('')}>Clear</button>
    )
  );

  return (
    <TextAreaComponent 
      id='conditional'
      value={text}
      input={(args) => setText(args.value || '')}
      focus={() => setIsFocused(true)}
      blur={() => setIsFocused(false)}
      appendTemplate={appendContent}
      placeholder='Start typing...'
    />
  );
}

export default App;
```

## Best Practices

- Keep adornments lightweight - avoid complex components
- Use meaningful icons and labels for clarity
- Position actions logically (submit/send on right/bottom)
- Test readability with different TextArea sizes
- Ensure adornments don't interfere with keyboard navigation
- Use horizontal flow for space efficiency in narrow layouts
- Use vertical flow for better organization in complex forms
