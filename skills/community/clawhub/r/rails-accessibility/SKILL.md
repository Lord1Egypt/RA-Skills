---
name: rails-accessibility
description: "Practical a11y patterns for Rails/Stimulus/Hotwire apps - ERB partials, axe-core CI, color contrast, modals, dynamic content. Not WCAG theory. Use when: building or auditing accessible forms, modals, navigation, or live-updating content; setting up axe-core in CI or RSpec; fixing Tailwind/oklch contrast failures; making Turbo Frame/Stream updates announce to screen readers; or when an accessibility spec breaks because public-page copy changed."
metadata: {"clawdbot":{"emoji":"♿","requires":{"bins":["bundle"]},"os":["linux","darwin","win32"],"version":"1.0.0"}}
---

# Rails Accessibility

Practical accessibility patterns for Rails 7+/8+ apps using Stimulus, Hotwire (Turbo), and Tailwind CSS. Not WCAG theory - actual ERB components, Stimulus controllers, and CI guardrails you drop in.

## When to Use

- Building or auditing a Rails app for accessibility
- Setting up automated a11y checks in CI (axe-core + RSpec)
- Implementing accessible forms, modals, navigation, or dynamic content
- Fixing color contrast issues in Tailwind/oklch color systems
- Adding screen-reader-friendly Turbo Frame / Turbo Stream interactions

## Philosophy

**Catch it in CI, not in production.** The patterns here are useful, but the real win is the axe-core RSpec matcher that runs on every `bin/rspec` - same as any other test failure. If it's not in CI, it doesn't exist.

**Patterns over gems.** These ERB partials and Stimulus controllers are meant to be copied into your app and adapted to your design system. They're not a gem - they're a starting point. Your Tailwind config, error styling, and i18n setup will differ.

**Test what users experience.** System specs with `driven_by(:selenium_headless)` can catch real a11y issues that static analysis misses. The axe-core matcher runs in the browser, not on the server.

## Quick Start

The axe-core + Capybara + system-spec setup in `references/testing.md` is the one file worth reading end to end on first use - it walks Gemfile additions, `AxeHelper`, Capybara driver config, the smoke test pattern, and the Devise sign-in gotcha.

## Reference Docs

Each reference covers one task. Read the one that matches what you're building, not all six.

- `references/forms.md` - Accessible form fields, error states, labels, Turbo gotchas
- `references/modals.md` - Focus trap, `aria-modal`, `role="dialog"`, ESC to close, Turbo Frame modal pattern
- `references/navigation.md` - Skip links, landmark roles, current-page indicator, mobile menu, breadcrumbs
- `references/dynamic-content.md` - `aria-live`, Turbo Frame/Stream announcements, flash messages, error summary focus
- `references/color-contrast.md` - oklch chroma rules, Tailwind shades that fail AA, dark mode
- `references/testing.md` - axe-core + RSpec + Capybara setup, smoke test pattern, per-rule skips, Devise sign-in gotcha

## Examples

- `examples/modal_controller.js` - Stimulus controller for accessible modals (the only standalone file worth keeping - drop straight into `app/javascript/controllers/`). The accessible field partial, skip link, and full axe system spec live as code blocks inside `references/forms.md`, `references/navigation.md`, and `references/testing.md` respectively, since they're tightly coupled to the surrounding explanation.

## Common Gotchas

### oklch chroma threshold

Tailwind's oklch color system can produce colors that look fine but fail WCAG AA. The full rule and the chroma-threshold table live in `references/color-contrast.md`; the one-line version: keep chroma <= 0.03 on text colors over light backgrounds. Above 0.04 almost certainly fails.

### aria-expanded without role="combobox"

`aria-expanded` on an input signals a combobox pattern, but axe-core requires `role="combobox"` on the same element. Having `aria-expanded` alone is a WCAG violation.

**Fix:** Add `role="combobox"` to any input with `aria-expanded`.

### Turbo Frame redirects break outside frame context

When a form inside `<turbo-frame id="modal">` redirects to a URL outside the frame, Turbo generates broken `GET /original-path/undefined` requests. Two related rules:

- Use `data: { turbo: false }` on forms that do full-page navigation (password changes, sign-out). Full pattern in `references/modals.md`.
- `data-turbo-frame` overrides `data-turbo="false"` - if both are present, Turbo processes within the frame and ignores the opt-out. Full pattern in `references/forms.md`.

### System spec sign_in failures in headless Chrome

Devise's `sign_in` test helper can silently fail in `driven_by(:selenium_headless)` - the session cookie doesn't transfer to the browser process. Use form-based sign-in (`visit new_user_session_path; fill_in ...; click_button`) instead. Full diagnosis in `references/testing.md`.

### Accessibility specs break when page copy changes

Screen-reader UX specs and other a11y checks often assert on exact page titles, h1 text, or landmark labels. When you change i18n keys or marketing copy, those assertions fail even though the page is still accessible.

**Example:** a screen-reader UX spec asserts:

```ruby
expect(page.title).to include("AI agents")
expect(page).to have_css("h1", text: /AI agents/i, visible: :all)
```

If the page title and h1 are changed to "AI assistants" / "Use your AI assistant.", the spec breaks with:

```
expected "AI assistants on Example · Example" to include "AI agents"
```

**Procedure when changing public-page copy:**

1. Search for the old text in `spec/system/` and `spec/requests/`:

   ```bash
   grep -R -n "old title text" spec/
   ```

2. Update any screen-reader, accessibility, or page-title specs that assert on that exact string.
3. Run the affected accessibility / screen-reader specs before pushing.

Do not rely on the general request spec suite to catch title/h1 mismatches - those specs often live in dedicated accessibility files and may not be included in a scoped run.

### Turbo Frame click_link race in system specs

`click_link` on a `data: { turbo_frame: "..." }` link returns before the async frame-swap resolves. Capybara's default 2s wait doesn't cover it, so the next `fill_in` runs against a frame that still has `aria-busy="true"` and no body - the failure looks like "field missing" but the controller is fine. Confirm with a direct rack-test request to the same endpoint (returns the full form), then wait for frame content (`have_selector("turbo-frame#modal form", wait: 10)`) instead of the frame element, or switch modal-flow tests to `:rack_test`. Full pattern in `references/testing.md`.

## Related

The reference docs and example above are this skill's complete content. Each reference covers a distinct triggering task (forms / modals / navigation / dynamic content / color contrast / testing). This file is the entry point.
