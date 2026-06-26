# Styling and Sizing

## Table of Contents

- [Predefined Sizes](#predefined-sizes)
- [Rounded Corner](#rounded-corner)
- [CSS Customization](#css-customization)
- [Floating Label Styling](#floating-label-styling)
- [TextBox Wrapper Styling](#textbox-wrapper-styling)
- [Theme Variations](#theme-variations)

## Predefined Sizes

The TextBox component supports three predefined sizes to match different layout requirements:

| Size | CSS Class | Use Case |
|------|-----------|----------|
| **Normal** | (default) | Standard desktop layouts |
| **Small** | `e-small` | Compact forms, limited space, dense UIs |
| **Large** | `e-bigger` | Mobile interfaces, touch targets, better accessibility |

### Applying Size Classes

Use the `cssClass` property to apply size classes:

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function SizeExample() {
  return (
    <div style={{ maxWidth: '400px', margin: '20px auto' }}>
      {/* Normal Size (Default) */}
      <div style={{ marginBottom: '20px' }}>
        <h4>Normal Size</h4>
        <TextBoxComponent
          placeholder="Enter text"
          floatLabelType="Auto"
        />
      </div>

      {/* Small Size */}
      <div style={{ marginBottom: '20px' }}>
        <h4>Small Size</h4>
        <TextBoxComponent
          placeholder="Enter text"
          floatLabelType="Auto"
          cssClass="e-small"
        />
      </div>

      {/* Large Size */}
      <div style={{ marginBottom: '20px' }}>
        <h4>Large Size</h4>
        <TextBoxComponent
          placeholder="Enter text"
          floatLabelType="Auto"
          cssClass="e-bigger"
        />
      </div>
    </div>
  );
}
```

### Size Comparison

```
Normal:  ┌─────────────────────┐
         │ Enter text          │
         └─────────────────────┘ (height: ~38px)

Small:   ┌──────────────┐
         │ Enter text   │
         └──────────────┘ (height: ~30px)

Large:   ┌─────────────────────────┐
         │ Enter text              │
         └─────────────────────────┘ (height: ~48px)
```

### Combining Size with Other Classes

Apply multiple classes using string concatenation:

```tsx
<TextBoxComponent
  placeholder="Search"
  floatLabelType="Auto"
  cssClass="e-small"
/>
```

## Rounded Corner

Apply rounded corners to the TextBox by adding the `e-corner` CSS class using the `cssClass` property. This creates a modern, polished appearance that aligns with contemporary design standards.

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

You can also combine `e-corner` with size classes:

```tsx
<TextBoxComponent placeholder="Small rounded" cssClass="e-corner e-small" floatLabelType="Auto" />
<TextBoxComponent placeholder="Large rounded" cssClass="e-corner e-bigger" floatLabelType="Auto" />
```

## CSS Customization

Customize TextBox appearance with CSS rules targeting various selectors.

### Custom Font Size and Height

```css
/* Apply to all TextBox inputs */
.e-input:not(:valid),
.e-input:valid,
.e-float-input.e-control-wrapper input:not(:valid),
.e-float-input.e-control-wrapper input:valid,
.e-float-input input:not(:valid),
.e-float-input input:valid,
.e-input-group input:not(:valid),
.e-input-group input:valid,
.e-input-group.e-control-wrapper input:not(:valid),
.e-input-group.e-control-wrapper input:valid,
.e-float-input.e-control-wrapper textarea:not(:valid),
.e-float-input.e-control-wrapper textarea:valid,
.e-float-input textarea:not(:valid),
.e-float-input textarea:valid,
.e-input-group.e-control-wrapper textarea:not(:valid),
.e-input-group.e-control-wrapper textarea:valid,
.e-input-group textarea:not(:valid),
.e-input-group textarea:valid {
  font-size: 16px;
  height: 45px;
  padding: 10px 12px;
}
```

**In App.tsx:**

```tsx
import './App.css';

export default function App() {
  return (
    <TextBoxComponent
      placeholder="Custom sized input"
      floatLabelType="Auto"
    />
  );
}
```

### Custom Border and Colors

```css
.e-input:focus,
.e-float-input input:focus,
.e-input-group input:focus {
  border-color: #2196F3;
  box-shadow: 0 0 5px rgba(33, 150, 243, 0.3);
}

.e-input {
  border: 2px solid #E0E0E0;
  border-radius: 4px;
}
```

### Custom Background Color

```css
.e-float-input.e-control-wrapper,
.e-input-group {
  background-color: #F5F5F5;
  border-radius: 8px;
}

.e-float-input.e-control-wrapper input,
.e-input-group input {
  background-color: #F5F5F5;
}

.e-input:focus {
  background-color: #FFFFFF;
}
```

### Custom Padding and Spacing

```css
.e-input,
.e-float-input input {
  padding: 12px 16px;
}

/* Increase spacing for better touch targets */
.e-bigger .e-input,
.e-bigger .e-float-input input {
  padding: 14px 18px;
}
```

## Floating Label Styling

Customize the appearance of floating labels with CSS:

### Floating Label Color

```css
/* Floating label color and font size */
.e-float-input.e-control-wrapper:not(.e-error) input:valid ~ label.e-float-text,
.e-float-input.e-control-wrapper:not(.e-error) input ~ label.e-label-top.e-float-text {
  color: #2196F3;
  font-size: 14px;
  font-weight: 500;
}
```

### Custom Floating Label Animation

```css
/* Smooth floating label transition */
.e-float-text {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Floating label in focused state */
.e-input-focus ~ .e-float-text,
.e-input:valid ~ .e-float-text {
  font-size: 12px;
  color: #1976D2;
  transform: translateY(-1.5em);
}
```

### Floating Label Color by State

```css
/* Success state - green floating label */
.e-success input:valid ~ label.e-float-text {
  color: #4CAF50;
}

/* Error state - red floating label */
.e-error input ~ label.e-float-text {
  color: #F44336;
}

/* Warning state - orange floating label */
.e-warning input ~ label.e-float-text {
  color: #FF9800;
}
```

### Complete Floating Label Example

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import './App.css';

export default function StyledFloatingLabel() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: ''
  });

  return (
    <div style={{ maxWidth: '400px', margin: '40px auto' }}>
      <h2>User Registration</h2>

      <div style={{ marginBottom: '20px' }}>
        <TextBoxComponent
          placeholder="Username"
          floatLabelType="Auto"
          value={formData.username}
          change={(e) => setFormData({ ...formData, username: e.value })}
        />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <TextBoxComponent
          placeholder="Email"
          floatLabelType="Auto"
          type="email"
          value={formData.email}
          change={(e) => setFormData({ ...formData, email: e.value })}
        />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <TextBoxComponent
          placeholder="Password"
          floatLabelType="Auto"
          type="password"
          value={formData.password}
          change={(e) => setFormData({ ...formData, password: e.value })}
        />
      </div>

      <button style={{ width: '100%', padding: '12px' }}>Register</button>
    </div>
  );
}
```

**CSS in App.css:**

```css
/* Custom floating label styling */
.e-float-input.e-control-wrapper:not(.e-error) input:valid ~ label.e-float-text,
.e-float-input.e-control-wrapper:not(.e-error) input ~ label.e-label-top.e-float-text {
  color: #2196F3;
  font-size: 14px;
  font-weight: 600;
}

/* Custom input styling */
.e-input {
  border: 2px solid #E0E0E0;
  border-radius: 6px;
  padding: 12px 14px;
  font-size: 15px;
  transition: all 0.3s ease;
}

.e-input:focus {
  border-color: #2196F3;
  box-shadow: 0 0 8px rgba(33, 150, 243, 0.2);
  background-color: #F8FBFF;
}

button {
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #1976D2;
}
```

## TextBox Wrapper Styling

Style the container element that wraps the TextBox:

### Add Margin and Spacing

```css
.e-float-input,
.e-input-group {
  margin-bottom: 20px;
}
```

### Create Cards/Containers

```css
.textbox-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 24px;
  background-color: #FFFFFF;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.textbox-container .e-float-input {
  margin-bottom: 0;
}
```

**Usage:**

```tsx
<div className="textbox-container">
  <TextBoxComponent placeholder="Name" floatLabelType="Auto" />
  <TextBoxComponent placeholder="Email" floatLabelType="Auto" />
  <TextBoxComponent placeholder="Phone" floatLabelType="Auto" />
</div>
```

### Responsive Layout

```css
@media (max-width: 768px) {
  .e-input {
    font-size: 16px; /* Prevents mobile zoom */
    padding: 14px 16px;
  }

  .e-bigger {
    padding: 16px 18px;
  }
}
```

## Theme Variations

Syncfusion provides multiple built-in themes. Switch themes by changing CSS imports in `App.css`:

### Available Themes

#### Material Design (Default)

```css
@import "../node_modules/@syncfusion/ej2-base/styles/material.css";
@import "../node_modules/@syncfusion/ej2-icons/styles/material.css";
@import "../node_modules/@syncfusion/ej2-react-inputs/styles/material.css";
```

#### Bootstrap 5

```css
@import "../node_modules/@syncfusion/ej2-base/styles/bootstrap5.css";
@import "../node_modules/@syncfusion/ej2-icons/styles/bootstrap5.css";
@import "../node_modules/@syncfusion/ej2-react-inputs/styles/bootstrap5.css";
```

#### Fluent (Microsoft Design)

```css
@import "../node_modules/@syncfusion/ej2-base/styles/fluent.css";
@import "../node_modules/@syncfusion/ej2-icons/styles/fluent.css";
@import "../node_modules/@syncfusion/ej2-react-inputs/styles/fluent.css";
```

#### High Contrast (Accessibility)

```css
@import "../node_modules/@syncfusion/ej2-base/styles/highcontrast.css";
@import "../node_modules/@syncfusion/ej2-icons/styles/highcontrast.css";
@import "../node_modules/@syncfusion/ej2-react-inputs/styles/highcontrast.css";
```

#### Tailwind 3 (Recommended)

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-icons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-inputs/styles/tailwind3.css";
```

### Theme Switching at Runtime

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import './App.css';

export default function ThemeSwitcher() {
  const [theme, setTheme] = useState('material');

  const switchTheme = (selectedTheme: string) => {
    setTheme(selectedTheme);
    document.documentElement.setAttribute('data-theme', selectedTheme);
  };

  return (
    <div style={{ maxWidth: '400px', margin: '20px auto' }}>
      <div style={{ marginBottom: '20px' }}>
        <button onClick={() => switchTheme('material')}>Material</button>
        <button onClick={() => switchTheme('bootstrap5')}>Bootstrap 5</button>
        <button onClick={() => switchTheme('fluent')}>Fluent</button>
      </div>

      <TextBoxComponent
        placeholder="Try different themes"
        floatLabelType="Auto"
      />
    </div>
  );
}
```

## Complete Styling Example

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import './App.css';

export default function StyledFormApp() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });

  const handleChange = (field: string, value: string) => {
    setFormData({ ...formData, [field]: value });
  };

  return (
    <div style={{ maxWidth: '500px', margin: '40px auto', padding: '20px' }}>
      <h2>Contact Form</h2>

      <div className="form-group">
        <TextBoxComponent
          placeholder="Full Name"
          floatLabelType="Auto"
          showClearButton={true}
          value={formData.name}
          change={(e) => handleChange('name', e.value)}
        />
      </div>

      <div className="form-group">
        <TextBoxComponent
          placeholder="Email Address"
          floatLabelType="Auto"
          showClearButton={true}
          type="email"
          value={formData.email}
          change={(e) => handleChange('email', e.value)}
        />
      </div>

      <div className="form-group">
        <TextBoxComponent
          placeholder="Message"
          floatLabelType="Auto"
          multiline={true}
          value={formData.message}
          change={(e) => handleChange('message', e.value)}
        />
      </div>

      <button className="submit-btn">Send Message</button>
    </div>
  );
}
```

**App.css:**

```css
.form-group {
  margin-bottom: 20px;
}

.e-input,
.e-float-input input {
  border: 2px solid #E0E0E0;
  border-radius: 6px;
  padding: 12px 14px;
  font-size: 15px;
  transition: all 0.3s ease;
}

.e-input:focus,
.e-float-input input:focus {
  border-color: #2196F3;
  box-shadow: 0 0 8px rgba(33, 150, 243, 0.2);
}

.e-float-input.e-control-wrapper:not(.e-error) input ~ label.e-float-text {
  color: #2196F3;
  font-weight: 600;
}

.submit-btn {
  width: 100%;
  padding: 12px 20px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-btn:hover {
  background-color: #1976D2;
}
```

## See Also

- [Getting Started](./getting-started.md) - CSS imports and theme setup
- [Features and Groups](./features-and-groups.md) - Floating labels and icons
- [Validation and States](./validation-and-states.md) - Error/warning/success styling
