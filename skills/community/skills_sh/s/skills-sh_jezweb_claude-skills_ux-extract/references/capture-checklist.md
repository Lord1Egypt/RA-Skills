# Capture Checklist

Per-pattern checklist of what to screenshot and note during extraction. Use as a walking reference while browsing the target app.

## Per-Route Baseline

On arriving at every route, before interacting:

- [ ] Screenshot at 1440×900 (baseline)
- [ ] Read the `<h1>` and note the page title style
- [ ] Note the URL pattern (semantic? slug? numeric ID?)
- [ ] Check for breadcrumbs — screenshot if present
- [ ] Check the browser console for errors (mentionable but not central to extract)
- [ ] Note page load time impression (instant / skeleton shown / slow)

## Lists & Tables

- [ ] Empty state (0 items)
- [ ] Populated state (many items)
- [ ] Row hover (trigger hover on a non-first row to see non-edge styling)
- [ ] Row selection (click checkbox, capture with action bar visible)
- [ ] Multi-selection (select 5+ rows)
- [ ] Sort: click a column header, capture the sorted state and the sort indicator
- [ ] Filter: apply one filter, capture; apply two, capture; clear all
- [ ] Search: type a query matching items, capture results; type garbage, capture no-results
- [ ] Pagination: at page 1, page 2, last page; change items-per-page
- [ ] Action menu on a row: hover or click the overflow menu, capture open
- [ ] Row click: capture the detail or drawer that opens

## Forms

- [ ] Default state (empty form, no interactions)
- [ ] Focused field (tab into one, note focus indicator)
- [ ] Partially filled (some valid, some empty)
- [ ] Validation error: submit with bad data or leave required field empty, screenshot the error
- [ ] Inline help text visible (hover or focus a help icon if present)
- [ ] Disabled state (fields that grey out based on other choices)
- [ ] Success state (after submission, capture the confirmation)
- [ ] Submit button: default, hover, active (mid-click), loading, disabled
- [ ] Cancel behaviour: click cancel from a dirty form — does it warn?

## Buttons

- [ ] Default
- [ ] Hover
- [ ] Focus (via Tab)
- [ ] Active (click and hold)
- [ ] Loading (click a button that triggers an async action, capture mid-load)
- [ ] Disabled
- [ ] All variants: primary, secondary, destructive, ghost, icon-only

## Modals & Dialogs

- [ ] Trigger: screenshot the button/link that opens the modal (before click)
- [ ] Open: modal fully visible with backdrop
- [ ] Focused field inside modal
- [ ] Filled and validated (if it has a form)
- [ ] Error state (form error inside modal)
- [ ] Success: post-submit confirmation (toast? modal replaces content?)
- [ ] Close methods tested: X button, Escape key, backdrop click
- [ ] Animation: record a GIF of open + close (`gif_creator`, 3 seconds)
- [ ] Nested modals if they exist (confirmation inside an edit modal)

## Confirmation Dialogs (destructive)

- [ ] Trigger the destructive action
- [ ] Capture the confirmation dialog with the exact copy visible
- [ ] Note the button placement (destructive left vs right)
- [ ] Note the destructive button style (red fill? outline? which variant?)
- [ ] Note default keyboard focus (on Cancel or on Destroy?)
- [ ] Cancel flow: click cancel, verify nothing destructive happened
- [ ] Do NOT complete destructive actions without explicit user approval

## Navigation

- [ ] Primary nav: default state, hover on an item, focus via Tab
- [ ] Current page indicator: how is the active item visually marked?
- [ ] Sub-nav / tabs: default and active states
- [ ] Collapsed/expanded nav (if it has a toggle)
- [ ] Mobile hamburger: tap trigger, drawer open, drawer close
- [ ] User menu: click user avatar, capture the menu open

## Empty States

For every route that can be empty:

- [ ] Capture with zero data
- [ ] Note: illustration? headline? description? CTA? secondary link?
- [ ] Copy the text verbatim
- [ ] If CTA is present, click it and capture what happens next

## Error States

- [ ] Inline form error (invalid input)
- [ ] Field-level error message position and styling
- [ ] Page-level error banner (e.g. after a failed save)
- [ ] Toast error
- [ ] 404 page: navigate to `/nonsense-route-12345`
- [ ] 403 / permission denied page (if you can trigger one)
- [ ] 500 / server error (rare — screenshot if you see one)
- [ ] Network-offline behaviour if you can simulate it (DevTools throttle → offline)

## Loading States

- [ ] Skeleton: reload a data-heavy page and capture the skeleton before data arrives
- [ ] Spinner: trigger a slow action and capture
- [ ] Progress bar: if you can trigger a known-slow operation (file upload, bulk action)
- [ ] Step indicator: multi-step flows, capture at steps 1, 2, 3

## Feedback

- [ ] Toast: trigger a save, screenshot the toast (and capture the copy verbatim)
- [ ] Toast variants: success, info, warning, error — trigger each if possible
- [ ] Inline confirmation (e.g. "Copied" next to a copy button)
- [ ] Unsaved-changes warning: try to navigate away from a dirty form

## Keyboard

- [ ] Press `?` and `Cmd+/` — does a shortcut sheet appear? Screenshot it
- [ ] Press `Cmd+K` — does a command palette open? Screenshot default state and with a query typed
- [ ] Tab through the page, screenshot the focus indicator on different element types (button, input, link, card)
- [ ] Try app-specific shortcuts from the sheet — verify they work
- [ ] Escape key: does it close modals? Clear search? Do something unexpected?

## Motion (record GIFs)

- [ ] Page transition between two main routes
- [ ] Modal open and close
- [ ] Toast appearing
- [ ] List item being added (submit a form that adds to a visible list)
- [ ] List item being deleted
- [ ] Skeleton → populated crossfade
- [ ] Any celebratory moments (upgrade success, onboarding milestone)
- [ ] Hover animations on cards or buttons if they have any (not just colour change)

## Responsive (repeat key captures at each width)

- [ ] 768px: nav behaviour, form layout, table-to-card transition
- [ ] 375px: mobile nav, floating buttons, bottom sheets, full-screen modals
- [ ] Note any width where the layout obviously breaks or transitions awkwardly — screenshot it

## Dark Mode (repeat key captures)

- [ ] Home / dashboard
- [ ] A list view
- [ ] A detail view
- [ ] A modal
- [ ] An empty state
- [ ] An error state (often forgotten in dark mode design)

## Permissions (if you can test multiple roles)

- [ ] Log in as lowest-privilege role
- [ ] Screenshot what's different in the nav
- [ ] Try to access a denied page directly (paste URL)
- [ ] Note what message/UX you get
- [ ] Try to take an action you shouldn't be able to — what happens?
- [ ] Log back in as admin; note items that were hidden

## Copy Corpus

Throughout the extraction, capture the exact text of:

- [ ] Every button label
- [ ] Every empty-state message
- [ ] Every error message (inline, toast, page)
- [ ] Every confirmation dialog
- [ ] Every tooltip
- [ ] Every placeholder
- [ ] Headings on main pages
- [ ] Onboarding copy (welcome messages, tour steps)
- [ ] Success messages
- [ ] Footer copy, legal text (quickly note but don't analyse)

Save these in `copy-corpus.md`, grouped by page or by category.

## Things to explicitly *not* do

- Don't scrape content rapidly with automation — act like a human
- Don't save or redistribute screenshots of copyrighted content (illustrations, logos) beyond internal reference
- Don't attempt to access paid features without a paid account
- Don't extract from apps that explicitly prohibit inspection in their ToS
- Don't complete real destructive actions on a live reference account — use a test account or stop at the confirmation dialog
