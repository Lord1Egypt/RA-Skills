# Events in React TextArea Component

## Table of Contents
- [Created Event](#created-event)
- [Input Event](#input-event)
- [Change Event](#change-event)
- [Focus Event](#focus-event)
- [Blur Event](#blur-event)
- [Destroyed Event](#destroyed-event)
- [Event Patterns](#event-patterns)

## Created Event

The `created` event fires when the TextArea component is created and fully initialized. Use this to perform setup actions.

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  const handleCreated = () => {
    console.log('TextArea component initialized');
    // Perform any setup actions
  };

  return (
    <TextAreaComponent 
      id='default'
      placeholder='Enter comments'
      created={handleCreated}
    />
  );
}

export default App;
```

### Use Cases for Created Event

- Initialize related UI components
- Load initial data
- Set focus programmatically
- Trigger animations
- Apply dynamic configuration

```typescript
const handleCreated = () => {
  // Set initial focus
  document.getElementById('default')?.focus();
  
  // Log initialization
  console.log('Form ready for user input');
};
```

## Input Event

The `input` event fires every time the user types or modifies the TextArea value. Use this for real-time content tracking.

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import type { InputEventArgs } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const [charCount, setCharCount] = useState(0);

  const handleInput = (args: InputEventArgs) => {
    const length = (args.value || '').length;
    setCharCount(length);
  };

  return (
    <div>
      <TextAreaComponent 
        id='editor'
        input={handleInput}
        placeholder='Start typing'
      />
      <p>Characters: {charCount}</p>
    </div>
  );
}

export default App;
```

### InputEventArgs Properties

```typescript
interface InputEventArgs {
  value: string;           // Current textarea value
  keyCode: number;         // Keyboard key code
  isComposed: boolean;     // Composition event flag
}
```

### Real-Time Use Cases

```typescript
const handleInput = (args: InputEventArgs) => {
  // Character count
  const count = (args.value || '').length;
  
  // Word count
  const words = (args.value || '').trim().split(/\s+/).length;
  
  // Line count
  const lines = (args.value || '').split('\n').length;
  
  // Search highlighting
  const searchMatches = (args.value || '').match(/pattern/g)?.length || 0;
};
```

## Change Event

The `change` event fires when the content changes and focus is lost. Use this for form submission or validation after user editing.

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import type { ChangedEventArgs } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  const handleChange = (args: ChangedEventArgs) => {
    console.log('Value changed to:', args.value);
    // Validate or save
  };

  return (
    <TextAreaComponent 
      id='feedback'
      placeholder='Your feedback'
      change={handleChange}
    />
  );
}

export default App;
```

### ChangedEventArgs Properties

```typescript
interface ChangedEventArgs {
  value: string;          // New textarea value
  isInteracted: boolean;  // User-initiated change
  previousValue: string;  // Previous value
}
```

### Change Event Use Cases

```typescript
const handleChange = (args: ChangedEventArgs) => {
  // Auto-save to database
  if (args.value && args.isInteracted) {
    saveToDatabase(args.value);
  }
  
  // Validate input
  validateInput(args.value);
  
  // Update preview
  updatePreview(args.value);
};
```

## Focus Event

The `focus` event fires when the TextArea gains focus. Use this to highlight the field or show help text.

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import type { FocusInEventArgs } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const [isFocused, setIsFocused] = useState(false);

  const handleFocus = (args: FocusInEventArgs) => {
    console.log('TextArea focused');
    setIsFocused(true);
  };

  return (
    <div>
      <TextAreaComponent 
        id='message'
        placeholder='Click to focus'
        focus={handleFocus}
      />
      {isFocused && <p className='help-text'>Help: Enter your message here</p>}
    </div>
  );
}

export default App;
```

### FocusInEventArgs Properties

```typescript
interface FocusInEventArgs {
  value: string;  // Current textarea value
}
```

### Focus Event Use Cases

```typescript
const handleFocus = (args: FocusInEventArgs) => {
  // Show helper text
  showHelpText();
  
  // Highlight related fields
  highlightRelatedFields();
  
  // Log user engagement
  logAnalytics('textarea_focused');
  
  // Clear previous errors
  clearErrorMessages();
};
```

## Blur Event

The `blur` event fires when focus is lost. Use this for validation or cleanup.

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import type { FocusOutEventArgs } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const [error, setError] = useState('');

  const handleBlur = (args: FocusOutEventArgs) => {
    console.log('TextArea lost focus');
    
    if (!args.value || args.value.trim() === '') {
      setError('Field is required');
    } else {
      setError('');
    }
  };

  return (
    <div>
      <TextAreaComponent 
        id='feedback'
        placeholder='Your feedback'
        blur={handleBlur}
      />
      {error && <p className='error'>{error}</p>}
    </div>
  );
}

export default App;
```

### FocusOutEventArgs Properties

```typescript
interface FocusOutEventArgs {
  value: string;  // Current textarea value
}
```

### Blur Event Use Cases

```typescript
const handleBlur = (args: FocusOutEventArgs) => {
  // Validate on blur
  validateAndShowError(args.value);
  
  // Trim whitespace
  trimValue(args.value);
  
  // Format content
  formatContent(args.value);
  
  // Hide helper text
  hideHelpText();
};
```

## Destroyed Event

The `destroyed` event fires when the TextArea component is destroyed or removed from the DOM. Use this for cleanup.

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  const handleDestroyed = () => {
    console.log('TextArea component destroyed');
    // Cleanup: unsubscribe events, clear timers, etc.
  };

  return (
    <TextAreaComponent 
      id='temporary'
      placeholder='Temporary textarea'
      destroyed={handleDestroyed}
    />
  );
}

export default App;
```

### Destroyed Event Use Cases

```typescript
const handleDestroyed = () => {
  // Clear watchers
  unsubscribeDataWatcher();
  
  // Clear timers
  clearInterval(autoSaveTimer);
  
  // Remove event listeners
  removeCustomEventListeners();
  
  // Save final state
  saveFinalState();
};
```

## Event Patterns

### Real-Time Character Counter

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import type { InputEventArgs } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const [stats, setStats] = useState({
    chars: 0,
    words: 0,
    lines: 1
  });

  const handleInput = (args: InputEventArgs) => {
    const value = args.value || '';
    setStats({
      chars: value.length,
      words: value.trim() ? value.trim().split(/\s+/).length : 0,
      lines: value.split('\n').length
    });
  };

  return (
    <div>
      <TextAreaComponent 
        id='counter'
        input={handleInput}
        placeholder='Type here'
        rows={5}
      />
      <div className='stats'>
        <span>Chars: {stats.chars}</span>
        <span>Words: {stats.words}</span>
        <span>Lines: {stats.lines}</span>
      </div>
    </div>
  );
}

export default App;
```

### Form Validation Flow

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import type { FocusOutEventArgs, InputEventArgs } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const [feedback, setFeedback] = useState({
    value: '',
    isTouched: false,
    error: ''
  });

  const handleInput = (args: InputEventArgs) => {
    setFeedback(prev => ({
      ...prev,
      value: args.value || '',
      isTouched: true
    }));
  };

  const handleBlur = (args: FocusOutEventArgs) => {
    let error = '';
    if (!args.value || args.value.trim() === '') {
      error = 'Feedback is required';
    } else if (args.value.length < 10) {
      error = 'Minimum 10 characters';
    }
    
    setFeedback(prev => ({
      ...prev,
      error
    }));
  };

  const handleChange = (args) => {
    if (feedback.error) {
      // Auto-validate on blur + input to clear errors
      setFeedback(prev => ({
        ...prev,
        error: ''
      }));
    }
  };

  return (
    <div>
      <TextAreaComponent 
        id='form-textarea'
        value={feedback.value}
        input={handleInput}
        blur={handleBlur}
        change={handleChange}
        placeholder='Your feedback'
        cssClass={feedback.error ? 'e-error' : ''}
      />
      {feedback.isTouched && feedback.error && (
        <p className='error'>{feedback.error}</p>
      )}
    </div>
  );
}

export default App;
```

### Multi-Field Coordination

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import type { InputEventArgs } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    title: '',
    description: ''
  });
  const [isValid, setIsValid] = useState(false);

  const handleTitleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      title: e.target.value
    }));
    checkFormValidity();
  };

  const handleDescriptionInput = (args: InputEventArgs) => {
    setFormData(prev => ({
      ...prev,
      description: args.value || ''
    }));
    checkFormValidity();
  };

  const checkFormValidity = () => {
    const valid = formData.title.length > 0 && formData.description.length > 10;
    setIsValid(valid);
  };

  return (
    <form>
      <input 
        type='text'
        value={formData.title}
        onChange={handleTitleChange}
        placeholder='Title'
      />
      <TextAreaComponent 
        id='description'
        value={formData.description}
        input={handleDescriptionInput}
        placeholder='Description'
      />
      <button disabled={!isValid}>Submit</button>
    </form>
  );
}

export default App;
```

## Event Listener Best Practices

- **Input event**: Real-time operations (character count, preview, search)
- **Change event**: Form submission, database saves, validation
- **Focus event**: UI feedback, help text, analytics
- **Blur event**: Validation, cleanup, state updates
- **Created event**: Initialization, setup
- **Destroyed event**: Cleanup, unsubscribe

## Performance Tips

- Use `change` instead of `input` for expensive operations (API calls)
- Debounce `input` event handlers for auto-save
- Unsubscribe from events in `destroyed` to prevent memory leaks
- Use `input` for UI feedback, `change` for persistence
