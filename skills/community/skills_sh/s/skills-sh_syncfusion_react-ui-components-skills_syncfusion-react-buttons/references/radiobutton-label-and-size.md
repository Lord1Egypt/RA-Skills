# Label and Size — Syncfusion React RadioButton

This guide covers configuring captions and size variants for the `RadioButtonComponent`.

---

## Label

Use the `label` property to add a caption next to the RadioButton. This avoids creating a separate HTML `<label>` element manually.

```tsx
import { RadioButtonComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  return <RadioButtonComponent label="Accept Terms" name="terms" />;
}
```

**Why use `label` instead of HTML `<label>`?**  
Syncfusion's `label` prop keeps the label and input properly associated internally, ensuring correct accessibility attributes (`aria-label`, `for`/`id` binding) without manual wiring.

---

## Label Position

Control whether the label appears **before** or **after** the RadioButton indicator using the `labelPosition` property.

| Value | Behavior |
|-------|----------|
| `'After'` (default) | Label appears to the **right** of the indicator |
| `'Before'` | Label appears to the **left** of the indicator |

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { RadioButtonComponent } from '@syncfusion/ej2-react-buttons';

enableRipple(true);

function App() {
  return (
    <ul>
      {/* Label on the left */}
      <li>
        <RadioButtonComponent
          label="Left Side Label"
          name="position"
          labelPosition="Before"
        />
      </li>

      {/* Label on the right (default) */}
      <li>
        <RadioButtonComponent
          label="Right Side Label"
          name="position"
          checked={true}
        />
      </li>
    </ul>
  );
}
export default App;
```

> **Tip:** Use `labelPosition="Before"` when building right-aligned option lists or custom form layouts.

---

## Size Variants

The RadioButton supports two sizes:

| Size | How to Apply | When to Use |
|------|-------------|-------------|
| **Default** | No extra class | Standard forms, cards |
| **Small** | `cssClass="e-small"` | Dense layouts, toolbars, compact tables |

### Default Size

```tsx
<RadioButtonComponent label="Default" name="size" />
```

### Small Size

Apply `e-small` via the `cssClass` property:

```tsx
<RadioButtonComponent label="Small" name="size" cssClass="e-small" />
```

### Comparison Example

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { RadioButtonComponent } from '@syncfusion/ej2-react-buttons';

enableRipple(true);

function App() {
  return (
    <ul>
      <li><RadioButtonComponent label="Small"   name="size" cssClass="e-small" /></li>
      <li><RadioButtonComponent label="Default" name="size" /></li>
    </ul>
  );
}
export default App;
```

---

## Combining Label Position and Size

```tsx
<RadioButtonComponent
  label="Compact Left Label"
  name="combo"
  labelPosition="Before"
  cssClass="e-small"
/>
```

---

## See Also

- [features-and-state.md](features-and-state.md) — checked, disabled, RTL
- [style-and-appearance.md](style-and-appearance.md) — full CSS customization
- [api.md](api.md) — `label`, `labelPosition`, `cssClass` API reference
