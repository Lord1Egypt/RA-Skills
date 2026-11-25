---

name: tailwind-rails
description: "Tailwind CSS component patterns for Ruby on Rails ERB views. Use when building UI components in Rails, creating shared partials, implementing dark mode, writing badge/button/card/table components, setting up a consistent design system, or checking Tailwind markup for contrast and accessibility problems. Trigger phrases: tailwind rails, rails UI components, ERB tailwind, rails dark mode, tailwind badge, tailwind button rails, shared partials tailwind, tailwind hidden class, tailwind contrast."
metadata: {"clawdbot":{"emoji":"\ud83c\udfa8","requires":{"bins":[]},"os":["linux","darwin","win32"],"version":"1.0.4"}}
---


# Tailwind CSS for Rails

Build consistent, dark-mode-ready component patterns in Rails ERB views using Tailwind utilities and reusable partials.

## Quick Start

Add a class name helper to collapse conditional logic:

```ruby
# app/helpers/application_helper.rb
def cn(*classes)
  classes.flatten.compact.join(' ').split.uniq.join(' ')
end
```

Use it in views to combine base and conditional classes:

```erb
<div class="<%= cn('px-4', active ? 'bg-blue-500' : 'bg-gray-200') %>">
  Content
</div>
```

Standard full-width container with responsive padding:

```erb
<div class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
  <!-- Page content -->
</div>
```

## Badge Pattern

```erb
<span class="inline-flex items-center rounded-full bg-green-100 px-3 py-1 text-sm font-medium text-green-800 dark:bg-green-900 dark:text-green-100">
  Label
</span>
```

**Colors:** Yellow=warning, Blue=info, Green=success, Red=danger, Gray=neutral  
Light: `bg-{color}-100` + `text-{color}-800` | Dark: `dark:bg-{color}-900` + `dark:text-{color}-100`

## Common Components

**Card with border and shadow:**

```erb
<div class="rounded-lg border border-gray-200 bg-white shadow-sm dark:border-gray-800 dark:bg-gray-950">
  <div class="px-6 py-4">
    <!-- content -->
  </div>
</div>
```

**Table wrapper with responsive shadow:**

```erb
<div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
  <table class="w-full divide-y divide-gray-200">
    <thead>...</thead>
    <tbody>...</tbody>
  </table>
</div>
```

**Tab navigation with underline:**

```erb
<nav class="flex space-x-8 border-b border-gray-300">
  <% tabs.each do |tab| %>
    <% active = current_tab == tab %>
    <%= link_to tab_path(tab),
        class: "py-2 px-1 border-b-2 font-medium text-sm #{active ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-600 hover:text-gray-700'}" do %>
      <%= tab.humanize %>
    <% end %>
  <% end %>
</nav>
```

## Best Practices

1. **Use the `cn()` helper** for all conditional class logic — it deduplicates and removes blanks.
2. **Pair light and dark classes always** — `bg-white dark:bg-gray-950`, `text-gray-900 dark:text-gray-100`.
3. **Mobile-first responsive design** — use `sm:`, `md:`, `lg:` prefixes for breakpoints.
4. **Extract repeated patterns into partials** — `_badge.html.erb`, `_button.html.erb`, `_card.html.erb`.
5. **Use semantic color names** — yellow for warnings, green for success, red for errors.
6. **Ensure sufficient contrast** in both light and dark modes.
7. **Test accessibility** with screen readers and keyboard navigation.

## Accessibility

### The Tailwind `hidden` class vs the HTML `hidden` attribute

These are **different mechanisms** and they interact in ways that surprise people.

| | Tailwind class | HTML attribute |
|---|---|---|
| Syntax | `class="hidden"` | `<div hidden>` |
| Mechanism | `display: none` via CSS | `display: none` via the UA stylesheet |
| Overridable by CSS? | **Yes** - any later `display:` rule wins | **No** - needs `[hidden] { display: none !important }` to beat |
| Hidden from screen readers? | Yes | Yes |
| Removed from tab order? | Yes | Yes |

**The trap:** the HTML `hidden` attribute has a *lower* specificity than almost any
Tailwind utility. A Tailwind class like `flex` or `block` on the same element
overrides it, and the element stays visible while the author believes it is hidden.

```erb
<%# BAD - the `flex` utility overrides the `hidden` attribute, element stays visible %>
<div hidden class="flex">
```

```erb
<%# GOOD - use the Tailwind class so the intent is explicit and wins by specificity %>
<div class="hidden">
```

**Rule:** pick one mechanism per element. If you use Tailwind for visibility
(`hidden`, `md:hidden`, `block`), do not also add the `hidden` attribute.

**Responsive visibility is CSS-only.** `hidden md:block` hides at small widths and
shows at `md+`. The element is never removed from the DOM, so assistive tech sees
it at all widths - it is only visually hidden. For content that must be removed
from the accessibility tree entirely (not just visually), remove the element from
the DOM server-side.

### Contrast is measured against the real background

A color pair that passes on white can fail on the actual container. Contrast is
computed between the **text color and the nearest painted background behind it** -
not against the page background.

```erb
<%# BAD - text-gray-400 on a gray-100 badge passes against white, fails on gray-100 %>
<span class="bg-gray-100 text-gray-400">
```

```erb
<%# GOOD - compute against the container that actually paints behind the text %>
<span class="bg-gray-100 text-gray-800">
```

WCAG AA thresholds:

| Text size | Minimum ratio |
|---|---|
| Normal (< 18px, or < 14px bold) | **4.5:1** |
| Large (>= 18px, or >= 14px bold) | **3:1** |
| UI components & focus indicators | **3:1** |

Common traps:

- **Disabled states.** `text-gray-400` on `bg-gray-50` is usually around 2.8:1.
  Disabled controls are exempt from WCAG contrast requirements - but "disabled"
  must be conveyed by more than color alone.
- **Placeholder text.** Placeholders are still text and need contrast. Browsers
  default them to low opacity.
- **Dark mode.** Every `text-*` needs a `dark:text-*` counterpart, and the ratio
  must hold in **both** modes. A pair that passes in light mode can fail in dark.
- **Text over images/gradients.** The background varies, so the ratio varies.
  Use a scrim or a solid backing behind the text.
- **Semantic color tokens.** `oklch()` colors with high chroma saturate and fail
  more often than the equivalent hex. Chroma above roughly 0.04 on light
  backgrounds is a reliable failure.

### Focus indicators must survive

Tailwind's preflight removes the browser's default outline. If you do not replace
it, keyboard users lose focus entirely.

```erb
<%# BAD - outline removed, nothing replaces it %>
<a class="focus:outline-none">
```

```erb
<%# GOOD - always pair outline-none with a visible ring %>
<a class="focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2">
```

Use `focus-visible` rather than `focus` so mouse clicks do not show the ring, but
keyboard navigation always does.

### Never hide content from screen readers with `display: none`

`hidden` (the class or the attribute) removes content from the accessibility tree
**and** from the tab order. If the content is still meaningful - for example a
label that is visually superseded by an icon - use `sr-only` instead:

```erb
<%# GOOD - visible to screen readers, invisible on screen %>
<button class="p-2">
  <%= render "icon", name: "trash" %>
  <span class="sr-only">Delete item</span>
</button>
```

### Icon-only buttons need an accessible name

```erb
<%# BAD - no accessible name %>
<button><svg ...></svg></button>

<%# GOOD %>
<button aria-label="Delete item">
  <svg aria-hidden="true" ...></svg>
</button>
```

Decorative SVGs need `aria-hidden="true"` so the screen reader does not announce
raw path data.

## References

- `references/components.md` — Reusable badge, button, and card partials with usage examples.
- `references/dark-mode-responsive.md` — Dark mode setup, responsive patterns, and animation utilities.
