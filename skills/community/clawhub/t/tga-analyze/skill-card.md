## Description:

Logs into TGA, parses projectId and dashboardId from a dashboard URL, downloads report ZIP files, unpacks them, and analyzes XLSX reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xifengxi](https://clawhub.ai/user/xifengxi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operators with authorized TGA access use this skill to export reports from a TGA dashboard URL, unpack the downloaded ZIP, and produce structured XLSX summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses TGA credentials, browser cookies, and a cached token.

Mitigation: Install only in a trusted agent environment, keep .env and .tga-token out of source control and shared folders, restrict their file permissions, and delete the cached token when finished.

Risk: Downloaded TGA report data may be sensitive.

Mitigation: Run download commands only for reports you intend to export and store downloaded ZIP files, extracted reports, and summaries in access-controlled locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xifengxi/skills/tga-analyze)
- [TGA web application](https://tga-web.hortorgames.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Analysis]

**Output Format:** [Markdown guidance with inline shell commands and structured analysis summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a cached token file, downloaded ZIP files, extracted report directories, and XLSX-derived summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
