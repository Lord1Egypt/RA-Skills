# Skeleton Styles and Visibility

## Table of Contents
- [Custom CSS with cssClass](#custom-css-with-cssclass)
- [Visibility Control](#visibility-control)
- [Loading to Content Transition](#loading-to-content-transition)
- [CSS Customization Examples](#css-customization-examples)

---

## Custom CSS with cssClass

Use the `cssClass` prop to apply one or more CSS classes to a `SkeletonComponent`. This lets you override the default skeleton appearance — changing shimmer wave color, background color, dimensions, border radius, or animation speed.

```tsx
<SkeletonComponent shape="Circle" width="60px" cssClass="e-customize" />
```

Define the class in your CSS file:

```css
/* Example: custom purple shimmer wave */
.e-customize.e-skeleton {
  background-color: #e8d5f5;
}

.e-customize.e-skeleton::after {
  background: linear-gradient(
    90deg,
    transparent,
    rgba(150, 80, 200, 0.4),
    transparent
  );
}
```

Multiple classes are supported (space-separated):

```tsx
<SkeletonComponent height="15px" width="80%" cssClass="e-custom-bg e-custom-wave" />
```

---

## Visibility Control

Use the `visible` prop to show or hide the skeleton placeholder based on your application's loading state.

- `visible={true}` — Skeleton is displayed (default)
- `visible={false}` — Skeleton is hidden

```tsx
<SkeletonComponent height="15px" width="60%" visible={true} />
```

The `visible` prop enables dynamic toggling without mounting/unmounting the component. Set it to `false` when content has finished loading, then render your actual content.

---

## Loading to Content Transition

A common pattern is to conditionally render either the skeleton or the real content based on loading state:

```tsx
import { SkeletonComponent } from '@syncfusion/ej2-react-notifications';
import * as React from 'react';

function UserProfile() {
  const [loading, setLoading] = React.useState(true);
  const [user, setUser] = React.useState<{ name: string; role: string } | null>(null);

  React.useEffect(() => {
    // Simulate data fetch
    setTimeout(() => {
      setUser({ name: 'Jane Smith', role: 'Developer' });
      setLoading(false);
    }, 2000);
  }, []);

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', padding: '16px' }}>
      {loading ? (
        <>
          <SkeletonComponent shape="Circle" width="48px" />
          <div>
            <SkeletonComponent width="120px" height="15px" />
            <br />
            <SkeletonComponent width="80px" height="12px" />
          </div>
        </>
      ) : (
        <>
          <div style={{ width: '48px', height: '48px', borderRadius: '50%', background: '#6366f1' }} />
          <div>
            <strong>{user?.name}</strong>
            <p style={{ margin: 0, fontSize: '12px' }}>{user?.role}</p>
          </div>
        </>
      )}
    </div>
  );
}
export default UserProfile;
```

Alternatively, use the `visible` prop to hide the skeleton while keeping it in the DOM:

```tsx
import { SkeletonComponent } from '@syncfusion/ej2-react-notifications';
import * as React from 'react';

function FadingContent() {
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    setTimeout(() => setLoading(false), 1500);
  }, []);

  return (
    <div>
      <SkeletonComponent height="20px" width="200px" visible={loading} />
      {!loading && <h2>Content Loaded!</h2>}
    </div>
  );
}
export default FadingContent;
```

---

## CSS Customization Examples

### Change background color
```css
.my-skeleton.e-skeleton {
  background-color: #dbeafe; /* light blue */
}
```

### Change wave/shimmer color
```css
.my-skeleton.e-skeleton::after {
  background: linear-gradient(
    90deg,
    transparent,
    rgba(59, 130, 246, 0.5),
    transparent
  );
}
```

### Slow down animation
```css
.my-skeleton.e-skeleton::after {
  animation-duration: 2.5s;
}
```

### Rounded rectangle
```css
.rounded-skeleton.e-skeleton {
  border-radius: 8px;
}
```

Apply the class:
```tsx
<SkeletonComponent shape="Rectangle" width="100%" height="120px" cssClass="rounded-skeleton" />
```
