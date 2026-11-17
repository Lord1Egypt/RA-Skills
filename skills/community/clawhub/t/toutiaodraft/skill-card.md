## Description:

Batch uploads user-provided content or markdown-formatted posts to the Toutiao micro-headline draft box, with optional image handling and draft saving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanlvxu](https://clawhub.ai/user/tanlvxu)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators or operators with an existing Toutiao creator login use this skill to turn direct text or markdown batches into saved micro-headline drafts, including optional image attachments, for later review and publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill operates through a logged-in Toutiao creator session and can create drafts in that account.

Mitigation: Install and run it only for accounts where the agent is allowed to create drafts; review every draft before publishing.

Risk: Image uploads may download user-provided image URLs into /tmp/openclaw/uploads.

Mitigation: Use trusted image URLs and delete temporary upload files after use when privacy matters.

Risk: Network or login state can prevent drafts from saving reliably.

Mitigation: Confirm draft creation in Toutiao after a batch run and retry only the missing entries.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tanlvxu/skills/toutiaodraft)
- [Toutiao Creator Publish Page](https://mp.toutiao.com/profile_v4/weitoutiao/publish)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown instructions and browser-action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use browser session state and temporary image files when images are included.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
