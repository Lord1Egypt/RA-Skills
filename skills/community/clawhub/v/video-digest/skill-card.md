## Description:

Turns YouTube videos or supplied transcripts into timestamped Quick, Deep, or Research notes, with optional claim verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bonniegeng-max](https://clawhub.ai/user/bonniegeng-max)

### License/Terms of Use:

MIT

## Use Case:

People reviewing videos or transcripts use the skill to decide whether to watch, understand arguments through timestamped notes, compare videos, or verify selected claims against public primary sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cache behavior was not fully assessed because one cache reference could not be resolved.

Mitigation: Review the helper's cache handling and use the skill only with transcript content suitable for its temporary per-user cache.

## Reference(s):

- [Output Modes](references/output-modes.md)
- [ClawHub skill release](https://clawhub.ai/bonniegeng-max/skills/video-digest)
- [Publisher profile](https://clawhub.ai/user/bonniegeng-max)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Timestamped structured notes, with optional source links and claim-verification tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Quick, Deep, Research, or Batch Quick mode; follows the user's language.]

## Skill Version(s):

2.0.8 (source: frontmatter, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
