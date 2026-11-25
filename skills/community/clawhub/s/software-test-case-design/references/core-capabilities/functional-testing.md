# Functional Testing

This document defines the test dimensions and strategy points for functional test cases, including design methods, linkage, routing, UI visual, interaction, and motion. It applies to all platforms.

## Contents

| Line | Section |
|------|------|
| 20 | Part 1: Test Case Design Methods |
| 154 | Part 2: Test Case Quality Standards |
| 183 | Part 3: Linkage Testing |
| 227 | Part 4: Routing Testing |
| 282 | Part 5: UI Visual Testing |
| 366 | Part 6: Page Interaction Testing |
| 401 | Part 7: Component Interaction Testing |
| 434 | Part 8: Interaction Motion Testing |

---

## Part 1: Test Case Design Methods

### 1.1 Equivalence Partitioning

**Definition**: divide all possible input data into equivalence classes and select a few representative values from each class as test cases.

**Steps**:
1. Analyze the requirement specification and determine the set of input conditions
2. Identify valid equivalence classes (reasonable, meaningful inputs)
3. Identify invalid equivalence classes (unreasonable, meaningless inputs)
4. Number each equivalence class
5. Design cases covering the valid equivalence classes
6. Design cases covering the invalid equivalence classes

**Example**: username input box (6–18 letters and digits)
- Valid class: combinations of 6–18 letters and digits
- Invalid classes: fewer than 6 characters, more than 18 characters, contains special characters, empty

---

### 1.2 Boundary Value Analysis

**Definition**: test the boundary values of inputs and outputs, because errors tend to occur near boundaries.

**Boundary types**: upper bound, lower bound, minimum, maximum, empty, first value, last value

**Example**: password length 6–18 characters
- Boundary tests: 5, 6, 7, 17, 18, 19 characters

---

### 1.3 Scenario Method

**Definition**: design test cases by simulating user operation scenarios based on business flowcharts.

**Scenario types**:
- Basic flow (normal flow)
- Alternative flows (exception flows, branch flows)

---

### 1.4 Error Guessing

**Definition**: based on the tester's experience and intuition, guess where errors are likely and design targeted test cases.

**Common error points**: empty input, special characters, network exceptions, repeated operations, timeout handling

---

### 1.5 Cause-Effect Graphing

**Definition**: analyze the relationship between input conditions (causes) and output results (effects), represent it as a cause-effect graph, and convert it into a decision table.

**Applicable scenarios**: combinations of multiple input conditions with complex logical relationships (see 1.8 for how to write a decision table)

---

### 1.6 Orthogonal Array Testing

**Definition**: use orthogonal arrays to select a moderate number of representative test cases from all possible combinations.

**Applicable scenarios**: combination testing with multiple factors and multiple levels

---

### 1.7 State Transition Testing

**Definition**: based on the states of the object under test and the triggering events, build a state transition table and cover all valid and invalid transitions.

**Applicable scenarios**: orders, approvals, tickets, accounts, and other business objects with clear state transitions

**Steps**:
1. List all states of the object
2. List the events that can be triggered in each state and the transition conditions
3. Build the state transition table (current state + event → next state)
4. Design at least 1 case for each valid transition
5. For events not allowed in each state, design invalid-transition cases that verify the event is rejected and the state is unchanged
6. Design consecutive-transition cases for core business paths (e.g., Pending Payment → Paid → Shipped → Completed)

**Example**: order status

| Current state | Event | Next state |
|---------|------|---------|
| Pending Payment | Payment succeeded | Paid |
| Pending Payment | User cancels / not paid within 30 minutes | Cancelled |
| Paid | Merchant ships | Shipped |
| Shipped | User confirms receipt | Completed |

- Invalid transition: paying for an order that is "Cancelled" → shows "The order has been cancelled and cannot be paid"; the state remains "Cancelled"
- Invalid transition: when the order is "Completed", the "Cancel Order" button cannot be clicked

---

### 1.8 Decision Table Testing

**Definition**: list combinations of condition values and the corresponding actions in a table; each column (rule) corresponds to at least 1 test case.

**Applicable scenarios**: business rules with multiple conditions such as "if A and B, or if C…", e.g., discounts, shipping fees, permission combinations

**Steps**:
1. List all conditions (condition stubs) and possible actions (action stubs)
2. List all combinations of condition values (at most 2ⁿ for n binary conditions)
3. Fill in the action for each combination
4. Remove impossible combinations; merge rules with the same action where one condition's value does not affect the result
5. Design at least 1 case per rule; for range conditions, also pick values using boundary value analysis

**Example**: shipping fee rule — member orders of 99 or more are free shipping, non-member orders of 199 or more are free shipping, all others pay a 10 shipping fee

| Condition / action | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 |
|------------|-------|-------|-------|-------|-------|-------|
| Member | Yes | Yes | Yes | No | No | No |
| Order amount | < 99 | 99 – 198.99 | ≥ 199 | < 99 | 99 – 198.99 | ≥ 199 |
| Shipping fee | 10 | Free | Free | 10 | 10 | Free |

- At least 1 case per rule; boundary amounts: 98.99, 99.00, 198.99, 199.00

---

### 1.9 Negative and Boundary Supplement Points

**Applicable scenarios**: in supplement mode, or when filling gaps in existing cases, check each category in the table below for uncovered test points.

| Category | Supplement points |
|-----|---------|
| Text input | Empty, spaces only, leading / trailing spaces, minimum / maximum length and ±1, full-width / half-width, emoji, line breaks, special characters |
| Numeric input | 0, negative numbers, too many decimal places, maximum / minimum and ±1, non-numeric characters |
| Date and time | February 29 in a leap year, crossing day / month / year, start time later than end time, past / future time |
| Operation behavior | Repeated submission, rapid consecutive clicks, cancel midway, two windows modifying the same record at the same time |
| Network / service | Request timeout, network disconnected, API returns 5xx, API returns empty data |
| Permission / session | Not logged in, session expired, no permission for the operation |
| Data volume | Empty list, only 1 item, pagination boundaries (page size, page size ±1), quantity limit reached |

---

## Part 2: Test Case Quality Standards

### 2.1 Completeness
- Cover all feature points
- Cover normal and negative scenarios
- Cover boundary conditions

### 2.2 Accuracy
- Steps are clear and unambiguous
- Expected results are explicit and verifiable
- No redundant steps

### 2.3 Executability
- Preconditions are achievable
- Steps are actionable
- Results are verifiable

### 2.4 Maintainability
- Clear structure
- Easy to understand and modify
- Highly reusable

### 2.5 Traceability
- Traceable to requirements
- Traceable to defects
- Clear version history

---

## Part 3: Linkage Testing

### 3.1 Form Linkage

| Test scenario | Test points |
|---------|---------|
| Province–city–district cascading | Selecting a province updates the city list; selecting a city updates the district list; changing a parent option resets child options automatically |
| Payment method linkage | Different payment methods show different form fields; switching payment methods clears entered data |
| Category selection linkage | Child categories reset when the parent category changes; options affect each other |

### 3.2 List Linkage

| Test scenario | Test points |
|---------|---------|
| Master–detail list linkage | Selecting a master item filters the detail list |
| Filter condition linkage | Multiple filter conditions stack in real time; clearing one condition does not affect others |
| Sort linkage | The list reorders when sorting changes; sort state is retained |

### 3.3 Search Linkage

| Test scenario | Test points |
|---------|---------|
| Keyword suggestions | Suggestions appear in real time while typing; suggestions match accurately |
| Search history linkage | Recent search terms are shown; clicking a history term runs the search |
| Trending search linkage | Trending terms are shown; clicking navigates to search results |

### 3.4 State Linkage

| Test scenario | Test points |
|---------|---------|
| Button state linkage | The submit button is enabled only when the form is complete; disabled buttons cannot be clicked |
| Menu state linkage | The selected menu is highlighted; menus without permission are hidden or disabled |
| Selection state linkage | List item selection state is correct; batch operations are enabled according to the selection |

### 3.5 Data Linkage

| Test scenario | Test points |
|---------|---------|
| Real-time data sync | Data updates in real time across pages without manual refresh |
| Multi-device data sync | Data is consistent between mobile and PC; data is retained when switching devices |
| Cache sync | Cache and database are consistent; cache invalidation is handled correctly |

---

## Part 4: Routing Testing

### 4.1 Direct Access

| Test scenario | Test points |
|---------|---------|
| Direct access to the home page | URL is correct and the page loads normally |
| Direct access to a detail page | URL contains the correct parameters and the page shows the correct content |
| Direct access to a list page | URL parameters are parsed correctly and the list data is correct |
| Direct access to the user center | Redirects to login when not logged in; shows user info when logged in |

### 4.2 Navigation

| Test scenario | Test points |
|---------|---------|
| Navigation bar clicks | Clicking navigates to the correct page; the current item is highlighted |
| Breadcrumbs | Clicking a breadcrumb returns to the upper level; the breadcrumb path is correct |
| Bottom / side navigation | Switching bottom tabs; expanding and collapsing the side menu |
| Button navigation | Clicking a button navigates to the correct page; navigation parameters are correct |

### 4.3 Browser Navigation

| Test scenario | Test points |
|---------|---------|
| Browser back | Returns to the previous page; page state is retained |
| Browser forward | Goes to the next page; state is retained |
| Browser refresh | Page data refreshes; current state is not lost |
| History | URL history is recorded correctly; deep links are accessible |

### 4.4 Deep Links

| Test scenario | Test points |
|---------|---------|
| Opening from an external link | Opening a specific page from WeChat / SMS, etc.; parameters are passed correctly |
| Opening from a push notification | Tapping a push notification opens the specified page in the app |
| Opening from a share link | A share link correctly launches the app or opens the H5 page |

### 4.5 Error Pages

| Test scenario | Test points |
|---------|---------|
| 404 page | A friendly 404 page is shown with a link back to the home page |
| 403 page | Indicates no permission and provides an entry to request permission |
| 500 page | Indicates a server error and provides a retry button |

### 4.6 Route Guards

| Test scenario | Test points |
|---------|---------|
| Login check | Accessing an authenticated page when not logged in redirects to the login page |
| Permission check | Accessing without permission redirects to the 403 page |
| Redirect after login | After a successful login, returns to the original page or goes to the home page |

---

## Part 5: UI Visual Testing

### 5.1 Layout

| Check item | Description |
|-------|------|
| Alignment | Left / center / right alignment of elements is correct |
| Consistent spacing | Spacing between elements is uniform and follows the design specification |
| Layering | z-index layering is correct; overlays cover correctly |
| Responsive layout | Layout works at different screen widths; no element overflow or overlap |
| Appropriate whitespace | Page margins and element spacing are appropriate |
| Visual balance | The visual center of the page is centered or matches the design intent |

### 5.2 Color

| Check item | Description |
|-------|------|
| Brand colors | Primary colors follow the brand specification |
| Secondary colors | Secondary colors are used correctly |
| Status colors | Success / failure / warning colors follow the specification |
| Contrast | Text-to-background contrast ≥ 4.5:1 |
| Theme adaptation | Light / dark theme colors are correct |
| Color-blind friendly | Important information is not distinguished by color alone |

### 5.3 Typography

| Check item | Description |
|-------|------|
| Font family | Correct font is used; fallback fonts work |
| Font size hierarchy | Title, body, and auxiliary text sizes are clearly distinguished |
| Line height | Line height is appropriate; text does not overlap |
| Font weight | Title / body / auxiliary font weights are correct |
| Text truncation | Long text is truncated correctly with an ellipsis |
| Multilingual adaptation | Fonts work when switching between Chinese and English; special characters display correctly |

### 5.4 Icons

| Check item | Description |
|-------|------|
| Icon style | Icon style is consistent (outline / filled) |
| Icon size | Icon sizes follow the design specification |
| Icon semantics | Icon meanings are clear and unambiguous |
| Icon states | Default / hover / pressed / disabled states are correct |
| Icon clarity | Icons are sharp, not blurry or distorted |

### 5.5 Images

| Check item | Description |
|-------|------|
| Image quality | Images are clear without distortion; compression ratio is appropriate |
| Image ratio | Images of different ratios display correctly without stretching |
| Loading state | A placeholder / skeleton screen is shown while loading |
| Error state | An error placeholder is shown when an image fails to load |
| Lazy loading | First-screen images load first; others load lazily |

### 5.6 Animation

| Check item | Description |
|-------|------|
| Easing curve | Animation curves are natural and intuitive |
| Duration | Animation duration is appropriate, neither too fast nor too slow |
| Performance | Animations are smooth at ≥ 60fps without stutter |
| Interruptible | Animations can be interrupted by rapid consecutive operations |
| No flicker | Animations have no visual flicker |

### 5.7 Interaction States

| Check item | Description |
|-------|------|
| Default state | Default element styles are correct |
| Hover state | Mouse hover styles are correct |
| Pressed state | Click feedback is correct |
| Disabled state | Disabled elements are clearly distinguished |
| Focus state | Keyboard-focused elements have a clear indicator |

### 5.8 Multiple Themes

| Check item | Description |
|-------|------|
| Light theme | The light theme displays correctly |
| Dark theme | The dark theme displays correctly with sufficient contrast |
| Theme switching | Switching themes is smooth without flicker |
| Theme persistence | The theme setting is retained after refresh |

## Part 6: Page Interaction Testing

### 6.1 Page Loading
- First load / refresh / weak network / offline loading
- Loading timeout handling
- Retry after load failure
- Skeleton screen display

### 6.2 Page Navigation
- Navigation bar displays correctly
- Back button, history
- Opening pages via deep links

### 6.3 Page Switching
- Tab switching / modal windows / drawers / pop-ups
- Smooth switching animation
- State retention, data refresh

### 6.4 Form Interaction
- Input focus / blur
- Input validation, error messages
- Autofill, input restrictions

### 6.5 List Interaction
- Pull to refresh, load more on scroll
- List item actions (tap, swipe, long press)
- List sorting and filtering

### 6.6 Pop-up Interaction
- Overlay, close button
- Closing with the ESC key
- Multiple layers of pop-ups, nested pop-ups

---

## Part 7: Component Interaction Testing

### 7.1 Button Component
- Normal / hover / pressed / disabled states
- Handling rapid consecutive clicks
- Loading state, permission control

### 7.2 Input Component
- Special characters, overly long text
- Copy and paste, clearing input
- Input hints, error messages

### 7.3 Drop-down Component
- Expand / collapse, option search
- Multi-select, cascading selection
- Keyboard operation

### 7.4 Table Component
- Column sorting, data filtering
- Pagination, row actions
- Batch operations, table export

### 7.5 Carousel Component
- Automatic / manual switching
- Indicators, infinite loop
- Pausing the carousel

### 7.6 Tab Component
- Switching by tap / swipe
- Closing tabs, drag-to-reorder

---

## Part 8: Interaction Motion Testing

### 8.1 Transition Animations
- Page transition animations
- Component appear / disappear
- Interruptible animations

### 8.2 Feedback Animations
- Button click ripple
- Loading spinner, success / failure feedback
- Progress bar animation

### 8.3 Gesture Animations
- List scrolling inertia
- Image zoom, drag-to-reorder
- Pull-to-refresh bounce, side-swipe menu

### 8.4 Performance Optimization
- Animation frame rate ≥ 60fps
- No stutter, reasonable memory usage
- GPU acceleration

---
