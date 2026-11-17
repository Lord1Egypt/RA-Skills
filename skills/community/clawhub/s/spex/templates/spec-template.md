---
version: "0.1.0"
markers: "Do not remove or modify <!-- spex:begin:* --> comment lines."
description: |
  [Replace this with a brief description of the topic in English.]
  [Multiple lines (no more than 10 lines) are welcome, and each line wrapped at]
  [80 characters.]
---

<!-- spex:begin:requirement -->
# Requirement

<!-- Replace this section with requirement analysis
     based on the user's original prompt -->

<!-- spex:begin:user-clarification -->
# User Clarification

<!-- Replace this section with clarifications from
     the user on ambiguous requirements -->

<!-- spex:begin:detailed-design -->
# Detailed Design

<!-- Replace this section with detailed design based on
     analysis of the current repository architecture
     and codebase -->

<!-- spex:begin:test-plan -->
# Test Plan

<!-- Replace this section with a detailed test plan
     based on the design above -->

<!-- spex:begin:constraints -->
# Constraints

- DRY — Don't Repeat Yourself: analyze existing architecture and code,
  reuse what exists, **never** generate duplicate code.
- KISS — Keep It Simple, Stupid: no over-engineering; keep it simple while
  considering performance and security.
- Single Responsibility: each function/method does one thing; consider
  splitting if it exceeds 30 lines.
- Small Batches: break development into atomic tasks so each step is under
  200 lines of code, easy to review, cherry-pick, and revert.
- Commit Often: create a commit after each development task; follow the
  Conventional Commits format; wrap commit messages at 72 characters.
- Test Often: run lint and unit tests after each step; proceed only when
  all checks pass.
