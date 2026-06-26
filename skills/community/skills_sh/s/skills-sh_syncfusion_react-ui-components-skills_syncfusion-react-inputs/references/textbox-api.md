# Syncfusion React TextBox API Reference

Complete API reference for the `TextBoxComponent` from `@syncfusion/ej2-react-inputs`.

**Import:**

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
```

---

## Properties

### appendTemplate

`string | function | JSX.Element`

Specifies the HTML template for custom elements to append (right side) to the TextBox input. Supports icons, buttons, or any valid HTML. Updates dynamically on property change. The template function must return `JSX.Element`.

**Default:** `null`

**Function Signature:** `() => JSX.Element`

```tsx
function appendTemplate(): JSX.Element {
  return (
    <>
      <span className="e-input-separator"></span>
      <span className="e-icons e-eye"></span>
    </>
  );
}

<TextBoxComponent appendTemplate={appendTemplate} />
```

---

### autocomplete

`string`

Specifies whether the browser is allowed to automatically enter or select a value for the textbox.

**Possible values:**
- `'on'` – Autocomplete is enabled (default)
- `'off'` – Autocomplete is disabled

**Default:** `'on'`

```tsx
<TextBoxComponent autocomplete="off" placeholder="Enter Name" />
```

---

### cssClass

`string`

Specifies the CSS class value appended to the wrapper of the TextBox. Use this to apply predefined size classes (`e-small`, `e-bigger`), validation states (`e-error`, `e-warning`, `e-success`), or custom appearance classes like `e-corner`.

**Default:** `''`

```tsx
<TextBoxComponent cssClass="e-corner" placeholder="Enter Date" />
<TextBoxComponent cssClass="e-small" placeholder="Small TextBox" />
<TextBoxComponent cssClass="e-bigger" placeholder="Large TextBox" />
<TextBoxComponent cssClass="e-error" placeholder="Error State" />
<TextBoxComponent cssClass="e-warning" placeholder="Warning State" />
<TextBoxComponent cssClass="e-success" placeholder="Success State" />
```

---

### enablePersistence

`boolean`

Enable or disable persisting TextBox state between page reloads. If enabled, the `value` state will be persisted.

**Default:** `false`

```tsx
<TextBoxComponent enablePersistence={true} placeholder="Persisted Input" />
```

---

### enableRtl

`boolean`

Enable or disable rendering the component in right-to-left direction.

**Default:** `false`

```tsx
<TextBoxComponent enableRtl={true} placeholder="RTL TextBox" />
```

---

### enabled

`boolean`

Specifies a Boolean value that indicates whether the TextBox allows user interaction. Set to `false` to disable the TextBox.

**Default:** `true`

```tsx
<TextBoxComponent enabled={false} placeholder="Disabled TextBox" />
```

---

### floatLabelType

`FloatLabelType`

Specifies the floating label behavior of the TextBox — how the placeholder text floats above the TextBox.

**Possible values:**
- `'Never'` – The placeholder text never floats (default)
- `'Always'` – The placeholder text always floats above the TextBox
- `'Auto'` – The placeholder text floats when the TextBox is focused or has a value

**Default:** `'Never'`

```tsx
<TextBoxComponent placeholder="First Name" floatLabelType="Auto" />
<TextBoxComponent placeholder="Last Name" floatLabelType="Always" />
<TextBoxComponent placeholder="Email" floatLabelType="Never" />
```

---

### htmlAttributes

`{ [key: string]: string }`

You can add additional HTML attributes such as `disabled`, `value`, `name`, `type`, `maxlength`, etc. to the element. If both property and equivalent HTML attribute are configured, the component considers the property value.

**Default:** `{}`

```tsx
import * as React from 'react';
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

class App extends React.Component {
  public htmlAttributes = { name: "username", type: "password", maxlength: "8" };
  public render() {
    return (<TextBoxComponent htmlAttributes={this.htmlAttributes} />);
  }
}

export default App;
```

---

### locale

`string`

Overrides the global culture and localization value for this component.

**Default:** `''` (uses global culture `'en-US'`)

```tsx
<TextBoxComponent locale="fr-FR" placeholder="Enter Name" />
```

---

### multiline

`boolean`

Specifies a boolean value that enables or disables multiline mode on the TextBox. The TextBox changes from single-line to multiline (textarea) when this is enabled.

**Default:** `false`

```tsx
<TextBoxComponent multiline={true} placeholder="Enter your address" floatLabelType="Auto" />
```

---

### placeholder

`string`

Specifies the text shown as a hint/placeholder until the user focuses or enters a value. The behavior depends on the `floatLabelType` property.

**Default:** `null`

```tsx
<TextBoxComponent placeholder="Enter your name" floatLabelType="Auto" />
```

---

### prependTemplate

`string | function | JSX.Element`

Specifies the HTML template for custom elements to prepend (left side) to the TextBox input. Supports icons, buttons, or any valid HTML. Updates dynamically on property change. The template function must return `JSX.Element`.

**Default:** `null`

**Function Signature:** `() => JSX.Element`

```tsx
function prependTemplate(): JSX.Element {
  return (
    <>
      <span className="e-icons e-user"></span>
      <span className="e-input-separator"></span>
    </>
  );
}

<TextBoxComponent prependTemplate={prependTemplate} placeholder="Enter Name" />
```

---

### readonly

`boolean`

Specifies the boolean value whether the TextBox allows users to change the text. When `true`, the input can be read and selected but not edited.

**Default:** `false`

```tsx
<TextBoxComponent readonly={true} value="Read only text" placeholder="Read-only" floatLabelType="Auto" />
```

---

### showClearButton

`boolean`

Specifies a Boolean value that indicates whether the clear button is displayed in the TextBox. The clear button appears only when the input has a value.

**Default:** `false`

```tsx
<TextBoxComponent showClearButton={true} placeholder="Enter text" floatLabelType="Auto" />
```

---

### type

`string`

Specifies the behavior of the TextBox such as `text`, `password`, `email`, `number`, `tel`, etc.

**Default:** `'text'`

```tsx
<TextBoxComponent type="password" placeholder="Enter password" floatLabelType="Auto" />
<TextBoxComponent type="email" placeholder="Enter email" floatLabelType="Auto" />
<TextBoxComponent type="number" placeholder="Enter number" floatLabelType="Auto" />
```

---

### value

`string`

Sets the content of the TextBox.

**Default:** `null`

```tsx
<TextBoxComponent value="Initial value" placeholder="Enter Name" floatLabelType="Auto" />
```

---

### width

`number | string`

Specifies the width of the TextBox component.

**Default:** `null`

```tsx
<TextBoxComponent width="300px" placeholder="Enter Name" />
<TextBoxComponent width={400} placeholder="Enter Name" />
```

---

## Methods

### addAttributes

Adding multiple attributes as key-value pairs to the TextBox element.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `attributes` | `{ [key: string]: string }` | Specifies the attributes to add to the TextBox element. |

**Returns:** `void`

```tsx
import { useRef } from 'react';
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function App() {
  const textboxRef = useRef<TextBoxComponent>(null);

  const handleCreate = () => {
    if (textboxRef.current) {
      textboxRef.current.addAttributes({ maxlength: '150', rows: '3' });
    }
  };

  return (
    <TextBoxComponent
      multiline={true}
      placeholder="Enter text"
      floatLabelType="Auto"
      ref={textboxRef}
      created={handleCreate}
    />
  );
}
```

---

### addIcon

Adding icons to the TextBox component. Creates a `<span>` element with the given icon class(es) placed at the specified position.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `position` | `string` | Icon placement — `'append'` (right) or `'prepend'` (left). |
| `icons` | `string \| string[]` | Icon CSS class(es) to apply to the created span element. |

**Returns:** `void`

```tsx
import { useRef } from 'react';
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function App() {
  const textboxRef = useRef<TextBoxComponent>(null);

  const handleCreate = () => {
    if (textboxRef.current) {
      textboxRef.current.addIcon('prepend', 'e-icons e-user');
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

---

### destroy

Removes the component from the DOM and detaches all its related event handlers. Also maintains the initial TextBox element from the DOM.

**Returns:** `void`

```tsx
import { useRef } from 'react';
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function App() {
  const textboxRef = useRef<TextBoxComponent>(null);

  const handleDestroy = () => {
    textboxRef.current?.destroy();
  };

  return (
    <>
      <TextBoxComponent ref={textboxRef} placeholder="Enter text" />
      <button onClick={handleDestroy}>Destroy</button>
    </>
  );
}
```

---

### focusIn

Sets the focus to the TextBox widget for interaction.

**Returns:** `void`

```tsx
import { useRef, useEffect } from 'react';
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function App() {
  const textboxRef = useRef<TextBoxComponent>(null);

  useEffect(() => {
    textboxRef.current?.focusIn();
  }, []);

  return (
    <TextBoxComponent ref={textboxRef} placeholder="Auto-focused" floatLabelType="Auto" />
  );
}
```

---

### focusOut

Removes the focus from the TextBox widget if it is in a focused state.

**Returns:** `void`

```tsx
import { useRef } from 'react';
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function App() {
  const textboxRef = useRef<TextBoxComponent>(null);

  const handleBlur = () => {
    textboxRef.current?.focusOut();
  };

  return (
    <>
      <TextBoxComponent ref={textboxRef} placeholder="Enter text" />
      <button onClick={handleBlur}>Remove Focus</button>
    </>
  );
}
```

---

### getPersistData

Gets the properties to be maintained in the persisted state.

**Returns:** `string`

```tsx
import { useRef } from 'react';
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function App() {
  const textboxRef = useRef<TextBoxComponent>(null);

  const logPersistData = () => {
    const data = textboxRef.current?.getPersistData();
    console.log('Persist data:', data);
  };

  return (
    <>
      <TextBoxComponent ref={textboxRef} placeholder="Enter text" enablePersistence={true} />
      <button onClick={logPersistData}>Get Persist Data</button>
    </>
  );
}
```

---

### removeAttributes

Removing multiple attributes by name from the TextBox element.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `attributes` | `string[]` | Specifies the attribute names to remove from the TextBox element. |

**Returns:** `void`

```tsx
import { useRef } from 'react';
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function App() {
  const textboxRef = useRef<TextBoxComponent>(null);

  const handleCreate = () => {
    if (textboxRef.current) {
      textboxRef.current.addAttributes({ maxlength: '10', readonly: 'true' });
    }
  };

  const handleRemove = () => {
    if (textboxRef.current) {
      textboxRef.current.removeAttributes(['maxlength', 'readonly']);
    }
  };

  return (
    <>
      <TextBoxComponent
        ref={textboxRef}
        placeholder="Enter text"
        floatLabelType="Auto"
        created={handleCreate}
      />
      <button onClick={handleRemove}>Remove Attributes</button>
    </>
  );
}
```

---

## Events

### blur

`EmitType<FocusOutEventArgs>`

Triggers when the TextBox loses focus (focus-out).

**Event Arguments (`FocusOutEventArgs`):**

| Property | Type | Description |
|----------|------|-------------|
| `event` | `MouseEvent \| TouchEvent` | Specifies the original event arguments. |
| `value` | `string` | Returns the current value of the TextBox. |

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function App() {
  const handleBlur = (args: any) => {
    console.log('TextBox blurred, value:', args.value);
  };

  return (
    <TextBoxComponent
      placeholder="Enter text"
      floatLabelType="Auto"
      blur={handleBlur}
    />
  );
}
```

---

### change

`EmitType<ChangedEventArgs>`

Triggers when the content of the TextBox has changed and gets focus-out.

**Event Arguments (`ChangedEventArgs`):**

| Property | Type | Description |
|----------|------|-------------|
| `event` | `Event` | Specifies the original event arguments. |
| `value` | `string` | Returns the current value of the TextBox. |
| `previousValue` | `string` | Returns the previous value of the TextBox. |
| `isInteraction` | `boolean` | Returns `true` if the change was triggered by a user interaction. |
| `isInteracted` | `boolean` | Returns `true` if the TextBox component was interacted by the user. |
| `container` | `HTMLElement` | Specifies the container element. |

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function App() {
  const handleChange = (args: any) => {
    console.log('New value:', args.value);
    console.log('Previous value:', args.previousValue);
  };

  return (
    <TextBoxComponent
      placeholder="Enter text"
      floatLabelType="Auto"
      change={handleChange}
    />
  );
}
```

---

### created

`EmitType<Object>`

Triggers when the TextBox component is created.

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useRef } from 'react';

export default function App() {
  const textboxRef = useRef<TextBoxComponent>(null);

  const handleCreated = () => {
    console.log('TextBox created');
    if (textboxRef.current) {
      textboxRef.current.addIcon('append', 'e-icons e-input-popup-date');
    }
  };

  return (
    <TextBoxComponent
      ref={textboxRef}
      placeholder="Enter Date"
      floatLabelType="Auto"
      created={handleCreated}
    />
  );
}
```

---

### destroyed

`EmitType<Object>`

Triggers when the TextBox component is destroyed.

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function App() {
  const handleDestroyed = () => {
    console.log('TextBox destroyed');
  };

  return (
    <TextBoxComponent
      placeholder="Enter text"
      destroyed={handleDestroyed}
    />
  );
}
```

---

### focus

`EmitType<FocusInEventArgs>`

Triggers when the TextBox gets focus.

**Event Arguments (`FocusInEventArgs`):**

| Property | Type | Description |
|----------|------|-------------|
| `event` | `MouseEvent \| TouchEvent` | Specifies the original event arguments. |
| `value` | `string` | Returns the current value of the TextBox. |

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';

export default function App() {
  const handleFocus = (args: any) => {
    console.log('TextBox focused, value:', args.value);
  };

  return (
    <TextBoxComponent
      placeholder="Enter text"
      floatLabelType="Auto"
      focus={handleFocus}
    />
  );
}
```

---

### input

`EmitType<InputEventArgs>`

Triggers each time when the value of the TextBox has changed (on every keystroke).

**Event Arguments (`InputEventArgs`):**

| Property | Type | Description |
|----------|------|-------------|
| `event` | `Event` | Specifies the original event arguments. |
| `value` | `string` | Returns the current value of the TextBox. |
| `previousValue` | `string` | Returns the previous value of the TextBox. |
| `isInteraction` | `boolean` | Returns `true` if the change was triggered by a user interaction. |
| `isInteracted` | `boolean` | Returns `true` if the TextBox was interacted by the user. |
| `container` | `HTMLElement` | Specifies the container element. |

```tsx
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

export default function App() {
  const [charCount, setCharCount] = useState(0);

  const handleInput = (args: any) => {
    setCharCount(args.value.length);
  };

  return (
    <div>
      <TextBoxComponent
        placeholder="Type something..."
        floatLabelType="Auto"
        input={handleInput}
      />
      <p>Characters: {charCount}</p>
    </div>
  );
}
```
