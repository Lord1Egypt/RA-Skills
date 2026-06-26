# Toast Positioning

## Table of Contents
- [Predefined Positions](#predefined-positions)
- [Custom Positions](#custom-positions)
- [Positioning Relative to a Target](#positioning-relative-to-a-target)
- [Multiple Toasts at Different Positions](#multiple-toasts-at-different-positions)

---

## Predefined Positions

Configure toast placement using the `position` property with `X` and `Y` string values:

```tsx
<ToastComponent
  ref={toast => toastInstance = toast!}
  title="Notification"
  content="Task completed successfully"
  position={{ X: 'Right', Y: 'Bottom' }}
  created={() => toastInstance.show()}
/>
```

**X values (horizontal):**
| Value | Placement |
|---|---|
| `'Left'` | Left edge of the screen/container |
| `'Center'` | Horizontally centered |
| `'Right'` | Right edge of the screen/container |

**Y values (vertical):**
| Value | Placement |
|---|---|
| `'Top'` | Top of the screen/container |
| `'Bottom'` | Bottom of the screen/container |

**Common combinations:**

| Position | X | Y |
|---|---|---|
| Top-Left | `'Left'` | `'Top'` |
| Top-Center | `'Center'` | `'Top'` |
| Top-Right | `'Right'` | `'Top'` |
| Bottom-Left | `'Left'` | `'Bottom'` |
| Bottom-Center | `'Center'` | `'Bottom'` |
| Bottom-Right (default-like) | `'Right'` | `'Bottom'` |

> **Note:** When multiple toasts are visible, position changes only apply to newly displayed toasts. Existing toasts retain their original positions. If `width="100%"`, the `X` position value has no effect.

---

## Custom Positions

For non-standard layouts, specify exact numeric or percentage coordinates:

```tsx
// Numeric values are treated as pixels
<ToastComponent
  ref={toast => toastInstance = toast!}
  title="Custom Positioned Toast"
  content="Pinned at 100px from left, 50px from top"
  position={{ X: 100, Y: 50 }}
  created={() => toastInstance.show()}
/>
```

```tsx
// Percentage values relative to the container
<ToastComponent
  ref={toast => toastInstance = toast!}
  title="Centered Custom Toast"
  content="At 40% from left, 80% from top"
  position={{ X: '40%', Y: '80%' }}
  created={() => toastInstance.show()}
/>
```

Numeric values are interpreted as pixels. Percentage values are calculated relative to the target container (or viewport when no target is set).

---

## Positioning Relative to a Target

When `target` is set, position is calculated relative to the target element rather than the viewport:

```tsx
function App() {
  let toastInstance: ToastComponent;

  return (
    <div id="toast_pos_target" style={{ position: 'relative', height: '400px' }}>
      <button onClick={() => toastInstance.show()}>Show Toast</button>
      <ToastComponent
        ref={toast => toastInstance = toast!}
        title="Panel Notification"
        content="This toast is inside the panel"
        target="#toast_pos_target"
        position={{ X: 'Right', Y: 'Bottom' }}
        created={() => toastInstance.show()}
      />
    </div>
  );
}
```

---

## Multiple Toasts at Different Positions

To show toasts simultaneously at different screen positions, create multiple `ToastComponent` instances — each with its own position configuration. A single instance can only occupy one position at a time:

```tsx
function App() {
  let toastBottom: ToastComponent;
  let toastTop: ToastComponent;

  function showBoth(): void {
    toastBottom.show();
    toastTop.show();
  }

  function onClick(e: ToastClickEventArgs): void {
    e.clickToClose = true;
  }

  return (
    <div>
      <button onClick={showBoth}>Show Both</button>

      {/* Bottom-right toast */}
      <ToastComponent
        ref={toast => toastBottom = toast!}
        title="Warning!"
        content="There was a problem with your network connection."
        position={{ X: 'Right', Y: 'Bottom' }}
        click={onClick}
      />

      {/* Top-right toast */}
      <ToastComponent
        ref={toast => toastTop = toast!}
        title="Info"
        content="Please check your inbox."
        position={{ X: 'Right', Y: 'Top' }}
        click={onClick}
      />
    </div>
  );
}
```

**When to use multiple instances:**
- Show success (top-right) and error (bottom-right) simultaneously
- Different message types that should not compete for the same screen area
- Separate auto-dismiss timers per location

## See Also

- [Configuration options](./configuration.md)
- [Multiple toasts how-to](./toast-services.md)
