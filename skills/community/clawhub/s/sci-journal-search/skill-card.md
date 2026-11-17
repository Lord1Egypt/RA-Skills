## Description:

Looks up SCI journal details including XinRui/CAS-style partition rankings, JCR category partitions, Top journal status, and optional LetPub metrics by journal name, ISSN, or common abbreviation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songxf1024](https://clawhub.ai/user/songxf1024)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and academic developers use this skill to retrieve journal ranking and metric summaries during literature review, venue selection, or manuscript planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill queries external journal websites and optional LetPub mode opens a browser session.

Mitigation: Use it only in environments where outbound journal-site queries and temporary browser automation are acceptable; close or stop the browser session after LetPub parsing.

Risk: Journal rankings and metrics can change and may affect academic decision-making.

Mitigation: Verify important venue-selection decisions against the cited source sites before relying on the returned values.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/songxf1024/skills/sci-journal-search)
- [XinRui Journal Ranking](https://www.xr-scholar.com)
- [LetPub Journal Search](https://www.letpub.com.cn)
- [Partition System Reference](references/partition-system.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown-oriented text with optional JSON browser-action payloads and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May query external journal sites; optional LetPub mode asks the agent to open a browser URL and close the browser session after parsing.]

## Skill Version(s):

1.5.0 (source: server release metadata, target metadata, package.json, README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
