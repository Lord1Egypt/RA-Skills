## Description:

Yanlin Report Gen generates broker-style industry investment research daily reports in Markdown from market, macro, news, and filings JSON inputs.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[caoling7878-arch](https://clawhub.ai/user/caoling7878-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and course participants use this skill to combine four structured Yanlin data inputs into a fixed-section industry investment research daily report. The generated report is for teaching and research reference, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Markdown can carry misleading or unsafe content when source inputs or upstream collectors are untrusted.

Mitigation: Treat generated Markdown as untrusted content and review the report before sharing or relying on it.

Risk: Standalone mode imports and runs companion Yanlin skill code.

Mitigation: Use standalone mode only when the companion skills are installed from trusted sources; prefer normal mode with known JSON inputs.

Risk: The report may be mistaken for investment advice.

Mitigation: Keep the teaching/demo disclosure and investment-advice disclaimer with generated reports.

Risk: The script writes output files to a user-selected directory.

Mitigation: Run the skill with a dedicated output folder.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown report file with JSON status on stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a dated report file to the selected output directory; optional standalone mode depends on trusted companion Yanlin skills.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
