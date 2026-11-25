# Common Testing Checklist

This document combines the checklists for functional testing, linkage testing, routing testing, UI visual testing, interaction testing, and usability and accessibility. For the API testing checklist, see `references/checklists/api-checklist.md`.

## Contents

| Line | Section |
|------|------|
| 19 | 0. Test Case Executability Check |
| 27 | 1. Functional Testing Checklist |
| 75 | 2. Linkage Testing Checklist |
| 120 | 3. Routing Testing Checklist |
| 171 | 4. UI Visual Testing Checklist |
| 242 | 5. Interaction Testing Checklist |
| 293 | 6. Usability and Accessibility Checklist |

---

## 0. Test Case Executability Check (common to all test types)

- [ ] Do the test steps give concrete input values / parameters / objects to operate on (instead of descriptive language)?
- [ ] Are there unacceptable descriptions such as "enter an overly long string", "enter special characters", "enter a test attack vector", or "fill in the required form fields"?
- [ ] Do large data input scenarios (e.g., 10,000-character text, 500 MB file) use descriptive language plus explicit parameters?

---

## 1. Functional Testing Checklist

### Test coverage
- [ ] All feature points are covered
- [ ] Normal flows are covered
- [ ] Negative flows are covered
- [ ] Boundary conditions are covered
- [ ] Special scenarios are covered
- [ ] Valid and invalid state transitions are covered (state transition testing)
- [ ] Multi-condition combination rules are covered one by one (decision table testing)

### Functional correctness
- [ ] Features are implemented as required
- [ ] Business logic is correct
- [ ] Data processing is correct
- [ ] State transitions are correct
- [ ] Access control is correct

### Input validation
- [ ] Valid input is handled correctly
- [ ] Invalid input gives friendly prompts
- [ ] Boundary values are handled correctly
- [ ] Special characters are handled correctly
- [ ] Empty values are handled correctly

### Output validation
- [ ] Displayed content is correct
- [ ] Data format is correct
- [ ] Sorting is correct
- [ ] Filtering is correct
- [ ] Statistics are correct

### Interaction
- [ ] User operation flow is smooth
- [ ] Page navigation is correct
- [ ] Buttons work correctly
- [ ] Form submission is correct
- [ ] List operations are correct

### Data consistency
- [ ] Front-end and back-end data are consistent
- [ ] Data is consistent across devices
- [ ] Cache and database are consistent
- [ ] History records are correct
- [ ] Real-time data is correct

---

## 2. Linkage Testing Checklist

### Form linkage
- [ ] Province–city–district cascading
- [ ] Category selection linkage
- [ ] Conditional show / hide
- [ ] Cascading data
- [ ] Form validation linkage
- [ ] Submit button state linkage

### List linkage
- [ ] Master–detail list linkage
- [ ] Filter condition linkage
- [ ] Sort linkage
- [ ] Pagination linkage
- [ ] Selection state linkage

### Search linkage
- [ ] Search keyword suggestions
- [ ] Search result linkage
- [ ] Search history linkage
- [ ] Trending search linkage

### State linkage
- [ ] Button state linkage
- [ ] Menu state linkage
- [ ] Tag state linkage
- [ ] Icon state linkage
- [ ] Color state linkage

### Data linkage
- [ ] Real-time data sync
- [ ] Multi-device data sync
- [ ] Cache and database sync
- [ ] Local and remote sync
- [ ] Two-way data binding

### Page linkage
- [ ] Page parameter passing
- [ ] Page state sync
- [ ] Multi-window linkage
- [ ] iframe linkage

---

## 3. Routing Testing Checklist

### Direct access
- [ ] Direct access to the home page URL
- [ ] Direct access to a detail page URL
- [ ] Direct access to a list page URL
- [ ] Direct access to the user center URL

### Navigation
- [ ] Navigation bar clicks
- [ ] Breadcrumb navigation
- [ ] Bottom navigation
- [ ] Sidebar navigation
- [ ] Tab switching
- [ ] Button navigation

### Browser navigation
- [ ] Browser back
- [ ] Browser forward
- [ ] Browser refresh
- [ ] History

### Deep links
- [ ] Opening a specific page from an external link (app / mini program / H5)
- [ ] Opening a specific page from a push notification
- [ ] Opening a specific page from a share link

### Error pages
- [ ] 404 page display
- [ ] 403 page display
- [ ] 500 page display

### Route parameters
- [ ] URL parameter passing
- [ ] URL parameter parsing
- [ ] Missing parameter handling
- [ ] Wrong parameter handling

### Route guards
- [ ] Login check
- [ ] Permission check
- [ ] Redirect to the login page when not logged in
- [ ] Redirect to 403 without permission

### Routing performance
- [ ] Smooth route switching
- [ ] Fast page loading
- [ ] Smooth route animations

---

## 4. UI Visual Testing Checklist

### Layout
- [ ] Correct alignment
- [ ] Consistent spacing
- [ ] Clear hierarchy
- [ ] Responsive layout adaptation
- [ ] Elements do not overlap
- [ ] Content does not overflow
- [ ] Appropriate whitespace
- [ ] Visual balance

### Color
- [ ] Correct brand colors
- [ ] Correct secondary colors
- [ ] Correct status colors (success / failure / warning)
- [ ] Contrast meets WCAG standards
- [ ] Dark mode adaptation
- [ ] Light mode adaptation
- [ ] Correct color semantics
- [ ] Color-blind friendly

### Typography
- [ ] Correct font family
- [ ] Clear font size hierarchy
- [ ] Appropriate line height
- [ ] Correct font weight
- [ ] Sufficient font color contrast
- [ ] Text not truncated
- [ ] Multilingual font adaptation
- [ ] Special characters display correctly

### Icons
- [ ] Consistent icon style
- [ ] Uniform icon size
- [ ] Clear icon semantics
- [ ] Correct icon states (default / hover / pressed / disabled)
- [ ] Sufficient icon clarity
- [ ] Icons load normally

### Images
- [ ] Clear image quality
- [ ] Correct image ratio
- [ ] Placeholder shown while loading
- [ ] Error image shown on failure
- [ ] Image lazy loading works
- [ ] Appropriate image compression

### Animation
- [ ] Natural easing curves
- [ ] Appropriate duration
- [ ] Smooth animation performance (≥ 60fps)
- [ ] Clear animation semantics
- [ ] Animations are interruptible
- [ ] No animation flicker

### Interaction states
- [ ] Correct default state
- [ ] Correct hover state
- [ ] Correct pressed state
- [ ] Correct disabled state
- [ ] Correct focus state

### Multiple themes
- [ ] Light theme works
- [ ] Dark theme works
- [ ] Smooth theme switching
- [ ] Theme setting remembered

---

## 5. Interaction Testing Checklist

### Page loading
- [ ] First load and refresh work normally
- [ ] Loading or error prompts on weak networks and offline
- [ ] Prompt on loading timeout
- [ ] Retry available after a load failure
- [ ] Skeleton screen / loading placeholder displays correctly

### Page navigation and switching
- [ ] Navigation bar displays correctly
- [ ] Back button returns to the correct page
- [ ] Tab / modal / drawer / pop-up switching works
- [ ] State retained or refreshed as needed after switching

### Form interaction
- [ ] Correct focus / blur states of input boxes
- [ ] Validation triggered correctly on blur or submit
- [ ] Correct position and wording of error messages
- [ ] Autofill and input restrictions take effect

### List interaction
- [ ] Pull to refresh and load more work
- [ ] Tap, swipe, and long press actions on list items are correct
- [ ] List sorting and filtering are correct

### Pop-up interaction
- [ ] Overlay covers correctly
- [ ] Closing via the close button, clicking the overlay, and the ESC key behaves as designed
- [ ] Multiple pop-up layers are stacked correctly and close in the right order
- [ ] Background cannot scroll while a pop-up is open

### Component interaction
- [ ] Buttons: normal / hover / pressed / disabled / loading states are correct
- [ ] Buttons: rapid consecutive clicks do not cause duplicate submissions
- [ ] Input boxes: special characters, overly long text, copy and paste, and clearing are correct
- [ ] Drop-downs: expand / collapse, option search, multi-select, cascading, and keyboard operation are correct
- [ ] Tables: sorting, filtering, pagination, row actions, batch operations, and export are correct
- [ ] Carousels: automatic / manual switching, indicators, infinite loop, and pause on hover are correct
- [ ] Tabs: tap / swipe switching, closing, and drag-to-reorder are correct

### Interaction motion
- [ ] Page transitions and component appear / disappear animations are natural
- [ ] Click feedback, loading, and success / failure feedback animations are correct
- [ ] Progress bar animation matches the actual progress
- [ ] Gesture animations such as scroll inertia, zoom, drag, and pull-down bounce are smooth
- [ ] Animations can be interrupted by quick operations without freezing
- [ ] Animation frame rate ≥ 60fps, without stutter or flicker

---

## 6. Usability and Accessibility Checklist

### Navigation and information architecture
- [ ] Users can clearly tell where they are (title, highlight, breadcrumbs)
- [ ] Every page has a path back to the upper level or the home page
- [ ] Entries to core features are prominent and easy to find

### Prompts and feedback
- [ ] Clear feedback for both successful and failed operations
- [ ] Error messages explain the cause and how to fix it, without showing raw error codes or stacks
- [ ] High-risk operations such as delete, overwrite, and payment require a second confirmation
- [ ] Time-consuming operations show progress or a waiting prompt

### Form usability
- [ ] Required fields are clearly marked
- [ ] Input format hints are provided (e.g., placeholders, examples)
- [ ] Entered data is not lost after a submission error
- [ ] Default values are reasonable

### Help and guidance
- [ ] Empty-state pages have an explanation and next-step guidance
- [ ] Onboarding can be skipped and viewed again
- [ ] Complex features have a help entry or explanatory text

### Accessibility
- [ ] All features can be completed with the keyboard only, with a sensible focus order
- [ ] Keyboard focus is clearly visible
- [ ] Images and icons have alternative text (alt / accessibility labels)
- [ ] Form controls have associated labels
- [ ] Important information is not conveyed by color alone
- [ ] Text-to-background contrast ≥ 4.5:1
- [ ] Screen readers correctly read the page structure and control states
- [ ] Content is not lost and features remain usable when the page is zoomed to 200%
