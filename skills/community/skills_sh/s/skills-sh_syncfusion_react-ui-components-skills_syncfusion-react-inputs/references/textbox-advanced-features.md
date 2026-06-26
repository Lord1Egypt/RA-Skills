# Advanced Features

## Table of Contents

- [Adornments](#adornments)
- [Prepend and Append Templates](#prepend-and-append-templates)
- [React Hooks Integration](#react-hooks-integration)
- [Event Handling](#event-handling)
- [Form Integration](#form-integration)

## Adornments

Adornments are visual or interactive elements added before (prepend) or after (append) the TextBox input. Use templates to add custom icons, buttons, text labels, or interactive controls.

### Prepend Template

Add content before the input using `prependTemplate`. The template function must return `JSX.Element`:

```tsx
import * as React from 'react';
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function PrependExample() {
  function prependIcon(): JSX.Element {
    return (
      <>
        <span className="e-icons e-user"></span>
        <span className="e-input-separator"></span>
      </>
    );
  }

  return (
    <TextBoxComponent
      placeholder="Enter username"
      floatLabelType="Auto"
      prependTemplate={prependIcon}
    />
  );
}
```

**Result:**
```
┌──────────────────────────┐
│ 👤 | Enter username      │
└──────────────────────────┘
```

### Append Template

Add content after the input using `appendTemplate`. The template function must return `JSX.Element`:

```tsx
import * as React from 'react';
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function AppendExample() {
  function appendButton(): JSX.Element {
    return (
      <>
        <span className="e-input-separator"></span>
        <span className="e-icons e-input-popup-date"></span>
      </>
    );
  }

  return (
    <TextBoxComponent
      placeholder="Select date"
      floatLabelType="Auto"
      appendTemplate={appendButton}
    />
  );
}
```

**Result:**
```
┌──────────────────────────┐
│ Select date            📅 |
└──────────────────────────┘
```

## Prepend and Append Templates

### Interactive Adornment: Password Visibility Toggle

```tsx
import * as React from 'react';
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useRef, useState } from 'react';

export default function PasswordToggle() {
  const textboxRef = useRef<TextBoxComponent>(null);
  const [isVisible, setIsVisible] = useState(false);

  const toggleVisibility = () => {
    if (textboxRef.current) {
      const newVisibility = !isVisible;
      textboxRef.current.type = newVisibility ? 'text' : 'password';
      setIsVisible(newVisibility);
    }
  };

  function appendToggle(): JSX.Element {
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
      appendTemplate={appendToggle}
    />
  );
}
```

### Interactive Adornment: Clear Button

```tsx
import * as React from 'react';
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useRef, useState } from 'react';

export default function ClearButton() {
  const textboxRef = useRef<TextBoxComponent>(null);
  const [value, setValue] = useState('');

  const handleClear = () => {
    if (textboxRef.current) {
      textboxRef.current.value = '';
      setValue('');
    }
  };

  function appendClear(): JSX.Element {
    return (
      <>
        <span className="e-input-separator"></span>
        <span
          className="e-icons e-trash"
          onClick={handleClear}
          style={{ cursor: 'pointer' }}
        ></span>
      </>
    );
  }

  return (
    <TextBoxComponent
      ref={textboxRef}
      placeholder="Text to clear"
      floatLabelType="Auto"
      value={value}
      change={(e) => setValue(e.value)}
      appendTemplate={value ? appendClear : undefined}
    />
  );
}
```

### Complex Adornment: Email with Domain

```tsx
import * as React from 'react';
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

export default function EmailWithDomain() {
  const [domain, setDomain] = useState('gmail.com');

  function prependEmail(): JSX.Element {
    return (
      <>
        <span className="e-icons e-input-popup-date"></span>
        <span className="e-input-separator"></span>
      </>
    );
  }

  function appendDomain(): JSX.Element {
    return (
      <>
        <span className="e-input-separator"></span>
        <span style={{ padding: '0 8px', color: '#666' }}>@{domain}</span>
      </>
    );
  }

  return (
    <div>
      <div style={{ marginBottom: '15px' }}>
        <label>Select Domain:</label>
        <select 
          value={domain} 
          onChange={(e) => setDomain(e.target.value)}
          style={{ padding: '8px', marginLeft: '10px' }}
        >
          <option>gmail.com</option>
          <option>outlook.com</option>
          <option>yahoo.com</option>
          <option>company.com</option>
        </select>
      </div>

      <TextBoxComponent
        placeholder="username"
        floatLabelType="Auto"
        prependTemplate={prependEmail}
        appendTemplate={appendDomain}
      />
    </div>
  );
}
```

### Multi-Element Adornment: Complex Form Input

```tsx
import * as React from 'react';
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

export default function CurrencyInput() {
  const [value, setValue] = useState('');
  const [currency, setCurrency] = useState('USD');

  function prependCurrency(): JSX.Element {
    return (
      <>
        <span style={{ padding: '0 8px', color: '#666', fontWeight: 'bold' }}>
          {currency === 'USD' ? '$' : currency === 'EUR' ? '€' : '£'}
        </span>
        <span className="e-input-separator"></span>
      </>
    );
  }

  function appendCurrency(): JSX.Element {
    return (
      <>
        <span className="e-input-separator"></span>
        <span style={{ padding: '0 8px', color: '#999', fontSize: '12px' }}>
          {currency}
        </span>
      </>
    );
  }

  return (
    <div>
      <div style={{ marginBottom: '15px' }}>
        <label>Currency:</label>
        <select 
          value={currency}
          onChange={(e) => setCurrency(e.target.value)}
          style={{ padding: '8px', marginLeft: '10px' }}
        >
          <option>USD</option>
          <option>EUR</option>
          <option>GBP</option>
        </select>
      </div>

      <TextBoxComponent
        placeholder="0.00"
        floatLabelType="Auto"
        type="number"
        value={value}
        change={(e) => setValue(e.value)}
        prependTemplate={prependCurrency}
        appendTemplate={appendCurrency}
      />

      {value && (
        <p style={{ marginTop: '10px', color: '#666' }}>
          Total: {currency === 'USD' ? '$' : currency === 'EUR' ? '€' : '£'}{value}
        </p>
      )}
    </div>
  );
}
```

## React Hooks Integration

### useState Hook

Manage TextBox value with `useState`:

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

export default function UseStateExample() {
  const [value, setValue] = useState('');

  return (
    <div style={{ maxWidth: '400px', margin: '20px auto' }}>
      <TextBoxComponent
        placeholder="Type something"
        floatLabelType="Auto"
        value={value}
        change={(e) => setValue(e.value)}
      />
      <p>Current value: {value || '(empty)'}</p>
    </div>
  );
}
```

### useRef Hook

Access TextBox methods and DOM properties directly:

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useRef } from 'react';

export default function UseRefExample() {
  const textboxRef = useRef<TextBoxComponent>(null);

  const focusTextbox = () => {
    textboxRef.current?.focusIn();
  };

  const clearValue = () => {
    if (textboxRef.current) {
      textboxRef.current.value = '';
    }
  };

  const getLength = () => {
    const length = textboxRef.current?.value?.length || 0;
    alert(`Text length: ${length}`);
  };

  return (
    <div style={{ maxWidth: '400px', margin: '20px auto' }}>
      <TextBoxComponent
        ref={textboxRef}
        placeholder="Type text"
        floatLabelType="Auto"
      />

      <div style={{ marginTop: '15px', display: 'flex', gap: '10px' }}>
        <button onClick={focusTextbox}>Focus</button>
        <button onClick={clearValue}>Clear</button>
        <button onClick={getLength}>Get Length</button>
      </div>
    </div>
  );
}
```

### useEffect Hook

Initialize or perform side effects:

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useRef, useEffect } from 'react';

export default function UseEffectExample() {
  const textboxRef = useRef<TextBoxComponent>(null);

  useEffect(() => {
    // Focus TextBox on component mount
    textboxRef.current?.focusIn();

    // Set icon after component mounts
    if (textboxRef.current) {
      textboxRef.current.addIcon('append', 'e-icons e-input-popup-date');
    }
  }, []); // Empty dependency array: runs once on mount

  return (
    <TextBoxComponent
      ref={textboxRef}
      placeholder="Auto-focused on load"
      floatLabelType="Auto"
    />
  );
}
```

### useReducer Hook

Manage complex form state:

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useReducer } from 'react';

interface FormState {
  name: string;
  email: string;
  message: string;
}

type FormAction = {
  type: 'SET_FIELD';
  field: keyof FormState;
  value: string;
} | {
  type: 'RESET';
};

function formReducer(state: FormState, action: FormAction): FormState {
  switch (action.type) {
    case 'SET_FIELD':
      return { ...state, [action.field]: action.value };
    case 'RESET':
      return { name: '', email: '', message: '' };
    default:
      return state;
  }
}

export default function UseReducerExample() {
  const initialState: FormState = { name: '', email: '', message: '' };
  const [state, dispatch] = useReducer(formReducer, initialState);

  const handleChange = (field: keyof FormState, value: string) => {
    dispatch({ type: 'SET_FIELD', field, value });
  };

  const handleReset = () => {
    dispatch({ type: 'RESET' });
  };

  return (
    <div style={{ maxWidth: '500px', margin: '20px auto' }}>
      <h2>Contact Form</h2>

      <div style={{ marginBottom: '20px' }}>
        <TextBoxComponent
          placeholder="Name"
          floatLabelType="Auto"
          value={state.name}
          change={(e) => handleChange('name', e.value)}
        />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <TextBoxComponent
          placeholder="Email"
          floatLabelType="Auto"
          type="email"
          value={state.email}
          change={(e) => handleChange('email', e.value)}
        />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <TextBoxComponent
          placeholder="Message"
          floatLabelType="Auto"
          multiline={true}
          value={state.message}
          change={(e) => handleChange('message', e.value)}
        />
      </div>

      <button onClick={handleReset}>Reset Form</button>

      <pre style={{ marginTop: '20px', backgroundColor: '#f5f5f5', padding: '10px' }}>
        {JSON.stringify(state, null, 2)}
      </pre>
    </div>
  );
}
```

## Event Handling

### Change Event

Triggered when the TextBox value changes:

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function ChangeEventExample() {
  const handleChange = (e: any) => {
    console.log('New value:', e.value);
    console.log('Previous value:', e.previousValue);
  };

  return (
    <TextBoxComponent
      placeholder="Type to trigger change event"
      floatLabelType="Auto"
      change={handleChange}
    />
  );
}
```

### Created Event

Triggered after the component initializes:

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useRef } from 'react';

export default function CreatedEventExample() {
  const textboxRef = useRef<TextBoxComponent>(null);

  const handleCreated = () => {
    console.log('TextBox created successfully');
    
    if (textboxRef.current) {
      // Add icon after creation
      textboxRef.current.addIcon('append', 'e-icons e-search');
      
      // Set initial focus
      textboxRef.current.focusIn();
    }
  };

  return (
    <TextBoxComponent
      ref={textboxRef}
      placeholder="TextBox with initialization"
      floatLabelType="Auto"
      created={handleCreated}
    />
  );
}
```

### Input Event

Triggered on every keystroke (real-time):

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

export default function InputEventExample() {
  const [charCount, setCharCount] = useState(0);

  const handleInput = (e: any) => {
    setCharCount(e.value.length);
  };

  return (
    <div>
      <TextBoxComponent
        placeholder="Type to see character count"
        floatLabelType="Auto"
        input={handleInput}
      />
      <p>Characters: {charCount}</p>
    </div>
  );
}
```

## Form Integration

### Complete Form with Validation

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { FormValidator } from '@syncfusion/ej2-inputs';
import { useEffect, useRef, useState } from 'react';

export default function CompleteForm() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    message: ''
  });

  const formRef = useRef<HTMLFormElement>(null);
  const nameRef = useRef<TextBoxComponent>(null);

  useEffect(() => {
    // Initialize form validator
    if (formRef.current) {
      const validator = new FormValidator('#contact-form', {
        rules: {
          name: { required: [true, 'Name is required'] },
          email: { 
            required: [true, 'Email is required'],
            email: [true, 'Enter valid email']
          },
          phone: { required: [true, 'Phone is required'] },
          message: { required: [true, 'Message is required'] }
        }
      });
    }

    // Auto-focus name field
    nameRef.current?.focusIn();
  }, []);

  const handleChange = (field: string, value: string) => {
    setFormData({ ...formData, [field]: value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Form submitted:', formData);
    alert('Form submitted successfully!');
  };

  return (
    <form 
      ref={formRef}
      id="contact-form"
      onSubmit={handleSubmit}
      style={{ maxWidth: '500px', margin: '30px auto' }}
    >
      <h2>Contact Us</h2>

      <div style={{ marginBottom: '20px' }}>
        <TextBoxComponent
          ref={nameRef}
          name="name"
          placeholder="Full Name"
          floatLabelType="Auto"
          value={formData.name}
          change={(e) => handleChange('name', e.value)}
          data-msg-containerid="error-name"
        />
        <div id="error-name"></div>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <TextBoxComponent
          name="email"
          type="email"
          placeholder="Email Address"
          floatLabelType="Auto"
          value={formData.email}
          change={(e) => handleChange('email', e.value)}
          data-msg-containerid="error-email"
        />
        <div id="error-email"></div>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <TextBoxComponent
          name="phone"
          type="tel"
          placeholder="Phone Number"
          floatLabelType="Auto"
          value={formData.phone}
          change={(e) => handleChange('phone', e.value)}
          data-msg-containerid="error-phone"
        />
        <div id="error-phone"></div>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <TextBoxComponent
          name="message"
          placeholder="Your Message"
          floatLabelType="Auto"
          multiline={true}
          value={formData.message}
          change={(e) => handleChange('message', e.value)}
          data-msg-containerid="error-message"
        />
        <div id="error-message"></div>
      </div>

      <button 
        type="submit"
        style={{
          width: '100%',
          padding: '12px',
          backgroundColor: '#2196F3',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
          fontSize: '16px'
        }}
      >
        Send Message
      </button>
    </form>
  );
}
```

## See Also

- [Features and Groups](./features-and-groups.md) - Floating labels and icons
- [Validation and States](./validation-and-states.md) - Input validation
- [Multiline TextBox](./multiline-textbox.md) - Textarea mode
- [Getting Started](./getting-started.md) - Basic setup
