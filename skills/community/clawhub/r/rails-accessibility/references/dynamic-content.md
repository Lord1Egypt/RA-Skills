# Accessible Dynamic Content

Patterns for making Turbo Frames, Turbo Streams, and Stimulus-driven UI updates accessible to screen readers.

## The Core Problem

When Turbo replaces DOM content, screen readers don't announce the change. Users can miss:

- Form validation errors appearing after submit
- New content loading into a Turbo Frame
- Flash messages appearing at the top of the page
- Live-updating counters or status indicators

## `aria-live` Regions

`aria-live` tells screen readers to announce content changes in a region. Three values:

| Value | Behavior |
|---|---|
| `off` | Default. No announcements. |
| `polite` | Announces when user is idle. Use for most updates. |
| `assertive` | Interrupts immediately. Use sparingly (errors, alerts). |

### Flash messages

```erb
<%# app/views/shared/_flash.html.erb %>
<% flash.each do |type, message| %>
  <div
    class="flash flash-<%= type %>"
    role="<%= type == 'alert' ? 'alert' : 'status' %>"
    aria-live="<%= type == 'alert' ? 'assertive' : 'polite' %>"
    aria-atomic="true"
  >
    <%= message %>
  </div>
<% end %>
```

**Key details:**
- `role="alert"` is implicitly `aria-live="assertive"` and `aria-atomic="true"`. Use it for error/alert flashes.
- Use `role="status"` + `aria-live="polite"` for success/info.
- **`aria-atomic="true"` makes the entire message get re-announced when it changes, not just the diff.** A flash that updates from "Sending…" to "Sent! (3 errors)" will be read as one complete new message, not "Sent! (3 errors)" over the top of the old "Sending…". Always pair it with the explicit `aria-live`.

### Form error summary

```erb
<% if resource.errors.any? %>
  <div
    id="error_explanation"
    class="rounded-md bg-red-50 p-4 mb-6"
    role="alert"
    aria-live="assertive"
    tabindex="-1"
    data-turbo-temporary
  >
    <h2 class="text-red-800 text-sm font-medium">
      <%= pluralize(resource.errors.count, "error") %> prohibited this from being saved:
    </h2>
    <ul class="mt-2 text-sm text-red-700 list-disc list-inside">
      <% resource.errors.full_messages.each do |message| %>
        <li><%= message %></li>
      <% end %>
    </ul>
  </div>
<% end %>
```

**Key details:**
- `tabindex="-1"` — allows programmatic focus (focus it after Turbo re-render so screen reader starts there)
- `data-turbo-temporary` — prevents Turbo from caching this element (errors should be fresh each render)

## Turbo Frame Loading States

### Announcing frame loads

```erb
<%= turbo_frame_tag "results",
  aria: { busy: true, live: "polite" },
  data: { turbo_busy_attribute: "aria-busy" } do %>
  <%# Content loads here %>
<% end %>
```

`aria-busy="true"` tells screen readers the region is updating. Turbo sets it during navigation and removes it when done.

### Loading indicator

```erb
<%= turbo_frame_tag "results" do %>
  <div class="animate-pulse" data-turbo-temporary>
    <p class="sr-only" role="status">Loading results...</p>
    <%# skeleton UI %>
  </div>
<% end %>
```

## Turbo Stream Announcements

For updates pushed via Turbo Stream, add a dedicated announcement region:

```erb
<%# In your layout %>
<div
  id="announcements"
  class="sr-only"
  role="status"
  aria-live="polite"
  aria-atomic="true"
></div>
```

```erb
<%# In your Turbo Stream response %>
<%= turbo_stream.update "announcements", "3 new rides available" %>
<%= turbo_stream.replace "ride-list", partial: "rides/list", locals: { rides: @rides } %>
```

## Stimulus: Announcing State Changes

```javascript
// app/javascript/controllers/announce_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static values = { message: String, polite: { type: Boolean, default: true } }

  connect() {
    this.announce()
  }

  announce() {
    const region = document.getElementById("announcements")
    if (!region) return

    region.setAttribute("aria-live", this.politeValue ? "polite" : "assertive")
    // Clear and re-set to trigger announcement
    region.textContent = ""
    setTimeout(() => {
      region.textContent = this.messageValue
    }, 50)
  }
}
```

Usage:

```erb
<div data-controller="announce" data-announce-message-value="Filter applied: 12 results"></div>
```

## Testing Dynamic Content

```ruby
it 'announces form errors' do
  visit new_ride_path
  click_button 'Submit'  # submit empty form

  # Error summary should be an alert region
  expect(page).to have_css('[role="alert"]')

  # Individual field errors should be linked
  expect(page).to have_css('input[aria-invalid="true"]')
  expect(page).to have_css('[aria-describedby*="_error"]')
end

it 'announces Turbo Stream updates' do
  visit rides_path

  # Trigger an update (e.g., filter change)
  select 'Completed', from: 'Status'

  # Announcement region should exist
  expect(page).to have_css('#announcements[aria-live]', visible: :all)
end
```

## Related

`forms.md` covers how the error summary above should wire into individual fields (`aria-describedby`, `aria-invalid`). `modals.md` covers the same `aria-live` / focus-management patterns applied to dialog content.
