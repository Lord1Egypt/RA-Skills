## Description:

Semantic conversation compressor - intelligently summarize long chat history while preserving key decisions, facts, and context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chen6896qqwee](https://clawhub.ai/user/chen6896qqwee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to compress long conversation histories before context compaction or session handoff while preserving decisions, active context, tool results, and key facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation transcripts may contain sensitive information that is preserved in the compressed Markdown output.

Mitigation: Use explicit invocation and avoid processing sensitive chat histories unless the resulting local summary is acceptable to store or share.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chen6896qqwee/skills/snip-compressor)

## Skill Output:

**Output Type(s):** [Markdown, Text, Analysis]

**Output Format:** [Markdown report with Summary, Key Decisions, Active Context, Compressed Transcript, and stats sections.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Token-budgeted compressed summary generated from JSON conversation input or stdin.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
