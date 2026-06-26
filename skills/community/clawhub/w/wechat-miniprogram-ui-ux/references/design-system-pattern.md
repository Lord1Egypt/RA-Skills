# Design-System Pattern For Mini Programs

This reference borrows the useful parts of `ui-ux-pro-max`: generate a small design system first, filter anti-patterns, then implement.

## Compact Design-System Template

Before editing UI code, define:

- Product/page type
- User goal
- Page pattern
- Visual tone
- Accent color
- Neutral palette
- Typography hierarchy
- Spacing scale
- Card/button/input style
- Feedback style
- Anti-patterns to avoid

## Recommended Page Patterns

### Task-first detail page

Best for dish, order, item, booking, ticket, profile action screens.

- Hero or summary block
- Trust/context block
- Key metadata
- Primary CTA
- Secondary detail

### Scan-first list page

Best for menus, feeds, order lists, favorites.

- Short header
- Filters or tabs only when needed
- High-signal cards
- Sticky summary only if it helps action completion

### Sectioned form page

Best for edit, create, apply, review flows.

- Intro context
- Sectioned inputs
- Inline help
- Persistent or bottom submit action

### Role-aware management page

Best for merchant, admin, reviewer, approver flows.

- Identity and status first
- Allowed actions grouped by priority
- Destructive actions isolated
- Permission reasoning visible

## Anti-Pattern Filter

Reject or tone down any direction that introduces:

- Desktop dashboard density on a phone screen
- Hard-to-read text over photos
- Excessive motion on task pages
- More than one “primary” button in the same region
- Decoration that weakens hierarchy
- Hidden state transitions

## Delivery Checklist

- One sentence summary of page intent
- One primary CTA
- Mobile-first hierarchy
- State coverage
- WeChat-consistent navigation expectations
- Readable contrast
- Safe-area aware bottom actions
