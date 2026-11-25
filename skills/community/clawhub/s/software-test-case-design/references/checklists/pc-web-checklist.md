# PC Web Testing Checklist

> The sections of this checklist correspond one-to-one with `references/platform/pc-web.md` and are used for item-by-item self-checking after test case design.

## Browser Compatibility
- [ ] Latest Chrome works
- [ ] Mainstream Chrome versions are compatible
- [ ] Latest Firefox works
- [ ] Mainstream Firefox versions are compatible
- [ ] Safari compatibility
- [ ] Edge compatibility
- [ ] Multi-engine browser compatibility
- [ ] JavaScript feature compatibility
- [ ] CSS feature compatibility
- [ ] Private mode access works
- [ ] No errors in developer tools
- [ ] Browser extension compatibility

## Page Layout and Resolution
- [ ] 1366×768 resolution works
- [ ] 1920×1080 resolution works
- [ ] 2K/4K resolution works
- [ ] 100% DPI scaling works
- [ ] 125% DPI scaling works
- [ ] 150% DPI scaling works
- [ ] Correct layout when the window is maximized
- [ ] Correct layout at custom window sizes
- [ ] Scrollbars display correctly
- [ ] Correct responsive breakpoints

## Keyboard Navigation
- [ ] Correct Tab focus order
- [ ] Enter triggers buttons
- [ ] Space toggles checkboxes
- [ ] Arrow keys navigate
- [ ] Global shortcuts work
- [ ] Esc closes pop-ups
- [ ] F5 refreshes the page
- [ ] Ctrl+C/V copy and paste
- [ ] Focus indicator clearly visible
- [ ] Accessibility skip link available

## Form Interaction
- [ ] Text input works
- [ ] Numeric input validation
- [ ] Date picker usable
- [ ] Drop-down selection works
- [ ] File upload
- [ ] Required field validation
- [ ] Form submission succeeds
- [ ] Duplicate submission prevented
- [ ] Form reset
- [ ] Input suggestions / autocomplete
- [ ] Copy and paste
- [ ] Disabled form state

## Session and Authentication
- [ ] Normal login succeeds
- [ ] Friendly prompt for wrong password
- [ ] Session expiration handling
- [ ] Remember me
- [ ] Normal logout
- [ ] Password recovery flow
- [ ] Password change
- [ ] Two-factor authentication (if any)
- [ ] Handling of concurrent logins on multiple devices
- [ ] Automatic logout on timeout

## Multiple Windows and Tabs
- [ ] Opening in a new window works
- [ ] Opening in a new tab works
- [ ] Cross-window communication works
- [ ] Confirmation when closing the window
- [ ] State retained when switching tabs
- [ ] Browser forward and back work
- [ ] Data retained on page refresh
- [ ] Window state remembered

## Routing and Navigation
- [ ] SPA route paths match correctly
- [ ] Correct nested route hierarchy
- [ ] Dynamic route parameters parsed correctly
- [ ] URL synchronized with page state
- [ ] Route guard redirects when not logged in
- [ ] Route redirect when permissions are insufficient
- [ ] 404 page displays correctly
- [ ] Direct access to deep links works
- [ ] Correct state on browser forward / back
- [ ] URL and page state consistent after refresh
- [ ] Correct breadcrumb hierarchy
- [ ] Anchor positioning works

## Data Linkage
- [ ] Parent–child component data sync
- [ ] Correct cross-component state sharing
- [ ] Clicking a list item navigates to its detail
- [ ] List refreshed after editing in the detail page
- [ ] Correct multi-condition filter linkage
- [ ] Correct data when switching pages
- [ ] Correct display when changing sort
- [ ] Page refreshed after submitting in a modal
- [ ] Correct dependencies between linked fields
- [ ] Data loading on tab switch

## Drag and Drop
- [ ] Element dragging works
- [ ] Correct position after drag-to-reorder
- [ ] Drag-to-upload succeeds
- [ ] Disabled drag state works
- [ ] Dragging operable via keyboard
- [ ] Dragging does not exceed boundaries
- [ ] Ctrl+Z undoes a drag
- [ ] Drag guide lines align
- [ ] Smooth dragging with many elements
- [ ] Data saved correctly after dragging

## Rich Text Editing
- [ ] Basic text input works
- [ ] Bold / italic / underline take effect
- [ ] Heading levels switch correctly
- [ ] Unordered / ordered lists work
- [ ] Inserting links / images / tables works
- [ ] Ctrl+Z undo works
- [ ] Ctrl+Y redo works
- [ ] Formatting retained when pasting from external sources
- [ ] Markdown editing and preview work
- [ ] Accurate word count

## File Operations
- [ ] File download works
- [ ] File preview works
- [ ] File save works
- [ ] File import works
- [ ] File export works
- [ ] File deletion confirmation
- [ ] Drag-to-upload files
- [ ] File type restrictions

## Internationalization
- [ ] Language switching works
- [ ] Static text translated correctly
- [ ] Dynamic content translated correctly
- [ ] Number format matches regional conventions
- [ ] Date and time format matches regional conventions
- [ ] Correct currency format
- [ ] RTL layout works (if applicable)
- [ ] Language selection persists
- [ ] Language retained after refresh
- [ ] Consistent language across pages

## Dark Mode
- [ ] Manually switching to dark mode
- [ ] Following the system dark mode
- [ ] Sufficient color contrast after switching
- [ ] Images / icons adapted to dark mode
- [ ] Correct form control styles
- [ ] Readable code block highlighting
- [ ] Mode persists (retained after refresh)
- [ ] Consistent mode across pages

## Printing
- [ ] Clicking the print button triggers printing
- [ ] Correct print preview content
- [ ] Correct print styles (non-essential elements hidden)
- [ ] Headers and footers display correctly
- [ ] Table headers repeat across pages
- [ ] Images print clearly
- [ ] Correct layout for A4 / Letter paper
- [ ] Consistent printing in Chrome / Firefox / Edge

## Network and Cache
- [ ] Normal network access
- [ ] Friendly prompt when offline
- [ ] Handling of network recovery
- [ ] Loading prompt on weak networks
- [ ] Strong caching takes effect
- [ ] Negotiated caching takes effect
- [ ] Cookies work
- [ ] LocalStorage works
- [ ] SessionStorage works
- [ ] Request retry mechanism

## Performance Experience
> Follow project requirements for metrics; when none exist, use these as reference values.

- [ ] First-screen load < 3 seconds
- [ ] Blank-screen time < 1 second
- [ ] Image lazy loading works
- [ ] Smooth animation at 60fps
- [ ] No memory leaks
- [ ] Long lists load correctly
- [ ] Code splitting takes effect
- [ ] Resource compression takes effect
