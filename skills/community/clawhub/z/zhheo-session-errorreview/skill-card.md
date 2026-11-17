## Description:

When the user says "报错回顾", this skill reviews tool-call errors in the current session, analyzes root causes, deduplicates recurring issues, and updates relevant user guidance or skill files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhheo](https://clawhub.ai/user/zhheo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to review current-session tool failures, classify root causes, and maintain persistent guidance that reduces repeated operational mistakes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reviews detailed current-session tool failures, which may include sensitive command arguments, paths, or error details.

Mitigation: Limit session-history review to the needed window and redact sensitive details before sharing or persisting summaries.

Risk: The skill directs automatic persistent edits to user skill files and TOOLS.md without confirmation.

Mitigation: Require proposed diffs or explicit approval before writes, and restrict write targets to user-owned skill and workspace guidance files.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with file edits and inline command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update user skill files and TOOLS.md based on classified session errors.]

## Skill Version(s):

2.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
