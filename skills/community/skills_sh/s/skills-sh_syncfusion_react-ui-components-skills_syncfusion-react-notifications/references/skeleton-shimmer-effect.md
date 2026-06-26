# Skeleton Shimmer Effects

## Table of Contents
- [Overview](#overview)
- [Effect Types](#effect-types)
- [Usage](#usage)
- [Examples](#examples)
- [Choosing an Effect](#choosing-an-effect)

---

## Overview

Shimmer effects provide animated visual feedback that signals to users the application is actively loading content. Configure the animation style with the `shimmerEffect` prop.

```tsx
<SkeletonComponent shape="Circle" width="48px" shimmerEffect="Pulse" />
```

Default effect is `"Wave"` when `shimmerEffect` is omitted.

---

## Effect Types

### Wave (default)
A flowing highlight sweeps across the skeleton from left to right, mimicking a scan or reflection. Best for most general-purpose loading states.

```tsx
<SkeletonComponent height="15px" width="100%" shimmerEffect="Wave" />
```

### Pulse
The entire skeleton fades in and out uniformly, creating a breathing or pulsing rhythm. Works well for lists and items where you want a subtler, less directional animation.

```tsx
<SkeletonComponent height="15px" width="100%" shimmerEffect="Pulse" />
```

### Fade
A gradual fade in/out animation. Provides the most subtle visual feedback; appropriate when you want a calm, non-distracting loading state.

```tsx
<SkeletonComponent height="15px" width="100%" shimmerEffect="Fade" />
```

---

## Usage

Apply `shimmerEffect` directly on any `SkeletonComponent`. All skeletons in a layout can share the same effect or use different ones:

```tsx
import { SkeletonComponent } from '@syncfusion/ej2-react-notifications';
import * as React from 'react';

function EffectDemo() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
      <SkeletonComponent height="15px" width="100%" shimmerEffect="Wave" />
      <SkeletonComponent height="15px" width="80%" shimmerEffect="Pulse" />
      <SkeletonComponent height="15px" width="60%" shimmerEffect="Fade" />
    </div>
  );
}
export default EffectDemo;
```

---

## Examples

### List Skeleton with Pulse
Pulse is ideal for list items where the whole row fades together:

```tsx
import { SkeletonComponent } from '@syncfusion/ej2-react-notifications';
import * as React from 'react';

function ListSkeleton() {
  return (
    <ul style={{ listStyle: 'none', padding: 0 }}>
      {[1, 2, 3].map((i) => (
        <li key={i} style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '14px' }}>
          <SkeletonComponent shape="Circle" width="40px" shimmerEffect="Pulse" />
          <div style={{ flex: 1 }}>
            <SkeletonComponent width="60%" height="15px" shimmerEffect="Pulse" />
            <br />
            <SkeletonComponent width="40%" height="15px" shimmerEffect="Pulse" />
          </div>
        </li>
      ))}
    </ul>
  );
}
export default ListSkeleton;
```

### Card Skeleton with Wave (default)
```tsx
import { SkeletonComponent } from '@syncfusion/ej2-react-notifications';
import * as React from 'react';

function CardSkeleton() {
  return (
    <div style={{ padding: '16px' }}>
      <SkeletonComponent shape="Rectangle" width="100%" height="180px" />
      <br />
      <SkeletonComponent height="18px" width="60%" />
      <br />
      <SkeletonComponent height="14px" width="90%" />
      <br />
      <SkeletonComponent height="14px" width="75%" />
    </div>
  );
}
export default CardSkeleton;
```

### Fade Effect for Subtle Transitions
```tsx
import { SkeletonComponent } from '@syncfusion/ej2-react-notifications';
import * as React from 'react';

function SubtleSkeleton() {
  return (
    <div>
      <SkeletonComponent shape="Circle" width="56px" shimmerEffect="Fade" />
      <br />
      <SkeletonComponent height="16px" width="50%" shimmerEffect="Fade" />
    </div>
  );
}
export default SubtleSkeleton;
```

---

## Choosing an Effect

| Effect | Best for | Visual style |
|--------|----------|-------------|
| `Wave` | General use, cards, images | Directional left-to-right sweep |
| `Pulse` | Lists, repeated items | Uniform in/out breathing |
| `Fade` | Subtle or low-distraction UI | Soft, non-directional fade |

> All three effects respect the `prefers-reduced-motion` media query for users who prefer reduced animation.
