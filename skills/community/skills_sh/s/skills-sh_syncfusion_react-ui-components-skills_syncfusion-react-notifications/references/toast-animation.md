# Toast Animation

Configure how toasts animate into and out of view using the `animation` property. Animations improve visual feedback and draw user attention to notifications.

## Animation Property Structure

```tsx
animation: {
  show: { effect: 'FadeIn', duration: 600, easing: 'linear' },
  hide: { effect: 'FadeOut', duration: 600, easing: 'linear' }
}
```

**Defaults:** `show.effect = 'FadeIn'`, `hide.effect = 'FadeOut'`, duration 600ms, easing linear.

---

## Basic Example

```tsx
import { Effect } from '@syncfusion/ej2-base';
import { ToastComponent } from '@syncfusion/ej2-react-notifications';

function App() {
  let toastInstance: ToastComponent;

  const animation = {
    show: { effect: 'SlideRightIn' as Effect },
    hide: { effect: 'SlideLeftOut' as Effect }
  };

  return (
    <div>
      <button onClick={() => toastInstance.show()}>Show Toast</button>
      <ToastComponent
        ref={toast => toastInstance = toast!}
        title="Animated Toast"
        content="Slides in from the right"
        position={{ X: 'Right', Y: 'Bottom' }}
        animation={animation}
        showProgressBar={true}
        created={() => toastInstance.show()}
      />
    </div>
  );
}
```

Import `Effect` from `@syncfusion/ej2-base` for TypeScript type safety when specifying animation effects.

---

## Available Effects

These effect names can be used for both `show` and `hide` animation settings:

| Effect | Description |
|---|---|
| `FadeIn` / `FadeOut` | Opacity transition (default) |
| `FadeZoomIn` / `FadeZoomOut` | Fade combined with scale |
| `FlipLeftDownIn` / `FlipLeftDownOut` | 3D flip from left downward |
| `FlipLeftUpIn` / `FlipLeftUpOut` | 3D flip from left upward |
| `FlipRightDownIn` / `FlipRightDownOut` | 3D flip from right downward |
| `FlipRightUpIn` / `FlipRightUpOut` | 3D flip from right upward |
| `SlideBottomIn` / `SlideBottomOut` | Slides from bottom |
| `SlideRightIn` / `SlideLeftOut` | Slides from right / exits left |
| `ZoomIn` / `ZoomOut` | Scale transform |

> Not all Effects are directional pairs — mix show and hide effects freely based on desired UX (e.g., `SlideBottomIn` show with `FadeOut` hide).

---

## Changing Animation Dynamically

Update animation effects at runtime by directly mutating the component's `animation` property:

```tsx
// Change show effect
toastInstance.animation.show = { effect: 'ZoomIn' as Effect };

// Change hide effect
toastInstance.animation.hide = { effect: 'ZoomOut' as Effect };
```

This is useful when you want different animations for different toast types.

---

## Controlling Duration and Easing

```tsx
const animation = {
  show: { effect: 'FadeIn' as Effect, duration: 300, easing: 'ease-out' },
  hide: { effect: 'FadeOut' as Effect, duration: 800, easing: 'ease-in' }
};
```

- `duration` — milliseconds for the animation to complete
- `easing` — CSS easing function (`'linear'`, `'ease'`, `'ease-in'`, `'ease-out'`, `'ease-in-out'`)

---

## Accessibility Note

Users who have set `prefers-reduced-motion` in their OS may experience issues with heavy animations. Consider reducing or disabling animations for these users:

```css
@media (prefers-reduced-motion: reduce) {
  .e-toast-container .e-toast {
    animation: none !important;
    transition: none !important;
  }
}
```

## See Also

- [API reference](./api.md) — `animation` property
- [Getting started](./getting-started.md)
