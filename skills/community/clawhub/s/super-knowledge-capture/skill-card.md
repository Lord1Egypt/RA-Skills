## Description:

Converts conversations, transcripts, and meeting notes into structured Notion documentation with summaries, decisions, action items, metadata, and related links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

Teams, operators, and knowledge managers use this skill to turn meeting transcripts, customer calls, architecture discussions, or interview notes into Notion pages that preserve decisions, key points, and next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting notes, transcripts, metadata, and extracted action items may be stored in a third-party Notion workspace.

Mitigation: Use an approved workspace and destination database before sending content.

Risk: A broad Notion integration token could expose or modify more workspace content than intended.

Mitigation: Use a scoped Notion integration token with only the permissions needed for the target database.

Risk: Sensitive, regulated, secret, or confidential customer content could be captured into Notion.

Mitigation: Avoid submitting such content unless the destination workspace is approved for that data.

## Reference(s):

- [Super Knowledge Capture on ClawHub](https://clawhub.ai/subaru0573/skills/super-knowledge-capture)
- [Notion API Documentation](https://developers.notion.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Structured Markdown or Notion-ready documentation with summaries, decisions, action items, and metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a scoped Notion integration token and approved target database.]

## Skill Version(s):

1.0.0 (source: release evidence and target metadata; artifact _meta.json reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
