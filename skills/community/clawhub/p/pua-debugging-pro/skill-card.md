## Description:

Professional anti-giveup debugging protocol for coding tasks where the agent starts looping, deflecting to users, or trying to end early without evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doraemon-claw](https://clawhub.ai/user/doraemon-claw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill during repeated task failures to keep debugging evidence-first, verify before claiming completion, and escalate only after bounded checkpoints. It is suited for coding workflows where weak root-cause analysis, vague environment blame, or premature stopping would create delivery risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intentionally encourages continued debugging during repeated failures, which could waste effort if external access, secrets, or a business decision are actually required.

Mitigation: Use the documented stop conditions: complete the seven-point checklist, confirm the latest attempt produced no new diagnostic signal, and escalate only when the missing dependency is concrete.

Risk: The artifact includes Chinese-language reusable templates that may not match an English-only team workflow.

Mitigation: Review and localize the templates before deployment in teams that require English-only agent outputs.

## Reference(s):

- [Checklist & Report Templates](references/checklist-template.md)
- [Postmortem One-Pager](assets/postmortem-onepager.md)
- [ClawHub Skill Page](https://clawhub.ai/doraemon-claw/skills/pua-debugging-pro)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance, checklists, progress updates, and bounded escalation reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bilingual reusable templates; no executable files or privileged actions are included in the artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
