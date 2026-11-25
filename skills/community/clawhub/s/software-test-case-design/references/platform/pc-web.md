# PC Web Test Points

> This file defines the test dimensions and strategy points that distinguish PC Web from other platforms.
> For the output format, see `references/examples/format-spec.md`; for the checklist, see `references/checklists/pc-web-checklist.md`.

## Contents

| Line | Section |
|------|------|
| 29 | 1. Browser Compatibility |
| 45 | 2. Page Layout and Resolution |
| 60 | 3. Keyboard Navigation |
| 77 | 4. Form Interaction |
| 93 | 5. Session and Authentication |
| 109 | 6. Multiple Windows and Tabs |
| 124 | 7. Routing and Navigation |
| 140 | 8. Data Linkage |
| 156 | 9. Drag and Drop |
| 172 | 10. Rich Text Editing |
| 189 | 11. File Operations |
| 206 | 12. Internationalization |
| 221 | 13. Dark Mode |
| 237 | 14. Printing |
| 253 | 15. Network and Cache |
| 271 | 16. Performance Experience |

---

## 1. Browser Compatibility

### Key focus points
- Mainstream browsers: Chrome / Firefox / Safari / Edge
- CSS feature differences: flexbox gap, aspect-ratio, container queries, etc.
- JavaScript API differences: polyfill coverage for new APIs
- Safari-specific issues: date formats, flex layout, input event differences
- Effect of private mode on cookies / Storage

### Common defects
- Safari date parsing fails (yyyy-MM-dd must be handled)
- Inconsistent scrollbar styles in Firefox
- localStorage writes throw errors in private mode

---

## 2. Page Layout and Resolution

### Key focus points
- Mainstream resolutions: 1366×768 / 1920×1080 / 2K / 4K
- DPI scaling: layout at 100% / 125% / 150%
- Content reflow when resizing the window (minimum width limits)
- Effect of scrollbar width on layout (especially auto-hiding scrollbars on Windows)

### Common defects
- Buttons or text clipped at 125% / 150% DPI
- Content overflow at small resolutions
- Layout jitter when the scrollbar appears / disappears

---

## 3. Keyboard Navigation

### Key focus points
- Tab focus order: top to bottom, left to right
- Enter triggers buttons, Space toggles checkboxes
- Esc closes pop-ups / cancels operations
- Global shortcuts (Ctrl+S to save, Ctrl+F to search, etc.)
- Focus indicator clearly visible
- Accessibility skip link (Skip to main content)

### Common defects
- Tab focus jumps to hidden elements
- Focus does not move into a pop-up when it opens
- Esc cannot close pop-ups

---

## 4. Form Interaction

### Key focus points
- Preventing duplicate form submission (rapid consecutive clicks)
- Required / format validation with real-time error messages
- Date pickers / drop-down selectors / file upload components
- Autofill (conflicts between browser autofill and custom components)
- Copy and paste (handling of formatted paste)

### Common defects
- Quick double-click on submit creates duplicate data
- Browser autofill overwrites custom component values
- Date picker format inconsistent with manual input

---

## 5. Session and Authentication

### Key focus points
- Session expiration handling: prompt dialog vs redirect to login page
- Login state synchronization across tabs (how tab B learns that tab A logged out)
- Remember me / auto login
- Handling of concurrent logins on multiple devices
- Single sign-on (SSO) flow

### Common defects
- No response or data loss when operating after the session expires
- Login state not synchronized across tabs
- Pages still accessible from the browser cache after logout

---

## 6. Multiple Windows and Tabs

### Key focus points
- Cross-tab communication (BroadcastChannel / localStorage events)
- State retention when switching tabs
- State restoration on browser back / forward / refresh
- Data passing between windows (window.opener / postMessage)

### Common defects
- Page state lost after going back
- Form data cleared after refresh
- Conflicts when multiple tabs operate on the same record

---

## 7. Routing and Navigation

### Key focus points
- SPA routing: URL synchronized with page state
- Parsing and type validation of dynamic route parameters
- Direct access to deep links (state not lost on refresh)
- Route guards: redirects when not logged in / without permission
- Correct breadcrumb hierarchy

### Common defects
- 404 after refresh (SPA without server-side route fallback)
- Wrong dynamic route parameter types not handled
- Wrong content shown after going back

---

## 8. Data Linkage

### Key focus points
- Parent–child component data sync and cross-component state sharing
- Data passing from list → detail and refresh on return
- Multi-condition filter linkage and pagination reset
- Data loading and caching strategy when switching tabs
- Page data refresh after operations in a modal

### Common defects
- The list is not refreshed after editing in the detail page and returning
- Pagination not reset after filter conditions change
- Data mix-up when switching tabs quickly

---

## 9. Drag and Drop

### Key focus points
- Drag to reorder and drag to upload
- Position preview and guide lines while dragging
- Feedback when dropping onto an invalid area
- Ctrl+Z to undo a drag
- Performance when dragging many elements

### Common defects
- Data order inconsistent with the visual order after dragging
- Data not rolled back after undoing a drag
- Stutter when dragging in large lists

---

## 10. Rich Text Editing

### Key focus points
- Basic formatting: bold / italic / underline / headings / lists
- Inserting links / images / tables
- Undo / redo (Ctrl+Z / Ctrl+Y)
- Formatting when pasting from Word / Excel
- Markdown editing and preview
- Word count and content limits

### Common defects
- Broken formatting when pasting Word content
- Undo / redo stack errors
- XSS risk when submitting rich text content

---

## 11. File Operations

### Key focus points
- File download: file name, format, garbled Chinese file names, large file download progress
- File preview: online preview of images / PDF / Office documents
- File import and export: template download, validation and error messages for imported data, exported content consistent with filter conditions
- File upload: type limits, size limits, multi-file upload, upload progress and cancellation
- File deletion: confirmation before deletion, list refresh after deletion

### Common defects
- Garbled Chinese file names on download
- Import failure without the specific error row
- Exported data inconsistent with the current filter conditions
- Oversized files not blocked on the front end or no prompt

---

## 12. Internationalization

### Key focus points
- Language switching: static text / dynamic content / date / number / currency formats
- RTL layout (Arabic, etc.)
- Language retained after refreshing the page
- Layout overflow in multiple languages (long-text languages such as German)

### Common defects
- Some text not translated after switching language
- Layout overflow in long-text languages
- Date format not matching regional conventions

---

## 13. Dark Mode

### Key focus points
- Manual switching vs following the system
- Contrast of all components in dark mode (≥ 4.5:1)
- Adaptation of images / icons / code blocks
- Retained after refresh
- Consistent across pages

### Common defects
- Some components not adapted to dark mode (white background)
- Code block highlighting unreadable in dark mode
- Mode reset after refresh

---

## 14. Printing

### Key focus points
- Print styles: hide navigation / buttons and other non-content elements
- Repeating table headers across pages
- Headers, footers, and page numbers
- Layout for different paper sizes (A4 / Letter)
- Print preview consistent with the actual output

### Common defects
- Unnecessary navigation and buttons included when printing
- Table headers lost across pages
- Blurry printed images

---

## 15. Network and Cache

### Key focus points
- Service Worker cache strategies (Cache First / Network First / Stale While Revalidate)
- Offline availability: whether cached pages are accessible after going offline
- Loading timeouts and retry on weak networks
- Effect of browser cache (HTTP Cache-Control / ETag) on resource updates
- IndexedDB / localStorage capacity limits and handling when exceeded
- Recovery behavior after clearing the cache

### Common defects
- Service Worker not updated, so users see the old version
- Blank page without an offline prompt after going offline
- Requests hang indefinitely without timeout feedback on weak networks
- Static resources cached without version numbers, so users still load old files after a CDN update

---

## 16. Performance Experience

### Key focus points
- First-screen load time, blank-screen time (follow project requirements; when none exist, use the reference values in the checklist)
- Rendering and scrolling smoothness of long lists / large tables
- Memory usage after staying on the page for a long time (whether it keeps growing)
- Resource loading: code splitting, resource compression, image lazy loading

### Common defects
- Long blank first screen
- Choppy scrolling in tables with large data volumes
- The page gets slower and slower after long use (memory leak)
