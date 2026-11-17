## Description:

Rating is a command-line utility for recording rating-related entries, viewing recent activity, searching logs, and exporting locally stored data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to access a simple CLI-style rating utility that records entries, reports status and statistics, searches prior activity, and exports local data. It should be reviewed carefully before use with sensitive content because the security evidence identifies local persistent logging risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that the skill can persist sensitive prompts, customer data, proprietary text, or other input in local log files indefinitely.

Mitigation: Review before installing, avoid using it with sensitive content, and verify documented retention, deletion, and configurable data-directory behavior before routine use.

Risk: The security verdict is suspicious because the package presents as a rating tool while behaving as a broad local logging utility.

Mitigation: Limit use to real rating tasks, inspect command behavior before execution, and confirm the package narrows data capture to expected rating workflows.

## Reference(s):

- [Rating on ClawHub](https://clawhub.ai/ckchzh/skills/rating)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with inline shell commands and CLI output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command guidance and text output for a local shell utility; the underlying artifact stores command inputs and activity logs under the user's local data directory.]

## Skill Version(s):

2.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
