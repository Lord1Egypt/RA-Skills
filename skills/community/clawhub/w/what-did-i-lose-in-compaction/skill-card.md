## Description:

Helps an agent recover the important operational facts most likely to be lost after context compaction by querying the local ClawPhylax ledger and producing a MUST NOT FORGET brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aeneassoft](https://clawhub.ai/user/aeneassoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill immediately after compaction, at session resume, or before retrying a failed action to recover blocked hosts, failed actions, silent failures, unconfirmed messages, working routes, and carry-forward notes from a local ledger.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on the ClawPhylax plugin to keep and read a local ledger of agent requests and tool outcomes.

Mitigation: Review the ClawPhylax plugin before installing or enabling it, and proceed without verified ledger evidence if the plugin is unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aeneassoft/skills/what-did-i-lose-in-compaction)
- [ClawPhylax project homepage](https://github.com/aeneassoft/clawphylax)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown brief with action, evidence, do-not, next-step, and scope sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depends on the ClawPhylax local ledger plugin for verified compaction evidence; without it, the agent reports what could not be verified.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
