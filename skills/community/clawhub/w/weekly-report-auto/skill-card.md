## Description:

Generates a weekly work report by reading current-week Markdown daily reports from a configured local WorkBuddyFile folder, deduplicating work items, and organizing summaries and next-week plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shijiezheng702-source](https://clawhub.ai/user/shijiezheng702-source)

### License/Terms of Use:

MIT-0

## Use Case:

Employees use this skill to turn local Markdown daily work reports into a weekly summary and next-week plan. It is suited for personal productivity workflows where the user controls the local report folder.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically scan the configured WorkBuddyFile folder when a weekly summary is requested.

Mitigation: Keep only intended Markdown daily reports in that folder before invoking the skill.

Risk: Weekly reports may contain sensitive work details from local daily reports.

Mitigation: Review the generated report before sharing it outside the intended audience.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shijiezheng702-source/skills/weekly-report-auto)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown weekly report with structured work summary and next-week plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Based on local Markdown daily reports in the configured WorkBuddyFile folder.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
