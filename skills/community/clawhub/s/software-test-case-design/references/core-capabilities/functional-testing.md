# Functional Testing

This document defines testing dimensions and strategy highlights for functional test cases, including design methods, linkage, routing, UI visual, interaction, and animation effects. Applicable to all platforms.

## Table of Contents

| Line | Section |
|------|---------|
| 20 | Part 1: Test Case Design Methods |
| 85 | Part 2: Test Case Quality Standards |
| 114 | Part 3: Linkage Testing |
| 158 | Part 4: Routing Testing |
| 213 | Part 5: UI Visual Testing |
| 299 | Part 6: Page Interaction Testing |
| 334 | Part 7: Component Interaction Testing |
| 367 | Part 8: Interactive Animation Effects Testing |

---

## Part 1: Test Case Design Methods

### 1.1 Equivalence Partitioning

**Definition**: Divide all possible input data into several equivalence classes, and select a small number of representative data from each class as test cases.

**Steps**:
1. Analyze the requirements specification to determine the set of input conditions
2. Partition valid equivalence classes (reasonable, meaningful inputs)
3. Partition invalid equivalence classes (unreasonable, meaningless inputs)
4. Number each equivalence class
5. Design test cases covering valid equivalence classes
6. Design test cases covering invalid equivalence classes

**Example**: Username input field (6-18 alphanumeric characters)
- Valid equivalence classes: 6-18 character alphanumeric combinations
- Invalid equivalence classes: fewer than 6 characters, more than 18 characters, contains special characters, null value

---

### 1.2 Boundary Value Analysis

**Definition**: Test the boundary values of inputs and outputs; errors often occur near boundaries.

**Boundary types**: Upper bound, lower bound, minimum value, maximum value, null value, first value, last value

**Example**: Password length 6-18 characters
- Boundary tests: 5 characters, 6 characters, 7 characters, 17 characters, 18 characters, 19 characters

---

### 1.3 Scenario-Based Testing

**Definition**: Design test cases by simulating user operation scenarios based on business flow diagrams.

**Scenario types**:
- Basic flow (normal process)
- Alternative flows (exception processes, branch processes)

---

### 1.4 Error Guessing

**Definition**: Based on the tester's experience and intuition, speculate on possible errors in the system and design targeted test cases.

**Common error points**: Empty input, special character input, network anomalies, duplicate operations, timeout handling

---

### 1.5 Cause-Effect Graphing

**Definition**: Analyze the relationship between input conditions (causes) and output results (effects), represent them with a cause-effect graph, and convert it into a decision table.

**Applicable scenarios**: Multiple input condition combinations with complex logical relationships

---

### 1.6 Orthogonal Array Testing

**Definition**: Use orthogonal arrays to select an appropriate, representative set of test cases from comprehensive testing.

**Applicable scenarios**: Multi-factor, multi-level combination testing

---

## Part 2: Test Case Quality Standards

### 2.1 Completeness
- Covers all functional points
- Covers normal and exception scenarios
- Covers boundary conditions

### 2.2 Accuracy
- Step descriptions are clear and unambiguous
- Expected results are explicit and verifiable
- No redundant steps

### 2.3 Executability
- Preconditions are achievable
- Steps are actionable
- Results are verifiable

### 2.4 Maintainability
- Clear structure
- Easy to understand and modify
- High reusability

### 2.5 Traceability
- Traceable to requirements
- Traceable to defects
- Clear version history

---

## Part 3: Linkage Testing

### 3.1 Form Linkage

| Test Scenario | Test Highlights |
|---------|---------|
| Province/City/District three-level linkage | Selecting a province updates the city list; selecting a city updates the district list; modifying a parent option auto-resets child options |
| Payment method linkage | Different payment methods display different form fields; switching payment methods clears previously entered data |
| Category selection linkage | Child categories reset when parent category changes; options influence each other |

### 3.2 List Linkage

| Test Scenario | Test Highlights |
|---------|---------|
| Master-detail list linkage | Selecting a master item filters the detail list display |
| Filter condition linkage | Multi-condition filters stack in real time; clearing a single condition does not affect others |
| Sort linkage | List reorders on sort change; sort state is preserved |

### 3.3 Search Linkage

| Test Scenario | Test Highlights |
|---------|---------|
| Keyword suggestions | Real-time suggestions displayed while typing; suggestions accurately match |
| Search history linkage | Recent search terms displayed; clicking a history term executes the search |
| Trending search linkage | Trending search terms displayed; clicking navigates to search results |

### 3.4 State Linkage

| Test Scenario | Test Highlights |
|---------|---------|
| Button state linkage | Submit button enabled only when form is fully filled; disabled buttons are not clickable |
| Menu state linkage | Selected menu highlighted; insufficient-permission menus hidden or disabled |
| Selection state linkage | List item selection state is correct; batch operations enabled based on selection state |

### 3.5 Data Linkage

| Test Scenario | Test Highlights |
|---------|---------|
| Real-time data sync | Multi-page data updates in real time; no manual refresh needed |
| Multi-platform data sync | Mobile and PC data consistent; data maintained when switching devices |
| Cache sync | Cache and database data consistent; cache invalidation handled correctly |

---

## Part 4: Routing Testing

### 4.1 Direct Access

| Test Scenario | Test Highlights |
|---------|---------|
| Direct access to home page | URL correct, page loads normally |
| Direct access to detail page | URL contains correct parameters, page displays correct content |
| Direct access to list page | URL parameters correctly parsed, list data correct |
| Direct access to profile page | Redirected to login page if not logged in; user info displayed if logged in |

### 4.2 Navigation Jumping

| Test Scenario | Test Highlights |
|---------|---------|
| Navigation bar click | Click navigates to correct page; current item highlighted in navigation |
| Breadcrumb navigation | Clicking breadcrumb returns to parent; breadcrumb path is correct |
| Bottom/Sidebar navigation | Bottom Tab switching; sidebar menu expand/collapse |
| Button click jump | Clicking button navigates to correct page; jump parameters correct |

### 4.3 Browser Navigation

| Test Scenario | Test Highlights |
|---------|---------|
| Browser back | Returns to previous page; page state preserved |
| Browser forward | Goes forward to next page; state preserved |
| Browser refresh | Page data refreshed; current state not lost |
| History records | URL history correctly recorded; deep links accessible |

### 4.4 Deep Links

| Test Scenario | Test Highlights |
|---------|---------|
| External link open | Opening specified page from WeChat/SMS, etc.; parameters correctly passed |
| Push notification open | Tapping push notification opens specified app page |
| Share link open | Share link correctly invokes app or opens H5 page |

### 4.5 Error Pages

| Test Scenario | Test Highlights |
|---------|---------|
| 404 page | Friendly 404 page displayed; link to return to home page provided |
| 403 page | No-permission prompt displayed; link to request permission provided |
| 500 page | Server error prompt displayed; retry button provided |

### 4.6 Route Guards

| Test Scenario | Test Highlights |
|---------|---------|
| Login verification | Unauthenticated access to pages requiring auth redirects to login page |
| Permission verification | Unauthorized access redirects to 403 page |
| Post-login redirect | After successful login, return to original page or navigate to home page |

---

## Part 5: UI Visual Testing

### 5.1 Layout Testing

| Check Item | Description |
|-------|------|
| Alignment | Elements left-aligned/centered/right-aligned correctly |
| Spacing consistency | Element spacing uniform; conforms to design specifications |
| Hierarchy | z-index levels correct; overlay layers correctly cover |
| Responsive layout | Layout correct at different screen widths; no element overflow or overlap |
| Whitespace | Page margins and element spacing appropriate |
| Visual balance | Page visual center of gravity centered or matching design intent |

### 5.2 Color Testing

| Check Item | Description |
|-------|------|
| Brand colors | Primary colors conform to brand specifications |
| Secondary colors | Secondary colors used correctly |
| Status colors | Success/failure/warning colors conform to specifications |
| Contrast | Text-to-background contrast ratio ≥ 4.5:1 |
| Theme adaptation | Light/dark theme colors correct |
| Color-blind friendly | Important information not relying solely on color distinction |

### 5.3 Font Testing

| Check Item | Description |
|-------|------|
| Font family | Correct font used; fallback fonts work correctly |
| Font size hierarchy | Title, body, and auxiliary text sizes clearly distinguished |
| Line height | Line height appropriate; text does not overlap |
| Font weight | Title/body/auxiliary font weights correct |
| Text truncation | Long text correctly truncated with ellipsis |
| Multi-language adaptation | Chinese/English font switching correct; special characters display correctly |

### 5.4 Icon Testing

| Check Item | Description |
|-------|------|
| Icon style | Icon style unified (outline/filled) |
| Icon size | Icon sizes conform to design specifications |
| Icon semantics | Icon meaning clear; no ambiguity |
| Icon states | Default/hover/click/disabled states correct |
| Icon clarity | Icons clear without blur; no distortion |

### 5.5 Image Testing

| Check Item | Description |
|-------|------|
| Image quality | Images clear without distortion; compression ratio appropriate |
| Image ratio | Different aspect ratio images display correctly; no stretching or deformation |
| Loading state | Placeholder/skeleton screen displayed during loading |
| Error state | Error placeholder displayed when image fails to load |
| Lazy loading | Above-the-fold images loaded first; below-the-fold deferred |

### 5.6 Animation Testing

| Check Item | Description |
|-------|------|
| Animation curve | Animation curves natural; intuitive |
| Animation duration | Animation duration appropriate; not too fast or too slow |
| Animation performance | Animation smooth ≥ 60fps; no stutter |
| Animation interruptible | Animations interruptible on rapid consecutive operations |
| No flickering | No visual flickering in animations |

### 5.7 Interaction State Testing

| Check Item | Description |
|-------|------|
| Default state | Element default style correct |
| Hover state | Mouse hover style correct |
| Click state | Click feedback correct |
| Disabled state | Disabled element style clearly distinct |
| Focus state | Keyboard-focused elements have clear visual indicator |

### 5.8 Multi-Theme Testing

| Check Item | Description |
|-------|------|
| Light theme | Light theme displays correctly |
| Dark theme | Dark theme displays correctly; color contrast sufficient |
| Theme switching | Theme switching smooth; no flicker |
| Theme memory | Theme setting retained after refresh |

> **Note**: Security test case design has been migrated to a standalone skill. This document no longer includes the security testing section.

## Part 6: Page Interaction Testing

### 6.1 Page Loading
- First load / refresh / weak network / offline loading
- Loading timeout handling
- Loading failure retry
- Skeleton screen display

### 6.2 Page Navigation
- Navigation bar displayed correctly
- Back button, history records
- Deep link opens page

### 6.3 Page Switching
- Tab switching / modal windows / drawers / dialogs
- Switching animation smooth
- State preservation, data refresh

### 6.4 Form Interaction
- Input field focus/blur
- Input validation, error prompts
- Autofill, input restrictions

### 6.5 List Interaction
- Pull-to-refresh, pull-up-to-load-more
- List item operations (tap, swipe, long-press)
- List sorting, filtering

### 6.6 Dialog Interaction
- Overlay layer, close button
- ESC key to close
- Multi-layer dialogs, nested dialogs

---

## Part 7: Component Interaction Testing

### 7.1 Button Component
- Normal/hover/click/disabled states
- Rapid consecutive click handling
- Loading state, permission control

### 7.2 Input Component
- Special characters, extremely long text
- Copy-paste, clear input
- Input hints, error prompts

### 7.3 Dropdown Component
- Expand/collapse, option search
- Multi-select, cascading selection
- Keyboard operation

### 7.4 Table Component
- Column sorting, data filtering
- Pagination switching, row operations
- Batch operations, table export

### 7.5 Carousel Component
- Auto/manual switching
- Indicators, infinite loop
- Pause carousel

### 7.6 Tab Component
- Click/swipe to switch
- Close tab, drag to reorder

---

## Part 8: Interactive Animation Effects Testing

### 8.1 Transition Animations
- Page switching animations
- Component appearance/disappearance
- Animations interruptible

### 8.2 Feedback Animations
- Button click ripple
- Loading spinner, success/failure feedback
- Progress bar animation

### 8.3 Gesture Animations
- List scrolling inertia
- Image zoom, drag-to-reorder
- Pull-to-refresh bounce-back, side-swipe menu

### 8.4 Performance Optimization
- Animation frame rate ≥ 60fps
- No stutter, reasonable memory usage
- GPU acceleration

---
