# UI Component Checklists (WCAG 2.1 A + AA)

Use these checklists during manual audits and remediation. Every item is action-oriented and maps to explicit WCAG SC IDs.

## Navigation
- [ ] Provide a visible skip link to main content for keyboard users. (SC 2.4.1, 2.4.7)
- [ ] Ensure primary navigation is fully keyboard operable. (SC 2.1.1)
- [ ] Ensure keyboard focus order in navigation matches visual/logical order. (SC 2.4.3)
- [ ] Ensure current page/location is programmatically exposed (for example `aria-current`). (SC 1.3.1, 4.1.2)
- [ ] Keep navigation mechanism order consistent across pages. (SC 3.2.3)
- [ ] Ensure link text in nav communicates destination. (SC 2.4.4)

## Header
- [ ] Ensure logo/home control has an appropriate accessible name and purpose. (SC 1.1.1, 2.4.4)
- [ ] Ensure page has descriptive title and heading hierarchy starting at top-level content. (SC 2.4.2, 2.4.6, 1.3.1)
- [ ] Ensure header controls (search/account/menu) are keyboard operable and focus visible. (SC 2.1.1, 2.4.7)
- [ ] Ensure sticky header does not obscure focused content at zoom/reflow states. (SC 1.4.10, 2.4.7)
- [ ] Ensure language selector announces state/value clearly. (SC 3.1.1, 4.1.2)

## Footer
- [ ] Mark footer as a landmark and keep structure semantic. (SC 1.3.1)
- [ ] Ensure repeated footer links have clear purpose in context. (SC 2.4.4)
- [ ] Ensure footer text and links meet minimum contrast. (SC 1.4.3)
- [ ] Ensure footer focus styles are visible in keyboard navigation. (SC 2.4.7)

## Links and Buttons
- [ ] Use native links for navigation and native buttons for actions. (SC 4.1.2)
- [ ] Ensure visible label matches or is contained in accessible name. (SC 2.5.3, 4.1.2)
- [ ] Ensure icon-only controls have meaningful text alternatives. (SC 1.1.1, 4.1.2)
- [ ] Ensure link/button text purpose is clear without ambiguous wording. (SC 2.4.4, 2.4.6)
- [ ] Ensure keyboard focus indicator is always visible and sufficiently contrasted. (SC 2.4.7, 1.4.11)
- [ ] Ensure disabled and active states are not conveyed by color alone. (SC 1.4.1)

## Forms
- [ ] Provide persistent labels for all inputs (not placeholder-only). (SC 3.3.2, 1.3.1)
- [ ] Associate labels, helper text, and errors programmatically. (SC 1.3.1, 4.1.2)
- [ ] Identify required fields and expected format with instructions. (SC 3.3.2)
- [ ] Expose errors with specific field-level identification. (SC 3.3.1)
- [ ] Provide actionable error suggestions where possible. (SC 3.3.3)
- [ ] For legal/financial/data submissions, provide review/confirm/reversible step. (SC 3.3.4)
- [ ] Ensure form error states are not color-only signals. (SC 1.4.1)
- [ ] Ensure personal-data fields use appropriate autocomplete purpose tokens. (SC 1.3.5)
- [ ] Ensure logical tab order and visible focus across all fields and controls. (SC 2.4.3, 2.4.7)

## Modal and Dialog
- [ ] Use semantic dialog role and accessible name for every modal. (SC 1.3.1, 4.1.2)
- [ ] Move focus into modal on open and return focus to trigger on close. (SC 2.4.3)
- [ ] Keep keyboard focus constrained within modal while open, without trapping user permanently. (SC 2.1.2, 2.1.1)
- [ ] Ensure modal is dismissible via keyboard (for example `Esc` or close button). (SC 2.1.1)
- [ ] Ensure modal content remains usable at zoom and narrow viewport widths. (SC 1.4.10, 1.4.4)

## Drawer
- [ ] Ensure drawer trigger and close controls have clear accessible names. (SC 4.1.2, 2.4.6)
- [ ] Move focus into drawer on open and restore on close. (SC 2.4.3)
- [ ] Prevent focus from moving behind open drawer content. (SC 2.1.2, 2.4.3)
- [ ] Ensure all drawer actions are keyboard operable and visibly focused. (SC 2.1.1, 2.4.7)
- [ ] Ensure drawer content reflows without horizontal scrolling at 320 CSS px. (SC 1.4.10)

## Tooltip and Popover
- [ ] Ensure supplemental content appears on keyboard focus as well as hover when relevant. (SC 1.4.13, 2.1.1)
- [ ] Ensure content is dismissible without moving pointer/focus unpredictably. (SC 1.4.13)
- [ ] Ensure pointer can move over revealed content without it disappearing unexpectedly. (SC 1.4.13)
- [ ] Ensure focus-triggered popovers do not trigger unexpected context changes. (SC 3.2.1)
- [ ] Ensure trigger control has appropriate role, name, and expanded state. (SC 4.1.2)

## Toast and Status
- [ ] Expose non-blocking status updates through programmatic announcements (for example `role=status`). (SC 4.1.3)
- [ ] Expose urgent errors through assertive announcements when appropriate (for example `role=alert`). (SC 4.1.3)
- [ ] Do not move focus for passive confirmations unless task-critical. (SC 3.2.1, 4.1.3)
- [ ] Ensure toast text contrast and icon contrast meet minimums. (SC 1.4.3, 1.4.11)
- [ ] Ensure toast timing supports comprehension and does not remove critical info too quickly. (SC 2.2.1)

## Tabs
- [ ] Implement tablist/tab/tabpanel semantics correctly. (SC 1.3.1, 4.1.2)
- [ ] Ensure keyboard navigation supports expected tab interactions. (SC 2.1.1)
- [ ] Ensure selected tab state is programmatically exposed. (SC 4.1.2)
- [ ] Ensure tab focus indicator is visible and contrasted. (SC 2.4.7, 1.4.11)
- [ ] Ensure tab labels clearly describe associated panel content. (SC 2.4.6)

## Accordion
- [ ] Use button semantics for expandable headers with proper state attributes. (SC 4.1.2)
- [ ] Ensure accordion headers are keyboard operable. (SC 2.1.1)
- [ ] Ensure focus order remains logical when panels expand/collapse. (SC 2.4.3)
- [ ] Ensure expanded/collapsed state is not color-only. (SC 1.4.1)
- [ ] Ensure heading/label wording is clear and consistent. (SC 2.4.6, 3.2.4)

## Carousel
- [ ] Provide pause/stop controls for auto-rotating slides. (SC 2.2.2)
- [ ] Ensure slide controls are keyboard operable with visible focus. (SC 2.1.1, 2.4.7)
- [ ] Ensure previous/next controls have clear names and roles. (SC 4.1.2, 2.4.4)
- [ ] Ensure slide change announcements are exposed when needed for context. (SC 4.1.3)
- [ ] Ensure swipe-only gestures have single-pointer alternatives. (SC 2.5.1)
- [ ] Ensure non-essential motion can be avoided or controlled. (SC 2.5.4)

## Table
- [ ] Use semantic table markup with header associations. (SC 1.3.1)
- [ ] Ensure table caption/summary communicates table purpose. (SC 2.4.6)
- [ ] Ensure sortable/filter controls in headers are keyboard operable and named. (SC 2.1.1, 4.1.2)
- [ ] Ensure focus order across interactive table controls is logical. (SC 2.4.3)
- [ ] Ensure status changes (sorting/filtering updates) are announced when needed. (SC 4.1.3)
- [ ] Ensure table layout supports reflow at narrow widths without loss of function. (SC 1.4.10)

## Search and Filter
- [ ] Ensure search input has explicit label and purpose. (SC 3.3.2, 4.1.2)
- [ ] Ensure keyboard-only users can apply and clear filters. (SC 2.1.1)
- [ ] Ensure selected filter states are exposed programmatically. (SC 1.3.1, 4.1.2)
- [ ] Ensure result counts/updates are announced as status messages when dynamically updated. (SC 4.1.3)
- [ ] Ensure filter controls do not trigger unexpected navigation on focus/input. (SC 3.2.1, 3.2.2)
- [ ] Ensure chip/badge and control contrast is sufficient. (SC 1.4.3, 1.4.11)

## Pagination
- [ ] Wrap pagination in a navigation landmark with clear label. (SC 1.3.1, 2.4.1)
- [ ] Ensure current page is programmatically indicated. (SC 4.1.2)
- [ ] Ensure page link text communicates destination and order. (SC 2.4.4)
- [ ] Ensure keyboard focus remains visible on page controls. (SC 2.4.7)
- [ ] Ensure multiple navigation paths exist for large result sets. (SC 2.4.5)

## Rich Media
- [ ] Provide captions for prerecorded and live video audio where applicable. (SC 1.2.2, 1.2.4)
- [ ] Provide audio description or media alternatives for prerecorded visual information. (SC 1.2.3, 1.2.5)
- [ ] Provide alternatives for audio-only and video-only media. (SC 1.2.1)
- [ ] Ensure media player controls are keyboard operable and named. (SC 2.1.1, 4.1.2)
- [ ] Provide controls for auto-playing audio over 3 seconds. (SC 1.4.2)
- [ ] Avoid flashing content above seizure thresholds. (SC 2.3.1)
- [ ] Ensure controls and captions remain usable at zoom/reflow settings. (SC 1.4.4, 1.4.10)
