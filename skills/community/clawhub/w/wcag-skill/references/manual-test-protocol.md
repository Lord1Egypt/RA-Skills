# Mandatory human-test protocol

Complete this protocol for every AAA audit and record the result in the evidence
matrix. Test every route, responsive variation, overlay, error path, and
third-party flow in scope. Mark a test not applicable only with a rationale.

## Keyboard and focus

1. Use only Tab, Shift+Tab, Enter, Space, Escape, arrow keys, and native
   shortcuts where relevant. Reach and operate every function without a trap.
2. Record the focus order through menus, modals, disclosures, custom widgets,
   validation errors, and dynamically added content. Ensure it follows a
   meaningful reading and operation order.
3. At every breakpoint and scroll position, confirm focus is fully visible,
   unobscured by sticky/overlay content, and meets the AAA focus-area and
   contrast requirements.

## Responsive and visual presentation

1. Test text resize to 200%, then reflow at 320 CSS pixels or 400% browser zoom
   without ordinary two-dimensional scrolling, clipping, overlap, or loss of
   content/function.
2. Apply the WCAG text-spacing override: line height 1.5, paragraph spacing 2,
   letter spacing 0.12em, and word spacing 0.16em. Confirm content and controls
   still work.
3. Measure every rendered text/background pair and every interactive state.
   Review text over images, transparency, gradients, charts, and canvases
   separately; do not infer contrast from a parent background.

## Motion, timing, and media

1. Enable reduced motion and confirm non-essential motion stops or is reduced.
2. Test time limits, interruption controls, reauthentication, and inactivity
   timeouts with entered data. Verify the relevant AAA preservation rules.
3. Review all video, audio, animation, and live media against the applicable
   captions, description, transcript, sign-language, and media-alternative rows.
4. Inspect flashing or rapidly changing content for seizure risk and provide a
   pause/stop/hide mechanism for applicable moving content.

## Forms, authentication, and understanding

1. Trigger each validation error. Confirm the error is identified in text,
   linked to the control where appropriate, preserves valid entries, and can be
   corrected by keyboard and assistive technology.
2. For every page that requires users to submit information, verify at least
   one SC 3.3.6 safeguard: submissions are reversible; entered data is checked
   for input errors (required information omitted or values outside the
   required format or allowed values) with an opportunity to correct them; or
   users can review, confirm, and correct information before finalizing.
   Record which alternative is met. Test consequential workflows only in an
   authorized staging/test environment with synthetic records and sandbox
   payments; do not perform live transactions, legal commitments, or record
   changes without explicit authorization. If safe testing is unavailable,
   inspect the available evidence and record any test limitation rather than
   executing a consequential action.
   Record authorization scope: environment, permitted operations, synthetic
   records, and transaction limits. Use read-only accounts for inspection and
   narrowly scoped test accounts for state-changing tests; enforce restrictions
   through the application/provider or tool host, not this document. Mock or
   staging success is evidence for that environment, not proof of production
   behavior. Record unexecuted checks as `Needs human review`, not `Pass` or
   `Not applicable`.
3. Test every authentication step with password-manager paste, copy/paste, and
   an alternative that avoids disallowed cognitive tests.
4. Review help, labels, instructions, unusual words, abbreviations, reading
   level, and pronunciation needs for the actual audience and task.

## Assistive technology and reporting

Test custom widgets, live regions, dialogs, dynamic errors, and complex controls
with at least one supported browser/screen-reader pair. Verify accessible names,
roles, values, state changes, announcements, and return-focus behaviour. Record
browser, assistive technology, version, date, tested route/state, and observed
result. Include disabled users in usability testing when possible; automated and
functional checks alone do not establish real-world usability.
