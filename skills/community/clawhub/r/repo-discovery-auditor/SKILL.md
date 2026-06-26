---
name: repo-discovery-auditor
description: Audit an unfamiliar codebase and map architecture, user-facing features, maturity, and risks. Use when the user asks to inspect a repo, summarize the stack, explain structure, list implemented features, judge what looks mature vs rough, or prepare a coding brief from an existing project.
user-invocable: true
---

# Repo Discovery Auditor

Inspect a repo before planning or coding.

## Core workflow

1. Start with high-signal files:
   - package manager files
   - app entrypoints and route layouts
   - config files
   - backend or data client setup
   - representative feature pages or modules
2. Identify:
   - framework and runtime
   - routing model
   - state management
   - data layer and auth
   - UI system
3. Map user-facing flows page by page or feature by feature.
4. Look for maturity signals:
   - validation
   - loading and error states
   - empty states
   - access control
   - reusable abstractions
   - side-effect handling
5. Look for risk signals:
   - stale schema references
   - duplicated business logic
   - weak typing
   - inconsistent auth or role checks
   - debug code and ad-hoc branching

## Evidence rule

Tie claims to actual files or patterns you inspected.
Do not claim runtime behavior you did not verify.
If something is inferred from static code only, say so.

## Suggested output

Return results in this order when useful:

1. **Architecture summary**
2. **Key stack and structure**
3. **User-facing feature map**
4. **What looks mature**
5. **What looks rough or incomplete**
6. **Important risks or inconsistencies**
7. **Best next move**

## Maturity labels

Use simple bands:
- **mature**
- **working but rough**
- **unclear or likely incomplete**

Explain each label with concrete evidence.

## Handoff use

If the repo audit will feed implementation work, end with a short section for Codex:
- likely files to touch
- architecture constraints
- risky areas to avoid breaking
- missing information that should be confirmed first
