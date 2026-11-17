## Description:

Checks WeCom Smart Table weekly reports by using Puppeteer to extract structured data, applying four report-quality rules, and generating weekly and project-level summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imchen7626-create](https://clawhub.ai/user/imchen7626-create)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, team leads, and operations reviewers use this skill to extract WeCom Smart Table weekly report data and check whether member reports are complete, specific, sufficiently detailed, and varied across weeks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes WeCom weekly-report data through a persistent logged-in browser profile.

Mitigation: Run it only on a trusted machine with authorization to process the report data, avoid shared machines, and clear the persistent browser profile when finished.

Risk: The skill opens user-supplied links with Chromium sandboxing disabled.

Mitigation: Use a links file you control, allow only expected WeCom HTTPS hosts, and prefer hardening the script to run Chromium with sandboxing enabled.

## Reference(s):

- [Weekly Report Rules Detail](references/rules-detail.md)
- [ClawHub Skill Page](https://clawhub.ai/imchen7626-create/skills/smarttable-weekly-check)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON data files, and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates per-week extracted JSON files, a weekly audit report, and an optional project summary under smartsheet_data/.]

## Skill Version(s):

1.1.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
