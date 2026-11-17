# Forms — Elementor MCP (reference)

## Forms

Branch on the Pro detection from the top of this skill.

### If Pro → native Form widget (preferred)

With Pro active the `add-form` MCP tool is exposed — build a real, submitting form
as a native widget with no third-party plugin. The whole form (fields, labels,
submit action, email notification) lives in Elementor and is editable in the
visual editor.

**Build pattern** — `add-form` into the contact-section container, then define
fields and the submit/email actions. Document and pass the form's settings the
same disciplined way the Fluent Forms class map below is documented:

```js
// Native Pro Form widget — placed in the contact section container
mcp__elementor__elementor-mcp-add-form({
  post_id: <page_id>,
  parent_id: <contact_section_container_id>,
  form_name: "Contact",
  // fields as the form-widget schema defines them (id/type/label/required/width);
  // load get-widget-schema for "form" first to confirm exact field-array keys
  form_fields: [
    { custom_id: "name",    field_type: "text",     field_label: "Name",    required: "true", width: "50" },
    { custom_id: "email",   field_type: "email",    field_label: "Email",   required: "true", width: "50" },
    { custom_id: "message", field_type: "textarea", field_label: "Message", required: "true", width: "100" }
  ],
  button_text: "Send",
  // Submit actions: "email" is the default; set the To address in the email action group.
  submit_actions: ["email"],
  email_to: "<site admin email>"
})
```

- **Confirm field/action key names against the live schema** before building:
  `get-widget-schema({ widget_type: "form" })`. The form widget's field array and
  action keys are the part most likely to drift between Pro versions — treat the
  schema as ground truth, exactly as with the container schema.
- **Styling** native form fields uses the widget's own style controls (typography,
  spacing, borders, button) passed as flat params — no scoped CSS hack needed. Only
  drop to a `<style>`-only HTML widget for things the controls don't expose, scoped
  to the form's `element_id` (same rule as everywhere else).
- This replaces the entire Fluent Forms split below — **don't** install Fluent
  Forms when Pro is present.

### If Free → Fluent Forms (fallback)

Elementor's native Form widget is Pro, and `add-form` is **not exposed** without it. The kit's wizard auto-installs **Fluent Forms** as the free workaround. The flow is split: the user builds the form, then Claude wires it into the page and styles it.

#### The split — what Claude does vs. what the user does

**The user does (manual, ~2-3 min in WP Admin):**

1. **Fluent Forms → New Form** → pick the *Contact Form* template *(pre-built with Name / Email / Subject / Message)* OR start from blank
2. *(optional)* Drag in extra fields — Phone, dropdown, etc.
3. **Save Form** — note the form ID at the top of the page (usually `1` for the first form)
4. **Settings → Email Notifications** → confirm the To address (default: `{admin_email}`)

**Claude does:**

1. Replace any placeholder form (HTML widget) in the contact section with `add-shortcode` widget containing `[fluentform id="<ID>"]`
2. Add a small `<style>` block (in an HTML widget alongside, NOT replacing the shortcode widget) that scopes Fluent Forms styling to match the site's design

#### Wiring the form

```js
// Drop the shortcode widget where the form should appear
mcp__elementor__elementor-mcp-add-shortcode({
  post_id: <page_id>,
  parent_id: <contact_section_container_id>,
  shortcode: '[fluentform id="1"]'
})
```

#### Styling — verified Fluent Forms class structure (Fluent 6.x)

```
.fluentform                            ← outer wrapper
.fluentform_wrapper_<formId>           ← per-form wrapper (e.g. .fluentform_wrapper_1)
  .ff-default                          ← default skin marker
    form.frm-fluent-form
      .ff-el-group                     ← each field block
        .ff-el-input--label            ← label
          label                        ← actual <label> tag
        .ff-el-input--content
          input.ff-el-form-control     ← text inputs
          textarea.ff-el-form-control  ← textareas
      .ff-t-container                  ← two-column row (e.g. first/last name)
        .ff-t-cell                       ← each cell
      .ff_submit_btn_wrapper
        button.ff-btn.ff-btn-submit    ← submit button
      .ff-el-is-required               ← required field marker
```

#### CSS variables (the easiest override path)

Fluent Forms exposes these custom properties on `:root`. **Redefine them on the per-form wrapper to restyle the whole form without specificity battles:**

```css
.fluentform_wrapper_1 {
  --fluentform-primary: #5C1A1B;          /* submit button bg + focus accent */
  --fluentform-secondary: #171615;        /* body text in inputs */
  --fluentform-border-color: #C9C2B3;     /* input borders */
  --fluentform-border-radius: 0px;        /* hairline-square inputs */
}
```

That alone gets you ~80% of the way to a custom design.

#### Full styling pattern (when CSS vars aren't enough)

For the remaining 20% (typography overrides, hairline-only borders, custom button feel), use scoped selectors with the per-form wrapper class. Specificity (0,2,0) matches Fluent's defaults; load order wins because your styles come after.

```css
/* Scope EVERYTHING to .fluentform_wrapper_<id> so you don't bleed into other pages. */

.fluentform_wrapper_1 .ff-el-form-control {
  font-family: 'Inter Tight', sans-serif;
  font-size: 14px;
  border: none;
  border-bottom: 1px solid var(--fluentform-border-color);
  border-radius: 0;
  padding: 14px 0;
  background: transparent;
  color: #171615;
}

.fluentform_wrapper_1 .ff-el-form-control:focus {
  border-bottom-color: #171615;
  box-shadow: none;
}

.fluentform_wrapper_1 textarea.ff-el-form-control {
  font-family: 'Cormorant Garamond', serif;
  font-size: 17px;
  min-height: 100px;
}

.fluentform_wrapper_1 .ff-el-input--label label {
  font-family: 'Inter Tight', sans-serif;
  font-size: 11px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: #8A857E;
}

.fluentform_wrapper_1 .ff-btn-submit {
  background: #5C1A1B;
  color: #fff;
  border: 1px solid #5C1A1B;
  border-radius: 0;
  padding: 16px 26px;
  font-family: 'Inter Tight', sans-serif;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.28em;
  text-transform: uppercase;
}

.fluentform_wrapper_1 .ff-btn-submit:hover {
  background: #3F1011;
  border-color: #3F1011;
}

/* Two-column rows — turn into a CSS grid with consistent gap */
.fluentform_wrapper_1 .ff-t-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 22px;
}
@media (max-width: 640px) {
  .fluentform_wrapper_1 .ff-t-container {
    grid-template-columns: 1fr;
  }
}

/* Asterisk marker on required fields */
.fluentform_wrapper_1 .ff-el-is-required label::after {
  color: #5C1A1B;
}
```

#### Where to inject the styles

Two options:

1. **Drop an HTML widget right above (or below) the Shortcode widget** with the `<style>` block inside. Wrap selectors in `.fluentform_wrapper_<id>` to keep them scoped. *(Recommended — keeps styles co-located with the form.)*
2. **Add to Customizer → Additional CSS** *(Appearance → Customize)* — site-wide, persists across page rebuilds. *(Better for production sites where the form appears on multiple pages.)*

#### Common gotchas

- **Find the form ID by looking at the form's URL in WP Admin** — `/wp-admin/admin.php?page=fluent_forms&route=editor&form_id=1` → ID is `1`. Or query the DB: `SELECT id, title FROM wp_fluentform_forms`.
- **Do NOT remove the `.ff-default` class** by overriding `class` attributes — Fluent's submit button styling cascades from it.
- **Fluent's CSS loads after page render via `enqueue_scripts`.** If your overrides aren't applying, check that your `<style>` block lives in a widget that renders inside the page body (not the head).
- **Asterisks for required fields** are pseudo-elements (`::after`) — color them via `.ff-el-is-required label::after { color: ... }`, not `color: ...` on the label itself.

### Other form options (when Fluent Forms isn't available)

1. **Contact Form 7** — same shortcode pattern: `[contact-form-7 id="..."]`. Less polished default look, but free and works.
2. **Styled HTML `<form>` with a JS-alert handler** — only as a flagged visual placeholder for early builds. **Tell the user explicitly: "form is visual only — submissions don't go anywhere yet. Wire to Fluent Forms before going live."**

