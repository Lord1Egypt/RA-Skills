# Accessible Forms

Patterns for accessible form fields, error states, labels, and Turbo-aware form submission in Rails + Tailwind.

## The `_accessible_field` Pattern

This is a core form field partial. It handles:

- Explicit `<label>` with `for` attribute
- `aria-describedby` linking to error messages
- `aria-invalid` when errors are present
- Error message rendering with `role="alert"`
- Required field indicators

### Partial: `app/views/shared/_accessible_field.html.erb`

```erb
<%#
  Accessible form field partial.

  Locals:
    form        - Rails form builder
    field       - field name (symbol)
    label       - label text (default: field.to_s.humanize)
    type        - input type (default: "text")
    required    - boolean (default: false)
    hint        - optional hint text
    options     - additional HTML options hash
    input_html  - additional input HTML options hash
%>
<%
  label ||= field.to_s.humanize
  type ||= "text"
  required ||= false
  options ||= {}
  input_html ||= {}

  field_id = "#{form.object_name}_#{field}"
  error_id = "#{field_id}_error"
  hint_id = "#{field_id}_hint"
  has_error = form.object.errors[field].any?

  described_by = []
  described_by << error_id if has_error
  described_by << hint_id if local_assigns[:hint]

  input_classes = [
    "block w-full rounded-md border px-3 py-2",
    "focus:outline-none focus:ring-2 focus:ring-brand-light",
    has_error ? "border-red-500 focus:ring-red-500" : "border-gray-300"
  ].join(" ")
%>

<div class="mb-4">
  <%= form.label field, class: "block text-sm font-medium mb-1" do %>
    <%= label %>
    <% if required %>
      <span class="text-red-500" aria-hidden="true">*</span>
      <span class="sr-only">(required)</span>
    <% end %>
  <% end %>

  <% if local_assigns[:hint] %>
    <p id="<%= hint_id %>" class="text-sm text-gray-500 mb-1"><%= hint %></p>
  <% end %>

  <%= form.send(
    "#{type}_field",
    field,
    **options,
    class: input_classes,
    id: field_id,
    aria: {
      describedby: described_by.join(" ").presence,
      invalid: has_error || nil,
      required: required || nil
    }.compact,
    **input_html
  ) %>

  <% if has_error %>
    <p id="<%= error_id %>" class="text-sm text-red-600 mt-1" role="alert">
      <%= form.object.errors.full_messages_for(field).to_sentence %>
    </p>
  <% end %>
</div>
```

### Usage

```erb
<%= render "shared/accessible_field",
  form: form,
  field: :email,
  type: :email,
  required: true,
  hint: "We'll never share your email" %>

<%= render "shared/accessible_field",
  form: form,
  field: :phone_number,
  type: :tel,
  label: "Phone" %>
```

## Key Rules

### 1. Every input needs a visible label

Placeholder text is NOT a label. Screen readers may not announce it, and it disappears on focus.

```erb
<%# BAD — no label, placeholder-only %>
<input type="text" placeholder="Search...">

<%# GOOD — visible label + input %>
<label for="search">Search</label>
<input type="text" id="search" name="search">
```

### 2. Error messages must be linked to the input

Use `aria-describedby` pointing to the error element. The error element needs `role="alert"` for screen readers to announce it.

### 3. Required fields need both visual and programmatic indicators

- Visual: asterisk or "(required)" text
- Programmatic: `aria-required="true"` or `required` attribute
- Screen-reader-only text for the asterisk: `<span class="sr-only">(required)</span>`

### 4. `aria-invalid` on error

Set `aria-invalid="true"` when the field has validation errors. Remove it (or set to `false`) when the error is resolved.

## Turbo Gotchas

Two gotchas break system specs even when the form markup is otherwise accessible:

1. `form_with ... local: true` does **not** opt the form out of Turbo; use `data: { turbo: false }` instead.
2. Inline `<script>` tags need the CSP nonce when nonces are enabled, otherwise custom page JS (preset buttons, validation) is silently blocked.

Those issues are not accessibility-specific, but they show up as "the form did nothing" in accessibility/system specs, so this reference links to the canonical skill rather than duplicating it.

### `button_to` with `data: { turbo: false }` doesn't work

`button_to` puts `data-turbo="false"` on the `<button>`, not the `<form>`. Turbo reads the form element. Use `form_with` + `submit_tag` instead.

### `data-turbo-frame` overrides `data-turbo="false"`

If a form has both `data-turbo-frame="modal"` and `data-turbo="false"`, Turbo ignores `data-turbo="false"` and processes within the frame. This is a real source of production bugs - the form appears to do nothing and the user is stuck in the modal. Full modal/Turbo Frame timing guidance is in `references/testing.md` and `references/modals.md`.

## Testing Form Accessibility

```ruby
# spec/system/sign_up_spec.rb
it 'has accessible form fields' do
  visit new_user_registration_path

  # Every input should have a label
  expect(page).to have_css('label[for="user_email"]')
  expect(page).to have_css('label[for="user_password"]')

  # Submit empty to trigger errors
  click_button 'Sign up'

  # Error fields should have aria-invalid
  expect(page).to have_css('input[aria-invalid="true"]')

  # Error messages should have role="alert"
  expect(page).to have_css('[role="alert"]')

  # Run axe
  expect_accessible
end
```

## Related

`color-contrast.md` covers the Tailwind/oklch rules that affect form styling (input borders, error colors). `testing.md` covers the system-spec patterns and the Devise sign-in gotcha that applies to authenticated form specs.
