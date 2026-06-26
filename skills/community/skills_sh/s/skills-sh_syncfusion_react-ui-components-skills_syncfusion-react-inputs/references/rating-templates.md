# Templates in React Rating Component

## Table of Contents
- [Overview](#overview)
- [Empty Template (Unrated Items)](#empty-template-unrated-items)
- [Full Template (Rated Items)](#full-template-rated-items)
- [Emoji Rating Symbols](#emoji-rating-symbols)
- [SVG Icon Rating Symbols](#svg-icon-rating-symbols)
- [PNG Image Rating Symbols](#png-image-rating-symbols)
- [Precision Support in Templates](#precision-support-in-templates)

---

## Overview

The Rating component supports two template directives:

| Template | Purpose |
|----------|---------|
| `emptyTemplate` | Appearance of **unrated** items |
| `fullTemplate` | Appearance of **rated** items |

If only `emptyTemplate` is provided, it is used for both rated and unrated items — apply CSS to differentiate states.

Templates receive context with `value` (current item value) and `index` (0-based item position).

---

## Empty Template (Unrated Items)

Customize unrated item appearance using a render function as `emptyTemplate`:

```tsx
import { RatingComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  function emptyTemplate() {
    return (
      <React.Fragment>
        <span className="custom-font sf-rating-heart"></span>
      </React.Fragment>
    );
  }

  return (
    <div className="wrap">
      <RatingComponent id="rating" value={3} emptyTemplate={emptyTemplate} />
    </div>
  );
}
export default App;
```

---

## Full Template (Rated Items)

Provide both `emptyTemplate` and `fullTemplate` to control rated and unrated items independently:

```tsx
import { RatingComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  function emptyTemplate() {
    return (
      <React.Fragment>
        <span className="custom-font sf-icon-empty-star"></span>
      </React.Fragment>
    );
  }

  function fullTemplate() {
    return (
      <React.Fragment>
        <span className="custom-font sf-icon-fill-star"></span>
      </React.Fragment>
    );
  }

  return (
    <div className="wrap">
      <RatingComponent
        id="rating"
        value={3}
        emptyTemplate={emptyTemplate}
        fullTemplate={fullTemplate}
      />
    </div>
  );
}
export default App;
```

---

## Emoji Rating Symbols

Use emojis as rating symbols. Access the `index` from template context to return different emojis per position. Enable `enableSingleSelection` for discrete emoji selection and disable `enableAnimation` to prevent animation conflicts:

```tsx
import { RatingComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  function emptyTemplate(props: { index: number }) {
    const emojis = ['😡', '🙁', '😐', '🙂', '😀'];
    const classes = ['angry', 'disagree', 'neutral', 'agree', 'happy'];
    return (
      <span className={`${classes[props.index]} emoji`}>
        {emojis[props.index]}
      </span>
    );
  }

  return (
    <div className="wrap">
      <RatingComponent
        id="rating"
        value={3}
        emptyTemplate={emptyTemplate}
        enableSingleSelection={true}
        enableAnimation={false}
      />
    </div>
  );
}
export default App;
```

---

## SVG Icon Rating Symbols

Use SVG elements as rating symbols. Access `index` in the template to create unique gradient IDs per item:

```tsx
import { RatingComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  function emptyTemplate() {
    return (
      <svg width="35" height="25" className="e-rating-svg-icon">
        <rect width="35" height="25" fill="transparent" strokeWidth="2" stroke="rgb(173,181,189)" />
      </svg>
    );
  }

  function fullTemplate(props: { index: number }) {
    return (
      <svg width="35" height="25" className="e-rating-svg-icon">
        <defs>
          <linearGradient id={`grad${props.index}`} x1="0%" y1="0%" x2="100%" y2="0%">
            <stop className="start" offset="0%" />
            <stop className="end" offset="100%" />
          </linearGradient>
        </defs>
        <rect
          width="35"
          height="25"
          fill={`url(#grad${props.index})`}
          strokeWidth="2"
          stroke="rgb(173,181,189)"
        />
      </svg>
    );
  }

  return (
    <div className="wrap">
      <RatingComponent
        id="rating"
        value={4}
        emptyTemplate={emptyTemplate}
        fullTemplate={fullTemplate}
        enableAnimation={false}
      />
    </div>
  );
}
export default App;
```

---

## PNG Image Rating Symbols

Use PNG images as rating symbols:

```tsx
import { RatingComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  function emptyTemplate() {
    return (
      <img
        src="/images/star-empty.png"
        width="25"
        height="25"
        alt="empty star"
      />
    );
  }

  function fullTemplate() {
    return (
      <img
        src="/images/star-filled.png"
        width="25"
        height="25"
        alt="filled star"
      />
    );
  }

  return (
    <div className="wrap">
      <RatingComponent
        id="rating"
        value={4}
        emptyTemplate={emptyTemplate}
        fullTemplate={fullTemplate}
      />
    </div>
  );
}
export default App;
```

---

## Precision Support in Templates

When using templates with precision modes (half, quarter, exact), use the CSS variable `--rating-value` or the `value` from the template context to apply partial fills:

```css
/* Apply partial fill based on item value */
.e-rating-item-container {
  --rating-value: 0; /* set by the component per item */
}

.my-template-icon {
  background: linear-gradient(
    to right,
    gold calc(var(--rating-value) * 100%),
    lightgray calc(var(--rating-value) * 100%)
  );
}
```

> The `value` in the template context represents how much of that specific item should be "filled" (0 to 1), which enables partial fill rendering for fractional ratings.

---

## Tips

- Use `enableAnimation={false}` with emoji or image templates to avoid visual glitches.
- Use `enableSingleSelection={true}` with emoji templates for discrete mood pickers.
- Always set unique gradient IDs when using SVG templates with multiple items.
