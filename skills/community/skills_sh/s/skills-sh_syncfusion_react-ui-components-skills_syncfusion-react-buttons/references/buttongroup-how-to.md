# How-To Guide — Syncfusion React ButtonGroup

## Table of Contents
- [Add Icons to Buttons](#add-icons-to-buttons)
- [Rounded Corners](#rounded-corners)
- [Disable Individual or All Buttons](#disable-individual-or-all-buttons)
- [Enable Ripple Effect](#enable-ripple-effect)
- [Enable RTL Support](#enable-rtl-support)
- [Vertical Orientation](#vertical-orientation)
- [Form Submit with ButtonGroup](#form-submit-with-buttongroup)
- [Initialize Using createButtonGroup Utility](#initialize-using-createbuttongroup-utility)

---

## Add Icons to Buttons

Use the `iconCss` property on `ButtonComponent` to display an icon alongside button text. Pass one or more CSS class names (space-separated) that map to icon font classes:

```tsx
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

// To render ButtonGroup with icons.
function App() {
  return (
    <div>
      <div className='e-btn-group'>
        <ButtonComponent iconCss='e-icons e-left-icon'>HTML</ButtonComponent>
        <ButtonComponent iconCss='e-icons e-middle-icon'>CSS</ButtonComponent>
        <ButtonComponent iconCss='e-icons e-right-icon'>Javascript</ButtonComponent>
      </div>
    </div>
  );
}
export default App;
ReactDom.render(<App />,document.getElementById('buttongroup'));
```

---

## Rounded Corners

Apply the `e-round-corner` class to the container `div` to add border-radius styling to the entire group:

```tsx
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

// To render ButtonGroup with rounded corner.
function App() {
  return (
    <div>
      <div className='e-btn-group e-round-corner'>
        <ButtonComponent>HTML</ButtonComponent>
        <ButtonComponent>CSS</ButtonComponent>
        <ButtonComponent>Javascript</ButtonComponent>
      </div>
    </div>
  );
}
export default App;
ReactDom.render(<App />,document.getElementById('buttongroup'));
```

---

## Disable Individual or All Buttons

### Disable a single button

Set `disabled={true}` on a specific `ButtonComponent` to disable only that button:

```tsx
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

// To disable single button/whole ButtonGroup.
function App() {
  return (
    <div>
      <div className='e-btn-group'>
        <ButtonComponent>HTML</ButtonComponent>
        <ButtonComponent disabled={true}>CSS</ButtonComponent>
        <ButtonComponent>Javascript</ButtonComponent>
      </div>
      <div className='e-btn-group'>
        <ButtonComponent disabled={true}>HTML</ButtonComponent>
        <ButtonComponent disabled={true}>CSS</ButtonComponent>
        <ButtonComponent disabled={true}>Javascript</ButtonComponent>
      </div>
    </div>
  );
}
export default App;
ReactDom.render(<App />,document.getElementById('buttongroup'));
```

> For radio/checkbox type ButtonGroups, add the `disabled` attribute directly to the `<input>` element to disable individual options.

---

## Enable Ripple Effect

Import `enableRipple` from `@syncfusion/ej2-base` and call it with `true` before rendering the component:

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

enableRipple(true);

// To enable ripple in ButtonGroup.
function App() {
  return (
    <div>
      <div className='e-btn-group'>
        <ButtonComponent>HTML</ButtonComponent>
        <ButtonComponent>CSS</ButtonComponent>
        <ButtonComponent>Javascript</ButtonComponent>
      </div>
    </div>
  );
}
export default App;
ReactDom.render(<App />,document.getElementById('buttongroup'));
```

---

## Enable RTL Support

Add the `e-rtl` class to the container `div` to flip the button order for right-to-left languages:

```tsx
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

// To render ButtonGroup with RTL.
function App() {
  return (
    <div>
      <div className='e-btn-group e-rtl'>
        <ButtonComponent>HTML</ButtonComponent>
        <ButtonComponent>CSS</ButtonComponent>
        <ButtonComponent>Javascript</ButtonComponent>
      </div>
    </div>
  );
}
export default App;
ReactDom.render(<App />,document.getElementById('buttongroup'));
```

---

## Vertical Orientation

Add the `e-vertical` class to the container `div` to stack buttons vertically instead of horizontally:

```tsx
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

// To render ButtonGroup with vertical orientation.
function App() {
  return (
    <div>
      <div className='e-btn-group e-vertical'>
        <ButtonComponent>HTML</ButtonComponent>
        <ButtonComponent>CSS</ButtonComponent>
        <ButtonComponent>Javascript</ButtonComponent>
      </div>
    </div>
  );
}
export default App;
ReactDom.render(<App />,document.getElementById('buttongroup'));
```

> Vertical orientation does not support SplitButton nesting.

---

## Form Submit with ButtonGroup

Use the `name` attribute on radio/checkbox inputs to group them for form submission. The value of the checked option is submitted with the form. Disabled inputs are excluded from submission.

```tsx
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

// To render ButtonGroup in form.
function App() {
  function componentDidMount(): void {
    (document.getElementById('female') as HTMLInputElement).checked = true;
  }
  return (
    <div>
      <form>
        <div className='e-btn-group'>
          <input type="radio" id="male" name="gender" value="male"/>
          <label className="e-btn" htmlFor="male">Male</label>
          <input type="radio" id="female" name="gender" value="female"/>
          <label className="e-btn" htmlFor="female">Female</label>
          <input type="radio" id="transgender" name="gender" value="transgender"/>
          <label className="e-btn" htmlFor="transgender">Transgender</label>
        </div>
        <ButtonComponent isPrimary={true}>Submit</ButtonComponent>
      </form>
    </div>
  );
}
export default App;
ReactDom.render(<App />,document.getElementById('buttongroup'));
```

---

## Initialize Using createButtonGroup Utility

The `createButtonGroup` utility function from `@syncfusion/ej2-splitbuttons` provides an alternative approach to initialize ButtonGroup with minimal JSX. It applies ButtonGroup styling to plain `<button>` or `<input>` elements programmatically.

Call `createButtonGroup` inside a `useEffect` hook so it runs after the DOM is ready. Pass the container selector and a `buttons` array with a `content` property for each button.

```tsx
import { createButtonGroup } from '@syncfusion/ej2-splitbuttons';
import { useEffect } from "react";
import * as React from 'react';
import * as ReactDom from 'react-dom';

// To render ButtonGroup using `util` function.
function App() {
  useEffect(() => {
    createButtonGroup('#basic', {
      buttons: [
          { content: 'HTML' },
          { content: 'CSS' },
          { content: 'Javascript'}
      ]
    });

    createButtonGroup('#checkbox', {
      buttons: [
          { content: 'Bold' },
          { content: 'Italic' },
          { content: 'Undeline'}
      ]
    });

    createButtonGroup('#radio', {
      buttons: [
          { content: 'Left' },
          { content: 'Center' },
          { content: 'Right'}
      ]
    });
  }, []);

  return (
    <div>
      <h5>Normal behavior</h5>
      <div id='basic'>
        <button/>
        <button/>
        <button/>
      </div>
      <h5>Checkbox type behavior</h5>
      <div id='checkbox'>
        <input type="checkbox" id="checkbold" name="font" value='bold' />
        <input type="checkbox" id="checkitalic" name="font" value='italic' />
        <input type="checkbox" id="checkunderline" name="font" value='underline' />
      </div>
      <h5>Radiobutton type behavior</h5>
      <div id='radio'>
        <input type="radio" id="radioleft" name="align" value='left'/>
        <input type="radio" id="radiomiddle" name="align" value='middle'/>
        <input type="radio" id="radioright" name="align" value='right'/>
      </div>
    </div>
  );
}
export default App;
ReactDom.render(<App />,document.getElementById('buttongroup'));
```

> If `null` is passed for a button option, that button is skipped by `createButtonGroup`.
