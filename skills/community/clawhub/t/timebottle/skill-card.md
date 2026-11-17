## Description:

Create, manage, and open time capsules that preserve a user's message for future delivery with an AI reflection on what changed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wyatt88](https://clawhub.ai/user/wyatt88)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to seal personal thoughts, decisions, wishes, or future-self letters and receive them later with a restrained reflection based on available memory context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores intimate messages and inferred context persistently.

Mitigation: Avoid secrets, regulated information, and highly sensitive personal content unless local plaintext retention is acceptable.

Risk: The skill schedules future agent activity to deliver capsules.

Mitigation: Review scheduled capsule jobs and remove or update them when deleting or changing a capsule.

Risk: The skill searches broad memory context during capsule opening.

Mitigation: Keep reflections scoped to relevant memory results and be explicit when little or no memory context is available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wyatt88/skills/timebottle)
- [Publisher profile](https://clawhub.ai/user/wyatt88)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with scheduled-agent instructions and JSON state updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores capsule records in local JSON, schedules future delivery, and may use memory search when a capsule opens.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
