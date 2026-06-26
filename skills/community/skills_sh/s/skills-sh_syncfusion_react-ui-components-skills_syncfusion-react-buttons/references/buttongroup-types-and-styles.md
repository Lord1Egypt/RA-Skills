# Types and Styles — Syncfusion React ButtonGroup

## Table of Contents
- [Outline ButtonGroup](#outline-buttongroup)
- [Predefined Styles](#predefined-styles)
- [Mixing Styles in a Group](#mixing-styles-in-a-group)

## Outline ButtonGroup

An outline ButtonGroup displays buttons with borders and transparent backgrounds. Apply the `e-outline` class to both the container `div` and to each `ButtonComponent` via the `cssClass` property.

```tsx
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

// To render outline ButtonGroup.
function App() {
  return (
    <div>
      <div className='e-btn-group e-outline'>
        <ButtonComponent cssClass='e-outline'>HTML</ButtonComponent>
        <ButtonComponent cssClass='e-outline'>CSS</ButtonComponent>
        <ButtonComponent cssClass='e-outline'>Javascript</ButtonComponent>
      </div>
    </div>
  );
}
export default App;
ReactDom.render(<App />,document.getElementById('buttongroup'));
```

> The ButtonGroup does not support `flat` or `round` button types. Use predefined styles for visual customization.

## Predefined Styles

Apply color-coded styles to individual buttons using the `cssClass` property on `ButtonComponent`. Available classes:

| CSS Class | Meaning |
|---|---|
| `e-primary` | Primary action |
| `e-success` | Positive / success action |
| `e-info` | Informative action |
| `e-warning` | Action requiring caution |
| `e-danger` | Negative / destructive action |

Each class gives the button a distinct background color so users can quickly understand the action's intent.

## Mixing Styles in a Group

Different buttons within the same group can each have different styles:

```tsx
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

// To render ButtonGroup with different styles.
function App() {
  return (
    <div>
      <div className='e-btn-group'>
        <ButtonComponent cssClass='e-info'>View</ButtonComponent>
        <ButtonComponent>Edit</ButtonComponent>
        <ButtonComponent cssClass='e-danger'>Delete</ButtonComponent>
      </div>
    </div>
  );
}
export default App;
ReactDom.render(<App />,document.getElementById('buttongroup'));
```

> Predefined styles provide visual indication only. Always ensure button labels clearly describe the action for screen reader users.
