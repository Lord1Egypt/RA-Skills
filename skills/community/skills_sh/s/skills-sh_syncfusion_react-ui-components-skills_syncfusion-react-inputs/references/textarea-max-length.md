# Maximum Length in React TextArea Component

Enforce character limit restrictions to control input length and prevent users from exceeding specified bounds. The `maxLength` property defines the maximum number of characters allowed.

## Setting Maximum Length

### Basic Usage

Use the `maxLength` property to restrict character input:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='comments'
      placeholder='Enter your comments'
      maxLength={500}
    />
  );
}

export default App;
```

When the user reaches the character limit, the TextArea prevents further input, ensuring compliance with the defined character limit.

## Character Limit Enforcement

### Automatic Prevention

Once the character limit is reached, users cannot type additional characters:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent 
      id='bio'
      placeholder='Your bio (max 200 chars)'
      maxLength={200}
      floatLabelType='Auto'
    />
  );
}

export default App;
```

**Behavior:**
- Characters can be entered up to the limit
- Input is rejected when limit is reached
- User can still delete or edit existing content
- Paste operations are truncated to fit the limit

## User Feedback

### Display Character Count

Show users how many characters they've entered and how many remain:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const [charCount, setCharCount] = useState(0);
  const maxChars = 500;
  const remaining = maxChars - charCount;

  const handleInput = (args) => {
    setCharCount((args.value || '').length);
  };

  return (
    <div>
      <TextAreaComponent 
        id='message'
        placeholder='Enter your message'
        maxLength={maxChars}
        input={handleInput}
        floatLabelType='Auto'
      />
      <p className='char-info'>
        {charCount} / {maxChars} characters
      </p>
      {remaining <= 50 && (
        <p className='warning'>
          {remaining} characters remaining
        </p>
      )}
    </div>
  );
}

export default App;
```

### Character Count with Progress Bar

Visual representation of character usage:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const [charCount, setCharCount] = useState(0);
  const maxChars = 500;
  const percentage = (charCount / maxChars) * 100;

  const handleInput = (args) => {
    setCharCount((args.value || '').length);
  };

  return (
    <div>
      <TextAreaComponent 
        id='feedback'
        placeholder='Share your feedback'
        maxLength={maxChars}
        input={handleInput}
      />
      
      <div className='progress-container'>
        <div 
          className='progress-bar'
          style={{width: `${percentage}%`}}
        ></div>
      </div>
      
      <span className='char-count'>
        {charCount} of {maxChars}
      </span>
    </div>
  );
}

export default App;
```

### Styling Based on Character Count

Apply different styles as users approach the limit:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const [charCount, setCharCount] = useState(0);
  const maxChars = 500;
  const percentage = (charCount / maxChars) * 100;

  const getStatusClass = () => {
    if (percentage < 50) return 'status-good';
    if (percentage < 80) return 'status-warning';
    return 'status-danger';
  };

  const handleInput = (args) => {
    setCharCount((args.value || '').length);
  };

  return (
    <div>
      <TextAreaComponent 
        id='essay'
        placeholder='Write your essay'
        maxLength={maxChars}
        input={handleInput}
        cssClass={getStatusClass()}
      />
      
      <div className={`char-status ${getStatusClass()}`}>
        <span>{charCount}/{maxChars}</span>
      </div>
    </div>
  );
}

export default App;
```

## Form Validation

### Combining with Validation Rules

Use maxLength with FormValidator:

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
        description: {
          required: [true, '* Description is required'],
          minLength: [50, '* Minimum 50 characters'],
          maxLength: [500, '* Maximum 500 characters']
        }
      }
    };
    
    formValidator = new FormValidator('#form1', options);
  }, []);

  return (
    <form id='form1'>
      <TextAreaComponent 
        id='description'
        name='description'
        placeholder='Product description (50-500 chars)'
        maxLength={500}
      />
      <button type='submit'>Submit</button>
    </form>
  );
}

export default App;
```

## Best Practices

### Setting Appropriate Limits

Choose limits based on use case:

```typescript
// Short feedback (Twitter-like)
<TextAreaComponent maxLength={280} />

// Medium form textarea
<TextAreaComponent maxLength={500} />

// Long essay or comment
<TextAreaComponent maxLength={2000} />

// Generous limit for detailed content
<TextAreaComponent maxLength={5000} />
```

### Mobile-Friendly Implementation

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const [charCount, setCharCount] = useState(0);
  const maxChars = 300; // Lower for mobile

  const handleInput = (args) => {
    setCharCount((args.value || '').length);
  };

  return (
    <div className='mobile-textarea'>
      <TextAreaComponent 
        id='feedback'
        maxLength={maxChars}
        input={handleInput}
        placeholder='Your feedback'
        showClearButton={true}
      />
      
      <div className='mobile-info'>
        <span className='count'>{charCount}/{maxChars}</span>
        <p className='hint'>
          {maxChars - charCount} characters left
        </p>
      </div>
    </div>
  );
}

export default App;
```

## Edge Cases

### Paste Behavior

Pasted content is truncated to fit within the limit:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  // When user pastes 1000 characters into maxLength={500},
  // only the first 500 characters are retained
  
  return (
    <TextAreaComponent 
      id='content'
      maxLength={500}
      placeholder='Paste text here (max 500 chars)'
    />
  );
}

export default App;
```

### Initial Value Handling

Initial values longer than maxLength are not truncated:

```typescript
// This will display all content even if value exceeds maxLength
<TextAreaComponent 
  id='text'
  value='This is a very long text that exceeds 500 chars'
  maxLength={500}
/>
```

To handle this, truncate initial values:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  const initialValue = 'Long text...';
  const maxChars = 500;
  
  const truncatedValue = initialValue.length > maxChars 
    ? initialValue.substring(0, maxChars)
    : initialValue;

  return (
    <TextAreaComponent 
      id='text'
      value={truncatedValue}
      maxLength={maxChars}
    />
  );
}

export default App;
```

## Real-World Examples

### Comment Form with Limit

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const [comment, setComment] = useState('');
  const maxChars = 500;
  const isNearLimit = comment.length > maxChars - 50;

  const handleSubmit = () => {
    if (comment.trim().length > 0) {
      console.log('Submitting comment:', comment);
      setComment('');
    }
  };

  return (
    <div className='comment-form'>
      <TextAreaComponent 
        id='comment'
        value={comment}
        input={(args) => setComment(args.value || '')}
        maxLength={maxChars}
        placeholder='Share your thoughts...'
        floatLabelType='Auto'
      />
      
      <div className='form-footer'>
        <span className={isNearLimit ? 'warning' : ''}>
          {comment.length} / {maxChars}
        </span>
        <button 
          onClick={handleSubmit}
          disabled={comment.trim().length === 0}
        >
          Post Comment
        </button>
      </div>
    </div>
  );
}

export default App;
```

### Product Review Form

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const [review, setReview] = useState('');
  const maxChars = 1000;
  const minChars = 50;
  const isValid = review.length >= minChars && review.length <= maxChars;

  return (
    <div>
      <TextAreaComponent 
        id='review'
        value={review}
        input={(args) => setReview(args.value || '')}
        maxLength={maxChars}
        placeholder='Write your review here...'
        rows={6}
      />
      
      <div className={`review-stats ${isValid ? 'valid' : 'invalid'}`}>
        <p>{review.length} / {maxChars} characters</p>
        {review.length < minChars && (
          <p>Minimum {minChars} characters required</p>
        )}
      </div>
      
      <button disabled={!isValid}>Submit Review</button>
    </div>
  );
}

export default App;
```
