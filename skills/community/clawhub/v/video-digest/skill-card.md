## Description:

Turns YouTube videos or supplied transcripts into timestamped notes in Quick, Deep, Research, Batch Quick, and Decision Card modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bonniegeng-max](https://clawhub.ai/user/bonniegeng-max)

### License/Terms of Use:

MIT

## Use Case:

External users can turn a YouTube video or supplied transcript into timestamped notes for quick screening, detailed understanding, comparison, or verification of material claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a suspicious verdict with medium confidence, including a reported unauthenticated token-request path that can run attacker-controlled JavaScript; scan coverage is incomplete.

Mitigation: Review the reported code path and scan coverage before installation, and proceed only if the behavior is acceptable for your environment.

Risk: Cookie mode can access a user's browser login, and the security guidance highlights this along with additional setup components.

Mitigation: Use cookie mode only after explicit user consent; never log, copy, or transmit cookie contents, and review optional setup components before enabling them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bonniegeng-max/skills/video-digest)
- [Output Modes](references/output-modes.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Timestamped notes with summaries, structured outlines, argument maps, quotations, and optional claim-verification tables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Notes follow the language of the request and retain timestamps for source tracing.]

## Skill Version(s):

2.2.0 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
