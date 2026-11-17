## Description:

Conduct deep research on any topic and produce comprehensive reports with citations, key findings, and actionable insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dophinl](https://clawhub.ai/user/dophinl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run YouMind-powered research workflows from an agent session, producing cited reports and brief key-finding summaries saved to a YouMind board.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research prompts and generated reports are sent to and stored by YouMind.

Mitigation: Avoid confidential or sensitive topics unless external processing and storage in a YouMind board are acceptable.

Risk: The workflow can install a global npm CLI.

Mitigation: Require explicit user confirmation before installation and prefer a pinned or contained CLI installation.

Risk: Research text may be passed through shell commands.

Mitigation: Use structured JSON or stdin rather than interpolating user research text into shell command strings.

Risk: Deep research can take several minutes and relies on polling.

Mitigation: Run polling in a background task when supported, use the documented timeout, and return the report link or status clearly.

## Reference(s):

- [Setup](references/setup.md)
- [Long-Running Tasks](references/long-running-tasks.md)
- [Error Handling](references/error-handling.md)
- [YouMind](https://youmind.com?utm_source=youmind-deep-research)
- [YouMind CLI](https://www.npmjs.com/package/@youmind-ai/cli)
- [YouMind Skills Gallery](https://youmind.com/skills?utm_source=youmind-deep-research)
- [YouMind Issue Tracker](https://github.com/YouMindInc/youmind/issues)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and links to saved YouMind research reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize up to 3-5 key findings while the full cited report remains available on the user's YouMind board.]

## Skill Version(s):

1.0.0 (source: evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
