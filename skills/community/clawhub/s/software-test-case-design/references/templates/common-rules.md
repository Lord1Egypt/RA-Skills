# Common Test Case Rules

This document defines the core specifications for test case design, including general writing rules, test type classification, priority rules, and numbering rules.

> For the test case output format, see `references/examples/format-spec.md`

## Contents

| Line | Section |
|------|------|
| 18 | 0. General Rules for Writing Test Cases |
| 37 | 1. Test Type Classification |
| 145 | 2. Priority Rules |
| 158 | 3. Test Case Numbering Rules |

---

## 0. General Rules for Writing Test Cases (mandatory for all test types)

1. **Steps must give concrete data**: test steps must directly state the concrete input values, parameters, and objects to operate on, so that testers can execute them verbatim. Descriptive language must not be used instead.
   - ❌ Not acceptable: `Enter an overly long string`, `Enter special characters`, `Enter a test attack vector`, `Fill in the required form fields`, `Send a request with wrong parameters`
   - ✅ Acceptable: `Enter ' OR '1'='1`, `Enter <script>alert(1)</script>`, `Enter username: testuser, password: Test@123456`, `Send the request with parameter name set to the empty string ""`
2. **Exception for large data**: when a test requires a large amount of input, descriptive language plus explicit parameters is allowed, and the full content does not need to be written out. Large data is defined as:
   - Text input > 1,000 characters
   - File upload > 1 MB
   - List / table data > 50 rows
   - Other scenarios clearly unsuitable for writing out in full
   - ✅ Acceptable: `Paste a text of 10,000 characters into the text box (e.g., repeat the word "test" 2,500 times)`
   - ✅ Acceptable: `Upload a 500 MB archive file (containing randomly generated data)`
   - ✅ Acceptable: `Enter a random string of 2,000 characters into the search box (can be generated with Python: "A"*2000)`
3. **One test case verifies one test point**: different scenarios (e.g., normal query, resource not found, invalid token) must be split into separate test cases.
4. **Steps and expected results correspond one-to-one**: each step is numbered separately with one action per step, and expected results are numbered the same way. Pure action steps (e.g., entering, selecting) must also have an observable concrete result, such as `The "Name" input box shows "TestData_20260101"`; vague descriptions such as "normal", "successful", or "input accepted normally" are not allowed. "Check / observe" content belongs in the expected results and is not a separate step. In API testing, setting request headers, setting the request body (or request parameters), and sending the request are separate steps and must not be merged; the expected result of a setting step is the concrete value shown in the request tool, such as `The request header shows Authorization: Bearer {{VALID_TOKEN}}`.
5. **Use placeholders for secret credentials**: use placeholders for tokens, API keys, secrets, etc., such as `{{VALID_TOKEN}}` and `{{API_KEY}}`; use obvious sample values for test accounts and passwords, such as `testuser / Test@123456`.

---

## 1. Test Type Classification

> The "Test Type" field uses the format `{Category} - {Subcategory}`; choose the category from the 10 categories below.

### 1. Functional Testing
Verify that features work as specified and that all feature points are implemented correctly.

**Subcategories**: CRUD, form validation, state transition, business rules, page interaction, component interaction

**Examples**: login, form submission, data query, list operations, state transitions

**Reference**: Parts 1, 2, 6, and 7 of `references/core-capabilities/functional-testing.md`

---

### 2. Linkage Testing
Verify data synchronization and state linkage between modules / components.

**Subcategories**: form linkage, list linkage, search linkage, state linkage, data linkage

**Examples**: province–city–district cascading, filter condition linkage, cross-page state synchronization

**Reference**: Part 3 of `references/core-capabilities/functional-testing.md`

---

### 3. Routing Testing
Verify page routing, parameter passing, and access control.

**Subcategories**: direct access, navigation, browser navigation, deep links, error pages, route guards

**Examples**: direct URL access, 404 handling, login interception

**Reference**: Part 4 of `references/core-capabilities/functional-testing.md`

---

### 4. UI Visual Testing
Verify that the interface display and visual presentation conform to the design specifications.

**Subcategories**: layout, color, typography, icons, images, animation, interaction states, multiple themes, interaction motion

**Examples**: misaligned page, inconsistent styles, choppy animation

**Reference**: Parts 5 and 8 of `references/core-capabilities/functional-testing.md`

---

### 5. Compatibility Testing
Verify that the system runs correctly in different runtime environments.

**Subcategories**: OS version compatibility, browser compatibility, device compatibility, app version compatibility

**Examples**: running on an old Android version, layout in Safari, old data still usable after upgrade

**Reference**: the corresponding platform file under `references/platform/`

---

### 6. Adaptability Testing
Verify the system's adaptation to different platform features, usage environments, and user settings.

**Subcategories**: screen size and resolution, portrait / landscape, font scaling, dark mode, language, network environment, platform interaction methods (gestures, shortcuts, windows, etc.)

**Examples**: layout after unfolding a foldable, display after enlarging the system font, loading on a weak network, pull-to-refresh gesture

**Reference**: the corresponding platform file under `references/platform/`

---

### 7. Performance Experience Testing
Verify user-perceivable performance. Only generate cases that can be observed manually or with tools; concurrency, stress, load, stability, and capacity testing are excluded.

**Subcategories**: startup / load time, operation response, smoothness, resource usage

**Examples**: slow first-screen load, choppy list scrolling, memory continuously growing after long use

---

### 8. Usability Testing
Verify the ease of use and user experience of the system, making sure it is easy to learn and use.

**Subcategories**: navigation, forms, help, accessibility

**Examples**: cumbersome operations, unclear prompts, cannot be operated with the keyboard

**Reference**: Part 6 of `references/checklists/common-checklist.md`; platform accessibility points are in the corresponding platform file under `references/platform/`

---

### 9. API Testing
Verify that the functionality, data, and exception handling of APIs conform to the API definition.

**Subcategories**: functional testing, status code verification, data validation, authentication and authorization, security testing, error handling, pagination and sorting, search and filtering, version compatibility

**Reference**: `references/core-capabilities/api-testing.md`

---

### 10. Agent Testing
Verify task execution, tool use, safety boundaries, and output quality of AI agents.

**Subcategories**: task completion, tools and memory, safety and boundaries, performance experience, content quality, knowledge base retrieval, multimodal and multilingual

**Reference**: `references/core-capabilities/agent-testing.md`

---

## 2. Priority Rules

> The case level indicates execution priority, not defect severity. When deciding, ask yourself: "If this case fails, what does it affect?"

| Level | Criteria | When to execute |
|-----|---------|---------|
| P0 - Smoke | Main flow and normal path of core features (e.g., login, ordering, payment); if it fails, the build cannot be submitted for testing or released | Must run on every test submission and release |
| P1 - High | Main negative branches of core features, normal paths of important features, data correctness | Must run in every test round |
| P2 - Medium | Secondary features, general negative cases, boundary values, compatibility / adaptability, UI display | Run during full regression |
| P3 - Low | Extreme scenarios, rare combinations, experience optimization | Run when time permits |

---

## 3. Test Case Numbering Rules

### Numbering format

```
TC_[Prefix]_[Module]_[Dimension]_[Sequence]
```

| Segment | Description | Example |
|----|------|------|
| TC | Fixed start | TC |
| Prefix | Platform or test type, see "Prefix Table" | APP, API, AGENT |
| Module | Uppercase English abbreviation of the feature module under test | LOGIN, ORDER, USER |
| Dimension | Test dimension, see "Dimension Abbreviation Tables" | FORM, GESTURE, TASK |
| Sequence | 3 digits, incrementing from 001 within the same "Prefix + Module + Dimension" | 001 |

### Prefix table

| Platform / type | Prefix |
|-----------|------|
| Mobile app | APP |
| Mini program | MP |
| Mobile web (H5) | H5 |
| Desktop | DESKTOP |
| PC Web | WEB |
| General functional testing (no platform) | FUNC |
| API testing | API |
| Agent testing | AGENT |

### Prefix selection rules

- No platform specified: functional, linkage, routing, UI, and similar cases use FUNC
- Single platform specified: all cases use that platform's prefix
- Multiple platforms specified: general functional cases use FUNC; platform-specific cases use their own platform prefixes
- Agent testing: cases about agent capabilities use AGENT; when there is a host platform, host-platform-specific cases use the platform prefix
- Agent + API: the API part uses API and the Agent part uses AGENT, with independent sequence numbers
- Supplement mode: follow the numbering style of the user's existing cases and continue from the largest sequence number; if the user's cases have no IDs, number them according to these rules

### Dimension abbreviation tables

**General dimensions**

| Dimension | Abbr. | Dimension | Abbr. |
|-----|------|-----|------|
| CRUD | CRUD | Form validation | FORM |
| List features | LIST | State transition | STATUS |
| Business rules | RULE | Linkage testing | LINKAGE |
| Routing testing | ROUTING | UI visual | UI |
| Page / component interaction | INTERACT | Interaction motion | ANIMATION |
| Negative scenarios | EXCEPTION | Boundary values | BOUNDARY |
| Data synchronization | SYNC | Performance experience | PERFORMANCE |
| Accessibility | A11Y | | |

**Platform-specific dimensions**

| Dimension | Abbr. | Dimension | Abbr. |
|-----|------|-----|------|
| Gestures | GESTURE | Screen adaptation | SCREEN |
| Interruption recovery | INTERRUPT | Network switching | NETWORK |
| Device / OS compatibility | COMPAT | Permission management | PERMISSION |
| Push notifications | PUSH | System interaction | SYSTEM |
| Storage and data | STORAGE | Updates and versions | UPDATE |
| Lifecycle | LIFECYCLE | Authorization management | AUTH |
| Sharing | SHARE | Payment | PAYMENT |
| Mini program navigation | JUMP | Subscription messages | SUBSCRIBE |
| Maps and location | MAP | Platform difference adaptation | PLATFORM |
| Browser compatibility | BROWSER | Touch interaction | TOUCH |
| Responsive layout | RESPONSIVE | Viewport configuration | VIEWPORT |
| Keyboard and input | INPUT | H5-specific features | FEATURE |
| Third-party login and payment | THIRDPARTY | WebView-specific | WEBVIEW |
| Network and cache | CACHE | SEO and sharing | SEO |
| Page layout and resolution | LAYOUT | Keyboard navigation | KEYBOARD |
| Session and authentication | SESSION | Multiple windows and tabs | TAB |
| Drag and drop | DRAG | Rich text editing | EDITOR |
| File operations | FILE | Internationalization | I18N |
| Dark mode | THEME | Printing | PRINT |
| Window management | WINDOW | Keyboard shortcuts | HOTKEY |
| System integration | INTEGRATE | Multi-monitor adaptation | MONITOR |
| Installation and updates | INSTALL | | |

**API testing dimensions**

| Dimension | Abbr. | Dimension | Abbr. |
|-----|------|-----|------|
| GET requests | GET | POST requests | POST |
| PUT/PATCH requests | PUT | DELETE requests | DELETE |
| Batch operations | BATCH | Status code verification | CODE |
| Data validation | VALID | Authentication and authorization | AUTH |
| Security testing | SEC | Error handling | ERROR |
| Pagination and sorting | PAGE | Search and filtering | SEARCH |
| Version compatibility | VERSION | | |

**Agent testing dimensions**

| Dimension | Abbr. | Dimension | Abbr. |
|-----|------|-----|------|
| Task completion | TASK | Tool calls | TOOL |
| Memory management | MEMORY | Safety and boundaries | SAFETY |
| Performance experience | PERFORMANCE | Content quality | CONTENT |
| Knowledge base retrieval | KNOWLEDGE | Multimodal | MULTIMODAL |
| Multilingual | LANG | | |

> For dimensions not in the tables, you may define your own uppercase English abbreviation of no more than 12 characters, kept consistent within the same batch of cases.

### Examples

```
TC_FUNC_DATA_CRUD_001      - General functional testing, data management module, CRUD case 1
TC_FUNC_LOGIN_FORM_002     - General functional testing, login module, form validation case 2
TC_FUNC_CITY_LINKAGE_001   - General functional testing, city selection module, linkage case 1
TC_APP_LIST_GESTURE_001    - Mobile app, list module, gesture case 1
TC_MP_SHARE_LIFECYCLE_003  - Mini program, sharing module, lifecycle case 3
TC_WEB_LOGIN_BROWSER_001   - PC Web, login module, browser compatibility case 1
TC_API_USER_GET_001        - API testing, user module, GET request case 1
TC_AGENT_FILE_TASK_001     - Agent testing, file module, task completion case 1
```
