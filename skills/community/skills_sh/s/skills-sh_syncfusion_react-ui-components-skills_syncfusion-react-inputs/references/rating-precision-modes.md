# Precision Modes in React Rating Component

Control how finely users can select rating values using the `precision` property with the `PrecisionType` enum.

## Supported Precision Types

| Type | Increment | Example values |
|------|-----------|----------------|
| `Full` (default) | 1.0 | 1, 2, 3, 4, 5 |
| `Half` | 0.5 | 2.5, 3.0, 3.5, 4.0 |
| `Quarter` | 0.25 | 3.75, 4.0, 4.25, 4.5 |
| `Exact` | 0.1 | 3.9, 4.0, 4.1, 4.2 |

---

## All Precision Types Together

```tsx
import { RatingComponent, PrecisionType } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div className="wrap">
      <label>Full Precision</label><br />
      <RatingComponent id="rating1" value={3} precision={PrecisionType.Full} /><br />

      <label>Half Precision</label><br />
      <RatingComponent id="rating2" value={2.5} precision={PrecisionType.Half} /><br />

      <label>Quarter Precision</label><br />
      <RatingComponent id="rating3" value={3.75} precision={PrecisionType.Quarter} /><br />

      <label>Exact Precision</label><br />
      <RatingComponent id="rating4" value={2.3} precision={PrecisionType.Exact} /><br />
    </div>
  );
}
export default App;
```

---

## Full Precision (Default)

Ratings snap to whole numbers. Most common for simple star ratings.

```tsx
<RatingComponent id="rating" value={3} precision={PrecisionType.Full} />
```

---

## Half Precision

Ratings snap to 0.5 increments. Useful for movie/product ratings where half stars are needed.

```tsx
import { RatingComponent, PrecisionType } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <RatingComponent id="rating" value={3.5} precision={PrecisionType.Half} />
  );
}
export default App;
```

---

## Quarter Precision

Ratings snap to 0.25 increments. Use when finer granularity than half is needed.

```tsx
<RatingComponent id="rating" value={3.75} precision={PrecisionType.Quarter} />
```

---

## Exact Precision

Ratings snap to 0.1 increments. Use when very fine-grained ratings are required.

```tsx
<RatingComponent id="rating" value={2.3} precision={PrecisionType.Exact} />
```

---

## Tips

- The `precision` property also accepts string values: `'Full'`, `'Half'`, `'Quarter'`, `'Exact'`.
- When using templates (`emptyTemplate`/`fullTemplate`), use the CSS variable `--rating-value` or the `value` from template context to support visual partial fills.
- Combine `precision={PrecisionType.Half}` with `showLabel={true}` to display the exact decimal value (e.g., "3.5").
