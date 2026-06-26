# PC Web Testing Checklist

## Browser Compatibility (12 items)
- [ ] Chrome latest version works correctly
- [ ] Chrome mainstream version compatible
- [ ] Firefox latest version works correctly
- [ ] Firefox mainstream version compatible
- [ ] Safari browser compatible
- [ ] Edge browser compatible
- [ ] Multi-engine browser compatible
- [ ] JavaScript feature compatibility
- [ ] CSS feature compatibility
- [ ] Private mode access works correctly
- [ ] No errors in developer tools
- [ ] Browser extension compatibility

## Page Layout (10 items)
- [ ] 1366×768 resolution works correctly
- [ ] 1920×1080 resolution works correctly
- [ ] 2K/4K resolution works correctly
- [ ] 100% DPI scaling works correctly
- [ ] 125% DPI scaling works correctly
- [ ] 150% DPI scaling works correctly
- [ ] Maximized window layout is correct
- [ ] Custom window size layout is correct
- [ ] Scrollbar displays correctly
- [ ] Responsive breakpoints are correct

## Keyboard Navigation (10 items)
- [ ] Tab key focus order is correct
- [ ] Enter key triggers buttons
- [ ] Space key operates checkboxes
- [ ] Arrow keys enable navigation
- [ ] Global shortcuts work correctly
- [ ] Esc key closes modals
- [ ] F5 refreshes the page
- [ ] Ctrl+C/V copy and paste
- [ ] Focus indicator is clearly visible
- [ ] Skip navigation links are usable

## Form Interaction (12 items)
- [ ] Text input works correctly
- [ ] Number input validation
- [ ] Date picker is usable
- [ ] Dropdown selection works correctly
- [ ] File upload functionality
- [ ] Form required-field validation
- [ ] Form submission succeeds
- [ ] Duplicate submission prevention
- [ ] Form reset functionality
- [ ] Input suggestions/autocomplete
- [ ] Copy-paste functionality
- [ ] Form disabled state

## Authentication & Sessions (10 items)
- [ ] Normal login succeeds
- [ ] Incorrect password prompt is friendly
- [ ] Session expiry is handled
- [ ] Remember-me functionality
- [ ] Normal logout
- [ ] Password recovery flow
- [ ] Password change functionality
- [ ] Two-factor authentication (if applicable)
- [ ] Multi-device login conflict handling
- [ ] Auto-logout on timeout

## Multi-Window & Tabs (8 items)
- [ ] New window opens correctly
- [ ] New tab opens correctly
- [ ] Cross-window communication works correctly
- [ ] Close window confirmation
- [ ] Tab switching preserves state
- [ ] Browser forward/back works correctly
- [ ] Page refresh preserves data
- [ ] Window state memory

## Routing & Navigation (12 items)
- [ ] SPA route path matching is correct
- [ ] Nested route hierarchy is correct
- [ ] Dynamic route parameter parsing is correct
- [ ] URL and page state are synchronized
- [ ] Route guard redirects when not logged in
- [ ] Route redirects when insufficient permissions
- [ ] 404 page displays correctly
- [ ] Deep link direct access works correctly
- [ ] Browser forward/back state is correct
- [ ] URL and page state are consistent after refresh
- [ ] Breadcrumb navigation hierarchy is correct
- [ ] Anchor positioning works correctly

## Data Linkage (10 items)
- [ ] Parent-child component data synchronization
- [ ] Cross-component state sharing is correct
- [ ] List item click navigates to detail
- [ ] List refreshes after detail modification
- [ ] Multi-condition filter linkage is correct
- [ ] Pagination switching data is correct
- [ ] Sort switching display is correct
- [ ] Page refreshes after modal submission
- [ ] Linked field dependencies are correct
- [ ] Tab switching loads data

## Drag-and-Drop Interaction (10 items)
- [ ] Element drag-and-drop works correctly
- [ ] Drag sort positions are correct
- [ ] Drag file upload succeeds
- [ ] Drag disabled state works correctly
- [ ] Drag keyboard operations are available
- [ ] Drag does not exceed boundaries
- [ ] Ctrl+Z undo drag
- [ ] Drag alignment guides appear
- [ ] Large number of elements drag smoothly
- [ ] Data is saved correctly after drag

## Rich Text Editing (10 items)
- [ ] Basic text input works correctly
- [ ] Bold/italic/underline take effect
- [ ] Heading level switching is correct
- [ ] Unordered/ordered lists work correctly
- [ ] Insert link/image/table works correctly
- [ ] Ctrl+Z undo works correctly
- [ ] Ctrl+Y redo works correctly
- [ ] Pasting from external sources preserves formatting
- [ ] Markdown editing preview works correctly
- [ ] Word count is accurate

## File Operations (8 items)
- [ ] File download works correctly
- [ ] File preview works correctly
- [ ] File save works correctly
- [ ] File import works correctly
- [ ] File export works correctly
- [ ] File deletion confirmation
- [ ] Drag file upload
- [ ] File type restriction

## Network & Cache (10 items)
- [ ] Normal network access
- [ ] Offline prompt is friendly
- [ ] Network recovery handling
- [ ] Weak network loading prompt
- [ ] Strong cache takes effect
- [ ] Conditional cache takes effect
- [ ] Cookies work correctly
- [ ] LocalStorage works correctly
- [ ] SessionStorage works correctly
- [ ] Request retry mechanism

## Internationalization & Localization (10 items)
- [ ] Language switching works correctly
- [ ] Static text translation is correct
- [ ] Dynamic content translation is correct
- [ ] Number format follows locale conventions
- [ ] Date/time format follows locale conventions
- [ ] Currency format is correct
- [ ] RTL layout works correctly (if applicable)
- [ ] Language selection is persisted
- [ ] Language is retained after refresh
- [ ] Language is consistent across pages

## Print Functionality (8 items)
- [ ] Print button triggers printing
- [ ] Print preview content is correct
- [ ] Print styles are correct (non-essential elements hidden)
- [ ] Headers and footers display correctly
- [ ] Table headers repeat across pages
- [ ] Images print clearly
- [ ] A4/Letter paper layout is correct
- [ ] Chrome/Firefox/Edge printing is consistent

## Dark Mode (8 items)
- [ ] Manual dark mode toggle
- [ ] Follow system dark mode
- [ ] Color contrast is sufficient after switching
- [ ] Images/icons adapt to dark mode
- [ ] Form control styles are correct
- [ ] Code block highlighting is readable
- [ ] Mode is persisted (retained after refresh)
- [ ] Mode is consistent across pages

## Performance Optimization (8 items)
- [ ] First-screen load < 3 seconds
- [ ] White screen time < 1 second
- [ ] Image lazy loading works correctly
- [ ] Animation is smooth at 60fps
- [ ] No memory leaks
- [ ] Long lists load correctly
- [ ] Code splitting takes effect
- [ ] Resource compression takes effect
