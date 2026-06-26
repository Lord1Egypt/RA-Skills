# Skeleton Shapes

## Table of Contents
- [Overview](#overview)
- [Available Shapes](#available-shapes)
- [Dimension Rules by Shape](#dimension-rules-by-shape)
- [Shape Examples](#shape-examples)
- [Multi-Shape Card Layout](#multi-shape-card-layout)
- [Choosing the Right Shape](#choosing-the-right-shape)

---

## Overview

Use the `shape` prop on `SkeletonComponent` to select the visual form of the loading placeholder. Each shape is designed to mirror a specific type of real content, helping users understand what is loading.

```tsx
<SkeletonComponent shape="Circle" width="60px" />
```

Default shape is `"Text"` when `shape` is omitted.

---

## Available Shapes

### Text (default)
Horizontal line representing a text row or headline. Use for paragraphs, titles, labels.

```tsx
<SkeletonComponent height="15px" width="70%" />
```

### Circle
Round placeholder for avatars, profile photos, or circular icons.

```tsx
<SkeletonComponent shape="Circle" width="60px" />
```

### Square
Equal-sided placeholder for compact icons, thumbnails, or grid tiles.

```tsx
<SkeletonComponent shape="Square" width="40px" />
```

### Rectangle
Rectangular placeholder for images, cards, banners, or large content blocks.

```tsx
<SkeletonComponent shape="Rectangle" width="100%" height="150px" />
```

---

## Dimension Rules by Shape

| Shape | Width | Height | Notes |
|-------|-------|--------|-------|
| `Text` | Optional | **Required** | Height controls line thickness |
| `Rectangle` | **Required** | **Required** | Both dimensions define the block |
| `Circle` | **Required** | Not needed | `width` is used as diameter |
| `Square` | **Required** | Not needed | `width` is used as side length |

> Height is ignored for `Circle` and `Square`; `width` alone determines their size.

---

## Shape Examples

### Circle — Avatar
```tsx
<SkeletonComponent shape="Circle" width="60px" />
```

### Square — Icon tile
```tsx
<SkeletonComponent shape="Square" width="40px" />
```

### Rectangle — Banner image
```tsx
<SkeletonComponent shape="Rectangle" width="100%" height="200px" />
```

### Text — Headline
```tsx
<SkeletonComponent height="20px" width="50%" />
```

### Text — Body paragraph lines
```tsx
<>
  <SkeletonComponent height="14px" width="100%" />
  <br />
  <SkeletonComponent height="14px" width="95%" />
  <br />
  <SkeletonComponent height="14px" width="80%" />
</>
```

---

## Multi-Shape Card Layout

Combine shapes to build a full card skeleton that mirrors real card content:

```tsx
import { SkeletonComponent } from '@syncfusion/ej2-react-notifications';
import * as React from 'react';

function CardSkeleton() {
  return (
    <div style={{ padding: '16px', maxWidth: '320px' }}>
      {/* Profile row */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
        <SkeletonComponent shape="Circle" width="60px" />
        <div style={{ flex: 1 }}>
          <SkeletonComponent width="30%" height="15px" />
          <br />
          <SkeletonComponent width="15%" height="15px" />
        </div>
      </div>

      {/* Image placeholder */}
      <SkeletonComponent shape="Rectangle" width="100%" height="150px" />

      {/* Action buttons row */}
      <div style={{ display: 'flex', gap: '8px', marginTop: '12px' }}>
        <SkeletonComponent shape="Rectangle" width="20%" height="32px" />
        <SkeletonComponent shape="Rectangle" width="20%" height="32px" />
      </div>
    </div>
  );
}
export default CardSkeleton;
```

---

## Choosing the Right Shape

| Content type | Recommended shape |
|---|---|
| Avatar / profile photo | `Circle` |
| Icon / badge | `Square` |
| Image / banner / card | `Rectangle` |
| Text line / heading | `Text` (default) |
| Button | `Rectangle` with small height |
| Paragraph block | Multiple `Text` lines stacked |
