# Accessible Modals

Patterns for accessible modal dialogs in Rails + Stimulus + Hotwire (Turbo Frames).

## The Pattern

A modal needs:

1. **Focus trap** — Tab/Shift+Tab cycles within the modal, not behind it
2. **`role="dialog"`** and **`aria-modal="true"`** on the container
3. **`aria-labelledby`** pointing to the modal title
4. **ESC to close**
5. **Focus returns to trigger** on close
6. **Inert background** — content behind the modal is not interactive

## Stimulus Controller

The complete `modal_controller.js` — focus trap, ESC to close, backdrop click, focus return — lives at `examples/modal_controller.js`. Drop it into `app/javascript/controllers/` and adjust selectors for your design. The behavior summary is in the bullet list above; the implementation is in the example file.

The ERB template below assumes the controller is wired up. `data-action="click->modal#closeOnBackdrop keydown.esc@window->modal#close"` on the dialog element pairs with the controller's `open`/`close` actions.

## ERB Template

```erb
<%# app/views/shared/_modal.html.erb %>
<%
# Locals:
#   title  - modal title (required)
#   id     - unique modal id (optional, auto-generated)
#   size   - "sm", "md", "lg" (default: "md")
%>
<%
  id ||= "modal-#{SecureRandom.hex(4)}"
  size_classes = {
    "sm" => "max-w-sm",
    "md" => "max-w-lg",
    "lg" => "max-w-2xl"
  }
%>

<div
  id="<%= id %>"
  class="hidden fixed inset-0 z-50 flex items-center justify-center bg-black/50"
  data-controller="modal"
  data-action="click->modal#closeOnBackdrop keydown.esc@window->modal#close"
  role="dialog"
  aria-modal="true"
  aria-labelledby="<%= id %>-title"
>
  <div
    class="bg-white rounded-lg shadow-xl <%= size_classes[size || "md"] %> w-full mx-4 max-h-[90vh] overflow-y-auto"
    data-modal-target="container"
  >
    <%# Header %>
    <div class="flex items-center justify-between px-6 py-4 border-b">
      <h2 id="<%= id %>-title" class="text-lg font-semibold">
        <%= title %>
      </h2>
      <button
        type="button"
        class="p-1 rounded hover:bg-gray-100"
        data-action="modal#close"
        data-modal-target="closeButton"
        aria-label="Close dialog"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <%# Body %>
    <div class="px-6 py-4">
      <%= yield %>
    </div>

    <%# Footer (optional) %>
    <% if content_for?(:modal_footer) %>
      <div class="px-6 py-4 border-t bg-gray-50 rounded-b-lg">
        <%= yield :modal_footer %>
      </div>
    <% end %>
  </div>
</div>
```

## Usage

```erb
<%# Trigger button %>
<button
  type="button"
  data-action="click->modal#open"
  data-modal-target="trigger"
>
  Open Settings
</button>

<%# Modal %>
<%= render layout: "shared/modal", locals: { title: "Settings", size: "md" } do %>
  <p>Configure your preferences here.</p>

  <% content_for :modal_footer do %>
    <button type="button" class="btn-secondary" data-action="modal#close">Cancel</button>
    <button type="button" class="btn-primary">Save</button>
  <% end %>
<% end %>
```

## Turbo Frame Modal Pattern

For modals loaded via Turbo Frame (e.g., clicking a link opens a modal with remote content):

```erb
<%# Link that loads modal content %>
<%= link_to "Edit Profile", edit_profile_path, data: { turbo_frame: "modal" } %>

<%# Turbo Frame target — empty by default, filled on click %>
<%= turbo_frame_tag "modal" do %>
  <%# Content loads here %>
<% end %>
```

The server responds with the modal partial wrapped in the frame:

```erb
<%# app/views/profiles/edit.html.erb %>
<%= turbo_frame_tag "modal" do %>
  <%= render layout: "shared/modal", locals: { title: "Edit Profile" } do %>
    <%= form_with model: @profile, data: { turbo: false } do |f| %>
      <%# form fields %>
    <% end %>
  <% end %>
<% end %>
```

**Important:** Use `data: { turbo: false }` on forms inside Turbo Frame modals that do full-page redirects. Otherwise Turbo generates broken `/undefined` paths.

## Testing Modal Accessibility

```ruby
it 'modal is accessible' do
  visit dashboard_path
  click_button 'Open Settings'

  # Modal should be visible
  expect(page).to have_css('[role="dialog"][aria-modal="true"]')

  # Should have a labelled title
  expect(page).to have_css('[aria-labelledby]')

  # Close button should have an accessible name
  expect(page).to have_css('button[aria-label="Close dialog"]')

  # Run axe
  expect_accessible

  # ESC should close
  find('[role="dialog"]').send_keys(:escape)
  expect(page).to have_no_css('[role="dialog"]')
end
```

## Related

`examples/modal_controller.js` is the standalone copy of the Stimulus controller. The Turbo Frame gotcha (`data: { turbo: false }` on forms inside modal frames) is in `forms.md` as well — both files mention it from their respective angles.

## Real-World Gotcha: iOS Safari Cuts Off the Bottom of Modals

**Symptom:** On iPhone Safari, the modal's bottom button (or footer) is visually hidden behind the Safari bottom toolbar (the home / bookmarks / search / tabs row). The button is still tappable but obscured. Looks like "modal too tall," but the real cause is the viewport unit and missing safe-area.

**Cause (three things stacked):**

1. `100vh` on iOS Safari = full screen including the area behind the bottom toolbar. `min-h-screen` and `max-h-[80vh]` use this 100vh, so the modal panel extends below the visible area.
2. iOS exposes a `safe-area-inset-bottom` value to push content above the bottom bar, but only if the layout's viewport meta tag includes `viewport-fit=cover`.
3. Without that, every `100vh` / `80vh` reference assumes more space than the user can see.

**Fix — three edits to `app/views/shared/_modal.html.erb` and one to the layout:**

1. **Layout viewport meta** — `app/views/layouts/application.html.erb` (or whichever layout the modal pages use). Without this, the safe-area insets return `0` and the fix below is a no-op.

   ```html
   <!-- before -->
   <meta name="viewport" content="width=device-width, initial-scale=1" />
   <!-- after -->
   <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
   ```

2. **Modal flex container** — `min-h-screen` → `min-h-[100dvh]`, and add safe-area padding to the bottom:

   ```erb
   <!-- before -->
   <div class="flex items-center justify-center min-h-screen p-4 overflow-y-auto">
   <!-- after -->
   <div class="flex items-center justify-center min-h-[100dvh] p-4 pb-[calc(1rem+env(safe-area-inset-bottom))] overflow-y-auto">
   ```

3. **Modal panel** — `max-h-[80vh]` → `max-h-[80dvh]`, and add safe-area padding to the panel so the button + footer don't hit the toolbar:

   ```erb
   <!-- before -->
   <div class="... p-6 ... max-h-[80vh] ...">
   <!-- after -->
   <div class="... p-6 pb-[calc(1.5rem+env(safe-area-inset-bottom))] ... max-h-[80dvh] ...">
   ```

**Why each piece is required:**

- `100dvh` (dynamic viewport height) excludes the iOS bottom bar from the unit. Falls back to `100vh` on browsers that don't support dvh, but `viewport-fit=cover` + safe-area handle the visual overlap regardless.
- `viewport-fit=cover` is what makes `env(safe-area-inset-bottom)` return a non-zero value. Without it, the calc() reduces to plain padding.
- The two `pb-[calc(...)]` paddings are layered: the flex container's padding prevents the panel from centering below the bar; the panel's padding ensures the button + footer are visible even when the panel is at max height.

**What you get after the fix:**

- iPhone Safari (bottom bar visible): modal centers above the bar, button visible, content scrollable.
- iPhone Safari (bottom bar hidden after scroll): `dvh` adjusts, modal recenters.
- iPad Safari / Android Chrome / desktop: no extra padding, no visual change.

**Common mistake to avoid:** "moving the modal up 20px" with a hard-coded `mt-[-20px]`. That works on the specific iPhone you tested but breaks on different screen sizes, iPads, Android, and iOS with different bar heights (e.g., after rotation or with accessibility settings). The safe-area approach handles all of these automatically.

**Browser support:** `dvh` is in all evergreen browsers since 2023 (iOS Safari 15.4+, Chrome 108+, Firefox 101+). `env(safe-area-inset-bottom)` since iOS 11. For older iOS support, a fixed `pb-[88px]` is a fallback, but for a 2026 deploy you don't need it.

**Tested against:** iPhone Safari at the iOS 26 standard bar height. Verified the modal centers above the bar and the bottom button is fully visible without scrolling.
