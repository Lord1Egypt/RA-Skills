## Description:

Self-Check performs OpenClaw environment diagnostics covering configuration, file integrity, permissions, dependencies, API token presence, and manual repair suggestions without applying fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solarise94](https://clawhub.ai/user/solarise94)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check an OpenClaw workspace before troubleshooting, after environment changes, or during routine health checks. It reports passed checks, warnings, errors, and suggested manual repair commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The diagnostic reads local OpenClaw configuration, skill metadata, logs, permissions, and API-key presence.

Mitigation: Install and run it only in workspaces where that local inspection is acceptable; the report indicates token presence without exposing token values.

Risk: Suggested repair commands may install packages, alter ownership, or start services if a user chooses to run them.

Mitigation: Review each suggested command before execution, avoid curl|bash installer patterns, and use sudo only when an ownership change is intentional.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/solarise94/skills/self-check)
- [ClawHub publisher profile](https://clawhub.ai/user/solarise94)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown diagnostic report with inline shell command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are sorted by severity and expose API token presence without printing token values.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
