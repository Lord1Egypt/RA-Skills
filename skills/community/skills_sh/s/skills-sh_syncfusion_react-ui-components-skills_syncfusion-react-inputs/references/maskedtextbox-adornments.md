# Adornments in MaskedTextBox

Adornments let you attach custom content — icons, buttons, separators, or labels — before or after the masked input using `prependTemplate` and `appendTemplate`. They enhance context and usability without affecting mask validation or float label behavior.

## Common Use Cases

- **Entry guidance**: Add a user/phone icon to indicate expected input type
- **Quick actions**: Include a send button, clear button, or copy icon
- **Context labels**: Add static prefixes like country code `+1` or suffixes like `MHz`
- **Visual feedback**: Show status indicators adjacent to the input

## Properties

| Property | Description |
|----------|-------------|
| `prependTemplate` | Renders content **before** the input (left side) |
| `appendTemplate` | Renders content **after** the input (right side) |

Both accept a `string`, `function`, or `JSX.Element`. Templates update dynamically on property change.

## Functional Component Example

```tsx
import * as React from 'react';
import { MaskedTextBoxComponent } from '@syncfusion/ej2-react-inputs';

function App() {
  const prependTemplate = (): React.ReactNode => (
    <>
      <span className="e-icons e-user"></span>
      <span className="e-input-separator"></span>
    </>
  );

  const appendTemplate = (): React.ReactNode => (
    <>
      <span className="e-input-separator"></span>
      <span className="e-icons e-send"></span>
    </>
  );

  return (
    <MaskedTextBoxComponent
      mask="000-000-0000"
      promptChar="#"
      cssClass="e-prepend-mask"
      placeholder="Enter phone number"
      floatLabelType="Auto"
      prependTemplate={prependTemplate}
      appendTemplate={appendTemplate}
    />
  );
}

export default App;
```

## Class Component Example

```tsx
import * as React from 'react';
import { MaskedTextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default class App extends React.Component {
  private prependTemplate = (): React.ReactNode => (
    <>
      <span className="e-icons e-user"></span>
      <span className="e-input-separator"></span>
    </>
  );

  private appendTemplate = (): React.ReactNode => (
    <>
      <span className="e-input-separator"></span>
      <span className="e-icons e-send"></span>
    </>
  );

  render(): React.ReactNode {
    return (
      <MaskedTextBoxComponent
        mask="000-000-0000"
        promptChar="#"
        cssClass="e-prepend-mask"
        placeholder="Enter phone number"
        floatLabelType="Auto"
        prependTemplate={this.prependTemplate}
        appendTemplate={this.appendTemplate}
      />
    );
  }
}
```

## Notes

- Use `e-input-separator` span between the icon and the input for proper visual separation
- Adornment content does not interfere with mask validation
- `cssClass="e-prepend-mask"` helps align the input wrapper when using prepend icons
- Use Syncfusion built-in icon classes (`e-icons e-user`, `e-icons e-send`, etc.) or any custom icon library
