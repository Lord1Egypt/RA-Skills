## Description:

Requires agents to state goals, track progress, define next steps, and provide completion evidence for multi-step tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dalomeve](https://clawhub.ai/user/dalomeve)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to keep multi-step agent work from stopping at plans by requiring progress updates, explicit next steps, and completion evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make agents stricter or more verbose by requiring progress and completion evidence for multi-step work.

Mitigation: Use it where stricter task handoff is desired and keep progress updates concise.

Risk: Completion evidence can expose secrets, credentials, or sensitive task details if logged unfiltered.

Mitigation: Review generated evidence before sharing it and avoid recording secrets, credentials, or sensitive task details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dalomeve/skills/ren-wu-shou-wei-qi)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown progress updates, checklists, and evidence summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include workspace paths, URLs, command summaries, and verification results as completion evidence.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
