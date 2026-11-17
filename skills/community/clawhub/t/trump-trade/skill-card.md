## Description:

English version of the Trump RSS analysis skill. Uses trumpstruth.org/feed to track Trump's public TRUTH posts, support Evidence / Latest / Time / Watch modes, and output educational market analysis plus Trump-style replies.

This skill is for research and development only.

## Publisher:

[vialiceq](https://clawhub.ai/user/vialiceq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to summarize public TRUTH RSS posts, analyze market themes in educational scenario form, and produce evidence-backed observations without trade instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a public RSS source and may reflect incomplete or unverified source data.

Mitigation: Verify RSS source accuracy and compare against authoritative sources before relying on the output.

Risk: Educational market scenarios could be mistaken for personalized financial advice.

Mitigation: Keep outputs framed as scenario and risk discussion, avoid buy/sell instructions, and do not make trades solely from generated commentary.

Risk: Watch mode does not provide its own scheduled execution.

Mitigation: Use an external scheduler for recurring checks and treat each run as an incremental evidence summary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vialiceq/skills/trump-trade)
- [Public TRUTH RSS feed](https://www.trumpstruth.org/feed)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with evidence lists, educational market commentary, scenario sketches, observation checklists, and risk warnings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Post-related claims must be grounded in shown RSS evidence or clearly marked as summary/inference; actual recurring watch execution requires external scheduling.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
