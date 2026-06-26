# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.1.0] - 2025-03-11

### Added

#### Dynamic Budget Mechanism
- Task complexity assessment table (Simple/Medium/Complex)
- Dynamic budget allocation based on complexity:
  - Simple: ≤3 tool calls, ≤50 lines output
  - Medium: ≤6 tool calls, ≤120 lines output
  - Complex: ≤10 tool calls, ≤200 lines output
- Soft warning extension mechanism when budget runs low

#### Token Consumption Self-Check
- High-consumption behaviors checklist (avoid list)
- Self-check timing: every 3 tool calls
- Quick verification questions for L0-L2 compliance

#### L3 Pull Scenarios (Explicit)
- Clear list of 4 scenarios requiring L3 (full content) pull:
  1. Code modification needing exact indentation
  2. Config debugging with interdependent settings
  3. Error analysis needing complete stack trace
  4. User explicit request
- Decision flow diagram for L2 → L3 escalation

#### Multi-Skill Collaboration
- Priority rules when multiple skills are active
- Functional skills take precedence
- TokenKiller acts as constraint layer
- User requests override throttling rules
- Collaboration mode diagram

#### New Examples
- Example 3: Code Refactoring (Dynamic Budget) - demonstrates complexity assessment and budget warnings
- Example 4: Test Verification (Cost Ordering) - shows cheap-to-expensive verification flow
- Example 5: L3 Pull Scenarios - 3 scenarios showing when to pull full content
- Example 6: Multi-Skill Collaboration - demonstrates working with pdf skill

### Changed

- **SKILL.md**: Translated to English; restructured with new sections
- **examples.md**: Translated to English; expanded from 2 to 6 examples
- **README.md**: Updated to reflect new features; added Key Features section

### Improved

- Budget gate section now references dynamic complexity assessment
- Anti-patterns list expanded with 3 additional items
- Overall documentation structure improved for better readability

---

## [1.0.0] - 2025-03-11

### Added

- Initial release of TokenKiller skill
- Core mechanisms: budgets, gating, progressive disclosure, deduped evidence
- L0-L3 information layer system
- Workflow guidelines for search, coding, debugging, testing, docs
- Output template structure
- Trigger words for auto-enable
- 2 initial examples
- MIT-0 license