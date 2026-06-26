# Chip Style Customization

## Table of Contents
- [Overview](#overview)
- [Chip Text Styling](#chip-text-styling)
- [Chip Icon Styling](#chip-icon-styling)
- [Chip Delete Button Styling](#chip-delete-button-styling)
- [Outline Chip Border Styling](#outline-chip-border-styling)
- [Chip Selection Styling](#chip-selection-styling)
- [Avatar Text Styling](#avatar-text-styling)
- [Chip Height / Size Customization](#chip-height--size-customization)
- [CSS Class Hierarchy](#css-class-hierarchy)

---

## Overview

Syncfusion Chips expose a set of CSS classes that you can override to customize appearance without modifying component internals. All customizations follow the pattern:

1. Define your CSS rule targeting the chip's specific CSS class.
2. Place overrides in your component's CSS file or a global stylesheet.
3. Avoid using `!important` unless overriding vendor specificity.

---

## Chip Text Styling

Customize the chip label's font size, color, and weight:

```css
.e-chip .e-chip-text {
  font-size: 14px;
  color: #333333;
  font-weight: 600;
}
```

- `.e-chip-text` — targets the text label inside every chip.

**Example: Larger, bold chip labels**
```css
.e-chip .e-chip-text {
  font-size: 16px;
  color: #1a1a2e;
  font-weight: bold;
}
```

---

## Chip Icon Styling

Customize the icon inside a chip (used with `leadingIconCss` or `avatarIconCss`):

```css
.e-chip .e-icon {
  background-image: url('https://example.com/images/avatar.png');
  opacity: 0.8;
}
```

- `.e-icon` — targets the icon element inside the chip.
- Set `background-image` for image-based icons.
- Adjust `opacity`, `width`, `height` as needed.

**Per-chip icon styling:**
```css
.e-chip .andrew {
  background-image: url('/images/andrew.png');
  background-size: cover;
  border-radius: 50%;
}

.e-chip .janet {
  background-image: url('/images/janet.png');
  background-size: cover;
  border-radius: 50%;
}
```

---

## Chip Delete Button Styling

Customize the appearance of the delete (×) button shown when `enableDelete={true}`:

```css
.e-chip-list .e-chip .e-chip-delete.e-dlt-btn {
  color: #e3165b;
  font-size: 12px;
}
```

- `.e-chip-delete.e-dlt-btn` — targets the delete button element.
- Adjust `color` and `font-size` to match your design.

**Hover state for delete button:**
```css
.e-chip-list .e-chip .e-chip-delete.e-dlt-btn:hover {
  color: #b0003a;
  cursor: pointer;
}
```

---

## Outline Chip Border Styling

Customize the border of outline chips (chips with `cssClass="e-outline"`):

```css
.e-chip-list .e-chip.e-outline {
  border-color: #e3165b;
  border-width: 2px;
  border-style: solid;
}
```

- `.e-chip.e-outline` — targets chips that use the outline variant.
- Modify `border-color`, `border-width`, and `border-style` freely.

---

## Chip Selection Styling

Customize the appearance of chips when they are selected (active state):

```css
/* Single selection — active chip */
.e-chip-list.e-selection .e-chip.e-active {
  background-color: #ffca1c;
  color: #e3165b;
}

/* Multiple selection — active chips */
.e-chip-list .e-chip.e-active {
  background-color: #e3165b;
  color: #ffffff;
}
```

- `.e-chip.e-active` — applied to chips in the selected state.
- `.e-chip-list.e-selection` — scopes rules to chip lists with `selection="Single"`.
- Use high-contrast colors to ensure WCAG compliance.

**Example: Custom teal selection**
```css
.e-chip-list .e-chip.e-active {
  background-color: #00796b;
  color: #ffffff;
}
```

---

## Avatar Text Styling

Customize the circular avatar area that shows text (used with `avatarText`):

```css
.e-chip-list .e-chip .e-chip-avatar {
  background-color: #d51a1a;
  color: #fafafa;
}
```

- `.e-chip-avatar` — targets the avatar container element.
- Set `background-color` for the avatar circle color and `color` for the text inside it.

**Example: Blue avatar for initials**
```css
.e-chip-list .e-chip .e-chip-avatar {
  background-color: #1565c0;
  color: #ffffff;
  font-weight: bold;
}
```

---

## Chip Height / Size Customization

Override the chip height to match your design system's scale:

```css
/* Larger chips */
.e-chip-list.e-chip {
  height: 40px;
}

/* Smaller chips */
.e-chip-list .e-chip {
  height: 24px;
  font-size: 11px;
  padding: 0 8px;
}
```

- Adjust `height`, `padding`, and `font-size` together for consistent scaling.
- Ensure the avatar/icon sizes also scale proportionally:

```css
.e-chip-list .e-chip .e-chip-avatar {
  width: 24px;
  height: 24px;
  font-size: 10px;
}
```

---

## CSS Class Hierarchy

Quick reference of CSS classes used by the Chips component:

| CSS Class | Element |
|-----------|---------|
| `.e-chip-list` | The `ChipListComponent` wrapper element |
| `.e-chip` | Individual chip element |
| `.e-chip-text` | The text label inside a chip |
| `.e-chip-avatar` | The avatar container (for `avatarText` / `avatarIconCss`) |
| `.e-icon` | The icon element (for `leadingIconCss` / `avatarIconCss`) |
| `.e-chip-delete` | The delete button element |
| `.e-dlt-btn` | Delete button icon class |
| `.e-outline` | Applied to chip when using outline variant |
| `.e-active` | Applied to chip when selected |
| `.e-selection` | Applied to `ChipListComponent` when `selection` is set |
| `.e-disabled` | Applied to chip when disabled |
