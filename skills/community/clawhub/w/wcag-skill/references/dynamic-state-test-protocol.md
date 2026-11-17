# WCAG 4.1.2 dynamic-state test protocol

WCAG 4.1.2 (Name, Role, Value) applies to user interface components. A source
inventory can find likely controls and state attributes, but cannot establish
the computed accessible name, rendered role, or whether state changes are
exposed correctly. A passing axe/Pa11y/QualWeb result is not evidence that an
interactive state transition works.

## 1. Inventory components and states

Run the bundled source check against each relevant HTML entry point:

```bash
python3 scripts/check-wcag-412.py path/to/page.html
```

Review its candidates in the rendered page. Also include controls created by
JavaScript, controls inside overlays or error flows, and controls whose state
changes are not evident from markup. The checker intentionally reports
candidates, not pass/fail results. Its `4.1.2-static` label means only that it
did not infer a dynamic state from the source.

Open [`../tests/fixtures/wcag-412-stateful-page.html`](../tests/fixtures/wcag-412-stateful-page.html)
to compare a “Dark theme” button that changes the page without exposing its
state with one whose `aria-pressed` value stays synchronized. The
`data-wcag-412-dynamic` attribute in that teaching fixture is an inventory hint
for the bundled checker; it does not add accessibility semantics.

Common dynamic candidates include `aria-pressed`, `aria-checked`,
`aria-expanded`, `aria-selected`, `aria-current`, `aria-valuenow`,
`aria-valuetext`, `aria-invalid`, and `aria-busy`; native checkboxes, radios,
range inputs, selects, and `<details>`; and custom switch, slider, spinbutton,
tab, menu, disclosure, dialog, and popover controls. Add
`data-wcag-412-dynamic` to an inventoried element when its state transition
cannot be inferred from its markup.

## 2. Test each transition

For every user-triggered change, capture evidence before and after activating
the control:

1. Locate by its accessible role and name, not only by CSS selector.
2. Verify that it is visible and its initial state/value is exposed.
3. Activate it with the supported pointer and keyboard interaction.
4. Assert the changed accessible state/value and the corresponding application
   state or visible result. These must agree.
5. Repeat the transition in reverse when the control is a toggle or disclosure.
6. Record a focused Playwright assertion as primary regression evidence. An
   ARIA snapshot may supplement it, but should not replace targeted assertions.

Use [`../templates/playwright-state.spec.ts`](../templates/playwright-state.spec.ts)
as a starting point. Adapt the accessible name, state attribute, and
application-state assertion to the real component; do not assume every toggle
uses `aria-pressed` or a `.dark` class.

## 3. Review the accessibility tree and assistive technology

Verify that the computed accessible name and role are correct in the rendered
accessibility tree. A declared ARIA attribute by itself does not prove correct
semantics, and absence of an explicit ARIA state does not imply failure when
native HTML semantics expose it.

Perform a manual browser/screen-reader check for custom widgets, live
announcements, dialogs, or states whose meaning depends on context. Record the
browser, assistive technology and version, date, route/state, and observed
result. Playwright and automated audits provide technical evidence, not a
substitute for this review.

## 4. Report without overclaiming

Use these review labels:

- `4.1.2-static`: no dynamic state was inferred; rendered name and role still
  need review.
- `4.1.2-dynamic-required`: a stateful component was found; the transition test
  is required.
- `4.1.2-manual-AT-review`: a manual assistive-technology check is needed in
  addition to the automated interaction test.

Do not mark a stateful component verified until the interaction test confirms
both programmatic state and application state. Keep a manual-review item open
where the screen-reader communication itself must be assessed.
