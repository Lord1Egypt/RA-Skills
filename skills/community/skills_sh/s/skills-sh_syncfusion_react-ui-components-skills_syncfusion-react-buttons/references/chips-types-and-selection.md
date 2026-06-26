# Chip Types and Selection

## Table of Contents
- [Chip Types Overview](#chip-types-overview)
- [Input Chip](#input-chip)
- [Choice Chip (Single Selection)](#choice-chip-single-selection)
- [Filter Chip (Multiple Selection)](#filter-chip-multiple-selection)
- [Action Chip](#action-chip)
- [Deletable Chip](#deletable-chip)
- [Pre-selecting Chips](#pre-selecting-chips)
- [Handling Click Events](#handling-click-events)
- [Handling Delete Events](#handling-delete-events)
- [Disabled Chips](#disabled-chips)

---

## Chip Types Overview

The `selection` property on `ChipListComponent` controls the chip type behavior:

| Type | `selection` value | Purpose |
|------|-------------------|---------|
| Input Chip | `"None"` (default) + `enableDelete={true}` | User-generated tags that can be removed |
| Choice Chip | `"Single"` | Select one option (radio-like) |
| Filter Chip | `"Multiple"` | Select multiple options (checkbox-like) |
| Action Chip | `"None"` (default) | Triggers an action on click |

---

## Input Chip

Input chips represent user-provided values (e.g., email tags, search filters). They are typically deletable.

```tsx
import {
  ChipListComponent,
  ChipsDirective,
  ChipDirective
} from '@syncfusion/ej2-react-buttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';

enableRipple(true);

function App() {
  return (
    <ChipListComponent id="input-chip" enableDelete={true} selection="Single">
      <ChipsDirective>
        <ChipDirective text="Andrew" />
        <ChipDirective text="Janet" />
        <ChipDirective text="Laura" />
        <ChipDirective text="Margaret" />
      </ChipsDirective>
    </ChipListComponent>
  );
}
export default App;
```

- `enableDelete={true}` — shows the delete (×) icon on each chip.
- `selection="Single"` — only one chip is selected at a time in this input scenario.

---

## Choice Chip (Single Selection)

Choice chips allow selecting exactly one option from a group — similar to radio buttons.

```tsx
import {
  ChipListComponent,
  ChipsDirective,
  ChipDirective
} from '@syncfusion/ej2-react-buttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';

enableRipple(true);

function App() {
  return (
    <ChipListComponent id="choice-chip" selection="Single">
      <ChipsDirective>
        <ChipDirective text="Small" />
        <ChipDirective text="Medium" />
        <ChipDirective text="Large" />
        <ChipDirective text="Extra Large" />
      </ChipsDirective>
    </ChipListComponent>
  );
}
export default App;
```

- Set `selection="Single"` to enable single-choice behavior.
- Clicking a chip selects it and deselects the previously selected chip.
- Common use cases: view toggle, size selector, sort preference.

---

## Filter Chip (Multiple Selection)

Filter chips allow selecting multiple options simultaneously — similar to checkboxes.

```tsx
import {
  ChipListComponent,
  ChipsDirective,
  ChipDirective
} from '@syncfusion/ej2-react-buttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';

enableRipple(true);

function App() {
  return (
    <ChipListComponent id="filter-chip" selection="Multiple">
      <ChipsDirective>
        <ChipDirective text="Chai" />
        <ChipDirective text="Chung" />
        <ChipDirective text="Aniseed Syrup" />
        <ChipDirective text="Ikura" />
      </ChipsDirective>
    </ChipListComponent>
  );
}
export default App;
```

- Set `selection="Multiple"` to allow multi-selection.
- Selected chips receive the `e-active` CSS class.
- Common use cases: category filters, skill selection, preference toggles.

---

## Action Chip

Action chips trigger operations when clicked. They do not have selection state — they simply fire the `onClick` event.

```tsx
import {
  ChipListComponent,
  ChipsDirective,
  ChipDirective
} from '@syncfusion/ej2-react-buttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';

enableRipple(true);

function App() {
  function handleChipClick(e: any) {
    alert('You clicked: ' + e.target.textContent);
  }

  return (
    <ChipListComponent id="action-chip" onClick={handleChipClick}>
      <ChipsDirective>
        <ChipDirective text="Send a text" />
        <ChipDirective text="Set a reminder" />
        <ChipDirective text="Read my emails" />
        <ChipDirective text="Set alarm" />
      </ChipsDirective>
    </ChipListComponent>
  );
}
export default App;
```

- No `selection` prop needed; defaults to `"None"`.
- Use `onClick` to respond to interactions.
- Common use cases: shortcut buttons, suggested actions, command chips.

---

## Deletable Chip

Show a delete icon on each chip to allow users to remove them from the list.

```tsx
import {
  ChipListComponent,
  ChipsDirective,
  ChipDirective
} from '@syncfusion/ej2-react-buttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';

enableRipple(true);

function App() {
  return (
    <ChipListComponent id="deletable-chip" enableDelete={true}>
      <ChipsDirective>
        <ChipDirective text="Send a text" />
        <ChipDirective text="Set a reminder" />
        <ChipDirective text="Read my emails" />
        <ChipDirective text="Set alarm" />
      </ChipsDirective>
    </ChipListComponent>
  );
}
export default App;
```

- `enableDelete={true}` renders a delete button (×) on each chip.
- Works alongside any selection mode.
- Use the `delete` event to intercept before removal, and `deleted` event for post-removal logic.

---

## Pre-selecting Chips

Use `selectedChips` to pre-select chips on initial render. Accepts index(es) or chip text value(s).

```tsx
import {
  ChipListComponent,
  ChipsDirective,
  ChipDirective
} from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  // Pre-select chips at index 1 and 3
  const preSelected = [1, 3];

  return (
    <ChipListComponent
      id="filter-chip"
      selection="Multiple"
      selectedChips={preSelected}
    >
      <ChipsDirective>
        <ChipDirective text="Extra small" />
        <ChipDirective text="Small" />
        <ChipDirective text="Medium" />
        <ChipDirective text="Large" />
        <ChipDirective text="Extra large" />
      </ChipsDirective>
    </ChipListComponent>
  );
}
export default App;
```

- `selectedChips` accepts `string[]`, `number[]`, or a single `number`.
- Must be used with `selection="Single"` or `selection="Multiple"` to have visible effect.

---

## Handling Click Events

Use `onClick` for action chips, or `beforeClick` to intercept and potentially cancel a click:

```tsx
import {
  ChipListComponent,
  ChipsDirective,
  ChipDirective
} from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  function handleBeforeClick(e: any) {
    // e.cancel = true; // Uncomment to prevent click
    console.log('Before click:', e.text);
  }

  function handleClick(e: any) {
    console.log('Chip clicked:', e.target.textContent);
  }

  return (
    <ChipListComponent
      id="chip-events"
      selection="Single"
      beforeClick={handleBeforeClick}
      onClick={handleClick}
    >
      <ChipsDirective>
        <ChipDirective text="Option A" />
        <ChipDirective text="Option B" />
        <ChipDirective text="Option C" />
      </ChipsDirective>
    </ChipListComponent>
  );
}
export default App;
```

- `beforeClick` — fires before click is processed; set `e.cancel = true` to prevent.
- `onClick` — fires after the click event.

---

## Handling Delete Events

```tsx
import {
  ChipListComponent,
  ChipsDirective,
  ChipDirective
} from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  function handleDelete(e: any) {
    // e.cancel = true; // Uncomment to prevent deletion
    console.log('About to delete:', e.text);
  }

  function handleDeleted(e: any) {
    console.log('Chip deleted:', e.text);
  }

  return (
    <ChipListComponent
      id="chip-delete-events"
      enableDelete={true}
      delete={handleDelete}
      deleted={handleDeleted}
    >
      <ChipsDirective>
        <ChipDirective text="Tag One" />
        <ChipDirective text="Tag Two" />
        <ChipDirective text="Tag Three" />
      </ChipsDirective>
    </ChipListComponent>
  );
}
export default App;
```

- `delete` — fires before the chip is removed (can cancel).
- `deleted` — fires after the chip has been removed.

---

## Disabled Chips

Disable the entire chip list using the `enabled` property:

```tsx
<ChipListComponent id="chip-disabled" enabled={false}>
  <ChipsDirective>
    <ChipDirective text="Disabled Chip 1" />
    <ChipDirective text="Disabled Chip 2" />
  </ChipsDirective>
</ChipListComponent>
```

- `enabled={false}` — disables all chips; they are visible but not interactive.
- ARIA: `aria-disabled="true"` is automatically applied.
