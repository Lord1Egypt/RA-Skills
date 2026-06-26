# Dark Mode & Responsive Patterns

Setup, utilities, and best practices for Tailwind in Rails applications.

## Dark Mode Setup

**tailwind.config.js**

```javascript
module.exports = {
  darkMode: 'class',
  theme: {
    extend: {},
  },
  plugins: [],
}
```

The `class` strategy means the `dark` class on the root `<html>` element controls dark mode.

**app/views/layouts/application.html.erb**

```erb
<!DOCTYPE html>
<html class="<%= current_user&.dark_mode? ? 'dark' : '' %>">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <%= csrf_meta_tags %>
    <%= csp_meta_tag %>
    <%= stylesheet_link_tag 'application', 'data-turbo-track': 'reload' %>
  </head>
  <body>
    <%= yield %>
  </body>
</html>
```

Toggle dark mode by setting a user preference, then updating the `<html>` class on the next page load or via JavaScript:

```javascript
// Toggle dark mode
document.documentElement.classList.toggle('dark');
localStorage.setItem('darkMode', document.documentElement.classList.contains('dark'));
```

On page load, restore the preference:

```javascript
if (localStorage.getItem('darkMode') === 'true') {
  document.documentElement.classList.add('dark');
}
```

## Color Pairing Rules

Always pair light and dark mode colors. Use these standard patterns:

**Text colors:**
```text
Light: text-gray-900
Dark:  dark:text-gray-100
```

**Backgrounds:**
```text
Light: bg-white
Dark:  dark:bg-gray-950
```

**Cards and containers:**
```text
Light: bg-white border-gray-200
Dark:  dark:bg-gray-900 dark:border-gray-800
```

**Hover states:**
```text
Light: hover:bg-gray-100
Dark:  dark:hover:bg-gray-800
```

**Examples:**

```erb
<!-- Paragraph -->
<p class="text-gray-700 dark:text-gray-300">Body text</p>

<!-- Card -->
<div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800">
  Content
</div>

<!-- Button -->
<button class="bg-blue-600 text-white hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600">
  Click me
</button>

<!-- Input -->
<input type="text" class="border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100">
```

## Responsive Design (Mobile-First)

Tailwind uses mobile-first breakpoints:
- **No prefix:** 0–639px (mobile)
- **sm:** 640px and up (small devices)
- **md:** 768px and up (tablets)
- **lg:** 1024px and up (desktops)
- **xl:** 1280px and up (large screens)

**Container padding (mobile → desktop):**

```erb
<!-- Responsive padding: 4 on mobile, 6 on sm, 8 on lg -->
<div class="px-4 sm:px-6 lg:px-8 py-8">
  Content
</div>
```

**Grid layout (stack on mobile, grid on md):**

```erb
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <% items.each do |item| %>
    <div class="p-4 border border-gray-200 dark:border-gray-800 rounded-lg">
      <%= item.name %>
    </div>
  <% end %>
</div>
```

**Show/hide elements:**

```erb
<!-- Hidden on mobile, visible on md+ -->
<div class="hidden md:block">
  Sidebar
</div>

<!-- Visible on mobile, hidden on md+ -->
<div class="md:hidden">
  Mobile menu
</div>
```

**Responsive typography:**

```erb
<h1 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold">
  Heading scales with screen size
</h1>
```

**Responsive spacing:**

```erb
<div class="mb-4 sm:mb-6 md:mb-8 lg:mb-10">
  Content with responsive margin
</div>
```

## Animation Utilities

### Fade In

```erb
<div class="animate-fadeIn">
  Content fades in on load
</div>
```

Add to `tailwind.config.js` if not present:

```javascript
theme: {
  extend: {
    animation: {
      fadeIn: 'fadeIn 0.5s ease-in',
    },
    keyframes: {
      fadeIn: {
        '0%': { opacity: '0' },
        '100%': { opacity: '1' },
      },
    },
  },
}
```

### Hover & Focus Transitions

```erb
<button class="transition-colors duration-200 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600">
  Smooth color change
</button>
```

### Slide In

```javascript
theme: {
  extend: {
    animation: {
      slideIn: 'slideIn 0.3s ease-out',
    },
    keyframes: {
      slideIn: {
        '0%': { transform: 'translateX(-100%)', opacity: '0' },
        '100%': { transform: 'translateX(0)', opacity: '1' },
      },
    },
  },
}
```

## Best Practices Checklist

- [ ] **Dark/light color pairs always together** — Never use `bg-white` without `dark:bg-gray-950`
- [ ] **Test contrast ratios** — Use a contrast checker tool for accessibility (WCAG AA minimum)
- [ ] **Mobile-first prefixes** — Add `sm:`, `md:`, `lg:` before hard-coding desktop styles
- [ ] **Use the `cn()` helper** — For all conditional class logic
- [ ] **Extract repeated patterns** — Create partials for badges, buttons, cards
- [ ] **Avoid inline styles** — Stick to Tailwind utilities; no `style=""` attributes
- [ ] **Use semantic color names** — Yellow = warning, green = success, red = danger
- [ ] **Test with keyboard navigation** — Ensure all interactive elements are accessible
- [ ] **Use focus rings** — Add `focus:ring-2 focus:ring-blue-500 focus:outline-none` to inputs
- [ ] **Responsive images** — Use `max-w-full` and `h-auto` for fluid image scaling
