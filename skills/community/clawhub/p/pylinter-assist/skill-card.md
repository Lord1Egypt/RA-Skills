## Description:

Provides context-aware Python linting with pattern-based heuristics for reviewing GitHub pull requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[claytantor](https://clawhub.ai/user/claytantor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to lint pull requests, staged changes, diffs, or selected files with Pylint plus custom checks for secrets, FastAPI docstrings, and React hook dependency issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Detected secrets can appear in reports, PR comments, or external notifications.

Mitigation: Avoid enabling PR comments or external notifications until secret findings are redacted or the output path has been reviewed.

Risk: Unsafe file and archive handling may be risky for untrusted diffs or workflow artifacts.

Mitigation: Run the skill only on trusted repositories and reviewed workflow artifacts, and avoid untrusted diff files.

Risk: The authoritative security verdict is suspicious.

Mitigation: Audit or patch the installed snapshot before installation and before enabling CI automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/claytantor/skills/pylinter-assist)
- [README.md](README.md)
- [SKILL.md](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance]

**Output Format:** [Markdown, JSON, or plain text lint reports with optional GitHub PR comments and notification messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May exit nonzero when configured error or warning thresholds are met.]

## Skill Version(s):

0.6.3 (source: server release, SKILL.md, pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
