## Description:

When the right response mode is unclear, classify the cause-effect domain first; decompose disorder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tjboudreaux](https://clawhub.ai/user/tjboudreaux)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when approach uncertainty requires classifying a decision, incident, or subsystem into a Cynefin domain before choosing first actions. It helps an agent distinguish when to run a playbook, analyze with expertise, probe safely, stabilize first, or decompose disorder.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Misclassifying work into the wrong Cynefin domain can lead the agent to use an ineffective response mode.

Mitigation: Require cause-effect evidence, mismatch checks, and a falsifier before committing to the first actions.

Risk: Over-applying classification can delay execution when the domain and method are already agreed.

Mitigation: Use the skill only under approach uncertainty and stop once the matched action is clear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tjboudreaux/skills/thinking-cynefin)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with a structured text output template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one classification record per unit with domain, cause-effect evidence, response mode, first actions, falsifier, and optional decomposed parts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
