# Multiline TextBox

## Table of Contents

- [Creating Multiline TextBox](#creating-multiline-textbox)
- [Floating Labels with Multiline](#floating-labels-with-multiline)
- [Auto-Resizing TextBox](#auto-resizing-textbox)
- [Disabling Resize](#disabling-resize)
- [Limiting Text Length](#limiting-text-length)
- [Character Counting](#character-counting)

## Creating Multiline TextBox

Transform the TextBox component into a multiline input (textarea) for capturing longer text content like addresses, comments, descriptions, or messages.

### Basic Multiline

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function MultilineExample() {
  return (
    <TextBoxComponent
      multiline={true}
      placeholder="Enter your address"
    />
  );
}
```

**Default Behavior:**
- Renders as an HTML `<textarea>` element
- Users can manually resize the textarea by dragging the bottom-right corner
- No floating label by default

### Multiline with Value

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function MultilineWithValue() {
  return (
    <TextBoxComponent
      multiline={true}
      placeholder="Enter your address"
      value="123 Main Street, Suite 100, New York, NY 10001"
    />
  );
}
```

## Floating Labels with Multiline

Combine floating labels with multiline input for better UX:

### Floating Label Types

#### Auto (Recommended)

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function MultilineFloatingAuto() {
  return (
    <TextBoxComponent
      multiline={true}
      placeholder="Enter your address"
      floatLabelType="Auto"
    />
  );
}
```

**Behavior:** Label floats above when focused or has content

#### Always

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function MultilineFloatingAlways() {
  return (
    <TextBoxComponent
      multiline={true}
      placeholder="Enter your address"
      floatLabelType="Always"
    />
  );
}
```

**Behavior:** Label always visible above textarea

#### Never

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function MultilineFloatingNever() {
  return (
    <TextBoxComponent
      multiline={true}
      placeholder="Enter your address"
      floatLabelType="Never"
    />
  );
}
```

### Complete Example: All Float Types

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function MultilineFloatingDemo() {
  return (
    <div style={{ maxWidth: '500px', margin: '20px auto' }}>
      <div style={{ marginBottom: '30px' }}>
        <label><strong>Float Label Type: Auto</strong></label>
        <TextBoxComponent
          multiline={true}
          placeholder="Enter your address"
          floatLabelType="Auto"
        />
      </div>

      <div style={{ marginBottom: '30px' }}>
        <label><strong>Float Label Type: Always</strong></label>
        <TextBoxComponent
          multiline={true}
          placeholder="Enter your address"
          floatLabelType="Always"
        />
      </div>

      <div style={{ marginBottom: '30px' }}>
        <label><strong>Float Label Type: Never</strong></label>
        <TextBoxComponent
          multiline={true}
          placeholder="Enter your address"
          floatLabelType="Never"
        />
      </div>
    </div>
  );
}
```

## Auto-Resizing TextBox

Create a multiline TextBox that automatically expands vertically as users type more content. This provides a seamless typing experience without manual resizing.

### Implementation with Functional Component

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useRef } from 'react';

export default function AutoResizeTextbox() {
  const textboxRef = useRef<TextBoxComponent>(null);

  const handleCreate = () => {
    if (textboxRef.current) {
      // Set initial height based on scroll height
      const element = textboxRef.current.respectiveElement as HTMLTextAreaElement;
      element.style.height = 'auto';
      element.style.height = element.scrollHeight + 'px';
    }
  };

  const handleInput = () => {
    if (textboxRef.current) {
      // Update height as user types
      const element = textboxRef.current.respectiveElement as HTMLTextAreaElement;
      element.style.height = 'auto';
      element.style.height = element.scrollHeight + 'px';
    }
  };

  return (
    <TextBoxComponent
      multiline={true}
      placeholder="Start typing and the box will expand automatically..."
      floatLabelType="Auto"
      ref={textboxRef}
      created={handleCreate}
      input={handleInput}
      style={{ minHeight: '60px', resize: 'none' }}
    />
  );
}
```

### Implementation with Class Component

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

export default class AutoResizeTextbox extends React.Component {
  private textboxRef = React.createRef<TextBoxComponent>();

  private handleCreate = () => {
    const element = (this.textboxRef.current?.respectiveElement) as HTMLTextAreaElement;
    if (element) {
      element.style.height = 'auto';
      element.style.height = element.scrollHeight + 'px';
    }
  };

  private handleInput = () => {
    const element = (this.textboxRef.current?.respectiveElement) as HTMLTextAreaElement;
    if (element) {
      element.style.height = 'auto';
      element.style.height = element.scrollHeight + 'px';
    }
  };

  public render() {
    return (
      <TextBoxComponent
        multiline={true}
        placeholder="Start typing..."
        floatLabelType="Auto"
        ref={this.textboxRef}
        created={this.handleCreate}
        input={this.handleInput}
        style={{ minHeight: '60px', resize: 'none' }}
      />
    );
  }
}
```

### CSS for Auto-Resize

```css
.auto-resize-textbox textarea,
.e-float-input textarea {
  resize: none;
  overflow: hidden;
  min-height: 60px;
  padding: 12px;
  font-size: 15px;
  line-height: 1.5;
  transition: height 0.2s ease;
}
```

## Disabling Resize

By default, multiline TextBox allows users to manually resize. Disable this behavior with CSS:

### CSS to Disable Resize

```css
textarea.e-input,
.e-float-input textarea,
.e-float-input.e-control-wrapper textarea,
.e-input-group textarea,
.e-input-group.e-control-wrapper textarea {
  resize: none;
}
```

### Disable in Component

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function NoResizeTextbox() {
  return (
    <TextBoxComponent
      multiline={true}
      placeholder="This textarea cannot be resized"
      floatLabelType="Auto"
      cssClass="disable-resize"
    />
  );
}
```

**App.css:**

```css
.disable-resize {
  resize: none;
}

.disable-resize textarea,
.disable-resize.e-float-input textarea {
  resize: none !important;
}
```

## Limiting Text Length

Control the maximum number of characters users can enter using the `maxLength` property:

### Using maxLength via htmlAttributes

Pass `maxlength` as an HTML attribute using the `htmlAttributes` property:

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function MaxLengthTextbox() {
  return (
    <TextBoxComponent
      multiline={true}
      placeholder="Maximum 200 characters"
      floatLabelType="Auto"
      htmlAttributes={{ maxlength: '200' }}
    />
  );
}
```

### Adding maxLength Programmatically

Use the `addAttributes` method to add maxLength after component creation:

**Functional Component:**

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useRef } from 'react';

export default function ProgrammaticMaxLength() {
  const textboxRef = useRef<TextBoxComponent>(null);

  const addMaxLength = () => {
    if (textboxRef.current) {
      textboxRef.current.addAttributes({ maxlength: 150 });
    }
  };

  return (
    <div>
      <TextBoxComponent
        multiline={true}
        placeholder="Click button to add max length limit"
        floatLabelType="Auto"
        ref={textboxRef}
      />
      <button onClick={addMaxLength} style={{ marginTop: '10px' }}>
        Add Max Length (150 chars)
      </button>
    </div>
  );
}
```

**Class Component:**

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

export default class ProgrammaticMaxLength extends React.Component {
  private textboxRef = React.createRef<TextBoxComponent>();

  private addMaxLength = () => {
    if (this.textboxRef.current) {
      this.textboxRef.current.addAttributes({ maxlength: 150 });
    }
  };

  public render() {
    return (
      <div>
        <TextBoxComponent
          multiline={true}
          placeholder="Click to add max length"
          floatLabelType="Auto"
          ref={this.textboxRef}
        />
        <button onClick={this.addMaxLength}>Add Max Length</button>
      </div>
    );
  }
}
```

## Character Counting

Display a live character count as users type:

### Simple Character Counter

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

export default function CharacterCounter() {
  const [count, setCount] = useState(0);
  const maxChars = 200;

  const handleInput = (e: any) => {
    setCount(e.value.length);
  };

  return (
    <div style={{ maxWidth: '500px', margin: '20px auto' }}>
      <TextBoxComponent
        multiline={true}
        placeholder="Type your message..."
        floatLabelType="Auto"
        htmlAttributes={{ maxlength: maxChars.toString() }}
        input={handleInput}
      />
      <div style={{ marginTop: '8px', fontSize: '14px', color: '#666' }}>
        {count} / {maxChars} characters
      </div>
    </div>
  );
}
```

### Advanced Counter with Warning

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

export default function AdvancedCharacterCounter() {
  const [count, setCount] = useState(0);
  const [text, setText] = useState('');
  const maxChars = 300;
  const warningThreshold = 250;

  const handleInput = (e: any) => {
    const value = e.value;
    setText(value);
    setCount(value.length);
  };

  const percentUsed = (count / maxChars) * 100;
  const isWarning = count > warningThreshold;
  const isFull = count === maxChars;

  return (
    <div style={{ maxWidth: '500px', margin: '20px auto' }}>
      <TextBoxComponent
        multiline={true}
        placeholder="Type your feedback..."
        floatLabelType="Auto"
        htmlAttributes={{ maxlength: maxChars.toString() }}
        value={text}
        input={handleInput}
        cssClass={isFull ? 'e-error' : isWarning ? 'e-warning' : ''}
      />

      <div style={{ marginTop: '12px' }}>
        {/* Character Count Display */}
        <div style={{ 
          fontSize: '14px',
          color: isFull ? '#F44336' : isWarning ? '#FF9800' : '#666',
          fontWeight: 'bold'
        }}>
          {count} / {maxChars} characters
          {isWarning && count < maxChars && (
            <span style={{ marginLeft: '10px', color: '#FF9800' }}>
              ⚠️ Approaching limit
            </span>
          )}
          {isFull && (
            <span style={{ marginLeft: '10px', color: '#F44336' }}>
              ❌ Maximum reached
            </span>
          )}
        </div>

        {/* Progress Bar */}
        <div style={{
          marginTop: '8px',
          height: '6px',
          backgroundColor: '#E0E0E0',
          borderRadius: '3px',
          overflow: 'hidden'
        }}>
          <div style={{
            height: '100%',
            width: `${percentUsed}%`,
            backgroundColor: isFull ? '#F44336' : isWarning ? '#FF9800' : '#4CAF50',
            transition: 'all 0.3s ease'
          }} />
        </div>
      </div>

      {/* Word Count (Bonus) */}
      <div style={{ marginTop: '10px', fontSize: '13px', color: '#999' }}>
        Words: {text.trim().split(/\s+/).filter(w => w.length > 0).length}
      </div>
    </div>
  );
}
```

### Counter with Class Component

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

export default class CharacterCounter extends React.Component<{}, { count: number }> {
  constructor(props: {}) {
    super(props);
    this.state = { count: 0 };
  }

  private maxChars = 300;

  private handleInput = (e: any) => {
    this.setState({ count: e.value.length });
  };

  public render() {
    const { count } = this.state;

    return (
      <div style={{ maxWidth: '500px', margin: '20px auto' }}>
        <TextBoxComponent
          multiline={true}
          placeholder="Type your comment..."
          floatLabelType="Auto"
          htmlAttributes={{ maxlength: this.maxChars.toString() }}
          input={this.handleInput}
        />
        <div style={{ marginTop: '8px', fontSize: '14px', color: '#666' }}>
          {count} / {this.maxChars} characters
        </div>
      </div>
    );
  }
}
```

## Complete Example: Feedback Form

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useState, useRef } from 'react';

export default function FeedbackForm() {
  const [feedback, setFeedback] = useState('');
  const [charCount, setCharCount] = useState(0);
  const textboxRef = useRef<TextBoxComponent>(null);
  const maxChars = 500;

  const handleFeedbackChange = (e: any) => {
    setFeedback(e.value);
    setCharCount(e.value.length);
  };

  const handleAutoResize = () => {
    if (textboxRef.current) {
      const element = textboxRef.current.respectiveElement as HTMLTextAreaElement;
      element.style.height = 'auto';
      element.style.height = element.scrollHeight + 'px';
    }
  };

  const handleCreate = () => {
    handleAutoResize();
  };

  const handleSubmit = () => {
    if (feedback.trim().length === 0) {
      alert('Please enter your feedback');
      return;
    }
    console.log('Feedback submitted:', feedback);
    alert('Thank you for your feedback!');
    setFeedback('');
    setCharCount(0);
  };

  return (
    <div style={{ maxWidth: '600px', margin: '30px auto', padding: '20px' }}>
      <h2>Send Us Your Feedback</h2>
      <p>We value your feedback and would love to hear from you.</p>

      <TextBoxComponent
        multiline={true}
        placeholder="Please share your thoughts, suggestions, or concerns..."
        floatLabelType="Auto"
        htmlAttributes={{ maxlength: maxChars.toString() }}
        value={feedback}
        input={handleFeedbackChange}
        created={handleCreate}
        ref={textboxRef}
        style={{ minHeight: '150px', resize: 'none' }}
      />

      {/* Character Counter */}
      <div style={{ 
        marginTop: '12px', 
        fontSize: '14px',
        color: charCount > maxChars * 0.9 ? '#FF9800' : '#666'
      }}>
        <strong>{charCount}</strong> / {maxChars} characters
        {charCount > maxChars * 0.9 && (
          <span style={{ marginLeft: '10px', color: '#FF9800' }}>
            ⚠️ Approaching limit
          </span>
        )}
      </div>

      {/* Submit Button */}
      <button 
        onClick={handleSubmit}
        style={{
          marginTop: '20px',
          padding: '12px 24px',
          backgroundColor: '#2196F3',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
          fontSize: '16px'
        }}
      >
        Submit Feedback
      </button>
    </div>
  );
}
```

## See Also

- [Getting Started](./getting-started.md) - Basic TextBox setup
- [Features and Groups](./features-and-groups.md) - Floating labels and icons
- [Styling and Sizing](./styling-and-sizing.md) - CSS customization
- [Advanced Features](./advanced-features.md) - React hooks and adornments
