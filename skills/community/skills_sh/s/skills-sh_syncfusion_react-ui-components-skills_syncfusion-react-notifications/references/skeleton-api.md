# Skeleton API Reference

## Table of Contents
- [Import](#import)
- [Properties](#properties)
- [Methods](#methods)
- [Enums](#enums)
- [Usage Examples](#usage-examples)

---

## Import

```tsx
import { SkeletonComponent } from '@syncfusion/ej2-react-notifications';
```

---

## Properties

### cssClass
`string` — Default: `""`

Defines one or more CSS classes (space-separated) for customizing the Skeleton's appearance. Use to override shimmer color, background, border-radius, and animation speed.

```tsx
<SkeletonComponent shape="Circle" width="60px" cssClass="my-custom-skeleton" />
```

---

### enablePersistence
`boolean` — Default: `false`

Enable or disable persisting the component's state between page reloads. When `true`, state is stored in browser local storage.

```tsx
<SkeletonComponent height="15px" enablePersistence={true} />
```

---

### enableRtl
`boolean` — Default: `false`

Enable or disable rendering the component in right-to-left direction. Mirrors shimmer animation and layout for RTL languages.

```tsx
<SkeletonComponent height="15px" width="80%" enableRtl={true} />
```

---

### height
`string | number` — Default: `""`

Defines the height of the Skeleton. Height is required for `"Text"` and `"Rectangle"` shapes. It is **not required** when `shape` is `"Circle"` or `"Square"` (width is used as the dimension for those).

```tsx
<SkeletonComponent height="20px" width="60%" />
<SkeletonComponent shape="Rectangle" width="100%" height="150px" />
```

---

### label
`string` — Default: `"Loading…"`

Defines the `aria-label` attribute value for accessibility. Customize to describe the specific content being loaded, improving screen reader context.

```tsx
<SkeletonComponent shape="Circle" width="48px" label="Loading user avatar" />
```

---

### locale
`string` — Default: `''`

Overrides the global culture and localization value for this component. The default global culture is `'en-US'`.

```tsx
<SkeletonComponent height="15px" locale="fr-FR" />
```

---

### shape
`string | SkeletonType` — Default: `SkeletonType.Text` (`"Text"`)

Defines the visual shape of the Skeleton. Accepted values: `"Text"`, `"Circle"`, `"Square"`, `"Rectangle"`.

```tsx
<SkeletonComponent shape="Circle" width="48px" />
<SkeletonComponent shape="Square" width="32px" />
<SkeletonComponent shape="Rectangle" width="100%" height="150px" />
<SkeletonComponent height="15px" /> {/* Text (default) */}
```

---

### shimmerEffect
`string | ShimmerEffect` — Default: `ShimmerEffect.Wave` (`"Wave"`)

Defines the animation effect of the Skeleton. Accepted values: `"Wave"`, `"Pulse"`, `"Fade"`.

```tsx
<SkeletonComponent shape="Circle" width="48px" shimmerEffect="Pulse" />
<SkeletonComponent height="15px" shimmerEffect="Fade" />
<SkeletonComponent height="15px" shimmerEffect="Wave" /> {/* default */}
```

---

### visible
`boolean` — Default: `true`

Defines the visibility state of the Skeleton. Set to `false` to hide the skeleton when content has loaded.

```tsx
<SkeletonComponent height="15px" width="60%" visible={true} />
<SkeletonComponent height="15px" width="60%" visible={false} />
```

---

### width
`string | number` — Default: `""`

Defines the width of the Skeleton. Width is **required** for `"Circle"` and `"Square"` shapes (used as the sole dimension). Width is also required for `"Rectangle"`. Optional for `"Text"`.

```tsx
<SkeletonComponent shape="Circle" width="60px" />
<SkeletonComponent shape="Rectangle" width="100%" height="200px" />
<SkeletonComponent height="15px" width="75%" />
```

---

## Methods

### destroy()
`void`

Destroys the Skeleton component instance, removing event listeners and cleaning up internal state. Call when programmatically removing the component outside of React's lifecycle.

```tsx
import { SkeletonComponent } from '@syncfusion/ej2-react-notifications';
import * as React from 'react';

function App() {
  const skeletonRef = React.useRef<SkeletonComponent>(null);

  const handleDestroy = () => {
    skeletonRef.current?.destroy();
  };

  return (
    <div>
      <SkeletonComponent ref={skeletonRef} height="15px" width="80%" />
      <button onClick={handleDestroy}>Destroy</button>
    </div>
  );
}
export default App;
```

---

## Enums

### SkeletonType
Defines the `shape` prop values:

| Value | Description |
|---|---|
| `Text` | Horizontal line (default) |
| `Circle` | Circle/round shape |
| `Square` | Equal-sided square |
| `Rectangle` | Rectangular block |

### ShimmerEffect
Defines the `shimmerEffect` prop values:

| Value | Description |
|---|---|
| `Wave` | Left-to-right sweeping wave (default) |
| `Pulse` | Uniform fade in/out pulsing |
| `Fade` | Gradual fade animation |

---

## Usage Examples

### All properties combined
```tsx
<SkeletonComponent
  shape="Rectangle"
  width="100%"
  height="200px"
  shimmerEffect="Pulse"
  cssClass="my-card-skeleton"
  label="Loading featured image"
  visible={true}
  enableRtl={false}
  enablePersistence={false}
/>
```

### Minimal text skeleton
```tsx
<SkeletonComponent height="15px" />
```

### Circle with custom label
```tsx
<SkeletonComponent shape="Circle" width="48px" label="Loading profile photo" />
```

### Hidden skeleton (content loaded)
```tsx
<SkeletonComponent height="20px" width="50%" visible={false} />
```
