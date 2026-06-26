# TextBox Features and Groups

## Table of Contents

- [Floating Labels](#floating-labels)
- [Icons and Adornments](#icons-and-adornments)
- [Clear Button](#clear-button)
- [Rounded Corner](#rounded-corner)
- [Disabled State](#disabled-state)
- [Groups](#groups)
- [Combining Features](#combining-features)

## Floating Labels

Floating labels enhance user experience by automatically animating placeholder text into a label position when the input is focused or has a value.

### Float Label Types

#### Auto (Recommended Default)

The label floats above the input only when focused or contains a value:

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function App() {
  return (
    <TextBoxComponent 
      placeholder="First Name"
      floatLabelType="Auto"
    />
  );
}
```

**Behavior:**
- **Empty & unfocused:** Placeholder text appears inside the input
- **Focused or has value:** Placeholder animates above as floating label

#### Always

The label is always visible above the input, even when empty:

```tsx
<TextBoxComponent 
  placeholder="Last Name"
  floatLabelType="Always"
/>
```

**Use when:** You want the label always visible for clarity

#### Never

No floating label behavior; placeholder remains inside the input:

```tsx
<TextBoxComponent 
  placeholder="Email"
  floatLabelType="Never"
/>
```

**Use when:** Space is limited or you prefer traditional placeholder-only design

### Complete Float Label Example

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

export default function FloatLabelDemo() {
  const [values, setValues] = useState({
    firstName: '',
    lastName: '',
    email: ''
  });

  return (
    <div style={{ maxWidth: '400px', margin: '20px auto' }}>
      <div style={{ marginBottom: '20px' }}>
        <h4>FloatLabelType: Auto</h4>
        <TextBoxComponent
          placeholder="First Name"
          floatLabelType="Auto"
          value={values.firstName}
          change={(e) => setValues({ ...values, firstName: e.value })}
        />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h4>FloatLabelType: Always</h4>
        <TextBoxComponent
          placeholder="Last Name"
          floatLabelType="Always"
          value={values.lastName}
          change={(e) => setValues({ ...values, lastName: e.value })}
        />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h4>FloatLabelType: Never</h4>
        <TextBoxComponent
          placeholder="Email"
          floatLabelType="Never"
          type="email"
          value={values.email}
          change={(e) => setValues({ ...values, email: e.value })}
        />
      </div>
    </div>
  );
}
```

## Icons and Adornments

Add visual context or interactive elements using icons. Icons can be placed before (prepend) or after (append) the input.

### Using addIcon Method

The `addIcon()` method adds icons to the TextBox during the `created` event:

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useRef } from 'react';

export default function IconExample() {
  const textboxRef = useRef<TextBoxComponent>(null);

  const handleCreate = () => {
    if (textboxRef.current) {
      // addIcon(position, iconClass)
      textboxRef.current.addIcon('append', 'e-icons e-input-popup-date');
    }
  };

  return (
    <TextBoxComponent
      placeholder="Enter Date"
      floatLabelType="Auto"
      ref={textboxRef}
      created={handleCreate}
    />
  );
}
```

### Icon Positions

#### Append (Right Side)

```tsx
textboxRef.current.addIcon('append', 'e-icons e-input-popup-date');
```

Result:
```
┌──────────────────────────┐
│ Enter Date            📅  │
└──────────────────────────┘
```

#### Prepend (Left Side)

```tsx
textboxRef.current.addIcon('prepend', 'e-icons e-user');
```

Result:
```
┌──────────────────────────┐
│ 👤 Enter Name           │
└──────────────────────────┘
```

#### Both Sides

```tsx
const handleCreate = () => {
  if (textboxRef.current) {
    textboxRef.current.addIcon('prepend', 'e-icons e-user');
    textboxRef.current.addIcon('append', 'e-icons e-input-popup-date');
  }
};
```

Result:
```
┌──────────────────────────────┐
│ 👤 Enter Date            📅  │
└──────────────────────────────┘
```

### Common Icon Classes

| Icon Class | Visual | Use Case |
|-----------|--------|----------|
| `e-input-popup-date` | 📅 Calendar | Date/date-time inputs |
| `e-input-down` | ⬇️ Dropdown arrow | Dropdown/combo inputs |
| `e-user` | 👤 User profile | Username/name fields |
| `e-people` | 👥 Group | Team/group fields |
| `e-trash` | 🗑️ Delete | Clear/remove action |
| `e-eye` | 👁️ Eye open | Show password toggle |
| `e-eye-slash` | 👁️‍🗨️ Eye closed | Hide password toggle |

## Clear Button

The clear button automatically appears when the input has a value and disappears when empty, providing users a quick way to reset the field.

### Enabling Clear Button

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function ClearButtonExample() {
  return (
    <TextBoxComponent
      placeholder="Enter your text"
      floatLabelType="Auto"
      showClearButton={true}
    />
  );
}
```

**Behavior:**
- **Empty:** No clear button visible
- **Has value:** Clear button (×) appears on the right
- **Click clear button:** Input value clears, button disappears

### Clear Button with Icons

Combine clear button with prepended icons:

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useRef } from 'react';

export default function ClearWithIcon() {
  const textboxRef = useRef<TextBoxComponent>(null);

  const handleCreate = () => {
    if (textboxRef.current) {
      textboxRef.current.addIcon('prepend', 'e-icons e-user');
    }
  };

  return (
    <TextBoxComponent
      placeholder="Enter username"
      floatLabelType="Auto"
      showClearButton={true}
      ref={textboxRef}
      created={handleCreate}
    />
  );
}
```

Result:
```
Empty:
┌────────────────────────────┐
│ 👤 Enter username          │
└────────────────────────────┘

With value:
┌────────────────────────────┐
│ 👤 john_doe            ×   │
└────────────────────────────┘
```

### Custom Clear Button Action

Monitor when clear button is clicked:

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

export default function ClearWithAction() {
  const [inputValue, setInputValue] = useState('');

  const handleChange = (e: any) => {
    setInputValue(e.value);
  };

  return (
    <>
      <TextBoxComponent
        placeholder="Search..."
        floatLabelType="Auto"
        showClearButton={true}
        value={inputValue}
        change={handleChange}
      />
      <p>Current value: {inputValue || '(empty)'}</p>
    </>
  );
}
```

## Rounded Corner

Apply rounded corners to the TextBox by adding the `e-corner` CSS class using the `cssClass` property. This creates a modern, polished appearance.

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function RoundedCornerExample() {
  return (
    <TextBoxComponent
      placeholder="Enter Date"
      cssClass="e-corner"
    />
  );
}
```

## Disabled State

Disable user interaction with the TextBox by setting the `enabled` property to `false`. A disabled TextBox prevents input, prevents focus, and displays with reduced opacity.

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function DisabledExample() {
  return (
    <TextBoxComponent
      placeholder="Enter Name"
      enabled={false}
    />
  );
}
```

### Toggle Enabled/Disabled State

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

export default function ToggleEnabled() {
  const [isEnabled, setIsEnabled] = useState(true);

  return (
    <div>
      <TextBoxComponent
        placeholder="Enter text"
        floatLabelType="Auto"
        enabled={isEnabled}
      />
      <button onClick={() => setIsEnabled(!isEnabled)}>
        {isEnabled ? 'Disable' : 'Enable'} TextBox
      </button>
    </div>
  );
}
```

## Groups

Groups organize related input elements together with optional labels, icons, and styling.

### Icon with Floating Label

Combine icons and floating labels for enhanced input groups:

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useRef } from 'react';

export default function IconWithFloatingLabel() {
  const textboxRef = useRef<TextBoxComponent>(null);

  const handleCreate = () => {
    if (textboxRef.current) {
      textboxRef.current.addIcon('append', 'e-icons e-input-popup-date');
    }
  };

  return (
    <div>
      <h4>TextBox with icon and floating label</h4>
      <TextBoxComponent
        id="date-input"
        placeholder="Enter Date"
        floatLabelType="Auto"
        ref={textboxRef}
        created={handleCreate}
      />
    </div>
  );
}
```

### Multiple Inputs with Clear Buttons

Create a group of related inputs, each with clear button:

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

export default function SearchFilters() {
  const [filters, setFilters] = useState({
    name: '',
    email: '',
    phone: ''
  });

  const handleChange = (field: string, value: string) => {
    setFilters({ ...filters, [field]: value });
  };

  return (
    <div style={{ maxWidth: '400px', margin: '20px auto' }}>
      <h3>Search Filters</h3>

      <div style={{ marginBottom: '15px' }}>
        <TextBoxComponent
          placeholder="Name"
          floatLabelType="Auto"
          showClearButton={true}
          value={filters.name}
          change={(e) => handleChange('name', e.value)}
        />
      </div>

      <div style={{ marginBottom: '15px' }}>
        <TextBoxComponent
          placeholder="Email"
          floatLabelType="Auto"
          showClearButton={true}
          type="email"
          value={filters.email}
          change={(e) => handleChange('email', e.value)}
        />
      </div>

      <div style={{ marginBottom: '15px' }}>
        <TextBoxComponent
          placeholder="Phone"
          floatLabelType="Auto"
          showClearButton={true}
          value={filters.phone}
          change={(e) => handleChange('phone', e.value)}
        />
      </div>

      <button>Search</button>
    </div>
  );
}
```

## Combining Features

### Comprehensive Example: Complete Registration Form

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useState, useRef } from 'react';

export default function RegistrationForm() {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    phone: '',
    address: ''
  });

  const passwordRef = useRef<TextBoxComponent>(null);

  const handleChange = (field: string, value: string) => {
    setFormData({ ...formData, [field]: value });
  };

  const togglePasswordVisibility = () => {
    if (passwordRef.current) {
      const currentType = passwordRef.current.type;
      passwordRef.current.type = currentType === 'password' ? 'text' : 'password';
    }
  };

  const handleCreate = () => {
    if (passwordRef.current) {
      passwordRef.current.addIcon('append', 'e-icons e-eye');
    }
  };

  return (
    <div style={{ maxWidth: '500px', margin: '20px auto', padding: '20px' }}>
      <h2>User Registration</h2>

      {/* First Name */}
      <div style={{ marginBottom: '20px' }}>
        <TextBoxComponent
          placeholder="First Name"
          floatLabelType="Auto"
          showClearButton={true}
          value={formData.firstName}
          change={(e) => handleChange('firstName', e.value)}
        />
      </div>

      {/* Last Name */}
      <div style={{ marginBottom: '20px' }}>
        <TextBoxComponent
          placeholder="Last Name"
          floatLabelType="Auto"
          showClearButton={true}
          value={formData.lastName}
          change={(e) => handleChange('lastName', e.value)}
        />
      </div>

      {/* Email */}
      <div style={{ marginBottom: '20px' }}>
        <TextBoxComponent
          placeholder="Email Address"
          floatLabelType="Auto"
          showClearButton={true}
          type="email"
          value={formData.email}
          change={(e) => handleChange('email', e.value)}
        />
      </div>

      {/* Password with visibility toggle */}
      <div style={{ marginBottom: '20px' }}>
        <TextBoxComponent
          ref={passwordRef}
          type="password"
          placeholder="Password"
          floatLabelType="Auto"
          value={formData.password}
          change={(e) => handleChange('password', e.value)}
          created={handleCreate}
        />
      </div>

      {/* Phone */}
      <div style={{ marginBottom: '20px' }}>
        <TextBoxComponent
          placeholder="Phone Number"
          floatLabelType="Auto"
          showClearButton={true}
          type="tel"
          value={formData.phone}
          change={(e) => handleChange('phone', e.value)}
        />
      </div>

      {/* Address (multiline) */}
      <div style={{ marginBottom: '20px' }}>
        <TextBoxComponent
          placeholder="Address"
          floatLabelType="Auto"
          multiline={true}
          value={formData.address}
          change={(e) => handleChange('address', e.value)}
        />
      </div>

      <button style={{ padding: '10px 20px' }}>Submit</button>
    </div>
  );
}
```

This example demonstrates:
- ✅ Floating labels for all inputs
- ✅ Clear button on most fields
- ✅ Icons with password visibility toggle
- ✅ Different input types (email, tel, password)
- ✅ Multiline input for address
- ✅ State management with `useState`

## See Also

- [Getting Started](./getting-started.md) - Initial setup and installation
- [Styling and Sizing](./styling-and-sizing.md) - Size variations and CSS customization
- [Validation and States](./validation-and-states.md) - Error, warning, and success states
- [Advanced Features](./advanced-features.md) - Adornments and React hooks
