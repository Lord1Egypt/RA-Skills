# Value Binding – Syncfusion React AutoComplete

Value binding associates a data value with the component. The AutoComplete supports binding both primitive types and full object values.

---

## Primitive Data Types

Bind a string, number, boolean, or null value using the `value` property. The component will pre-select the matching item:

```tsx
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

export default class App extends React.Component<{}, {}> {
  private records: string[] = [];
  private value: string = 'Item 1';

  constructor(props: {}) {
    super(props);
    this.records = Array.from({ length: 10 }, (_, i) => `Item ${i + 1}`);
  }

  public render() {
    return (
      <AutoCompleteComponent
        id="datas"
        dataSource={this.records}
        value={this.value}
        popupHeight="200px"
        placeholder="e.g. Item 1"
      />
    );
  }
}
```

Supported primitive types:
- `string`
- `number`
- `boolean`
- `null` (clears selection)

---

## Object Data Types (allowObjectBinding)

When `allowObjectBinding={true}`, the `value` property holds a full object instead of a primitive. The object type matches the selected item in the data source.

```tsx
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

export default class App extends React.Component<{}, {}> {
  private fields: object = { value: 'text' };
  private records: { [key: string]: Object }[] = [];

  // Pre-select "Item 1" by providing the full object
  private value: { [key: string]: Object } = { id: 'id1', text: 'Item 1' };

  constructor(props: {}) {
    super(props);
    this.records = Array.from({ length: 150 }, (_, i) => ({
      id: `id${i + 1}`,
      text: `Item ${i + 1}`,
    }));
  }

  public render() {
    return (
      <AutoCompleteComponent
        id="datas"
        dataSource={this.records}
        fields={this.fields}
        value={this.value as any}
        allowObjectBinding={true}
        popupHeight="200px"
        placeholder="e.g. Item 1"
      />
    );
  }
}
```

> When `allowObjectBinding` is enabled, the `change` event's `value` argument will be the full matching object, not just a scalar value.

---

## Key Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `value` | `number \| string \| boolean \| object \| null` | `null` | Gets or sets the selected value |
| `allowObjectBinding` | `boolean` | `false` | When true, value is the full selected object |
