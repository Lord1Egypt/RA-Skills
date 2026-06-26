# Customization — Syncfusion React Tooltip

## Table of Contents
- [cssClass Property](#cssclass-property)
- [Tip Pointer Customization](#tip-pointer-customization)
- [Full Tooltip Styling](#full-tooltip-styling)
- [Curved Tip Arrow](#curved-tip-arrow)
- [Bubble Tip Arrow](#bubble-tip-arrow)
- [Dimensions (Width and Height)](#dimensions-width-and-height)
- [Scroll Mode](#scroll-mode)
- [RTL Support](#rtl-support)

---

## cssClass Property

Use `cssClass` to attach one or more custom CSS class names to the tooltip popup element. All visual overrides go through this prop:

```tsx
<TooltipComponent content="Custom styled tooltip" cssClass="my-tooltip">
  <button className="e-btn">Hover</button>
</TooltipComponent>
```

```css
/* Target the tooltip popup container */
.my-tooltip.e-tooltip-wrap {
  background: #333;
  border-color: #333;
  color: #fff;
  border-radius: 4px;
  font-size: 13px;
}
/* Arrow fill */
.my-tooltip.e-tooltip-wrap .e-arrow-tip-outer {
  border-top-color: #333;
}
.my-tooltip.e-tooltip-wrap .e-arrow-tip-inner {
  border-top-color: #333;
}
```

---

## Tip Pointer Customization

Override tip pointer size and color via CSS on the arrow elements:

```tsx
<TooltipComponent content="Custom arrow" cssClass="customtip">
  <div id="target">Show Tooltip</div>
</TooltipComponent>
```

```css
.customtip.e-tooltip-wrap .e-arrow-tip-outer.e-tip-bottom,
.customtip.e-tooltip-wrap .e-arrow-tip-outer.e-tip-top {
  border-left-width: 8px;
  border-right-width: 8px;
  border-top-width: 12px;
}
.customtip.e-tooltip-wrap .e-arrow-tip-inner.e-tip-bottom,
.customtip.e-tooltip-wrap .e-arrow-tip-inner.e-tip-top {
  border-left-width: 7px;
  border-right-width: 7px;
  border-top-width: 11px;
}
```

> Tip pointer directions: `.e-tip-top`, `.e-tip-bottom`, `.e-tip-left`, `.e-tip-right` — apply overrides only to the relevant direction for your `position` setting.

---

## Full Tooltip Styling

Customize the complete tooltip appearance:

```tsx
<TooltipComponent content="Customized tooltip" cssClass="customtooltip">
  <div id="target">Show Tooltip</div>
</TooltipComponent>
```

```css
.customtooltip.e-tooltip-wrap .e-tip-content {
  background-color: #fafafa;
  color: #333;
  font-size: 14px;
  font-family: 'Segoe UI', sans-serif;
  line-height: 1.5;
  padding: 8px 12px;
}
.customtooltip.e-tooltip-wrap {
  background-color: #fafafa;
  border: 1px solid #ccc;
  border-radius: 6px;
  opacity: 0.95;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}
```

---

## Curved Tip Arrow

Achieve a curved (CSS3 transformed) tip arrow by overriding the `.e-arrow-tip` classes:

```tsx
<TooltipComponent content="Curved tip" cssClass="curvetips e-tooltip-css" target="#target">
  <button className="e-btn" id="target">Curved Tip Arrow</button>
</TooltipComponent>
```

```css
.curvetips.e-tooltip-wrap .e-arrow-tip-outer.e-tip-bottom,
.curvetips.e-tooltip-wrap .e-arrow-tip-outer.e-tip-top {
  border-left: none !important;
  border-right: none !important;
  border-top: none !important;
}
.curvetips.e-tooltip-wrap .e-arrow-tip.e-tip-top {
  transform: rotate(170deg);
}
```

> Curved tips work best with `position="TopCenter"` or `position="BottomLeft"`.

---

## Bubble Tip Arrow

Create a rounded bubble/balloon effect by styling both inner and outer arrow elements as circles:

```tsx
<TooltipComponent
  content="Bubble tip"
  cssClass="bubbletip e-tooltip-css"
  target="#bubbletip"
  position="TopRight"
>
  <button className="e-btn" id="bubbletip">Bubble Tip Arrow</button>
</TooltipComponent>
```

```css
.bubbletip.e-tooltip-wrap .e-arrow-tip-outer.e-tip-bottom,
.bubbletip.e-tooltip-wrap .e-arrow-tip-outer.e-tip-top {
  border-radius: 50px;
  height: 10px;
  width: 10px;
}
.bubbletip.e-tooltip-wrap .e-arrow-tip-inner.e-tip-bottom,
.bubbletip.e-tooltip-wrap .e-arrow-tip-inner.e-tip-top {
  border-radius: 50px;
  height: 10px;
  width: 10px;
}
```

> Use `offsetY` to adjust the tooltip position when the bubble tip changes the visual gap between tooltip and target.

---

## Dimensions (Width and Height)

Control tooltip size with `width` and `height` (string or number, default `'auto'`):

```tsx
{/* Fixed size */}
<TooltipComponent width="180px" height="40px" content="Fixed size tooltip">
  <div id="target">Show Tooltip</div>
</TooltipComponent>

{/* Numeric values (treated as px) */}
<TooltipComponent width={250} height={80} content="Numeric dimensions">
  <div id="target">Show Tooltip</div>
</TooltipComponent>
```

> When `width="auto"` (default), the tooltip auto-adjusts to fit its content within the viewport.

---

## Scroll Mode

When `height` is fixed and content overflows, the tooltip enables a scrollbar automatically:

```tsx
function longContent() {
  return (
    <span>
      <p>
        <strong>Environmentally friendly</strong> or <strong>environment-friendly</strong>,
        (also referred to as eco-friendly, nature-friendly, and green) are marketing
        and sustainability terms referring to goods and services, laws, guidelines and
        policies that inflict reduced, minimal, or no harm upon ecosystems or the environment.
      </p>
    </span>
  );
}

<TooltipComponent
  width="300px"
  height="60px"
  isSticky={true}
  content={longContent}
  style={{ display: 'inline-block', padding: '5px' }}
>
  <a><u>environmentally friendly</u></a>
</TooltipComponent>
```

> Sticky mode (`isSticky={true}`) is recommended when scroll mode is needed, so the user can scroll without the tooltip closing.

---

## RTL Support

Enable right-to-left rendering for Arabic, Hebrew, and other RTL languages:

```tsx
<TooltipComponent
  content="نص تلميح"
  enableRtl={true}
  position="TopCenter"
>
  <button className="e-btn">عرض التلميح</button>
</TooltipComponent>
```

---

## See Also
- [Position](position.md) — `showTipPointer`, `tipPointerPosition`
- [Animation](animation.md) — using `showTipPointer={false}` with flip effects
- [API Reference](api.md) — `cssClass`, `width`, `height`, `enableRtl`
