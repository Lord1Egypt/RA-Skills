# PC Web Platform-Specific Testing

> This document defines specialized testing dimensions and strategy highlights specific to PC Web, distinct from other platforms.
> See `references/examples/format-spec.md` for output format and `references/checklists/pc-web-checklist.md` for the checklist.

## Table of Contents

| Line | Section |
|------|---------|
| 26 | I. Browser Compatibility |
| 42 | II. Page Layout & Resolution |
| 57 | III. Keyboard Navigation |
| 74 | IV. Form Interaction |
| 90 | V. Sessions & Authentication |
| 106 | VI. Multi-Window & Tabs |
| 121 | VII. Routing & Navigation |
| 137 | VIII. Data Linkage |
| 153 | IX. Drag-and-Drop Interaction |
| 169 | X. Rich Text Editing |
| 186 | XI. Internationalization |
| 201 | XII. Dark Mode |
| 217 | XIII. Print Functionality |
| 233 | XIV. Network & Cache |

---

## I. Browser Compatibility

### Focus Areas
- Mainstream browsers: Chrome / Firefox / Safari / Edge
- CSS feature differences: flexbox gap, aspect-ratio, container queries, etc.
- JavaScript API differences: polyfill coverage for new APIs
- Safari-specific issues: date format, flex layout, input event differences
- Impact of private mode on Cookies/Storage

### Common Defects
- Safari date parsing failure (requires yyyy-MM-dd compatibility)
- Firefox scrollbar style inconsistency
- localStorage write errors in private mode

---

## II. Page Layout & Resolution

### Focus Areas
- Mainstream resolutions: 1366×768 / 1920×1080 / 2K / 4K
- Layout behavior under DPI scaling: 100% / 125% / 150%
- Content reflow during window resize (minimum width constraint)
- Impact of scrollbar width on layout (especially Windows auto-hide scrollbar)

### Common Defects
- Buttons or text clipped under 125%/150% DPI
- Content overflow at small resolutions
- Layout jitter when scrollbar appears/disappears

---

## III. Keyboard Navigation

### Focus Areas
- Tab focus order: top to bottom, left to right
- Enter triggers buttons, Space operates checkboxes
- Esc closes modals/cancels operations
- Global shortcuts (Ctrl+S save, Ctrl+F search, etc.)
- Focus indicator clearly visible
- Skip navigation links (Skip to main content)

### Common Defects
- Tab focus jumps to hidden elements
- Focus not moved into modal when opened
- Esc cannot close modal

---

## IV. Form Interaction

### Focus Areas
- Duplicate submission prevention (rapid consecutive clicks)
- Required field/format validation with real-time error prompts
- Date picker/dropdown selector/file upload components
- Autofill (conflict between browser autofill and custom components)
- Copy-paste (handling of formatted paste)

### Common Defects
- Duplicate data from rapid double-click submission
- Browser autofill overwriting custom component values
- Date picker and manual input format inconsistency

---

## V. Sessions & Authentication

### Focus Areas
- Session expiry handling: dialog prompt vs redirect to login page
- Multi-tab login state synchronization (logout in Tab A; how does Tab B detect it?)
- Remember-me / auto-login
- Multi-device login conflict handling
- Single Sign-On (SSO) flow

### Common Defects
- No response or data loss after session expiry
- Login state not synchronized across multiple tabs
- Browser cache still accessible after logout

---

## VI. Multi-Window & Tabs

### Focus Areas
- Cross-tab communication (BroadcastChannel / localStorage events)
- State preservation during tab switching
- State restoration on browser forward/back/refresh
- Inter-window data passing (window.opener / postMessage)

### Common Defects
- Page state lost after going back
- Form data cleared after refresh
- Data conflicts from multiple tabs operating on the same record

---

## VII. Routing & Navigation

### Focus Areas
- SPA routing: URL and page state synchronization
- Dynamic route parameter parsing and type validation
- Deep link direct access (state not lost on refresh)
- Route guards: redirect when not logged in / unauthorized
- Breadcrumb navigation hierarchy correctness

### Common Defects
- 404 after refresh (SPA not configured with server-side route fallback)
- Dynamic route parameter type errors not handled
- Incorrect page content displayed after going back

---

## VIII. Data Linkage

### Focus Areas
- Parent-child component data synchronization and cross-component state sharing
- List → detail data passing and return refresh
- Multi-condition filter linkage and pagination reset
- Data loading and caching strategy during Tab switching
- Page data refresh after modal operation

### Common Defects
- List not refreshed after returning from detail modification
- Pagination not reset after filter condition change
- Data corruption from rapid Tab switching

---

## IX. Drag-and-Drop Interaction

### Focus Areas
- Drag sorting and drag uploading
- Position preview and alignment guides during drag
- Feedback when dragging to invalid area
- Ctrl+Z undo drag operation
- Performance with large number of elements

### Common Defects
- Data order inconsistent with visual after drag
- Data not rolled back after undo drag
- Stutter when dragging in large lists

---

## X. Rich Text Editing

### Focus Areas
- Basic formatting: bold/italic/underline/headings/lists
- Insert link/image/table
- Undo/redo (Ctrl+Z / Ctrl+Y)
- Format handling when pasting from Word/Excel
- Markdown editing and preview
- Word count and content limits

### Common Defects
- Format corruption when pasting Word content
- Undo/redo stack anomalies
- XSS risk in rich text content submission

---

## XI. Internationalization

### Focus Areas
- Language switching: static text/dynamic content/date/number/currency formats
- RTL layout (Arabic, etc.)
- Language retention after page refresh
- Layout overflow for verbose languages (German, etc.)

### Common Defects
- Partial untranslated text after language switch
- Layout overflow in verbose languages
- Date format not following locale conventions

---

## XII. Dark Mode

### Focus Areas
- Manual toggle vs follow system
- Contrast ratio for all components in dark mode (≥4.5:1)
- Image/icon/code block adaptation
- Mode retention after refresh
- Mode consistency across pages

### Common Defects
- Some components not adapted in dark mode (white background)
- Code block highlighting unreadable in dark mode
- Mode reset after refresh

---

## XIII. Print Functionality

### Focus Areas
- Print styles: hide non-content elements (nav, buttons)
- Table header repetition across pages
- Headers, footers, and page numbers
- Layout for different paper sizes (A4/Letter)
- Print preview consistency with actual output

### Common Defects
- Unnecessary navigation and buttons included in print
- Table headers lost across pages
- Blurry image printing

---

## XIV. Network & Cache

### Focus Areas
- Service Worker caching strategies (Cache First / Network First / Stale While Revalidate)
- Offline availability: whether cached pages are accessible after disconnection
- Loading timeout and retry mechanism under weak network
- Impact of browser cache (HTTP Cache-Control / ETag) on resource updates
- IndexedDB / localStorage capacity limits and overflow handling
- Recovery behavior after cache clearing

### Common Defects
- Service Worker not updated, causing users to see old version
- White screen with no offline prompt after disconnection
- Requests hanging indefinitely without timeout feedback under weak network
- Static resource cache without version hashes; users still load old files after CDN update
