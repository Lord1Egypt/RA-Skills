# Selection and Nesting — Syncfusion React ButtonGroup

## Table of Contents
- [Single Selection (Radio Type)](#single-selection-radio-type)
- [Multiple Selection (Checkbox Type)](#multiple-selection-checkbox-type)
- [Set Initial Selected State](#set-initial-selected-state)
- [Nesting with DropDownButton](#nesting-with-dropdownbutton)
- [Nesting with SplitButton](#nesting-with-splitbutton)

## Single Selection (Radio Type)

Radio-type ButtonGroup allows only one button to be active at a time. Create it using `<input type="radio">` elements paired with `<label>` elements:

- Each `<input>` gets a unique `id` and a shared `name` to form the radio group.
- Each `<label>` has `htmlFor` matching the input's `id` and the `e-btn` class to style it as a button.

```tsx
import * as React from 'react';
import * as ReactDom from 'react-dom';

// To render radio type ButtonGroup.
function App() {
  return (
    <div>
      <div className='e-btn-group'>
          <input type="radio" id="radioleft" name="align" value="left" />
          <label className="e-btn" htmlFor="radioleft">Left</label>
          <input type="radio" id="radiomiddle" name="align" value="middle" />
          <label className="e-btn" htmlFor="radiomiddle">Center</label>
          <input type="radio" id="radioright" name="align" value="right"/>
          <label className="e-btn" htmlFor="radioright">Right</label>
      </div>
    </div>
  );
}
export default App;
ReactDom.render(<App />,document.getElementById('buttongroup'));
```

## Multiple Selection (Checkbox Type)

Checkbox-type ButtonGroup allows multiple buttons to be selected simultaneously. Create it using `<input type="checkbox">` elements paired with `<label>` elements:

```tsx
import * as React from 'react';
import * as ReactDom from 'react-dom';

// To render checkbox type ButtonGroup.
function App() {
  return (
    <div>
      <div className='e-btn-group'>
          <input type="checkbox" id="checkbold" name="font" value="bold"/>
          <label className="e-btn" htmlFor="checkbold">Bold</label>
          <input type="checkbox" id="checkitalic" name="font" value="italic" />
          <label className="e-btn" htmlFor="checkitalic">Italic</label>
          <input type="checkbox" id="checkline" name="font" value="underline"/>
          <label className="e-btn" htmlFor="checkline">Underline</label>
      </div>
    </div>
  );
}
export default App;
ReactDom.render(<App />,document.getElementById('buttongroup'));
```

## Set Initial Selected State

To show a button as selected on initial render, add the `checked={true}` attribute to the corresponding `<input>` element:

```tsx
import * as React from 'react';
import * as ReactDom from 'react-dom';

// To render checkbox type ButtonGroup with pre-selected state.
function App() {
  return (
    <div>
      <div className='e-btn-group'>
          <input type="checkbox" id="checkbold" name="font" value="bold" checked={true}/>
          <label className="e-btn" htmlFor="checkbold">Bold</label>
          <input type="checkbox" id="checkitalic" name="font" value="italic" />
          <label className="e-btn" htmlFor="checkitalic">Italic</label>
          <input type="checkbox" id="checkline" name="font" value="underline"/>
          <label className="e-btn" htmlFor="checkline">Underline</label>
      </div>
    </div>
  );
}
export default App;
ReactDom.render(<App />,document.getElementById('buttongroup'));
```

This works the same way for radio-type ButtonGroups — add `checked={true}` to the radio input that should be initially active.

## Nesting with DropDownButton

Import `DropDownButtonComponent` from `@syncfusion/ej2-react-splitbuttons` and place it inside the `e-btn-group` container alongside `ButtonComponent` elements:

```tsx
import * as React from 'react';
import * as ReactDom from 'react-dom';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { DropDownButtonComponent, ItemModel } from '@syncfusion/ej2-react-splitbuttons';

// To render ButtonGroup with DropDownButton nesting.
function App() {
  let items: ItemModel[] = [
    { text: 'Learn SQL' },
    { text: 'Learn PHP' },
    { text: 'Learn Bootstrap' }
  ];

  return (
    <div>
      <div className='e-btn-group'>
          <ButtonComponent>HTML</ButtonComponent>
          <ButtonComponent>CSS</ButtonComponent>
          <ButtonComponent>Javascript</ButtonComponent>
          <DropDownButtonComponent id="dropdownelement" items={items}> More </DropDownButtonComponent>
      </div>
    </div>
  );
}
export default App;
ReactDom.render(<App />,document.getElementById('buttongroup'));
```

## Nesting with SplitButton

Import `SplitButtonComponent` from `@syncfusion/ej2-react-splitbuttons` and place it inside the `e-btn-group` container:

```tsx
import * as React from 'react';
import * as ReactDom from 'react-dom';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { SplitButtonComponent, ItemModel } from '@syncfusion/ej2-react-splitbuttons';

// To render ButtonGroup with SplitButton nesting.
function App() {
    let items: ItemModel[] = [
    { text: 'Paste' },
    { text: 'Paste Text' },
    { text: 'Paste Special' }
  ];

  return (
    <div>
      <div className='e-btn-group'>
          <ButtonComponent>Cut</ButtonComponent>
          <ButtonComponent>Copy</ButtonComponent>
          <SplitButtonComponent id="splitbuttonelement" items={items}> Paste </SplitButtonComponent>
      </div>
    </div>
  );
}
export default App;
ReactDom.render(<App />,document.getElementById('buttongroup'));
```

> SplitButton nesting is not supported in vertical orientation (`e-vertical`).
