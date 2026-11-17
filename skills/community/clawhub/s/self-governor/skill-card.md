## Description:

Self-Governor is a Chinese-language meta-decision skill that prompts an agent to choose one next action at branching points, before costly or irreversible actions, or when progress has stalled.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z1one0415](https://clawhub.ai/user/z1one0415)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add a lightweight self-governance step to multi-step agent workflows. It helps the agent pick a single next action when choices branch, a costly action is about to run, or recent steps have not improved progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The degrade_continue action can encourage progress through imperfect conditions before irreversible or public actions.

Mitigation: Review this behavior before deployment and require human confirmation where the host workflow treats publishing, deletion, or external side effects as approval-gated.

Risk: A meta-decision helper can introduce incorrect or misleading next-step guidance into an agent workflow.

Mitigation: Review and scan the Markdown-only skill before deployment, and keep the host agent responsible for final task execution.

## Reference(s):

- [Self-Governor ClawHub Skill Page](https://clawhub.ai/z1one0415/skills/self-governor)
- [Actions Reference](references/actions.md)
- [Input-Output Reference](references/input-output.md)
- [Triggers Reference](references/triggers.md)
- [Examples Reference](references/examples.md)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Text]

**Output Format:** [Structured text or JSON-like decision output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs one next_action, one short reason, and an optional fallback_if_fail.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
