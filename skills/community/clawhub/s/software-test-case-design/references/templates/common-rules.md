# General Test Case Rules

This document defines the core specifications for test case design, including test type classification, priority rules, and numbering rules.

> See `references/examples/format-spec.md` for output format

## Table of Contents

| Line | Section |
|------|---------|
| 18 | 0. General Rules for Writing Test Cases |
| 34 | I. Test Type Classification |
| 99 | II. Priority Determination Rules |
| 140 | III. Test Case Numbering Rules |

---

## 0. General Rules for Writing Test Cases (mandatory for all test types)

1. **Steps must provide concrete data**: Test steps must directly provide specific input values, parameters, and operation targets so that testers can copy and execute them verbatim. Descriptive language must not be used as a substitute.
   - ❌ Unacceptable: `Enter an excessively long string`, `Enter special characters`, `Enter test attack vector`, `Fill in form required fields`, `Send request with invalid parameters`
   - ✅ Acceptable: `Enter ' OR '1'='1`, `Enter <script>alert(1)</script>`, `Enter username: testuser, password: Test@123456`, `Send request with parameter name set to empty string ""`
2. **Exception for large data**: When testing requires input of large amounts of content, descriptive language with explicit parameter specifications is permitted, without needing to write out the full content. Criteria for large data:
   - Text input > 1000 characters
   - File upload > 1MB
   - List/table data > 50 rows
   - Other scenarios clearly unsuitable for writing out in full
   - ✅ Acceptable: `Paste a 10,000-character Chinese text into the text area (can repeat "测试" 5,000 times)`
   - ✅ Acceptable: `Upload a 500MB compressed archive file (content is randomly generated data)`
   - ✅ Acceptable: `Enter a random string of 2,000 characters into the search box (can be generated with Python: "A"*2000)`

---

## I. Test Type Classification

### 1. Functional Testing
Verify that features work correctly according to requirements specifications, ensuring all function points are properly implemented.

**Sub-types**: CRUD (Create/Read/Update/Delete), Form Validation, State Transitions, Business Rules, Data Validation

**Examples**: Login functionality, Form submission, Data queries, List operations, State transitions

---

### 3. Compatibility Testing
Verify system compatibility across different environments, ensuring a consistent experience.

**Sub-types**: Platform Compatibility, Browser Compatibility, Device Compatibility, Version Compatibility

**Examples**: Adaptation across different device models, Layout across different browsers, Version upgrade compatibility

---

### 4. UI Testing
Verify that interface display and interaction are correct, ensuring a good user experience.

**Sub-types**: Layout Testing, Style Testing, Interaction Testing, Theme Testing

**Examples**: Page misalignment, Style inconsistency, Animation lag

---

### 5. Performance Testing
Verify that system performance metrics meet standards, ensuring a smooth experience.

**Sub-types**: Response Time, Concurrency Capacity, Resource Usage, Stability

**Examples**: Slow first-screen loading, Stuttering/crashing, High-concurrency crashes

---

### 6. Usability Testing
Verify system ease-of-use and user experience, ensuring it is easy to learn and use.

**Sub-types**: Navigation Testing, Form Testing, Help Testing, Accessibility

**Examples**: Cumbersome operations, Unclear prompts, Inability to use keyboard

---

### 7. Linkage Testing
Verify data synchronization and state linkage between different modules/components.

**Sub-types**: Form Linkage, List Linkage, Search Linkage, State Linkage, Data Linkage

**Examples**: Province/city/district cascading, Filter condition linkage, Cross-page state synchronization

---

### 8. Routing Testing
Verify page route navigation, parameter passing, and permission control.

**Sub-types**: Navigation Jumping, Browser Navigation, Route Parameters, Deep Links

**Examples**: Direct URL access, 404 handling, Login interception

---

## II. Priority Determination Rules

### P0 - Critical
- Core functionality
- Affects main flow
- Causes system crash
- Data loss

**Action**: Fix immediately, blocks release

---

### P1 - Major
- Important functionality
- Affects user experience
- Functional errors
- Severe UI issues

**Action**: Fix as soon as possible, affects release

---

### P2 - Minor
- Secondary functionality
- Minor experience issues
- Minor UI issues
- Inaccurate prompts

**Action**: Schedule for fix, can release with known issue

---

### P3 - Trivial
- Optimization suggestions
- UI beautification
- Does not affect functionality

**Action**: Fix when available

---

## III. Test Case Numbering Rules

### Numbering Format

```
[Platform]_[Module]_[Dimension]_[SequenceNumber]
```

### Platform Prefixes

| Platform | Prefix |
|-----|------|
| Mobile App | APP |
| Desktop | DESKTOP |
| Mini-Program | MP |
| Mobile Web | H5 |
| PC Web | WEB |
| General Functional Testing | FUNC |
| General Linkage Testing | LINKAGE |
| General Routing Testing | ROUTING |
| Agent Testing | AGENT |

### Dimension Abbreviations

| Dimension | Abbreviation |
|-----|------|
| Gesture Operations | GESTURE |
| Screen Adaptation | SCREEN |
| Interruption Recovery | INTERRUPT |
| Network Switching | NETWORK |
| Device Compatibility | COMPAT |
| Permission Management | PERMISSION |
| System Interaction | SYSTEM |
| Performance Experience | PERFORMANCE |
| Lifecycle | LIFECYCLE |
| API Testing | API |
| UI Visual | UI |
| Linkage Testing | LINKAGE |
| Routing Testing | ROUTING |
| Payment Testing | PAYMENT |
| Data Synchronization | SYNC |
| Authorization Management | AUTH |
| Browser Compatibility | BROWSER |
| Task Completion | TASK |
| Tool Invocation | TOOL |
| Memory Management | MEMORY |
| Security Boundary | SAFETY |
| Content Quality | CONTENT |
| Knowledge Base Invocation | KNOWLEDGE |

### Examples (Full Format)

```
APP_LOGIN_GESTURE_001   - Mobile app login gesture operation test case #1
APP_ORDER_NETWORK_005   - Mobile app order network switching test case #5
MP_SHARE_LIFECYCLE_003  - Mini-program sharing lifecycle test case #3
WEB_LOGIN_BROWSER_001   - PC Web login browser compatibility test case #1
LINKAGE_FORM_001        - Linkage testing form linkage test case #1
ROUTING_NAV_001         - Routing testing navigation jump test case #1
AGENT_TASK_UNDERSTAND_001 - Agent testing task understanding test case #1
```

### Simplified Format (General Test Cases)

For general test cases, a simplified format may be used:

```
TC_[TestTypePrefix]_[ScenarioKeyword]_[SequenceNumber]
```

Simplified Prefix Mapping:

| Full Prefix | Simplified Prefix | Applicable Scenario |
|---------|---------|---------|
| FUNC_CRUD | FUNC | Functional - CRUD |
| FUNC_LIST | FUNC | Functional - List |
| FUNC_FORM | FUNC | Functional - Form Validation |
| FUNC_STATUS | FUNC | Functional - State Management |
| LINKAGE | LINKAGE | Linkage Testing |
| ROUTING | ROUTING | Routing Testing |
| API | API | API Testing |
| UI | UI | UI Visual Testing |
| AGENT | AGENT | Agent Testing |

Simplified Format Examples:

```
TC_FUNC_CRUD_001     - Functional testing - Create record #1
TC_FUNC_FORM_001     - Functional testing - Form validation #1
TC_LINKAGE_CITY_001  - Linkage testing - City selection #1
TC_ROUTING_URL_001   - Routing testing - URL access #1
TC_API_GET_001       - API testing - GET request #1
TC_UI_LAYOUT_001     - UI testing - Layout alignment #1
TC_AGENT_TASK_001    - Agent testing - Task completion #1
```
