# Methods in React TextArea Component

This section outlines the methods available for programmatic interaction with the TextArea component.

## FocusIn Method

The `focusIn()` method sets focus to the textarea element, enabling keyboard interaction. Useful for directing user attention or automated workflows.

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useRef } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const textareaRef = useRef<TextAreaComponent>(null);

  const handleFocusClick = () => {
    if (textareaRef.current) {
      textareaRef.current.focusIn();
    }
  };

  return (
    <div>
      <TextAreaComponent 
        ref={textareaRef}
        id='textarea'
        placeholder='Click button to focus'
      />
      <button onClick={handleFocusClick}>Focus TextArea</button>
    </div>
  );
}

export default App;
```

### Use Cases for FocusIn

```typescript
const handleFocusClick = () => {
  // Direct user attention to textarea
  textareaRef.current?.focusIn();
  
  // Programmatically set focus after validation
  if (validationPassed) {
    textareaRef.current?.focusIn();
  }
  
  // Move focus in wizard workflow
  textareaRef.current?.focusIn();
};
```

## FocusOut Method

The `focusOut()` method removes focus from the textarea element, ending keyboard interaction.

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useRef } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const textareaRef = useRef<TextAreaComponent>(null);

  const handleBlurClick = () => {
    if (textareaRef.current) {
      textareaRef.current.focusOut();
    }
  };

  return (
    <div>
      <TextAreaComponent 
        ref={textareaRef}
        id='textarea'
        placeholder='Click button to remove focus'
      />
      <button onClick={handleBlurClick}>Blur TextArea</button>
    </div>
  );
}

export default App;
```

### Use Cases for FocusOut

```typescript
const handleBlurClick = () => {
  // Move focus to next field
  textareaRef.current?.focusOut();
  nextFieldRef.current?.focusIn();
  
  // Close modal/dialog
  textareaRef.current?.focusOut();
  closeModal();
};
```

## GetPersistData Method

The `getPersistData()` method retrieves properties needed for persistence state. It returns an object containing configuration options and state information for maintaining data across sessions.

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useRef } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const textareaRef = useRef<TextAreaComponent>(null);

  const handleGetPersistData = () => {
    if (textareaRef.current) {
      const persistData = textareaRef.current.getPersistData();
      console.log('Persist Data:', persistData);
      // Save to localStorage or session storage
    }
  };

  return (
    <div>
      <TextAreaComponent 
        ref={textareaRef}
        id='textarea'
        value='Sample content'
        enablePersistence={true}
      />
      <button onClick={handleGetPersistData}>Get Persist Data</button>
    </div>
  );
}

export default App;
```

### Save State to LocalStorage

```typescript
const saveState = () => {
  if (textareaRef.current) {
    const persistData = textareaRef.current.getPersistData();
    localStorage.setItem('textareaState', JSON.stringify(persistData));
  }
};

const restoreState = () => {
  const savedState = localStorage.getItem('textareaState');
  if (savedState && textareaRef.current) {
    textareaRef.current.setPersistData(JSON.parse(savedState));
  }
};
```

## AddAttributes Method

The `addAttributes()` method adds multiple HTML attributes to the TextArea element dynamically.

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useRef } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const textareaRef = useRef<TextAreaComponent>(null);

  const handleAddAttributes = () => {
    if (textareaRef.current) {
      textareaRef.current.addAttributes({
        'data-testid': 'textarea-field',
        'aria-label': 'User feedback',
        'title': 'Enter your feedback here'
      });
    }
  };

  return (
    <div>
      <TextAreaComponent 
        ref={textareaRef}
        id='textarea'
        placeholder='Enter content'
      />
      <button onClick={handleAddAttributes}>Add Attributes</button>
    </div>
  );
}

export default App;
```

### Common Attribute Additions

```typescript
// Add accessibility attributes
textareaRef.current?.addAttributes({
  'aria-required': 'true',
  'aria-describedby': 'help-text-id',
  'aria-invalid': 'false'
});

// Add data attributes
textareaRef.current?.addAttributes({
  'data-field-name': 'comments',
  'data-required': 'true',
  'data-max-length': '500'
});

// Add validation attributes
textareaRef.current?.addAttributes({
  'data-validation': 'required|minLength:10',
  'data-error-message': 'Invalid input'
});
```

## RemoveAttributes Method

The `removeAttributes()` method removes multiple HTML attributes from the TextArea element.

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useRef } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const textareaRef = useRef<TextAreaComponent>(null);

  const handleAddAttributes = () => {
    if (textareaRef.current) {
      textareaRef.current.addAttributes({
        'title': 'User Feedback',
        'data-info': 'This is feedback form'
      });
    }
  };

  const handleRemoveAttributes = () => {
    if (textareaRef.current) {
      textareaRef.current.removeAttributes(['title', 'data-info']);
    }
  };

  return (
    <div>
      <TextAreaComponent 
        ref={textareaRef}
        id='textarea'
        placeholder='Enter content'
      />
      <button onClick={handleAddAttributes}>Add Attributes</button>
      <button onClick={handleRemoveAttributes}>Remove Attributes</button>
    </div>
  );
}

export default App;
```

### Attribute Cleanup

```typescript
const cleanupAttributes = () => {
  textareaRef.current?.removeAttributes([
    'data-testid',
    'data-validation',
    'aria-invalid',
    'title'
  ]);
};
```

## Destroy Method

The `destroy()` method removes the component from the DOM and detaches all event handlers. It also maintains the original textarea element.

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useRef } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const textareaRef = useRef<TextAreaComponent>(null);

  const handleDestroy = () => {
    if (textareaRef.current) {
      textareaRef.current.destroy();
      console.log('TextArea component destroyed');
    }
  };

  return (
    <div>
      <TextAreaComponent 
        ref={textareaRef}
        id='textarea'
        placeholder='This will be destroyed'
      />
      <button onClick={handleDestroy}>Destroy Component</button>
    </div>
  );
}

export default App;
```

### Cleanup in Unmount

```typescript
import { useEffect } from 'react';

useEffect(() => {
  return () => {
    // Cleanup when component unmounts
    textareaRef.current?.destroy();
  };
}, []);
```

## Practical Examples

### Multi-Step Form with Focus Management

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useRef, useState } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const textareaRef = useRef<TextAreaComponent>(null);
  const [step, setStep] = useState(1);

  const handleNext = () => {
    if (step === 1) {
      // Validate and move focus
      textareaRef.current?.focusOut();
      setStep(2);
    }
  };

  const handlePrevious = () => {
    if (step === 2) {
      setStep(1);
      textareaRef.current?.focusIn();
    }
  };

  return (
    <div>
      {step === 1 && (
        <div>
          <TextAreaComponent 
            ref={textareaRef}
            id='description'
            placeholder='Enter description'
          />
          <button onClick={handleNext}>Next</button>
        </div>
      )}
      
      {step === 2 && (
        <div>
          <p>Review your input...</p>
          <button onClick={handlePrevious}>Back</button>
        </div>
      )}
    </div>
  );
}

export default App;
```

### Accessibility Enhancement

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useRef, useEffect } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const textareaRef = useRef<TextAreaComponent>(null);

  useEffect(() => {
    // Add accessibility attributes on mount
    if (textareaRef.current) {
      textareaRef.current.addAttributes({
        'aria-label': 'Feedback form textarea',
        'aria-describedby': 'feedback-help',
        'aria-required': 'true',
        'role': 'textbox'
      });
    }
  }, []);

  return (
    <div>
      <TextAreaComponent 
        ref={textareaRef}
        id='feedback'
        placeholder='Enter feedback'
      />
      <p id='feedback-help'>Please provide constructive feedback</p>
    </div>
  );
}

export default App;
```

### State Persistence

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useRef, useEffect } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const textareaRef = useRef<TextAreaComponent>(null);

  useEffect(() => {
    // Enable persistence
    if (textareaRef.current) {
      textareaRef.current.enablePersistence = true;
    }

    // Optional: Add custom persistence
    window.addEventListener('beforeunload', () => {
      if (textareaRef.current) {
        const persistData = textareaRef.current.getPersistData();
        sessionStorage.setItem('textareaBackup', persistData);
      }
    });

    return () => {
      textareaRef.current?.destroy();
    };
  }, []);

  return (
    <TextAreaComponent 
      ref={textareaRef}
      id='draft'
      placeholder='Your work will be saved'
    />
  );
}

export default App;
```

## Best Practices

- Use `focusIn()` to guide user attention in complex forms
- Call `focusOut()` before programmatic field changes
- Use `getPersistData()` for cross-session state management
- Add accessibility attributes with `addAttributes()`
- Remove temporary attributes with `removeAttributes()`
- Always call `destroy()` in unmount handlers to prevent memory leaks
- Test all methods in different browser environments
