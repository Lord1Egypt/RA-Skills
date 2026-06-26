# Chip Customization

## Table of Contents
- [Predefined Styles](#predefined-styles)
- [Leading Icon](#leading-icon)
- [Leading Icon URL](#leading-icon-url)
- [Avatar Image](#avatar-image)
- [Avatar Text](#avatar-text)
- [Trailing Icon](#trailing-icon)
- [Trailing Icon URL](#trailing-icon-url)
- [Outline Chip](#outline-chip)
- [Custom Template](#custom-template)
- [HTML Attributes](#html-attributes)
- [Disabled State](#disabled-state)
- [RTL Support](#rtl-support)

---

## Predefined Styles

Apply semantic color styles using the `cssClass` property on `ChipDirective` or `ChipListComponent`.

| Class | Meaning |
|-------|---------|
| `e-primary` | Primary action or important chip |
| `e-success` | Positive / success status |
| `e-info` | Informational / neutral content |
| `e-warning` | Caution or warning |
| `e-danger` | Error, negative, or destructive action |

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
    <ChipListComponent id="styled-chips">
      <ChipsDirective>
        <ChipDirective text="Primary" cssClass="e-primary" />
        <ChipDirective text="Success" cssClass="e-success" />
        <ChipDirective text="Info" cssClass="e-info" />
        <ChipDirective text="Warning" cssClass="e-warning" />
        <ChipDirective text="Danger" cssClass="e-danger" />
      </ChipsDirective>
    </ChipListComponent>
  );
}
export default App;
```

- Apply `cssClass` on `ChipDirective` for per-chip styling, or on `ChipListComponent` to apply to all chips.

---

## Leading Icon

Place an icon to the left of the chip text using `leadingIconCss`. Define the CSS class with a background image.

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
    <ChipListComponent id="leading-icon-chips">
      <ChipsDirective>
        <ChipDirective text="Andrew" leadingIconCss="andrew" />
        <ChipDirective text="Janet" leadingIconCss="janet" />
        <ChipDirective text="Laura" leadingIconCss="laura" />
        <ChipDirective text="Margaret" leadingIconCss="margaret" />
      </ChipsDirective>
    </ChipListComponent>
  );
}
export default App;
```

CSS to define each icon class:
```css
.andrew {
  background-image: url('path/to/andrew.png');
}
.janet {
  background-image: url('path/to/janet.png');
}
```

- `leadingIconCss` — CSS class applied to the leading icon element.

---

## Leading Icon URL

Provide a direct image URL for the leading icon using `leadingIconUrl`:

```tsx
<ChipDirective
  text="Profile"
  leadingIconUrl="https://example.com/images/profile.png"
/>
```

- Useful when you don't want to define CSS background-image classes.
- `leadingIconUrl` sets the `src` of an `<img>` element inside the chip.

---

## Avatar Image

Display a circular avatar image using `avatarIconCss`. The CSS class defines the avatar's background image.

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
    <ChipListComponent id="avatar-chips">
      <ChipsDirective>
        <ChipDirective text="Andrew" avatarIconCss="andrew" />
        <ChipDirective text="Janet" avatarIconCss="janet" />
        <ChipDirective text="Laura" avatarIconCss="laura" />
        <ChipDirective text="Margaret" avatarIconCss="margaret" />
      </ChipsDirective>
    </ChipListComponent>
  );
}
export default App;
```

CSS:
```css
.andrew {
  background-image: url('path/to/andrew.png');
}
```

- `avatarIconCss` renders the icon inside a circular avatar container (distinct from `leadingIconCss`).

---

## Avatar Text

Show initials or short labels inside a circular avatar using `avatarText`:

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
    <ChipListComponent id="avatar-text-chips">
      <ChipsDirective>
        <ChipDirective text="Andrew" avatarText="A" />
        <ChipDirective text="Janet" avatarText="J" />
        <ChipDirective text="Laura" avatarText="L" />
        <ChipDirective text="Margaret" avatarText="M" />
      </ChipsDirective>
    </ChipListComponent>
  );
}
export default App;
```

- `avatarText` — ideal for user initials when avatar images aren't available.
- Renders text inside the circular avatar area.

---

## Trailing Icon

Add an icon to the right of the chip text using `trailingIconCss`:

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
    <ChipListComponent id="trailing-icon-chips">
      <ChipsDirective>
        <ChipDirective text="Andrew" trailingIconCss="e-dlt-btn" />
        <ChipDirective text="Janet" trailingIconCss="e-dlt-btn" />
        <ChipDirective text="Laura" trailingIconCss="e-dlt-btn" />
        <ChipDirective text="Margaret" trailingIconCss="e-dlt-btn" />
      </ChipsDirective>
    </ChipListComponent>
  );
}
export default App;
```

- `trailingIconCss` — applies a CSS class to the trailing icon element on the right side.
- Use `e-dlt-btn` for the built-in delete icon style.

---

## Trailing Icon URL

Provide a direct image URL for the trailing icon using `trailingIconUrl`:

```tsx
<ChipDirective
  text="Download"
  trailingIconUrl="https://example.com/icons/download.svg"
/>
```

---

## Outline Chip

Create chips with a visible border and transparent background using `cssClass="e-outline"`:

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
    <div>
      {/* Outline chip list */}
      <ChipListComponent id="outline-chips" cssClass="e-outline">
        <ChipsDirective>
          <ChipDirective text="Chai" />
          <ChipDirective text="Chang" />
          <ChipDirective text="Aniseed Syrup" />
          <ChipDirective text="Ikura" />
        </ChipsDirective>
      </ChipListComponent>

      {/* Outline chip list with delete */}
      <ChipListComponent id="outline-deletable" cssClass="e-outline" enableDelete={true}>
        <ChipsDirective>
          <ChipDirective text="Andrew" />
          <ChipDirective text="Janet" />
          <ChipDirective text="Laura" />
          <ChipDirective text="Margaret" />
        </ChipsDirective>
      </ChipListComponent>
    </div>
  );
}
export default App;
```

- Apply `cssClass="e-outline"` on the `ChipListComponent` to outline all chips in the list.

---

## Custom Template

Use the `template` prop on `ChipDirective` to fully customize the chip's inner HTML content:

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
    <ChipListComponent id="template-chips">
      <ChipsDirective>
        <ChipDirective
          leadingIconCss="trendingIcon"
          template='<a href="https://example.com/news" target="_blank" class="chip-link">#BreakingNews</a><span class="chip-count">125k posts</span>'
        />
        <ChipDirective
          leadingIconCss="cameraIcon"
          template='<a href="https://example.com/photos" target="_blank" class="chip-link">#PhotoOfTheDay</a>'
        />
      </ChipsDirective>
    </ChipListComponent>
  );
}
export default App;
```

- `template` accepts an HTML string and replaces the default chip content.
- Combine with `leadingIconCss` or `avatarIconCss` for richer layouts.
- Useful for chips that include links, badges, or custom sub-elements.

---

## HTML Attributes

Pass additional HTML attributes (e.g., `aria-label`, `title`, `data-*`) using `htmlAttributes`:

```tsx
<ChipListComponent
  id="chip-accessible"
  htmlAttributes={{ 'aria-label': 'Contact chips', title: 'Team Members' }}
>
  <ChipsDirective>
    <ChipDirective text="Andrew" />
    <ChipDirective text="Janet" />
  </ChipsDirective>
</ChipListComponent>
```

- `htmlAttributes` accepts `{ [key: string]: string }`.
- Useful for accessibility labels, test IDs, or custom data attributes.

---

## Disabled State

Disable the chip list so chips are visible but not interactive:

```tsx
<ChipListComponent id="chip-disabled" enabled={false}>
  <ChipsDirective>
    <ChipDirective text="Disabled" />
    <ChipDirective text="Not Clickable" />
  </ChipsDirective>
</ChipListComponent>
```

---

## RTL Support

Enable right-to-left layout for RTL languages:

```tsx
<ChipListComponent id="chip-rtl" enableRtl={true}>
  <ChipsDirective>
    <ChipDirective text="مرحبا" />
    <ChipDirective text="العالم" />
  </ChipsDirective>
</ChipListComponent>
```

- `enableRtl={true}` — flips the chip layout direction for Arabic, Hebrew, etc.
