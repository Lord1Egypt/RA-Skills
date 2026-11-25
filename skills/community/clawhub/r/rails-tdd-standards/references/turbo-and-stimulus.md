# Turbo And Stimulus

Turbo Stream and Frame semantics, Stimulus controllers, and importmap.

## Turbo and Stimulus

### `turbo_stream.replace` destroys its target

`turbo_stream.replace "dom_id", partial: "..."` replaces the **entire** element
with that id. Any Stimulus controller attached to that element is destroyed and
re-initialized — and its state is lost.

```erb
<%# ❌ replaces the whole card — the controller is torn down %>
<%= turbo_stream.replace "card_#{item.id}" do %>
  <%= render "item", item: item %>
<% end %>
```

```erb
<%# ✅ appends inside — the controller survives %>
<%= turbo_stream.append "list_#{item.id}" do %>
  <%= render "item", item: item %>
<% end %>
```

Use `update` for a targeted content swap:

```erb
<%= turbo_stream.update "status_#{item.id}" do %>
  <%= render "status", item: item %>
<% end %>
```

### Turbo Frame specs

```ruby
# ✅ assert the frame's content, not the whole page
within_frame "modal" do
  expect(page).to have_content("Confirm")
  click_button "Yes"
end
```

`within_frame` scopes the assertions; without it, a `have_content` can match
text elsewhere on the page and the spec passes for the wrong reason.

### `data-turbo="false"` does not opt a `form_with` out

`form_with` adds `data-turbo` itself. To get a non-Turbo form you need
`form_with(..., data: { turbo: false })` — and the form must not also carry a
`data-turbo-frame` target, or Turbo still intercepts the submit.

```erb
<%# ❌ still submitted by Turbo %>
<%= form_with model: @record, local: true %>
```

```erb
<%# ✅ explicit opt-out %>
<%= form_with model: @record, data: { turbo: false } %>
```

**Symptom:** the form submits, the page stays put, no flash, no error. The
request never reaches the server.

### Stimulus controllers

A Stimulus controller that fails to initialize is simply absent — no error is
raised on the server, and the element just does nothing.

Work through these three checks in order when a controller appears dead:

1. **Registered** — the controller is listed in the app's Stimulus registry
   file under `app/javascript/controllers/`.
2. **Loaded** — the controller file is reachable by the browser. With importmap,
   a missing pin produces a 404 in the browser console, not a server error.
3. **Attached** — the element carries the matching `data-controller` attribute.

In a system spec, JS console errors are invisible by default. Surface them:

```ruby
# ✅ surface browser console errors in the spec output
Capybara::Selenium::Driver#browser.logs.get(:browser)
```

Or assert on the *effect* rather than the console — an effect is what the user
actually experiences:

```ruby
expect(page).to have_content("Copied")
```

---
