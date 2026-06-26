# Routing Patterns

Use these examples only when the main skill is not enough.

| User intent | Route |
| --- | --- |
| "Which skill should handle this?" | `using-agent-skills-router` |
| "Build, test, review, and ship this" | `spec-plan-build-review` |
| "This touches production/secrets/release risk" | `doubt-driven-development` |
| "Just fix a typo" | Direct edit, no lifecycle |
| "Review this PR" | Code-review stance or PR review skill |

Prefer one primary route. Add a second skill only when it covers a different risk.
