---
name: tailwind-rails
description: "Tailwind CSS component patterns for Ruby on Rails ERB views. Use when building UI components in Rails, creating shared partials, implementing dark mode, writing badge/button/card/table components, or setting up a consistent design system. Trigger phrases: tailwind rails, rails UI components, ERB tailwind, rails dark mode, tailwind badge, tailwind button rails, shared partials tailwind."
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
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

## References

- `references/components.md` — Reusable badge, button, and card partials with usage examples.
- `references/dark-mode-responsive.md` — Dark mode setup, responsive patterns, and animation utilities.
