# Value and Content Management in React TextArea

Efficiently manage TextArea content by setting initial values, updating content dynamically, and retrieving values for form submission or data processing.

## Setting Initial Values

### Direct Property Binding

Set the initial value using the `value` property when the component renders:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <TextAreaComponent 
      id='comments'
      value='Enter your feedback here'
    />
  );
}

export default App;
```

### Using State Variable

For dynamic initial values or updates, use React state:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';

function App() {
  const [initialComment, setInitialComment] = useState('Please enter your comments');

  return (
    <TextAreaComponent 
      id='comments'
      value={initialComment}
    />
  );
}

export default App;
```

### Loading Values from Data

Fetch and populate initial values from an API or database:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState, useEffect } from 'react';
import * as React from 'react';

function App() {
  const [feedbackValue, setFeedbackValue] = useState('');

  useEffect(() => {
    // Simulate API call
    const fetchFeedback = async () => {
      const response = await fetch('/api/feedback/123');
      const data = await response.json();
      setFeedbackValue(data.message);
    };
    
    fetchFeedback();
  }, []);

  return (
    <TextAreaComponent 
      id='feedback'
      value={feedbackValue}
    />
  );
}

export default App;
```

## Getting Current Value

### From State Variable

Access the current value through the state variable:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';

function App() {
  const [textValue, setTextValue] = useState('');

  const handleGetValue = () => {
    console.log('Current textarea value:', textValue);
    return textValue;
  };

  return (
    <div>
      <TextAreaComponent 
        id='content'
        value={textValue}
      />
      <button onClick={handleGetValue}>Get Value</button>
    </div>
  );
}

export default App;
```

### From Component Reference

Use a ref to directly access the component instance:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useRef } from 'react';
import * as React from 'react';

function App() {
  const textareaRef = useRef(null);

  const handleGetValue = () => {
    if (textareaRef.current) {
      const value = textareaRef.current.value;
      console.log('TextArea value from ref:', value);
      return value;
    }
  };

  return (
    <div>
      <TextAreaComponent 
        ref={textareaRef}
        id='content'
      />
      <button onClick={handleGetValue}>Get Value</button>
    </div>
  );
}

export default App;
```

## Real-Time Change Detection

### Using Input Event

The `input` event fires every keystroke, providing real-time value updates:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import type { InputEventArgs } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';

function App() {
  const [text, setText] = useState('');
  const [charCount, setCharCount] = useState(0);

  const handleInput = (args: InputEventArgs) => {
    const value = args.value || '';
    setText(value);
    setCharCount(value.length);
  };

  return (
    <div>
      <TextAreaComponent 
        id='editor'
        input={handleInput}
      />
      <p>Characters typed: {charCount}</p>
      <p>Content: {text}</p>
    </div>
  );
}

export default App;
```

### Using Change Event

The `change` event fires when focus is lost, useful for form submissions:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import type { ChangedEventArgs } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';

function App() {
  const [savedValue, setSavedValue] = useState('');

  const handleChange = (args: ChangedEventArgs) => {
    setSavedValue(args.value || '');
    console.log('Value saved on blur:', args.value);
  };

  return (
    <div>
      <TextAreaComponent 
        id='notes'
        change={handleChange}
      />
      <p>Last saved: {savedValue}</p>
    </div>
  );
}

export default App;
```

## Updating Content Dynamically

### Update from External Events

Change textarea content in response to user actions:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';

function App() {
  const [text, setText] = useState('');

  const handleLoadTemplate = () => {
    setText('Dear User,\nThank you for your feedback.\nBest regards');
  };

  const handleClear = () => {
    setText('');
  };

  return (
    <div>
      <TextAreaComponent 
        id='message'
        value={text}
      />
      <button onClick={handleLoadTemplate}>Load Template</button>
      <button onClick={handleClear}>Clear</button>
    </div>
  );
}

export default App;
```

### Append Text

Add text to existing content:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';

function App() {
  const [text, setText] = useState('Initial text\n');

  const handleAppend = () => {
    setText(prev => prev + 'New line added\n');
  };

  return (
    <div>
      <TextAreaComponent 
        id='document'
        value={text}
      />
      <button onClick={handleAppend}>Add Line</button>
    </div>
  );
}

export default App;
```

### Replace All Text

Completely replace textarea content:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';

function App() {
  const [text, setText] = useState('');

  const handleReplace = () => {
    setText('This is completely new content');
  };

  return (
    <div>
      <TextAreaComponent 
        id='editor'
        value={text}
      />
      <button onClick={handleReplace}>Replace All</button>
    </div>
  );
}

export default App;
```

## Form Submission

### Get Value for Form Submit

Collect textarea value when form is submitted:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';

function App() {
  const [formData, setFormData] = useState({
    name: '',
    comments: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Form submitted with:', formData);
    // Send to API
  };

  return (
    <form onSubmit={handleSubmit}>
      <input 
        type='text'
        placeholder='Name'
        value={formData.name}
        onChange={(e) => setFormData({...formData, name: e.target.value})}
      />
      <TextAreaComponent 
        id='comments'
        value={formData.comments}
        input={(args) => setFormData({...formData, comments: args.value || ''})}
      />
      <button type='submit'>Submit</button>
    </form>
  );
}

export default App;
```

## Content Transformation

### Transform and Update

Apply transformations to content while editing:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';

function App() {
  const [text, setText] = useState('');

  const handleToUpperCase = () => {
    setText(text.toUpperCase());
  };

  const handleToLowerCase = () => {
    setText(text.toLowerCase());
  };

  const handleTrim = () => {
    setText(text.trim());
  };

  return (
    <div>
      <TextAreaComponent 
        id='text-editor'
        value={text}
        input={(args) => setText(args.value || '')}
      />
      <button onClick={handleToUpperCase}>UPPERCASE</button>
      <button onClick={handleToLowerCase}>lowercase</button>
      <button onClick={handleTrim}>Trim</button>
    </div>
  );
}

export default App;
```

## Empty State Handling

### Check if Empty

Validate before submission:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';

function App() {
  const [text, setText] = useState('');

  const handleValidate = () => {
    if (!text || text.trim() === '') {
      console.log('TextArea is empty');
      return false;
    }
    console.log('TextArea has content');
    return true;
  };

  return (
    <div>
      <TextAreaComponent 
        id='feedback'
        value={text}
        input={(args) => setText(args.value || '')}
      />
      <button onClick={handleValidate}>Validate</button>
    </div>
  );
}

export default App;
```

### Default Values

Provide fallback values:

```typescript
const getTextValue = (value: string | undefined | null): string => {
  return (value || 'No content provided').trim();
};
```

## Best Practices

- **Always manage state** for controlled components
- **Use `input` event** for real-time tracking
- **Use `change` event** for form submissions
- **Validate empty content** before processing
- **Transform text** safely with proper null checks
- **Keep refs minimal** - prefer state management
