# Accessible Navigation

Skip links, landmark roles, and navigation patterns for Rails + Tailwind.

## Skip Link

The first interactive element on every page. Lets keyboard and screen reader users jump past repetitive navigation to the main content.

### Partial: `app/views/shared/_skip_link.html.erb`

```erb
<a
  href="#main-content"
  class="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:z-50 focus:px-4 focus:py-2 focus:bg-brand-dark focus:text-white focus:rounded"
>
  Skip to main content
</a>
```

Place it as the first element inside `<body>`:

```erb
<%# app/views/layouts/application.html.erb %>
<body>
  <%= render "shared/skip_link" %>
  <%= render "shared/navbar" %>

  <main id="main-content" tabindex="-1">
    <%= yield %>
  </main>
</body>
```

**Key details:**
- `tabindex="-1"` on `<main>` — makes it programmatically focusable (needed for skip link to work in all browsers)
- `sr-only focus:not-sr-only` — invisible until focused, then appears as a visible button
- Must be the FIRST focusable element on the page

## Landmark Roles

Use semantic HTML5 elements (which have implicit ARIA roles) rather than explicit `role` attributes where possible:

| HTML Element | Implicit Role |
|---|---|
| `<header>` | `banner` (when child of `<body>`) |
| `<nav>` | `navigation` |
| `<main>` | `main` |
| `<footer>` | `contentinfo` (when child of `<body>`) |
| `<aside>` | `complementary` |
| `<section>` | `region` (when has accessible name) |
| `<form>` | `form` (when has accessible name) |

### Navigation with `aria-label`

Multiple `<nav>` elements need unique labels:

```erb
<nav aria-label="Main navigation">
  <%# primary nav links %>
</nav>

<nav aria-label="Breadcrumb">
  <%# breadcrumb trail %>
</nav>

<nav aria-label="Footer">
  <%# footer links %>
</nav>
```

### Current page indicator

```erb
<%= link_to "Dashboard", dashboard_path,
  class: "nav-link",
  aria: { current: current_page?(dashboard_path) ? "page" : nil } %>
```

## Navigation Patterns

### Mobile hamburger menu

```erb
<nav aria-label="Main navigation" data-controller="mobile-nav">
  <%# Hamburger button %>
  <button
    type="button"
    class="lg:hidden"
    data-action="mobile-nav#toggle"
    data-mobile-nav-target="button"
    aria-expanded="false"
    aria-controls="mobile-menu"
  >
    <span class="sr-only">Open menu</span>
    <%# hamburger icon %>
  </button>

  <%# Menu panel %>
  <div
    id="mobile-menu"
    class="hidden lg:block"
    data-mobile-nav-target="menu"
  >
    <%# nav links %>
  </div>
</nav>
```

**Key details:**
- `aria-expanded` toggles between `true`/`false`
- `aria-controls` links button to the menu panel
- The menu panel needs an `id` matching `aria-controls`

### Breadcrumbs

```erb
<nav aria-label="Breadcrumb">
  <ol class="flex space-x-2 text-sm text-gray-500">
    <li>
      <%= link_to "Home", root_path %>
      <span aria-hidden="true">/</span>
    </li>
    <li>
      <%= link_to "Rides", rides_path %>
      <span aria-hidden="true">/</span>
    </li>
    <li aria-current="page">
      Ride #<%= @ride.id %>
    </li>
  </ol>
</nav>
```

## Testing Navigation Accessibility

```ruby
it 'has accessible navigation' do
  visit root_path

  # Skip link should exist
  expect(page).to have_link('Skip to main content', visible: :all)

  # Main content should have id
  expect(page).to have_css('#main-content')

  # Nav elements should have labels
  expect(page).to have_css('nav[aria-label]')

  # Current page should be indicated
  expect(page).to have_css('[aria-current="page"]')

  # Run axe
  expect_accessible
end
```

## Related

`testing.md` covers the system-spec patterns and the Devise sign-in gotcha for any navigation test that needs an authenticated user.
