# Usability Audit Checklist (Default)

> Adapted from 《易用性与用户体验专项检查项清单》
> Compatible with both Chinese and English audit workflows.

---

## 1. Navigation & Page Layout

### 1.1 Menu Hierarchy Reasonableness
- **Standard**: Menu depth ≤ 3 levels; high-frequency entries (submit, query, create) placed prominently; no deeply hidden functions
- **Check method**: Expand all menus, verify depth and prominence of key entries
- **Severity**: P0

### 1.2 Cross-Device Layout Consistency
- **Standard**: PC and mobile layouts follow same logic; core function entry positions are consistent
- **Check method**: Compare PC vs mobile screenshots of same function
- **Severity**: P1

### 1.3 Page Control Zoning Reasonableness
- **Standard**: Controls grouped clearly; query area, action buttons, and data table are visually separated; no cluttered buttons
- **Check method**: Screenshot review — check for clear visual grouping
- **Severity**: P1

### 1.4 Key Information Visual Prominence
- **Standard**: Amounts, status, error messages are visually highlighted (color, icon, font weight); core content is quickly locatable
- **Check method**: Check if status fields use color/icon differentiation
- **Severity**: P0

### 1.5 Global Search Capability
- **Standard**: Global search is available; user can quickly locate documents, functions, or dictionary data without navigating menus
- **Check method**: Look for search box in top nav or sidebar
- **Severity**: P1

---

## 2. Operation Flow Efficiency

### 2.1 Core Flow Step Minimization
- **Standard**: Core process (e.g., submit expense report) has reasonable step count; no unnecessary jumps or popups; shortest path to completion
- **Check method**: Trace a complete flow end-to-end; count steps
- **Severity**: P0

### 2.2 Quick Fill Capability
- **Standard**: Copy from previous, batch import, and template-based filling are supported to reduce duplicate data entry
- **Check method**: Look for "Copy", "Batch Import", "Use Template" buttons
- **Severity**: P1

### 2.3 Form Validation Proactiveness
- **Standard**: Required fields and format validation happen in real-time as user types; errors are not revealed only after submission
- **Check method**: Trigger validation by leaving required fields empty; check if error appears immediately
- **Severity**: P0

### 2.4 High-Frequency Operation Convenience
- **Standard**: Withdraw, save draft, batch approve, one-click print and similar high-frequency actions are easily accessible; keyboard shortcuts supported
- **Check method**: Check for batch operation checkboxes, draft save, shortcut hints
- **Severity**: P1

### 2.5 Data Linkage Auto-Fill
- **Standard**: Cross-document and cross-module data auto-populates linked fields; user does not manually re-enter the same information
- **Check method**: Test data linkage between related pages
- **Severity**: P1

---

## 3. Prompt & Copy Interaction

### 3.1 Error Message Precision
- **Standard**: Error messages clearly state the cause and provide actionable fix; no vague or generic errors
- **Check method**: Trigger various error conditions; evaluate message quality
- **Severity**: P0

### 3.2 Field Explanation Completeness
- **Standard**: Input fields, dropdowns, and special fields have hover tips or example text; domain-specific terms have plain-language explanations
- **Check method**: Check for `placeholder`, `title`, or tooltip on inputs
- **Severity**: P1

### 3.3 Operation Feedback Clarity
- **Standard**: Success/failure of operations has clear visual feedback (toast, top alert, status change); no silent failures
- **Check method**: Perform save/submit actions; verify feedback appears
- **Severity**: P0

### 3.4 Interaction Copy Uniformity
- **Standard**: Button labels and operation terms are consistent throughout the system; no ambiguous text or same-function-different-naming
- **Check method**: Compare button labels across pages for consistency
- **Severity**: P2

### 3.5 Empty State Guidance Completeness
- **Standard**: Empty pages or no-data scenarios provide guided copy and a clear next action; no blank page with no hint
- **Check method**: Check empty table / first-visit page states
- **Severity**: P0

---

## 4. Learnability & Help Guidance

### 4.1 New User Guidance Completeness
- **Standard**: First-time users see guided walkthrough or bubble hints for core flows; learning curve is reduced
- **Check method**: Log in with a fresh account; check for onboarding guide
- **Severity**: P1

### 4.2 Help System Completeness
- **Standard**: In-app help docs, video tutorials, or FAQ entry is available and searchable
- **Check method**: Look for "?" help icon, help center link
- **Severity**: P2

### 4.3 Configuration Threshold Reduction
- **Standard**: Complex configurations provide default/recommended values; user does not start from zero
- **Check method**: Open configuration pages; check for defaults and recommendations
- **Severity**: P2

### 4.4 Dictionary Search Convenience
- **Standard**: Fields, dictionaries, and codes support fuzzy search; user does not need to memorize exact codes
- **Check method**: Test search inputs with partial text
- **Severity**: P1

---

## 5. Cross-Device Consistency

### 5.1 Field & Rule Consistency
- **Standard**: Same form has identical fields, validation rules, and display content on PC and mobile
- **Check method**: Compare PC and mobile versions of same form
- **Severity**: P0

### 5.2 Mobile Adaptation Reasonableness
- **Standard**: Mobile layout adapts to screen; text and buttons are not crowded or truncated; touch targets are adequate
- **Check method**: Review mobile screenshots for layout issues
- **Severity**: P0

### 5.3 Mobile Core Operation Completeness
- **Standard**: Core mobile operations (photo upload, OCR, signature, approve/reject) are smooth and complete
- **Check method**: Test core workflows on mobile interface
- **Severity**: P1

---

## 6. Fault Tolerance & Security Experience

### 6.1 Misoperation Undo Capability
- **Standard**: Misoperations can be undone; closing page auto-saves draft; data is not lost
- **Check method**: Close page mid-edit; reopen and check for draft recovery
- **Severity**: P1

### 6.2 High-Risk Operation Confirmation
- **Standard**: Delete, void, and similar high-risk actions trigger a secondary confirmation dialog
- **Check method**: Click delete/void buttons; verify confirmation dialog appears
- **Severity**: P0

### 6.3 Upload Operation Feedback Clarity
- **Standard**: Large file uploads show progress; file size limits are explained; no silent upload failures
- **Check method**: Upload a file; check for progress indicator and size limit hints
- **Severity**: P1

### 6.4 Offline Data Protection
- **Standard**: Auto-saves entered content on network interruption; no re-entry required after reconnection
- **Check method**: Simulate network interruption during data entry
- **Severity**: P2

---

## Scoring Reference

| Severity | Meaning |
|----------|---------|
| P0 | Critical — blocks core usability, fix immediately |
| P1 | High — significantly impacts user experience |
| P2 | Medium — improvement recommended |

> To customize: copy this file, modify items, and point `checklist` in your `config.json` to your version.
