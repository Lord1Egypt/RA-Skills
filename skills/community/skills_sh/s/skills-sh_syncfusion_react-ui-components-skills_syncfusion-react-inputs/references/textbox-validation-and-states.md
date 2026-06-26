# Validation and States

## Table of Contents

- [Validation States](#validation-states)
- [Disabled State](#disabled-state)
- [Read-Only State](#read-only-state)
- [Dynamic State Changes](#dynamic-state-changes)
- [Color Changes Based on Value](#color-changes-based-on-value)

## Validation States

The TextBox supports three predefined validation states to provide visual feedback: `error`, `warning`, and `success`. Apply these states using CSS classes via the `cssClass` property.

### Error State

Use the error state to indicate invalid input:

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function ErrorStateExample() {
  return (
    <TextBoxComponent
      placeholder="Input with error"
      cssClass="e-error"
      floatLabelType="Auto"
    />
  );
}
```

**Appearance:**
- Red border around the input
- Red floating label (if applicable)
- Typically used for invalid email, required fields not filled, etc.

### Warning State

Use the warning state to highlight caution or potential issues:

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function WarningStateExample() {
  return (
    <TextBoxComponent
      placeholder="Input with warning"
      cssClass="e-warning"
      floatLabelType="Auto"
    />
  );
}
```

**Appearance:**
- Orange/yellow border
- Orange/yellow floating label
- Used for weak passwords, future dates, etc.

### Success State

Use the success state to indicate valid input:

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function SuccessStateExample() {
  return (
    <TextBoxComponent
      placeholder="Input with success"
      cssClass="e-success"
      floatLabelType="Auto"
    />
  );
}
```

**Appearance:**
- Green border
- Green floating label
- Used for confirmed entries, validated data, etc.

### All Three States

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function ValidationStatesDemo() {
  return (
    <div style={{ maxWidth: '400px', margin: '20px auto' }}>
      <div style={{ marginBottom: '20px' }}>
        <h4>Warning State</h4>
        <TextBoxComponent
          placeholder="Input with warning"
          cssClass="e-warning"
          floatLabelType="Auto"
        />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h4>Error State</h4>
        <TextBoxComponent
          placeholder="Input with error"
          cssClass="e-error"
          floatLabelType="Auto"
        />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h4>Success State</h4>
        <TextBoxComponent
          placeholder="Input with success"
          cssClass="e-success"
          floatLabelType="Auto"
        />
      </div>
    </div>
  );
}
```

### Functional Component with Validation

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

export default function ValidatedInput() {
  const [email, setEmail] = useState('');
  const [validationState, setValidationState] = useState('');

  const validateEmail = (value: string) => {
    if (!value) {
      setValidationState(''); // No state when empty
    } else if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
      setValidationState('e-success');
    } else {
      setValidationState('e-error');
    }
  };

  const handleChange = (e: any) => {
    const value = e.value;
    setEmail(value);
    validateEmail(value);
  };

  return (
    <div style={{ maxWidth: '400px', margin: '20px auto' }}>
      <h3>Email Validation</h3>
      <TextBoxComponent
        type="email"
        placeholder="Enter email"
        floatLabelType="Auto"
        value={email}
        change={handleChange}
        cssClass={validationState}
      />
      <p style={{ marginTop: '10px', fontSize: '14px', color: '#666' }}>
        {validationState === 'e-success' && '✓ Valid email'}
        {validationState === 'e-error' && '✗ Invalid email format'}
        {!validationState && 'Enter an email address'}
      </p>
    </div>
  );
}
```

### Class Component with Validation

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

export default class ValidatedInput extends React.Component<{}, { 
  password: string;
  validationState: string;
}> {
  constructor(props: {}) {
    super(props);
    this.state = { password: '', validationState: '' };
  }

  private validatePassword = (value: string) => {
    if (!value) {
      this.setState({ validationState: '' });
    } else if (value.length < 8) {
      this.setState({ validationState: 'e-warning' });
    } else if (value.length >= 12) {
      this.setState({ validationState: 'e-success' });
    } else {
      this.setState({ validationState: 'e-warning' });
    }
  };

  private handleChange = (e: any) => {
    const value = e.value;
    this.setState({ password: value });
    this.validatePassword(value);
  };

  public render() {
    const { password, validationState } = this.state;

    return (
      <div style={{ maxWidth: '400px', margin: '20px auto' }}>
        <h3>Password Strength</h3>
        <TextBoxComponent
          type="password"
          placeholder="Enter password"
          floatLabelType="Auto"
          value={password}
          change={this.handleChange}
          cssClass={validationState}
        />
        <p style={{ marginTop: '10px', fontSize: '14px' }}>
          {validationState === 'e-warning' && '⚠️ Weak password (min 8 characters)'}
          {validationState === 'e-success' && '✓ Strong password'}
          {!validationState && 'Enter at least 8 characters'}
        </p>
      </div>
    );
  }
}
```

## Disabled State

Disable TextBox to prevent user interaction while keeping it visible. Use the `enabled` property set to `false`:

### Basic Disabled State

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function DisabledExample() {
  return (
    <TextBoxComponent
      placeholder="This input is disabled"
      floatLabelType="Auto"
      enabled={false}
      value="Cannot edit this value"
    />
  );
}
```

**Behavior:**
- Input appears greyed out
- User cannot click or type
- Value cannot be changed

### Toggle Enabled/Disabled State

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

export default function ToggleDisabled() {
  const [isEnabled, setIsEnabled] = useState(true);
  const [inputValue, setInputValue] = useState('Type here');

  return (
    <div style={{ maxWidth: '400px', margin: '20px auto' }}>
      <div style={{ marginBottom: '20px' }}>
        <button onClick={() => setIsEnabled(!isEnabled)}>
          {isEnabled ? 'Disable' : 'Enable'} Input
        </button>
      </div>

      <TextBoxComponent
        placeholder="Try to edit"
        floatLabelType="Auto"
        enabled={isEnabled}
        value={inputValue}
        change={(e) => setInputValue(e.value)}
      />

      <p style={{ marginTop: '10px', fontSize: '14px', color: '#666' }}>
        State: {isEnabled ? '🔓 Enabled' : '🔒 Disabled'}
      </p>
    </div>
  );
}
```

## Read-Only State

Make the input read-only so users can view and select the content but cannot edit it. Use the `readonly` property:

### Basic Read-Only State

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function ReadOnlyExample() {
  return (
    <TextBoxComponent
      placeholder="Read-only value"
      floatLabelType="Auto"
      readonly={true}
      value="This value cannot be edited"
    />
  );
}
```

**Behavior:**
- Input appears normal (not greyed out)
- User can select and copy the text
- User cannot edit the content
- Can be focused and included in tab order

### Disabled (`enabled={false}`) vs Read-Only (`readonly={true}`)

| Feature | Disabled (`enabled={false}`) | Read-Only (`readonly={true}`) |
|---------|------------------------------|-------------------------------|
| **Appearance** | Greyed out | Normal |
| **Selectable** | No | Yes |
| **Copyable** | No | Yes |
| **Tab Focus** | No | Yes |
| **Form Submit** | Excluded | Included |
| **Use Case** | Temporary disable | Display data, prevent editing |

### Example: Disabled vs Read-Only

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function DisabledVsReadOnly() {
  return (
    <div style={{ maxWidth: '500px', margin: '20px auto' }}>
      <div style={{ marginBottom: '20px' }}>
        <h4>Disabled State (enabled=false)</h4>
        <TextBoxComponent
          placeholder="Disabled"
          floatLabelType="Auto"
          enabled={false}
          value="Cannot select or edit"
        />
        <small>Greyed out, not copyable</small>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h4>Read-Only State</h4>
        <TextBoxComponent
          placeholder="Read-Only"
          floatLabelType="Auto"
          readonly={true}
          value="Can select and copy but not edit"
        />
        <small>Normal appearance, selectable</small>
      </div>
    </div>
  );
}
```

## Dynamic State Changes

Change validation states dynamically based on user input or application logic:

### Form Validation Example

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

export default function FormValidation() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: ''
  });

  const [validationStates, setValidationStates] = useState({
    username: '',
    email: '',
    password: ''
  });

  // Username validation: min 3 characters
  const validateUsername = (value: string) => {
    if (!value) return '';
    return value.length < 3 ? 'e-error' : 'e-success';
  };

  // Email validation
  const validateEmail = (value: string) => {
    if (!value) return '';
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) ? 'e-success' : 'e-error';
  };

  // Password validation: min 8 characters, mix of letter and number
  const validatePassword = (value: string) => {
    if (!value) return '';
    const hasLetters = /[a-zA-Z]/.test(value);
    const hasNumbers = /[0-9]/.test(value);
    
    if (value.length < 8) return 'e-error';
    if (!hasLetters || !hasNumbers) return 'e-warning';
    return 'e-success';
  };

  const handleUsernameChange = (e: any) => {
    const value = e.value;
    setFormData({ ...formData, username: value });
    setValidationStates({
      ...validationStates,
      username: validateUsername(value)
    });
  };

  const handleEmailChange = (e: any) => {
    const value = e.value;
    setFormData({ ...formData, email: value });
    setValidationStates({
      ...validationStates,
      email: validateEmail(value)
    });
  };

  const handlePasswordChange = (e: any) => {
    const value = e.value;
    setFormData({ ...formData, password: value });
    setValidationStates({
      ...validationStates,
      password: validatePassword(value)
    });
  };

  const isFormValid = 
    validationStates.username === 'e-success' &&
    validationStates.email === 'e-success' &&
    validationStates.password === 'e-success';

  return (
    <div style={{ maxWidth: '500px', margin: '30px auto' }}>
      <h2>Create Account</h2>

      {/* Username */}
      <div style={{ marginBottom: '20px' }}>
        <TextBoxComponent
          placeholder="Username"
          floatLabelType="Auto"
          value={formData.username}
          change={handleUsernameChange}
          cssClass={validationStates.username}
        />
        <small style={{ display: 'block', marginTop: '5px', color: '#666' }}>
          {validationStates.username === 'e-success' && '✓ Valid username'}
          {validationStates.username === 'e-error' && '✗ At least 3 characters required'}
        </small>
      </div>

      {/* Email */}
      <div style={{ marginBottom: '20px' }}>
        <TextBoxComponent
          placeholder="Email"
          floatLabelType="Auto"
          type="email"
          value={formData.email}
          change={handleEmailChange}
          cssClass={validationStates.email}
        />
        <small style={{ display: 'block', marginTop: '5px', color: '#666' }}>
          {validationStates.email === 'e-success' && '✓ Valid email'}
          {validationStates.email === 'e-error' && '✗ Invalid email format'}
        </small>
      </div>

      {/* Password */}
      <div style={{ marginBottom: '20px' }}>
        <TextBoxComponent
          placeholder="Password"
          floatLabelType="Auto"
          type="password"
          value={formData.password}
          change={handlePasswordChange}
          cssClass={validationStates.password}
        />
        <small style={{ display: 'block', marginTop: '5px', color: '#666' }}>
          {validationStates.password === 'e-success' && '✓ Strong password'}
          {validationStates.password === 'e-warning' && '⚠️ Include letters and numbers'}
          {validationStates.password === 'e-error' && '✗ At least 8 characters required'}
        </small>
      </div>

      {/* Submit Button */}
      <button 
        disabled={!isFormValid}
        style={{
          padding: '12px 20px',
          backgroundColor: isFormValid ? '#4CAF50' : '#CCC',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: isFormValid ? 'pointer' : 'not-allowed'
        }}
      >
        Create Account
      </button>

      <p style={{ marginTop: '15px', fontSize: '14px', color: '#666' }}>
        Form Status: {isFormValid ? '✓ All fields valid' : '✗ Complete the form'}
      </p>
    </div>
  );
}
```

## Color Changes Based on Value

Change TextBox colors dynamically based on input using the `input` event (fires on every keystroke) or `change` event (fires on blur):

### Dynamic Color Example

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

export default function DynamicColorTextbox() {
  const [cssClass, setCssClass] = useState('');

  const handleInput = (e: any) => {
    const inputValue = e.value;

    // Change color based on whether value is numeric
    const isNumeric = /^[0-9]+$/.test(inputValue);
    if (!inputValue) {
      setCssClass('');
    } else if (!isNumeric) {
      setCssClass('e-error');
    } else {
      setCssClass('e-success');
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '20px auto' }}>
      <h3>Enter Numeric Values</h3>
      <TextBoxComponent
        placeholder="Enter numeric values"
        floatLabelType="Auto"
        input={handleInput}
        cssClass={cssClass}
      />
    </div>
  );
}
```

### Stock Price Color Indicator

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

export default function StockPriceIndicator() {
  const [price, setPrice] = useState('');
  const [status, setStatus] = useState('');
  const basePrice = 100;

  const handleChange = (e: any) => {
    const value = parseFloat(e.value);
    setPrice(e.value);

    if (!e.value) {
      setStatus('');
    } else if (isNaN(value)) {
      setStatus('e-error');
    } else {
      const change = value - basePrice;
      if (change > 0) {
        setStatus('e-success'); // Price up - green
      } else if (change < 0) {
        setStatus('e-error'); // Price down - red
      } else {
        setStatus(''); // Price unchanged - normal
      }
    }
  };

  const change = parseFloat(price) - basePrice || 0;

  return (
    <div style={{ maxWidth: '400px', margin: '20px auto' }}>
      <h3>Stock Price Tracker</h3>
      <p>Base Price: ${basePrice}</p>

      <TextBoxComponent
        placeholder="Enter current price"
        floatLabelType="Auto"
        type="number"
        value={price}
        change={handleChange}
        cssClass={status}
      />

      {price && (
        <div style={{ marginTop: '10px', fontSize: '14px' }}>
          <p>Change: ${change > 0 ? '+' : ''}{change.toFixed(2)}</p>
          <p style={{
            color: change > 0 ? '#4CAF50' : change < 0 ? '#F44336' : '#666'
          }}>
            {change > 0 ? '↑ Up' : change < 0 ? '↓ Down' : '→ Unchanged'}
          </p>
        </div>
      )}
    </div>
  );
}
```

## See Also

- [Getting Started](./getting-started.md) - Basic setup
- [Features and Groups](./features-and-groups.md) - Floating labels and icons
- [Styling and Sizing](./styling-and-sizing.md) - CSS customization
- [Advanced Features](./advanced-features.md) - React hooks and adornments
