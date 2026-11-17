## Description:

Summarizes supplied documents, meetings, papers, threads, transcripts, data, and code changes while preserving claims, attribution, numbers, hedges, and omissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this agent skill to create faithful, audience-specific summaries of long or high-stakes source material. It is useful when a source must be compressed, recut for another reader or channel, audited for faithfulness, or summarized across several related inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically keeps local memory and may update shared contact or project notes.

Mitigation: Install only when stateful summarization is desired, and review proposed writes to shared contacts or project files.

Risk: Confidential transcripts, contracts, reports, or personal data may be summarized or indexed locally.

Mitigation: Disable storage where possible for sensitive sources and review any durable local notes before retaining them.

Risk: Source material may contain credentials or secrets.

Mitigation: Strip credential values before writing to disk and retain only non-secret pointers such as environment variable names or vault locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/summarizer)
- [Skill homepage](https://clawic.com/skills/summarizer)
- [Skill definition](artifact/SKILL.md)
- [Working file templates](artifact/memory-template.md)
- [Faithfulness and coverage audit](artifact/verification.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration instructions, Guidance]

**Output Format:** [Markdown or plaintext summaries, with optional local note updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist source indexes, preferences, templates, deadlines, corrections, and summaries under configured local Clawic data paths.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
