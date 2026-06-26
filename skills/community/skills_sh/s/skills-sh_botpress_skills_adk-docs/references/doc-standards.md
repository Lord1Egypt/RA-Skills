# ADK Documentation Standards

Standards, templates, and quality metrics for ADK documentation.

## Document Types

Choose the appropriate style based on what you're documenting:

### Reference Documentation (CLI, API endpoints)

- **Length:** 400-500 lines
- **Style:** Concise, one clear example per command/endpoint from actual project code
- **Structure:** Quick Start at top, command reference, quick reference at bottom
- **Focus:** Syntax, options, and practical workflows from real code

```markdown
# [Topic Name]

Brief introduction (1-2 sentences)

## Quick Start

5-10 line essential usage example from actual project

## Commands / Endpoints

### command-name / GET /endpoint

Brief description
**Options:** (if applicable)
**Example:** (one example from project code)

## Common Workflows

Only 3-4 workflows verified from actual project code

## Quick Reference

Command summary table or list

## See Also

Links to related docs
```

### Conceptual Guides (workflows, state management, patterns)

- **Length:** 500-700 lines
- **Style:** Examples from actual project implementations
- **Structure:** Intro, Core Concepts, Features, Quick Reference
- **Focus:** Understanding through real code patterns

### Comprehensive Guides (messages, conversations, tables)

- **Length:** 600-800 lines
- **Style:** Complete API coverage with verified examples
- **Structure:** Full TOC, Features, Patterns, Reference
- **Focus:** Complete feature coverage with real implementations

```markdown
# [Topic Name]

Brief introduction (2-3 sentences)

## Table of Contents

- Clear links to major sections
- Include subsection highlights

## Core Concepts

Basic understanding needed

## [Main Feature 1]

### Basic Usage (example from actual project code)

### Edge Cases (only if critical and seen in project)

## [Main Feature 2]

...

## Quick Reference

Essential patterns at a glance (if helpful)
```

## Quality Checklists

### All Documents

- [ ] Clear `##` and `###` headers for ripgrep
- [ ] Every concept has code example from actual project
- [ ] All examples verified in actual source locations
- [ ] Searchable section names (no vague "Advanced Topics")
- [ ] Critical distinctions highlighted (ADK vs SDK)
- [ ] File paths included for code verification
- [ ] No Common Mistakes or Best Practices sections unless user-provided

### Reference Docs (CLI, API)

- [ ] Quick Start at top with example from project
- [ ] One clear example per command/endpoint
- [ ] 3-4 workflows verified from project code
- [ ] 400-500 lines total

### Conceptual/Comprehensive Guides

- [ ] Table of contents with descriptive links
- [ ] Quick Reference section (if helpful)
- [ ] 500-800 lines depending on complexity

## Document Health Metrics

**Reference Docs (CLI, API):**

- Good: 400-500 lines, Quick Start at top, one example per command, 3-4 workflows
- Warning: >600 lines, multiple examples per command, separate best practices section

**Conceptual Guides:**

- Good: 500-700 lines, progressive examples, verified workflows
- Warning: >800 lines, vague sections, missing patterns

**All Documents:**

- Good: Every concept has code example, clear `##` headers, searchable section names
- Warning: Vague section names ("Advanced", "Other"), no table of contents

## Review Report Format

When reviewing documentation, report findings in this structure:

1. **Critical Issues** — Wrong code, broken examples, invented examples
2. **Searchability Issues** — Missing TOC, unclear headers
3. **Speculative Content** — Common mistakes without user feedback, invented best practices
4. **Missing Verification** — Examples without file path references
5. **Recommendations** — Priority improvements
