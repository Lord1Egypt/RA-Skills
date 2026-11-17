# Interaction Test Plan

When the user needs E2E or UI interaction testing, generate a detailed plan BEFORE executing any tests. This prevents:

- Missing interactive behaviors (validation, loading, errors, empty states)
- Testing only happy paths
- Overlooking accessibility or keyboard interactions
- Undefined pass/fail criteria for each test

## When to Activate

- User says: E2E, 交互测试, UI testing, browser testing, 端到端测试, functional test plan
- Recommended test types include E2E
- Project has a user-facing UI (web, mobile, desktop)
- User asks "how do I test this UI"

## Phase 1: Feature Inventory

List EVERY user-facing feature, page, or flow. Do not skip anything a user can see or interact with.

### Discovery Methods

1. **Read route definitions**: `app/routes/`, `pages/`, `src/router/`, URL patterns
2. **Read component tree**: Entry components, page components, shared components
3. **Read navigation**: Menus, tabs, breadcrumbs, sidebar items
4. **Read API endpoints**: What data drives each page (forms, lists, detail views)
5. **Ask the user**: "Are there any features or workflows I haven't discovered?"

### Output: Feature List

```
1. Login page (/login)
2. Registration page (/register)
3. Dashboard (/dashboard)
4. User profile (/profile)
5. Settings (/settings)
6. ...
```

## Phase 2: Element Registry

For each feature, enumerate ALL interactive elements:

| Element Type | Examples | What to Document |
|-------------|----------|-----------------|
| Buttons | Submit, Cancel, Delete, Edit, Save | Label, action, disabled state |
| Text inputs | Email, Password, Search, Name | Placeholder, validation rules, input type |
| Textareas | Description, Comment, Bio | Char limit, auto-resize behavior |
| Selects/Dropdowns | Country, Role, Category | Options, default, multi-select support |
| Checkboxes | "Remember me", "Agree to terms" | Default state, required flag |
| Radio groups | Payment method, Shipping option | Options, default selection |
| Toggles/Switches | Dark mode, Notifications | On/off states, persistence |
| Date/Time pickers | Birthdate, Appointment | Format, range limits |
| File uploads | Avatar, Attachment | Accepted types, size limit, preview |
| Modals/Dialogs | Confirm delete, Edit details | Trigger, close methods (X, Escape, backdrop click) |
| Tooltips | Info icons, Help text | Trigger (hover/click), content |
| Drag handles | Reorder list, Resize panel | Drop targets, animation |
| Tabs | Content sections | Active indicator, lazy loading |
| Accordions | FAQ, Sections | Expand/collapse behavior |
| Infinite scroll | Feeds, Lists | Load more trigger, loading indicator |
| Search/Autocomplete | Lookup fields | Debounce, results dropdown, keyboard navigation |

## Phase 3: Behavior Catalog

For each element, document ALL behavioral states:

### Universal States (check every element)

1. **Happy path** — Correct input → expected output
2. **Validation feedback** — Invalid input → error message + visual indicator
   - Required field left empty
   - Format violation (email, phone, URL)
   - Range violation (min/max length, value)
   - Type mismatch
3. **Loading state** — What shows while data/action is in progress
   - Spinner or skeleton
   - Button disabled state
   - Progress indicator for long operations
4. **Empty state** — What shows when there is no data
   - Empty state illustration + message
   - Call to action (if applicable)
5. **Error state** — What shows when something fails
   - API error → error message or toast
   - Network error → retry option
   - Permission error → appropriate messaging
6. **Edge cases** — Unusual but valid inputs
   - Very long input (names, descriptions)
   - Special characters (Unicode, emoji)
   - Boundary values (0, -1, very large numbers)
   - Whitespace-only input
   - Leading/trailing spaces
7. **Failure paths** — What happens when backend operations fail
   - API returns 4xx (400, 401, 403, 404, 409, 422, 429)
   - API returns 5xx (500, 502, 503)
   - Partial failures (batch operations with mixed results)
   - Timeout (long-running operations exceed limit)
   - Resource limits exceeded (file too large, quota full)
8. **Boundary attacks** — Malicious or extreme input
   - XSS injection (`<script>alert(1)</script>`)
   - SQL injection fragments (`'; DROP TABLE users; --`)
   - Extremely long input (10,000+ characters)
   - Zero-width characters, control characters
   - Emoji-only input, RTL text
9. **Concurrent race conditions** — Multiple operations in flight
   - Double-click / rapid click on submit buttons
   - Form submission while previous request is still pending
   - Navigating away before operation completes
   - Same data modified by another user (optimistic concurrency)

### Interaction-Specific Behaviors

| Element | Extra Checks |
|---------|-------------|
| Form submission | Double-submit prevention, unsaved changes warning |
| Modal/Dialog | Focus trap, Escape to close, backdrop click to close, scroll lock |
| Dropdown/Select | Keyboard navigation (Arrow keys, Enter, Escape), option filtering |
| Drag and drop | Visual feedback during drag, valid drop zones, cancel behavior |
| File upload | Drag-to-upload zone, progress bar, cancel upload, invalid file feedback |
| Search | Debounce timing, clear button, "no results" state, keyboard shortcut |

## Phase 4: Test Plan Output

```markdown
## Interaction Test Plan: {project}

### Feature: {feature name} ({route})

| # | Element | Selector | Action | Expected Behavior | State Type |
|---|---------|----------|--------|-------------------|------------|
| 1 | Email input | `getByLabel('Email')` | Leave empty, click Submit | Shows "Email is required" error, red border | Validation |
| 2 | Email input | `getByLabel('Email')` | Type "not-an-email" | Shows "Invalid email format" | Validation |
| 3 | Email input | `getByLabel('Email')` | Type "user@example.com" | No error, green checkmark | Happy path |
| 4 | Password input | `getByLabel('Password')` | Type 5 characters | Shows "Minimum 8 characters" | Validation |
| 5 | Password input | `getByLabel('Password')` | Type 8+ characters | No error | Happy path |
| 6 | Submit button | `getByRole('button', { name: 'Submit' })` | Click with valid form | Button shows spinner, fields disabled | Loading |
| 7 | Submit button | `getByRole('button', { name: 'Submit' })` | Click, API returns 500 | Shows toast "Something went wrong. Try again." | Error |
| 8 | Submit button | `getByRole('button', { name: 'Submit' })` | Click twice rapidly | Second click ignored (disabled state) | Concurrent |
| 9 | Submit button | `getByRole('button', { name: 'Submit' })` | Click, API returns 401 | Shows "Invalid credentials" message | Failure path |
| 10 | Email input | `getByLabel('Email')` | Type `<script>alert(1)</script>` | Input sanitized, shows validation error | Boundary attack |
| 11 | Login form | — | Tab through all fields | Focus order: Email → Password → Submit → Forgot password | Accessibility |

### Feature: {next feature}
...
```

## Phase 5: Execution

After generating the test plan, proceed to execution directly:

1. **Code mode (default)**: Load `references/e2e-test-execution.md` and convert the test plan
   into Playwright `.spec.ts` files. Each row in the plan becomes a `test()` block with
   concrete selectors, actions, and assertions. Run the tests and capture results.
2. **Live operation mode** (when user explicitly requests interactive verification):
   Invoke the Agent Browser skill with the test plan for step-by-step browser automation.

After execution, produce the **QA Report** (see `references/e2e-test-execution.md` Part 8).

## Remember

- **Happy path is the minimum, not the plan.** Every element has at least 3 states.
- **Validation states are often the most bug-prone** — give them extra attention.
- **Failure paths are mandatory** — test what happens when things go wrong, not just when they go right.
- **Boundary attacks are mandatory for input elements** — XSS, injection, extreme length.
- **Concurrent operations must be tested for submit actions** — double-click, race conditions.
- **Ask the user** if there are features or edge cases you haven't discovered.
- **Use the Selector column** to write Playwright locators directly from the plan.
