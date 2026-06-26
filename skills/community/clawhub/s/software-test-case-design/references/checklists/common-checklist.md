# General Testing Checklist

This document consolidates checklists for functional testing, linkage testing, routing testing, and UI visual testing. See `checklists/api-checklist.md` for API testing checklist.

## Table of Contents

| Line | Section |
|------|---------|
| 17 | 0. Test Case Executability Check |
| 25 | I. Functional Testing Checklist |
| 71 | II. Linkage Testing Checklist |
| 116 | III. Routing Testing Checklist |
| 167 | IV. UI Visual Testing Checklist |

---

## 0. Test Case Executability Check (common to all test types)

- [ ] Do test steps provide concrete input values/parameters/operation targets (rather than descriptive language)?
- [ ] Are there any unqualified descriptions such as "enter an excessively long string," "enter special characters," "enter test attack vector," or "fill in form required fields"?
- [ ] For large data input scenarios (e.g., 10,000-character text, 500MB file), is descriptive language with explicit parameter specifications used?

---

## I. Functional Testing Checklist

### Test Coverage
- [ ] All function points are covered
- [ ] Normal flows are covered
- [ ] Exception flows are covered
- [ ] Boundary conditions are covered
- [ ] Special scenarios are covered

### Functional Correctness
- [ ] Functions are implemented per requirements
- [ ] Business logic is correct
- [ ] Data processing is correct
- [ ] State transitions are correct
- [ ] Permission control is correct

### Input Validation
- [ ] Valid input is handled correctly
- [ ] Invalid input provides friendly prompts
- [ ] Boundary values are handled correctly
- [ ] Special characters are handled correctly
- [ ] Null values are handled correctly

### Output Validation
- [ ] Displayed content is correct
- [ ] Data format is correct
- [ ] Sorting is correct
- [ ] Filtering is correct
- [ ] Statistics are correct

### Interaction Testing
- [ ] User operation flow is smooth
- [ ] Page navigation is correct
- [ ] Button functionality is correct
- [ ] Form submission is correct
- [ ] List operations are correct

### Data Consistency
- [ ] Frontend-backend data is consistent
- [ ] Multi-platform data is consistent
- [ ] Cache and database are consistent
- [ ] History records are correct
- [ ] Real-time data is correct

---

## II. Linkage Testing Checklist

### Form Linkage
- [ ] Province/city/district cascading
- [ ] Category selection linkage
- [ ] Conditional show/hide
- [ ] Data cascading
- [ ] Form validation linkage
- [ ] Submit button state linkage

### List Linkage
- [ ] Master-detail list linkage
- [ ] Filter condition linkage
- [ ] Sort linkage
- [ ] Pagination linkage
- [ ] Selection state linkage

### Search Linkage
- [ ] Search keyword suggestions
- [ ] Search result linkage
- [ ] Search history linkage
- [ ] Trending search linkage

### State Linkage
- [ ] Button state linkage
- [ ] Menu state linkage
- [ ] Tab state linkage
- [ ] Icon state linkage
- [ ] Color state linkage

### Data Linkage
- [ ] Real-time data synchronization
- [ ] Multi-platform data synchronization
- [ ] Cache and database synchronization
- [ ] Local and remote synchronization
- [ ] Bidirectional data binding

### Page Linkage
- [ ] Page parameter passing
- [ ] Page state synchronization
- [ ] Multi-window linkage
- [ ] iframe linkage

---

## III. Routing Testing Checklist

### Direct Access
- [ ] Direct access to home page URL
- [ ] Direct access to detail page URL
- [ ] Direct access to list page URL
- [ ] Direct access to profile page URL

### Navigation Jumping
- [ ] Navigation bar click jump
- [ ] Breadcrumb navigation jump
- [ ] Bottom navigation jump
- [ ] Sidebar navigation jump
- [ ] Tab switching
- [ ] Button click jump

### Browser Navigation
- [ ] Browser back
- [ ] Browser forward
- [ ] Browser refresh
- [ ] History records

### Deep Links
- [ ] External link opens specified app page
- [ ] Push notification opens specified page
- [ ] Share link opens specified page

### Error Pages
- [ ] 404 page display
- [ ] 403 page display
- [ ] 500 page display

### Route Parameters
- [ ] URL parameter passing
- [ ] URL parameter parsing
- [ ] Missing parameter handling
- [ ] Invalid parameter handling

### Route Guards
- [ ] Login verification
- [ ] Permission verification
- [ ] Redirect to login page when not authenticated
- [ ] Redirect to 403 when unauthorized

### Route Performance
- [ ] Route switching is smooth
- [ ] Page loading is fast
- [ ] Route animations are smooth

---

## IV. UI Visual Testing Checklist

### Layout Testing
- [ ] Alignment is correct
- [ ] Spacing is consistent
- [ ] Hierarchy is clear
- [ ] Responsive layout adapts correctly
- [ ] Elements do not overlap
- [ ] Content does not overflow
- [ ] Whitespace is reasonable
- [ ] Visual balance is maintained

### Color Testing
- [ ] Brand colors are correct
- [ ] Secondary colors are correct
- [ ] Status colors are correct (success/failure/warning)
- [ ] Contrast meets WCAG standards
- [ ] Dark mode adaptation
- [ ] Light mode adaptation
- [ ] Color semantics are correct
- [ ] Color-blind friendly

### Font Testing
- [ ] Font family is correct
- [ ] Font size hierarchy is clear
- [ ] Line height is appropriate
- [ ] Font weight is correct
- [ ] Font color contrast is sufficient
- [ ] Text is not truncated
- [ ] Multi-language font adaptation
- [ ] Special characters display correctly

### Icon Testing
- [ ] Icon style is consistent
- [ ] Icon sizes are uniform
- [ ] Icon semantics are clear
- [ ] Icon states are correct (default/hover/click/disabled)
- [ ] Icon clarity is sufficient
- [ ] Icon loading is normal

### Image Testing
- [ ] Image quality is clear
- [ ] Image aspect ratio is correct
- [ ] Loading state shows placeholder
- [ ] Error state shows error image
- [ ] Image lazy loading works correctly
- [ ] Image compression is appropriate

### Animation Testing
- [ ] Animation curves are natural
- [ ] Animation duration is appropriate
- [ ] Animation performance is smooth (≥60fps)
- [ ] Animation semantics are clear
- [ ] Animations are interruptible
- [ ] No animation flickering

### Interaction State Testing
- [ ] Default state is correct
- [ ] Hover state is correct
- [ ] Click state is correct
- [ ] Disabled state is correct
- [ ] Focus state is correct

### Multi-Theme Testing
- [ ] Light theme works correctly
- [ ] Dark theme works correctly
- [ ] Theme switching is smooth
- [ ] Theme preference is remembered

---

## Inspection Completion Record

| Check Item | Result | Issue Notes | Fix Status |
|-------|---------|---------|---------|
| Functional Testing | ✅ Pass | - | - |
| Linkage Testing | To check | - | - |
| Routing Testing | To check | - | - |
| UI Visual Testing | To check | - | - |