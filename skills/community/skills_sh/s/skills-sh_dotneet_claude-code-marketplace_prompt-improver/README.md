# Prompt Improver

A Claude Code skill that improves prompts by applying the official [Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices).

## What it does

This skill analyzes your prompts and transforms them into more effective versions based on proven patterns from Anthropic's internal teams and engineers using Claude Code.

When you provide a prompt, the skill outputs:

- **Improved prompt** - A rewritten version applying best practices
- **Missing information** - What additional context would make the prompt more effective
- **Improvement points** - Specific explanations of what was improved and why

## Key Best Practices Applied

The skill evaluates and improves prompts based on these core principles:

| Best Practice | What the skill checks |
|---------------|----------------------|
| **Give Claude a way to verify its work** | Does the prompt include tests, expected outputs, or success criteria? |
| **Explore first, then plan, then code** | Should Plan Mode be used for this task? |
| **Provide specific context** | Are files, constraints, and existing patterns referenced? |
| **Use subagents for investigation** | Would delegating research keep context clean? |

## Usage

Invoke the skill with `/prompt-improver` followed by your prompt:

```
/prompt-improver fix the login bug
```

Or ask Claude to improve a prompt conversationally:

```
Improve this prompt: "add tests for foo.py"
```

## Example

**Input:**
```
/prompt-improver make the dashboard look better
```

**Output:**

```markdown
## Prompt Analysis

### Original Prompt
make the dashboard look better

### Issues
- Vague instruction ("look better") - Claude cannot verify success
- No reference to existing design patterns or components
- No verification method specified

### Missing Information
- Screenshot or mockup of desired design
- Specific aspects to improve (layout, colors, typography, etc.)
- Reference to existing UI patterns in the codebase

### Improved Prompt
[paste screenshot of current dashboard] implement this updated design for the dashboard.
reference the existing component patterns in src/components/ui/.
take a screenshot of the result and compare it to the original.
list any differences and fix them.

### Improvement Points
1. Added verification method (screenshot comparison)
2. Referenced existing patterns for consistency
3. Made success criteria explicit
```

## Reference

- [Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices)
- [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works)
