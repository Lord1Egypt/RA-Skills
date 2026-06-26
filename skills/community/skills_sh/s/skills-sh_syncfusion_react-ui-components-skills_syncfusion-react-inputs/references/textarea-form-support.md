# Form Support in React TextArea Component

## Table of Contents
- [Overview](#overview)
- [HTML Form Integration](#html-form-integration)
- [FormValidator Integration](#formvalidator-integration)
- [Validation Rules](#validation-rules)
- [Form Submission](#form-submission)
- [Error Display](#error-display)

## Overview

The TextArea component seamlessly integrates with HTML forms and Syncfusion's FormValidator component. This enables efficient submission of multiline text data, comprehensive validation, and error messaging.

## HTML Form Integration

### Basic Form with TextArea

Integrate TextArea directly in an HTML form:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget as HTMLFormElement);
    console.log('Form data:', Object.fromEntries(formData));
  };

  return (
    <form onSubmit={handleSubmit}>
      <TextAreaComponent 
        id='comments'
        name='myTextarea'
        placeholder='Enter your comments'
        floatLabelType='Auto'
      />
      <button type='submit'>Submit</button>
    </form>
  );
}

export default App;
```

### Required Field Validation

Mark textarea as required:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <form>
      <TextAreaComponent 
        id='feedback'
        name='feedback'
        placeholder='Your feedback'
        floatLabelType='Auto'
        required={true}
      />
      <button type='submit'>Submit</button>
    </form>
  );
}

export default App;
```

### Form with Multiple Fields

Combine TextArea with other form inputs:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  const [formData, setFormData] = React.useState({
    name: '',
    email: '',
    comments: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Submitted:', formData);
    // Send to API
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <input 
          type='text'
          name='name'
          placeholder='Full Name'
          value={formData.name}
          onChange={(e) => setFormData({...formData, name: e.target.value})}
        />
      </div>
      <div>
        <input 
          type='email'
          name='email'
          placeholder='Email'
          value={formData.email}
          onChange={(e) => setFormData({...formData, email: e.target.value})}
        />
      </div>
      <div>
        <TextAreaComponent 
          id='comments'
          name='comments'
          placeholder='Comments'
          value={formData.comments}
          input={(args) => setFormData({...formData, comments: args.value || ''})}
          floatLabelType='Auto'
        />
      </div>
      <button type='submit'>Submit</button>
    </form>
  );
}

export default App;
```

## FormValidator Integration

The TextArea component integrates seamlessly with Syncfusion's `FormValidator` component for comprehensive form validation.

### Basic FormValidator Setup

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { FormValidator } from '@syncfusion/ej2-inputs';
import { useEffect } from 'react';
import * as React from 'react';
import './App.css';

let formValidator;

function App() {
  useEffect(() => {
    const options = {
      rules: {
        comments: {
          required: [true, '* Please enter your comments']
        }
      }
    };
    
    formValidator = new FormValidator('#form1', options);
  }, []);

  return (
    <form id='form1'>
      <TextAreaComponent 
        id='comments'
        name='comments'
        placeholder='Enter your comments'
        floatLabelType='Auto'
      />
      <button type='submit'>Submit</button>
    </form>
  );
}

export default App;
```

### Validation with Multiple Rules

Apply multiple validation rules to a single TextArea:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { FormValidator } from '@syncfusion/ej2-inputs';
import { useEffect } from 'react';
import * as React from 'react';
import './App.css';

let formValidator;

function App() {
  useEffect(() => {
    const options = {
      rules: {
        message: {
          required: [true, '* Message is required'],
          minLength: [10, '* Minimum 10 characters required'],
          maxLength: [500, '* Maximum 500 characters allowed']
        }
      }
    };
    
    formValidator = new FormValidator('#form1', options);
  }, []);

  return (
    <form id='form1'>
      <TextAreaComponent 
        id='message'
        name='message'
        placeholder='Enter your message (10-500 chars)'
        floatLabelType='Auto'
        maxLength={500}
      />
      <button type='submit'>Submit</button>
    </form>
  );
}

export default App;
```

## Validation Rules

### Required Field

```typescript
rules: {
  feedback: {
    required: [true, '* Feedback is required']
  }
}
```

### Minimum Length

Enforce minimum character count:

```typescript
rules: {
  description: {
    minLength: [20, '* Minimum 20 characters required']
  }
}
```

### Maximum Length

Set maximum character limit:

```typescript
rules: {
  bio: {
    maxLength: [200, '* Maximum 200 characters allowed']
  }
}
```

### Pattern Matching

Validate against a regex pattern:

```typescript
rules: {
  code: {
    required: [true, '* Code is required'],
    pattern: [/^[A-Z0-9]{5,10}$/, '* Invalid code format']
  }
}
```

### Custom Validation

Define custom validation logic:

```typescript
rules: {
  email: {
    required: [true, '* Email is required'],
    email: [true, '* Please enter a valid email']
  },
  message: {
    required: [true, '* Message is required'],
    min: [5, '* Message must be at least 5 characters']
  }
}
```

## Form Submission

### Complete Feedback Form Example

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { FormValidator } from '@syncfusion/ej2-inputs';
import { useEffect, useState } from 'react';
import * as React from 'react';
import './App.css';

let formValidator;

function App() {
  const [submitStatus, setSubmitStatus] = useState('');

  useEffect(() => {
    const options = {
      rules: {
        email: {
          required: [true, '* Please enter valid email'],
          email: [true, '* Please enter a valid email address']
        },
        comments: {
          required: [true, '* Please enter your comments'],
          minLength: [10, '* Minimum 10 characters required']
        }
      }
    };
    
    formValidator = new FormValidator('#form1', options);
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (formValidator.validate()) {
      const formElement = e.currentTarget as HTMLFormElement;
      const formData = new FormData(formElement);
      
      console.log('Form submitted with:', Object.fromEntries(formData));
      setSubmitStatus('Form submitted successfully!');
      
      // Reset form
      formElement.reset();
      setTimeout(() => setSubmitStatus(''), 3000);
    }
  };

  return (
    <div>
      <form id='form1' onSubmit={handleSubmit}>
        <div className='form-group'>
          <div className='e-float-input'>
            <label>Email</label>
            <input 
              type='email' 
              id='email' 
              name='email'
              data-required-message='Required field'
              required
            />
            <span className='e-float-line'></span>
          </div>
          <div id='emailError'></div>
        </div>

        <div className='form-group'>
          <label>Comments</label>
          <TextAreaComponent 
            id='comments'
            name='comments'
            placeholder='Enter your comments'
            floatLabelType='Auto'
            required={true}
          />
          <div id='commentError'></div>
        </div>

        <div className='form-actions'>
          <button type='submit'>Submit</button>
          <button type='reset'>Reset</button>
        </div>
      </form>
      
      {submitStatus && <p className='success'>{submitStatus}</p>}
    </div>
  );
}

export default App;
```

## Error Display

### Error Container Pattern

Display validation errors in designated containers:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { FormValidator } from '@syncfusion/ej2-inputs';
import { useEffect } from 'react';
import * as React from 'react';
import './App.css';

let formValidator;

function App() {
  useEffect(() => {
    const options = {
      rules: {
        message: {
          required: [true, '* Message is required'],
          minLength: [5, '* Minimum 5 characters']
        }
      }
    };
    
    formValidator = new FormValidator('#myForm', options);
  }, []);

  return (
    <form id='myForm'>
      <div className='form-group'>
        <label>Your Message:</label>
        <TextAreaComponent 
          id='message'
          name='message'
          placeholder='Enter message'
          data-msg-containerid='messageError'
        />
        <div id='messageError' className='error-container'></div>
      </div>
      
      <button type='submit'>Submit</button>
    </form>
  );
}

export default App;
```

### Custom Error Styling

```css
.error-container {
  color: #d32f2f;
  font-size: 0.875rem;
  margin-top: 4px;
  display: none;
}

.error-container.show {
  display: block;
}

.e-field.e-error {
  border-color: #d32f2f;
  background-color: #ffebee;
}
```

### Real-Time Error Feedback

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [errors, setErrors] = useState<string[]>([]);

  const validateText = (value: string) => {
    const newErrors: string[] = [];
    
    if (!value || value.trim() === '') {
      newErrors.push('Text is required');
    } else if (value.length < 5) {
      newErrors.push('Minimum 5 characters required');
    } else if (value.length > 200) {
      newErrors.push('Maximum 200 characters exceeded');
    }
    
    setErrors(newErrors);
  };

  const handleInput = (args) => {
    const value = args.value || '';
    setText(value);
    validateText(value);
  };

  return (
    <div>
      <TextAreaComponent 
        id='feedback'
        value={text}
        input={handleInput}
        placeholder='Enter feedback'
        floatLabelType='Auto'
        cssClass={errors.length > 0 ? 'e-error' : ''}
      />
      {errors.length > 0 && (
        <div className='error-messages'>
          {errors.map((error, i) => (
            <p key={i} className='error-text'>{error}</p>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
```

## Best Practices

- Always use `name` attribute for form data collection
- Provide clear validation messages
- Set `required={true}` for mandatory fields
- Use `maxLength` property with validation rules for consistency
- Display errors near the input field
- Test form submission with various inputs
- Use `floatLabelType='Auto'` for modern UX
- Validate on both client and server side
- Clear errors when user corrects the input
- Provide visual feedback for validation states
