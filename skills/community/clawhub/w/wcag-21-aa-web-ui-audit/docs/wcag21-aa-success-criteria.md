# WCAG 2.1 Level A + AA Success Criteria (Web UI)

This reference lists all WCAG 2.1 Level A and Level AA success criteria (50 total), grouped by principle. For each SC, use the UI meaning and impacted component notes to speed triage and remediation.

## Perceivable

### SC 1.1.1 Non-text Content (Level A)
UI meaning: Provide text alternatives for non-text UI so assistive tech can convey purpose or outcome.
Common impacted components: Images, icons, icon-only buttons, charts, CAPTCHA, media controls.

### SC 1.2.1 Audio-only and Video-only (Prerecorded) (Level A)
UI meaning: Provide equivalent alternatives for prerecorded audio-only or video-only content.
Common impacted components: Help clips, onboarding media, support tutorials.

### SC 1.2.2 Captions (Prerecorded) (Level A)
UI meaning: Add synchronized captions for prerecorded audio content in video.
Common impacted components: Product demos, explainer videos, tutorials.

### SC 1.2.3 Audio Description or Media Alternative (Prerecorded) (Level A)
UI meaning: Provide audio description or a full text alternative for prerecorded video content.
Common impacted components: Marketing videos, walkthroughs, feature demos.

### SC 1.2.4 Captions (Live) (Level AA)
UI meaning: Provide captions for live audio content when live video/audio is used.
Common impacted components: Webinars, live events, live support broadcasts.

### SC 1.2.5 Audio Description (Prerecorded) (Level AA)
UI meaning: Provide audio description for important visual information in prerecorded video.
Common impacted components: Training videos, visual-only demonstrations.

### SC 1.3.1 Info and Relationships (Level A)
UI meaning: Preserve structural relationships programmatically so they are available beyond visual presentation.
Common impacted components: Forms, tables, headings, lists, grouped controls.

### SC 1.3.2 Meaningful Sequence (Level A)
UI meaning: Ensure reading and interaction order is meaningful when linearized.
Common impacted components: Responsive layouts, drawers, modals, multi-column forms.

### SC 1.3.3 Sensory Characteristics (Level A)
UI meaning: Do not rely only on shape, position, color, or sound in instructions.
Common impacted components: Error guidance, onboarding hints, validation prompts.

### SC 1.3.4 Orientation (Level AA)
UI meaning: Do not restrict use to only portrait or only landscape unless essential.
Common impacted components: Mobile app shells, checkout forms, dashboards.

### SC 1.3.5 Identify Input Purpose (Level AA)
UI meaning: Use programmatic input purpose tokens for common personal data fields.
Common impacted components: Sign-up, checkout, profile and billing forms.

### SC 1.4.1 Use of Color (Level A)
UI meaning: Color cannot be the only way to communicate meaning, state, or action.
Common impacted components: Validation states, charts, status labels, links.

### SC 1.4.2 Audio Control (Level A)
UI meaning: Provide a way to pause/stop/volume-control auto-playing audio over 3 seconds.
Common impacted components: Hero media, auto-play ads, embedded media.

### SC 1.4.3 Contrast (Minimum) (Level AA)
UI meaning: Maintain minimum contrast for text and images of text.
Common impacted components: Body text, form labels, button text, helper/error text.

### SC 1.4.4 Resize text (Level AA)
UI meaning: Text must be resizable to 200% without loss of content/function.
Common impacted components: Navigation bars, forms, cards, tables.

### SC 1.4.5 Images of Text (Level AA)
UI meaning: Use real text instead of images of text except for essential or customizable cases.
Common impacted components: Badges, banners, callouts, branded UI labels.

### SC 1.4.10 Reflow (Level AA)
UI meaning: Content must reflow without two-dimensional scrolling at 320 CSS px width.
Common impacted components: Data tables, filter sidebars, checkout layouts.

### SC 1.4.11 Non-text Contrast (Level AA)
UI meaning: UI components and visual indicators need sufficient contrast against adjacent colors.
Common impacted components: Focus rings, form controls, icons, chart markers.

### SC 1.4.12 Text Spacing (Level AA)
UI meaning: Content must remain usable when users apply increased text spacing overrides.
Common impacted components: Paragraph text, buttons, form hints, accordion labels.

### SC 1.4.13 Content on Hover or Focus (Level AA)
UI meaning: Hover/focus-triggered content must be dismissible, hoverable, and persistent as needed.
Common impacted components: Tooltips, menus, popovers, inline help.

## Operable

### SC 2.1.1 Keyboard (Level A)
UI meaning: All functionality must be operable via keyboard without specific timing.
Common impacted components: Menus, forms, carousels, dialogs, custom widgets.

### SC 2.1.2 No Keyboard Trap (Level A)
UI meaning: Keyboard focus must not get trapped; user can move away using standard keys.
Common impacted components: Modals, drawers, embedded widgets, editors.

### SC 2.1.4 Character Key Shortcuts (Level A)
UI meaning: Single-character shortcuts must be turn-off-able, remappable, or active only on focus.
Common impacted components: Search UIs, command palettes, rich text editors.

### SC 2.2.1 Timing Adjustable (Level A)
UI meaning: Time limits must be adjustable, extendable, or non-essential.
Common impacted components: Session timeouts, carts, OTP flows, timed quizzes.

### SC 2.2.2 Pause, Stop, Hide (Level A)
UI meaning: Moving/blinking/auto-updating content must be pausable or stoppable.
Common impacted components: Carousels, live tickers, animations, rotating promos.

### SC 2.3.1 Three Flashes or Below Threshold (Level A)
UI meaning: Avoid flashing content that can trigger seizures.
Common impacted components: Promotional animations, video effects, alerts.

### SC 2.4.1 Bypass Blocks (Level A)
UI meaning: Provide a mechanism to skip repeated blocks of content.
Common impacted components: Global navigation, repeated sidebars, page shells.

### SC 2.4.2 Page Titled (Level A)
UI meaning: Pages need descriptive titles that reflect purpose.
Common impacted components: Route templates, auth pages, checkout steps.

### SC 2.4.3 Focus Order (Level A)
UI meaning: Focus moves in a logical sequence preserving meaning and operability.
Common impacted components: Forms, modals, drawers, custom popups.

### SC 2.4.4 Link Purpose (In Context) (Level A)
UI meaning: Link purpose must be clear from text or context.
Common impacted components: Cards, pagination, table actions, footer links.

### SC 2.4.5 Multiple Ways (Level AA)
UI meaning: Provide more than one way to find pages within a set of pages.
Common impacted components: Site search, nav menus, sitemap, index pages.

### SC 2.4.6 Headings and Labels (Level AA)
UI meaning: Headings and labels must clearly describe topic or control purpose.
Common impacted components: Form labels, section headings, dialog titles.

### SC 2.4.7 Focus Visible (Level AA)
UI meaning: Keyboard focus indicator must always be visible.
Common impacted components: Buttons, links, inputs, tabs, menu items.

### SC 2.5.1 Pointer Gestures (Level A)
UI meaning: Complex multipoint/path gestures need a simple single-pointer alternative.
Common impacted components: Carousels, maps, zoom/pan views, touch controls.

### SC 2.5.2 Pointer Cancellation (Level A)
UI meaning: Prevent accidental activation by supporting abort/cancel before completion.
Common impacted components: Drag/drop, press interactions, destructive controls.

### SC 2.5.3 Label in Name (Level A)
UI meaning: Accessible name should contain visible label text.
Common impacted components: Voice-command targets, buttons, icon+text controls.

### SC 2.5.4 Motion Actuation (Level A)
UI meaning: Motion-triggered actions need UI alternatives and disable options.
Common impacted components: Shake gestures, device-tilt actions.

## Understandable

### SC 3.1.1 Language of Page (Level A)
UI meaning: Set the primary human language of each page programmatically.
Common impacted components: App shell HTML root, localized pages.

### SC 3.1.2 Language of Parts (Level AA)
UI meaning: Mark language changes within content when needed.
Common impacted components: Mixed-language content, embedded quotes, legal text.

### SC 3.2.1 On Focus (Level A)
UI meaning: Focusing a control must not trigger unexpected context changes.
Common impacted components: Menu items, form fields, auto-open popups.

### SC 3.2.2 On Input (Level A)
UI meaning: Changing input value must not unexpectedly submit/navigate without warning.
Common impacted components: Filters, selects, toggles, settings controls.

### SC 3.2.3 Consistent Navigation (Level AA)
UI meaning: Repeated navigation mechanisms should appear in consistent order.
Common impacted components: Global nav, side nav, footer nav.

### SC 3.2.4 Consistent Identification (Level AA)
UI meaning: Components with same function should be identified consistently.
Common impacted components: Reused icons, action buttons, help links.

### SC 3.3.1 Error Identification (Level A)
UI meaning: Input errors must be identified and described to users.
Common impacted components: Sign-up, checkout, profile update forms.

### SC 3.3.2 Labels or Instructions (Level A)
UI meaning: Provide labels/instructions when user input is required.
Common impacted components: Forms, payment fields, search boxes.

### SC 3.3.3 Error Suggestion (Level AA)
UI meaning: Provide suggestions for correcting input errors when possible.
Common impacted components: Email, password, address, payment forms.

### SC 3.3.4 Error Prevention (Legal, Financial, Data) (Level AA)
UI meaning: For critical submissions, provide review/confirmation/reversible safeguards.
Common impacted components: Checkout submit, account deletion, legal agreements.

## Robust

### SC 4.1.1 Parsing (Level A)
UI meaning: Markup should parse reliably without duplicate IDs or broken structure.
Common impacted components: Page templates, component libraries, SSR output.

### SC 4.1.2 Name, Role, Value (Level A)
UI meaning: Custom and native controls expose correct name, role, state, and value.
Common impacted components: Custom selects, tabs, accordions, toggles, dialogs.

### SC 4.1.3 Status Messages (Level AA)
UI meaning: Important status updates are announced programmatically without moving focus.
Common impacted components: Toasts, inline validation, cart updates, loading completion.

## Reference Notes

[^wcag21]: W3C, *Web Content Accessibility Guidelines (WCAG) 2.1*, Recommendation. Use as source of truth for SC names and levels.
[^quickref]: WAI, *How to Meet WCAG (Quick Reference)*. Use Level A + AA filtering and technique guidance for implementation choices.
[^understanding-413]: WAI, *Understanding Success Criterion 4.1.3: Status Messages*. Use for announcements such as toast confirmations, save states, and cart updates.

Reference usage: [^wcag21] [^quickref] [^understanding-413]
