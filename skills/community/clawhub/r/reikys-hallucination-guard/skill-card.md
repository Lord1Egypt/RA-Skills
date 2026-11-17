## Description:

Execution-based verification guardrail with 14 check items for AI agent output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reikys](https://clawhub.ai/user/reikys)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to verify agent outputs against concrete checks for file paths, commands, syntax, URLs, package references, completeness, consistency, and overconfident claims before final reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run shell commands, URL checks, and package registry lookups during verification.

Mitigation: Use explicit target paths, prefer read-only or dry-run operation, and review commands before execution in sensitive workspaces.

Risk: The skill can guide agents to modify files while fixing failed verification checks.

Mitigation: Require approval before applying fixes and review resulting file changes before deployment.

Risk: Custom command checks from untrusted repositories could expand what the agent executes.

Mitigation: Disable arbitrary custom command checks from untrusted repositories.

## Reference(s):

- [Python ast module documentation](https://docs.python.org/3/library/ast.html)
- [npm registry API](https://registry.npmjs.org/<package-name>)
- [PyPI JSON API](https://pypi.org/pypi/<package-name>/json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown PASS/FAIL report with shell command snippets and optional JSON summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports full, quick, scoped, brief, and JSON-style report modes.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
