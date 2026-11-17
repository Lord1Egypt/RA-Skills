## Description:

Summarizes URLs, articles, YouTube videos, PDFs, and pasted text into structured digests with TL;DR, key takeaways, action items, and a worth-reading assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billyhetech](https://clawhub.ai/user/billyhetech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to quickly understand long-form or linked content, compare multiple items, and decide whether the original material is worth reading in full.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Summaries are saved locally by default, which can retain sensitive content from links, PDFs, videos, or pasted text.

Mitigation: Use the skill only with material suitable for local archiving, or disable, review, or regularly delete the archive at ~/.openclaw/summaries.

Risk: Broad auto-activation rules can summarize shared URLs or long text without clear opt-in.

Mitigation: Confirm user intent before processing confidential, regulated, or ambiguous inputs, and report inaccessible sources instead of guessing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/billyhetech/skills/smart-summarizer-v1)
- [Publisher profile](https://clawhub.ai/user/billyhetech)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Structured Markdown summary with optional saved Markdown archive file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Matches the source or requested language and includes TL;DR, key takeaways, optional action items, and a worth-reading assessment.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
