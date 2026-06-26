# Modal – Syncfusion React Speed Dial

## Overview

Enable modal mode by setting the `modal` property to `true`. When active, a semi-transparent overlay appears behind the popup, dimming the page and blocking interaction with elements outside the Speed Dial menu.

**When to use:** Use modal mode to guide users through required actions, prevent accidental background interaction, or create a focused workflow.

**Behavior:**
- A translucent overlay covers the page behind the Speed Dial popup
- Clicking anywhere on the overlay closes the popup
- Only Speed Dial items remain interactive while the popup is open

## Example

```tsx
import { SpeedDialComponent, SpeedDialItemModel } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import * as ReactDom from 'react-dom';

function App() {
  const items: SpeedDialItemModel[] = [
    { iconCss: 'e-icons e-cut' },
    { iconCss: 'e-icons e-copy' },
    { iconCss: 'e-icons e-paste' }
  ];

  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <SpeedDialComponent id='speeddial' items={items} openIconCss='e-icons e-edit'
        modal={true} target='#targetElement' />
    </div>
  );
}
export default App;
ReactDom.render(<App />, document.getElementById('button'));
```

## Notes

- `modal` defaults to `false` (no overlay)
- When `modal={true}` and the user clicks outside the items, the popup closes automatically
- Combine with `beforeClose` event to intercept or prevent closure on overlay click
