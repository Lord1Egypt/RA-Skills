---
name: test-case-design
description: This skill should be used when generating test cases, writing test cases, designing test cases, supplementing exception scenarios and boundary values, designing complex interaction test cases, or outputting standardized test cases for specific scenarios or features, such as: functional testing, compatibility testing, adaptation testing, API testing, UI visual testing, mobile/App/mini-program/H5/desktop/PC Web testing, AI Agent testing, linkage testing, or routing testing. It only focuses on writing test cases and does not involve test plans, test strategies, or automation scripts.
---

## Execution Flow

1. **Identify Test Case Type**:
   - Contains "API testing" → API test cases
   - Contains "AI agent testing"/"Agent testing"/"Agent"/"intelligent agent" → Agent test cases
   - Default → Functional test cases
2. **Load Capability Files**: Always load `references/templates/common-rules.md` (rules); select capability files by type:
   - API testing → `references/core-capabilities/api-testing.md`
   - Agent testing → `references/core-capabilities/agent-testing.md` + Part 1: Test Case Design Methods and Part 2: Test Case Quality Standards from `references/core-capabilities/functional-testing.md`
   - Functional testing → `references/core-capabilities/functional-testing.md`
3. **Load Platform-Specific Files** (skip for API testing):
   - Match platform keywords → load `references/platform/{platform}.md`
4. **Generate Test Cases**: Generate test cases according to the loaded capability files and platform-specific files
5. **Self-Check**:
   - API testing → `references/checklists/api-checklist.md`
   - Agent testing → `references/checklists/agent-checklist.md` + Section I: Functional Testing Checklist from `references/checklists/common-checklist.md`
   - Agent testing + platform → `references/checklists/agent-checklist.md` + Section I: Functional Testing Checklist from `references/checklists/common-checklist.md` + `references/checklists/{platform}-checklist.md`
   - Functional testing + platform → `references/checklists/common-checklist.md` + `references/checklists/{platform}-checklist.md`
   - Functional testing without platform → `references/checklists/common-checklist.md`
6. **Output**: Output in Markdown table format as specified in `references/examples/format-spec.md`

## Capability Boundaries
✅ Can generate: Functional testing, API testing, AI Agent testing (including Agent security & boundaries), platform-specific testing
❌ Cannot generate: Test plans, test strategies, test planning documents, penetration testing execution, vulnerability scanning, performance/stress testing (concurrency/stress/load), automation scripts

## Instruction Mapping Table

> The rules file `references/templates/common-rules.md` is always loaded. Capability files are selected by test case type; platform files are overlaid as needed.

### Capability Files

| Keyword Trigger | Load | Description |
|-----------|------|------|
| "API testing" | `references/core-capabilities/api-testing.md` | Used standalone; no platform overlay |
| "Agent testing", "Agent", "intelligent agent" | `references/core-capabilities/agent-testing.md` + Part 1: Test Case Design Methods and Part 2: Test Case Quality Standards from `references/core-capabilities/functional-testing.md` | Can overlay any platform |
| Default | `references/core-capabilities/functional-testing.md` | Functional testing |

### Platform Files (overlay on top of capability files, except for API testing)

| Keyword Trigger | Load | Description |
|-----------|------|------|
| "Mobile testing", "App testing" | `references/platform/mobile-app.md` | Gestures/interruptions/network/permissions/push/compatibility/performance |
| "Mini-program testing" | `references/platform/mini-program.md` | Lifecycle/authorization/sharing/payment/navigation/subscription |
| "Mobile Web testing", "H5 testing" | `references/platform/mobile-web.md` | Responsive/touch/browser/viewport/H5/SEO |
| "Desktop testing", "Desktop app testing" | `references/platform/desktop.md` | Window/shortcuts/files/system integration/multi-monitor |
| "PC Web testing", "Web testing" | `references/platform/pc-web.md` | Browser/layout/keyboard/forms/sessions/routing/drag-and-drop |
