# Getting Started with React TextBox Component

## Table of Contents

- [Project Setup](#project-setup)
- [Installing TextBox Package](#installing-textbox-package)
- [Adding CSS References](#adding-css-references)
- [Creating Your First TextBox](#creating-your-first-textbox)
- [Adding Icons to TextBox](#adding-icons-to-textbox)
- [Running the Application](#running-the-application)
- [Floating Labels](#floating-labels)

## Project Setup

### Using Vite (Recommended)

Vite provides a faster development environment with smaller bundle sizes compared to create-react-app. Create a new React application:

```bash
npm create vite@latest my-textbox-app
```

When prompted, select:
- **Framework:** React
- **Variant:** JavaScript or TypeScript (as needed)

```bash
cd my-textbox-app
npm run dev
```

### Using Create React App

If you prefer create-react-app:

```bash
npx create-react-app my-textbox-app
cd my-textbox-app
npm start
```

## Installing TextBox Package

Install the Syncfusion React inputs package (which includes TextBox):

```bash
npm install @syncfusion/ej2-react-inputs --save
```

The `--save` flag adds the package to your `package.json` dependencies.

> **Note:** Make sure you have Node.js 14+ installed. Check with `node --version`.

## Adding CSS References

### Step 1: Import CSS in App.css

Add the following CSS imports to your `src/App.css` file:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-icons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-inputs/styles/tailwind3.css";
```

These imports provide:
- **ej2-base:** Core Syncfusion styles
- **ej2-icons:** Icon library used for adornments
- **ej2-react-inputs:** TextBox-specific styling

### Alternative Themes

Syncfusion provides multiple theme options. Replace `tailwind3.css` with one of:

- `bootstrap5.css` - Bootstrap 5 theme
- `material.css` - Material Design theme
- `fluent.css` - Microsoft Fluent theme
- `highcontrast.css` - High contrast for accessibility

```css
/* Example: Using Material theme */
@import "../node_modules/@syncfusion/ej2-base/styles/material.css";
@import "../node_modules/@syncfusion/ej2-icons/styles/material.css";
@import "../node_modules/@syncfusion/ej2-react-inputs/styles/material.css";
```

### Step 2: Import CSS in App.tsx

Ensure `App.css` is imported in your main `App.tsx`:

```tsx
import './App.css';
```

## Creating Your First TextBox

### Basic TextBox (Class Component)

```tsx
import * as React from "react";
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import './App.css';

export default class App extends React.Component<{}, {}> {
  public render() {
    return (
      <TextBoxComponent 
        id="textbox-default"
        placeholder="Enter Name"
      />
    );
  }
}
```

### Basic TextBox (Functional Component)

```tsx
import React from "react";
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import './App.css';

export default function App() {
  return (
    <TextBoxComponent 
      id="textbox-default"
      placeholder="Enter Name"
    />
  );
}
```

### Output

The TextBox renders as a styled input field with a placeholder:

```
┌─────────────────────────┐
│ Enter Name              │
└─────────────────────────┘
```

## Adding Icons to TextBox

### Adding a Single Icon

Add an icon after the input using the `addIcon()` method and the `created` event:

**Functional Component:**

```tsx
import React, { useRef } from "react";
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import './App.css';

export default function App() {
  const textboxRef = useRef<TextBoxComponent>(null);

  const handleCreate = () => {
    if (textboxRef.current) {
      // addIcon(position, iconClass)
      // position: 'append' (right) or 'prepend' (left)
      textboxRef.current.addIcon('append', 'e-icons e-input-popup-date');
    }
  };

  return (
    <TextBoxComponent
      id="textbox-icon"
      placeholder="Enter Date"
      ref={textboxRef}
      created={handleCreate}
    />
  );
}
```

### Available Icon Classes

Syncfusion provides icon classes with the format `e-icons e-{icon-name}`:

- `e-input-popup-date` - Calendar icon
- `e-input-down` - Dropdown arrow
- `e-user` - User/profile icon
- `e-people` - Group/people icon
- `e-trash` - Delete/trash icon
- `e-eye` - Eye icon (visibility)
- `e-eye-slash` - Eye with slash icon

### Adding Multiple Icons

Add icons on both sides:

```tsx
const handleCreate = () => {
  if (textboxRef.current) {
    // Icon on the left (prepend)
    textboxRef.current.addIcon('prepend', 'e-icons e-user');
    // Icon on the right (append)
    textboxRef.current.addIcon('append', 'e-icons e-input-popup-date');
  }
};
```

### Output

```
┌──────────────────────────────┐
│ 👤 Enter Date            📅  │
└──────────────────────────────┘
```

### Custom Icon Styling

Add CSS to style icons:

```css
.e-input-group .e-icons.e-input-popup-date {
  font-size: 16px;
  color: #007bff;
}
```

## Running the Application

### Vite Development Server

```bash
npm run dev
```

Output:
```
  Local:        http://localhost:5173/
  press h to show help
```

Open `http://localhost:5173/` in your browser to see the TextBox.

### Create React App Development Server

```bash
npm start
```

The browser opens automatically, showing your TextBox component.

## Floating Labels

The floating label feature automatically animates the placeholder text above the input when focused or filled.

### Floating Label Types

#### Auto (Recommended)

Label floats when input is focused or has a value:

```tsx
<TextBoxComponent 
  placeholder="First Name"
  floatLabelType="Auto"
/>
```

Behavior:
- Empty and unfocused: Placeholder shows inside input
- Focused or has value: Placeholder moves above input as label

#### Always

Label always floats above the input:

```tsx
<TextBoxComponent 
  placeholder="Last Name"
  floatLabelType="Always"
/>
```

Behavior: Label is always visible above, even when empty and unfocused

#### Never (Default)

Placeholder stays inside the input (no floating label):

```tsx
<TextBoxComponent 
  placeholder="Email"
  floatLabelType="Never"
/>
```

### Complete Floating Label Example

```tsx
import React from "react";
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import './App.css';

export default function App() {
  return (
    <div>
      <h3>Floating Label Examples</h3>
      
      <div>
        <label>Auto - Float on focus/fill</label>
        <TextBoxComponent 
          placeholder="First Name"
          floatLabelType="Auto"
        />
      </div>

      <div>
        <label>Always - Label always visible</label>
        <TextBoxComponent 
          placeholder="Last Name"
          floatLabelType="Always"
        />
      </div>

      <div>
        <label>Never - Placeholder inside input</label>
        <TextBoxComponent 
          placeholder="Email"
          floatLabelType="Never"
        />
      </div>
    </div>
  );
}
```

## Next Steps

- **Add validation:** See [Validation and States](./validation-and-states.md) for error/warning/success states
- **Customize styling:** See [Styling and Sizing](./styling-and-sizing.md) for size and appearance options
- **Add clear button:** See [Features and Groups](./features-and-groups.md) for built-in functionality
- **Use multiline:** See [Multiline TextBox](./multiline-textbox.md) for textarea mode
- **Advanced features:** See [Advanced Features](./advanced-features.md) for adornments and hooks

## Troubleshooting

**Issue:** Styles not applied (no borders or spacing)

**Solution:** Ensure CSS imports are in `App.css`:
```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-icons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-inputs/styles/tailwind3.css";
```

**Issue:** Icons not showing

**Solution:** Icons require `ej2-icons` CSS import. Add to `App.css`:
```css
@import "../node_modules/@syncfusion/ej2-icons/styles/tailwind3.css";
```

**Issue:** TextBox not rendering

**Solution:** 
1. Verify package is installed: `npm list @syncfusion/ej2-react-inputs`
2. Check import path: `from '@syncfusion/ej2-react-inputs'`
3. Verify `App.css` imports are correct
