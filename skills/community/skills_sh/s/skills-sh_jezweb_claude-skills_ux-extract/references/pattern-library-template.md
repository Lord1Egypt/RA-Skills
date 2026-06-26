# Pattern Library Output Template

Structure for the pattern library produced by `ux-extract`. Write to `docs/ux-extracts/<app-name>/pattern-library.md`.

```markdown
# Pattern Library: [App Name]

**Extracted**: YYYY-MM-DD
**URL**: https://app.example.com
**Scope**: [Whole app / Settings flow / Empty states only / etc.]
**Focus lens**: [optional — e.g. "data-heavy lists"]
**Viewport captured**: 1440×900 baseline + 768 + 375
**Browser**: Chrome MCP / Playwright
**Screenshots**: [N] in `./screenshots/`

## Contents

1. [Wayfinding](#wayfinding)
2. [Lists & Tables](#lists--tables)
3. [Forms](#forms)
4. [Modals & Dialogs](#modals--dialogs)
5. [Feedback](#feedback)
6. [Onboarding & Empty States](#onboarding--empty-states)
7. [Permissions & Roles](#permissions--roles)
8. [Copy & Microcopy](#copy--microcopy)
9. [Keyboard](#keyboard)
10. [Motion](#motion)
11. [Responsive](#responsive)
12. [Notable Absences](#notable-absences)

---

## Wayfinding

### Primary Navigation
- **Layout**: [sidebar / top bar / hybrid]
- **Width / height**: [specific values observed]
- **Sections**: [list each section with its items]
- **Current-location indicator**: [bold text / background fill / border / left-edge stripe]
- **Collapse behaviour**: [at what breakpoint does it collapse? to what?]
- **Screenshots**: `screenshots/010-nav-default.png`, `screenshots/011-nav-collapsed.png`, `screenshots/012-nav-mobile-drawer.png`
- **Used on**: every page

### Breadcrumbs
- **Present**: Yes / No / Partial (only on N routes)
- **Style**: [separator character, truncation behaviour, home icon present?]
- **Example**: `Home › Clients › Jenny O'Brien › Policy #123`
- **Screenshots**: `screenshots/020-breadcrumb.png`
- **Used on**: detail pages

### Back Navigation
- **Explicit back button**: [present / absent / contextual]
- **Browser back**: [preserves filters? / resets view?]
- **Deep links**: [all routes linkable / some require navigation from parent]

---

## Lists & Tables

### List Row (primary pattern)
- **Height**: 56px
- **Layout**: `[Avatar] [Name + subtitle stack] [Metadata columns] [Actions on hover]`
- **Hover state**: background fill, action buttons fade in on right
- **Selected state**: left-edge stripe in accent colour, subtle background tint
- **Click target**: entire row → navigates to detail
- **Screenshots**: `screenshots/100-list-row-default.png`, `screenshots/101-list-row-hover.png`, `screenshots/102-list-row-selected.png`
- **Used on**: /clients, /projects, /invoices, /team (4 occurrences)
- **Variants**:
  - *Compact* (32px height) on /settings/integrations
  - *Dense* with 2 lines of subtitle on /reports

### Table (data-heavy)
- **Used instead of list when**: [N+ columns, user needs to scan comparatively]
- **Header**: sticky on scroll, sortable indicators on clickable columns
- **Row**: [same as list row or different?]
- **Selection**: checkbox column, select-all in header, count shown in action bar
- **Action bar**: appears at top when rows selected, with [Actions] [Export] [Delete] buttons
- **Screenshots**: `screenshots/110-table-default.png`, `screenshots/111-table-selection.png`, `screenshots/112-table-action-bar.png`

### Filters
- **Style**: [chip filters / sidebar / toolbar dropdown]
- **Multi-select**: Y/N
- **Active filter display**: [chips at top / text summary / counter badge]
- **Clear all**: [present / absent]
- **URL reflection**: [filters in query string? reload-safe?]
- **Screenshots**: `screenshots/120-filters-default.png`, `screenshots/121-filters-active.png`

### Pagination
- **Style**: [page numbers / prev-next / infinite scroll / load more]
- **Items per page**: [options: 25, 50, 100]
- **Position**: bottom-right
- **Deep link to page N**: [works / redirects to 1]

### Empty State (list)
- **Layout**: centred, with illustration, headline, description, CTA button
- **Copy example**: *"No clients yet"* / *"Add your first client to see them here"*
- **CTA**: `"Add Client"` (primary style)
- **Screenshots**: `screenshots/130-empty-list.png`

---

## Forms

### Field Layout
- **Label position**: above input
- **Required marker**: asterisk in accent colour, after label text
- **Help text position**: below input, muted
- **Error text position**: below input, replaces help text, red
- **Inline validation**: on blur (not on keystroke)
- **Screenshots**: `screenshots/200-form-default.png`, `screenshots/201-form-error.png`

### Input Styles
- **Height**: 40px standard, 48px large (for primary CTAs like search)
- **Border**: 1px neutral, 2px accent on focus
- **Rounded corners**: 8px
- **Focus ring**: 2px accent offset by 2px

### Buttons
- **Primary**: accent fill, white text, 40px height, 12px h-padding
- **Secondary**: neutral outline, dark text
- **Destructive**: red fill on solid / red text on outline
- **Disabled**: 40% opacity
- **Loading state**: spinner replaces label, button remains same width
- **Copy style**: verb-first, specific (`"Save Client"` not `"Save"`)
- **Screenshots**: `screenshots/210-button-primary.png` through `215-button-disabled.png`

### Form Feedback
- **Save confirmation**: toast top-right, dismisses after 3s
- **Unsaved changes warning**: browser beforeunload on form with dirty state
- **Autosave**: [present / absent — where used]

---

## Modals & Dialogs

### Modal Chrome
- **Backdrop**: 60% black overlay, blur 4px
- **Sizing**: 560px wide default, max-height 80vh with scroll
- **Position**: centred horizontally, 10vh from top
- **Close**: X top-right + Escape key + click backdrop
- **Focus**: auto-focused on first input, trapped within modal
- **Animation**: fade + slight scale-up on enter (150ms), fade on exit
- **Screenshots**: `screenshots/300-modal-open.png`, `screenshots/301-modal-form.png`

### Confirmation Dialog
- **Used for**: destructive actions (delete, archive, revoke)
- **Copy pattern**: *"[Verb] [specific thing]? [Consequence]. This [can / cannot] be undone."*
  - Example: *"Delete Jenny O'Brien? 3 policies will also be removed. This cannot be undone."*
- **Buttons**: destructive action on right in red, cancel on left in neutral
- **Keyboard**: Escape cancels, Enter activates primary (which is cancel — safer default)
- **Screenshots**: `screenshots/310-confirm-destructive.png`

### Drawer (side panel)
- **Used instead of modal when**: editing a record inline, showing detail alongside a list
- **Position**: right side, 480px wide
- **Overlay**: lighter (30% black)
- **Close behaviour**: same as modal

---

## Feedback

### Toast
- **Position**: top-right
- **Stack**: new toasts push old ones down, max 3 visible
- **Duration**: 3s default, 5s for errors, sticky for critical
- **Dismiss**: X button + auto-timeout
- **Variants**: success (green), info (blue), warning (amber), error (red)
- **Copy**: specific (*"Client Jenny O'Brien saved"*, not *"Saved"*)
- **Screenshots**: `screenshots/400-toast-success.png`, `screenshots/401-toast-error.png`

### Inline Confirmation
- **Pattern**: next to the triggering button, short label appears for 2s
- **Example**: *"✓ Copied"* next to a copy-link button

### Loading States
- **Skeleton**: used for list/table loads, matches final layout
- **Spinner**: used for action feedback (button click → spinner in button)
- **Full-page skeleton**: used on route change if data > 500ms
- **Screenshots**: `screenshots/410-skeleton-list.png`, `screenshots/411-skeleton-detail.png`

### Progress
- **Determinate**: progress bar with % for file uploads, bulk operations
- **Indeterminate**: looping bar at top of page for slow nav transitions
- **Step indicator**: numbered pills across top for multi-step flows

---

## Onboarding & Empty States

### First-Run Experience
- **Welcome screen**: Y/N — [description]
- **Tour**: Y/N — [steps, dismissable?]
- **Sample data**: [seeded / placeholder / none]
- **Screenshots**: `screenshots/500-first-run.png`

### Empty State Anatomy
| Element | Present? | Treatment |
|---------|----------|-----------|
| Illustration | Y | Abstract, brand-coloured, 120px square |
| Headline | Y | Bold, sentence case, ends without period |
| Description | Y | One sentence, explains *what this is* and *why it's empty* |
| CTA | Y | Primary button, verb-first, specific |
| Secondary link | Sometimes | "Learn more" link to docs |

### Copy Patterns for Empty States
- *"No [thing] yet. [One-line explanation]. [CTA]."*
- Examples:
  - *"No conversations yet. Start one below to see it here. [Start chat]"*
  - *"No clients yet. Add your first to begin tracking policies. [Add Client]"*

---

## Permissions & Roles

### Role Indicator
- **Visible?**: [always visible in nav / only in settings / not shown]
- **Placement**: near user avatar / in sidebar footer
- **Example**: *"Jane · Admin"*

### Denied Access
- **Page-level**: redirect to dashboard with toast *"You don't have access to that page"*
- **Action-level**: button hidden (not disabled with tooltip)
- **Data-level**: records silently filtered out of lists

### Role-Specific UX
- **Admins see**: [what's added]
- **Viewers see**: [what's removed]
- **Clients see**: [totally different nav? same nav with subset?]

---

## Copy & Microcopy

High-signal examples extracted verbatim. Full corpus in [copy-corpus.md](./copy-corpus.md).

### Button labels
- `Start chat` (not "New conversation" or "Create")
- `Upgrade plan` (not "Upgrade")
- `Delete forever` (used for hard-delete vs soft-delete "Archive")
- `Try again` (error recovery, not "Retry")

### Error messages
- *"We couldn't save that change. Try again, or contact support if it keeps happening."* — apologetic, actionable
- *"That email's already in use. Sign in instead?"* — redirect option
- *"This link expired. Ask the sender for a new one."* — blame-free

### Empty states
- *"You're all caught up. Check back later or create a new [thing]."*
- *"No results for '[query]'. Try a different search or browse all [things]."*

### Confirmation dialogs
- *"Delete project 'Launch Q2'? 14 tasks and 3 members will lose access. This cannot be undone."*

### Tone notes
- [first-person plural "we" used throughout / second-person "you" / neutral]
- [apostrophes used / not used]
- [emoji used / not used / only in celebratory moments]
- [exclamation marks rare / common / only in errors]

---

## Keyboard

### Shortcut Sheet
- **Access**: `?` or `Cmd+/` opens a modal listing all shortcuts
- **Organisation**: grouped by context (Global, Navigation, Editing)
- **Screenshot**: `screenshots/700-shortcut-sheet.png`

### Global Shortcuts
- `Cmd+K` — command palette
- `G then C` — go to Clients
- `G then P` — go to Projects
- `/` — focus search
- `Esc` — close modal / clear search

### Command Palette (`Cmd+K`)
- **Style**: centred modal, single input with live results
- **Categories**: Pages, Actions, Recent
- **Fuzzy match**: Y
- **Keyboard**: arrows navigate, Enter selects, Tab dismisses
- **Screenshots**: `screenshots/710-palette-open.png`, `screenshots/711-palette-search.png`

### Focus Indicators
- **Style**: 2px solid accent ring, offset 2px from element
- **Visibility**: high contrast in both light and dark mode
- **Tab order**: top-to-bottom, left-to-right, matches visual grouping

---

## Motion

### Page Transitions
- **Style**: fade-through, 150ms
- **Exception**: auth flows use slide left/right

### Modal Enter / Exit
- **Enter**: backdrop fade 150ms, modal fade + scale-up (98→100%) 200ms
- **Exit**: reverse
- **GIF**: `screenshots/800-modal-open.gif`

### List Item Enter / Exit
- **New item**: fade + slight slide-down, 200ms
- **Removed item**: fade + slide-up, 150ms

### Loading → Loaded
- **Skeleton replacement**: crossfade 100ms
- **No layout shift** on content arrival

### Success Moments
- *"Task complete" checkmark draws in 400ms*
- *Confetti on plan upgrade*
- *GIF: `screenshots/810-success.gif`*

---

## Responsive

### Breakpoints Observed
- **1440px**: baseline desktop
- **1280px**: standard desktop (same layout)
- **1024px**: sidebar collapses to icon-only, main content widens
- **768px**: sidebar becomes hamburger drawer, content stacks
- **375px**: mobile, bottom-tab nav replaces sidebar entirely

### Mobile-Specific Patterns
- **Bottom tab nav** with 5 icons on 375px
- **Floating action button** replaces in-page CTAs on list views
- **Full-screen modals** instead of centred modals
- **Bottom sheet** for action menus instead of dropdown
- **Screenshots**: `screenshots/900-mobile-nav.png`, `screenshots/901-mobile-fab.png`, `screenshots/902-bottom-sheet.png`

### Touch Targets
- Minimum 44×44px observed
- Primary CTAs 56px tall on mobile

---

## Notable Absences

Patterns that *aren't* present, worth documenting:

- **No undo** on destructive actions — only confirmation, no time-window restore
- **No bulk edit** — can select multiple but only delete in bulk, not update
- **No keyboard shortcut** for new-record creation on any list page
- **No offline mode** — blank screen if network fails
- **No activity feed** on dashboard — can't tell what changed since last visit

---

## Re-extraction

This library is a snapshot of [Date]. The app will change. Re-extract every 6–12 months for apps we reference often, sooner if a major redesign ships. Check `archive.org/wayback` for historical comparisons.
```

## Guidelines for writing the library

- **Every claim needs a screenshot**. If you can't point to a screenshot, you don't actually know.
- **Copy is verbatim**. Code blocks or blockquotes for exact text. Paraphrasing loses the voice.
- **Notable Absences is as important as presence**. What an app doesn't do is a design decision.
- **Cross-reference freely**. "See also [Modal Chrome](#modal-chrome)" prevents repetition.
- **Timestamp everything**. Apps change. A library without a date decays into misinformation.
- **Write opinions into an audit, not an extract**. Extracts describe what exists.
