## Description:

Profile HTTP requests with timing, memory, and query breakdowns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to log and review HTTP profiling notes for slow routes, query behavior, middleware execution, reports, and batch endpoint analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local logs and exports may retain sensitive request details if users enter tokens, cookies, credentials, private headers, or customer data.

Mitigation: Avoid entering secrets or sensitive data, and review or delete ~/.local/share/web-profiler-bundle when retained logs or exports are no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bytesagain1/skills/web-profiler-bundle)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands; command output is stdout text with optional JSON, CSV, or TXT export files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local logs and exports under ~/.local/share/web-profiler-bundle.]

## Skill Version(s):

1.0.0 (source: evidence release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
