# Form Validation with MaskedTextBox

Integrate the Syncfusion `FormValidator` with MaskedTextBox to enforce validation rules, display custom error messages, and check for complete vs. partial masked input.

## Setup

Import FormValidator from `@syncfusion/ej2-inputs`:

```bash
npm install @syncfusion/ej2-inputs --save
```

```tsx
import { FormValidator, FormValidatorModel } from '@syncfusion/ej2-inputs';
import { MaskedTextBoxComponent } from '@syncfusion/ej2-react-inputs';
```

## Custom Validation Example

The following example validates a mobile number field. The custom rule checks that the entered value is either empty (skip) or contains at least 10 digits.

```tsx
import { FormValidator, FormValidatorModel } from '@syncfusion/ej2-inputs';
import { MaskedTextBoxComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import * as ReactDOM from 'react-dom';

export default class App extends React.Component<{}, {}> {
  public maskInstance: any;

  public componentDidMount(): void {
    // Returns true if value length >= 10 (or is empty)
    const customFn = (args: { [key: string]: string }) => {
      const length = (args.element as any).ej2_instances[0].value.length;
      if (length !== 0) {
        return length >= 10;
      }
      return true;
    };

    // Returns 0 if empty, otherwise returns length (for maxLength rule)
    const custom = (args: { [key: string]: string }) => {
      const length = (args.element as any).ej2_instances[0].value.length;
      return length === 0 ? 0 : length;
    };

    const options: FormValidatorModel = {
      customPlacement: (inputElement: HTMLElement, errorElement: HTMLElement) => {
        // Place error message in a specific container
        (document.querySelector('#masktextbox') as HTMLElement).appendChild(errorElement);
      },
      rules: {
        // 'mask_value' must match the `name` attribute on the MaskedTextBoxComponent
        mask_value: {
          numberValue: [customFn, 'Enter valid mobile number']
        }
      }
    };

    const formObject = new FormValidator('#form-element', options);

    // Additional rule: show message when field is empty
    formObject.addRules('mask_value', {
      maxLength: [custom, 'Enter mobile number']
    });

    (document.getElementById('submit_btn') as HTMLElement).addEventListener('click', () => {
      formObject.validate('mask_value');
      // Check for complete fill: no prompt characters remaining
      if (
        this.maskInstance.value !== '' &&
        this.maskInstance.value.indexOf(this.maskInstance.promptChar) === -1
      ) {
        alert('Submitted');
      }
    });
  }

  public render() {
    return (
      <form id="form-element">
        <MaskedTextBoxComponent
          id="mask"
          name="mask_value"
          ref={(mask) => { this.maskInstance = mask; }}
          placeholder="Mobile Number"
          mask="000-000-0000"
          floatLabelType="Always"
        />
        <label className="e-error" htmlFor="mask_value" />
        <div id="masktextbox" />
        <button id="submit_btn" type="button" style={{ marginTop: '10px' }}>
          Submit
        </button>
      </form>
    );
  }
}

ReactDOM.render(<App />, document.getElementById('root'));
```

## Key Validation Concepts

### Accessing MaskedTextBox Value in Custom Rules

Inside a FormValidator custom function, access the component instance via `ej2_instances`:

```tsx
const value = (args.element as any).ej2_instances[0].value;
// `value` is the raw input without literals and prompt characters
```

### Checking for Incomplete Mask Input

After form submission, verify all mask positions are filled by checking that `promptChar` is not present in the raw value:

```tsx
const isComplete =
  maskInstance.value !== '' &&
  maskInstance.value.indexOf(maskInstance.promptChar) === -1;
```

### Custom Error Placement

Use `customPlacement` in `FormValidatorModel` to position error messages in a specific DOM container instead of adjacent to the input:

```tsx
customPlacement: (inputElement, errorElement) => {
  document.querySelector('#error-container').appendChild(errorElement);
}
```

### Name Attribute Requirement

The `name` attribute on `MaskedTextBoxComponent` must match the field name used in `FormValidator` rules:

```tsx
// Component
<MaskedTextBoxComponent name="mask_value" ... />

// Validator rules
rules: {
  mask_value: { required: [true, 'This field is required'] }
}
```

## Notes

- `FormValidator` works on the underlying `<input>` element identified by `name`
- Use `addRules()` to add additional rules after initialization
- Combine `required`, `minLength`, `maxLength`, and custom functions in the `rules` object
