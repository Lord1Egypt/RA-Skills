## Description:

PUA Skill pushes an agent to continue stuck tasks with exhaustive, evidence-based investigation, validation, and follow-through.

This skill is ready for commercial/non-commercial use.

## Publisher:

[knifehzh](https://clawhub.ai/user/knifehzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to prompt an agent to persist through stalled debugging, implementation, or investigation work by broadening the search path, checking assumptions, and reporting objective evidence before closure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Implicit invocation may apply a more assertive troubleshooting posture without an explicit request.

Mitigation: Keep normal tool approvals, workspace boundaries, and review checkpoints in place for file reads, command execution, and user-facing conclusions.

Risk: The skill encourages persistent troubleshooting and may produce forceful guidance that is not appropriate for every task.

Mitigation: Use it for stuck technical work and review outputs for tone, relevance, and evidence before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/knifehzh/skills/pua-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text guidance, often with commands, code snippets, checklists, or structured failure reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May be invoked implicitly according to the artifact policy; no executable code is bundled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
