# Style, Appearance & Customization

## Table of Contents
- [Float Label Types](#float-label-types)
- [Custom CSS Class](#custom-css-class)
- [CSS Overrides](#css-overrides)
- [Cursor Position on Focus](#cursor-position-on-focus)
- [Numeric Keypad on Mobile](#numeric-keypad-on-mobile)
- [Additional Properties](#additional-properties)

## Float Label Types

Control how the placeholder/label floats with `floatLabelType`:

| Value | Behavior |
|-------|----------|
| `"Never"` (default) | Placeholder does not float; stays inside the input |
| `"Always"` | Label always floats above the input |
| `"Auto"` | Label floats above when focused or when a value is entered |

```tsx
<MaskedTextBoxComponent
  mask="000-000-0000"
  placeholder="Phone Number"
  floatLabelType="Auto"
/>
```

## Custom CSS Class

Use `cssClass` to apply a custom CSS class to the MaskedTextBox root element for targeted styling.

```tsx
import { MaskedTextBoxComponent, MaskFocusEventArgs } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

export default class App extends React.Component {
  public onfocus(args: MaskFocusEventArgs) {
    // Set cursor to start on focus
    args.selectionEnd = args.selectionStart;
  }

  public render() {
    return (
      <MaskedTextBoxComponent
        id="mask1"
        name="mask_value"
        placeholder="Enter user ID"
        floatLabelType="Always"
        mask="00000"
        cssClass="e-style"
        value="42648"
        focus={this.onfocus}
      />
    );
  }
}
```

## CSS Overrides

### Wrapper Element (height, font size, border)

```css
.e-input-group input.e-input,
.e-input-group.e-control-wrapper input.e-input {
  font-size: 20px;
  border-color: red;
  height: 40px;
  border: 2px solid;
}
```

### Hover State

```css
.e-input-group input.e-input,
.e-input-group input.e-input:hover:not(.e-success):not(.e-warning):not(.e-error):not([disabled]):not(:focus),
.e-input-group.e-control-wrapper input.e-input,
.e-input-group.e-control-wrapper input.e-input:hover:not(.e-success):not(.e-warning):not(.e-error):not([disabled]):not(:focus) {
  border: 3px solid red;
}
```

## Cursor Position on Focus

By default, MaskedTextBox selects the entire mask on focus. Use the `focus` event with `MaskFocusEventArgs` to override cursor placement.

### Available properties in `MaskFocusEventArgs`

| Property | Type | Description |
|----------|------|-------------|
| `selectionStart` | number | Starting position of the cursor selection |
| `selectionEnd` | number | Ending position of the cursor selection |
| `maskedValue` | string | The full masked string including literals |

### Cursor at Start

```tsx
import { MaskedTextBoxComponent, MaskFocusEventArgs } from '@syncfusion/ej2-react-inputs';

export default class App extends React.Component {
  public onfocus(args: MaskFocusEventArgs) {
    args.selectionEnd = args.selectionStart = 0;
  }

  public render() {
    return (
      <MaskedTextBoxComponent
        mask="00000-00000"
        value="83929-4342"
        placeholder="Cursor at start"
        floatLabelType="Always"
        focus={this.onfocus}
      />
    );
  }
}
```

### Cursor at End

```tsx
public onfocusEnd(args: MaskFocusEventArgs) {
  args.selectionStart = args.selectionEnd = args.maskedValue.length;
}
```

### Cursor at Specific Position

```tsx
public onfocusPosition(args: MaskFocusEventArgs) {
  args.selectionStart = 3;
  args.selectionEnd = 3;
}
```

### Multiple Inputs with Different Cursor Behaviors (Functional)

```tsx
import * as React from 'react';
import { MaskedTextBoxComponent, MaskFocusEventArgs } from '@syncfusion/ej2-react-inputs';

function App() {
  const focusStart = (args: MaskFocusEventArgs) => {
    args.selectionEnd = args.selectionStart = 0;
  };
  const focusEnd = (args: MaskFocusEventArgs) => {
    args.selectionStart = args.selectionEnd = args.maskedValue.length;
  };
  const focusAt3 = (args: MaskFocusEventArgs) => {
    args.selectionStart = 3;
    args.selectionEnd = 3;
  };

  return (
    <div>
      <MaskedTextBoxComponent mask="00000-00000" value="93828-32132" placeholder="Default cursor" floatLabelType="Always" />
      <MaskedTextBoxComponent mask="00000-00000" value="83929-4342" placeholder="Cursor at start" floatLabelType="Always" focus={focusStart} />
      <MaskedTextBoxComponent mask="00000-00000" value="83929-3213" placeholder="Cursor at end" floatLabelType="Always" focus={focusEnd} />
      <MaskedTextBoxComponent mask="+1 000-000-0000" value="234-432-432" placeholder="Cursor at position 3" floatLabelType="Always" focus={focusAt3} />
    </div>
  );
}
```

> **Note:** When all mask positions are filled, `selectionStart` and `selectionEnd` default to `0` (HTML5 input behavior). This is expected.

## Numeric Keypad on Mobile

By default, MaskedTextBox shows an alphanumeric keyboard on mobile. To show only the numeric keypad, set the HTML `type` attribute to `tel` via `htmlAttributes`:

```tsx
import * as React from 'react';
import { MaskedTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default class App extends React.Component {
  public render() {
    return (
      <MaskedTextBoxComponent
        name="mask_value"
        mask="999-99999"
        value="342-45432"
        htmlAttributes={{ type: 'tel' }}
      />
    );
  }
}
```

> Setting `htmlAttributes={{ type: 'tel' }}` triggers a numeric keypad on iOS and Android while preserving mask behavior.

## Additional Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `enabled` | boolean | `true` | Enables or disables the component |
| `readonly` | boolean | `false` | Makes the input read-only |
| `showClearButton` | boolean | `false` | Shows a clear (×) icon inside the input |
| `enableRtl` | boolean | `false` | Renders the component right-to-left |
| `width` | number \| string | `null` | Sets the width of the component |
| `enablePersistence` | boolean | `false` | Persists the `value` state across page reloads |
